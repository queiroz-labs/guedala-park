"""Le a aparencia de cada objeto (visibilidade, transparencia, cores) direto do .FCStd, sem abrir o FreeCAD.

As cores ficam em GuiDocument.xml: cada ViewProvider aponta para um arquivo ShapeAppearance<N> dentro do zip
(lista binaria de materiais; os nomes dos arquivos sao renumerados a cada gravacao, entao se compara o CONTEUDO).
Devolve {nome: {'v': visivel, 't': transparencia %, 'c': 'RRGGBB,...' cores difusas distintas, 'h': impressao digital}}.
"""
import hashlib, io, struct, zipfile
import xml.etree.ElementTree as ET

TAM_MATERIAL = 36  # ambiente, difusa, especular, emissiva (4 bytes cada) + brilho, transparencia (float) + 12 reservados


def cores_difusas(blob):
    """Cores difusas distintas (hex RRGGBB) de um arquivo ShapeAppearance (versao 3)."""
    if len(blob) < 4:
        return []
    n = struct.unpack('<I', blob[:4])[0]
    cores, pos = [], 4
    for _ in range(n):
        reg = blob[pos:pos + 24]  # ambiente, difusa, especular, emissiva (4 B cada), brilho e transparencia (float)
        if len(reg) < 24:
            break
        hexa = '%02X%02X%02X' % (reg[5], reg[6], reg[7])  # bytes 4..7 = alfa, R, G, B da difusa
        if hexa not in cores:
            cores.append(hexa)
        pos += 24
        for _ in range(3):  # tres textos (imagem, caminho, uuid): tamanho de 4 bytes + conteudo
            if pos + 4 > len(blob):
                return cores
            pos += 4 + struct.unpack('<I', blob[pos:pos + 4])[0]
    return cores


def ler_aparencia(caminho_fcstd):
    z = zipfile.ZipFile(caminho_fcstd)
    if 'GuiDocument.xml' not in z.namelist():
        return None
    res = {}
    for _, el in ET.iterparse(io.BytesIO(z.read('GuiDocument.xml')), events=('end',)):
        if el.tag != 'ViewProvider':
            continue
        nome = el.get('name')
        vis, transp, partes, cores = None, None, [], []
        for p in el.iter('Property'):
            pn = p.get('name')
            if pn == 'Visibility':
                b = p.find('Bool')
                vis = b is not None and b.get('value') == 'true'
            elif pn == 'Transparency':
                i = p.find('Integer')
                transp = int(i.get('value')) if i is not None else None
            elif pn in ('ShapeAppearance', 'MaterialList'):
                m = p.find('MaterialList')
                if m is not None and m.get('file') in z.namelist():
                    blob = z.read(m.get('file'))
                    partes.append(blob)
                    cores += [c for c in cores_difusas(blob) if c not in cores]
            elif pn in ('ShapeMaterial', 'LineMaterial'):
                m = p.find('PropertyMaterial')
                if m is not None:
                    partes.append(('%s:%s:%s' % (pn, m.get('diffuseColor'), m.get('transparency'))).encode())
            elif pn in ('LineColor', 'PointColor'):
                c = p.find('PropertyColor')
                if c is not None:
                    partes.append(('%s:%s' % (pn, c.get('value'))).encode())
        h = hashlib.sha1(('%s|%s|' % (vis, transp)).encode() + b'|'.join(partes)).hexdigest()[:10]
        res[nome] = {'v': vis, 't': transp, 'c': ','.join(cores), 'h': h}
        el.clear()
    return res
