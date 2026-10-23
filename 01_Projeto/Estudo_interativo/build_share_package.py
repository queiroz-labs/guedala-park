"""Pacote explícito para encaminhar: CAD canônico e fichas/documentação corrente."""
from pathlib import Path
import zipfile, json, hashlib
from html import escape

STUDY=Path(__file__).resolve().parent
ROOT=STUDY.parent.parent
DEST=ROOT/'05_Entregas/Compartilhar_R14'
CAD='01_Projeto/Consolidacao_R45_2026-10-23/Guedala_Park_R45_Consolidado.FCStd'
FBASE='05_Entregas/Fichas_fabricacao_R13/'
PBASE='05_Entregas/Planta_cotada_R13/'

def build():
    DEST.mkdir(parents=True,exist_ok=True)
    manifest=json.loads((ROOT/FBASE/'manifest.json').read_text(encoding='utf-8'))
    paths=[CAD,'02_Plantas_e_manuais/Planta_oficial.pdf']+[FBASE+name for name in manifest['files']]+[PBASE+name for name in ['index.html','Planta_cotada.svg','Planta_oficial.png','Cotas.json']]
    assert len(paths)==len(set(paths))
    assert all((ROOT/p).is_file() for p in paths)
    sha=hashlib.sha256((ROOT/CAD).read_bytes()).hexdigest()
    body=f'''<h1>Guedala Park · comece aqui</h1><p>Modelo FreeCAD R45 + fichas técnicas R14 · 23/10/2026.</p>
<ol><li>Extraia o ZIP inteiro para uma pasta.</li><li>No FreeCAD, escolha <strong>Arquivo → Abrir</strong> e selecione <strong>Guedala_Park_R45_Consolidado.FCStd</strong> na pasta <code>01_Projeto/Consolidacao_R45_2026-10-23</code>.</li><li>Para consultar medidas, ferragens e furação, abra as fichas abaixo no navegador.</li></ol>
<nav><a href="{CAD}">Modelo FreeCAD R45</a><a href="{FBASE}index.html">20 fichas dos móveis</a><a href="{FBASE}Pendencias.html">Projeto, oficina e apartamento</a><a href="{FBASE}Levantamento.html">Folha de medição no apartamento</a><a href="{PBASE}index.html">Planta cotada</a><a href="https://queiroz-labs.github.io/guedala-park/">Site interativo</a><a href="https://github.com/queiroz-labs/guedala-park#readme">Menu no GitHub</a></nav>
<h2>Qual arquivo é o atual?</h2><p>O arquivo editável é a consolidação <strong>R45</strong>. Foi gravado com FreeCAD <strong>1.1R20260928</strong>, conforme o próprio documento. Prefira a mesma versão ou uma versão compatível ao editar; salve as alterações em uma cópia com outro nome.</p>
<p>A <strong>R14 é a revisão das fichas</strong>. Inclui seleções de ferragens e mapas nominais de furação, mas não aplica todas essas alterações ao modelo 3D. O arquivo FreeCAD foi preservado. Não confundir a tabela de furação com programa CNC liberado.</p>
<h2>Antes de montar</h2><p>Consulte a situação de cada operação. Banco, cesto, ligações ainda sem mapa e interfaces de mecanismos têm pendências técnicas nas fichas. Medidas reais do apartamento estão em uma folha separada. Branco TX continua definido para interiores, com os padrões escolhidos nas faces aparentes.</p>
<p>Os HTML, SVG e CSV deste pacote abrem localmente. Links de fabricantes e o site interativo precisam de internet. O preenchimento da folha de campo não é salvo automaticamente: imprima ou salve em PDF.</p><footer>Integridade do FreeCAD · SHA256: {sha}</footer>'''
    html='<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Guedala Park · comece aqui</title><style>body{font:16px/1.6 system-ui;color:#263f3b;background:#f7f6f2;max-width:900px;margin:auto;padding:32px}h1,h2{font-family:Georgia}nav{display:grid;gap:10px;margin:25px 0}a{color:#2c5947}nav a{background:white;border:1px solid #dbe0d6;border-radius:8px;padding:12px 16px;text-decoration:none}code{overflow-wrap:anywhere}footer{font-size:11px;border-top:1px solid #ccd7c7;padding-top:18px;overflow-wrap:anywhere}</style>'+body+'</html>'
    package_info={'revision':'R14','cadRevision':'R45','cadPath':CAD,'cadSHA256':sha,'files':['COMECE_AQUI.html','manifest.json']+paths,'scope':'Explicit CAD and current fabrication/floorplan artifacts only.'}
    data=json.dumps(package_info,ensure_ascii=False,indent=2)
    target=DEST/'Guedala_Park_R14.zip'
    with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as archive:
        def add(name,content):
            info=zipfile.ZipInfo('Guedala_Park_R14/'+name,date_time=(2026,10,23,12,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16
            archive.writestr(info,content)
        add('COMECE_AQUI.html',html.encode('utf-8'));add('manifest.json',data.encode('utf-8'))
        for path in paths:add(path,(ROOT/path).read_bytes())
    with zipfile.ZipFile(target) as archive:
        assert archive.testzip() is None
        assert hashlib.sha256(archive.read('Guedala_Park_R14/'+CAD)).hexdigest()==sha
    (DEST/'manifest.json').write_text(data,encoding='utf-8')
    print(f'Pacote R14: {len(package_info["files"])} arquivos; {target.stat().st_size/1024**2:.1f} MB; CAD preservado.')

if __name__=='__main__':build()
