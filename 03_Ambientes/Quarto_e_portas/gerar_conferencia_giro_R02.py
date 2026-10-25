from pathlib import Path
import math,json
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

HERE=Path(__file__).parent;ROOT=HERE.parents[1]
D=json.loads((HERE/'Conferencia_giro_canto_R02.json').read_text(encoding='utf-8'))
OUT=ROOT/'06_Entregas/pdf/Quarto_conferencia_giro_R02_2026-10-12.pdf'
for n,f in [('Reg','arial.ttf'),('Bold','arialbd.ttf')]:pdfmetrics.registerFont(TTFont(n,str(Path('C:/Windows/Fonts')/f)))
W,H=842,595;INK='#243E40';MUTED='#5E706F';PAPER='#FAF8F3';WOOD='#D8C3A4';GREEN='#B5CEC1';BLUE='#176B79';GOLD='#B77831';RED='#B14A3C';LINE='#BCC7C2'
c=canvas.Canvas(str(OUT),pagesize=(W,H));c.setTitle('Guedala Park | Conferência do giro do canto | R02');page=0
def line(x,y,xx,yy,col=LINE,w=1,dash=None):
 c.setStrokeColor(HexColor(col));c.setLineWidth(w);c.setDash(dash or []);c.line(x,H-y,xx,H-yy);c.setDash([])
def rect(x,y,w,h,col=PAPER,stroke=LINE):
 c.setFillColor(HexColor(col));c.setStrokeColor(HexColor(stroke));c.setLineWidth(.7);c.rect(x,H-y-h,w,h,fill=1,stroke=1)
def text(t,x,y,size=10,font='Reg',col=INK):
 c.setFillColor(HexColor(col));c.setFont(font,size);c.drawString(x,H-y-size,t)
def para(t,x,y,w,size=10):
 p=Paragraph(t,ParagraphStyle('p',fontName='Reg',fontSize=size,leading=size*1.4,textColor=HexColor(INK)));_,h=p.wrap(w,600)
 assert y+h<551,(page,y,h,t);p.drawOn(c,x,H-y-h);return y+h
def poly(points,col,stroke=INK):
 p=c.beginPath();p.moveTo(points[0][0],H-points[0][1])
 for x,y in points[1:]:p.lineTo(x,H-y)
 p.close();c.setFillColor(HexColor(col));c.setStrokeColor(HexColor(stroke));c.setLineWidth(.7);c.drawPath(p,fill=1,stroke=1)
def dot(x,y,col=INK,r=3):
 c.setFillColor(HexColor(col));c.circle(x,H-y,r,fill=1,stroke=0)
def start(title,sub):
 global page
 if page:c.showPage()
 page+=1;rect(0,0,W,H,PAPER,PAPER);text('GUEDALA PARK / QUARTO',30,20,10,'Bold');text('CONFERÊNCIA R02 / 12.10.2026',630,20,9,col=MUTED)
 text(title,30,49,24,'Bold');para(sub,30,86,780,10);line(30,116,812,116)
 line(30,558,812,558);text('Triagem de interferências | Ferragens documentadas; giro real e fabricação ainda não liberados.',30,570,8,col=MUTED);text(f'{page:02}',790,568,11,'Bold')
def note(title,body,x,y,w):
 text(title,x,y,12,'Bold');return para(body,x,y+21,w,10)+17
def pts(a,b):
 a,b=math.radians(a),math.radians(b);p=(65,65);q=(65-40*math.cos(a),65+40*math.sin(a));r=(q[0]+40*math.sin(a+b),q[1]+40*math.cos(a+b));return p,q,r
def diagram(x,y,s,a,b,fill=0,neigh=None):
 def tr(p):return x+p[0]*s,y+p[1]*s
 poly([tr(p) for p in [(0,0),(65,0),(65,65),(25,65),(25,105),(0,105)]],GREEN)
 rect(*tr((65,0)),48*s,65*s,WOOD,LINE)
 rect(*tr((0,105)),25*s,80*s,WOOD,LINE)
 if fill:rect(*tr((0,105)),25*s,fill*s,'#D8B68B',GOLD)
 line(*tr((25,65)),*tr((65,65)),MUTED,1,[3,2]);line(*tr((25,65)),*tr((25,105)),MUTED,1,[3,2])
 p,q,r=pts(a,b);line(*tr(p),*tr(q),BLUE,3.5);line(*tr(q),*tr(r),GOLD,3.5);dot(*tr(p),BLUE);dot(*tr(q),GOLD)
 if neigh is not None:
  width=(180-fill)/4;piv=(25,105+fill+width);d=math.radians(neigh);end=(25+width*math.sin(d),piv[1]-width*math.cos(d));line(*tr(piv),*tr(end),RED,3.5);dot(*tr(piv),RED)
 return tr

start('Abertura ampla demais cria interferência','A R01 não está validada como está. A principal correção é limitar a dobradiça da caixa; os 60° da articulação são outro movimento.')
text('155° / segunda folha retorna ao maleiro',30,133,12,'Bold',RED)
t=diagram(38,165,1.38,155,60);r=pts(155,60)[2];dot(*t(r),RED,5)
text('interferência no modelo',205,219,9,'Bold',RED)
text('92° / posição proposta para o limitador',414,133,12,'Bold',BLUE)
diagram(421,165,1.38,92,60)
para('<b>Sem limitador:</b> a ponta da segunda folha ultrapassa o plano frontal do maleiro vizinho. Isso já ocorre a 110° quando a articulação está a 60°, no modelo de eixos fixos.',30,439,363,10)
para('<b>Com limitador de 92°:</b> a posição crítica desenhada fica à frente do maleiro. A separação nominal da ponta ao plano é 4,66 cm; não é folga executiva garantida.',414,439,387,10)
para('Geometria ilustrada com eixos virtuais. A dobradiça Blum real também desloca a porta durante a abertura; por isso esta triagem identifica riscos, mas não certifica o conjunto.',30,516,772,9)

start('A porta vizinha também precisa entrar no teste','Abrir só o canto, mantendo todo o resto fechado, não verifica o uso simultâneo. Foi encontrada uma configuração de choque na R01.')
text('R01 / sem faixa fixa',30,134,12,'Bold',RED)
t=diagram(45,165,1.42,10,0,0,D['r01_simultaneous_collision_witness']['neighbour_angle_deg'])
w=D['r01_simultaneous_collision_witness'];dot(*t(w['intersection_point']),RED,5)
line(*t(w['intersection_point']),260,312,RED);text('folhas se cruzam',265,299,10,'Bold',RED)
para('Canto a 10°, articulação a 0° e porta vizinha a aproximadamente 11°. As linhas já se cruzam; acrescentar espessura não elimina esse conflito.',30,440,363,10)
text('R02 / estudar faixa fixa de 15 cm',414,134,12,'Bold',BLUE)
t=diagram(429,165,1.42,23.75,0,15,25)
text('15',*t((5,108)),10,'Bold',GOLD)
para('A primeira porta começa depois da faixa fixa e fica com dobradiças na extremidade afastada do canto. As quatro faixas móveis passam de 45 para 41,25 cm.',414,440,387,10)
para('A faixa é uma proposta para criar margem. Não foi aprovada por Elias. O interior atrás dela pode integrar o primeiro compartimento, acessível pela porta ao lado.',30,516,772,9)

start('O que a varredura geométrica mostrou','Painéis de 18 mm; eixos fixos; 88.929 pares de ângulos do canto. A porta vizinha foi envolvida por um disco que contém todo o seu giro.')
text('Faixa fixa',40,143,10,'Bold');text('Cada frente móvel',171,143,10,'Bold');text('Separação no modelo',349,143,10,'Bold');text('Leitura',550,143,10,'Bold')
for i,r in enumerate(D['transition_front_sensitivity']):
 yy=168+i*42;rect(30,yy,782,42,'#F0E9DD' if i%2==0 else PAPER,LINE)
 text(f"{r['fixed_front_cm']} cm",40,yy+12,11)
 text(f"{r['neighbour_width_cm']:.2f} cm".replace('.',','),171,yy+12,11)
 gap=r['separation_from_enclosing_disk_cm']-D['sampling_distance_bound_cm']
 text(('não separado' if gap<0 else f'>= {gap:.2f} cm'.replace('.',',')),349,yy+12,11,'Bold',RED if gap<0 else BLUE)
 label={0:'Choque demonstrado',8:'Sem afastamento suficiente no teste',10:'Margem quase nula',12:'Margem pequena para compatibilizar',15:'Reserva preferida para próximo estudo'}[r['fixed_front_cm']]
 text(label,550,yy+13,9)
para('<b>Como ler:</b> valor positivo indica separação dos painéis do canto em relação ao disco de giro da primeira porta vizinha, neste modelo. Já foi descontado 0,263 cm como limite do erro de amostragem. Resultado negativo do disco isoladamente não prova colisão; na R01 há também um cruzamento explícito entre folhas.',30,402,782,10)
para('<b>Limite importante:</b> o catálogo mostra deslocamento da porta de 32 mm em uma configuração a 90°, além de valores de protrusão e ajuste. Uma dobradiça oculta não é um pino simples no vértice. Portanto, mesmo os 4,82 cm da proposta com faixa de 15 não equivalem a folga garantida na montagem.',30,480,782,10)

start('Ferragens definidas para compatibilizar','Referências comerciais para montar o próximo desenho técnico ou gabarito. Não comprar nem cortar a partir desta triagem.')
parts=[('Principal na caixa','Blum CLIP top 71T7550 / 155°','Prende a folha A à caixa.'),('Articulação entre folhas','Blum CLIP top 79T8500 / 60°','Une B a A; aplicação em frentes de 15 a 23 mm.'),('Limitador da principal','Blum 70T7553.09 / 92°','Usar esta referência; a versão de 110° não resolve o risco encontrado.')]
for i,(title,part,body) in enumerate(parts):
 yy=139+i*77;text(title,30,yy,11,'Bold');text(part,30,yy+19,11,'Bold',BLUE);para(body,30,yy+39,400,9)
para('Quantidade, calços e furação ainda a dimensionar. A família CLIP top escolhida tem fechamento por mola; não prometer amortecimento integrado. A folha A recebe os canecos da dobradiça principal e da articulação, conforme o planejamento Blum.',30,379,400,10)
para('Conjunto baixo: duas folhas nominais 40 × 30,4 × 1,8 cm pesariam cerca de 3,50 kg de painel, com densidade hipotética de 800 kg/m³. Ferragens e puxadores acrescentam peso. Essa conta não valida duas dobradiças nem a resistência das fixações.',30,461,400,10)
y=note('O que fica preservado','Canto 65 × 105 recortado em L; profundidades 65/25; face inferior 213,2; topo de estudo 244; altura interna geométrica 27,2; varão 205.',460,139,345)
y=note('Ajuste proposto na cabeceira','Trecho restante 180 = faixa fixa 15 + quatro frentes de 41,25. Se o espaço atrás da faixa integrar o primeiro compartimento, ele ocupa 56,25 cm; os três seguintes, 41,25. Cortes e folgas ainda a descontar.',460,y,345)
y=note('Para confirmar que não bate','Montar as ferragens reais em CAD cinemático ou gabarito, com calços, recobrimentos, 18 mm, puxadores e frentes de correr. Conferir todo o curso, ajustes extremos e portas vizinhas abertas. A lista de materiais só fecha depois da conferência de carga e fixação.',460,y,345)
para('Fontes: catálogo oficial Blum 2025, pp. 31, 32 e 47; planejamento do canto, catálogo 2024/2025 p. 117; artigo oficial sobre limitadores 155°. Consultados em 12/10/2026.',460,y,345,9)
text('Catálogo / planejamento / limitador',460,530,9,'Bold',BLUE)
for x1,x2,url in [(460,515,'https://d2.blum.com/services/BEC003/concealedhinges_ep_dok_bus_%24sen-us_%24aof_%24v18.pdf'),(518,602,'https://publications.blum.com/2024/catalogue/en/117/'),(604,805,'https://ea.blum.com/en/opening-angle-stops-155-hinges/')]:c.linkURL(url,(x1,H-545,x2,H-527),relative=0)
c.save();print(OUT)
