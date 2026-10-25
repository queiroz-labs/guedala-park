"""Pacote explícito para encaminhar: CAD canônico e fichas/documentação corrente."""
from pathlib import Path
import zipfile, json, hashlib, shutil
from plain_language import plain_html

STUDY=Path(__file__).resolve().parent
ROOT=STUDY.parent.parent
DEST=ROOT/'05_Entregas/Compartilhar_R16'
LEGACY=ROOT/'05_Entregas/Compartilhar_R14'
CASTERS='01_Projeto/Cozinha/Rodizios_gaveta_2026-10-24/'
R46='01_Projeto/Fichas_no_CAD_R46_2026-10-24/'
R48='01_Projeto/Depurador_sem_canal_R48_2026-10-24/'
R49='01_Projeto/Gavetas_escritorio_R49_2026-10-24/'
CAD=R49+'Guedala_Park_R49_Gavetas_escritorio.FCStd'
LIGHT='01_Projeto/Iluminacao/Fechamento_custo_beneficio_2026-10-24/'
VISUAL='03_Referencias/Iluminacao_CB02_2026-10-24/'
CURRENT_UPDATES=[R48+'README.md', R49+'README.md', R49+'Verificacao_R49.json', R49+'Diferencas_CAD.json', LIGHT+'Revisao_quarto_CB02.md', LIGHT+'Composicao_CB02.json', VISUAL+'Galeria.md']+[VISUAL+name for name in ['01_Quarto_economico.png','02_Cozinha_lavanderia.png','03_Sala_escritorio.png','04_Banheiro_L02.png']]
BATH='01_Projeto/Banheiro/Fechamento_pre_entrega_2026-10-24/'
BATH_FILES=['Fechamento.html','Escolhas.json','Situacao.json','Iluminacao_e_materiais.json','Luminarias_selecao_L02.html','Luminarias_selecao_L02.json','Verificacao_luminarias_L02.json','Luminarias_selecao_L01.html','Luminarias_selecao_L01.json','Hidraulica_cenarios.json','Verificacao_unioes_P19.json','P19_Unioes_nominais.csv','Consultas_tecnicas.txt','Espelheiro_P19_Unioes_NOMINAIS.FCStd']
COLORS='01_Projeto/Cores_FreeCAD_R16_2026-10-23/README.md'
COLOR_REPORTS=[str(Path(COLORS).parent/name).replace('\\','/') for name in ['Plano_de_cores.json','Verificacao_cores.json','Verificacao_geometria.json']]
FBASE='05_Entregas/Fichas_fabricacao_R13/'
PBASE='05_Entregas/Planta_cotada_R13/'

def build():
    DEST.mkdir(parents=True,exist_ok=True)
    manifest=json.loads((ROOT/FBASE/'manifest.json').read_text(encoding='utf-8'))
    paths=[CAD,COLORS]+COLOR_REPORTS+[CASTERS+name for name in ['Selecao.md','Selecao.json','Verificacao_CAD.json']]+[R46+name for name in ['README.md','Verificacao_R46.json']]+['02_Plantas_e_manuais/Planta_oficial.pdf']+[FBASE+name for name in manifest['files']]+[PBASE+name for name in ['index.html','Planta_cotada.svg','Planta_oficial.png','Cotas.json']]
    assert len(paths)==len(set(paths))
    paths += [BATH+name for name in BATH_FILES]+CURRENT_UPDATES
    assert all((ROOT/p).is_file() for p in paths)
    sha=hashlib.sha256((ROOT/CAD).read_bytes()).hexdigest()
    body=f'''<h1>Guedala Park · comece aqui</h1><p>Pacote R16 atualizado · FreeCAD R49 · cores R16 · fichas R14 · 24/10/2026.</p>
<ol><li>Extraia o ZIP inteiro para uma pasta.</li><li>No FreeCAD, escolha <strong>Arquivo → Abrir</strong> e selecione <strong>Guedala_Park_R49_Gavetas_escritorio.FCStd</strong> na pasta <code>{R49}</code>.</li><li>Para consultar medidas, ferragens e furação, abra as fichas abaixo no navegador.</li></ol>
<nav><a href="{CAD}">FreeCAD R49 · modelo atual</a><a href="{FBASE}index.html">20 fichas dos móveis</a><a href="{FBASE}Pendencias.html">Projeto, oficina e apartamento</a><a href="{FBASE}Levantamento.html">Folha de medição no apartamento</a><a href="{PBASE}index.html">Planta cotada</a><a href="{VISUAL}Galeria.md">Imagens das luminárias</a><a href="{LIGHT}Revisao_quarto_CB02.md">Iluminação econômica do quarto</a><a href="{COLORS}">Registro da atualização de cores</a><a href="https://queiroz-labs.github.io/guedala-park/">Site interativo</a><a href="https://github.com/queiroz-labs/guedala-park#readme">Menu no GitHub</a></nav>
<h2>Qual arquivo é o atual?</h2><p>O arquivo editável é a <strong>R49</strong>: gavetas do escritório com 7 mm livres sob o tampo e trava direita espelhada. Mantém a R48 com depurador sem canal de duto e divisor do aéreo D até o fundo, as cores R16, as fichas R14 e os rodízios P08. <a href="{R49}README.md">O que mudou na R49</a>; <a href="{R49}Verificacao_R49.json">verificação</a>. Use FreeCAD <strong>1.1</strong> ou versão compatível.</p>
<p>A <strong>R14 é a revisão das fichas</strong>. Na R46, cada móvel traz no FreeCAD as ferragens da ficha (propriedades <em>Ficha R14</em>), cada peça traz sua especificação de material e os 52 Minifix aparecem como marcadores laranja, sem furar as chapas. As gavetas P01/P06 mantêm a geometria Blum como envelope da FGVTN 500 selecionada, e a dobradiça piano do banco não está modelada. <a href="{R46}README.md">O que mudou na R46</a>. Os rodízios P08 são gabaritos nominais; chapa, material, altura e fixação devem ser conferidos na peça real. Não confundir a tabela de furação com programa CNC liberado.</p>
<h2>Antes de montar</h2><p>Consulte a situação de cada operação. Banco, cesto, ligações ainda sem mapa e interfaces de mecanismos têm pendências técnicas nas fichas. Medidas reais do apartamento estão em uma folha separada. Branco TX continua definido para interiores, com os padrões escolhidos nas faces aparentes.</p>
<p><a href="{BATH}Fechamento.html">Banheiro: escolhas e fechamento pré-entrega de24/10</a>. O estudo P19 contém as novas uniões nominais da caixa, em arquivo separado; os furos não estão aplicados ao principal. Beige Matt/Louro Freijó Poro e teto3000 K escolhidos. Suspensão, montagem, produtos e levantamento permanecem condicionados.</p>
<p>Os HTML, SVG e CSV deste pacote abrem localmente. Links de fabricantes e o site interativo precisam de internet. O preenchimento da folha de campo não é salvo automaticamente: imprima ou salve em PDF.</p><footer>Integridade do FreeCAD · SHA256: {sha}</footer>'''
    html='<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Guedala Park · comece aqui</title><style>body{font:16px/1.6 system-ui;color:#263f3b;background:#f7f6f2;max-width:900px;margin:auto;padding:32px}h1,h2{font-family:Georgia}nav{display:grid;gap:10px;margin:25px 0}a{color:#2c5947}nav a{background:white;border:1px solid #dbe0d6;border-radius:8px;padding:12px 16px;text-decoration:none}code{overflow-wrap:anywhere}footer{font-size:11px;border-top:1px solid #ccd7c7;padding-top:18px;overflow-wrap:anywhere}</style>'+plain_html(body)+'</html>'
    package_info={'revision':'R16','cadRevision':'R49 (R48 + gavetas do escritório corrigidas) 2026-10-24','appearanceRevision':'R16','fabricationRevision':'R14','lightingRevision':'CB02','cadPath':CAD,'cadSHA256':sha,'legacyAliases':['05_Entregas/Compartilhar_R14/Guedala_Park_R14.zip'],'files':['COMECE_AQUI.html','manifest.json']+paths,'scope':'Current FreeCAD R49: 7 mm top clearance and mirrored right locks in office drawers; R48 recirculating hood without duct channel retained. R16 appearance, R14 fabrication data and P08 casters retained. Lighting CB02 and illustrative images included. Legacy R14 ZIP URL serves this same updated R16 package.'}
    data=json.dumps(package_info,ensure_ascii=False,indent=2)
    target=DEST/'Guedala_Park_R16.zip'
    with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as archive:
        def add(name,content):
            info=zipfile.ZipInfo('Guedala_Park_R16/'+name,date_time=(2026,10,23,12,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16
            archive.writestr(info,content)
        add('COMECE_AQUI.html',html.encode('utf-8'));add('manifest.json',data.encode('utf-8'))
        for path in paths:add(path,(ROOT/path).read_bytes())
    with zipfile.ZipFile(target) as archive:
        assert archive.testzip() is None
        assert hashlib.sha256(archive.read('Guedala_Park_R16/'+CAD)).hexdigest()==sha
    (DEST/'manifest.json').write_text(data,encoding='utf-8')
    # Keep previously shared URLs working; both addresses deliver the current package.
    LEGACY.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(target,LEGACY/'Guedala_Park_R14.zip')
    shutil.copyfile(DEST/'manifest.json',LEGACY/'manifest.json')
    assert hashlib.sha256((LEGACY/'Guedala_Park_R14.zip').read_bytes()).digest()==hashlib.sha256(target.read_bytes()).digest()
    print(f'Pacote R16 atualizado: {len(package_info["files"])} arquivos; {target.stat().st_size/1024**2:.1f} MB; CAD R49, cores R16, fichas R14 e iluminação CB02.')

if __name__=='__main__':build()
