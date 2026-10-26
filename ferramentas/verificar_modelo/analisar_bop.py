"""Analisa BOP no FreeCADCmd, usando somente copias em memoria; nunca salva CAD.

GP_BOP_SAIDA substitui o destino 02_Modelo_3D/Analise_bop.json.
Compara fontes arquivadas, curvas sobre superficies, fix/removeSplitter e
booleanas de controle. Os ensaios nao aprovam fabricacao ou qualquer reparo.
"""
import collections
import hashlib
import json
import math
import os
from pathlib import Path

import FreeCAD as App
import Part

RAIZ = Path(__file__).resolve().parents[2]


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def check(s):
    try:
        s.check(True)
        return {'ok': True, 'erros': {}}
    except Exception as e:
        return {'ok': False, 'erros': dict(collections.Counter(
            line.strip() for line in str(e).splitlines() if line.strip() and line.strip() != 'No error'))}


def stats(s):
    if s.isNull():
        return {'nula': True, 'volume_mm3': 0}
    b = s.BoundBox
    return {'nula': False, 'valida': bool(s.isValid()), 'volume_mm3': float(s.Volume),
            'area_mm2': float(s.Area), 'solidos': len(s.Solids), 'faces': len(s.Faces),
            'caixa_mm': [b.XMin, b.YMin, b.ZMin, b.XMax, b.YMax, b.ZMax],
            'tolerancia_max_mm': s.getTolerance(1),
            'curvas': dict(collections.Counter(type(e.Curve).__name__ for e in s.Edges)),
            'superficies': dict(collections.Counter(type(f.Surface).__name__ for f in s.Faces)),
            'bop': check(s)}


def local(s):
    cp = s.copy()
    cp.Placement = App.Placement()
    return cp


def continuidade(s):
    rows = []
    for i, edge in enumerate(s.Edges, 1):
        c = edge.Curve
        if hasattr(c, 'getMultiplicities'):
            mult = c.getMultiplicities()
            rows.append({'aresta': i, 'grau': c.Degree, 'multiplicidades': mult,
                         'continuidade_minima_interna': c.Degree - max(mult[1:-1]) if len(mult) > 2 else None})
    return rows


def pcurvas(s):
    """Amostragem e um limite inferior do maximo, nao uma certificacao exata."""
    rows = []
    for i, edge in enumerate(s.Edges, 1):
        # O wrapper FreeCAD soma 1 ao indice antes de chamar o OCCT:
        # o indice Python e zero-based, embora o indice C++ seja one-based.
        for index in range(8):
            value = edge.curveOnSurface(index)
            if value is None:
                break
            c2d, surf, pose, first, last = value
            samples = [first + (last - first) * j / 128 for j in range(129)]
            try:
                samples.extend(t for t in edge.Curve.getKnots() if first <= t <= last)
            except AttributeError:
                pass
            maximum, at = -1., None
            for t in samples:
                uv = c2d.value(t)
                on_surface = pose.multVec(surf.value(uv.x, uv.y))
                distance = (edge.valueAt(t) - on_surface).Length
                if distance > maximum:
                    maximum, at = distance, t
            tol = edge.getTolerance(1, Part.Edge)
            rows.append({'aresta': i, 'representacao': index, 'amostras': len(samples),
                         'desvio_max_amostrado_mm': maximum, 'parametro': at,
                         'tolerancia_aresta_mm': tol, 'excede_tolerancia_na_amostra': maximum > tol})
    return rows


def particoes(s):
    """Tres cortes ortogonais centrais; nao simulam uma usinagem real."""
    bb = s.BoundBox
    low = [bb.XMin, bb.YMin, bb.ZMin]
    high = [bb.XMax, bb.YMax, bb.ZMax]
    rows = []
    for axis in range(3):
        origin = [v - 10 for v in low]
        lengths = [b - a + 20 for a, b in zip(low, high)]
        origin[axis] = (low[axis] + high[axis]) / 2
        lengths[axis] = high[axis] - origin[axis] + 10
        cutter = Part.makeBox(*lengths, App.Vector(*origin))
        try:
            inside, outside = s.common(cutter), s.cut(cutter)
            delta = inside.Volume + outside.Volume - s.Volume
            overlap = inside.common(outside).Volume
            rows.append({'eixo': 'XYZ'[axis], 'intersecao': stats(inside), 'diferenca': stats(outside),
                         'delta_volume_mm3': delta, 'sobreposicao_resultados_mm3': overlap})
        except Exception as exc:
            rows.append({'eixo': 'XYZ'[axis], 'excecao': str(exc)})
    return rows


def tratamentos(s):
    rows = {}
    for nome in ('fix', 'removeSplitter'):
        try:
            cp = s.copy()
            if nome == 'fix':
                returned = cp.fix(1e-7, 1e-7, 1e-5)
            else:
                cp, returned = cp.removeSplitter(), None
            rows[nome] = {'retorno': returned, 'forma': stats(cp), 'delta_volume_mm3': cp.Volume - s.Volume}
        except Exception as exc:
            rows[nome] = {'excecao': str(exc)}
    return rows


def comparar_fonte(raw, atual):
    # Alinhamento por translacao apenas: so e uma comparacao geometrica se
    # as orientacoes da fonte e da peca ja coincidirem. Guarda as caixas.
    a, b = local(raw), local(atual)
    ba, bb = a.BoundBox, b.BoundBox
    a.translate(App.Vector(bb.XMin - ba.XMin, bb.YMin - ba.YMin, bb.ZMin - ba.ZMin))
    result = {'fonte': stats(raw), 'alinhada_por_translacao': stats(a),
              'delta_volume_atual_menos_fonte_mm3': b.Volume - raw.Volume}
    try:
        ab, b_a = a.cut(b), b.cut(a)
        result['diferencas_orientacao_nao_certificada'] = {'fonte_menos_atual': stats(ab), 'atual_menos_fonte': stats(b_a)}
    except Exception as e:
        result['excecao_diferenca'] = str(e)
    # Controle independente do efeito de transformGeometry em uma isometria.
    mirror = App.Matrix()
    mirror.A11 = -1
    mirror.A14 = 7400
    for nome, geometrica in (('transformGeometry_espelho', True), ('transformShape_espelho', False)):
        try:
            cp = raw.copy()
            if geometrica:
                cp = cp.transformGeometry(mirror)
            else:
                cp.transformShape(mirror, True)
            result[nome] = stats(cp)
        except Exception as e:
            result[nome] = {'excecao': str(e)}
    return result


def main():
    release = json.loads((RAIZ / 'ferramentas/site/current_release.json').read_text(encoding='utf-8'))
    triagem = json.loads((RAIZ / '02_Modelo_3D/Triagem_geometria.json').read_text(encoding='utf-8'))
    modelo = RAIZ / release['cadPath']
    study = RAIZ / '03_Ambientes/Cozinha/Fischer_Grill/Grelhas_manutencao/Grelhas_Manutencao_R02.FCStd'
    base = RAIZ / '02_Modelo_3D/Base_verificacao.json.gz'
    hashes = {p: sha(p) for p in (modelo, study, base)}
    assert hashes[modelo] == release['cadSHA256'] == triagem['sha256']
    principals = [r['id'] for code in ('P06', 'P07') for r in triagem['fichas'][code] if not r['check']['ok']]
    # Escopo pedido: operacoes do projeto. Nao abrir os STEPs recebidos nem
    # repetir a analise das travas/corpos de dobradica fornecidos.
    targets = list(dict.fromkeys(principals + ['GrelhaInferiorR31']))
    detalhar = set(targets)
    result = {'schema': 1, 'modelo': release['cadPath'], 'sha256': hashes[modelo],
              'freecad': App.Version(), 'occt': Part.OCC_VERSION,
              'metodo': 'Pecas do projeto, sem analisar STEPs recebidos. Copias somente em memoria; pcurvas amostradas, nao maximos certificados; particoes sinteticas.',
              'escopo_sem_steps_recebidos': True,
              'referencias': ['https://github.com/Open-Cascade-SAS/OCCT/blob/V7_8_1/src/BOPAlgo/BOPAlgo_ArgumentAnalyzer.cxx'],
              'objetos': {}, 'fontes': {}, 'limites': ['Cortes de controle nao aprovam CNC.', 'Diferencas de fonte exigem orientacao coincidente.']}
    docs = []
    try:
        doc = App.openDocument(str(modelo), True)
        docs.append(doc)
        for name in targets:
            obj = doc.getObject(name)
            s = obj.Shape.copy()
            row = {'rotulo': obj.Label, 'fonte_declarada': str(getattr(obj, 'Fonte', '')), 'forma': stats(s)}
            if name in detalhar:
                row['continuidade_arestas'] = continuidade(s)
                row['pcurvas'] = pcurvas(s)
            if name in principals:
                row['tratamentos_em_copia'] = tratamentos(s)
                row['particoes_de_controle'] = particoes(local(s))
            result['objetos'][name] = row
            print('BOP analisado:', name, flush=True)
        source = App.openDocument(str(study), True)
        docs.append(source)
        for name in principals + ['GrelhaInferiorR31']:
            if name.endswith('R31'):
                src = source.getObject(name[:-3])
                result['fontes'][name] = comparar_fonte(src.Shape, doc.getObject(name).Shape)
    finally:
        for d in reversed(docs):
            App.closeDocument(d.Name)
    result['arquivos_inalterados'] = all(sha(p) == before for p, before in hashes.items())
    assert result['arquivos_inalterados']
    result['fontes_sha256'] = {p.relative_to(RAIZ).as_posix(): h for p, h in hashes.items()}
    output = Path(os.environ.get('GP_BOP_SAIDA', str(RAIZ / '02_Modelo_3D/Analise_bop.json')))
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Analise BOP concluida:', len(result['objetos']), 'objetos', flush=True)


main()  # FreeCADCmd importa scripts .py como modulos.
