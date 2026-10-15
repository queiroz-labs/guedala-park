from pathlib import Path
import math, json
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).parent
OUT=ROOT/'output/pdf/Quarto_armario_em_L_2026-10-12.pdf'
OUT.parent.mkdir(parents=True,exist_ok=True)
for name,file in [('Reg','arial.ttf'),('Bold','arialbd.ttf')]:pdfmetrics.registerFont(TTFont(name,str(Path('C:/Windows/Fonts')/file)))
W,H=842,595
INK='#263E40';MUTED='#617171';PAPER='#FAF8F3';WOOD='#C6A77C';PALE='#E8DCC9';BLUE='#3A666D';LINE='#BBC1BB'
c=canvas.Canvas(str(OUT),pagesize=(W,H));c.setTitle('Quarto | Encontro do armário em L | Direção aceita em 12/10/2026')
page=0
def rect(x,y,w,h,fill=PALE,stroke=LINE):
 c.setFillColor(HexColor(fill));c.setStrokeColor(HexColor(stroke));c.setLineWidth(.7);c.rect(x,H-y-h,w,h,fill=1,stroke=1)
def line(x,y,x2,y2,color=LINE,width=.8,dash=None):
 c.setStrokeColor(HexColor(color));c.setLineWidth(width);c.setDash(dash or []);c.line(x,H-y,x2,H-y2);c.setDash([])
def text(s,x,y,size=10,font='Reg',color=INK):
 c.setFillColor(HexColor(color));c.setFont(font,size);c.drawString(x,H-y-size,s)
def para(s,x,y,w,size=10,font='Reg',color=INK):
 p=Paragraph(s,ParagraphStyle('p',fontName=font,fontSize=size,leading=size*1.4,textColor=HexColor(color)))
 _,h=p.wrap(w,500);assert y+h<551,(page,s,y,h);p.drawOn(c,x,H-y-h);return y+h
def note(title,body,y,x=558,w=250):
 text(title,x,y,12,'Bold');return para(body,x,y+23,w)+22
def start(title,sub):
 global page
 if page:c.showPage()
 page+=1;rect(0,0,W,H,PAPER,PAPER)
 text('GUEDALA PARK / QUARTO',30,21,10,'Bold');text('DIREÇÃO ACEITA / ESTUDO',600,21,9,color=MUTED)
 text(title,30,49,24,'Bold');text(sub,30,85,10,color=MUTED);line(30,108,812,108)
 line(30,557,812,557);text('12/10/2026 | COTAS EM CM | DETALHAMENTO DE ESTUDO, SEM LIBERAÇÃO DE FABRICAÇÃO',30,570,8,color=MUTED);text(str(page).zfill(2),791,568,11,'Bold')
def dim(x,y,x2,y2,label):
 line(x,y,x2,y2,MUTED)
 if y==y2:
  for xx in [x,x2]:line(xx,y-4,xx,y+4,MUTED)
  size=9;sw=pdfmetrics.stringWidth(label,'Reg',size);rect((x+x2-sw)/2-3,y-16,sw+6,14,PAPER,PAPER);text(label,(x+x2-sw)/2,y-15,size)
 else:
  for yy in [y,y2]:line(x-4,yy,x+4,yy,MUTED)
  text(label,x+7,(y+y2)/2-6,9)

start('O L fica no alto, com o canto bem definido','Recomendação: maleiro com portas de correr; aéreo raso com portas de abrir; topo visual contínuo em Arenza.')
ox,oy,s=86,163,1.13
def plan(x,y,w,d,col=PALE):rect(ox+x*s,oy+y*s,w*s,d*s,col,INK)
plan(0,0,200,60,WOOD);plan(0,63,25,222,PALE);plan(0,0,25,60,'#A6B8AB')
line(ox,oy+60*s,ox+200*s,oy+60*s,BLUE,2)
for yy in [63,118.5,174,229.5,285]:line(ox,oy+yy*s,ox+25*s,oy+yy*s,INK)
text('Maleiro do guarda-roupa',ox+36,oy+12,10,'Bold');text('Portas deslizam nesta frente',ox+36,oy+37,8)
dim(ox,oy-16,ox+200*s,oy-16,'200 - referência preservada')
dim(ox+217*s,oy,ox+217*s,oy+60*s,'60')
dim(ox,oy+300*s,ox+25*s,oy+300*s,'25')
line(ox+25*s,oy+62*s,ox+82*s,oy+99*s,BLUE);text('Junta técnica de estudo: 3',ox+83*s,oy+97*s,10,'Bold')
line(ox+25*s,oy+162*s,ox+82*s,oy+162*s,BLUE);text('Aéreo sobre a cabeceira',ox+83*s,oy+154*s,11,'Bold')
para('Extensão no modelo: 225.<br/>Com junta de 3: corpo de estudo 222.<br/>Extremidade junto à janela a conferir.',ox+83*s,oy+178*s,242,10)
text('PLANTA DOS ARMÁRIOS ALTOS',30,125,10,'Bold')
y=note('Um único volume no canto','A faixa de 25 × 60 em destaque pertence ao maleiro. O aéreo termina antes da frente do guarda-roupa; não há dois móveis sobrepostos.',131)
y=note('Aparência','Mesmo Arenza e arremate superior alinhado ao teto. O encontro tem uma pequena junta recuada e um desnível inferior de 8,2 cm.',y)
y=note('Aberturas separadas','Portas de correr no maleiro evitam varrer o aéreo. Portas do aéreo abrem para a cama, com curso de estudo até 90°.',y)
y=note('Programa preservado','Quatro gavetas, cabideiros, divisão entre moradores e maleiro permanecem. RO-32 é a referência técnica proposta para o maleiro; condições nas páginas 5 e 6.',y)
text('Planta nominal sem camadas posteriores. Cenário com proteção e limites de acesso: página 3.',30,532,9,color=MUTED)

start('O desnível correto é de 8,2 cm','Manter as duas bases preserva os cabideiros e a altura disponível do aéreo da cabeceira.')
text('VISTAS DESDOBRADAS DO TRECHO SUPERIOR / ALTURA AMPLIADA PARA LEITURA',30,124,9,'Bold')
base=434;v=3.1;left=55;split=285;end=507
def z(h):return base-(h-190)*v
# Body top 244 is illustrative: H247 minus trim3; not a measured bedroom ceiling.
rect(left,z(247),200,z(244)-z(247),WOOD);rect(split,z(247),222,z(244)-z(247),WOOD)
rect(left,z(244),200,z(215)-z(244),WOOD);rect(left,z(215),200,1.8*v,PALE,INK)
rect(split,z(244),222,z(206.8)-z(244),PALE);rect(split,z(206.8),222,1.8*v,WOOD,INK)
line(left+100,z(244),left+100,z(215),INK)
for div in [55.5,111,166.5]:line(split+div,z(244),split+div,z(205),INK)
line(left,z(205),left+200,z(205),BLUE,2)
text('Varão superior: 205',left+12,z(205)+9,10,'Bold',BLUE)
text('Maleiro',left+62,z(235),13,'Bold');text('Aéreo raso',split+69,z(235),13,'Bold')
line(left,z(215),left+200,z(215),INK,1.5);text('215 / superfície de guarda',left,z(215)-17,9)
line(left+200,z(213.2),split-7,z(213.2),BLUE,1,[3,2]);line(split-7,z(213.2),split-7,z(205),BLUE,1)
text('8,2',split-35,z(210),10,'Bold',BLUE)
text('Face inferior: 213,2',left+35,z(213.2)+7,9);text('Face inferior: 205',split+49,z(205)+9,10,'Bold')
text('Teto 247 e arremate 3 são somente cenário ilustrativo',55,173,9,color=MUTED)
line(55,z(247),507,z(247),INK,1,[3,2])
y=note('A conta','215 é a superfície superior da prateleira do maleiro. Com chapa de 1,8: face inferior 213,2. Portanto, 213,2 - 205 = <b>8,2 cm</b>.',131)
y=note('Por que manter o degrau','Baixar o maleiro para alinhar a base a 205 colocaria sua chapa na altura do varão. Subir o aéreo para 213,2 retiraria 8,2 cm da sua altura útil.',y)
y=note('Topo real','Definir C = teto acabado - arremate de montagem. Ambos os corpos terminam em C; o arremate completa visualmente até o teto.',y)
y=note('Exemplo de altura útil','Se teto 247 e arremate 3: C = 244.<br/>Maleiro: 244 - 1,8 - 215 = 27,2.<br/>Aéreo: 244 - 205 - 3,6 = 35,4.',y)
para('A base inferior contínua não é requisito aprovado. A continuidade proposta acontece no topo, no material e na virada em L. Chapas de 18 mm continuam hipótese; resistência e vãos precisam de dimensionamento.',30,487,485,10)

start('Portas e alcance: o que o desenho resolve','Verificação de volumes e trajetórias ideais; medidas de ferragens e objetos reais permanecem necessárias.')
ox,oy,s=81,179,1.33
rect(ox,oy,200*s,60*s,WOOD,INK);rect(ox,oy+63*s,25*s,111*s,PALE,INK)
for yy in [63,118.5,174]:line(ox,oy+yy*s,ox+25*s,oy+yy*s,INK)
# Sliding doors remain inside the maleiro footprint, ending at its front plane.
line(ox+2*s,oy+58*s,ox+110*s,oy+58*s,BLUE,2)
line(ox+91*s,oy+55*s,ox+198*s,oy+55*s,BLUE,2)
text('Maleiro: movimento paralelo à frente',ox,oy-24,11,'Bold')
for hi in [118.5,174]:
 hinge=(ox+25*s,oy+hi*s)
 for angle in [30,60,90]:
  a=math.radians(angle);x2=hinge[0]+55.2*s*math.sin(a);y2=hinge[1]-55.2*s*math.cos(a)
  line(*hinge,x2,y2,BLUE,1,[3,3] if angle!=90 else None)
text('Aéreo: 0°, 30°, 60°, 90°',ox+55,oy+199*s,10,'Bold')
dim(ox+25*s,oy+191*s,ox+80.2*s,oy+191*s,'55,2 / folha de teste')
para('Quatro frentes nominais no aéreo de 222: passo 55,5; folha de teste 55,2 com junta de 3 mm. São parâmetros de ensaio, não uma lista de corte.',30,476,485,10)
y=note('Resultado geométrico','Até 90°, as folhas do aéreo permanecem no seu próprio trecho longitudinal. O plano do maleiro fica separado pela junta de 3 cm. Não é necessário alternar a abertura dos dois móveis neste modelo.',131)
y=note('Onde o acesso é menor','O aéreo ocupa a aproximação direta aos primeiros 25 cm do maleiro esquerdo. Esse canto é alcançado pela abertura ao lado; não contar como acesso frontal integral.',y)
y=note('Exemplo de abertura livre','Vão total hipotético 196,4 e transpasse de estudo 2,5: abertura nominal ~96,95. No lado do aéreo, faixa frontal direta ~73,75 cm antes dos demais descontos.',y)
y=note('Camadas posteriores','Cenário com 1 cm: projeções 61 e 26; aéreo passa de 222 para 221 se a ponta oposta ficar fixa. Proteção lateral também desloca a caixa de 200; conferir a entrada sem reduzir seu interior.',y)
text('A proteção é dependência já registrada no projeto; material, instalação e faces aplicáveis devem ser conferidos no detalhamento.',30,531,8,color=MUTED)

start('Direção aceita para desenvolver o conjunto','Aceite funcional em 12/10/2026; medidas de estudo e ferragens ainda dependem do detalhamento técnico.')
items=[('FORMA','Dois corpos em L, frentes retas, mesmo Arenza, topo visual contínuo e base com degrau de 8,2.'),('ENCONTRO','Canto pertence ao maleiro; junta técnica nominal 3; sem somar o volume duas vezes ou criar outro armário sobre o guarda-roupa.'),('PORTAS','Maleiro: duas folhas de correr, sistema contido no envelope de 60. Aéreo: quatro folhas de abrir como ensaio, limitadas a 90°.'),('USO','Canto do maleiro esquerdo para itens ocasionais que passem pela abertura real; conferir retirada de malas e caixas. Acesso pelo colchão já decidido.'),('ESTRUTURA','Dimensionar apoios e fixações próprios para os corpos. Arremate ao teto é acabamento; não contar com o forro como apoio.'),('ANTES DE FABRICAR','Medir teto/piso/paredes/janela; selecionar ferragens e suas folgas; conferir portas, largura útil, profundidades e objetos; dimensionar painéis e fixações.')]
for i,(label,body) in enumerate(items):
 yy=135+i*60;text(label,30,yy,10,'Bold');para(body,156,yy,365,10)
y=note('O que foi preservado','Caixa de referência 200 × 60, varão superior a 205, superfície do maleiro a 215, quatro gavetas, divisão igual e aéreo raso.',131)
y=note('O que esta rodada resolveu','Diferença correta das bases; posição e propriedade do canto; estratégia de portas sem varredura cruzada; parâmetros de encontro e suas tolerâncias.',y)
y=note('O que falta dimensionar','Junta 3; quatro frentes; altura e comprimento dos corpos são estudo. RO-32 proposto nas páginas seguintes; aplicação nas folhas baixas e largas ainda precisa de confirmação.',y)
para('<b>Fontes locais:</b> Guarda-roupa interior R02; Cabeceira e armário superior R00; Aéreos contínuos 25/09; modelo R09; revisão de piso e armários 25/09; auditoria de ambientes 06/10.',30,512,780,9,color=MUTED)
start('Maleiro: referência Rometal RO-32','Proposta de ferragem para duas portas internas em Arenza; seleção técnica condicional, sem compra ou corte.')
text('FRENTE ESQUEMÁTICA / CENÁRIO DE TETO 247',30,126,10,'Bold')
rect(52,181,460,135,WOOD,INK)
rect(62,193,440,110,PAPER,INK)
rect(62,207,222.8,82,PALE,INK)
rect(279.2,207,222.8,82,WOOD,INK)
for xx in [87,255,304,477]:
 rect(xx,284,12,7,BLUE,BLUE)
text('2 carros com rolamento por folha',99,325,10,'Bold')
dim(62,171,502,171,'196,4 / vão nominal')
dim(62,364,284.8,364,'99,45 / folha nominal')
line(282,215,392,154,BLUE);text('Transpasse: 2,5',375,137,10,'Bold')
para('Porta 1 em uma via; porta 2 em outra. Guias superiores acompanham as duas extremidades de cada folha. Desenho ilustra o princípio, sem escala vertical e sem gabarito de furação.',30,393,485,10)
para('<b>Pegada proposta:</b> puxador de embutir, sem projeção que impeça o cruzamento das folhas. Ensaiar posição acessível fora da faixa encoberta pelo aéreo e afastada de carros/guias.',30,466,485,10)
y=note('Conjunto de referência','RO-32 com rolamento, fixação embutida na face interna. Para MDF de 18 mm: estudar RM-030 superior e RM-022 inferior, conforme manual Rev. 12.',131)
y=note('Quantitativo para cotação','Dois kits de uma porta: total de 4 carros, 4 guias e 4 freios. Duas vias superiores e duas inferiores; prever ~1,964 m por via, com corte final em obra.',y)
y=note('Altura das folhas','Vão vertical de estudo 27,2. Manual Rev. 12: descontar 3,2; folha de estudo 24,0. A página comercial desconta 2,5: divergência de 7 mm a confirmar antes do corte.',y)
y=note('Peso estimado','Folha 99,45 × 24 × 1,8: ~3,44 kg com densidade hipotética 800 kg/m³. Com provisão de 0,6 kg para acessórios: ~4,04 kg. Confirmar peso acabado.',y)

start('O que fecha agora e o que depende da aplicação','A escolha de referência avança; confirmação técnica da Rometal e levantamento final ainda necessários.')
text('RESERVA FRONTAL DO MALEIRO / CORTE EM PLANTA',30,126,10,'Bold')
rect(58,177,455,121,PALE,INK)
rect(58,177,14,121,WOOD,INK)
rect(457,177,56,121,'#D6E0D7',INK)
line(475,177,475,298,BLUE,3);line(497,177,497,298,BLUE,3)
text('fundo',45,310,9);text('guarda',251,225,13,'Bold');text('vias',470,309,9)
dim(58,154,513,154,'60 / profundidade externa de referência')
dim(457,340,513,340,'7 / reserva')
para('Reserva frontal proposta de 7 cm, dentro dos 60 cm existentes. Com fundo hipotético de 1,8, restam 51,2 cm brutos atrás dessa faixa. Reserva de projeto, não dimensão certificada do kit; conferir perfil, guia e puxador.',30,365,485,10)
para('A divisória central deve apoiar a estrutura sem atravessar o percurso dos carros e folhas. Recuo, ligação e resistência do apoio inferior precisam do detalhamento da marcenaria. Os freios limitam o curso; não foram especificados amortecedores.',30,448,485,10)
y=note('Escolha comparada','SlideLine 55 do catálogo brasileiro exige altura de 70 a 150 cm e largura de 40 a 80 cm. Não atende às folhas baixas e ~99 cm largas deste estudo.',131)
y=note('Confirmar com a Rometal','1. RO-32 admite folha ~99,45 × 24 × 1,8 cm? Há limite de proporção ou retenção adicional?<br/>2. Para RM-030/RM-022 e guia compatível, descontar 32 ou 25 mm? Confirmar revisão, guia e kit exatos.',y)
y=note('Conferir no móvel','Medir o vão acabado; pesar folhas; verificar retirada para manutenção, retenção, deslizamento, acesso ao canto e alinhamento dos trilhos. Teto de 240/247/257 gera folhas de estudo 17/24/34 cm pelo desconto de 32 mm.',y)
para('<b>Fontes:</b> Rometal RO-31/32, página do produto e manual cód. 2086 Rev. 12; Hettich Brasil, catálogo SlideLine 55, p. 220. Consultados em 12/10/2026. Links ativos: ',30,517,780,8,color=MUTED)
text('Rometal / produto',30,540,8,color=BLUE);c.linkURL('https://www.rometal.com.br/sistemas/solucoes-para-balcoes-aereos-e-paineis/s/sustentacao-na-base/ro-3132',(30,H-550,130,H-538),relative=0)
text('Rometal / manual Rev. 12',170,540,8,color=BLUE);c.linkURL('https://www.rometal.com.br/download/ef75b9d8-6780-11f1-bfb1-02006e230003/en',(170,H-550,305,H-538),relative=0)
text('Hettich / catálogo consultado',350,540,8,color=BLUE);c.linkURL('https://hettich.com.br/wp-content/uploads/sites/2/2022/12/Catalogo-Produto-SlideLine-55.pdf',(350,H-550,515,H-538),relative=0)
c.save()

# Analytical bounds plus sampled coordinates: no hardware or structural certification.
samples=[]
for i in range(4):
 hinge=63+(i+1)*55.5-.15
 for degrees in range(91):
  a=math.radians(degrees)
  for j in range(101):
   t=55.2*j/100
   samples.append((25+t*math.sin(a),hinge-t*math.cos(a)))
min_y=min(y for x,y in samples)
assert min_y>60
assert abs(215-1.8-205-8.2)<1e-9
results={'data':'2026-10-12','status':'direção funcional aceita; RO-32 proposto condicionalmente, sem liberação de fabricação','output':str(OUT),'pages':6,
 'under_maleiro':213.2,'under_aerial':205,'step':8.2,'nominal_gap':3,'aerial_length_base':222,'aerial_length_with_1cm_rear':221,
 'swing':{'angle_range':[0,90],'samples':len(samples),'minimum_y':round(min_y,3),'wardrobe_front_y':60,'centerline_gap_min':round(min_y-60,3),'analytical_bound':'y = hinge - t*cos(theta), 0<=theta<=90 e 0<=t<=55.2. Toda folha permanece no próprio intervalo longitudinal.','conservative_gap_after_1_8cm_allowance':round(min_y-60-1.8,3),'not_included':['ferragens','puxadores','empenamento','instalação real','pessoa','conteúdo']},
 'sliding_opening_example':{'opening':(196.4-2.5)/2,'left_direct_approach':1.8+(196.4-2.5)/2-25,'overlap_assumed':2.5,'door_width_before_final_gaps':(196.4+2.5)/2,'hardware_reference':'RO-32 embutido, condicional','hardware_validated':False},
 'hardware':{'manufacturer':'Rometal','system':'RO-32','installation':'embutido na face interna das folhas','upper_profile':'RM-030','lower_profile':'RM-022','guide':'compatível com canal 26 mm; código final a confirmar','kits_one_door':2,'rollers':4,'guides':4,'brakes':4,'upper_runs':2,'lower_runs':2,'run_length_study_cm':196.4,'front_reserve_study_cm':7,'soft_close_included':False,'door_height_deduction_manual_mm':32,'door_height_deduction_web_mm':25,'application_low_wide_confirmed':False,'density_hypothesis_kg_m3':800,'accessories_allowance_kg':0.6,'example_total_leaf_mass_kg':round(.9945*.24*.018*800+.6,3)},
 'height_scenarios':[{'ceiling':h,'trim':3,'body_top':h-3,'maleiro_clear':round(h-3-1.8-215,1),'aerial_clear':round(h-3-205-3.6,1)} for h in [240,247,257]],
 'preserved':['largura200','profundidade60 de referência','varão205','superfície maleiro215','quatro gavetas','divisão igual','aéreo raso25'],
 'limits':'Geometria nominal. Sistema de correr precisa caber na altura/profundidade, acessibilidade do canto e estrutura ainda não demonstradas fisicamente.'}
(HERE/'Encontro_L_resultados_2026-10-12.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(results,ensure_ascii=False))
