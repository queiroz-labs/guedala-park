"""L02: custo-benefício com IRC do espelho preservado; preços vistos na loja."""
from pathlib import Path
from decimal import Decimal as D
from html import escape as h
import copy, json, re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]

def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def write(path, data):
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def money(value):
    return 'R$ '+f'{value:,.2f}'.replace(',','X').replace('.',',').replace('X','.')

old = read(HERE/'Luminarias_selecao_L01.json')
data = copy.deepcopy(old)
buy_indirect = 'https://www.3reletrica.com.br/fita-de-led-12v-24w-3000k-amarela-48wm-60-ledsm-ip65-5-metros-cristallux'
technical_indirect = 'https://www.cristallux.com.br/produto/fita-led-cristall-pro-dry-5mt-12v-4-8w-m-3000k-460lm-m-ip65-60led-m-irc-80'
buy_source = 'https://luzdecasa.com.br/produto/fonte-12v-slim-opus-36-watts-3a-ip67-270x20x20mm-ac-31002/24454'
technical_source = 'https://opusled.com.br/produto/fonte-blindada-32w-12v/'
data.update(revision='L02',supersedes='Luminarias_selecao_L01.json',
    scope='Revisão solicitada por Elias: fontes e fitas por custo-benefício, preservando qualidade do espelho. Total de compra dos componentes, sem frete e instalação; não contrato, compra ou liberação executiva.',
    priced_components_complete=True, purchase_made=False, installation_released=False,
    complete_luminaires_released=False, main_cad_modified=False)
mirror = data['groups'][1]
mirror.update(driver='Opus OPS 31002, 12 Vcc, 3 A, 36 W, IP67',
    status='Mesma fita COB 4000 K/IRC>90 da L01, mesmas duas barras de 550 mm, preço e oferta confirmados. Montagem e posição inferior condicionadas.')
indirect = data['groups'][2]
indirect.update(product='Cristallux Cristall Pro Dry SMD CLX-FT200530',code='021965',ean='7899440021965',
    cut_pitch_mm=50,strip_section_mm=[8,2.2],watts_per_m=4.8,watts_at_length_cap=9.6,
    current_at_length_cap_a=0.8,lumens_per_m=460,lumens_before_diffuser_at_length_cap=920,
    cri='>80',driver='Opus OPS 31002, 12 Vcc, 3 A, 36 W, IP67',dimmable=False,
    product_url=technical_indirect,buy_url=buy_indirect,
    status='Luz complementar oculta: potência menor e IRC>80 aceito somente neste grupo. Até 2 m continua limite de orçamento, não medição real.')
bom = copy.deepcopy(old['bom'][:4])
bom[0].update(availability='Preço 141,90 e vendedor Paris Luz confirmados na página real; compra habilitada. Entrega depende do CEP.',
    price_method='Preço exibido sem cupom',price_verification='Navegador, 24/10/2026')
bom[1].update(price_brl=169.26,card_price_brl=174.49,
    availability='Estoque disponível na página real; leitura anterior sob consulta dos buscadores foi superada.',
    price_method='Pix',price_verification='Navegador, 24/10/2026')
bom[2].update(product='Cristallux CLX-FT200530 /021965, SMD, 3000 K, 4,8 W/m',price_brl=62.56,
    card_price_brl=64.49,seller='3R Soluções Elétricas',availability='Estoque disponível na página real',
    buy_url=buy_indirect,price_method='Pix',price_verification='Navegador, 24/10/2026')
bom[3].update(price_evidence='34,41 por barra de 2 m confirmado na página real, sem aplicar cupom.',
    availability='Compra habilitada; despacho anunciado em até 10 dias úteis, além do transporte.',
    card_price_brl=36.22,price_method='Pix, sem cupom',price_verification='Navegador, 24/10/2026')
bom.append(dict(product='Opus OPS 31002, 12 V /3 A /36 W, IP67',quantity=2,unit='unidade',
    price_brl=85.05,card_price_brl=89.78,seller='Luz de Casa',buy_url=buy_source,
    availability='Compra habilitada; preparação e despacho anunciados em 5 dias úteis, além do transporte.',
    price_method='Pix/boleto, desconto de 10% exibido, sem cupom',
    price_verification='Navegador, 24/10/2026',
    envelope_mm=[276,21,20],
    lot_note='Fabricante atual: 172×21×20 mm, policarbonato e garantia 3 anos. Loja descreve versão 276×20×20 mm, alumínio e garantia 1 ano, consistente com catálogos Opus antigos. Reservada a maior envoltória; não prometer lote novo/garantia 3 anos no preço da versão anunciada. Conferir etiqueta 12 V/3 A/36 W/IP67 e lote recebido antes de definir o compartimento.'))
data['bom'] = bom
total = sum(D(str(i['price_brl']))*i['quantity'] for i in bom)
card_total = sum(D(str(i.get('card_price_brl',i['price_brl'])))*i['quantity'] for i in bom)
old_with_mirror = D(str(old['cost']['known_components_subtotal_brl']))+D('169.26')
saving = old_with_mirror-total
data['checks']['mirror'].update(driver_w=36,driver_current_a=3,load_percent=36.67,
    calculation='2 ×0,55 m ×12 W/m =13,2 W; corrente 1,1 A. 13,2/36 =36,7% da fonte. Barras em paralelo.')
data['checks']['indirect'].update(power_w=9.6,current_a=0.8,driver_w=36,driver_current_a=3,
    load_percent=26.67,cuts_at_cap=40,
    calculation='Até 2,00 m ×4,8 W/m =9,6 W; corrente 0,8 A. 9,6/36 =26,7% da fonte. Cortes a cada 50 mm.')
data['cost'] = dict(components_total_brl=float(total),known_components_subtotal_brl=float(total),
    complete_total_brl=None,installed_total_brl=None,
    payment_basis='À vista: Pix nas fitas/perfis e Pix ou boleto nas fontes; plafon no preço exibido. Sem cupons condicionais.',
    card_advertised_components_total_brl=float(card_total),
    card_note='Soma dos preços de cartão exibidos, sem juros adicionais: as condições e parcelas variam entre as lojas.',
    includes=['1 plafon','1 rolo completo de fita 4000 K','1 rolo completo de fita 3000 K','2 perfis de 2 m com difusores, 8 tampas e 8 garras no total','2 fontes independentes'],
    excludes=['Fretes','Corte e montagem dos perfis','Cabos, caixas, conectores e materiais para proteção/vedação das terminações','Interruptores e placas','Fixações ao substrato','Mão de obra elétrica'],
    previous_selection_comparable_brl=float(old_with_mirror),saving_vs_L01_brl=float(saving),
    saving_percent=round(float(saving/old_with_mirror*100),2),
    group_totals_brl={'teto':141.90,'espelho':288.72,'indireta':182.02},
    comparison_note='L01 645,83 sem a fita do espelho +mesma fita agora precificada em169,26 =815,09. A diferença é entre componentes das duas seleções, não desconto contratado ou economia lançada no total do apartamento.',
    note='Total dos componentes principais fechado com preços publicados e conferidos na página real. Total instalado não cotado. Rolos inteiros contabilizados, inclusive sobras.')
data['commercial_review'] = dict(
    mirror_preserved={'sku':'CLX-FT331240','kelvin':4000,'cri':'>90','cob':True,'length_m':1.1,'watts':13.2,'raw_lumens':1320},
    indirect_change={'old_w_per_m':12,'new_w_per_m':4.8,'power_reduction_percent':60,'old_cri':'>90','new_cri':'>80','reason':'Uso complementar oculto; preservar IRC alto no espelho. Luz ambiente mais suave, com difusor e reflexão, sem pontos diretamente visíveis.'},
    source_saving_brl=138.78,indirect_strip_saving_brl=63.67,
    roll_strategy='Não foi localizada oferta pública por metro do SKU exato do espelho com custo total e fornecimento confirmáveis. Comprados por rolo de 5 m no cálculo: sobra3,9 m de4000 K e pelo menos3 m de3000 K. Não dividir artificialmente o valor do rolo pelo comprimento usado para anunciar uma economia inexistente.',
    candidates=[
        {'product':'Mean Well LPV-20-12 +LPV-35-12','price_brl':308.88,'decision':'Substituídas: custo maior para estas cargas; não foi demonstrada vantagem prática que justifique a diferença neste projeto.'},
        {'product':'Opus OPS31002 2 unidades','price_brl':170.10,'decision':'Selecionadas: tensão, corrente e IP documentados; ambas com folga e acionamentos independentes. Envoltória/lote devem ser conferidos.'},
        {'product':'Romalux60029 30 W, IP67','unit_reference_brl':112.44,'decision':'Mais cara que a Opus encontrada e sem vantagem necessária para as cargas nominais.'},
        {'product':'Cristallux COB CLX-FT331240 4000 K','price_brl':169.26,'decision':'Mantida: preserva IRC>90, COB, comprimento e fluxo da seleção anterior; agora com preço e estoque visíveis.'},
        {'product':'Eklart EKF4496HL9065','unit_reference_brl':252.10,'decision':'Mais cara por rolo; não oferece economia sobre manter a COB Cristallux. Não adotada.'},
        {'product':'Gaya COB IP65 5630','unit_reference_brl':128.80,'decision':'IRC80 da variante não atende ao espelho; descartada apesar do preço menor.'},
    ])
holds = list(old['execution_holds'])
holds[4] = 'Indireta: medir o trecho protegido da faixa, cortar somente nas marcas de50 mm e manter até2 m neste orçamento. Não completar metragem entrando no box. Suporte elétrico e faixa hidráulica com manutenção independente.'
holds[5] = 'Fontes Opus: instalar em compartimento técnico seco, ventilado, acessível e substituível, fora da guarda do espelheiro. Reservar até276 mm de comprimento por fonte até conhecer o lote; não assumir as dimensões das antigas Mean Well. Seguir etiqueta/manual, inclusive aterramento quando indicado. Não cobrir com isolamento.'
holds[6] = 'Três teclas físicas: teto; fonte do espelho; fonte da indireta. Uma fonte por retorno, saídas independentes. Acionamento liga/desliga; não usar dimmer de parede nestas fontes nem na fita indireta não dimerizável.'
data['execution_holds'] = holds
data['evidence_notes'] = [
    'Preços e botões de compra/estoque lidos no navegador, sem adicionar ao carrinho ou enviar dados. Buscadores tinham versões divergentes (inclusive preço sob consulta); prevalece a página real verificada.',
    'Sem alegação de igual durabilidade ou menor flicker entre marcas: a seleção usa características documentadas, não ensaio comparativo independente.',
    'Os fluxos nominais da indireta variam em catálogos históricos da Cristallux; especificação atual informa460 lm/m. Conferir etiqueta do lote. Não adotar o fluxo antigo de230 lm/m como se fosse o mesmo lote atual.',
    'Fontes Opus: existem versões dimensionais e garantias diferentes sob o código31002. O preço da loja não comprova entrega da versão mais nova. O cálculo usa apenas dados elétricos coincidentes de12 V/3 A/36 W, IP67.',
    'Não substituir a fita do espelho por SMD IRC80 ou COB IP20 apenas por título parecido. A indireta mudou de forma expressa para021965, preservando3000 K e IP65 da fita intacta.',
]
data['sources'] = [s for s in old['sources'] if s['title'] not in ('indireta','fonte20','fonte35')]+[
    {'title':'Cristallux indireta4,8 W/m: ficha atual','url':technical_indirect},
    {'title':'Opus OPS31002: ficha atual','url':technical_source},
    {'title':'Catálogo Opus2021: versão270 mm','url':'https://dellasiluminacao.com.br/wp-content/uploads/2021/05/Catalogo-2021-Opusled-Oficial_compressed.pdf'}]
data['budget_mapping'] = dict(
    source='01_Projeto/Orcamento_R43_2026-10-22/Orcamento_R43.md',
    ceiling={'code':'Parte de L04','amount_brl':141.90,'note':'Substitui apenas a parcela do banheiro; não elimina o plafon da lavanderia.'},
    mirror={'code':'L05','amount_brl':288.72,'note':'Composição completa do espelho neste levantamento: fita, fonte e um perfil. Não somar novamente seus componentes em L06.'},
    indirect={'code':'Parte de L06','amount_brl':182.02,'note':'Detalhamento da indireta do banheiro dentro da verba geral de perfis/fitas/fontes; não lançar612,64 em acréscimo às verbas antigas.'},
    installation={'code':'I01','note':'Montagem elétrica já pertence à verba de instalações; o valor específico do banheiro não foi cotado.'},
    global_budget_changed=False,
    reason='L06 é verba compartilhada sem desdobramento completo dos outros cômodos; detalhar a parcela do banheiro não autoriza lançar economia global ou reduzir verba dos demais ambientes.')
write(HERE/'Luminarias_selecao_L02.json',data)
write(HERE/'Verificacao_luminarias_L02.json',{
    'date':'2026-10-24','revision':'L02','components_total_brl':float(total),
    'total_by_group_brl':data['cost']['group_totals_brl'],
    'driver_loads_percent':[36.67,26.67],'nominal_loads_w':[13.2,9.6],
    'checks':['4000 K e IRC>90 do mesmo SKU de espelho preservados','3 retornos e 2 fontes independentes','Fita do espelho:550/25=22 módulos por barra','Indireta até2000/50=40 módulos','8 tampas/8 garras fornecidas nos2 perfis; previsão de6 tampas/8 garras','Soma com Decimal; preços de rolos inteiros','Não houve compra, envio, publicação externa ou mudança no CAD'],
    'not_validated':['Encaixe interno e dissipação do perfil','Terminações e proteção da montagem completa','Curso real da torneira/mão junto à barra inferior','Cotas e volumes reais de instalação','Iluminância, ofuscamento e uniformidade no rosto','Estoque reservado, fretes e preço de instalação']})

rows = ''.join(f'<tr><td>{h(i["product"])}</td><td>{i["quantity"]} {h(i["unit"])}</td><td>{money(i["price_brl"])}</td><td>{money(D(str(i["price_brl"]))*i["quantity"])}</td><td><a href="{h(i["buy_url"])}">{h(i["seller"])}</a><br><small>{h(i["availability"])}</small></td></tr>' for i in bom)
links = ''.join(f'<li><a href="{h(s["url"])}">{h(s["title"])}</a></li>' for s in data['sources'])
holds_html = ''.join(f'<li>{h(s)}</li>' for s in holds)
svg = re.search(r'<svg .*?</svg>',(HERE/'Luminarias_selecao_L01.html').read_text(encoding='utf-8'),re.S)[0]
page = f'''<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Banheiro · luminárias L02 · {money(total)}</title>
<style>body{{max-width:1100px;margin:32px auto;padding:0 20px;background:#faf8f3;color:#29352f;font:16px/1.55 system-ui}}h1{{font-size:32px}}a{{color:#32634f}}table{{width:100%;border-collapse:collapse;background:white}}th,td{{padding:12px;border-bottom:1px solid #ddd;text-align:left;vertical-align:top}}th{{background:#e9eee6}}.note{{padding:18px;border-left:4px solid #648773;background:#edf1e9}}.price{{font-size:34px;font-weight:700;margin:8px 0}}small{{font-size:13px}}li{{margin:12px 0}}svg{{width:100%;height:auto;background:white}}@media(max-width:650px){{.scroll{{overflow-x:auto}}table{{min-width:650px}}}}@media print{{body{{font-size:10pt}}tr,svg{{break-inside:avoid}}}}</style>
<main><p><a href="Fechamento.html#B05">← Fechamento do banheiro</a></p><h1>Luminárias do banheiro · custo-benefício</h1><p>24/10/2026 · L02 · substitui a seleção L01</p>
<div class="note"><p class="price">{money(total)} à vista</p><p><b>Total dos componentes principais:</b> plafon, dois rolos de fita, dois perfis com difusores/tampas/garras e duas fontes. Todos os itens têm preço publicado conferido na loja. Frete, corte/montagem, terminações, cabos, caixas, interruptores, fixações e mão de obra elétrica ficam na instalação e não estão incluídos.</p><p><b>Economia de {money(saving)} ({data['cost']['saving_percent']:.2f}%)</b> sobre a L01 completada com o preço da mesma fita do espelho. Total instalado ainda não cotado.</p></div>
<div class="scroll"><table><tr><th>Grupo</th><th>Composição e custo</th><th>O que mudou</th></tr>
<tr><td>Teto ·3000 K</td><td>Galaxy Firefly9605 branco,25 W,2000 lm,IP44.<br><b>R$141,90</b></td><td>Mantido. Sobrepor, fora do box; ponto real a conferir.</td></tr>
<tr><td>Espelho ·4000 K</td><td>Cristallux COB CLX-FT331240 /221513; duas barras de550 mm,13,2 W,IRC&gt;90,1320 lm antes do difusor. Um perfil MOV4329 cortado em dois corpos de560 mm e uma fonte Opus36 W.<br><b>R$288,72</b></td><td><b>Qualidade da fita preservada:</b> mesmo SKU, temperatura, IRC, COB, comprimento e fluxo da L01. Fonte mais econômica, com folga de potência.</td></tr>
<tr><td>Indireta ·3000 K</td><td>Cristallux SMD CLX-FT200530 /021965; até2 m,9,6 W,IRC&gt;80,até920 lm antes do difusor/reflexão. Um perfil MOV4329 e uma fonte Opus36 W.<br><b>R$182,02</b></td><td>Fita de4,8 W/m substitui12 W/m:60% menos potência neste grupo. Luz complementar oculta, com difusor e reflexão. Fita não dimerizável; comando liga/desliga preservado.</td></tr></table></div>
<h2>Lista de compra com valores completos</h2><div class="scroll"><table><tr><th>Produto</th><th>Quantidade de compra</th><th>Unitário à vista</th><th>Total</th><th>Link da loja</th></tr>{rows}<tr><th colspan="3">Total de componentes à vista</th><th>{money(total)}</th><td>Pix; fontes também boleto. Sem cupons.</td></tr></table></div>
<p>Preços de cartão exibidos somam <b>{money(card_total)}</b>, sem juros adicionais; as condições e quantidades de parcelas variam por loja. Não houve compra, reserva de estoque, contato com fornecedor ou envio de dados. Os valores podem mudar até a compra.</p>
<h2>Por que esta revisão custa menos</h2><p>As duas fontes Mean Well custavamR$308,88. Duas Opus OPS31002 custamR$170,10: redução de<b>R$138,78</b>. A fita indireta caiu deR$126,23 paraR$62,56: redução de<b>R$63,67</b>. Plafon e perfis foram mantidos. O preço deR$169,26 da fita4000 K foi confirmado na página real, com estoque disponível; o resultado antigo “sob consulta” vinha de uma leitura desatualizada.</p>
<p>A comparação usa a L01 aR$645,83 mais a mesma fita do espelho agora precificada emR$169,26: <b>R$815,09</b>. A redução para{money(total)} não é uma economia calculada contra um subtotal que excluía a fita. Não foi demonstrada vantagem de manutenção/durabilidade que justificasse o preço maior das Mean Well neste conjunto; também não se afirma desempenho idêntico entre marcas sem ensaio independente.</p>
<h2>Rolos e sobras</h2><p>O total inclui os dois rolos completos de5 m. Uso nominal:1,10 m no espelho e até2 m na indireta. Sobras:3,90 m de4000 K e pelo menos3 m de3000 K. Não foi localizada oferta pública por metro do mesmo SKU do espelho com custo de fornecimento confirmável; por isso o valor fechado conta os rolos, sem rateio fictício. Não ligar os rolos inteiros às fontes: o orçamento elétrico considera apenas os trechos instalados.</p>
<h2>Fontes, comandos e manutenção</h2><p>Uma Opus OPS31002 de12 V/3 A/36 W por grupo de fita:13,2 W/1,1 A no espelho, ocupando36,7% da fonte; até9,6 W/0,8 A na indireta, ocupando26,7%. Três teclas físicas: teto; fonte do espelho; fonte da indireta. Duas barras do espelho ligadas em paralelo. As fontes e suas saídas permanecem independentes; acionamento liga/desliga.</p>
<p>O fabricante atual informa172×21×20 mm,policarbonato e3 anos de garantia paraOPS31002. A oferta da Luz de Casa descreve a versão de276×20×20 mm,alumínio e1 ano, coerente com catálogos anteriores. Para esta compra, reservar até276 mm de comprimento por fonte e não prometer a versão nova pelo preço da antiga. Etiqueta e lote devem confirmar12 V/3 A/36 W/IP67. Instalar em compartimento técnico seco, ventilado e acessível, fora do armazenamento do espelheiro.</p>
<h2>Espelho preservado</h2>{svg}<p>Perfis brancos Nordecor MOV4329:2 barras de2 m, cada uma com difusor,4 tampas e4 garras. Primeira barra cortada em2 corpos nominais de560 mm; cada um recebe550 mm da fitaCOB. Segunda barra: indireta de até2 m, a medir. Previsão total:6 tampas/8 garras; fornecimento8 tampas/8 garras. Não alterar portas, vidro ou guarda interna.</p>
<p>O corpo do perfil tem7 mm de projeção e17 mm de altura, dentro da antiga envoltória externa. A montagem interna da fita10×3 mm, presilhas, soldas, terminais e dissipação ainda precisa de conferência de bancada. A barra inferior depende da abertura real da torneira e do espaço da mão. O CAD principal foi preservado.</p>
<h2>Condições de instalação</h2><p>IP65 é da fita intacta; o perfil éIP20. IP67 das fontes não classifica a luminária montada. Terminações cortadas devem receber proteção compatível com a posição real. A revisão fecha componentes e preço de compra, sem transformar o conjunto em luminária certificada ou liberar instalação por coordenadas nominais.</p><ol>{holds_html}</ol>
<h2>Como entra no orçamento</h2><p>TetoR$141,90 detalha a parcela de banheiro daL04; espelhoR$288,72 substitui o conjuntoL05; indiretaR$182,02 detalha parte da verba geralL06. Não adicionar{money(total)} novamente por cima dessas verbas. Montagem elétrica pertence àI01; o custo do banheiro ainda não foi discriminado. O total geral do apartamento foi preservado porqueL06 também atende outros cômodos e ainda não foi desdobrada.</p>
<h2>Fontes técnicas e conferência</h2><ul>{links}</ul><p><a href="Luminarias_selecao_L02.json">Especificação e comparações JSON</a> · <a href="Verificacao_luminarias_L02.json">Conferência de cargas, cortes e total</a> · <a href="Luminarias_selecao_L01.html">Histórico L01</a></p></main></html>'''
(HERE/'Luminarias_selecao_L02.html').write_text(page,encoding='utf-8')

materials = read(HERE/'Iluminacao_e_materiais.json')
materials['lighting'].update(groups=data['groups'],selection='Luminarias_selecao_L02.json',components_selected=True,
    fixtures_selected=False,priced_components_complete=True,components_total_brl=float(total),
    power_supplies='2×Opus OPS31002,12 V/3 A/36 W/IP67, uma por grupo; compartimento técnico acessível fora da guarda. Reservar276 mm de comprimento por fonte até conferir o lote.',sources=data['sources'])
materials['approved']['controls'] = 'Três grupos físicos independentes; seleção de componentes e total de material L02; instalação a compatibilizar'
write(HERE/'Iluminacao_e_materiais.json',materials)
for filename in ['Escolhas.json','Situacao.json']:
    record = read(HERE/filename)
    if filename=='Escolhas.json': record['controls']=materials['approved']['controls']
    else:
        record['choices']['controls']=materials['approved']['controls']
        b05=next(s for s in record['sections'] if s['id']=='B05')
        b05.update(status='Componentes e total de compra definidos em L02; instalação condicionada',
            result='Total dos componentesR$612,64 à vista, sem frete e instalação. Teto3000 K: Galaxy Firefly9605. Espelho4000 K: mesma Cristallux COB CLX-FT331240,2×550 mm,13,2 W,IRC>90. Indireta3000 K: CLX-FT200530 SMD4,8 W/m,até2 m/9,6 W.2 fontes Opus OPS31002 e2 perfis MOV4329. Economia comparávelR$202,45 sobreL01 com fita do espelho incluída.',
            next='Conferir canal/dissipação, terminações, difusão no rosto e lote das fontes. Perfil IP20 não se tornaIP65 pela fita. Posição inferior depende da torneira; cotas da indireta e instalação real ainda serão verificadas. Total instalado/fretes não cotados.',
            source='Luminarias_selecao_L02.html')
    write(HERE/filename,record)
closing=(HERE/'Fechamento.html').read_text(encoding='utf-8')
replacement=f'<tr id="B05"><td><b>B05 · Iluminação</b><p>{h(b05["status"])}</p></td><td>{h(b05["result"])}</td><td>{h(b05["next"])}<p><a href="Luminarias_selecao_L02.html">Seleção L02: total e links de compra</a></p></td></tr>'
closing,n=re.subn(r'<tr id="B05">.*?</tr>',lambda m:replacement,closing,count=1,flags=re.S)
assert n==1
closing=closing.replace('R02 local · iluminação L01','R03 local · iluminação L02').replace('href="Luminarias_selecao_L01.html">Luminárias: seleção e links','href="Luminarias_selecao_L02.html">Luminárias L02: total e links')
(HERE/'Fechamento.html').write_text(closing,encoding='utf-8')
old_page=(HERE/'Luminarias_selecao_L01.html').read_text(encoding='utf-8')
banner='<p class="note" id="historico-l02"><b>Histórico L01, superado.</b> <a href="Luminarias_selecao_L02.html">Abrir L02: componentes R$612,64, com IRC do espelho preservado.</a></p>'
if 'id="historico-l02"' not in old_page:
    old_page=old_page.replace('<main>','<main>'+banner,1)
(HERE/'Luminarias_selecao_L01.html').write_text(old_page,encoding='utf-8')

# Integração nas fontes canônicas; as revisões anteriores permanecem históricas.
source_path=ROOT/'01_Projeto/Estudo_interativo/src/data.js'
source=source_path.read_text(encoding='utf-8')
card={
 'name':'Teto 3000 K +espelho 4000 K +indireta 3000 K',
 'dimensions':'Firefly25 W; espelho2×550 mm /13,2 W; indireta até2 m /9,6 W',
 'choice':'L02: componentes R$612,64 à vista; custo-benefício',
 'source':'24/10/2026',
 'measure':'Montagem e posições a validar; frete/instalação fora do total',
 'notes':'Teto Galaxy Firefly9605 branco IP44,3000 K. Espelho: mesma Cristallux COB CLX-FT331240,4000 K,IRC>90,1,10 m. Indireta: Cristallux SMD CLX-FT200530,3000 K,4,8 W/m,IRC>80,até2 m.2 fontes Opus OPS31002 12 V/3 A/36 W/IP67,2 perfis MOV4329 com difusores; três comandos separados. Total de componentesR$612,64 à vista, rolos inteiros incluídos;R$202,45 abaixo da L01 com espelho precificado. Perfil IP20 não viraIP65 pela fita. Encaixe interno, terminais, dissipação e luz no rosto a conferir; barra inferior depende da torneira. Reservar até276 mm por fonte até conferir o lote. Links: Banheiro/Fechamento_pre_entrega_2026-10-24/Luminarias_selecao_L02.html. Sem compra ou alteração no CAD.'}
source,n=re.subn(r'Object\.assign\(ITEMS\.find\(i=>i\.id==="bathlight"\),.*?\);',lambda m:'Object.assign(ITEMS.find(i=>i.id==="bathlight"),'+json.dumps(card,ensure_ascii=False,separators=(',',':'))+');',source,count=1)
assert n==1
source_path.write_text(source,encoding='utf-8')

note='**24/10/2026 — luminárias do banheiro L02:** total dos componentes **R$612,64 à vista**, sem frete e instalação. Espelho preservado: mesma fita COB4000 K/IRC>90,2×550 mm. Indireta3000 K: Cristallux CLX-FT200530 de4,8 W/m;2 fontes Opus OPS31002; teto Firefly9605 e perfis MOV4329 mantidos. [Valores e links de compra](Banheiro/Fechamento_pre_entrega_2026-10-24/Luminarias_selecao_L02.html). Economia de referênciaR$202,45 contraL01 com a fita do espelho incluída. Rolos inteiros no total, sem compra ou instalação liberada; orçamento global preservado para evitar duplicidade comL04/L05/L06. A L01 abaixo é histórico.\n\n'
for filename in ['Painel_de_decisoes.md','Registro_de_decisoes.md','Resumo.md','Lista_curta_luminarias_e_madeira_R00.md']:
    path=ROOT/'01_Projeto'/filename
    current=path.read_text(encoding='utf-8-sig')
    if not current.startswith('**24/10/2026 — luminárias do banheiro L02:**'):
        path.write_text(note+current,encoding='utf-8')

path=HERE.parent/'README.md'
current=path.read_text(encoding='utf-8-sig')
first='**24/10/2026 — iluminação L02:** [total e links de compra](Fechamento_pre_entrega_2026-10-24/Luminarias_selecao_L02.html): **R$612,64 à vista em componentes**, sem frete e instalação. Teto3000 K: Firefly9605; espelho4000 K: mesma Cristallux COB CLX-FT331240/IRC>90; indireta3000 K: Cristallux SMD CLX-FT200530/4,8 W/m.2 fontes Opus OPS31002 e2 perfis MOV4329 com difusores. Três comandos preservados. Corte/montagem, terminais, encaixe no perfil e implantação condicionados; compra não realizada.'
current=first+'\n\n'+current.split('\n\n',1)[1]
path.write_text(current,encoding='utf-8')

path=HERE.parent/'Decisoes_consolidadas_2026-09-18.md'
current=path.read_text(encoding='utf-8-sig')
current=current.replace('Iluminação L01: seleção e links','Iluminação L02: total e links').replace('Luminarias_selecao_L01.html','Luminarias_selecao_L02.html')
current=current.replace('e indireta 3000 K CLX-FT431230, perfis MOV 4329 e fontes LPV-20-12/LPV-35-12','e indireta 3000 K SMD CLX-FT200530/4,8 W/m, perfis MOV4329 e2 fontes Opus OPS31002; componentes R$612,64 à vista sem frete/instalação')
current=re.sub(r'^\| Iluminação \|.*$', '| Iluminação | **Teto3000 K, espelho4000 K e indireta3000 K**, três comandos físicos. L02: componentesR$612,64 à vista. Firefly9605; espelho Cristallux COB CLX-FT331240/IRC>90; indireta SMD CLX-FT200530/4,8 W/m; MOV4329 e2 fontes Opus OPS31002 | Sem frete/instalação. Encaixe/dissipação, terminais/proteção e luz no rosto a conferir. Barra inferior condicionada à torneira; até2 m de indireta é limite do kit. Fontes com versões dimensionais diferentes: conferir lote |',current,flags=re.M)
path.write_text(current,encoding='utf-8')

path=ROOT/'01_Projeto/Estado_atual.md'
current=path.read_text(encoding='utf-8-sig')
current=current.replace('[Componentes selecionados L01](Banheiro/Fechamento_pre_entrega_2026-10-24/Luminarias_selecao_L01.html)','[Componentes L02: R$612,64 à vista](Banheiro/Fechamento_pre_entrega_2026-10-24/Luminarias_selecao_L02.html)')
current=current.replace('os componentes já estão selecionados em L01, faltando cotação de 4000 K, prova do perfil e montagem','os componentes estão selecionados e precificados em L02, faltando prova do perfil, terminações e montagem')
path.write_text(current,encoding='utf-8')

budget_root=ROOT/'01_Projeto/Orcamento_R43_2026-10-22'
budget_note='> **24/10/2026 — iluminação do banheiro L02:** [composição e links](../Banheiro/Fechamento_pre_entrega_2026-10-24/Luminarias_selecao_L02.html), componentes **R$612,64 à vista**, sem frete/instalação. TetoR$141,90 detalha a parte do banheiro emL04; espelhoR$288,72 substituiL05; indiretaR$182,02 detalha parte deL06. Não somar o total novamente às verbas existentes. I01 já prevê montagem elétrica. O total geral e a meta de iluminação ficam preservados até desdobrarL06 nos demais ambientes.\n\n'
for filename in ['Orcamento_R43.md','LEIA-ME.md']:
    path=budget_root/filename
    current=path.read_text(encoding='utf-8-sig')
    if not current.startswith('> **24/10/2026 — iluminação do banheiro L02:**'):
        path.write_text(budget_note+current,encoding='utf-8')
write(budget_root/'Reconciliacao_iluminacao_banheiro_L02.json',dict(date='2026-10-24',components_total_brl=float(total),**data['budget_mapping']))
print(json.dumps({'components_total_brl':float(total),'saving_brl':float(saving),'card_total_brl':float(card_total),'groups':data['cost']['group_totals_brl']},ensure_ascii=False))
