"""Biblioteca técnica explícita. Não percorre nem publica pastas privadas.

Invocado por preparar_pages.py antes do HTML; somente os arquivos da lista DOCS e ASSETS
são publicados em .site/docs. Links locais fora da seleção ficam sem navegação.
"""
from pathlib import Path
from html import escape
from urllib.parse import urlsplit, unquote, quote
import json, re, shutil, posixpath, runpy, copy
from document_library import configure as configure_library, HOME as LIBRARY_HOME
from current_release import load_release
RELEASE = load_release()

STUDY = Path(__file__).resolve().parent
ROOT = STUDY.parent.parent
R45 = '04_Moveis/Inventario_dimensional/'
CAD_COLORS = '02_Modelo_3D/Historico/Cores/'
P08_CASTERS = '03_Ambientes/Cozinha/Rodizios_gaveta/'
BATH = '03_Ambientes/Banheiro/Fechamento_pre_entrega/'
R47 = '04_Moveis/Banco_e_cesto/Fixacao_Southco/'
TAPS = '03_Ambientes/Cozinha/Conferencia_torneiras/'
R48 = '02_Modelo_3D/Historico/Depurador_sem_canal/'
R49 = '02_Modelo_3D/Historico/Gavetas_escritorio/'
LIGHT = '03_Ambientes/Iluminacao/Fechamento_custo_beneficio/'
LIGHT_IMAGES = '09_Referencias/Iluminacao_CB02/'
FABRICS = '09_Referencias/Cortinas_estofados/'
FINISHES = '09_Referencias/Tons_marcenaria/'
DOCS = []
FABRICATION = {}
GENERATED_PAGES = {}
def doc(id, title, category, rooms, status, summary, path):
    DOCS.append(dict(id=id,title=title,category=category,rooms=rooms.split(','),status=status,summary=summary,path=path))

doc('dossie','Guia do montador','Começar','all','Consolidado','Medidas, ferragens, acabamentos e pendências por módulo.','06_Entregas/Dossie_marcenaria_R45.html')
doc('pacote-compartilhar','Pacote '+RELEASE['packageRevision']+' · pacote de consulta','Começar','all',RELEASE['cadRevision']+' · '+RELEASE['releaseDate'],'FreeCAD corrente, fichas, planta, HTML offline e avanços técnicos selecionados.',RELEASE['packageDirectory']+'/'+RELEASE['packageFile'])
doc('matriz','Medidas dos 20 módulos','Medidas','all','Nominal','Vãos internos em milímetros e o que falta fechar.',R45+'Inventario/Matriz_20_modulos.md')
doc('interfaces','Uniões entre chapas','Montagem','all','Em estudo','171 contatos nominais; ligação e caminho da carga a definir.',R45+'Inventario/Interfaces_retangulares.md')
doc('fixas','Ferragens fixas e suspensão','Ferragens','all','Candidatas','Pinos, conectores, suportes e restrições de montagem.',R45+'Inventario/Ferragens_fixas.md')
doc('varoes','Varões do roupeiro','Ferragens','quarto','Em estudo','Quatro varões; oito terminais. Corte depende do suporte.',R45+'Inventario/Varoes.md')
doc('bancada','Estrutura da bancada','Montagem','escritorio','Alternativa','Bancada de 2000 × 700 × 30 mm; reforço separado em estudo.',R45+'Inventario/Bancada.md')
doc('minifix','Minifix do aéreo C','Ferragens','cozinha','Alternativa','20 conjuntos propostos para montagem fixa em chapa de 18 mm.',R45+'Inventario/Minifix_C.md')
doc('espelheiro','Pinos e prateleiras do espelheiro','Ferragens','banho','Em estudo','Oito apoios candidatos; carga da chapa e parede não liberadas.',R45+'Inventario/Espelheiro.md')
doc('gavetas','Gavetas, guias e rodízios','Ferragens','cozinha,quarto,escritorio','Em estudo','Compatibilidade, carga, engates e retirada das gavetas.',R45+'Gavetas/Resultado.html')
doc('rodizios-p08','Gaveta baixa: 6 rodas de 38 mm + espaçadores de 1 mm','Ferragens','cozinha','Selecionado','Kit Leão Aço e link de compra; apoio de 39 mm e útil de 88 mm preservados.','03_Ambientes/Cozinha/Rodizios_gaveta/Selecao.md')
doc('banheiro-fechamento','Banheiro: fechamento antes das chaves','Compatibilização','banho','R01 · 24/10','Códigos Beige Matt/Louro Freijó Poro e teto3000 K escolhidos; mapa P19, hidráulica e próximos fechamentos.',BATH+'Fechamento.html')
doc('cad-p19','FreeCAD: uniões nominais do espelheiro','FreeCAD','banho','Estudo separado','12 conjuntos Minifix nas seis interfaces da caixa; não substitui o CAD principal nem libera fabricação.',BATH+'Espelheiro_P19_Unioes_NOMINAIS.FCStd')
doc('luz-banho','Luminárias do banheiro: total e compra','Iluminação','banho','L02 · R$612,64','Espelho COB 4000 K/IRC>90 preservado; indireta 3000 K de 4,8 W/m e fontes Opus. Total dos componentes à vista, sem frete e instalação.',BATH+'Luminarias_selecao_L02.html')

doc('movento','Alternativa MOVENTO 400','Ferragens','escritorio','Alternativa','Preserva o útil; conflitos locais e retirada ainda pendentes.',R45+'Gavetas/Alternativas_escritorio/Resultado.html')
doc('portas','Portas e articulações','Ferragens','all','Em estudo','Ensaios de portas, banco e mecanismos; não é liberação executiva.',R45+'Portas_e_articulacoes/Relatorio.html')
doc('cesto','Cesto basculante','Ferragens','lavanderia','Em estudo','Frente 550 × 521 × 18; saco removível e curso até 55° preservados.',R45+'Portas_e_articulacoes/Cesto_selecao_e_esforcos.md')
doc('mesa-varal','Mesa Berlin e varal','Compatibilização','sala,lavanderia','Em estudo','Mesa pronta; quadro do varal de 1000 × 500, sem placa de ocultação.',R45+'Portas_e_articulacoes/Mesa_e_varal.md')
doc('banco','Apoios e estrutura do banco','Montagem','sala','Em estudo','Duas tampas e armazenamento preservados; apoios e ligações pendentes.',R45+'Banco_estrutura/Resultado.html')
doc('southco','Southco: registro anterior','Histórico','sala','Superado como direção P20','Registro R47 preservado. A solução operacional usa piano e trava nas fichas atuais.',R47+'Relatorio.html')
doc('batente','Batente mecânico: geometria anterior','Histórico','sala','Registro de estudo','Parada nominal de90° em estudo anterior; não é especificação atual de eixo ou montagem.',R47+'Batente_estudo.md')
doc('torneiras','Conferência de cubas e torneiras','Compatibilização','cozinha,banho','Em estudo','Envelopes e medidas disponíveis; instalação depende dos produtos.',TAPS+'Conferencia.html')
doc('purangi','Purangi: vedação e abertura','Compatibilização','banho','Não liberado','Compatibilidade integral não comprovada; troca não liberada.',TAPS+'Resultado_vedacao_abertura.md')
doc('forno','Forno: grelhas e manutenção','Compatibilização','cozinha','Em estudo','R02 dos apoios e grelhas removíveis; montagem e ventilação condicionadas.','03_Ambientes/Cozinha/Fischer_Grill/Grelhas_manutencao/README.md')
doc('cad','FreeCAD '+RELEASE['cadRevision']+' · modelo atual','FreeCAD','all',RELEASE['cadRevision']+' · '+RELEASE['releaseDate'],RELEASE['notes'],RELEASE['cadPath'])
DOCS[-1]['localOnly']=True
doc('cad-atual-notas','O que mudou na '+RELEASE['cadRevision'],'FreeCAD','all','Revisão local verificada',RELEASE['notes'],RELEASE['cadReadme'])
doc('cad-r49','O que mudou na R49','FreeCAD','escritorio','R49 · 24/10','Correções das gavetas do escritório e conferências P01, P02, P04 e P18.',R49+'README.md')
doc('cad-r48','Depurador sem canal de duto','FreeCAD','cozinha','R48 · mantida na R49','Canal removido do aéreo D e divisor levado até o fundo.',R48+'README.md')
doc('cad-cores','Atualização de cores do FreeCAD','Acabamentos','all','R16','Registro dos acabamentos visuais; cores aproximadas e limites da atualização.',CAD_COLORS+'README.md')
doc('cad-southco','FreeCAD: estudo histórico Southco','Histórico','sala','Não operacional','Arquivo R47 preservado para rastreio; não substitui a direção atual piano e trava.',R47+'Southco_Fixacao_ESTUDO.FCStd')
doc('cad-purangi','FreeCAD: sensibilidade Purangi','FreeCAD','banho','Estudo separado','Envelopes hipotéticos para conferir abertura; não é CAD certificado.',TAPS+'Purangi_R45_SENSIBILIDADE.FCStd')
doc('executivo','Pranchas executivas e plano de corte','Executivo','all','Pendente','Faltam cotas de campo, furação, fitas de borda, folgas, ligações e liberação por peça.',None)
doc('planta','Planta oficial do apartamento','Arquitetura','all','Documento de origem','Referência de planta; não substitui levantamento acabado.','09_Referencias/Plantas_e_manuais/Planta_oficial.pdf')
doc('pisos','Pisos e rodapés','Arquitetura','all','Escolhas e estudos','Acabamentos, interfaces e condições de instalação. Conferir revisão e quantitativos nas fontes.','01_Programa_e_decisoes/Pisos_e_rodapes.md')
doc('luz-quarto','Iluminação do quarto','Iluminação','quarto','Smart com Alexa/celular','Proposta Jurerê + WiZ; SKU, uso com vidro e montagem pendentes. Escolha de Elias26/10/2026.','03_Ambientes/Quarto_e_portas/Iluminacao.md')
doc('luz-economica','Quarto: revisão econômica','Iluminação','quarto','CB02 · 26/10','Quarto smart: referência parcial R$376,32; uso WiZ/Jurerê e códigos comerciais pendentes. Sem frete e instalação.',LIGHT+'Revisao_quarto_CB02.md')
doc('luz-imagens','Luminárias nos ambientes: imagens','Iluminação','all','Simulações CB02','Quarto econômico, cozinha, lavanderia, sala, escritório e banheiro. Luz e escala aproximadas.',LIGHT_IMAGES+'Galeria.md')
doc('luz-selecao','Iluminação: composição e pendências','Iluminação','all','CB01 · histórico','Seleção por ambiente; a CB02 substitui o plafon caro do quarto.',LIGHT+'Selecao_CB01.md')
doc('tecidos-escolhas','Cortinas e estofados escolhidos','Acabamentos','sala,quarto,escritorio','Areia · 24/10','Cortina da sala C2 Areia e suede areia no banco e na cabeceira; tecido claro no escritório.',FABRICS+'LEIA-ME.md')
doc('tecidos-codigos','Tecidos: códigos para amostra','Acabamentos','sala,quarto,escritorio','Candidatos comerciais','Artesanart 7260 Areia e Victor Decor 4842; confirmar amostras antes de comprar.',FABRICS+'Codigos_comerciais_2026-10-24.md')
doc('cores-escolhidas','Tons escolhidos para a marcenaria','Acabamentos','banho,escritorio','Direção aprovada','Areia e madeira natural no banheiro; marfim claro no aéreo do escritório.',FINISHES+'Escolha_aprovada_R02.md')
doc('marfim-codigo','Marfim do escritório: amostra comercial','Acabamentos','escritorio','Candidato','Guararapes Lume Matt como candidato para comparar com a direção Marfim escolhida.',FINISHES+'Pesquisa_Marfim_comercial_2026-10-24.md')
doc('instalacoes','Instalações: compatibilização executiva','Instalações','all','Pendente','Conferir em campo os pontos elétricos, hidráulicos, gás e ventilação; plantas executivas compatibilizadas ainda não reunidas.',None)
doc('levantamento','Levantamento para fabricação','Executivo','all','Pendente','Cotas acabadas, diagonais, prumo, esquadro, níveis, revestimentos e substratos de fixação precisam de levantamento.',None)
doc('acabamentos-r13','Acabamento por peça física','Acabamentos','all','Escolhido','Um padrão por chapa; peças separadas18 externa e15 interna podem ter cores distintas, com identificação e conferência do conjunto.','ferramentas/site/fabrication/Decisao_acabamentos_R13.md')
doc('planta-cotada','Planta cotada · distâncias entre paredes','Arquitetura','all','R13','Cotas oficiais por ambiente e diferenças da reconstrução identificadas.','06_Entregas/Planta_cotada/index.html')

doc('banco-atual','Banco P20: assento, apoios e operação','Montagem','sala','Condicionado','Direção piano e trava; composição, ligações e capacidade ainda dependem de detalhamento e protótipo.','04_Moveis/P20/Assento_fechado/README.md')
for item in RELEASE.get('technicalDocuments',[]):
    doc(item['id'],item['title'],item.get('category','Avanços e pendências'),item['room'],item.get('status','Estudo separado'),item['summary'],item['path'])

ASSETS = [
    'ferramentas/site/current_release.json',
    *[str(Path(RELEASE['cadReadme']).parent/n).replace('\\','/')for n in RELEASE['cadEvidence']],
    R49+'Verificacao_R49.json', R49+'Diferencas_CAD.json',
    LIGHT+'Composicao_CB01.json', LIGHT+'Composicao_CB02.json',
    '02_Modelo_3D/Historico/Fichas_no_CAD/Guedala_Park_R46_Fichas_R14.FCStd',
    BATH+'Luminarias_selecao_L02.json', BATH+'Verificacao_luminarias_L02.json',
    BATH+'Luminarias_selecao_L01.html',
    BATH+'Luminarias_selecao_L01.json',
    BATH+'Escolhas.json', BATH+'Situacao.json', BATH+'Iluminacao_e_materiais.json',
    BATH+'Hidraulica_cenarios.json', BATH+'Verificacao_unioes_P19.json',
    BATH+'P19_Unioes_nominais.csv', BATH+'Consultas_tecnicas.txt',
    P08_CASTERS+'Selecao.json',
    P08_CASTERS+'Verificacao_CAD.json',
    '02_Modelo_3D/Historico/Fichas_no_CAD/README.md',
    '02_Modelo_3D/Historico/Fichas_no_CAD/Verificacao_R46.json',
    CAD_COLORS+'Plano_de_cores.json',
    CAD_COLORS+'Verificacao_cores.json',
    CAD_COLORS+'Verificacao_geometria.json',
    '06_Entregas/Compartilhar_R16/manifest.json',
    # Compatibility aliases: previously shared R14 URL serves the current R16 ZIP.
    '06_Entregas/Compartilhar_R14/Guedala_Park_R14.zip',
    '06_Entregas/Compartilhar_R14/manifest.json',
    R45+'Guedala_Park_R45_Consolidado.FCStd',
    '06_Entregas/Planta_cotada/Planta_cotada.svg',
    '06_Entregas/Planta_cotada/Planta_oficial.png',
    '06_Entregas/Planta_cotada/Cotas.json',
    R45+'Gavetas/Alternativas_escritorio/Corte_vertical.svg',
    R45+'Gavetas/Alternativas_escritorio/Blum_MOVENTO_oficial.pdf',
    R45+'Gavetas/Alternativas_escritorio/Blum_planejamento.png',
    R45+'Gavetas/Alternativas_escritorio/Blum_vertical.png',
    R45+'Portas_e_articulacoes/Banco_abertura_frontal.svg',
    R47+'Fixacao_proposta.png', TAPS+'Cozinha_estudo.png', TAPS+'Banheiro_estudo.png',
    TAPS+'Purangi_sensibilidade.png', R45+'Inventario/Bancada_R02.png',
    '03_Ambientes/Cozinha/Fischer_Grill/Grelhas_manutencao/Grelhas_manutencao.png',
    '03_Ambientes/Cozinha/Fischer_Grill/Grelhas_manutencao/Grelhas_manutencao.svg',
]
ASSETS += [LIGHT_IMAGES+name for name in ['01_Quarto_economico.png','02_Cozinha_lavanderia.png','03_Sala_escritorio.png','04_Banheiro_L02.png']]
ASSETS += [FABRICS+name for name in ['01_Cortinas_C1_C2_C3.png','02_Estofados_E1_E2_E3.png']]
ASSETS += [FINISHES+name for name in ['04_R02_Banheiro_frentes.png','05_R02_Offwhite.png','06_R02_Madeiras.png']]
ASSETS += [p for item in RELEASE.get('technicalDocuments',[])for p in item.get('files',[])]
ASSETS += [RELEASE['packageDirectory']+'/manifest.json','06_Entregas/Compartilhar_R16/Guedala_Park_R16.zip','06_Entregas/Compartilhar_R17/Guedala_Park_R17.zip','06_Entregas/Compartilhar_R17/manifest.json',RELEASE['packageDirectory']+'/Verificacao_pacote.json']

HARDWARE = {
 'P01':['Quatro varões Ø20 nominais; oito terminais. Ø25 é alternativa, não substituição.','Trilhos e gavetas: conferir estudo de mecanismos.'],
 'P02':['Canto com referências de dobradiças; confirmar montagem e movimentos no conjunto real.'],
 'P03':['Mecanismo de correr: conferir estudo de portas.'],
 'P04':['Suspensão e ligações dos divisores ainda a dimensionar.'],
 'P05':['Duas portas; dobradiças reguláveis com amortecimento escolhidas.'],
 'P06':['FGVTN 500 candidata; capacidade publicada corrigida para 35 kg.','Engates, folgas e fixações ainda a fechar.'],
 'P07':['Inserto M4 curto nas grelhas: candidato, retenção no MDF não comprovada.'],
 'P08':['Seis rodízios Leão Aço de 38 mm, roda Ø30 × 15 mm, com seis espaçadores rígidos de 1 mm; apoio total 39 mm. Compra pendente.','Guias 3 mm com corrida 2 mm são proposta; batente removível a definir.'],
 'P09':['Dobradiças com amortecimento; suspensão e ligações a detalhar.'],
 'P10':['20 conjuntos Minifix 262.26.034 + 262.28.920 como alternativa fixa.'],
 'P11':['Suspensão, ligação da prateleira e carga a dimensionar.'],
 'P12':['Fixação do divisor e suspensão pendentes.'],
 'P13':['Apoio e fixação da chapa precisam ser demonstrados.'],
 'P14':['Pivôs, retenção, amortecimento e limitador a 55° não selecionados.','FGVTN excluiu fornecimento de mecanismo para esta aplicação.'],
 'P15':['Suspensão e ligação com fundo ou reforço ainda a definir.'],
 'P16':['FGVTN 400 e MOVENTO 400 são alternativas em estudo.','Engates, datum, retirada e interferências ainda pendentes.'],
 'P17':['Dobradiças amortecidas; suspensão e ligações ainda a dimensionar.'],
 'P18':['Referência vigente BC43 de correr; frente removível M6 em estudo.'],
 'P19':['Oito pinos Häfele 282.04.711 candidatos para duas prateleiras.'],
 'P20':['Dobradiça piano e articuladores/trava são a direção atual.','Composição, eixo real, fixação, retenção e capacidade continuam a detalhar.'],
}
EXTRA_DOCS = {'P01':['varoes','gavetas','portas'],'P02':['portas'],'P03':['portas'],'P04':['portas'],'P05':['torneiras','portas'],'P06':['gavetas'],'P07':['fixas'],'P08':['gavetas'],'P09':['portas'],'P10':['minifix','portas'],'P11':['fixas','portas'],'P12':['portas'],'P13':['fixas'],'P14':['cesto','mesa-varal'],'P15':['fixas','mesa-varal'],'P16':['gavetas','movento','bancada'],'P17':['bancada','portas'],'P18':['portas','torneiras','purangi'],'P19':['espelheiro','torneiras','purangi'],'P20':['banco-atual','mesa-varal']}
ROOMS = {**dict.fromkeys(['P01','P02','P03','P04'],'quarto'),**dict.fromkeys(['P05','P06','P07','P08','P09','P10','P11','P12','P13'],'cozinha'),'P14':'lavanderia','P15':'lavanderia','P16':'escritorio','P17':'escritorio','P18':'banho','P19':'banho','P20':'sala'}

def finish(id):
    if id in ['P09','P10','P11','P12']: return 'Guararapes Azul Petróleo escolhido. Conferir amostra, lote, faces e fita de borda.'
    if id in ['P05','P06','P07','P08','P14','P15']: return 'Greenplac Arenza escolhido como composição. Confirmar distribuição por peça, faces e fita de borda.'
    if id in ['P18','P19']: return 'Direção: bege fosco liso nas frentes e madeira clara nas laterais. Código de chapa pendente; espelheiro com frente espelhada.'
    return 'Direção: off-white fosco e madeira clara/Arenza como referência de composição. Código e distribuição por peça, amostras e bordas a definir.'

def matrix():
    rows=[]
    for line in (ROOT/R45/'Inventario/Matriz_20_modulos.md').read_text(encoding='utf-8').splitlines():
        if re.match(r'\| P\d\d \|',line):
            row=[part.strip() for part in line.strip('|').split('|')]
            rows.append(dict(zip(['id','name','measure','pending'],row)))
    assert len(rows)==20
    next(r for r in rows if r['id']=='P20')['pending']='Detalhar a composição e a fixação da dobradiça piano com articuladores/trava, eixo, apoios, almofadas e capacidade. Conferir protótipo e operação antes da fabricação.'
    return rows

STYLE='''body{font:16px/1.6 system-ui,sans-serif;color:#26322d;background:#faf9f5;max-width:1120px;margin:auto;padding:40px}h1{font-size:36px;line-height:1.15}h2{margin-top:40px}h3{margin-bottom:8px}a{color:#336d57}table{width:100%;border-collapse:collapse;font-size:14px}td,th{border-bottom:1px solid #d8dfd8;padding:10px;text-align:left;vertical-align:top}th{background:#e8eee7}section{padding:20px 0;border-bottom:1px solid #d8dfd8}.note{padding:18px;background:#edf1e9;border-radius:10px}.meta{font-size:13px;color:#607066}.tags{display:flex;gap:12px;flex-wrap:wrap}button{padding:10px 18px;border:1px solid #667767;border-radius:8px;background:white;cursor:pointer}@media print{body{background:white;padding:0;font-size:10pt}h1{font-size:24pt}.no-print{display:none}section{break-inside:avoid}a{color:inherit;text-decoration:none}table{font-size:9pt}h2,h3{break-after:avoid}}'''
def page(title,body): return '<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+escape(title)+'</title><style>'+STYLE+'</style><main>'+body+'</main></html>'
def inline(text):
    text=escape(text)
    text=re.sub(r'!\[([^\]]*)\]\(([^)]+)\)',lambda m:'<img alt="'+m[1]+'" src="'+m[2]+'" style="max-width:100%;height:auto">',text)
    text=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',lambda m:'<a href="'+m[2]+'">'+m[1]+'</a>',text)
    text=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',text)
    return re.sub(r'`([^`]+)`',r'<code>\1</code>',text)
def markdown(text):
    out=[]; in_table=False
    for line in text.splitlines():
        if line.startswith('|'):
            cells=[c.strip() for c in line.strip('|').split('|')]
            if all(re.fullmatch(r'[-: ]+',c or '-') for c in cells): continue
            if not in_table: out.append('<table>'); in_table=True
            out.append('<tr>'+''.join('<td>'+inline(c)+'</td>' for c in cells)+'</tr>'); continue
        if in_table: out.append('</table>'); in_table=False
        match=re.match(r'^(#{1,6}) (.*)',line)
        if match: out.append(f'<h{len(match[1])}>'+inline(match[2])+f'</h{len(match[1])}>')
        elif line.strip(): out.append('<p>'+inline(line)+'</p>')
    if in_table: out.append('</table>')
    return '\n'.join(out)

def write_if_changed(path,content):
    data=content.replace('\r\n','\n').encode('utf8')
    if path.exists() and path.read_bytes()==data:return False
    path.write_bytes(data);return True


def write_sources():
    from plain_language import plain_data
    rows=matrix()
    EXTRA_DOCS['P07']=['forno','fixas']
    EXTRA_DOCS['P08']=['rodizios-p08','gavetas','cad']
    EXTRA_DOCS['P18']=['banheiro-fechamento','luz-banho','portas','torneiras','purangi']
    EXTRA_DOCS['P19']=['banheiro-fechamento','luz-banho','cad-p19','espelheiro','portas','torneiras','purangi']
    guidance={r['id']:dict(hardware=HARDWARE[r['id']],pending=[r['pending'],'Conferir medidas de campo, material efetivo, bordas, furação e ligações antes do corte.'],finish=finish(r['id']),documentIds=list(dict.fromkeys(['matriz','fixas']+EXTRA_DOCS[r['id']]))) for r in rows}
    for code,f in FABRICATION.items():
        guidance[code].update(fabrication=f,finish=f['finishSummary'],pending=f['technicalChecks'])
        guidance[code]['hardware']=[r['item']+': '+str(r.get('reference') or 'definição específica na ficha')+' · '+r['status'] for r in f['hardwareRows']]
        guidance[code]['documentIds'].insert(0,'ficha-'+code)
        guidance[code]['documentIds'].append('acabamentos-r13')
    # Estudos publicados em separado, acessiveis tambem pela ficha de cada movel.
    for code in ['P17','P12']:
        guidance[code]['documentIds'].append('suspensao-'+code.lower())
        guidance[code]['hardware'].append('Suspensão compacta candidata: implantação nominal; ferragem, fixadores e capacidade ainda em qualificação.')
        guidance[code]['pending'].insert(0,'Conferir ferramenta do auxiliar traseiro, juntas/rigidez da caixa e contato inferior; executar qualificação física antes de adotar a suspensão.')
    config=RELEASE['documentLibrary']
    for code,g in guidance.items():
        g['documentIds']=list(dict.fromkeys(['ficha-'+code]+config['moduleStudies'][code]+['furacao-pecas','acabamentos-r13']))
    guidance = plain_data(guidance)
    write_if_changed(STUDY/'src/workshop-docs.js','/* Fontes explícitas. Conferir as medidas antes de fabricar. */\nconst WORKSHOP_DOCS = '+json.dumps(DOCS,ensure_ascii=False,separators=(',',':'))+';\nconst MODULE_GUIDANCE = '+json.dumps(guidance,ensure_ascii=False,indent=2)+';\nfunction WORKSHOP_DOC_URL(doc){return doc.path ? "docs/"+doc.path+(doc.path.endsWith(".md") ? ".html" : "") : null;}\n')
    body='<h1>Guia do montador</h1><p>Modelo '+escape(RELEASE['cadRevision'])+'; consultar fichas e condições atuais antes da fabricação.</p>'
    if FABRICATION:
        body='<p class="meta">GUEDALA PARK · MARCENARIA · FICHAS R15</p><h1>Guia do montador.</h1><p>As fichas completas reúnem medidas, esquemas dimensionais, peças, acabamentos, ferragens e orientações de montagem.</p><p><a href="Fichas_fabricacao/index.html">Abrir as 20 fichas completas →</a></p><p><a href="Fichas_fabricacao/Levantamento.html">Levantamento de medidas no apartamento →</a></p><h2>Consulta direta por móvel</h2>'
        for code,f in FABRICATION.items():
            body+='<section id="'+code+'"><h3><a href="Fichas_fabricacao/'+code+'.html">'+code+' · '+escape(f['name'])+'</a></h3><p>'+escape(f['finishSummary'])+'</p><p>'+str(len(f['panels']))+' peças com medidas nominais. Fechamentos técnicos na ficha; condições físicas do apartamento na folha de levantamento.</p></section>'
    write_if_changed(ROOT/'06_Entregas/Dossie_marcenaria_R45.html',page('Guedala Park · guia do montador',body))

BASE_DOCS=copy.deepcopy(DOCS)
BASE_ASSETS=list(ASSETS)


def build(target=None, regenerate=False, build_package=False, export_docs=True):
    global FABRICATION,GENERATED_PAGES
    DOCS[:]=copy.deepcopy(BASE_DOCS)
    ASSETS[:]=BASE_ASSETS
    if export_docs and target is None and (ROOT/'.site/docs').exists() and any((ROOT/'.site/docs').iterdir()):
        raise FileExistsError('Existing .site/docs preserved. Choose --output-dir or --sources-only.')
    from plain_language import plain_data, plain_html, document_intro, DOCUMENT_COPY, public_document
    if regenerate:
        generated=runpy.run_path(str(STUDY/'build_fabrication.py'))
        FABRICATION,assets=generated['build']()
    else:
        text=(STUDY/'src/fabrication-data.js').read_text(encoding='utf8')
        FABRICATION=json.loads(re.search(r'const FABRICATION_DATA\s*=\s*(\{.*\});',text,re.S)[1])['modules']
        assets=json.loads((ROOT/'06_Entregas/Fichas_fabricacao/manifest.json').read_text(encoding='utf8'))['files']
    if build_package:runpy.run_path(str(STUDY/'build_share_package.py'))['build']()
    base='06_Entregas/Fichas_fabricacao/'
    doc('fichas','Fichas completas dos 20 móveis','Começar','all','R15','Medidas, peças, acabamentos, ferragens selecionadas e furação rastreável.',base+'index.html')
    doc('pendencias-r14','O que falta · projeto, oficina e apartamento','Começar','all','R15','Próximos passos separados por etapa, com decisões e fontes nas fichas.',base+'Pendencias.html')
    doc('campo','O que medir no apartamento','Levantamento','all','Preencher em campo','Folha por móvel: dimensões físicas, instalações, níveis e paredes.',base+'Levantamento.html')
    for code,f in FABRICATION.items():
        doc('ficha-'+code,code+' · '+f['name'],'Ficha de montagem',f['room'],'R15','Ferragens, furação com referências, peças CSV e próximas conferências.',base+code+'.html')
    ASSETS.extend(base+p for p in assets)
    ASSETS.append(base+'manifest.json')
    DOCS[:] = [plain_data(d) for d in DOCS]
    for d in DOCS:
        if d['id'] in DOCUMENT_COPY:
            d['title'], d['summary'] = DOCUMENT_COPY[d['id']]
        elif d['id'].startswith('ficha-'):
            code = d['id'][6:]
            d['title'] = code+' · '+FABRICATION[code]['name']
            d['summary'] = 'Consulte as medidas, os materiais, a montagem e o que falta conferir.'
        public_document(d)
    for d in DOCS:
        if d.get('path'):d['available']=d['id']=='pacote-compartilhar' or (ROOT/d['path']).is_file()
    GENERATED_PAGES,migration,_=configure_library(DOCS,RELEASE,FABRICATION,ROOT,page)
    write_if_changed(STUDY/'Documentos_antes_depois.csv',migration)
    write_sources()
    if not export_docs:return dict(modules=20,documents=len(DOCS),exported=False)
    mapping={d['path']:d['path']+('.html' if d['path'].endswith('.md') else '') for d in DOCS if d['path'] and not d.get('generated')}
    mapping.update({p:p for p in ASSETS})
    missing_sources=[src for src in mapping if not(ROOT/src).is_file()]
    mapping={src:dst for src,dst in mapping.items()if(ROOT/src).is_file()}
    mapping.update({p:p for p in GENERATED_PAGES})
    materialized=set(mapping.values())
    document_by_path = {d['path']:d for d in DOCS if d.get('path')}
    target=Path(target)if target else ROOT/'.site/docs'
    published=[]; omitted=[dict(source=src,reference=src,reason='Historical source not present locally; excluded from artifact')for src in missing_sources]
    for src, dst in mapping.items():
        source=ROOT/src
        if not source.is_file() and src not in GENERATED_PAGES:
            omitted.append(dict(source=src,reference=src,reason='Historical source not present locally; no archive extracted'))
            continue
        dest=target/dst; dest.parent.mkdir(parents=True,exist_ok=True)
        if source.suffix.lower() in ['.md','.html']:
            content=GENERATED_PAGES[src] if src in GENERATED_PAGES else source.read_text(encoding='utf-8')
            if source.suffix=='.md': content=page(source.stem,markdown(content))
            def local_link(m):
                attr,delimiter,url=m.group(1,2,3)
                parsed=urlsplit(unquote(url))
                if src in GENERATED_PAGES and url==LIBRARY_HOME:return m[0]
                if parsed.scheme in ['http','https','mailto','data'] or url.startswith('#'): return m[0]
                resolved=posixpath.normpath(posixpath.join(posixpath.dirname(src),parsed.path))
                if resolved in mapping or resolved in materialized:
                    rel=posixpath.relpath(mapping.get(resolved,resolved),posixpath.dirname(dst))
                    return attr+'='+delimiter+quote(rel,safe='/')+('#'+parsed.fragment if parsed.fragment else '')+delimiter
                omitted.append(dict(source=src,reference=url))
                return 'data-unpublished-reference='+delimiter+escape(url,quote=True)+delimiter
            content=re.sub(r'\b(href|src)\s*=\s*([\"\'])(.*?)\2',local_link,content,flags=re.I)
            # Original reports may contain action scripts; documentation is read-only.
            content=re.sub(r'<script\b[^>]*>.*?</script>','',content,flags=re.I|re.S)
            document = document_by_path.get(src)
            if document and not src.startswith('06_Entregas/'):
                content = document_intro(content, document)
            dest.write_text(plain_html(content),encoding='utf-8')
        else: shutil.copyfile(source,dest)
        published.append(dst)
    (target/'manifest.json').write_text(json.dumps(dict(files=published,unpublishedReferences=omitted,policy='Explicit technical allowlist only; no recursive inclusion.'),ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(dict(documents=len(DOCS),modules=20,published=len(published),unpublishedReferences=len(omitted),directory=str(target)),ensure_ascii=False))

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--output-dir');parser.add_argument('--sources-only',action='store_true');parser.add_argument('--regenerate',action='store_true');a=parser.parse_args()
    build(target=a.output_dir,regenerate=a.regenerate,export_docs=not a.sources_only)
