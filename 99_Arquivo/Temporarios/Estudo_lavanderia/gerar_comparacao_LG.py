from pathlib import Path
import json, shutil, hashlib
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Flowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT/'02_Projeto_em_desenvolvimento/A04.3_Comparacao_LG'
OUT.mkdir(exist_ok=True)
MAN = ROOT/'01_Documentos_base/Manuais_equipamentos'
MAN.mkdir(exist_ok=True)
manual = MAN/'LG_CV3012WC5_127V_MFL72097501.pdf'
shutil.copy2(Path(__file__).parent/'Manual_LG_CV3012WC5.pdf', manual)
pdfmetrics.registerFont(TTFont('Segoe', 'C:/Windows/Fonts/segoeui.ttf'))
pdfmetrics.registerFont(TTFont('SegoeBold', 'C:/Windows/Fonts/segoeuib.ttf'))
pdfmetrics.registerFontFamily('Segoe', normal='Segoe', bold='SegoeBold', italic='Segoe', boldItalic='SegoeBold')
INK=HexColor('#173B43'); MUTED=HexColor('#536466'); LIGHT=HexColor('#EDF3F1'); GOLD=HexColor('#9D663A')
styles={
 'title':ParagraphStyle('title',fontName='SegoeBold',fontSize=23,leading=28,textColor=INK,spaceAfter=12),
 'h':ParagraphStyle('h',fontName='SegoeBold',fontSize=12,leading=16,textColor=INK,spaceBefore=13,spaceAfter=6),
 'body':ParagraphStyle('body',fontName='Segoe',fontSize=10,leading=14,textColor=INK,spaceAfter=7),
 'small':ParagraphStyle('small',fontName='Segoe',fontSize=8,leading=11,textColor=MUTED,spaceAfter=5),
 'cell':ParagraphStyle('cell',fontName='Segoe',fontSize=9,leading=12,textColor=INK),
 'th':ParagraphStyle('th',fontName='SegoeBold',fontSize=9,leading=12,textColor=white),
}
def P(s,style='body'): return Paragraph(s, styles[style])
story=[]
def p(s,style='body'): story.append(P(s,style))
def table(rows,widths):
 t=Table([[P(str(x),'th' if i==0 else 'cell') for x in r] for i,r in enumerate(rows)],colWidths=widths,hAlign='LEFT')
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),INK),('ROWBACKGROUNDS',(0,1),(-1,-1),[LIGHT,white]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),('LINEBELOW',(0,-1),(-1,-1),.5,HexColor('#B9CAC6'))]))
 story.extend([t,Spacer(1,8)])

sources={
 'LG VC5 127 V':'https://www.lg.com/br/lavanderia/lava-e-seca/cv3012wc5/',
 'LG VC5 220 V':'https://www.lg.com/br/lavanderia/lava-e-seca/cv3012wc5a/',
 'LG VC4 127 V':'https://www.lg.com/br/lavanderia/lava-e-seca/cv5012wc4/',
 'LG VC4 220 V':'https://www.lg.com/br/lavanderia/lava-e-seca/cv5012wc4a/',
 'Manual LG VC5 127 V':'https://www.lg.com/br/suporte/suporte-ao-producto/cs-CV3012WC5.ABWFBRS#manual-tab',
 'Electrolux IB6':'https://loja.electrolux.com.br/geladeira-electrolux-frost-free-inverter-400l-efficient-rapid-freeze-inverse-branca--ib6-/p',
 'E15 GN - oferta Leroy Merlin':'https://www.leroymerlin.com.br/aquecedor-a-gas-rinnai-15-gn-branco-e15_90555640',
 'Rinnai E15 - ficha técnica':'https://www.rinnai.com.br/aquecedores-a-gas/linha-prata/e15-1/',
}

p('Lava e seca LG<br/>e orçamento parcelado','title')
p('A04.3 R00 | Guedala Park | Elias | 09/09/2026','small')
p('<b>Recomendação para decidir: LG VC5 12 kg.</b> É a opção mais econômica das duas cotadas na loja oficial. A VC4 acrescenta Wi-Fi, sem ganho de capacidade. Modelo, cor e tensão da LG ainda não aprovados por Elias.')
table([
 ['Comparação','LG VC5 branca','LG VC4 branca'],
 ['Lavagem / secagem','12 kg / 7 kg','12 kg / 7 kg'],
 ['AI DD / vapor Steam','Sim / sim','Sim / sim'],
 ['Wi-Fi ThinQ','Não','Sim'],
 ['Preço total parcelado¹','R$ 3.999,00','R$ 4.599,00'],
 ['Condição LG¹','Até 12x sem juros','Até 12x sem juros'],
 ['Código 127 V','CV3012WC5','CV5012WC4'],
 ['Código 220 V','CV3012WC5A','CV5012WC4A'],
 ],[151,177,177])
p('¹ Mesmos preços observados nas duas tensões em cada família. Consulta às páginas ao vivo da loja LG, sem cupom, Pix ou desconto condicionado a cadastro. Frete e disponibilidade para entrega dependem do CEP. Não é uma busca exaustiva pelo menor preço.','small')
p('O conjunto ultrapassa os R$ 9.000','h')
table([
 ['Equipamento / loja','Total parcelado','Condição observada'],
 ['IB6 / Electrolux','R$ 3.699,00','10x de R$ 369,90 sem juros'],
 ['LG VC5 / LG','R$ 3.999,00','Até 12x sem juros'],
 ['E15 GN branco / Leroy²','R$ 2.446,70','Até 8x; 8x de R$ 305,84³'],
 ['Cenário com VC5','R$ 10.144,70','R$ 1.144,70 acima do teto'],
 ['Cenário com VC4','R$ 10.744,70','R$ 1.744,70 acima do teto'],
 ],[192,130,183])
p('² Aquecedor candidato, código Leroy 90555640. Gás da unidade e código completo do aparelho ainda precisam ser confirmados. Preço ao vivo válido em 09/09/2026 para São Paulo e Região. ³ Parcela arredondada exibida pela loja; total anunciado usado nas somas.','small')
p('<b>Para manter o teto:</b> LG + aquecedor precisam somar até R$ 5.301. Com a LG a R$ 3.999, sobram R$ 1.302 para o aquecedor. Não há conjunto fechado dentro do teto nesta cotação. Instalação, frete, kits e adaptações estão fora das somas.','small')

story.append(PageBreak())
p('O espaço da máquina instalada','title')
p('Ensaio dimensional da candidata VC5 127 V. Não é desenho de fabricação.','small')
p('O manual MFL72097501, páginas 10 a 13, confirma o corpo de <b>60 x 85 x 56,5 cm</b> (L x A x P), profundidade de <b>62 cm até a porta fechada</b> e <b>110 cm com a porta a 90°</b>, medidos a partir da traseira do equipamento.')
table([
 ['Reserva','Cálculo em centímetros','Uso no estudo'],
 ['Vão livre lateral','2 + 60 + 2 = 64','Mínimo entre obstáculos; painéis e apoios ficam fora desse vão.'],
 ['Altura livre mínima','85 + 0,5 = 85,5','Até a face inferior da bancada/apoios. Acrescentar o que o nivelamento exigir.'],
 ['Da parede à porta fechada','10 + 62 = 72','Somando a folga traseira mínima; tubulações podem exigir mais.'],
 ['Da parede à porta a 90°','10 + 110 = 120','Reserva de abertura, ainda sem espaço para a pessoa se movimentar.'],
 ],[143,149,213])

class DimensionSketch(Flowable):
 def __init__(self): Flowable.__init__(self); self.width=505; self.height=126
 def draw(self):
  c=self.canv; x=14; y=48; k=2.75
  c.setFillColor(LIGHT); c.rect(0,12,505,108,fill=1,stroke=0)
  c.setStrokeColor(INK); c.setLineWidth(2); c.line(x,26,x,111)
  c.setFillColor(HexColor('#D7E3DF')); c.rect(x+10*k,y,62*k,38,fill=1,stroke=0)
  c.setStrokeColor(GOLD); c.setLineWidth(2); c.line(x+72*k,y+19,x+120*k,y+19)
  c.setStrokeColor(INK); c.line(x+154*k,26,x+154*k,111)
  c.setFont('Segoe',8); c.setFillColor(INK)
  c.drawString(x+5,98,'Parede'); c.drawString(x+10*k+8,63,'Máquina fechada')
  c.drawString(x+72*k+6,80,'Porta a 90°'); c.drawString(x+120*k+8,63,'34 cm*')
  c.setFont('SegoeBold',9); c.drawString(x+10*k,30,'72 cm'); c.drawString(x+92*k,30,'120 cm')
  c.drawString(x+127*k,98,'Parede oposta')
story.append(DimensionSketch())
p('* Se a seção real tiver os 154 cm da planta e estiver livre: 154 - 72 = <b>82 cm</b> com a porta fechada; 154 - 120 = <b>34 cm</b> com a porta a 90°. O desenho ilustra profundidades, não o giro completo. Recessos, rodapés e outras portas podem reduzir esses espaços.','small')
p('O que isso muda na bancada','h')
p('Os 56,5 cm do corpo não autorizam uma bancada de 60 cm com frente alinhada. A frente da máquina instalada pode avançar. Definir a pedra após conferir mangueiras, porta, gaveta de sabão e acesso ao filtro. Manter tampa original, frente acessível e apoio da pedra independente da máquina.')
p('A largura de 64 cm ocupa parte dos 129 cm paralelos à bancada: a sobra aritmética é 65 cm, <b>antes</b> do tanque, shaft, tubos, painéis e estrutura. Isso não prova cabimento de tanque + cesto + máquina. O retorno em L de cerca de 15 cm fica junto à janela; não se soma como módulo nessa sequência.')
p('Escopo das medidas: o manual salvo é da VC5 127 V. A ficha VC5 220 V publica as mesmas dimensões externas, mas seu manual elétrico deve ser conferido se essa tensão for escolhida. A VC4 127 V publica as mesmas profundidades; a página VC4 220 V contém largura/ordem de medidas conflitantes. Confirmar pelo manual antes de dimensionar essa alternativa.','small')

story.append(PageBreak())
p('Fechamentos para o próximo desenho','title')
p('<b>Registrado:</b> pagamento parcelado; tensão da lavanderia ainda desconhecida; orçamento mantido em R$ 9.000; IB6 escolhida; LG obrigatória; uso de água quente sem banho e torneira simultâneos.')
p('Aquecedor: candidato de 15 L/min','h')
p('O Rinnai E15 FEH informa 15 L/min com elevação de 20 °C e vazão mínima de acionamento de 3,5 L/min. Esses números não garantem o mesmo desempenho em qualquer temperatura nem o acionamento com torneira muito restritiva. Confirmar vazão do chuveiro, temperatura desejada, pressão e atendimento das torneiras antes de escolher o modelo.')
p('O E15 GN usado no orçamento é apenas referência comercial da família. Conferir código completo e gás GN/GLP antes da seleção. A quantidade de visitas não exige aumento automático de capacidade, pois Elias dispensou o uso simultâneo de banho e torneira. A alimentação da VC5 é de água fria; ela não depende da rede de água quente do aquecedor.')
p('Levantamento objetivo que ainda falta','h')
table([
 ['Conferência','Resultado necessário'],
 ['Elétrica da lavanderia','Tensão do ponto, tomada, aterramento e circuito compatíveis com o modelo escolhido. Obter com construtora/condomínio ou profissional.'],
 ['Bancada e tanque','Largura útil por trecho, shaft/recessos, espessuras, posição dos pontos, espaço para sifão e cesto removível ventilado.'],
 ['Janela e retorno em L','Altura do peitoril, abertura das folhas, grelha, comprimento disponível e apoios da faixa de aproximadamente 15 cm.'],
 ['Água quente e gás','Tipo de gás; pontos atendidos pela rede; vazão/pressão; identificação da abertura de exaustão e das ventilações permanentes.'],
 ['Uso e manutenção','Simular porta e gaveta da LG, retirada da máquina, cesto, varal aberto e portas dos armários. Não fechar a reserva do aquecedor sem validação.'],
 ],[146,359])
p('Decisão proposta','h')
p('Adotar a <b>VC5 como candidata principal</b> e manter R$ 9.000 como teto, buscando nova condição parcelada para o conjunto após confirmar tensão e gás. Aumentar o orçamento ou escolher o modelo exige decisão de Elias. Não houve compra, mudança de acabamento ou liberação de marcenaria.')
p('Fontes e prioridade documental','h')
p('Consulta em 09/09/2026. Preços conferidos nas páginas ao vivo, após carregamento das condições de pagamento. Resultados antigos de busca e valores Pix não entraram nas somas. Links clicáveis:','small')
for labels in [['LG VC5 127 V','LG VC5 220 V','LG VC4 127 V','LG VC4 220 V'],['Manual LG VC5 127 V','Electrolux IB6'],['E15 GN - oferta Leroy Merlin','Rinnai E15 - ficha técnica']]:
 p(' | '.join(f'<a href="{sources[x]}" color="#176974">{x}</a>' for x in labels),'small')
p('A04.3 R00 complementa A04.2 R01 e prevalece para esta comparação, cotação e respostas sobre pagamento/tensão. A01.2 segue como base dimensional. O partido da lavanderia e os demais acabamentos do memorial permanecem vigentes.','small')

def page(c,doc):
 c.setTitle('A04.3 - Comparação LG e orçamento parcelado - Elias')
 c.setAuthor('Projeto Guedala Park - Elias')
 c.setStrokeColor(HexColor('#CEDCD7')); c.line(45,37,550,37)
 c.setFont('Segoe',8); c.setFillColor(MUTED)
 c.drawString(45,23,'GUEDALA PARK  |  A04.3 R00  |  ESTUDO PRELIMINAR')
 c.drawRightString(550,23,f'{doc.page} / 3')

pdf=OUT/'A04.3_Comparacao_LG_e_orcamento_R00.pdf'
SimpleDocTemplate(str(pdf),pagesize=(595.28,841.89),rightMargin=45,leftMargin=45,topMargin=39,bottomMargin=51).build(story,onFirstPage=page,onLaterPages=page)

data=json.loads((ROOT/'01_Projeto/Lavanderia/Dados_da_lavanderia_R01.json').read_text(encoding='utf-8'))
data.update(documento='A04.3',revisao='R00',status='comparação e cotação; modelo LG e aquecedor ainda pendentes; teto não aumentado',pagamento='parcelado',tensao_lavanderia_status='Elias ainda não sabe')
data['fontes'].update(sources)
data['equipamentos']['lava_seca']['candidata_principal']='LG VC5 12 kg branca - CV3012WC5 (127 V) ou CV3012WC5A (220 V)'
data['equipamentos']['lava_seca']['candidata_aprovada']=False
data['orcamento_atual']={
 'teto_brl':9000,'pagamento':'parcelado','ib6_brl':3699,'ib6_parcelas_sem_juros':10,
 'saldo_LG_mais_aquecedor_brl':5301,'lg_vc5_brl':3999,'lg_vc4_brl':4599,'lg_parcelas_sem_juros_ate':12,
 'rinnai_e15_gn_brl':2446.70,'rinnai_codigo_loja':'Leroy Merlin 90555640','rinnai_parcelas_ate':8,
 'cenario_vc5_brl':10144.70,'cenario_vc4_brl':10744.70,'excesso_vc5_brl':1144.70,'excesso_vc4_brl':1744.70,
 'total_conjunto_escolhido_brl':None,'instalacao_incluida':False,'frete_incluido':False,'kits_incluidos':False,
 'consulta':'2026-09-09','metodo':'páginas ao vivo; sem Pix/cupons; CEP final pendente; referência Rinnai em GN, gás da unidade desconhecido'
}
data['ensaio_vc5_127v']={'corpo_LAP_cm':[60,85,56.5],'profundidade_porta_fechada_cm':62,'profundidade_porta_90_cm':110,'folgas_cm':{'lateral_cada':2,'traseira':10,'superior':0.5},'minimos_calculados_cm':{'largura_livre':64,'altura_livre_sem_acrescimo_nivelamento':85.5,'parede_ate_porta_fechada':72,'parede_ate_porta_90':120},'cabimento_no_apartamento_comprovado':False,'fonte_manual':str(manual.relative_to(ROOT)),'manual_sha256':hashlib.sha256(manual.read_bytes()).hexdigest(),'manual_paginas':[10,11,12,13,16,18]}
data['pendencia_vc4_220v']='Ficha online contém 660 mm e ordem L/A/P conflitante; confirmar manual do código exato, não transferir medidas sem validação.'
(OUT/'A04.3_Registro_R00.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

md='''# A04.3 - Comparação LG e orçamento parcelado

**R00 | 09/09/2026 | Complemento vigente da A04.2 R01 para seleção e orçamento**

[Abrir comparação e ensaio dimensional em PDF](A04.3_Comparacao_LG_e_orcamento_R00.pdf)

## Respostas de Elias incorporadas

- Pagamento dos equipamentos: **parcelado**. Comparar pelo total pago, excluindo descontos de Pix e cupons não verificados.
- Tensão disponível para a lava e seca: **ainda desconhecida**. Não escolher 127 V ou 220 V por suposição.
- Permanecem: teto de R$ 9.000, geladeira IB6 escolhida, marca LG obrigatória, aquecedor pendente, sem banho e torneira quente simultâneos. Modelo e cor da LG ainda não aprovados.

## Duas candidatas LG

| Critério | VC5 branca | VC4 branca |
|---|---|---|
| Código 127 V | CV3012WC5 | CV5012WC4 |
| Código 220 V | CV3012WC5A | CV5012WC4A |
| Lavagem / secagem | 12 / 7 kg | 12 / 7 kg |
| AI DD / vapor Steam | Sim / sim | Sim / sim |
| Wi-Fi ThinQ | Não | Sim |
| Total parcelado na loja LG | R$ 3.999 | R$ 4.599 |
| Parcelamento observado | Até 12x sem juros | Até 12x sem juros |

As quatro páginas oficiais mostraram esses valores ao vivo. A VC5 custa R$ 600 menos nesta comparação. Recomendo-a como candidata principal pelo custo e pela capacidade; isso não representa escolha de Elias. Não foi feita uma busca exaustiva pelo menor preço nem verificado estoque/frete por CEP. Não se presume que a numeração VC5 indique uma categoria superior à VC4.

## Orçamento em parcelas

| Item | Total | Condição consultada |
|---|---:|---|
| IB6, loja Electrolux | R$ 3.699,00 | 10x de R$ 369,90 sem juros |
| LG VC5, loja LG | R$ 3.999,00 | Até 12x sem juros |
| Rinnai E15 GN branco, Leroy Merlin 90555640 | R$ 2.446,70 | Até 8x; parcela de R$ 305,84 exibida pela loja |
| **Cenário VC5** | **R$ 10.144,70** | **Excesso de R$ 1.144,70** |
| **Cenário VC4** | **R$ 10.744,70** | **Excesso de R$ 1.744,70** |

Consulta ao vivo em 09/09/2026; Leroy indicou São Paulo e Região e validade nessa data. As parcelas podem apresentar arredondamento; a soma usa o total anunciado. A Electrolux também exibia 12x com juros, condição não usada no cenário. Cada loja tem seu prazo: não tratar o conjunto inteiro como uma única compra em 12x sem juros.

O aquecedor é candidato, não modelo dimensionado nem aprovado. O preço é da oferta E15 GN indicada; conferir código completo, versão e gás antes da compra. Gás da unidade não confirmado. Não extrapolar cotação GN para GLP. Frete, instalação, kits e adaptações não incluídos.

**Meta para respeitar o teto:** LG + aquecedor <= R$ 5.301. Mantendo a LG em R$ 3.999, o aquecedor teria de custar até R$ 1.302. Mantendo o aquecedor desta cotação, a LG teria de custar até R$ 2.854,30. São limites aritméticos, não ofertas encontradas. O orçamento não foi aumentado.

## Ensaio de instalação da VC5 127 V

Manual LG MFL72097501 Rev.00_112323, obtido no suporte oficial do código CV3012WC5.ABWFBRS. Cópia em `02_Plantas_e_manuais/Manuais/LG_CV3012WC5_127V_MFL72097501.pdf`. Páginas 10 e 12 verificadas visualmente.

- Corpo: **60 x 85 x 56,5 cm**, L x A x P.
- Traseira até a porta fechada: **62 cm**; até porta a 90°: **110 cm**.
- Folgas mínimas do manual: **2 cm em cada lateral, 10 cm atrás e 0,5 cm acima**.
- Vão livre mínimo calculado: **64 cm de largura** e **85,5 cm de altura**, antes de eventual acréscimo pelo nivelamento. Não é a altura acabada da bancada. Espessura e apoios da pedra entram acima/fora do vão necessário.
- Profundidade instalada calculada: **72 cm até porta fechada**, **120 cm com porta a 90°**. Tubos/obstáculos podem pedir mais. Não adotar bancada de 60 cm supondo alinhamento da frente.
- Se a seção útil real coincidir com a cota de 154 cm da planta, restariam 82 cm com porta fechada e 34 cm com porta a 90°. São contas condicionais, não circulação medida nem prova de conforto. Avaliar operação da porta, posição da pessoa e outras interferências no local.
- Na extensão de 129 cm paralela à bancada, 129 - 64 = 65 cm antes de shaft, tanque, cesto, painéis, tubos e estrutura. Não prova cabimento.
- Entrada de água fria; manter alimentação disponível também conforme o ciclo de secagem. Não conectar à rede quente do aquecedor. Conferir drenagem e acesso com o manual.
- Pedra com estrutura independente, sem retirada presumida da tampa. Preservar acesso à gaveta, filtro, plugue e retirada da máquina para manutenção. Não fechar a frente com portas sem validação do fabricante.

A ficha VC5 220 V publica as mesmas dimensões externas, mas o manual elétrico dessa versão precisa ser conferido se escolhida. A VC4 127 V publica 60 x 85 x 56,5 cm e profundidades 62/110 cm; a página VC4 220 V contém valores conflitantes (largura 660 mm e ordem das dimensões). Não dimensionar a alternativa 220 V sem conferir seu manual. As folgas da VC5 não foram automaticamente atribuídas à VC4.

## Aquecedor e levantamento pendente

O Rinnai E15 FEH informa 15 L/min a uma elevação de 20 °C e acionamento mínimo de 3,5 L/min. A escolha depende da vazão do chuveiro e das torneiras, temperatura, pressão dinâmica, gás, rede quente, ventilação e exaustão. Torneiras com fluxo restritivo podem não acionar o aparelho. Número de visitas não implica demanda simultânea. Fonte técnica: Rinnai, não a descrição comercial do varejo.

Conferir com construtora/condomínio ou profissional a tensão da lavanderia e o gás da unidade. No local, levantar peitoril e janela aberta, grelhas e abertura circular, eixos de água/esgoto/gás, recessos e shaft, altura livre, largura útil e comprimento do retorno em L. O vídeo não confirma tensão ou gás nem resolve as medidas restantes.

Depois da escolha e dessas conferências: implantação cotada com giro de portas, manutenção, cesto removível ventilado abaixo do tanque, varal e apoio independente da pedra. Manter o retorno em L de aproximadamente 15 cm junto à janela; não tratá-lo como módulo linear depois da máquina. Nada foi liberado para fabricação.

## Prioridade e fontes

A04.3 R00 prevalece sobre referências de orçamento da A04.2 R01 para esta cotação e registra as respostas sobre parcelas/tensão. A04.2 R01 continua válida para o partido e decisões anteriores; A01.2 é a base dimensional. Memorial v2 e demais escolhas, inclusive ausência de azul no quarto, permanecem.

'''
md+='\n'.join(f'- [{label}]({url})' for label,url in sources.items())+'\n'
(OUT/'A04.3_Comparacao_e_pendencias_R00.md').write_text(md,encoding='utf-8')

index=ROOT/'99_Arquivo/Organizacao_anterior/Indice_anterior.md'
s=index.read_text(encoding='utf-8')
s=s.replace('com total a recompor.','pagamento parcelado e tensão da lavanderia desconhecida. A cotação A04.3 apresenta cenário com VC5 + E15 por R$ 10.144,70, acima do teto; modelos ainda pendentes.')
s=s.replace('## Abrir primeiro\n','## Abrir primeiro\n\n- [Comparação LG e orçamento parcelado atual - A04.3 R00](../../Estudos_anteriores/Equipamentos/Comparacao_LG_e_orcamento_R00.pdf)\n- [Comparação, decisões e pendências - A04.3 R00](../../Estudos_anteriores/Equipamentos/Comparacao_e_pendencias_R00.md)\n')
s=s.replace('**A04.2 R01 é a revisão vigente:**','**A04.2 R01 é o estudo vigente de implantação; A04.3 R00 complementa a seleção e atualiza a cotação:**')
s=s.replace('estudo atual A04.2 R01 de lavanderia e equipamentos.','estudo A04.2 R01 de lavanderia e comparação atual A04.3 R00 de LG/orçamento parcelado.')
s=s.replace('decisões v2. As escolhas de equipamentos foram complementadas pela A04.2 R01.','decisões v2, com escolhas complementadas por A04.2/A04.3; subpasta de manuais de equipamentos candidatos.')
index.write_text(s,encoding='utf-8')
oldmd=ROOT/'01_Projeto/Lavanderia/Decisoes_da_lavanderia_R01.md'
s=oldmd.read_text(encoding='utf-8')
note='> **Complemento posterior:** [A04.3 R00](../A04.3_Comparacao_LG/A04.3_Comparacao_e_pendencias_R00.md) registra pagamento parcelado, tensão desconhecida, comparação de duas LG e nova cotação. Consultar esse complemento para orçamento; o partido desta R01 permanece.\n\n'
s=s.replace('## Decisões vigentes de Elias',note+'## Decisões vigentes de Elias',1)
oldmd.write_text(s,encoding='utf-8')
print(pdf)
print('MD, JSON, índice e aviso na R01 atualizados. Manual preservado em Documentos base.')
