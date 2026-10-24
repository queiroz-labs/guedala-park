"""Biblioteca técnica explícita. Não percorre nem publica pastas privadas.

Invocado por preparar_pages.py antes do HTML; somente os arquivos da lista DOCS e ASSETS
são publicados em .site/docs. Links locais fora da seleção ficam sem navegação.
"""
from pathlib import Path
from html import escape
from urllib.parse import urlsplit, unquote, quote
import json, re, shutil, posixpath, runpy

STUDY = Path(__file__).resolve().parent
ROOT = STUDY.parent.parent
R45 = '01_Projeto/Consolidacao_R45_2026-10-23/'
CAD_COLORS = '01_Projeto/Cores_FreeCAD_R16_2026-10-23/'
R47 = '01_Projeto/Southco_banco_R47_2026-10-23/'
TAPS = '01_Projeto/Conferencia_torneiras_2026-10-23/'
DOCS = []
FABRICATION = {}
def doc(id, title, category, rooms, status, summary, path):
    DOCS.append(dict(id=id,title=title,category=category,rooms=rooms.split(','),status=status,summary=summary,path=path))

doc('dossie','Guia do montador','Começar','all','Consolidado','Medidas, ferragens, acabamentos e pendências por módulo.','05_Entregas/Dossie_marcenaria_R45.html')
doc('pacote-compartilhar','Baixar pacote para compartilhar','Começar','all','R16','FreeCAD com cores R16 e geometria R45, fichas R14, planta cotada e instruções em um ZIP.','05_Entregas/Compartilhar_R16/Guedala_Park_R16.zip')
doc('matriz','Medidas dos 20 módulos','Medidas','all','Nominal','Vãos internos em milímetros e o que falta fechar.',R45+'Inventario/Matriz_20_modulos.md')
doc('interfaces','Uniões entre chapas','Montagem','all','Em estudo','171 contatos nominais; ligação e caminho da carga a definir.',R45+'Inventario/Interfaces_retangulares.md')
doc('fixas','Ferragens fixas e suspensão','Ferragens','all','Candidatas','Pinos, conectores, suportes e restrições de montagem.',R45+'Inventario/Ferragens_fixas.md')
doc('varoes','Varões do roupeiro','Ferragens','quarto','Em estudo','Quatro varões; oito terminais. Corte depende do suporte.',R45+'Inventario/Varoes.md')
doc('bancada','Estrutura da bancada','Montagem','escritorio','Alternativa','Bancada de 2000 × 700 × 30 mm; reforço separado em estudo.',R45+'Inventario/Bancada.md')
doc('minifix','Minifix do aéreo C','Ferragens','cozinha','Alternativa','20 conjuntos propostos para montagem fixa em chapa de 18 mm.',R45+'Inventario/Minifix_C.md')
doc('espelheiro','Pinos e prateleiras do espelheiro','Ferragens','banho','Em estudo','Oito apoios candidatos; carga da chapa e parede não liberadas.',R45+'Inventario/Espelheiro.md')
doc('gavetas','Gavetas, guias e rodízios','Ferragens','cozinha,quarto,escritorio','Em estudo','Compatibilidade, carga, engates e retirada das gavetas.',R45+'Gavetas/Resultado.html')
doc('movento','Alternativa MOVENTO 400','Ferragens','escritorio','Alternativa','Preserva o útil; conflitos locais e retirada ainda pendentes.',R45+'Gavetas/Alternativas_escritorio/Resultado.html')
doc('portas','Portas e articulações','Ferragens','all','Em estudo','Ensaios de portas, banco e mecanismos; não é liberação executiva.',R45+'Portas_e_articulacoes/Relatorio.html')
doc('cesto','Cesto basculante','Ferragens','lavanderia','Em estudo','Frente 550 × 521 × 18; saco removível e curso até 55° preservados.',R45+'Portas_e_articulacoes/Cesto_selecao_e_esforcos.md')
doc('mesa-varal','Mesa Berlin e varal','Compatibilização','sala,lavanderia','Em estudo','Mesa pronta; quadro do varal de 1000 × 500, sem placa de ocultação.',R45+'Portas_e_articulacoes/Mesa_e_varal.md')
doc('banco','Apoios e estrutura do banco','Montagem','sala','Em estudo','Duas tampas e armazenamento preservados; apoios e ligações pendentes.',R45+'Banco_estrutura/Resultado.html')
doc('southco','Southco: fixação e almofadas','Ferragens','sala','Em estudo','R47 separada da R45; eixo, fixações e batente ainda não fechados.',R47+'Relatorio.html')
doc('batente','Batente mecânico do banco','Montagem','sala','Alternativa','Geometria nominal de parada a 90°; não fabricar pelo eixo hipotético.',R47+'Batente_estudo.md')
doc('torneiras','Conferência de cubas e torneiras','Compatibilização','cozinha,banho','Em estudo','Envelopes e medidas disponíveis; instalação depende dos produtos.',TAPS+'Conferencia.html')
doc('purangi','Purangi: vedação e abertura','Compatibilização','banho','Não liberado','Compatibilidade integral não comprovada; troca não liberada.',TAPS+'Resultado_vedacao_abertura.md')
doc('forno','Forno: grelhas e manutenção','Compatibilização','cozinha','Em estudo','R02 dos apoios e grelhas removíveis; montagem e ventilação condicionadas.','01_Projeto/Cozinha/Fischer_Grill_2026-10-19/Grelhas_manutencao_R02/README.md')
doc('cad','FreeCAD · cores atualizadas R16','FreeCAD','all','Geometria R45','Aparência alinhada ao site e às fichas; geometria R45 preservada e pendências técnicas mantidas.',CAD_COLORS+'Guedala_Park_R45_Cores_R16.FCStd')
doc('cad-cores','Atualização de cores do FreeCAD','Acabamentos','all','R16','Registro dos acabamentos visuais; cores aproximadas e limites da atualização.',CAD_COLORS+'README.md')
doc('cad-southco','FreeCAD: fixação Southco','FreeCAD','sala','Estudo separado','Proposta R47 para inspeção; não substitui o modelo principal.',R47+'Southco_Fixacao_ESTUDO.FCStd')
doc('cad-purangi','FreeCAD: sensibilidade Purangi','FreeCAD','banho','Estudo separado','Envelopes hipotéticos para conferir abertura; não é CAD certificado.',TAPS+'Purangi_R45_SENSIBILIDADE.FCStd')
doc('executivo','Pranchas executivas e plano de corte','Executivo','all','Pendente','Faltam cotas de campo, furação, fitas de borda, folgas, ligações e liberação por peça.',None)
doc('planta','Planta oficial do apartamento','Arquitetura','all','Documento de origem','Referência de planta; não substitui levantamento acabado.','02_Plantas_e_manuais/Planta_oficial.pdf')
doc('pisos','Pisos e rodapés','Arquitetura','all','Escolhas e estudos','Acabamentos, interfaces e condições de instalação. Conferir revisão e quantitativos nas fontes.','01_Projeto/Pisos_e_rodapes.md')
doc('luz-quarto','Iluminação do quarto','Iluminação','quarto','Em desenvolvimento','Comandos, temperaturas e relação com a cabeceira e os armários.','01_Projeto/Portas_e_quarto/Iluminacao_R00.md')
doc('instalacoes','Instalações: compatibilização executiva','Instalações','all','Pendente','Conferir em campo os pontos elétricos, hidráulicos, gás e ventilação; plantas executivas compatibilizadas ainda não reunidas.',None)
doc('levantamento','Levantamento para fabricação','Executivo','all','Pendente','Cotas acabadas, diagonais, prumo, esquadro, níveis, revestimentos e substratos de fixação precisam de levantamento.',None)
doc('acabamentos-r13','Branco TX nos interiores','Acabamentos','all','Escolhido','Diretriz vigente por face: interiores Branco TX e padrões escolhidos nas faces aparentes.','01_Projeto/Estudo_interativo/fabrication/Decisao_acabamentos_R13.md')
doc('planta-cotada','Planta cotada · distâncias entre paredes','Arquitetura','all','R13','Cotas oficiais por ambiente e diferenças da reconstrução identificadas.','05_Entregas/Planta_cotada_R13/index.html')

ASSETS = [
    CAD_COLORS+'Plano_de_cores.json',
    CAD_COLORS+'Verificacao_cores.json',
    CAD_COLORS+'Verificacao_geometria.json',
    '05_Entregas/Compartilhar_R16/manifest.json',
    # Compatibility aliases: previously shared R14 URL serves the current R16 ZIP.
    '05_Entregas/Compartilhar_R14/Guedala_Park_R14.zip',
    '05_Entregas/Compartilhar_R14/manifest.json',
    R45+'Guedala_Park_R45_Consolidado.FCStd',
    '05_Entregas/Planta_cotada_R13/Planta_cotada.svg',
    '05_Entregas/Planta_cotada_R13/Planta_oficial.png',
    '05_Entregas/Planta_cotada_R13/Cotas.json',
    R45+'Gavetas/Alternativas_escritorio/Corte_vertical.svg',
    R45+'Gavetas/Alternativas_escritorio/Blum_MOVENTO_oficial.pdf',
    R45+'Gavetas/Alternativas_escritorio/Blum_planejamento.png',
    R45+'Gavetas/Alternativas_escritorio/Blum_vertical.png',
    R45+'Portas_e_articulacoes/Banco_abertura_frontal.svg',
    R47+'Fixacao_proposta.png', TAPS+'Cozinha_estudo.png', TAPS+'Banheiro_estudo.png',
    TAPS+'Purangi_sensibilidade.png', R45+'Inventario/Bancada_R02.png',
    '01_Projeto/Cozinha/Fischer_Grill_2026-10-19/Grelhas_manutencao_R02/Grelhas_manutencao.png',
    '01_Projeto/Cozinha/Fischer_Grill_2026-10-19/Grelhas_manutencao_R02/Grelhas_manutencao.svg',
]

HARDWARE = {
 'P01':['Quatro varões Ø20 nominais; oito terminais. Ø25 é alternativa, não substituição.','Trilhos e gavetas: conferir estudo de mecanismos.'],
 'P02':['Dobradiças de referência em revisão; quatro formas inválidas registradas.'],
 'P03':['Mecanismo de correr: conferir estudo de portas.'],
 'P04':['Suspensão e ligações dos divisores ainda a dimensionar.'],
 'P05':['Duas portas; dobradiças reguláveis com amortecimento escolhidas.'],
 'P06':['FGVTN 500 candidata; capacidade publicada corrigida para 35 kg.','Engates, folgas e fixações ainda a fechar.'],
 'P07':['Inserto M4 curto nas grelhas: candidato, retenção no MDF não comprovada.'],
 'P08':['Seis rodízios, roda 30 e altura total 39 mm; produto exato pendente.','Guias 3 mm com corrida 2 mm são proposta; batente removível a definir.'],
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
 'P20':['Southco candidata com fixação R47 em estudo separado.','Rockler traseira e abertura frontal foram rejeitadas. Batente independente pendente.'],
}
EXTRA_DOCS = {'P01':['varoes','gavetas','portas'],'P02':['portas'],'P03':['portas'],'P04':['portas'],'P05':['torneiras','portas'],'P06':['gavetas'],'P07':['fixas'],'P08':['gavetas'],'P09':['portas'],'P10':['minifix','portas'],'P11':['fixas','portas'],'P12':['portas'],'P13':['fixas'],'P14':['cesto','mesa-varal'],'P15':['fixas','mesa-varal'],'P16':['gavetas','movento','bancada'],'P17':['bancada','portas'],'P18':['portas','torneiras','purangi'],'P19':['espelheiro','torneiras','purangi'],'P20':['banco','southco','batente','mesa-varal']}
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
    next(r for r in rows if r['id']=='P20')['pending']='Fechar eixo real, ligações, apoios, almofadas e batente independente conforme R47. Southco permanece candidata; Rockler traseira e abertura frontal rejeitadas.'
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

def write_sources():
    rows=matrix()
    EXTRA_DOCS['P07']=['forno','fixas']
    guidance={r['id']:dict(hardware=HARDWARE[r['id']],pending=[r['pending'],'Conferir medidas de campo, material efetivo, bordas, furação e ligações antes do corte.'],finish=finish(r['id']),documentIds=list(dict.fromkeys(['matriz','fixas']+EXTRA_DOCS[r['id']]))) for r in rows}
    for code,f in FABRICATION.items():
        guidance[code].update(fabrication=f,finish=f['finishSummary'],pending=f['technicalChecks'])
        guidance[code]['hardware']=[r['item']+': '+str(r.get('reference') or 'definição específica na ficha')+' · '+r['status'] for r in f['hardwareRows']]
        guidance[code]['documentIds'].insert(0,'ficha-'+code)
        guidance[code]['documentIds'].append('acabamentos-r13')
    (STUDY/'src/workshop-docs.js').write_text('/* Fontes explícitas. Medidas nominais; não constitui liberação para fabricação. */\nconst WORKSHOP_DOCS = '+json.dumps(DOCS,ensure_ascii=False,indent=2)+';\nconst MODULE_GUIDANCE = '+json.dumps(guidance,ensure_ascii=False,indent=2)+';\nfunction WORKSHOP_DOC_URL(doc){return doc.path ? "docs/"+doc.path+(doc.path.endsWith(".md") ? ".html" : "") : null;}\n',encoding='utf-8')
    body='<p class="meta">GUEDALA PARK · MARCENARIA · 23 OUTUBRO 2026</p><h1>Do ambiente à peça.</h1><p>Guia de consulta para orçamento, conferência e montagem.</p><p class="note">Base dimensional R45, complementada pelos estudos R47 e de torneiras. Todas as medidas abaixo são nominais do modelo, em <strong>milímetros</strong>. Nenhum módulo está liberado para fabricação apenas pela presença neste guia.</p><p class="no-print"><button onclick="window.print()">Imprimir / salvar PDF</button></p><nav class="tags"><a href="#cobertura">Cobertura</a><a href="#modulos">20 módulos</a><a href="#executivo">Executivo pendente</a><a href="#fontes">Documentos</a></nav><h2 id="cobertura">O que está disponível</h2><table><tr><th>Informação</th><th>Cobertura</th><th>Próximo fechamento</th></tr>'
    for values in [('Medidas e espessuras','20 módulos inventariados; cotas de modelo','Levantamento final e tolerâncias por peça'),('Acabamentos','Escolhas e direções de composição registradas','Código, amostra, lote, sentido do veio e fitas de borda'),('Ferragens','Candidatos, conflitos e estudos locais','SKU final, quantidade, engates e desenho de montagem'),('Uniões e cargas','171 contatos e cenários de cálculo','Ligações, cargas admissíveis e ancoragem real'),('FreeCAD','R45 principal e estudos separados','CAD executivo, furação, ferragens reais e revisão liberada'),('Plano de corte','Não localizado como pacote executivo liberado','Lista por peça, usinagem, bordas e autorização de fabricação')]:
        body+='<tr>'+''.join('<td>'+escape(x)+'</td>' for x in values)+'</tr>'
    body+='</table><h2 id="modulos">Consulta por módulo</h2>'
    for r in rows:
        g=guidance[r['id']]
        body+='<section id="'+r['id']+'"><p class="meta">'+r['id']+' · '+ROOMS[r['id']].upper()+' · NOMINAL / EM DESENVOLVIMENTO</p><h3>'+escape(r['name'])+'</h3><p><strong>Medidas e chapas.</strong> '+escape(r['measure'])+'</p><p><strong>Acabamento.</strong> '+escape(g['finish'])+'</p><p><strong>Ferragens.</strong> '+escape(' '.join(g['hardware']))+'</p><p><strong>Antes de cortar ou montar.</strong> '+escape(r['pending'])+'</p><p class="meta">Fontes: '+ ' · '.join('<a href="../'+next(d['path'] for d in DOCS if d['id']==did)+'">'+escape(next(d['title'] for d in DOCS if d['id']==did))+'</a>' for did in g['documentIds'])+'</p></section>'
    body+='<h2 id="executivo">Pacote executivo ainda pendente</h2><p>Levantamento de cotas acabadas, prumo e esquadro; posição das instalações e substratos; plantas, elevações e cortes finais por ambiente; identificação de cada painel; espessura e composição reais; lado aparente, sentido do veio e fita de borda; folgas de funcionamento e montagem; mapa de furação; conectores e fixadores; cargas e apoios; lista de ferragens e plano de corte revisados. Compatibilizar recortes hidráulicos, ventilação e retirada dos aparelhos.</p><p>Não transformar vãos internos em comprimentos de corte sem descontar ferragens e encaixes. Modelo 3D, escolha de acabamento e ensaio de mecanismo são registros distintos da liberação executiva.</p><h2 id="fontes">Biblioteca técnica</h2>'
    for d in DOCS[1:]:
        body+='<p>'+('<a href="../'+d['path']+'">'+escape(d['title'])+'</a>' if d['path'] else '<strong>'+escape(d['title'])+'</strong>')+' — '+escape(d['status'])+'. '+escape(d['summary'])+'</p>'
    if FABRICATION:
        body='<p class="meta">GUEDALA PARK · MARCENARIA · FICHAS R14</p><h1>Guia do montador.</h1><p>As fichas completas reúnem medidas, esquemas dimensionais, peças, acabamentos, ferragens e orientações de montagem.</p><p><a href="Fichas_fabricacao_R13/index.html">Abrir as 20 fichas completas →</a></p><p><a href="Fichas_fabricacao_R13/Levantamento.html">Levantamento de medidas no apartamento →</a></p><h2>Consulta direta por móvel</h2>'
        for code,f in FABRICATION.items():
            body+='<section id="'+code+'"><h3><a href="Fichas_fabricacao_R13/'+code+'.html">'+code+' · '+escape(f['name'])+'</a></h3><p>'+escape(f['finishSummary'])+'</p><p>'+str(len(f['panels']))+' peças com medidas nominais. Fechamentos técnicos na ficha; condições físicas do apartamento na folha de levantamento.</p></section>'
    (ROOT/'05_Entregas/Dossie_marcenaria_R45.html').write_text(page('Guedala Park · guia do montador',body),encoding='utf-8')

def build():
    global FABRICATION
    generated=runpy.run_path(str(STUDY/'build_fabrication.py'))
    FABRICATION,assets=generated['build']()
    runpy.run_path(str(STUDY/'build_share_package.py'))['build']()
    base='05_Entregas/Fichas_fabricacao_R13/'
    doc('fichas','Fichas completas dos 20 móveis','Começar','all','R14','Medidas, peças, acabamentos, ferragens selecionadas e furação rastreável.',base+'index.html')
    doc('pendencias-r14','O que falta · projeto, oficina e apartamento','Começar','all','R14','Próximos passos separados por etapa, com decisões e fontes nas fichas.',base+'Pendencias.html')
    doc('campo','O que medir no apartamento','Levantamento','all','Preencher em campo','Folha por móvel: dimensões físicas, instalações, níveis e paredes.',base+'Levantamento.html')
    for code,f in FABRICATION.items():
        doc('ficha-'+code,code+' · '+f['name'],'Ficha de montagem',f['room'],'R14','Ferragens, furação com referências, peças CSV e próximas conferências.',base+code+'.html')
    ASSETS.extend(base+p for p in assets)
    ASSETS.append(base+'manifest.json')
    write_sources()
    mapping={d['path']:d['path']+('.html' if d['path'].endswith('.md') else '') for d in DOCS if d['path']}
    mapping.update({p:p for p in ASSETS})
    target=ROOT/'.site/docs'
    published=[]; omitted=[]
    for src, dst in mapping.items():
        source=ROOT/src
        if not source.is_file(): raise FileNotFoundError(source)
        dest=target/dst; dest.parent.mkdir(parents=True,exist_ok=True)
        if source.suffix.lower() in ['.md','.html']:
            content=source.read_text(encoding='utf-8')
            if source.suffix=='.md': content=page(source.stem,markdown(content))
            def local_link(m):
                attr,delimiter,url=m.group(1,2,3)
                parsed=urlsplit(unquote(url))
                if parsed.scheme in ['http','https','mailto','data'] or url.startswith('#'): return m[0]
                resolved=posixpath.normpath(posixpath.join(posixpath.dirname(src),parsed.path))
                if resolved in mapping:
                    rel=posixpath.relpath(mapping[resolved],posixpath.dirname(dst))
                    return attr+'='+delimiter+quote(rel,safe='/')+('#'+parsed.fragment if parsed.fragment else '')+delimiter
                omitted.append(dict(source=src,reference=url))
                return 'data-unpublished-reference='+delimiter+escape(url,quote=True)+delimiter
            content=re.sub(r'\b(href|src)\s*=\s*([\"\'])(.*?)\2',local_link,content,flags=re.I)
            # Original reports may contain action scripts; documentation is read-only.
            content=re.sub(r'<script\b[^>]*>.*?</script>','',content,flags=re.I|re.S)
            dest.write_text(content,encoding='utf-8')
        else: shutil.copyfile(source,dest)
        published.append(dst)
    (target/'manifest.json').write_text(json.dumps(dict(files=published,unpublishedReferences=omitted,policy='Explicit technical allowlist only; no recursive inclusion.'),ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(dict(documents=len(DOCS),modules=20,published=len(published),unpublishedReferences=len(omitted),directory=str(target)),ensure_ascii=False))

if __name__=='__main__': build()
