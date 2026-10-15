from pathlib import Path
import math, json
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).parent
OUT = ROOT / 'output/pdf/Quarto_canto_independente_R01_2026-10-12.pdf'
for name, file in [('Reg','arial.ttf'),('Bold','arialbd.ttf')]:
    pdfmetrics.registerFont(TTFont(name, str(Path('C:/Windows/Fonts') / file)))
W,H=842,595
INK='#243E40'; MUTED='#5E706F'; PAPER='#FAF8F3'; WOOD='#D8C3A4'; GREEN='#B5CEC1'; BLUE='#176B79'; GOLD='#B77831'; LINE='#BCC7C2'
c=canvas.Canvas(str(OUT),pagesize=(W,H)); c.setTitle('Guedala Park | Canto independente articulado | Estudo R01')
page=0
def line(x,y,xx,yy,col=LINE,width=1,dash=None):
    c.setStrokeColor(HexColor(col)); c.setLineWidth(width); c.setDash(dash or []); c.line(x,H-y,xx,H-yy); c.setDash([])
def rect(x,y,w,h,col=PAPER,stroke=LINE):
    c.setFillColor(HexColor(col));c.setStrokeColor(HexColor(stroke));c.setLineWidth(.7);c.rect(x,H-y-h,w,h,fill=1,stroke=1)
def text(t,x,y,size=10,font='Reg',col=INK):
    c.setFillColor(HexColor(col));c.setFont(font,size);c.drawString(x,H-y-size,t)
def para(t,x,y,w,size=10):
    p=Paragraph(t,ParagraphStyle('p',fontName='Reg',fontSize=size,leading=size*1.4,textColor=HexColor(INK)))
    _,h=p.wrap(w,600); assert y+h<554,(page,y,h,t);p.drawOn(c,x,H-y-h);return y+h
def poly(points,col,stroke=INK):
    p=c.beginPath();p.moveTo(points[0][0],H-points[0][1])
    for x,y in points[1:]:p.lineTo(x,H-y)
    p.close();c.setFillColor(HexColor(col));c.setStrokeColor(HexColor(stroke));c.setLineWidth(.8);c.drawPath(p,fill=1,stroke=1)
def dot(x,y,col=INK):
    c.setFillColor(HexColor(col));c.circle(x,H-y,3,fill=1,stroke=0)
def dim(x,y,xx,yy,t):
    line(x,y,xx,yy,MUTED)
    if y==yy:
        for a in (x,xx):line(a,y-3,a,y+3,MUTED)
        sw=pdfmetrics.stringWidth(t,'Reg',9);rect((x+xx-sw)/2-3,y-16,sw+6,14,PAPER,PAPER);text(t,(x+xx-sw)/2,y-15,9)
    else:
        for a in (y,yy):line(x-3,a,x+3,a,MUTED)
        text(t,x+6,(y+yy)/2-5,9)
def start(title,sub):
    global page
    if page:c.showPage()
    page+=1;rect(0,0,W,H,PAPER,PAPER)
    text('GUEDALA PARK / QUARTO',30,20,10,'Bold');text('ESTUDO R01 / 12.10.2026',660,20,9,col=MUTED)
    text(title,30,48,25,'Bold');para(sub,30,85,780,10);line(30,114,812,114)
    line(30,558,812,558);text('Cotas em cm | Proposta dimensional; medidas de corte, ferragens e montagem ainda não liberadas.',30,570,8,col=MUTED);text(f'{page:02}',790,568,11,'Bold')
def note(title,body,x,y,w=278):
    text(title,x,y,12,'Bold');return para(body,x,y+22,w,10)+20

start('Um compartimento próprio na quina','Direção acolhida por Elias: aprofundar o canto independente com duas folhas articuladas. As dimensões abaixo são uma proposta nova.')
ox,oy,s=79,163,1.16
def xy(x,y):return ox+x*s,oy+y*s
def rr(x,y,w,h,col):rect(*xy(x,y),w*s,h*s,col,INK)
rr(65,0,135,65,WOOD);rr(0,105,25,180,WOOD)
poly([xy(x,y) for x,y in [(0,0),(65,0),(65,65),(25,65),(25,105),(0,105)]],GREEN)
line(*xy(25,65),*xy(65,65),BLUE,4);line(*xy(25,65),*xy(25,105),GOLD,4)
for y in (150,195,240):line(*xy(0,y),*xy(25,y),MUTED)
line(*xy(132.5,58),*xy(198,58),BLUE,1.5);line(*xy(67,62),*xy(133,62),BLUE,1.5)
text('CANTO',*xy(7,22),10,'Bold');text('ÚNICO',*xy(7,35),10,'Bold')
text('Maleiro reto',*xy(80,18),10,'Bold');text('135 × 65',*xy(93,36),10)
dim(*xy(0,-14),*xy(65,-14),'65');dim(*xy(65,-14),*xy(200,-14),'135')
dim(*xy(-21,0),*xy(-21,105),'105');dim(*xy(218,0),*xy(218,65),'65')
dim(*xy(25,83),*xy(65,83),'40');dim(*xy(78,65),*xy(78,105),'40')
dim(*xy(0,297),*xy(25,297),'25')
line(*xy(25,187),*xy(72,187),MUTED);text('Aéreo raso restante',*xy(76,175),10,'Bold');text('180 × 25 / quatro módulos ~45',*xy(76,194),9)
para('Planta nominal dos armários altos. A região verde é um L, não um retângulo maciço de 65 × 105.',350,426,148,9)
y=note('Duas frentes, um só espaço','Faixas de frente de 40 + 40. Sem montante vertical na quina de acesso. Laterais apenas nas extremidades do módulo; base e tampa em L.',521,133)
y=note('O trecho fundo tem 65 cm','A profundidade de 25 sobre a cabeceira é preservada. O ganho é acessar o volume fundo que antes ficava atrás do encontro.',521,y)
y=note('A antiga junta muda','Os 3 cm entre os dois móveis deixam de existir dentro deste canto integrado. Folgas entre portas passam a seguir o desenho da ferragem; não manter um vazio de 3 cm na articulação.',521,y)
note('Sem ampliar o móvel sobre a cama','O envelope externo do conjunto é preservado, exceto pelo preenchimento da antiga junta. A passagem nominal de 49 cm no piso não muda.',521,y)

start('Como as duas folhas trabalham','A folha A prende na caixa; a folha B prende na A. As portas se articulam para liberar as duas faces do canto.')
def mini(x,y,stage):
    s=1.48
    def p(a,b):return x+a*s,y+b*s
    poly([p(a,b) for a,b in [(0,0),(65,0),(65,65),(25,65),(25,105),(0,105)]],GREEN)
    rect(*p(65,0),38*s,65*s,WOOD,LINE);rect(*p(0,105),25*s,34*s,WOOD,LINE)
    P=(65,65);Q=(25,65);R=(25,105)
    # Ideal line-segment model, not manufacturer axis geometry or a collision certification.
    if stage==1:R=(25+40*math.sin(math.radians(60)),65+40*math.cos(math.radians(60)))
    if stage==2:Q=(65,105);R=(65+40*math.cos(math.radians(-60)),105+40*math.sin(math.radians(-60)))
    line(*p(65,65),*p(25,65),MUTED,1,[3,3]);line(*p(25,65),*p(25,105),MUTED,1,[3,3])
    line(*p(*P),*p(*Q),BLUE,4);line(*p(*Q),*p(*R),GOLD,4)
    dot(*p(*P),BLUE);dot(*p(*Q),GOLD)
    if stage==0:
        text('A',*p(43,53),11,'Bold',BLUE);text('B',*p(30,83),11,'Bold',GOLD)
    if stage==2:
        text('acesso',*p(25,71),9,'Bold',BLUE);text('ao canto',*p(25,82),9,'Bold',BLUE)

for i,(title,body) in enumerate([
 ('1 / Fechado','As duas folhas fazem a quina em 90°. O compartimento é independente dos módulos vizinhos.'),
 ('2 / Articulação','A folha B gira na dobradiça de canto. Ela acompanha a folha principal durante o manuseio.'),
 ('3 / Acesso','O conjunto se afasta do vão. Não são duas portas com dobradiças fixas em paredes opostas.')]):
    x=38+i*267;text(title,x,134,13,'Bold');mini(x+12,172,i);para(body,x,390,238,10)
rect(30,469,782,72,'#E8EEEA','#CAD6CF')
para('<b>Desenho de princípio, não simulação da ferragem.</b> A última posição usa giro ilustrativo de 90° na caixa e 60° na articulação. Os eixos foram simplificados: espessuras, braços e folgas não estão modelados. Não há validação de curso livre, de abertura simultânea ou de limitador a 90°.',44,480,752,10)

start('Medidas, ferragens e o que falta fechar','O conceito tem ferragem comercial documentada. A aplicação no nosso maleiro baixo ainda precisa de compatibilização.')
rows=[('Altura dos três trechos','Face inferior 213,2 / topo da caixa 244'),('Altura externa / interna','30,8 / 27,2 antes das ferragens'),('Canto proposto','Envelope 65 × 105, recortado em L'),('Frentes do canto','Faixas nominais 40 + 40; corte a calcular'),('Maleiro reto restante','135 × 65; duas folhas de correr a estudar'),('Aéreo raso restante','180 × 25; quatro faixas nominais de 45')]
text('PROPOSTA DIMENSIONAL',30,134,11,'Bold')
for i,(a,b) in enumerate(rows):
    yy=160+i*43;rect(30,yy,435,43,'#F0E9DD' if i%2==0 else PAPER,LINE);text(a,40,yy+5,9,'Bold');text(b,40,yy+22,10)
para('Alturas calculadas com teto de estudo 247, arremate 3 e chapas de 1,8. A profundidade total de 65 inclui portas. Caixa útil menor; não chamar o envelope de espaço interno.',30,428,435,10)
para('Para guardar: roupas de cama dobradas e volumes baixos. O fundo do canto continuará exigindo alcance. Não prometer entrada de malas ou caixas pelo tamanho interno: conferir também o vão real.',30,489,435,10)
y=note('Referência comercial','Blum CLIP top 79T8500, para frentes de 15 a 23 mm, combinada com dobradiça de 155° ou 170° na caixa. MDF de 18 mm cabe na faixa de espessura. Isso não valida carga, quantidade ou curso do conjunto.',496,133,310)
y=note('Três verificações decisivas','1. Eixos, folgas e movimento junto às portas vizinhas.<br/>2. Fixação e quantidade de dobradiças para o par baixo de folhas; posição dos canecos.<br/>3. Sustentação da base/tampa em L e divisão do maleiro, sem interferir no varão a 205.',496,y,310)
y=note('O que continua pendente','Ferragem das portas de correr do maleiro reto, agora menor. A RO-32 continua sem aprovação. Também falta definir puxador e eventual limitação de abertura do canto.',496,y,310)
para('Referência: catálogo oficial Blum, p. 32 (2025), consultado em 12/10/2026. Folhas podem ter larguras iguais ou diferentes; o corte depende dos descontos da montagem.',496,y,310,9)
c.linkURL('https://d2.blum.com/services/BEC003/concealedhinges_ep_dok_bus_%24sen-us_%24aof_%24v18.pdf',(496,H-546,806,H-515),relative=0)
text('Abrir catálogo oficial da Blum',496,531,9,'Bold',BLUE)
c.save()

result={'status':'proposta R01 para estudo; conceito acolhido, medidas não aprovadas para fabricação','date':'2026-10-12','units':'cm','plan_coordinates':'x ao longo do guarda-roupa; y ao longo da cabeceira; origem na quina externa nominal, sem camadas posteriores','corner_polygon':[[0,0],[65,0],[65,65],[25,65],[25,105],[0,105]],'nominal_front_bands':[40,40],'straight_maleiro':[135,65],'straight_aerial':[180,25],'aerial_nominal_front_bands':[45,45,45,45],'underside':213.2,'shelf_top':215,'body_top_assumed':244,'ceiling_assumed':247,'body_height':30.8,'inner_geometric_height':27.2,'panels_assumed':1.8,'old_gap_3cm':'substituída por módulo de canto integrado; folgas de ferragem a detalhar','opening_diagram':'segmentos ideais; giro ilustrativo 90 na caixa e 60 entre folhas; sem validação cinemática, colisão, carga ou limitador','hardware_candidate':'Blum 79T8500 + dobradiça de caixa 155 ou 170; quantidades e montagem pendentes','source':'https://d2.blum.com/services/BEC003/concealedhinges_ep_dok_bus_%24sen-us_%24aof_%24v18.pdf','source_page':32}
(HERE/'Canto_independente_R01_2026-10-12.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(OUT)
