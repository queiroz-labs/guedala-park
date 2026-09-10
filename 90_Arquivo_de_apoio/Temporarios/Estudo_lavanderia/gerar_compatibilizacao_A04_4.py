from pathlib import Path
import json, subprocess, shutil
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / '02_Projeto_em_desenvolvimento/A04.4_Compatibilizacao'
PDF = OUT / 'A04.4_Implantacao_preliminar_R00.pdf'
QA = ROOT / 'tmp/pdfs/A04_4_implantacao'
QA.mkdir(parents=True, exist_ok=True)
pdfmetrics.registerFont(TTFont('Segoe', 'C:/Windows/Fonts/segoeui.ttf'))
pdfmetrics.registerFont(TTFont('SegoeB', 'C:/Windows/Fonts/segoeuib.ttf'))
pdfmetrics.registerFontFamily('Segoe', normal='Segoe', bold='SegoeB')
W, H = 841.89, 595.28
INK = colors.HexColor('#183742')
TEXT = colors.HexColor('#26343B')
MUTED = colors.HexColor('#647477')
PALE = colors.HexColor('#EFF3F1')
STONE = colors.HexColor('#ECE8DF')
BLUE = colors.HexColor('#367791')
AMBER = colors.HexColor('#93642E')
WOOD = colors.HexColor('#D7C8B5')
WHITE = colors.white
c = canvas.Canvas(str(PDF), pagesize=(W,H))
c.setTitle('A04.4 - Implantação preliminar e reservas | Guedala Park')
c.setAuthor('Projeto Apartamento Elias')

def p(text,x,top,w,size=10,color=TEXT,bold=False):
    obj=Paragraph(text,ParagraphStyle('p',fontName='SegoeB' if bold else 'Segoe',fontSize=size,leading=size*1.3,textColor=color))
    _,h=obj.wrap(w,1000)
    assert top+h < 550, (text,top,h)
    obj.drawOn(c,x,H-top-h)
    return h

def box(x,top,w,h,fill=PALE,stroke=None,dash=None):
    c.setFillColor(fill or WHITE)
    c.setStrokeColor(stroke or fill or WHITE)
    c.setLineWidth(.9)
    c.setDash(dash or [])
    c.rect(x,H-top-h,w,h,fill=int(fill is not None),stroke=int(stroke is not None))
    c.setDash([])

def line(x,t,x2,t2,color=INK,width=.9,dash=None):
    c.setStrokeColor(color); c.setLineWidth(width); c.setDash(dash or [])
    c.line(x,H-t,x2,H-t2); c.setDash([])

def label(text,x,t,size=9,color=TEXT,center=False):
    c.setFont('Segoe',size); c.setFillColor(color)
    (c.drawCentredString if center else c.drawString)(x,H-t-size,text)

def dh(x1,x2,t,text,color=BLUE):
    line(x1,t,x2,t,color,.75)
    for x in (x1,x2): line(x-3,t+4,x+3,t-4,color,.75)
    tw=pdfmetrics.stringWidth(text,'Segoe',8.5)+8
    box((x1+x2-tw)/2,t-13,tw,12,WHITE)
    label(text,(x1+x2)/2,t-13,8.5,color,True)

def dv(x,t1,t2,text,color=BLUE):
    line(x,t1,x,t2,color,.75)
    for t in (t1,t2): line(x-4,t+3,x+4,t-3,color,.75)
    c.saveState(); c.translate(x-5,H-(t1+t2)/2); c.rotate(90)
    c.setFillColor(WHITE)
    tw=pdfmetrics.stringWidth(text,'Segoe',8.5)+8
    c.rect(-tw/2,-1,tw,12,stroke=0,fill=1)
    c.setFillColor(color); c.setFont('Segoe',8.5); c.drawCentredString(0,1,text)
    c.restoreState()

def head(n,title,sub):
    box(0,0,W,8,INK)
    p('GUEDALA PARK / ELIAS',34,23,450,10,INK,True)
    p('A04.4 / R00 / 09.09.2026',613,23,195,9,MUTED)
    p(title,34,47,774,22,INK,True)
    p(sub,34,82,774,10,MUTED)
    line(34,555,808,555,colors.HexColor('#C9D3D0'),.7)
    label('ESTUDO PRELIMINAR / Apartamento ainda não entregue / Sem liberação para fabricação',34,568,8,MUTED)
    label(f'{n:02d} / 05',786,567,9,INK)

def table(headers,rows,widths,x,top,size=9):
    def cell(s,header=False):
        return Paragraph(s,ParagraphStyle('t',fontName='SegoeB' if header else 'Segoe',fontSize=size,leading=size*1.27,textColor=WHITE if header else TEXT))
    tab=Table([[cell(s,True) for s in headers]]+[[cell(s) for s in row] for row in rows],colWidths=widths)
    tab.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),INK),('ROWBACKGROUNDS',(0,1),(-1,-1),[WHITE,PALE]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
    _,h=tab.wrap(sum(widths),1000)
    assert top+h<550,(top,h)
    tab.drawOn(c,x,H-top-h)
    return h

# 1. Documento original e organização funcional, sem implantar módulos fictícios sobre P01.
head(1,'Planta: base e organização funcional','Orientação de P01 preservada: janela à esquerda; cozinha e entrada à direita.')
box(34,110,774,34)
p('As cotas do imóvel vêm da planta. Os espaços dos equipamentos vêm dos manuais. As posições finais ainda dependem das instalações e das medidas acabadas.',46,117,746,9.5)
src=Image.open(ROOT/'90_Arquivo_de_apoio/Temporarios/Base_dimensional/planta_300.png')
crop=src.crop((1180,1230,2200,1610))
c.drawImage(ImageReader(crop),44,H-157-217,582,217)
p('RECORTE DE P01<br/>Sem escala de impressão',650,157,155,9,INK,True)
p('<b>129 cm</b> serviço, paralelo à bancada.<br/><br/><b>154 cm</b> transversal do serviço.<br/><br/><b>352 cm</b> trecho da cozinha.<br/><br/><b>155 cm</b> transversal da cozinha.',650,196,155,9.5)
p('Faixa entre setores: dimensão e natureza ainda pendentes.',650,332,155,9,AMBER)
p('SEQUÊNCIA FUNCIONAL / BLOCOS SEM ESCALA',44,391,750,9,INK,True)
box(49,413,15,63,STONE,AMBER)
box(49,459,590,10,STONE,AMBER)
box(87,424,116,35,WHITE,INK)
p('TANQUE + CESTO',97,434,100,9,INK,True)
box(227,417,107,42,WHITE,BLUE,[4,3])
p('VC4<br/>Reserva: 64 cm',238,423,92,9,BLUE,True)
box(358,424,280,35,WOOD,INK)
p('COZINHA / módulos a compatibilizar',372,434,255,9,INK)
box(664,417,134,59,WHITE,BLUE,[4,3])
p('IB6<br/>Reserva: 81,1 cm<br/>Posição a testar',677,422,115,9,BLUE)
p('L: faixa de aproximadamente 15 cm de largura; extensão e apoio a definir.',44,482,588,8.5,AMBER)
p('129 + 352 = 481 cm exclui a faixa intermediária e não define a bancada. O contorno do shaft, a porta da entrada e as folgas da geladeira impedem fixar os módulos somente por essa soma.',44,507,754,9)
c.showPage()

# 2. Elevação conceitual, dimensões numéricas somente onde verificadas.
head(2,'Elevação frontal: referências de implantação','De frente para a bancada, a cozinha fica à esquerda e a janela à direita. Elevação esquemática, sem escala.')
p('Compartimentos, alturas dos aéreos e posição do aquecedor são indicativos. Os números em azul são reservas derivadas dos manuais.',34,109,774,9.5)
line(48,143,772,143,MUTED,1,[4,3])
p('TETO / REBAIXOS A INFORMAR',48,129,600,8,MUTED,True)
floor=445
s=1.35
fx=66; fw=60.1*s; fh=186.6*s
box(fx-10*s,floor-fh-10*s,fw+20*s,fh+10*s,None,BLUE,[4,3])
box(fx,floor-fh,fw,fh,WHITE,INK)
line(fx,floor-62*s,fx+fw,floor-62*s,MUTED)
p('IB6',fx+17,258,58,11,INK,True)
p('Branca',fx+12,280,61,9,MUTED)
box(191,167,355,118,colors.HexColor('#DEE8EC'),BLUE)
p('AÉREOS AZUL PETRÓLEO',207,191,322,10,INK,True)
p('Até o teto onde tecnicamente possível.<br/>Profundidade e limites a compatibilizar<br/>com forro, bancada e varal.',207,213,320,9.5)
box(405,260,127,18,WHITE,BLUE,[3,2])
p('VARAL RECOLHIDO',413,262,116,8,BLUE,True)
line(421,299,534,299,BLUE,1,[3,3])
line(421,309,534,309,BLUE,1,[3,3])
box(607,164,106,122,None,AMBER,[4,3])
p('AQUECEDOR<br/><br/>Modelo, espaço<br/>e exaustão<br/>pendentes',616,177,87,9,AMBER,True)
line(764,205,764,333,BLUE,3)
p('JANELA',729,182,77,8,BLUE,True)
p('Parede sem<br/>armários',723,340,83,8,BLUE)
box(191,318,522,8,STONE,AMBER)
box(191,326,202,119,WOOD,INK)
p('COZINHA',207,354,170,10,INK,True)
p('Pia, cooktop e área de uso<br/>da air fryer: módulos<br/>e recortes a compatibilizar.',207,375,171,9)
mx=443; mw=60*s; mh=85*s
box(mx-2*s,floor-85.5*s,mw+4*s,85.5*s,None,BLUE,[4,3])
box(mx,floor-mh,mw,mh,WHITE,INK)
line(mx,floor-mh+18,mx+mw,floor-mh+18,MUTED)
c.setStrokeColor(MUTED);c.circle(mx+mw/2,H-(floor-mh+65),25,stroke=1,fill=0)
p('LG VC4',mx+13,420,65,8,INK,True)
box(607,326,106,27,WHITE,INK)
p('TANQUE',626,332,74,9,INK,True)
p('Sifão / redes',610,359,102,8,MUTED)
box(609,378,102,64,WHITE,BLUE,[3,3])
for xx in range(617,706,10):line(xx,383,xx,437,colors.HexColor('#B4C7CD'),.6)
box(614,397,93,29,WHITE)
p('CESTO<br/>removível',624,400,79,8.5,BLUE,True)
line(48,floor,772,floor,INK,1.3)
dh(fx-10*s,fx+fw+10*s,475,'81,1 cm livres')
dh(mx-2*s,mx+mw+2*s,475,'64 cm livres')
p('85,5 cm + nivelamento',413,491,170,9,BLUE,True)
p('Vão livre sob pedra e apoios.',413,506,175,8.5,MUTED)
p('Branco Itaúnas com apoio independente da máquina. Altura final da pedra e espessura ainda a definir.',48,507,342,9)
p('A faixa em L, o cesto e o varal precisam ser testados com janela, redes e acessos.',607,491,195,9)
c.showPage()

# 3. Seções de referência: limite da porta aberta indicado como envelope, sem inventar sua trajetória.
head(3,'Lava e seca: profundidade e uso da porta','Seções transversais de referência. Cotas em centímetros; dimensionamento documental, sem levantamento local.')
p('A seção de 154 cm foi extraída de P01. As reservas abaixo acrescentam 10 cm atrás da VC4; conexões podem exigir mais espaço.',34,108,774,9.5)
scale=2.15
for n,x,opened in [(0,52,False),(1,445,True)]:
    p('PORTA FECHADA' if not opened else 'LIMITE COM PORTA A 90°',x,145,340,11,INK,True)
    fl=397; wall=x; roomend=x+154*scale
    back=x+10*scale; bodyend=back+56.5*scale
    closed=x+72*scale; extent=x+(120 if opened else 72)*scale
    box(wall,176,154*scale,221,PALE)
    line(wall,170,wall,fl,INK,2)
    line(roomend,170,roomend,fl,INK,2)
    box(back,fl-85*scale,56.5*scale,85*scale,WHITE,INK)
    line(bodyend,fl-66*scale,closed,fl-58*scale,MUTED)
    line(closed,fl-58*scale,closed,fl-25*scale,MUTED)
    line(closed,fl-25*scale,bodyend,fl-18*scale,MUTED)
    p('VC4',back+26,274,74,12,INK,True)
    p('Corpo: 85 cm<br/>de altura',back+17,301,90,9,MUTED)
    line(wall,fl,roomend,fl,INK,1.2)
    if opened:
        line(extent,178,extent,fl,BLUE,1.2,[4,3])
        p('Limite frontal<br/>a 90°',extent-97,177,94,9,BLUE,True)
        line(closed,268,extent,268,BLUE,.8,[4,3])
    else:
        line(closed,fl,closed,fl+15,BLUE,.8)
    dh(wall,extent,429,'120 [R]' if opened else '72 [R]')
    dh(extent,roomend,429,'34 [C]' if opened else '82 [C]')
    dh(wall,roomend,464,'154 [P]')
    p('10 atrás + 110 até a porta aberta' if opened else '10 atrás + 62 até a porta fechada',x,480,338,9,BLUE)
box(34,510,774,34)
p('82 cm e 34 cm são sobras aritméticas. Não incluem a pessoa nem validam o giro completo da porta, o acesso ao filtro ou a retirada da máquina.',46,517,748,9.5)
c.showPage()

# 4. Reservas próprias da geladeira; portabilidade e portas permanecem em aberto.
head(4,'Geladeira: espaço instalado e circulação','IB6 branca, 400 L. Guia oficial: corpo de 60,1 x 186,6 x 74,75 cm e afastamento de 10 cm das paredes.')
p('Reserva preliminar entre obstáculos laterais. Ventilação, abertura de portas e gavetas ainda precisam ser conciliadas com a entrada da cozinha.',34,109,774,9.5)
scale=1.35; floor=433
bx=109; bw=60.1*scale; bh=186.6*scale
top=floor-bh
p('VISTA FRONTAL',47,147,300,10,INK,True)
box(bx-10*scale,top-10*scale,bw+20*scale,bh+10*scale,None,BLUE,[4,3])
box(bx,top,bw,bh,WHITE,INK)
line(bx,floor-62*scale,bx+bw,floor-62*scale,MUTED)
p('IB6',bx+18,265,63,12,INK,True)
line(81,floor,231,floor,INK,1.3)
dv(61,top-10*scale,floor,'196,6 cm + nivelamento [R]')
dh(bx-10*scale,bx+bw+10*scale,464,'81,1 cm livres [R]')
p('60,1 + 10 de cada lado.<br/>Painéis fora da reserva.',49,484,215,9,BLUE)
p('SEÇÃO TRANSVERSAL / PORTAS FECHADAS',366,147,429,10,INK,True)
wall=398; rear=wall+10*scale; front=rear+74.75*scale; far=wall+155*scale
box(wall,166,155*scale,floor-166,PALE)
line(wall,161,wall,floor,INK,2)
line(far,161,far,floor,INK,2)
box(rear,top,74.75*scale,bh,WHITE,INK)
line(rear,floor-62*scale,front,floor-62*scale,MUTED)
p('IB6',rear+36,266,60,12,INK,True)
line(wall,floor,far,floor,INK,1.3)
dh(wall,front,464,'84,75 [R]')
dh(front,far,464,'70,25 [C]')
dh(wall,far,495,'155 [P]')
p('10 cm atrás<br/>+ 74,75 cm<br/>do produto.',643,188,153,10,BLUE)
p('70,25 cm é a diferença até a parede oposta. A posição final pode ser limitada pelo giro da porta da entrada.',643,275,153,10)
p('Abertura da IB6 e extração de gavetas: envelope ainda pendente.',643,385,153,9.5,AMBER,True)
p('Reservas térmicas não aprovam nicho fechado. Manter livre a ventilação e o acesso à conexão elétrica.',366,519,432,9,MUTED)
c.showPage()

# 5. Estado do trabalho e documentação que permite avançar antes da entrega.
head(5,'O que está definido e o que falta fechar','Elias informou que o apartamento ainda não foi entregue e que não recebeu o manual do proprietário.')
table(['Etapa','Resultado desta revisão'],[
    ['2 / Manuais','VC4: duas tensões conferidas. IB6: manual e guia conferidos. Reservas incorporadas às pranchas.'],
    ['3 / Aquecedor','GN confirmado. Addra Livo Black Matte com desviador escolhida. Aquecedor ainda sem modelo definido.'],
    ['4 / Medidas','Cotas documentais e quadro M01-M12 consolidados. Medições na unidade ficam para quando houver acesso.'],
    ['5 / Desenhos','Planta de referência, elevação esquemática e seções com reservas. Implantação final e detalhamento dos móveis ainda pendentes.'],
],[100,335],34,114,9.5)
p('DOCUMENTAÇÃO DA CONSTRUTORA',496,115,308,10,INK,True)
p('Para avançar antes da entrega, quando disponível:<br/><br/>1. Planta de instalações e cotas de pontos, forro, janela e shaft.<br/><br/>2. Dados da rede de água: pressão prevista e alimentação de água quente.<br/><br/>3. Capacidade de gás e solução prevista para ventilação e exaustão do aquecedor.',496,140,306,9.5)
box(34,344,774,54)
p('<b>Banho mantido:</b> 45 °C no inverno, água quente sem mistura; 37 °C no verão. A sensação de jato firme com a Addra Livo depende da vazão, da rede e da capacidade do aquecedor. Escolha da ducha registrada; compatibilização hidráulica pendente.',46,353,746,10)
p('FONTES E LEITURA DAS COTAS',34,418,774,10,INK,True)
p('<b>[P]</b> Planta oficial P01 / A01.2 R00. Cotas escritas prevalecem sobre o desenho.<br/><b>[R]</b> Reserva calculada: dimensões do equipamento + folgas de instalação.<br/><b>[C]</b> Diferença aritmética; não comprova circulação ou manuseio.',34,440,404,9)
p('<b>LG VC4:</b> manuais MFL71434602 e MFL71434601, pp. 10 e 12.<br/><b>IB6:</b> guia G0046764/003, pp. 2 e 6; manual G0040815/008, pp. 3 e 4.<br/><b>Decisões:</b> A04.2 R01 e registro A04.4 R00.',466,440,338,9)
p('As instalações observadas no vídeo pertencem a outra unidade espelhada. Nenhuma dimensão física foi extraída desse vídeo para completar os campos pendentes.',34,509,774,9,MUTED)
c.showPage()
c.save()

reader=PdfReader(PDF)
assert len(reader.pages)==5
for page in reader.pages:
    assert page.extract_text().strip()
pdftoppm=shutil.which('pdftoppm')
assert pdftoppm
subprocess.run([pdftoppm,'-r','140','-png',str(PDF),str(QA/'prancha')],check=True,capture_output=True)
print(PDF)
print('5 páginas geradas e renderizadas para inspeção.')
