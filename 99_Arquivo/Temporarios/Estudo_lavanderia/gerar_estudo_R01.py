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
PDF = OUT/'A04.2_Lavanderia_e_equipamentos_R01.pdf'
pdfmetrics.registerFont(TTFont('Segoe', 'C:/Windows/Fonts/segoeui.ttf'))
pdfmetrics.registerFont(TTFont('SegoeB', 'C:/Windows/Fonts/segoeuib.ttf'))
pdfmetrics.registerFontFamily('Segoe', normal='Segoe', bold='SegoeB')
W,H=841.89,595.28
INK=colors.HexColor('#183742'); TEXT=colors.HexColor('#26343B')
MUTED=colors.HexColor('#647477'); PALE=colors.HexColor('#EFF3F1')
STONE=colors.HexColor('#ECE8DF'); BLUE=colors.HexColor('#367791')
AMBER=colors.HexColor('#93642E'); WHITE=colors.white
c=canvas.Canvas(str(PDF),pagesize=(W,H))
c.setTitle('A04.2 - Lavanderia e equipamentos | Estudo preliminar R01')
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
    p('A04.2 / R01 / 09.09.2026',614,23,195,9,MUTED)
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
'ib6':'https://loja.electrolux.com.br/geladeira-electrolux-frost-free-inverter-400l-efficient-rapid-freeze-inverse-branca--ib6-/p',
'e15':'https://www.rinnai.com.br/aquecedores-a-gas/linha-prata/e15-1/'
}

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
p('LAVA E SECA LG<br/>VC4 / vão pendente',298,308,100,9,BLUE,True)
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
p('LAVA E SECA LG',204,455,125,9,INK,True)
p('VC4 / vão pendente',214,471,105,8,MUTED)
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


head(3,'Equipamentos: decisões atualizadas','Etapa 5 / IB6 e LG VC4 com Wi-Fi escolhidas; tensão e aquecedor pendentes. Teto atualizado por Elias: R$ 10.000.')
table(['Equipamento','Decisão vigente','Base para o projeto','Pendência'],[
['<b>Geladeira</b>','<b>Electrolux IB6</b><br/>Inverse, branca, 400 litros.<br/>Modelo escolhido por Elias.','Corpo: 60,1 x 186,6 x 74,7 cm (L x A x P). Referência registrada na R00: <b>R$ 3.699</b>.','Confirmar manual de instalação, folgas, abertura das portas e condições comerciais antes de comprar.'],
['<b>Lava e seca</b>','<b>LG VC4 com Wi-Fi.</b><br/>Branca; 12 kg de lavagem e 7 kg de secagem. Referência escolhida.','CV5012WC4 (127 V) ou CV5012WC4A (220 V). Tensão e vão pendentes. Referência parcelada: <b>R$ 4.599</b>.','Confirmar tensão e manual da VC4. Fechar o vão sob bancada, profundidade total, folgas e abertura frontal.'],
['<b>Aquecedor</b>','Modelo e capacidade pendentes. Rinnai E15 FEH continua apenas em avaliação.','Água quente nas torneiras desejadas; sem necessidade de banho e torneira juntos.','Validar demanda e infraestrutura, tipo de gás, pressão, ventilação e exaustão. Obter cotação.']
],[108,218,237,211],116,9.5)
box(34,374,774,76)
p('Orçamento atualizado: teto de R$ 10.000',46,384,742,12,INK,True)
p('IB6 R$ 3.699 + LG VC4 R$ 4.599 + candidato E15 R$ 2.446,70 = <b>R$ 10.744,70: R$ 744,70 acima do teto</b>. Após IB6 + VC4, restam R$ 1.702 para o aquecedor. Cotações registradas na A04.3.',46,408,742,11)
p('O preço da IB6 é a referência já registrada na pesquisa de 09/09/2026, não uma nova cotação desta revisão. Frete, instalação, kits e adaptações não estão incluídos. Teto atualizado para R$ 10.000 por Elias.',34,463,774,9.5,AMBER)
p('A Midea e a IF44 saem da seleção vigente. Os preços, dimensões e totais da combinação anterior ficam apenas no histórico e não dimensionam os móveis da LG.',34,510,774,9.5)
c.showPage()

head(4,'Compatibilização após a escolha','LG VC4 escolhida. Validar a versão elétrica e o manual antes de definir os vãos de instalação.')
box(34,113,374,144)
p('Geladeira IB6: corpo e nicho',48,125,346,13,INK,True)
p('A dimensão do produto é referência inicial, não a dimensão do móvel. Verificar folgas térmicas, abertura das portas e gavetas, acesso para manutenção e passagem de entrega.',48,153,346,10)
p('A bancada começa após o espaço instalado da geladeira, já consideradas as folgas necessárias.',48,216,346,10)
box(431,113,377,144)
p('LG: fechar o manual do modelo exato',445,125,347,13,INK,True)
p('LG VC4 escolhida; tensão pendente. O manual da versão correta ainda precisa ser conferido. Vão e folgas sem validação para fabricação.',445,153,347,10)
p('A pedra terá apoio independente da máquina. Não se presume retirada da tampa do equipamento.',445,216,347,10)
table(['Interface','Condição para fechar o desenho'],[
['LG / instalações','Confirmar no manual da LG escolhida: tensão, tomada e circuito, alimentação de água, escoamento, mangueiras e condições de instalação sob bancada. Não transportar especificações da Midea.'],
['LG / circulação','Conferir profundidade total fechada, porta aberta, gaveta de sabão, filtro e retirada para manutenção. Comparar profundidades de mesma origem e acrescentar espaço de manuseio.'],
['Tanque / cesto','Reservar o volume de sifão e tubulações. Manter cesto embaixo do tanque, ventilado, extraível e transportável; testar o percurso junto à porta da LG.'],
['Aquecedor / aéreos / varal','Uso de um ponto por vez na avaliação inicial. E15 permanece candidato, condicionado à demanda e à instalação. Manter ventilação e acesso; varal oculto sem conflito com equipamentos.'],
['Retorno em L / janela','Faixa de aproximadamente 15 cm de largura confirmada. Comprimento, peitoril, grelhas, giro da esquadria e apoio da pedra ainda a compatibilizar.']
],[190,584],280,9.5)
c.showPage()

head(5,'Registro da revisão R01','Esta revisão atualiza a seleção de equipamentos e substitui a R00 como referência de continuidade.')
table(['Situação','Conteúdo'],[
['<b>Decidido por Elias</b>','Geladeira Electrolux IB6, conforme a opção branca inverse de 400 L apresentada. Lava e seca LG VC4 branca com Wi-Fi escolhida; tensão pendente.'],
['<b>Requisitos mantidos</b>','R$ 10.000 para os três equipamentos, sem instalação; um morador, possibilidade de dois e visitas de mais quatro; água quente nas torneiras desejadas, sem banho e torneira simultâneos; retorno em L de aproximadamente 15 cm.'],
['<b>Próximos fechamentos</b>','Confirmar manual/tensão da VC4 e selecionar aquecedor; conferir orçamento e gás; cruzar manuais com medições e desenhar vãos, aberturas, cesto, varal e apoios da pedra.'],
['<b>Limite desta revisão</b>','As escolhas da IB6 e LG VC4 e o teto de R$ 10.000 estão registrados. Os móveis continuam em estudo preliminar, sem liberação para fabricação; não houve compra de equipamentos.']
],[169,605],113,9.5)
p('Continuidade dos documentos',34,338,774,12,INK,True)
p('A01.2 permanece como base dimensional das etapas 1 a 3. As cotas de P01 e as evidências dos levantamentos R01/R02 são preservadas. A revisão atual não refaz medições nem reinterpreta o vídeo.',34,362,774,10)
p('A04.2 R00 fica como histórico. A04.3 R01 detalha a seleção atual e os preços de referência. Teto atualizado para R$ 10.000 por instrução de Elias; os demais dados do memorial permanecem.',34,408,774,10)
p('Fontes e registro das decisões',34,455,774,11,INK,True)
smalllink('Electrolux IB6: fonte da ficha e referência de preço da R00',urls['ib6'],34,480,774)
smalllink('Rinnai E15: candidato em avaliação, ainda não selecionado',urls['e15'],34,505,774)
p('Escolhas e teto: instruções de Elias. Fontes locais: P01, memorial v2, A01.2 e A04.3 R01. Sem nova cotação.',34,530,774,8.5,MUTED)
c.showPage();c.save()
print(PDF)
