from pathlib import Path
import json, sys
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader

sys.stdout.reconfigure(encoding='utf-8')
WORK = Path(__file__).resolve().parent
ROOT = WORK.parents[2]
OUT = ROOT/'02_Projeto_em_desenvolvimento'/'A04.2_Lavanderia_e_equipamentos'
OUT.mkdir(parents=True, exist_ok=True)
PDF = OUT/'A04.2_Lavanderia_e_equipamentos_R00.pdf'
pdfmetrics.registerFont(TTFont('Segoe', 'C:/Windows/Fonts/segoeui.ttf'))
pdfmetrics.registerFont(TTFont('SegoeB', 'C:/Windows/Fonts/segoeuib.ttf'))
pdfmetrics.registerFontFamily('Segoe', normal='Segoe', bold='SegoeB')
W,H=841.89,595.28
INK=colors.HexColor('#183742'); TEXT=colors.HexColor('#26343B')
MUTED=colors.HexColor('#647477'); PALE=colors.HexColor('#EFF3F1')
STONE=colors.HexColor('#ECE8DF'); BLUE=colors.HexColor('#367791')
AMBER=colors.HexColor('#93642E'); WHITE=colors.white
c=canvas.Canvas(str(PDF),pagesize=(W,H))
c.setTitle('A04.2 - Lavanderia e equipamentos | Estudo preliminar R00')
c.setAuthor('Projeto Apartamento Elias')

def p(t,x,top,w,size=10,color=TEXT,bold=False):
    obj=Paragraph(t,ParagraphStyle('p',fontName='SegoeB' if bold else 'Segoe',fontSize=size,leading=size*1.32,textColor=color))
    _,h=obj.wrap(w,1000)
    assert top+h<550, (t,top,h)
    obj.drawOn(c,x,H-top-h)
    return h

def box(x,t,w,h,fill=PALE,stroke=None,dash=None):
    c.setFillColor(fill); c.setStrokeColor(stroke or fill); c.setLineWidth(1);c.setDash(dash or [])
    c.rect(x,H-t-h,w,h,fill=1,stroke=int(stroke is not None));c.setDash([])

def line(x1,t1,x2,t2,color=INK,width=1,dash=None):
    c.setStrokeColor(color);c.setLineWidth(width);c.setDash(dash or [])
    c.line(x1,H-t1,x2,H-t2);c.setDash([])

def arrow(x1,t1,x2,t2,color=BLUE):
    import math
    line(x1,t1,x2,t2,color,1.3)
    a=math.atan2(t2-t1,x2-x1)
    for d in [-.45,.45]: line(x2,t2,x2-7*math.cos(a+d),t2-7*math.sin(a+d),color,1.3)

def head(n,title,sub):
    box(0,0,W,8,INK)
    p('GUEDALA PARK / ELIAS',34,23,430,10,INK,True)
    p('A04.2 / R00 / 09.09.2026',614,23,195,9,MUTED)
    p(title,34,47,776,23,INK,True)
    p(sub,34,83,776,10,MUTED)
    line(34,555,808,555,colors.HexColor('#C9D3D0'),.7)
    c.setFont('Segoe',8);c.setFillColor(MUTED)
    c.drawString(34,20,'ESTUDO PRELIMINAR / Sem escala / Dimensões de móveis pendentes / Não liberar fabricação')
    c.setFont('SegoeB',10);c.drawRightString(808,19,f'{n:02d} / 05')

def table(headers,rows,widths,top,size=9):
    def cell(s,header=False):
        return Paragraph(s,ParagraphStyle('t',fontName='SegoeB' if header else 'Segoe',fontSize=size,leading=size*1.27,textColor=WHITE if header else TEXT))
    tb=Table([[cell(v,True) for v in headers]]+[[cell(v) for v in row] for row in rows],colWidths=widths)
    tb.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),INK),('ROWBACKGROUNDS',(0,1),(-1,-1),[WHITE,PALE]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
    _,h=tb.wrap(774,1000);assert top+h<545,(top,h)
    tb.drawOn(c,34,H-top-h);return h

def smalllink(label,url,x,top,w):
    p(f'<link href="{url}" color="#367791">{label}</link>',x,top,w,8.5)

urls={
'midea':'https://www.midea.com.br/lava-e-seca-11kg-branca-inverter-midea-2731/p',
'manual_midea':'https://conteudo.midea.com.br/manuais/lava-e-seca-ciclo-pets.pdf',
'if44':'https://loja.electrolux.com.br/geladeira-electrolux-frost-free-400l-autosense-inverter-duplex-branca--if44-/p',
'catalogo_electrolux':'https://loja.electrolux.com.br/eletrodomesticos/geladeiras---refrigeradores?page=3',
'ib6':'https://loja.electrolux.com.br/geladeira-electrolux-frost-free-inverter-400l-efficient-rapid-freeze-inverse-branca--ib6-/p',
'rinnai':'https://www.rinnai.com.br/aquecedores-a-gas/aquecedores-a-g%C3%81s/e21-1/',
'manual_rinnai':'https://www.rinnai.com.br/uploads/repositorio/REUE170_E210FEH%202c242dc3bad3726f1f78ae69ba40e1334.pdf',
'oferta_e21':'https://www.leroymerlin.com.br/aquecedor-a-gas-rinnai-21-gn-prata-e21_91697305',
'lg':'https://www.lg.com/br/lavanderia/lava-e-seca/cv3012wc5/'
}
urls['e15']='https://www.rinnai.com.br/aquecedores-a-gas/linha-prata/e15-1/'

head(1,'Lavanderia: organização em planta','Etapa 4 / Proposta funcional para discussão, mantendo a orientação da planta oficial P01.')
box(34,112,774,47)
p('<b>Decisão de Elias:</b> faixa de pedra com aproximadamente 15 cm de largura, fazendo um retorno em L junto à janela. O comprimento desse retorno ainda será definido.',46,121,748,11)

# Esquema funcional, propositalmente sem cotas de módulos e sem contorno fictício do cômodo.
p('VISTA DE CIMA / SEM ESCALA',52,180,480,10,INK,True)
box(91,231,24,132,STONE,AMBER)
box(91,293,461,70,STONE,AMBER)
line(81,222,81,293,BLUE,3)
p('JANELA',42,208,100,8,BLUE,True)
p('Retorno em L',123,236,145,10,AMBER,True)
p('Largura aprox. 15 cm<br/>Extensão a definir',123,254,140,9)
arrow(130,252,104,252,AMBER)
box(145,305,108,46,WHITE,INK)
p('TANQUE',158,318,90,11,INK,True)
box(289,297,112,60,WHITE,BLUE,[4,3])
p('LAVA E SECA<br/>sob a pedra',302,308,94,10,BLUE,True)
line(429,294,429,362,MUTED,1,[4,3])
p('CONTINUA<br/>NA COZINHA',449,310,95,9,INK,True)
line(91,367,552,367,INK,3)
p('Parede da bancada / lado inferior de P01',157,377,379,9,MUTED)
arrow(345,291,345,269)
p('Acesso frontal',293,250,130,9,BLUE)
p('cesto abaixo',158,336,90,8,BLUE)
arrow(562,329,583,329)
p('COZINHA / ENTRADA À DIREITA',289,411,305,9,INK,True)

p('Como usar este desenho',605,182,191,12,INK,True)
p('Tanque próximo da região técnica existente; máquina adjacente, em direção à cozinha. A posição exata ainda depende dos pontos e do volume sob o tanque.',605,207,190,10)
p('A faixa em L não é uma sobra linear de 15 cm depois da máquina. O canto e os apoios da pedra precisarão de detalhe próprio.',605,299,190,10)
p('Os blocos mostram a relação entre usos. Não demonstram que tudo cabe dentro do trecho de 1,29 m.',605,390,190,10,AMBER,True)
box(34,451,774,86)
p('Base dimensional preservada',46,460,738,11,INK,True)
p('P01: 1,29 m é o trecho da área de serviço paralelo à bancada; 1,54 m é a direção perpendicular. A posição da máquina em relação à faixa entre cozinha e serviço será testada depois das folgas. Não se presume deslocamento do tanque nem alteração das instalações.',46,483,742,10)
c.showPage()

head(2,'Vista frontal e funcionamento','Observador de frente para a bancada: a cozinha fica à esquerda e a janela à direita.')
p('COZINHA',54,119,170,9,INK,True);p('JANELA / RETORNO EM L',467,119,195,9,INK,True)
line(54,144,596,144,MUTED,1,[4,3]);p('Teto ou limite real do forro - altura pendente',54,132,400,8,MUTED)
box(54,144,276,112,PALE,INK)
line(54,205,330,205,MUTED)
line(174,144,174,256,MUTED)
p('ESTOQUE',67,182,240,10,INK,True)
p('USO DIÁRIO',67,216,125,10,INK,True)
box(191,215,125,24,WHITE,BLUE,[3,2]);p('VARAL RECOLHIDO',197,220,117,8,BLUE,True)
line(207,267,316,267,BLUE,1,[3,2]);line(207,281,316,281,BLUE,1,[3,2])
p('abertura a compatibilizar',186,286,165,8,BLUE)
box(366,169,187,137,WHITE,AMBER,[4,3])
box(415,193,86,76,PALE,INK)
p('AQUECEDOR',421,220,83,9,INK,True)
p('Reserva técnica sem porta',373,281,179,8.5,AMBER)
line(459,193,459,176,MUTED)
line(583,178,583,327,BLUE,3)
box(54,328,542,10,STONE,AMBER)
box(193,349,134,134,WHITE,INK)
line(201,372,319,372,MUTED)
c.setStrokeColor(INK);c.circle(260,H-420,35,stroke=1,fill=0)
p('LAVA E SECA',212,458,120,9,INK,True)
box(379,338,158,34,WHITE,INK)
p('TANQUE',427,345,105,9,INK,True)
box(383,391,148,91,WHITE,BLUE,[3,3])
for xx in range(390,527,12):line(xx,400,xx,470,colors.HexColor('#B4C7CD'),.6)
box(389,427,136,27,WHITE)
p('CESTO VENTILADO',397,433,135,9,BLUE,True)
p('Sifão + tubulações: reservar volume',363,375,221,8,MUTED)
line(54,487,596,487,INK,1.5)
p('Pedra com apoio independente da máquina. Altura, espessura e vãos ainda não definidos.',54,505,540,9,MUTED)

p('Regras mantidas',624,128,174,12,INK,True)
p('<b>Pedra contínua:</b> Branco Itaúnas, do fim da geladeira à janela; juntas de execução serão detalhadas.',624,154,174,9.5)
p('<b>Cesto:</b> extraível, removível e transportável. A retirada não pode colidir com porta, tubulações ou sifão.',624,222,174,9.5)
p('<b>Parte alta:</b> aéreos até o teto onde houver espaço técnico; varal oculto e sem interferir nos usos previstos.',624,292,174,9.5)
p('<b>Janela:</b> sem armários nessa parede. Retorno de pedra condicionado ao peitoril, abertura e ventilação.',624,362,174,9.5)
p('<b>Acabamentos:</b> superiores Azul Petróleo; inferiores Arenza. Tons deste esquema são apenas códigos gráficos.',624,432,174,9.5)
c.showPage()

head(3,'Equipamentos para escolhermos juntos','Etapa 5 / Um morador, possibilidade de dois e visitas de mais quatro pessoas. Teto: R$ 9.000 sem instalação.')
rows=[
['<b>Lava e seca</b><br/>Midea MFA01D110B/WK<br/>Branca, 11 kg / 7 kg', '59,5 x 84,5 x 57,5 cm.<br/>Manual: profundidade total D = 61 cm; porta aberta F = 111,5 cm.', '<b>R$ 3.199</b> no Pix.<br/>R$ 3.367,37 parcelado.<br/>Loja Midea [1].', 'Candidata inicial pela capacidade e custo. Vão, folgas, tampa e manutenção ainda precisam ser compatibilizados.'],
['<b>Geladeira</b><br/>Electrolux IF44<br/>Duplex, 400 litros', '60,4 x 183,5 x 71,2 cm.<br/>Freezer na parte superior.<br/>Porta não reversível.', '<b>R$ 2.899 a R$ 3.199</b> nas páginas oficiais consultadas [2].', 'Candidata para priorizar orçamento. Conferir lado de abertura, ventilação, giro e acesso ao interior.'],
['<b>Aquecedor: cenário inicial</b><br/>Rinnai E21 FEH<br/>21 litros/min nominais', '35 x 48,3 x 15,7 cm no manual da família.<br/>Dimensões sem duto, conexões e afastamentos.', '<b>R$ 2.519 à vista</b> exibidos na Leroy Merlin [3]; validade informada: 08/09.', 'Após a confirmação de uso sem simultaneidade, avaliar E15. E21 não foi selecionado. Gás do imóvel ainda não confirmado.']
]
table(['Candidato, não aprovado','Dimensões L x A x P','Referência de preço','O que decide a escolha'],rows,[186,209,171,208],116,9)
box(34,377,774,67)
p('Orçamento de trabalho',46,386,742,12,INK,True)
p('Reservas propostas: máquina R$ 3.200 + geladeira R$ 2.900 + aquecedor R$ 2.900 = <b>R$ 9.000</b>. São metas de compra, não preços garantidos. A referência com o anúncio anterior do E21 soma R$ 8.617 a R$ 8.917.',46,409,742,10)
p('Valores consultados em 09/09/2026, sem frete, instalação, kits ou adaptação hidráulica. A oferta do aquecedor informa validade em 08/09; precisa ser renovada. O conjunto só terá preço fechado após confirmar tensão, gás, CEP e pagamento.',34,456,774,9.5,AMBER)
p('IB6 inverse: 400 L, R$ 3.699 [4], 60,1 x 186,6 x 74,7 cm. Com Midea + E21 de referência: R$ 9.417. Para manter a IB6 e a Midea dentro de R$ 9.000, o aquecedor precisa custar até R$ 2.102. E15 passa a ser avaliado; compra ainda não fechada.',34,503,774,9)
c.showPage()

head(4,'Água quente e interferências','Confirmado por Elias: não precisa de banho e torneira quente ao mesmo tempo. Rede existente ainda a conferir.')
box(34,113,374,163)
p('E15 entra na comparação',48,125,346,13,INK,True)
p('Com um ponto de uso por vez, comparar um aparelho de 15 L/min, como o Rinnai E15. A capacidade final depende da vazão do chuveiro, temperatura desejada, pressão e condições de instalação.',48,153,346,10)
p('A rede precisa chegar à cozinha, lavatório e tanque, além do chuveiro. A torneira com dois comandos no vídeo não comprova água quente na unidade.',48,222,346,10)
box(431,113,377,163)
p('Por que não fechar só pelos litros',445,125,347,13,INK,True)
p('O E15 declara 15 L/min com elevação de 20 °C. Na comparação térmica aproximada, a 30 °C de elevação seriam 10 L/min. Isso não substitui a curva nem a medição de vazão e pressão.',445,153,347,10)
p('O E15 declara acionamento a partir de 3,5 L/min. Verificar a torneira isolada e suas condições reais. O 8º andar não informa a pressão.',445,222,347,10)

table(['Interface','Condição para fechar o desenho'],[
['Lava e seca / pedra','A máquina candidata recebe água fria, conforme manual. Não ligar sua alimentação ao aquecedor. Conferir altura sob apoios, folga superior e traseira, mangueiras, abertura da porta e filtro.'],
['Circulação / portas','A profundidade total de porta aberta é medida desde a traseira do produto. Para avaliar avanço na circulação, usar a diferença entre profundidades com a mesma origem e acrescentar espaço de manuseio.'],
['Tanque / cesto / gás','Medir o volume ocupado pelas redes e sifão. O cesto permanece sob o tanque, ventilado e removível; geometria do tanque e percurso de retirada serão testados juntos.'],
['Aquecedor / aéreos / varal','Compatibilizar gás, pressão dinâmica, exaustão, ventilação permanente e afastamentos do modelo com o instalador. Sem fechamento decorativo aprovado nesta revisão.'],
['Retorno em L / janela','Medir altura de peitoril e grelha, giro da esquadria e extensão livre. A faixa de cerca de 15 cm terá suporte próprio e não poderá bloquear aberturas.']
],[190,584],294,9)
smalllink('Fonte complementar: ficha oficial Rinnai E15',urls['e15'],34,528,600)
c.showPage()

head(5,'O que esta revisão deixa encaminhado','Registro das decisões, sequência de trabalho e fontes para retomar sem depender da conversa.')
table(['Situação','Conteúdo'],[
['Confirmado por Elias','Retorno em L de aproximadamente 15 cm; escolha conjunta dos equipamentos; R$ 9.000 sem instalação; um morador, possibilidade de dois, mais quatro visitas; água quente nas torneiras, sem necessidade de banho e torneira juntos.'],
['Proposto nesta revisão','Tanque na região técnica, cesto abaixo, máquina em direção à cozinha, pedra contínua e reserva aberta para aquecedor. Midea 11/7 kg; IF44 versus IB6; avaliar E15 após confirmação de uso sem simultaneidade.'],
['Ainda a decidir','Modelos e acabamentos dos aparelhos; preferência por freezer superior ou inferior; capacidade do aquecedor após checagem da demanda. Nenhuma compra, folga de nicho ou largura de módulo foi aprovada.'],
['Próxima etapa de compatibilização','Obter gás GN/GLP, tensão dos pontos e projeto hidráulico; medir peitoril, grelhas, rebaixos, ressaltos e eixos das redes. Com isso, testar aberturas, cesto, varal e bancada em desenho cotado.']
],[169,605],113,9.5)

p('Vídeo e documentos do projeto',34,337,774,12,INK,True)
p('O vídeo completo foi recebido em 90_Arquivo_de_apoio: 12 min 54,131 s, 1920 x 1080. Nesta revisão foram conferidos os metadados; o arquivo completo não foi reproduzido novamente. As evidências visuais usadas continuam sendo os frames revisados na A01.2.',34,360,774,9)
p('A01.2 permanece salva em 02_Projeto_em_desenvolvimento/A01.2_Base_dimensional. Esta A04.2 corrige a interpretação do apoio de 15 cm e substitui as hipóteses de cabimento da A04.1 R00. Mantém as decisões do memorial v2.',34,398,774,9)

p('Fontes consultadas / links clicáveis',34,439,774,11,INK,True)
smalllink('[1] Midea: produto e preço',urls['midea'],34,462,235)
smalllink('Midea: manual Rev.04, fev.2026',urls['manual_midea'],290,462,247)
smalllink('[2] Electrolux: IF44',urls['if44'],559,462,249)
smalllink('Electrolux: catálogo e preços',urls['catalogo_electrolux'],34,487,235)
smalllink('[3] Leroy Merlin: oferta E21 GN',urls['oferta_e21'],290,487,247)
smalllink('Rinnai: manual E17 / E21 FEH',urls['manual_rinnai'],559,487,249)
smalllink('[4] Electrolux: IB6 inverse',urls['ib6'],34,512,235)
p('Fontes locais: P01, memorial v2, A01.1 R01/R02, A01.2 e respostas de Elias.',290,513,518,8.5,MUTED)
c.showPage();c.save()

md='''# A04.2 - Lavanderia e equipamentos

**R00 | 09/09/2026 | Etapas 4 e 5 | Estudo preliminar, sem liberação para fabricação**

[Abrir as cinco pranchas](A04.2_Lavanderia_e_equipamentos_R00.pdf)

## Decisões novas de Elias

- O apoio é uma faixa de pedra de aproximadamente 15 cm de largura, fazendo retorno em L junto à janela. O comprimento desse retorno e a altura ainda serão definidos. Não é uma sobra linear de 15 cm depois da máquina.
- Os modelos da lava e seca, geladeira e aquecedor serão escolhidos em conjunto.
- Orçamento total dos três: R$ 9.000, sem instalação.
- Um morador, possibilidade de dois; visitas de mais quatro pessoas.
- Água quente em todas as torneiras desejadas. O atendimento simultâneo ainda não foi respondido; não se presume abertura de todos os pontos ao mesmo tempo.

## Partido para testar

Na orientação de P01, janela à esquerda e cozinha/entrada à direita: tanque na região técnica junto à janela, cesto removível e ventilado abaixo, máquina adjacente em direção à cozinha. Pedra visualmente contínua do fim da geladeira à janela, com o retorno em L. A implantação exata do tanque e da máquina depende do volume técnico e dos modelos.

Na vista frontal voltada à bancada, a cozinha aparece à esquerda e a janela à direita. Os desenhos são diagramas sem escala, não plantas de fabricação. Os blocos não provam cabimento em 1,29 m. A cota 1,54 m é perpendicular à bancada, não um segundo comprimento disponível.

As posições e larguras dos módulos da cozinha não foram redefinidas. Preservam-se o cooktop a gás, o acesso cotidiano à air fryer e as demais decisões do memorial. A condição do limite entre cozinha e área de serviço precisa ser conferida antes de atravessá-lo com qualquer módulo.

Manter os superiores Azul Petróleo (alternativa já documentada Azul Profundo), inferiores Arenza, pedra Branco Itaúnas, piso PL01 e iluminação acolhedora do briefing. Os tons usados no PDF são gráficos e não uma simulação de amostras. Nenhuma alteração nos móveis do quarto, que permanecem sem azul.

O varal deve ser alto e oculto quando recolhido. Compatibilizar suas posições fechado e aberto com janela, aquecedor, portas e circulação, sem relaxar os requisitos do briefing. A pedra terá estrutura independente da máquina; espessura, juntas e apoios ainda pendentes. A reserva técnica do aquecedor não é autorização para fechar o equipamento com portas ou ripados.

## Candidatos iniciais, ainda não aprovados

| Equipamento | Candidato | Dimensões L x A x P | Referência de preço consultada em 09/09/2026 |
|---|---|---|---|
| Lava e seca | Midea MFA01D110B/WK-01 (127 V) ou -02 (220 V), branca, lava 11 kg e seca 7 kg | 59,5 x 84,5 x 57,5 cm; manual: D=61 cm incluindo saliências, F=111,5 cm com porta aberta | R$ 3.199 no Pix; R$ 3.367,37 parcelado na Midea |
| Geladeira | Electrolux IF44, duplex, 400 L | 60,4 x 183,5 x 71,2 cm; porta não reversível | R$ 2.899 no catálogo e R$ 3.199 na página de produto consultada; divergência a reconfirmar |
| Aquecedor | Rinnai E21 FEH, 21 L/min nominais com elevação de 20 °C | 35 x 48,3 x 15,7 cm no manual da família; sem duto, ligações e afastamentos | R$ 2.519 à vista, R$ 2.679,79 a prazo no anúncio GN prata da Leroy Merlin; a página informa validade em 08/09/2026 |

Os preços são referências observadas, não cotação firme. A validade do anúncio E21 é anterior à consulta. Não se confirmou estoque/entrega por CEP nem preço final para a versão correta. O gás da unidade e as tensões das tomadas ainda não estão confirmados. Midea -01/-02 e IF44 são versões distintas por tensão, não aparelhos bivolt.

Meta de distribuição: máquina R$ 3.200 + geladeira R$ 2.900 + aquecedor R$ 2.900 = R$ 9.000. A soma das referências com a oferta anterior do aquecedor fica em R$ 8.617 a R$ 8.917. Frete, instalação, kits e adaptações não estão incluídos. Não há folga garantida para custos adicionais.

A Electrolux IB6 inverse, branca, 400 L, é alternativa para refrigerador em cima e freezer embaixo: 60,1 x 186,6 x 74,7 cm, R$ 3.699 na loja oficial. Com as outras duas referências, total R$ 9.417: R$ 417 acima do teto, além de maior profundidade. As cores dos aparelhos são propostas de comparação, não decisões finais.

A LG VC5 CV3012WC5 de 12 kg também foi identificada como alternativa para comparação futura, mas não recebeu cotação firme nesta rodada. Não foi incorporada ao orçamento nem ao dimensionamento dos móveis. A primeira seleção não presume diferenças de durabilidade entre marcas que não foram verificadas.

## Compatibilização dos equipamentos

- A Midea anuncia profundidade C=575 mm, mas seu diagrama de instalação distingue D=610 mm, E=590 mm e F=1115 mm. Foram inspecionadas as páginas 10 e 11 do manual Rev.04 (fev.2026). Dimensões de referência admitem variação. Não usar 57,5 cm como profundidade do nicho.
- As folgas do móvel e autorização/condições de instalação sob bancada ainda precisam ser fechadas com o manual completo e assistência. A máquina não suporta a pedra. A menor altura livre sob qualquer apoio deve atender à altura instalada mais folga superior. Não se presume retirada da tampa.
- Para comparar avanço de uma porta na circulação, usar profundidades com origem comum. No diagrama Midea, F-D = 50,5 cm é o avanço adicional em relação ao envelope fechado D. Acrescentar espaço para operação e verificar a trajetória inteira da porta, não apenas o ponto final.
- A alimentação da Midea é de água fria: o manual expressamente proíbe conectar em água quente (p.6). A intenção de aquecer torneiras não altera a alimentação da máquina.
- Tanque, sifão, registros e tubulação aparente precisam de volume de manutenção. O cesto continua embaixo do tanque; tamanho e percurso não estão definidos.
- Geladeira: corpo não equivale a nicho; verificar folgas térmicas, dobradiça, abertura para retirar gavetas, relação com entrada e passagem de entrega.

## Aquecimento: comparação, não dimensionamento final

Desejo registrado: atender cozinha, lavatório, tanque e chuveiro, na medida em que forem pontos de uso desejados e houver infraestrutura adequada. A rede atual não foi comprovada pelo vídeo. A torneira de dois comandos não prova água quente na unidade.

Para comparar E17 e E21, usa-se apenas a hipótese de um chuveiro mais uma torneira. O usuário não confirmou simultaneidade. O manual declara 17 e 21 L/min para elevação de 20 °C. Mantida a potência útil como aproximação, Q(30 °C) = Q(20 °C) x 20/30: 11,3 e 14 L/min. Não são vazões medidas no apartamento nem substituem curvas do fabricante.

Por exemplo, um chuveiro hipotético de 8 L/min mais torneira de 4 L/min demandaria 12 L/min na temperatura de uso: o E21 oferece mais margem nessa comparação a 30 °C de elevação. Essas vazões e temperaturas são hipóteses didáticas; nenhum chuveiro ou torneira foi especificado. Não se conclui que o E21 atenda todos os pontos simultaneamente.

Antes da escolha: conferir pontos efetivamente alimentados, vazão dos metais, temperaturas de projeto, pressão dinâmica com os pontos em uso, gás GN/GLP e capacidade da rede, exaustão e ventilação. Avaliar vazão mínima de acionamento para torneira isolada. O andar não substitui medida de pressão. A marcenaria aguarda afastamentos e acesso de manutenção do modelo efetivamente escolhido.

## Próximos fechamentos

1. Escolher entre geladeira duplex econômica e inverse, acabamento e prioridade de marcas. A proposta inicial privilegia cumprir o teto; não houve aprovação de compra.
2. Confirmar simultaneidade de água quente e obter projetos de gás/hidráulica e tensões. Não comprar aquecedor com base apenas no anúncio GN.
3. Medir peitoril, grelha e abertura circular, rebaixos, volumes técnicos, trecho livre e eixos dos pontos. Definir comprimento do retorno em L.
4. Com modelos e folgas, desenhar implantação cotada, portas abertas, extração do cesto, varal e vistas. Depois desenvolver modulação e detalhamento da pedra.

## Vídeo recebido

Arquivo original mantido em `90_Arquivo_de_apoio/Video Apartamento Espelhado.mp4`.

- Tamanho: 179.596.236 bytes.
- Metadados: 774,131 s (12 min 54,131 s), 1920 x 1080.
- SHA-256: `1cd9822933d7199fc92150184379912301e205012e5e4fcd312cd72ffda6dc3d`.
- Nesta etapa foram conferidos arquivo e metadados, sem nova reprodução integral. As imagens de referência continuam sendo os frames já revisados e mapeados na A01.2. Não se afirma igualdade métrica entre unidades espelhadas.

## Continuidade documental

A base A01.2 já está salva dentro de `02_Projeto_em_desenvolvimento/A01.2_Base_dimensional`. Foi preservada como registro das etapas 1 a 3. Esta revisão resolve a direção do apoio de 15 cm que estava pendente ali e substitui as hipóteses de cabimento da A04.1 R00, sem apagar o histórico. O memorial v2 e as instruções mais recentes de Elias continuam sendo as fontes das decisões.

## Fontes públicas consultadas em 09/09/2026

'''
md=md.replace('O atendimento simultâneo ainda não foi respondido; não se presume abertura de todos os pontos ao mesmo tempo.', 'Elias confirmou que não precisa de banho e torneira quente funcionando juntos. Considerar um ponto de uso por vez na avaliação inicial.')
md=md.replace('## Aquecimento: comparação, não dimensionamento final', '## Aquecimento: atualização após resposta de Elias\n\nElias confirmou que não precisa de banho e torneira quente juntos. A comparação inicial com E21 fica como referência histórica de orçamento. Passa a ser avaliado o Rinnai E15 FEH para um ponto por vez, condicionado à demanda real. A ficha oficial declara 15 L/min a uma elevação de 20 °C e vazão mínima de acionamento de 3,5 L/min. Aproximação térmica para elevação de 30 °C: 10 L/min. Conferir o chuveiro, as torneiras e a rede antes da escolha.\n\nCom IB6 de R$ 3.699 e Midea de R$ 3.199, restam R$ 2.102 para o aquecedor. Isso torna possível buscar uma combinação dentro do teto, mas ainda não há cotação firme dessa combinação. Um anúncio de E15 encontrado a R$ 2.099 informava validade em 28/08 e dados contraditórios do produto; não foi adotado como oferta confirmada.\n\n### Comparação inicial preservada para contexto')
md=md.replace('Para comparar E17 e E21, usa-se apenas a hipótese de um chuveiro mais uma torneira. O usuário não confirmou simultaneidade.', 'Antes da última resposta, compararam-se E17 e E21 com a hipótese de um chuveiro mais uma torneira. Essa simultaneidade não é mais requisito do projeto.')
md=md.replace('2. Confirmar simultaneidade de água quente e obter projetos de gás/hidráulica e tensões.', '2. Considerar um ponto por vez, conforme confirmado, e obter projetos de gás/hidráulica e tensões.')
for name,url in urls.items(): md+=f'- [{name}]({url})\n'
(OUT/'A04.2_Decisoes_e_selecao_R00.md').write_text(md,encoding='utf-8')
(OUT/'A04.2_Registro_R00.json').write_text(json.dumps({
    'revisao':'R00','data':'2026-09-09','status':'estudo preliminar; equipamentos não aprovados',
    'orcamento_brl':9000,'moradores':1,'moradores_futuros':2,'visitas_adicionais':4,
    'apoio':{'forma':'retorno em L junto à janela','largura_aproximada_cm':15,'comprimento_cm':None,'altura_cm':None},
    'agua_quente':{'desejo':'todas as torneiras','necessita_banho_e_torneira_simultaneos':False,'resposta_sobre_simultaneidade_recebida':True,'rede_existente_confirmada':False,'aquecedor_em_avaliacao_apos_resposta':'Rinnai E15 FEH'},
    'reserva_orcamento_brl':{'lava_seca':3200,'geladeira':2900,'aquecedor':2900},
    'precos_observados':{'midea_pix':3199,'midea_parcelado':3367.37,'if44_catalogo':2899,'if44_pagina':3199,'e21_vista_validade_2026_09_08':2519,'ib6':3699},
    'video':{'caminho':'90_Arquivo_de_apoio/Video Apartamento Espelhado.mp4','bytes':179596236,'duracao_s':774.131,'dimensoes_px':[1920,1080],'sha256':'1cd9822933d7199fc92150184379912301e205012e5e4fcd312cd72ffda6dc3d','nova_reproducao_integral':False},
    'fontes':urls
},ensure_ascii=False,indent=2),encoding='utf-8')
print(PDF)
