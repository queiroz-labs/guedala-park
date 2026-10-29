"""Gera páginas autônomas de cotação e anexo R15; não envia nem altera CAD.

Revisar os escopos abaixo quando houver decisão nova. Preços são solicitados,
não embutidos nos pedidos. Rodar na raiz com python -B.
"""
from pathlib import Path
from html import escape
import csv
import io
import json
import re
import zipfile
from consolidar_quantidades_cotacao import annex, CSV as QUANTITIES

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / '06_Entregas/Cotacao'
LIGHT = (ROOT / '03_Ambientes/Iluminacao/Lista_curta_luminarias_e_madeira.md').read_text(encoding='utf-8')
MATERIAL = (ROOT / '01_Programa_e_decisoes/Caderno_de_especificacoes.md').read_text(encoding='utf-8')
URLS = re.findall(r'https?://[^\s)]+', LIGHT + '\n' + MATERIAL)


def url(fragment):
    return next(u for u in URLS if fragment in u)


# Arquivo, destinatário, assunto, canal, escopo, fora, retorno técnico.
PAGES = [
    ('Marcenaria', 'Marcenarias selecionadas por Elias (mesmo pedido a três oficinas)',
     'Cotação preliminar D05-C / D06-B com fichas R15', '',
     'Cotar base integral dos 20 módulos e seis complementos e, separadamente, etapa inicial sem P16, P17, C01, C03, C04 e C05. Manter P01–P15, P18–P20, C02 e C06, conforme fichas R15 e pendências. Preservar armazenamento e ferragens de todos os móveis retidos, espessuras, paleta e armários até o teto. Sem tubos ou quadro metálico substituto. Uma chapa física tem acabamento igual nas duas faces; não acrescentar caixa interna de 15 mm automaticamente.',
     'Na etapa inicial ficam fora: duas gavetas e aéreo do escritório (P16/P17), cabeceira estofada (C01), encosto/almofadas do banco (C03), painel e duas prateleiras da TV (C04), prateleiras/suportes de acessórios do escritório (C05). Perdem-se esses volumes de armazenamento e estofamentos temporariamente; preservar banco-baú e armazenamento do quarto. Pedras, eletros, louças, mesa/cadeiras, sofás, componentes de iluminação e instalação elétrica não pertencem ao pacote de marcenaria. Televisores, soundbar, cadeira de escritório, monitores, volante e pedais não são itens a cotar. E06/prateleiras adiada; E05/TV mantida como interface, sem fornecer aparelho.',
     'Informar preço por módulo/complemento, crédito real de cada adiamento, preço instalado da etapa e custo de segunda mobilização. Cotar suportes independentes para TV/PS5 e E05, e indireta da cabeceira em face inferior acessível sem C01. Não transferir custo ou retirar ferragens silenciosamente. Incluir medição, materiais, bordas, ferragens, fabricação, montagem, arremates e impostos; discriminar frete. Confirmar inclusão do acabamento M03 para evitar duplicidade. Responder no CSV anexo. Fichas têm medidas nominais; produto, ensaios e medição real condicionam execução.'),
    ('Amostras_Madeiramar', 'Madeiramar / Guararapes', 'D02: amostras Lume Matt A e Areia Matt C', url('madeiramar.com.br/produto/mdf-lume'),
     'Solicitar uma amostra física identificada de Lume Matt (A) e uma de Areia Matt (C), para comparação ao lado do Arenza. Referências de revenda: Lume 18 mm 10520 e Areia 18 mm 6734. Solicitar também catálogo vigente de Azul Petróleo Matt e Branco TX.',
     'Não é compra de chapas nem escolha final da cor. Nuvem não integra este pedido de amostras. Não substituir textura, substrato ou cor sem informar.',
     'Informar fabricante, código de fábrica e de revenda, textura, lote, acabamento nas duas faces, espessuras disponíveis de 15/18 mm, formato e borda equivalente. Separar preço de cada amostra, envio e preço por chapa. Distinguir disponibilidade de catálogo de estoque real.'),
    ('Amostras_Fabi', 'Fabi Compensados / Greenplac', 'Amostra Arenza para comparação D02 A/C', url('fabicompensados.com.br/grupo/186'),
     'Solicitar uma amostra física identificada de Greenplac Arenza Colore/Lizze, para comparar com Lume Matt e Areia Matt Guararapes. Referência de revenda Arenza 18 mm: 00004872, a confirmar. Solicitar catálogo e disponibilidade em 15 e 18 mm.',
     'Sem compra de chapas, substituição de Arenza ou adoção automática da versão HR. As amostras Guararapes são solicitadas separadamente.',
     'Identificar código de fábrica, lote, textura, tamanho da chapa, revestimento nas duas faces e bordas. Separar amostra, frete e preço por chapa. Explicar diferenças da variante HR, sem presumir mesma textura ou estoque.'),
    ('IL02_Abastece', 'Abastece / suporte WiZ', 'IL02: quatro A60 e três WiZmotes', url('abastece.com.br/products/lampada'),
     'Cotar quatro A60 smart E27 RGB/brancos para rede 127 V, em dois Jurerê 30 cm 2×E27 (sala/escritório), e três WiZmotes: geral sala, geral escritório e E05/TV. Referências documentais 929002424712 e 929002426812; conciliar SKU/EAN do lote nacional.',
     'Quarto usa Elgin. E06/prateleiras adiada. Não cotar um quarto WiZmote; o controle de E05 já está nas três unidades, não somar ao pedido do kit IL08.',
     'Enviar etiquetas, manuais, estoque e condições escritas de uso de duas A60 no Jurerê com vidro: fechamento, orientação, ventilação e temperatura. Confirmar Alexa/celular, comando físico, pilhas/base e garantia; oferecer alternativa identificada se o uso for restrito.'),
    ('IL03_Taschibra', 'Taschibra Store / suporte técnico', 'IL03: dois Jurerê 52040021-01', url('taschibrastore.com.br'),
     'Cotar dois plafons Jurerê brancos, 30 cm, 2×E27, referência 52040021-01, sem lâmpadas. Aplicação com duas WiZ A60 por corpo, rede 127 V; regulagem na lâmpada smart, sem dimmer na rede.',
     'Lâmpadas e controles são cotados na IL02; não duplicar. Não substituir por Jurerê 25 cm ou outro corpo.',
     'Enviar desenho das dimensões úteis, manual, EAN, fechamento/ventilação e restrições térmicas. A indicação de corpo não dimerizável impede a regulagem interna de lâmpadas smart? Responder por escrito, incluindo acessórios necessários.'),
    ('IL04_Tramontina', 'Tramontina — suporte técnico', 'IL04: pulsador 57115027 em sinal de 12 V CC', 'https://globaltramontina.zendesk.com/hc/pt-br/requests/new',
     'Avaliar três pulsadores 57115027 com placas/suportes 57106204, ligados à entrada de sinal de Shelly Plus RGBW PM alimentado em 12 V CC. O contato não recebe rede 127 V nem alimenta diretamente a fita.',
     'Não considerar a inscrição 10 A/250 V CA como comprovação desta aplicação. Não substituir por interruptor com retenção, iluminação ou eletrônica.',
     'Confirmar contato seco normalmente aberto/momentâneo, limites mínimos de tensão/corrente e adequação a sinal CC. Identificar ficha/revisão, dados que precisam vir da Shelly e alternativa se inadequado. Informar preço ou canal de cotação, acessórios e eventual custo de suporte; instalação pelo RT.'),
    ('IL04_Cotia', 'Elétrica Cotia', 'IL04: três pulsadores e três placas', url('eletricacotia.lojaintegrada.com.br/modulo'),
     'Cotar três pulsadores Tramontina 57115027 e três placas 57106204 com suporte completo, brancos. Aplicação em sinal de controlador Shelly, sujeita à resposta técnica do fabricante.',
     'Sem compra antes da comprovação da aplicação. Não oferecer interruptor comum como equivalente ao pulsador.',
     'Enviar SKU/EAN, ficha, prazo/estoque, conteúdo das embalagens e total por item. Informar se falta algum suporte, parafuso ou acessório. A análise elétrica é solicitada à Tramontina e Shelly; não presumir compatibilidade.'),
    ('IL05_4Tronics', '4Tronics / suporte Shelly', 'IL05: três Plus RGBW PM SNDC-0D4P10WW', url('loja.4tronics.com.br'),
     'Cotar três Shelly Plus RGBW PM, cada um com fonte 12 V CC e fita monocromática. Avaliar pulsador Tramontina 57115027 na entrada de comando.',
     'Fontes e fitas são cotadas separadamente; não duplicar. Não trocar por BLU/bateria ou outro controlador sem identificar diferenças.',
     'Enviar manual/revisão e diagrama aplicável: entrada I1, referência negativa, tensão/corrente no contato, limites de cabo e função toque curto/longo para ligar/regular. Confirmar adequação do pulsador ou indicar Wall Switch 1 Button cabeado com SKU, acessórios e preço separado. Instalação pelo RT.'),
    ('IL06_Andre', 'André Iluminação / Opus e Brilia', 'IL06 + IL09: cinco fontes e três G9', url('andreiluminacao.com.br/driver'),
     'Cotar cinco Opus OPS31002 12 V/36 W/3 A (três com Shelly e duas no banheiro) e três Brilia mini G9 314450, 3,5 W, 3000 K, 127 V. São grupos distintos, não combinar fonte com G9.',
     'Sonoff D1/RM433 são cotados em outra loja. Não acrescentar fontes aos kits WiZ. Nenhuma duplicação do pacote do banheiro.',
     'Fontes: identificar lote, esclarecer corpo de 172/270 mm, desenho, dissipação, montagem em móvel e limites com PWM/Shelly. G9: enviar documentação de dimerização e compatibilidade/restrição com Sonoff D1, inclusive carga mínima. Cotar acessórios e identificar o que ainda exige ensaio.'),
    ('IL07_3R', '3R Elétrica / Cristallux', 'IL07: COB 3000 K e COB 4000 K', url('3reletrica.com.br/fita-led-cob-480led/m-ip65-3000'),
     'Cotar um rolo de 5 m COB 3000 K CLX-FT431230/221506 e um rolo de 5 m COB 4000 K correspondente (referência de loja 1513). Identificar código do fabricante, tensão e lote.',
     'Não cotar a antiga SMD 021965: foi substituída pela Brilia 318939 em pedido separado. Metragem e reaproveitamento de sobras não estão definidos.',
     'Enviar largura/altura, passo de corte, potência e corrente por metro conciliadas com o manual do lote. Informar conexões, proteção de pontas, dissipação e restrições de montagem com Opus/Shelly. Separar acessórios indispensáveis e frete.'),
    ('IL07_Belluce', 'Belluce / Brilia', 'IL07: um rolo Brilia 318939', url('belluce.com.br'),
     'Cotar um rolo de 5 m Brilia 318939, 12 V, 3000 K, 4,8 W/m, IP65; SKU de loja BLL604418. Uso na indireta do banheiro com interruptor comum, fonte Opus OPS31002 e perfil MOV4329 previstos.',
     'Fonte e perfil estão em outros pedidos; não duplicar. IP65 da fita não demonstra proteção da instalação após cortes nem autoriza qualquer posição no banheiro.',
     'Enviar ficha/manual, passo de corte, conexões, dissipação, seção compatível com MOV4329 e proteção das terminações. Cotar acessórios para montagem e manutenção. Trecho real e volumes do banheiro serão conferidos pelo RT.'),
    ('IL08_Planet_Leds', 'Planet Leds pelo Magalu', 'IL08: um kit WiZ 2 m para E05/TV', url('magazineluiza.com.br'),
     'Cotar um kit completo WiZ Lightstrip 2 m, anúncio kf72hc7016. Confirmar correspondência com 929002681171/EAN 8719514336957. E05/TV permanece; o kit de E06/prateleiras foi adiado.',
     'Não cotar dois kits. O WiZmote de E05 já está entre os três da IL02; indicar compatibilidade sem somar outro controle. Não duplicar fonte/controlador incluídos.',
     'Enviar etiqueta, manual, conteúdo exato, faixa de brancos, Alexa/WiZmote, cortes/reconexão/extensões e dissipação. Informar montagem independente da marcenaria adiada e acessórios necessários. Identificar estoque nacional e prazo de entrega.'),
    ('IL09_Eoutlet', 'Eoutlet / Stella', 'IL09: uma EVO STH21967/30', url('eoutlet.com.br'),
     'Cotar uma Stella EVO STH21967/30 branca, 3000 K, para geral da cozinha em 127 V, com interruptor comum.',
     'Não substituir por luminária smart. Posição final depende do giro dos armários e do RT.',
     'Enviar etiqueta/manual do lote, dimensões, fixação, acessórios e restrições de instalação. Identificar SKU/EAN e pacote completo, sem presumir instalação incluída.'),
    ('IL09_Galaxy', 'Galaxy Shop / Galaxy LED', 'IL09: Firefly 9608 e 9605', url('galaxyshop.com.br'),
     'Cotar um Firefly 9608 quadrado 3000 K para lavanderia e um 9605 redondo 3000 K para banheiro, brancos, com interruptores comuns. Se o 9605 não for vendido por este canal, informar canal nacional ou indisponibilidade separadamente.',
     'Não cotar 9607 (redondo 6500 K) como equivalente. Posição com varal e volumes do banheiro dependem do RT.',
     'Enviar SKU/EAN, etiqueta, manual, dimensões e restrições. Separar preço/estoque de cada modelo e acessórios; não assumir que a oferta de um comprova estoque do outro.'),
    ('IL09_Paris_Luz', 'Paris Luz pelo Leroy Merlin', 'IL09: Firefly 9605 redondo 3000 K', url('leroymerlin.com.br/plafon-de-sobrepor-firefly'),
     'Revalidar a cotação de uma unidade Firefly 9605 redonda, branca, 3000 K, para banheiro com interruptor comum. A validade anunciada na referência anterior expirou.',
     'Cotação alternativa para a mesma unidade 9605 pedida à Galaxy: não comprar duas nem somar as propostas. Não substituir por 6500 K.',
     'Confirmar fabricante/código, estoque nacional, prazo, etiqueta/manual, dimensões e acessórios. Identificar vendedor responsável e garantia; instalação/volumes pelo RT.'),
    ('IL09_LED_RS', 'LED RS / Nordecor', 'IL09: duas arandelas EVY 2054', url('ledrs.net'),
     'Cotar duas EVY 2054 brancas, 3000 K, uma por lado da cabeceira, com acionamento independente.',
     'Perfis MOV4329 são cotados em outro pedido. Não substituir cor/modelo nem presumir interruptor próprio.',
     'Confirmar interruptor do produto, alimentação para uso em 127 V, dimensões/envelope, manual, fixação e acessórios. Informar tudo que falta para cada lado funcionar separadamente.'),
    ('IL09_AZ_Led', 'AZ Led / Nordecor', 'IL09: sete barras MOV4329', url('azlediluminacao.com.br'),
     'Cotar sete barras de 2 m MOV4329 brancas, referência de loja 212600, com difusores, tampas e presilhas. Quantidade é provisão; não autoriza cortes.',
     'Não inclui as fitas, fontes ou usinagem. Não reduzir a quantidade automaticamente por D06: E06 usava kit WiZ, sem rateio destas barras.',
     'Enviar seção útil, desenho, acessórios por barra e condições de montagem/dissipação para as fitas Cristallux e Brilia 318939. Discriminar itens vendidos separadamente e plano comercial de fornecimento.'),
    ('IL09_Arevo', 'Arevo Iluminação', 'IL09: Jabuticaba triplo preto/âmbar', url('arevoiluminacao.com.br'),
     'Cotar um pendente Jabuticaba de três globos âmbar, preto, 3×G9, referência C82P3 a confirmar. O anúncio 2623 tem “2xG9” na URL; esclarecer código e variante.',
     'Lâmpadas G9 e dimmer são cotados separadamente. Não considerar preço anterior à seleção do vidro como total final.',
     'Enviar etiqueta, foto da variante, dimensões, manual, altura regulável, acessórios e preço completo com vidro âmbar. Confirmar número de globos/soquetes e estoque.'),
    ('IL09_Analphabot', 'Analphabot / Sonoff', 'IL09: D1 e RM433 com base', url('analphabot.lojaintegrada.com.br/sonoff-d1'),
     'Cotar um D1 (loja KWC6QBJS5) e um RM433 com base (MQU8G25TG), para três Brilia G9 314450 de 3,5 W/127 V.',
     'As três lâmpadas são cotadas separadamente. Não declarar compatibilidade apenas pela soma de potências; conjunto depende de documentação e ensaio aplicável.',
     'Enviar manual/revisão, faixa de carga e carga mínima LED, tipo de dimerização, compatibilidade ou restrição com essas G9, e conteúdo do RM433 (base/bateria). Separar qualquer acessório adicional.'),
    ('IL09_Avanti', 'Avanti Store / Elgin', 'IL09: uma 48D18WSRWIFI no quarto', url('avantistore.com.br'),
     'Cotar uma luminária smart branca Elgin 48D18WSRWIFI, loja 35032460, para o quarto, com brilho regulável, Alexa/celular e uso em 127 V.',
     'Não cotar substituição nas gerais da cozinha/lavanderia/banheiro, que mantêm interruptor comum e seus modelos. Não presumir controle físico equivalente ao WiZmote.',
     'Enviar manual, dimensões, etiqueta e alimentação. Qual comando físico liga/desliga e regula sem celular? Informar SKU, preço e inclusão ou não; explicar funcionamento sem internet e após retorno da energia. Cotar todos os acessórios necessários.'),
]

CSS = '''@page{size:A4;margin:14mm}*{box-sizing:border-box}body{margin:0;background:#e7ece9;color:#20332e;font:14.5px/1.4 Arial,sans-serif}.page{width:182mm;min-height:269mm;margin:18px auto;background:white;padding:10mm}h1{font-size:24px;line-height:1.15;margin:8px 0 12px}h2{font-size:16px;border-bottom:1px solid #cbd7d1;margin:16px 0 5px}p{margin:5px 0 9px}.tag{font-size:12px;letter-spacing:.05em;color:#4b6359}.meta{border-left:4px solid #37664e;padding:8px 12px;background:#f1f5f2}a{color:#245f53;overflow-wrap:anywhere}footer{margin-top:18px;font-size:12px;color:#53685e}li{margin:7px 0}@media print{body{background:white}.page{margin:0;padding:0;min-height:0;width:auto}.tools{display:none}}'''


def page_html(name, title, channel, scope, excluded, technical, zipped=False):
    channel_html = ('<a href="' + escape(channel, quote=True) + '">Atendimento na página oficial da loja/fabricante</a>') if channel else 'Canal comercial habitual da oficina selecionada por Elias; enviar individualmente a três oficinas.'
    extra = ''
    style = CSS
    if name.startswith('Marcenarias'):
        prefix = 'Fichas_R15/' if zipped else '../Fichas_fabricacao/'
        extra = f'<p><b>Anexos:</b> <a href="{prefix}index.html">20 fichas R15</a>, <a href="{prefix}Pendencias.html">pendências</a>, <a href="{prefix}Levantamento.html">levantamento</a> e formulário CSV no ZIP. Extrair o ZIP inteiro antes de abrir.</p>'
        extra += annex()
        style += 'table{border-collapse:collapse;width:100%;font-size:12px}th,td{text-align:left;border:1px solid #cbd7d1;padding:4px 6px}thead{display:table-header-group}tr{break-inside:avoid}'
    return f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>{escape(title)}</title><style>{style}</style></head><body><main class="page">
<div class="tag">GUEDALA PARK · COTAÇÃO PRELIMINAR · 27/10/2026 · NÃO ENVIADO</div><h1>{escape(title)}</h1>
<div class="meta"><b>Para:</b> {escape(name)}<br><b>Canal:</b> {channel_html}<br><b>Resposta solicitada:</b> 30/10/2026, às 18h (Brasília). Se inviável, confirmar recebimento e informar outra data.</div>
<h2>Escopo a cotar</h2><p>{escape(scope)}</p>{extra}<h2>O que fica fora</h2><p>{escape(excluded)}</p>
<h2>O que precisamos receber de volta</h2><p>{escape(technical)}</p>
<p><b>Condições comerciais:</b> preço unitário por móvel/item e total; frete separado; instalação/montagem incluída, cobrada à parte ou não oferecida; acessórios; impostos; pagamento; prazo de entrega; validade e garantia. Não deixar campo ausente valer zero. Dados de entrega serão informados privadamente por Elias para cálculo do frete.</p>
<footer>Pedido de informação e orçamento, sem ordem de compra, reserva de estoque, contratação ou fabricação. Produtos e implantação continuam sujeitos aos documentos técnicos, medidas reais e profissional responsável.</footer></main></body></html>'''


FORM_FIELDS = ['ID', 'Item', 'Etapa', 'Preço integral instalado (R$)', 'Preço etapa inicial instalado (R$)', 'Crédito real do adiamento (R$)', 'Materiais e ferragens', 'Frete (R$)', 'Instalação', 'Validade', 'Incluído em outro item?', 'Pendências e exclusões']


def form_rows(old):
    """Regenera somente formulário vazio; serviços não se multiplicam a cada build."""
    if any(v for r in old for k,v in r.items() if k not in ('ID','Item','Etapa')):
        raise ValueError('Formulário contém respostas; preservar e revisar antes de gerar')
    rows = []
    seen=set()
    for row in old:
        if not row['ID']:
            continue
        code = row['ID']
        if code=='TOTAL' or re.fullmatch(r'S\d{2}',code):continue
        if code in seen:raise ValueError('Módulo/complemento repetido: '+code)
        seen.add(code)
        item = re.sub(r'\s+\d+.*$', '', row['Item']) if code in ('P01', 'C02') else row['Item']
        stage = 'Futura; fora da etapa inicial D05-C' if code in ('P16', 'P17', 'C01', 'C03', 'C04', 'C05') else 'Etapa inicial; seguir R15 e pendências'
        rows.append([code, item, stage] + [''] * (len(FORM_FIELDS) - 3))
    for code, label in [('S01', 'Medição e projeto executivo'), ('S02', 'Frete e movimentação'), ('S03', 'Montagem e arremates'), ('S04', 'Tributos'), ('S05', 'Adaptações TV/PS5, E05 e Q06'), ('S06', 'Segunda mobilização futura'), ('TOTAL', 'Total sem dupla contagem')]:
        rows.append([code, label, 'Discriminar inclusão; não somar duas vezes'] + [''] * (len(FORM_FIELDS) - 3))
    return rows


def require_unsent():
    package=ROOT/'05_Orcamento_e_cronograma/Orcamento/Marcenaria_35mil/Pacote_cotacao_marcenaria_R01.md'
    intro='\n'.join(package.read_text(encoding='utf-8').splitlines()[:4])
    overview=next(line for line in (ROOT/'06_Entregas/README.md').read_text(encoding='utf-8').splitlines() if line.startswith('**Cotação para envio'))
    for text in (intro,overview):
        if not re.search(r'não enviados?',text,re.I) or re.search(r'\benviad[oa]s?\b',re.sub(r'não enviados?','',text,flags=re.I),re.I):
            raise ValueError('Estado de envio não é inequivocamente não enviado; preparar só adendo')


def build():
    require_unsent()
    source = ROOT / '05_Orcamento_e_cronograma/Orcamento/Marcenaria_35mil/Formulario_resposta_cotacao_R01.csv'
    old = list(csv.DictReader(io.StringIO(source.read_text(encoding='utf-8-sig')), delimiter=';'))
    rows=form_rows(old)
    OUT.mkdir(exist_ok=True)
    for filename, name, title, channel, scope, excluded, technical in PAGES:
        (OUT / (filename + '.html')).write_text(page_html(name, title, channel, scope, excluded, technical), encoding='utf-8')
    with source.open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f, delimiter=';'); writer.writerow(FORM_FIELDS); writer.writerows(rows)
    fichas = ROOT / '06_Entregas/Fichas_fabricacao'
    manifest = json.loads((fichas / 'manifest.json').read_text(encoding='utf-8'))
    assert manifest['revision'] == 'R15' and manifest['modules'] == 20
    with zipfile.ZipFile(OUT / 'Marcenaria.zip', 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('Pedido.html', page_html(*PAGES[0][1:], zipped=True))
        z.write(source, 'Formulario_resposta.csv')
        z.write(QUANTITIES, 'Quantidades_referencia.csv')
        for filename in manifest['files'] + ['manifest.json']:
            z.write(fichas / filename, 'Fichas_R15/' + filename)
    items = []
    for filename, name, title, channel, *_ in PAGES:
        file = 'Marcenaria.zip' if filename == 'Marcenaria' else filename + '.html'
        link = f'<a href="{escape(channel, quote=True)}">canal da loja / atendimento</a>' if channel else 'contato comercial das três oficinas escolhidas; nomes não constam do projeto'
        items.append(f'<li><input type="checkbox"> <b>{escape(name)}</b> — {link} — <a href="{file}">{file}</a></li>')
    intro = '<p>Revisar e enviar cada arquivo somente ao respectivo destinatário. As páginas são autônomas: anexar o HTML como documento ou abrir e copiar o texto no atendimento. Se o canal recusar HTML, imprimir a página em PDF A4, sem cabeçalhos do navegador. Para marcenaria, enviar o ZIP com fichas R15 e Quantidades_referencia.csv (estimativa nominal de 29/10, com exclusões e divergências); a proposta integral é comparação, a etapa inicial segue D05-C/D06-B.</p><p><b>Prazo solicitado em todos:</b> 30/10/2026 às 18h, Brasília. Registrar o envio real privadamente. Não há envio automático. Galaxy e Paris Luz são cotações alternativas da mesma unidade 9605; não somar. IL08 não duplica o controle de IL02. Os links de produto/canal são referências, não confirmação de estoque.</p>'
    index = f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Elias envia hoje</title><style>{CSS}</style></head><body><main class="page"><div class="tag">CHECKLIST · 27/10/2026 · NÃO ENVIADO</div><h1>Elias envia hoje</h1>{intro}<p><a href="Pacote_cotacao.zip">Baixar todos os pedidos</a></p><ol>{"".join(items)}</ol><footer>Não encaminhar orçamento interno, metas ou dados pessoais junto aos pedidos. Amostras Lume/Areia dependem da comparação física com Arenza. Nenhuma compra autorizada.</footer></main></body></html>'
    (OUT / 'index.html').write_text(index, encoding='utf-8')
    with zipfile.ZipFile(OUT / 'Pacote_cotacao.zip', 'w', zipfile.ZIP_DEFLATED) as z:
        for filename, *_ in PAGES:
            if filename != 'Marcenaria':
                z.write(OUT / (filename + '.html'), filename + '.html')
        z.write(OUT / 'Marcenaria.zip', 'Marcenaria.zip')
        z.writestr('index.html', index.replace('<a href="Pacote_cotacao.zip">Baixar todos os pedidos</a>', 'Pacote extraído: enviar os arquivos indicados abaixo.'))
    print(f'{len(PAGES)} pedidos individuais; ZIP R15 com {len(manifest["files"])} arquivos do manifesto; nada enviado')


if __name__ == '__main__':
    build()
