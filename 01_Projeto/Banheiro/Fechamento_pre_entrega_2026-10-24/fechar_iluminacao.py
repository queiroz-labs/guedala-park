"""Registra a seleção de componentes; não libera instalação nem altera o CAD."""
from pathlib import Path
from html import escape as h
from decimal import Decimal
import json, re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]

def read(name):
    return json.loads((HERE/name).read_text(encoding='utf-8-sig'))

def save(name, data):
    (HERE/name).write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

urls = {
 'teto': 'https://galaxyled.com.br/produtos?product=PLAFON+FIREFLY+25W+3000K+REDONDO&uniqMod=000108&uniqProd=0000025889&uniqTp=00080',
 'comprar_teto': 'https://www.magazineluiza.com.br/plafon-de-sobrepor-firefly-redondo-branco-30cm-led-25w-3000k-bivolt-galaxy-led/p/hf39c74bce/cj/plfn/?seller_id=parisluzcombr',
 'espelho': 'https://www.cristallux.com.br/produto/fita-led-cristall-pro-dry-cob-5mt-12v-12w-m-4000k-1200lm-m-ip65-480led-m-irc-90',
 'comprar_espelho': 'https://www.3reletrica.com.br/fita-de-led-cob-480led/m-ip65-4000k-12v-5-metros-dimerizavel-cristallux',
 'indireta': 'https://www.cristallux.com.br/produto/fita-led-cristall-pro-dry-cob-5mt-12v-12w-m-3000k-1200lm-m-ip65-480led-m-irc-90',
 'comprar_indireta': 'https://loja.cemel.ind.br/produtos/fita-led-cristall-pro-dry-cob-480led-m-ip65-221506/',
 'perfil': 'https://nordecor.com.br/produto/perfil-de-sobrepor-mov-17x7mm/',
 'comprar_perfil': 'https://www.cialight.com.br/perfil-mov-de-sobrepor-17x7mm-2m-branco-nordecor-4329',
 'fonte20': 'https://www.meanwell.com/Upload/PDF/LPV-20/LPV-20-SPEC.PDF',
 'fonte35': 'https://www.meanwell.com/Upload/PDF/LPV-35/LPV-35-SPEC.PDF',
 'comprar_fonte20': 'https://www.fontesmeanwell.com.br/fonte-chaveada-p-led-20w-90-264vca-127-370vcc-saida-12vcc-1-67a-lpv-20-12-mean-well',
 'comprar_fonte35': 'https://www.fontesmeanwell.com.br/fonte-chaveada-p-led-36w-90-264vca-127-370vcc-saida-12vcc-1a-lpv-35-12-mean-well',
}
groups = [
 dict(id='B11', function='Geral do teto', kelvin=3000, product='Galaxy LED Firefly 9605',
      installed_quantity=1, watts=25, lumens=2000, cri='>80', ip_component='IP44',
      input='100–240 Vca, bivolt', finish='Branco, redondo, difusor opalino',
      envelope_mm=[300,300,50],
      dimension_note='Diâmetro 300 mm; anúncio informa 45 mm de altura e catálogo Galaxy 50 mm. Reservar 50 mm e conferir o lote.',
      mounting='Sobrepor no teto, fora do box; posição do ponto existente a conferir.',
      product_url=urls['teto'], buy_url=urls['comprar_teto']),
 dict(id='B09', function='Frontal do espelho', kelvin=4000,
      product='Cristallux Cristall Pro Dry COB CLX-FT331240', code='221513', ean='7908024221513',
      installed_length_m=1.10, segments_mm=[550,550], cut_pitch_mm=25, strip_section_mm=[10,3],
      watts_per_m=12, watts=13.2, current_a=1.1, lumens_per_m=1200, lumens_before_diffuser=1320,
      cri='>90', ip_component='IP65 da fita intacta; cortes e montagem não classificados', input='12 Vcc',
      profile='Nordecor MOV 4329 branco, alumínio e difusor PC, seção externa 17 × 7 mm',
      nominal_profile_lengths_mm=[560,560],
      driver='Mean Well LPV-20-12, 12 Vcc, 1,67 A, 20 W, IP67',
      mounting='Duas barras horizontais fixas acima/abaixo do espelheiro; luz voltada para o rosto. Sem fios nas portas.',
      status='Componentes selecionados; posição inferior, encaixe interno e proteção da montagem condicionados.',
      product_url=urls['espelho'], buy_url=urls['comprar_espelho']),
 dict(id='B10', function='Indireta de ambiente', kelvin=3000,
      product='Cristallux Cristall Pro Dry COB CLX-FT431230', code='221506', ean='7908024221506',
      design_length_cap_m=2, cut_pitch_mm=25, strip_section_mm=[10,3], watts_per_m=12,
      watts_at_length_cap=24, current_at_length_cap_a=2, lumens_per_m=1200,
      lumens_before_diffuser_at_length_cap=2400, cri='>90',
      ip_component='IP65 da fita intacta; cortes e montagem não classificados', input='12 Vcc',
      profile='Nordecor MOV 4329 branco, alumínio e difusor PC, seção externa 17 × 7 mm',
      driver='Mean Well LPV-35-12, 12 Vcc, 3 A, 36 W, IP67',
      mounting='Oculta na faixa do canto do teto, emitindo para teto/parede; não apontar diretamente aos olhos.',
      status='Comprimento de até 2 m é limite do kit dimensionado, não medição ou aprovação de um traçado de 2 m.',
      product_url=urls['indireta'], buy_url=urls['comprar_indireta']),
]
bom = [
 dict(product='Galaxy LED Firefly 9605, 3000 K', quantity=1, unit='unidade', price_brl=141.90,
      seller='Paris Luz pelo Magalu', availability='Anúncio com compra; entrega depende do CEP', buy_url=urls['comprar_teto']),
 dict(product='Cristallux CLX-FT331240 / 221513, 4000 K', quantity=1, unit='rolo de 5 m',
      price_brl=None, seller='3R Soluções Elétricas', availability='Consulte o preço; estoque e fornecimento não confirmados',
      buy_url=urls['comprar_espelho'], consumed_m=1.1, remainder_m=3.9),
 dict(product='Cristallux CLX-FT431230 / 221506, 3000 K', quantity=1, unit='rolo de 5 m', price_brl=126.23,
      seller='Cemel', availability='Página indicava última peça; reconfirmar na compra', buy_url=urls['comprar_indireta'],
      consumed_m_cap=2, remainder_m_min=3),
 dict(product='Nordecor MOV 4329, branco, com difusor', quantity=2, unit='barra de 2 m', price_brl=34.41,
      price_evidence='Preço indexado na categoria da Cia Light; página individual não exibe preço no extrator. Referência a reconfirmar.',
      seller='Cia Light', availability='Despacho anunciado em até 10 dias úteis, além do transporte', buy_url=urls['comprar_perfil'],
      included_total={'caps':8,'clips':8}, needed_total={'caps':6,'clips':8},
      cut_plan_mm=[[560,560],[2000]],
      cut_note='Primeira barra: dois perfis nominais de 560; segunda: indireta até 2000. Ajustar tampa, saída de cabo e corte útil. Não cortar fita a 560: seus trechos são 550.'),
 dict(product='Mean Well LPV-20-12, 12 V / 1,67 A / 20 W', quantity=1, unit='unidade', price_brl=140.92,
      seller='Fontes Mean Well / MCEIG', availability='Pronta entrega anunciada; preço sem impostos calculados no checkout',
      envelope_mm=[118,35,26], buy_url=urls['comprar_fonte20']),
 dict(product='Mean Well LPV-35-12, 12 V / 3 A / 36 W', quantity=1, unit='unidade', price_brl=167.96,
      seller='Fontes Mean Well / MCEIG', availability='Pronta entrega anunciada; preço sem impostos calculados no checkout',
      envelope_mm=[148,40,30], buy_url=urls['comprar_fonte35']),
]
subtotal = float(sum(Decimal(str(i['price_brl']))*i['quantity'] for i in bom if i['price_brl'] is not None))
checks = dict(
 mirror=dict(length_m=1.10, power_w=13.2, current_a=1.1, driver_w=20, load_percent=66,
             cuts_per_segment=22, calculation='2 × 0,55 m × 12 W/m = 13,2 W; dois trechos em paralelo, nunca em série.'),
 indirect=dict(max_length_m=2, power_w=24, current_a=2, driver_w=36, load_percent=66.67,
               cuts_at_cap=80, calculation='2,00 m × 12 W/m = 24 W; 24/36 = 66,7%. Não alimentar o rolo inteiro de 60 W.'),
 nominal_mirror_fit=dict(cabinet_width_mm=600, former_bar_envelope_mm=[560,7,20],
    new_body_envelope_mm=[560,7,17], interpretation='Corpo externo dentro da antiga envoltória. Não inclui presilhas, tampas, soldas, fio ou suporte e não comprova encaixe da fita 10 × 3 mm no interior do perfil.',
    door_z_ranges_mm={'lower_bar':[1110,1127],'cabinet':[1150,1900],'upper_bar':[1910,1927]},
    nominal_vertical_gaps_mm={'lower_to_cabinet':23,'upper_to_cabinet':10},
    validation='Comparação analítica de envoltórias nominais, sem novo ensaio de giro ou mudança no CAD.'),
 lighting=dict(flux_note='Fluxos de fita são anteriores às perdas do difusor e da reflexão. Não equivalem a lux no rosto ou no piso.',
    test='Pré-montar no espelheiro, observar rosto/maquiagem, reflexos com portas fechadas e abertas e ofuscamento. Se o resultado falhar, rever óptica/posição antes de instalar.'),
)
holds = [
 'Comprar o plafon pelo SKU 9605 / 3000 K; conferir etiqueta e altura do lote. Produto IP44 não libera automaticamente posição dentro ou junto ao box.',
 'Antes da compra dos perfis/fita em quantidade: conferir fisicamente ou por desenho do canal o encaixe da fita siliconada 10 × 3 mm, a dissipação para 12 W/m e a passagem das soldas. A largura externa de 17 mm não prova a largura interna.',
 'Perfil MOV é IP20. A proteção IP65 pertence à fita intacta e IP67 às fontes encapsuladas. Exigir terminais/cortes protegidos conforme fabricante e adequação do conjunto à posição real pelo responsável elétrico; não anunciar luminária montada IP65.',
 'Manter as barras em suporte fixo independente das portas. Montar e testar sem reduzir armazenamento, sem fixar em vidro e sem colar fita diretamente no MDF. Posição inferior só é liberada depois do curso real da torneira e do espaço para a mão.',
 'Na indireta, medir o trecho protegido da faixa do teto e cortar na marcação de 25 mm, dentro do limite de 2 m. Não avançar para o box para completar comprimento. Faixa hidráulica e suporte elétrico independentes, com manutenção de ambos.',
 'Instalar as duas fontes em compartimento técnico seco, ventilado, acessível e removível, fora do armazenamento do espelheiro e da caixa do chuveiro. Não enclausurar ou cobrir fontes com isolamento. Conferir curvas térmicas e potência disponível na condição final.',
 'Três teclas físicas: teto; fonte do espelho; fonte da indireta. Ligar cada fonte em seu próprio retorno de rede. Não unir saídas das fontes nem misturar os dois grupos de fitas. Fontes LPV escolhidas para liga/desliga; não usar dimmer de parede na entrada delas.',
 'Cabos, caixas, conectores, fixações no substrato e proteção do circuito serão definidos pelo eletricista conforme percurso e banheiro real. Terminações da fita fazem parte da encomenda montada, não estão incluídas nos preços dos rolos.',
]
sources = [{'title': k, 'url': v} for k,v in urls.items() if not k.startswith('comprar_')]
data = dict(date='2026-10-24', revision='L01',
 scope='Seleção técnica para o projeto e cotação. Temperaturas aprovadas por Elias. Novos modelos são a seleção proposta nesta rodada; não registrar compra ou aceite pessoal de SKU que ainda não ocorreu.',
 temperatures_approved=True, components_selected=True, complete_luminaires_released=False,
 installation_released=False, purchase_made=False, main_cad_modified=False,
 groups=groups, bom=bom, checks=checks, execution_holds=holds,
 cost=dict(known_components_subtotal_brl=subtotal, complete_total_brl=None,
   excludes=['Fita 4000 K sob consulta','Fretes','Tributos adicionais no checkout das fontes','Montagem e proteção de terminações','Cabos e caixas','Interruptores/placas','Fixações e mão de obra'],
   note='Referência parcial; não é orçamento fechado nem economia lançada no orçamento geral. Rolo inteiro contado na compra; sobras não foram creditadas como economia.'),
 evidence_notes=[
   'Cristallux 3000 K: página traz corrente 0,1 A/m, incompatível com 12 W/m a 12 V. Dimensionamento usa P/V = 1 A/m; o rótulo e o lote devem confirmar potência.',
   'Não trocar CLX-FT431230 COB de 3000 K por CLX-FT331230 SMD, nem CLX-FT331240 COB de 4000 K por CLX-FT231240 SMD: são variantes diferentes, inclusive IRC.',
   'LPV-35-12 tem 3 A e 36 W conforme ficha Mean Well. Título de anúncio menciona 1 A por erro; prevalecem ficha e etiqueta.',
   'Nenhuma avaliação de comprador ou medição independente foi usada como prova de IRC, conforto ou resistência. Especificações são declarações dos fabricantes.',
   'Brilia Alto IRC IP44 de 1 m sem corte descartado pelo espelheiro de 600 mm; Opus Áquila IRC >80 não atende ao critério do espelho; perfis sem canal documentado exigem amostra.',
 ], sources=sources)
save('Luminarias_selecao_L01.json', data)

def money(x):
    return 'Sob consulta' if x is None else 'R$ '+f'{x:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')

rows = ''.join(f'<tr><td>{h(i["product"])}</td><td>{i["quantity"]} {h(i["unit"])}</td><td>{money(i["price_brl"])}</td><td>{h(i["seller"])}<br><small>{h(i["availability"])}</small><br><a href="{h(i["buy_url"])}">Abrir oferta</a></td></tr>' for i in bom)
source_html = ''.join(f'<li><a href="{h(s["url"])}">{h(s["title"])}</a></li>' for s in sources)
holds_html = ''.join(f'<li>{h(s)}</li>' for s in holds)
page = f'''<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Luminárias do banheiro · seleção L01</title>
<style>body{{max-width:1100px;margin:32px auto;padding:0 20px;background:#faf8f3;color:#29352f;font:16px/1.55 system-ui}}h1{{font-size:32px}}a{{color:#32634f}}table{{width:100%;border-collapse:collapse;background:white}}th,td{{padding:12px;border-bottom:1px solid #ddd;text-align:left;vertical-align:top}}th{{background:#e9eee6}}.note{{padding:18px;border-left:4px solid #648773;background:#edf1e9}}small{{font-size:13px}}li{{margin:12px 0}}svg{{width:100%;height:auto;background:#fff}}@media(max-width:650px){{.scroll{{overflow-x:auto}}table{{min-width:650px}}}}@media print{{body{{font-size:10pt}}tr,svg{{break-inside:avoid}}}}</style>
<main><p><a href="Fechamento.html#B05">← Fechamento do banheiro</a></p><h1>Luminárias do banheiro</h1>
<p>24/10/2026 · L01 · seleção de componentes para cotação</p>
<p class="note"><b>3000 K no teto e na indireta; 4000 K no espelho.</b> Três comandos físicos separados. Modelos abaixo selecionados para o projeto; conjunto montado e instalação ainda condicionados às verificações descritas. Não houve compra ou envio de consulta.</p>
<div class="scroll"><table><tr><th>Grupo</th><th>Solução selecionada</th><th>Dimensionamento</th></tr>
<tr><td>B11 · teto<br><b>3000 K</b></td><td><a href="{urls['teto']}">Galaxy LED Firefly 9605</a>, branco redondo, sobrepor, IP44.</td><td>1 un. · 25 W · 2000 lm · Ø300 mm. Reservar 50 mm de altura. Bivolt. Fora do box.</td></tr>
<tr><td>B09 · espelho<br><b>4000 K</b></td><td><a href="{urls['espelho']}">Cristallux Pro Dry COB CLX-FT331240</a>, IRC &gt;90, em dois perfis brancos MOV com difusor. Duas barras fixas acima/abaixo.</td><td>2 × 550 mm de fita; 13,2 W e 1,1 A no total; 1320 lm antes do difusor. Fonte LPV-20-12 de 20 W. Corpo dos perfis nominal: 2 ×560 mm.</td></tr>
<tr><td>B10 · indireta<br><b>3000 K</b></td><td><a href="{urls['indireta']}">Cristallux Pro Dry COB CLX-FT431230</a>, IRC &gt;90, em perfil MOV oculto na faixa do canto do teto.</td><td>Kit dimensionado para até 2 m: até 24 W / 2 A. Fonte LPV-35-12 de 36 W. Comprimento de obra a medir, em múltiplos de 25 mm.</td></tr></table></div>
<h2>Espelho: preservação da abertura e da guarda</h2>
<svg viewBox="0 0 900 430" role="img" aria-label="Esquema frontal nominal do espelheiro de 600 mm e duas barras horizontais fixas; barra inferior condicionada à torneira">
<text x="50" y="35" font-size="19" fill="#29352f">Esquema nominal de frente · sem escala de execução</text>
<rect x="100" y="87" width="280" height="7" rx="2" fill="#b8d8db"/>
<rect x="90" y="110" width="300" height="275" fill="#dce4e5" stroke="#7e9090" stroke-width="2"/>
<path d="M240 110V385" stroke="#8e9e9e" stroke-width="2"/>
<rect x="100" y="401" width="280" height="7" rx="2" fill="#b8d8db" stroke="#b17f49" stroke-dasharray="5 3"/>
<text x="155" y="260" font-size="22" fill="#465c5d">600 ×750 mm</text>
<text x="445" y="94" font-size="18" fill="#29352f">Barra fixa superior · 4000 K</text>
<text x="445" y="141" font-size="17" fill="#29352f">Sem fios nas portas espelhadas.</text>
<text x="445" y="175" font-size="17" fill="#29352f">Sem fonte ocupando o interior útil.</text>
<text x="445" y="222" font-size="17" fill="#29352f">Perfil externo: 560 ×17 ×7 mm</text>
<text x="445" y="254" font-size="17" fill="#29352f">Fita: 550 mm por barra, corte de 25 mm</text>
<text x="445" y="365" font-size="17" fill="#805b35">Barra inferior: conferir torneira aberta,</text>
<text x="445" y="397" font-size="17" fill="#805b35">mão, respingos e suporte antes de fixar.</text>
</svg>
<p>O corpo externo do MOV tem 7 mm de projeção e 17 mm de altura, dentro da envoltória antiga de 7 ×20 mm. A comparação é analítica: não inclui presilhas, tampas e fios e não substitui ensaio de montagem. Não foram alteradas posições nem geometrias do FreeCAD principal. As fitas siliconadas medem 10 ×3 mm; o encaixe interno do perfil e a dissipação precisam de prova de bancada antes da encomenda montada.</p>
<h2>Lista para cotar e links de compra</h2>
<div class="scroll"><table><tr><th>Produto</th><th>Compra prevista</th><th>Preço unitário</th><th>Fornecedor / link</th></tr>{rows}</table></div>
<p><b>Subtotal conhecido: {money(subtotal)} + fita de 4000 K sob consulta.</b> Referências consultadas em24/10/2026; preço do perfil obtido no índice comercial e sujeito a reconfirmação. Frete, tributos adicionais das fontes, montagem, terminações protegidas, cabos, caixas, interruptores e mão de obra não incluídos. Não é preço do conjunto completo instalado.</p>
<p>Compra por rolo de 5 m: espelho usa 1,10 m e deixa 3,90 m; indireta usa até 2 m e deixa pelo menos 3 m. Para evitar sobras, pedir também cotação por metro do mesmo SKU em conjunto montado. Os rolos inteiros de 60 W não podem ser ligados nas fontes dimensionadas para os trechos.</p>
<p>Dois perfis 4329 de 2 m fornecem oito tampas e oito garras segundo o fabricante. Previsão: quatro tampas/quatro garras nas duas barras do espelho e duas tampas/quatro garras na indireta. Corte da primeira barra: dois corpos nominais de 560 mm. Conferir comprimento final com as tampas e passagem do cabo; fita de 550 mm dentro de cada corpo.</p>
<h2>Comandos, alimentação e manutenção</h2>
<p>Tecla 1 → plafon bivolt. Tecla 2 → LPV-20-12 → duas barras de 4000 K em paralelo. Tecla 3 → LPV-35-12 → indireta de 3000 K. Cada fonte tem seu retorno próprio; saídas independentes. Acionamento liga/desliga. As fontes LPV não foram escolhidas para dimmer de parede; eventual regulagem exige controlador e análise próprios.</p>
<p>As cargas nominais ocupam 66% da fonte do espelho e até 66,7% da fonte da indireta. Potência com margem não dispensa verificar temperatura/curvas de redução da fonte na instalação. IRC é declaração do fabricante; fluxo antes do difusor não comprova iluminância ou conforto no rosto.</p>
<h2>Condições para a montagem final</h2><ol>{holds_html}</ol>
<h2>Conferência de códigos</h2><p>3000 K: <b>CLX-FT431230 /221506</b>. 4000 K: <b>CLX-FT331240 /221513</b>. A família SMD semelhante não substitui a COB selecionada. A página quente tem um erro de corrente (0,1 A/m); o dimensionamento usa12 W ÷12 V =1 A/m. A LPV-35-12 entrega3 A/36 W conforme ficha oficial, apesar do erro “1 A” no título comercial.</p>
<p>Foram descartadas barras Brilia de1 m que não admitem corte para o espelheiro de600 mm e luminárias de espelho com IRC declarado apenas acima de80. A antiga Stella STL23820/40 deixa de ser a referência de compra desta seleção.</p>
<h2>Fontes técnicas</h2><ul>{source_html}</ul><p><a href="Luminarias_selecao_L01.json">Especificação completa, cálculos e evidências em JSON</a></p></main></html>'''
(HERE/'Luminarias_selecao_L01.html').write_text(page, encoding='utf-8')

materials = read('Iluminacao_e_materiais.json')
materials['approved']['controls'] = 'Três grupos físicos independentes; componentes selecionados em L01, execução elétrica a compatibilizar'
materials['lighting'].update(groups=groups, fixtures_selected=False, components_selected=True,
    complete_luminaires_released=False, selection='Luminarias_selecao_L01.json',
    sources=sources, power_supplies='LPV-20-12 para espelho e LPV-35-12 para indireta. Compartimento técnico acessível, ventilado e seco, fora da guarda do espelheiro; localização executiva a conferir.')
save('Iluminacao_e_materiais.json', materials)
status = read('Situacao.json')
status['choices']['controls'] = materials['approved']['controls']
b05 = next(i for i in status['sections'] if i['id']=='B05')
b05.update(status='Modelos e componentes selecionados; conjunto montado e implantação condicionados',
 result='Teto 3000 K: Galaxy Firefly 9605, 25 W/IP44. Espelho 4000 K: Cristallux COB CLX-FT331240, 2×550 mm, 13,2 W, IRC>90. Indireta 3000 K: CLX-FT431230, até 2 m/24 W. Perfis MOV 4329 brancos/difusor; fontes LPV-20-12 e LPV-35-12; três comandos separados. Links e composição emitidos em L01.',
 next='Fechar preço/fornecimento da fita 4000 K e montagem protegida. Provar canal do perfil para fita 10×3 mm, dissipação, difusão no rosto e terminais. Perfil é IP20; IP65 não se transfere da fita ao conjunto. Posição inferior depende da torneira; cotas da indireta, suportes e volumes elétricos dependem da implantação. Não executar por coordenadas nominais.',
 source='Luminarias_selecao_L01.html')
source_map = {s['url']:s for s in status['sources'] if s.get('title')!='Stella STL23820/40'}
source_map.update({s['url']:s for s in sources})
status['sources'] = list(source_map.values())
save('Situacao.json', status)
choices = read('Escolhas.json')
if isinstance(choices, dict) and 'controls' in choices:
    choices['controls'] = materials['approved']['controls']
save('Escolhas.json', choices)

closing = (HERE/'Fechamento.html').read_text(encoding='utf-8')
replacement = f'<tr id="B05"><td><b>B05 · Iluminação</b><p>{h(b05["status"])}</p></td><td>{h(b05["result"])}</td><td>{h(b05["next"])}<p><a href="Luminarias_selecao_L01.html">Seleção, dimensionamento e links de compra</a></p></td></tr>'
closing, n = re.subn(r'<tr id="B05">.*?</tr>', lambda m: replacement, closing, count=1, flags=re.S)
assert n==1
closing = closing.replace('R01 local · medidas nominais', 'R02 local · iluminação L01 · medidas nominais')
if 'Luminárias: seleção e links de compra</a>' not in closing:
    closing = closing.replace('<p><a href="Espelheiro_P19', '<p><a href="Luminarias_selecao_L01.html">Luminárias: seleção e links de compra</a> · <a href="Espelheiro_P19',1)
(HERE/'Fechamento.html').write_text(closing, encoding='utf-8')
print(json.dumps({'components_selected':True,'installation_released':False,'subtotal_known_brl':subtotal,'files_written':6},ensure_ascii=False))
