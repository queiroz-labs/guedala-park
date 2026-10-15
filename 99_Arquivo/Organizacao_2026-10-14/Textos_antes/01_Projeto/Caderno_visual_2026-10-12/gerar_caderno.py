from pathlib import Path
import json, re
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'output/pdf/Caderno_visual_Guedala_Park_2026-10-12.pdf'
OUT.parent.mkdir(parents=True,exist_ok=True)
for name,file in [('Reg','arial.ttf'),('Bold','arialbd.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(Path('C:/Windows/Fonts')/file)))
W,H=842,595
INK='#243D40'; MUTED='#637071'; PAPER='#FAF8F3'; WOOD='#CAB08D'; PALE='#E9E1D5'; BLUE='#355C63'; GREEN='#89947C'; LINE='#CACCC5'
c=canvas.Canvas(str(OUT),pagesize=(W,H))
c.setTitle('Guedala Park | Caderno visual de estudo | 12/10/2026')
c.setAuthor('Projeto Guedala Park')
page=0
def rect(x,y,w,h,fill=PALE,stroke=None):
    c.setFillColor(HexColor(fill)); c.setStrokeColor(HexColor(stroke or fill)); c.setLineWidth(.6)
    c.rect(x,H-y-h,w,h,fill=1,stroke=bool(stroke))
def line(x,y,x2,y2,color=LINE,width=.7,dash=None):
    c.setStrokeColor(HexColor(color));c.setLineWidth(width);c.setDash(dash or [])
    c.line(x,H-y,x2,H-y2);c.setDash([])
def text(s,x,y,size=10,font='Reg',color=INK):
    c.setFont(font,size);c.setFillColor(HexColor(color));c.drawString(x,H-y-size,s)
def para(s,x,y,w,size=10,color=INK,font='Reg'):
    st=ParagraphStyle('p',fontName=font,fontSize=size,leading=size*1.4,textColor=HexColor(color),spaceAfter=0)
    p=Paragraph(s,st); aw,ah=p.wrap(w,500)
    assert y+ah<=552,(page,s,y,ah)
    p.drawOn(c,x,H-y-ah);return y+ah
def start(kicker,title,sub):
    global page
    if page:c.showPage()
    page+=1
    rect(0,0,W,H,PAPER);text('GUEDALA PARK',30,20,10,'Bold');text(kicker.upper(),590,20,9,color=MUTED)
    text(title,30,49,25,'Bold');text(sub,30,83,10,color=MUTED)
    line(30,107,812,107)
    line(30,559,812,559);text('12 OUT 2026  |  COTAS EM CM  |  ESTUDO - SEM LIBERAÇÃO PARA FABRICAÇÃO',30,570,8,color=MUTED)
    text(f'{page:02d}',790,568,11,'Bold')
def source(s):text(s,30,542,7.5,color=MUTED)
def note(title,body,y=130,x=580,w=230):
    text(title,x,y,11,'Bold');return para(body,x,y+22,w,10)+22
def pic(path,x,y,w,h):
    p=ROOT/path; im=Image.open(p); iw,ih=im.size;s=min(w/iw,h/ih)
    rw,rh=iw*s,ih*s;c.drawImage(ImageReader(im),x+(w-rw)/2,H-y-rh,rw,rh,mask='auto')
    return rh
def dim(x1,y1,x2,y2,label):
    line(x1,y1,x2,y2,MUTED)
    if abs(y1-y2)<1:
        line(x1,y1-4,x1,y1+4,MUTED);line(x2,y2-4,x2,y2+4,MUTED)
        sw=pdfmetrics.stringWidth(label,'Reg',9);rect((x1+x2-sw)/2-4,y1-16,sw+8,14,PAPER);text(label,(x1+x2-sw)/2,y1-15,9)
    else:
        line(x1-4,y1,x1+4,y1,MUTED);line(x2-4,y2,x2+4,y2,MUTED)
        text(label,x1+6,(y1+y2)/2-6,9)
def block(label,value,y):
    text(label,580,y,9,color=MUTED);return para(value,580,y+16,230,12,font='Bold')+20

start('Caderno visual de estudo','O apartamento, reunido','Decisões locais até 09/10/2026 | Consolidação em 12/10/2026')
pic('03_Referencias/Sala_referencia_aprovada_R03.png',30,126,520,351)
y=note('Onde estamos','Visual e uso dos ambientes bem definidos. Desenhos e verificações dimensionais em desenvolvimento.')
y=note('O que este caderno entrega','Planta esquemática, referências aprovadas, desenhos por ambiente, medidas de estudo e próximas conferências.',y)
y=note('O que falta para executar','Medição acabada, compatibilização das instalações, estrutura e ferragens, produtos finais e orçamento completo.',y)
para('Referência visual da sala R03 aprovada. As proporções, ferragens e detalhes da imagem não definem cotas de obra.',30,492,520,10,color=MUTED)
source('Base: registros locais, auditoria de 06/10 e continuidade da cozinha/banco em 08-09/10. Fontes organizadas na página 12.')

start('01 / Implantação','Planta geral de estudo','Reconstrução do modelo local R09; mobiliário simplificado e sem escala de impressão contratual.')
app=(ROOT/'01_Projeto/Estudo_interativo/src/app.js').read_text(encoding='utf-8')
# Reuse the documented model geometry rather than the obsolete R01 furnished plan.
floors=json.loads(re.search(r'const floors=(\[.*?\]);',app).group(1).replace("'",'"'))
walls=json.loads(re.search(r'const walls=(\[.*?\]);',app).group(1).replace("'",'"'))
s=.55;ox=75;oy=135
def planbox(x,z,w,d,color,label=None):
    rect(ox+x*s,oy+z*s,w*s,d*s,color,LINE)
    if label:text(label,ox+x*s+4,oy+z*s+4,8,'Bold')
for r,x,z,w,d,m in floors:planbox(x,z,w,d,'#F0ECE4' if m=='vinyl' else '#E1E4DA')
for a in walls:planbox(*a[1:5],INK)
for a in [(5,120,200,160,PALE,'Queen'),(0,335,200,60,WOOD,'Armário'),(270,0,200,70,WOOD,'Bancada'),(257,82,90,140,PALE,'Daiane'),(630,185,110,180,PALE,'Bonnie'),(685,375,55,180,WOOD,'Banco'),(615,390,75,150,WOOD,'Mesa'),(388,637,186.9,63,WOOD,None),(584.9,615.25,60.1,74.75,'#B8C2C2','IB6S'),(255,625,59,75,WOOD,'Tanque'),(320,628,60,62,'#B8C2C2','LG'),(255,405,80,124,GREEN,'Box'),(405,484,60,45,WOOD,None)]:planbox(*a)
for x,z,w,d in [(60,90,120,10),(315,-10,115,10),(533,175,139,10),(245,569,10,106),(245,435,10,40)]:planbox(x,z,w,d,'#ACC8CA')
for z in [396,446,496]:planbox(580,z,35,44,PALE)
text('Escritório',275,180,10,'Bold');text('Quarto',110,303,10,'Bold');text('Sala / jantar',354,343,10,'Bold')
dim(ox+388*s,oy+710*s,ox+740*s,oy+710*s,'cozinha 352')
y=note('Programa atual','Sala/jantar integrados; cozinha linear; lavanderia; quarto queen; escritório com hóspedes; banheiro.')
y=note('Cotas documentais','Cozinha: 352 × 155.<br/>Banheiro: 209 × 124.<br/>São cotas de planta, a conferir acabadas.',y)
y=note('Representação','Mesa recolhida em 150; banco 180 × 55; três cadeiras na lateral. Aéreos omitidos para ler o piso.',y)
y=note('Limites da planta','Portas, percursos e objetos pequenos não são verificados nesta síntese. A lavanderia tem divergência entre a cota documental e o modelo gráfico.',y)
source('Geometria: Estudo interativo R09, app.js. Cotas documentais: base de medidas e conferência do banheiro.')

start('02 / Cozinha','Uma frente contínua','Azul Petróleo nos superiores, Arenza nos inferiores e Branco Itaúnas na bancada.')
sx=43; sy=477; k=1.78
def elev(x,z,w,h,col,label=None):
    rect(sx+x*k,sy-(z+h)*1.18,w*k,h*1.18,col,LINE)
    if label:text(label,sx+x*k+5,sy-(z+h)*1.18+7,9,'Bold',PAPER if col==BLUE else INK)
# Left to right on the elevation: cooking, sink, prep, refrigerator.
elev(0,5,60,61,'#5C6767','Forno');elev(60,18,65,72,WOOD,'Pia');elev(125,18,61.9,72,WOOD)
for z in [58,74]:line(sx+125*k,sy-z*1.18,sx+186.9*k,sy-z*1.18,INK)
for label,z in [('G1 / 16',82),('G2 / 16',66),('G3 / 40',36)]:text(label,sx+130*k,sy-z*1.18,9)
elev(0,90,186.9,2,'#D6D0C3');elev(196.9,0,60.1,186.6,'#B9C3C3','IB6S')
elev(-2.5,197.6,65,57.4,BLUE,'D');elev(62.5,155,54.7,100,BLUE,'C');elev(117.2,194,69.7,61,BLUE,'B');elev(186.9,198.4,80.1,56.6,BLUE,'A')
elev(128.5,155,46.1,29,'#667172','Micro');elev(0,174,60,17.6,'#BBC3C0','Depurador')
for a,b,label in [(0,60,'60'),(60,125,'65'),(125,186.9,'61,9'),(186.9,267,'80,1')]:dim(sx+a*k,502,sx+b*k,502,label)
text('Elevação esquemática | medidas nominais dos módulos',43,133,10,color=MUTED)
y=block('Bancada de estudo','92 A × 63 P',130)
y=note('Passagem nominal','155 - 63 = 92 cm. Projeções de aparelhos e circulação em uso precisam de conferência.',y)
y=note('Organização adotada','G1 talheres; G2 utensílios; G3 mantimentos/bebidas. C1 mantém duas pilhas de pratos; sanduicheira prevista em C2.',y)
y=note('Conferências que faltam','Corte forno/cooktop; ventilação do micro; torre de tomadas; hidráulica da pia; ferragens e objetos reais.',y)
source('Base: R09; fechamento cozinha/lavanderia 27/09; compatibilizações 28/09 a 09/10. Alturas superiores são estudo.')

start('03 / Lavanderia','Lavar, secar e guardar','Tanque esculpido e lava e seca sob a pedra; cesto basculante com saco removível.')
# Front schematic; no invented installation location for heater.
sx=90;sy=420;k=2.85
rect(sx,sy-92*2,133*k,4,'#D6D0C3');rect(sx,sy-90*2,59*k,72*2,WOOD,LINE)
rect(sx+65*k,sy-85*2,60*k,85*2,'#B8C2C2',INK)
c.setStrokeColor(HexColor(INK));c.setLineWidth(1);c.circle(sx+95*k,H-(sy-44*2),42,stroke=1,fill=0)
rect(sx+8*k,sy-92*2,38*k,11,PAPER,INK);text('Tanque',sx+12*k,sy-75*2,11,'Bold')
text('Cesto',sx+14*k,sy-43*2,11,'Bold');text('LG VC4',sx+80*k,sy-75*2,11,'Bold')
dim(sx,452,sx+133*k,452,'133 no modelo - conferir com a parede acabada')
text('Vista frontal simplificada',90,137,11,color=MUTED)
rect(88,171,150,14,WOOD);text('Varal 100 × 50: desenho de uso separado',88,194,10)
y=block('Tanque / volume interno','38 × 35 × 20',130)
y=block('Cesto / gabarito','45 × 25 × 45 | giro 55°',y)
y=note('Uso já definido','Retirar saco com máquina fechada; fechar cesto antes de abrir a LG. Varal vazio oculto; alto para secar; baixo para carregar.',y)
y=note('Ainda em desenvolvimento','Varal/fixação/carga, banquinho, hidráulica do tanque e mecanismo do cesto. Aquecedor E21 com implantação técnica pendente.',y)
para('Pedra de estudo: 75 cm de profundidade. A frente do cesto a 63 cm é proposta técnica. A cota transversal oficial de 154 cm e os 161 cm do modelo exigem reconciliação antes de fechar a circulação.',30,485,515,10)
source('Base: Tanque/cesto R08; Cesto retirada e Operação lavanderia 30/09; relatório de lavanderia 06/10; R09.')

start('04 / Sala e jantar','A referência visual já está escolhida','Composição R03 aprovada; medidas e construção organizadas separadamente da imagem.')
pic('03_Referencias/Sala_referencia_aprovada_R03.png',30,128,520,343)
y=block('Sofá Bonnie','180 L | 110 P fechado / 136 aberto',128)
y=block('Mesa extensível','150 / 180 × 75 | cantos R15',y)
y=block('Banco','180 × 55 externo | assento a 47',y)
y=note('Disposição atual','Três cadeiras na lateral livre; sem cadeira na cabeceira. Folha removível de 30 × 75 guardada no banco.',y)
y=note('Painel e TV','TV de 50″; painel ~115. Uma prateleira acima e outra abaixo da TV. Fixação, alturas e modelo da TV a fechar.',y)
para('Base da mesa, guias, folha e apoio precisam de detalhamento. A imagem é referência de aparência; não valida estabilidade ou circulação.',30,490,520,10,color=MUTED)
source('Base: Sala R03; Mesa completa 30/09; Painel sob medida R01; modelo R09 e revisão de ambientes 06/10.')

start('05 / Banco e armazenamento','A organização foi aprovada','Aceite funcional em 08/10; retirada das almofadas aceita em 09/10. Estrutura ainda em estudo.')
pic('01_Projeto/Compatibilizacao_2026-10-08/Detalhe_acesso_balde.png',30,127,520,345)
y=note('Banco preservado','180 × 55 externos; profundidade do assento 45; topo a 47. Folha da mesa preservada.')
y=note('Guarda prevista','Potes, travessas e batedeira; liquidificador, jarra e térmica; balde de 8 L; aspirador e poucos jogos nos vãos reservados.',y)
y=note('Solução em desenvolvimento','Tampas de 2 cm com almofadas separadas: abertura de estudo de 37,8 cm no corte. Retirar almofada também para acessar a térmica.',y)
y=note('O que falta comprovar','Carga e resistência; dobradiças e retenção; balde com alça; objetos completos; manuseio junto à mesa e ao encosto.',y)
para('Fruteira com base ventilada sobre a mesa: direção escolhida para as poucas batatas, cebolas e alho. Dimensões e produto ainda em estudo.',30,492,520,10)
source('Base: Cozinha e banco 08/10 e Detalhe banco/conteúdo, com continuidade aceita em 09/10.')

start('06 / Quarto','Madeira, cabeceira e armários em L','Referência visual R03 aprovada; quarto sem TV e sem cortina externa.')
pic('03_Referencias/Quarto_referencia_aprovada_R03.png',30,128,520,348)
y=block('Guarda-roupa / envelope','200 L × 60 P | até o teto',128)
y=note('Interior aprovado','Divisão igual, quatro gavetas, dez pares de tênis até 42, dois casacos longos e prioridade para cabides.',y)
y=block('Aéreo / profundidade de estudo','25 cm',y)
y=note('Encontro dos armários','Base do maleiro a 215 e base do aéreo da cabeceira a 205 são referências diferentes. O encontro em L precisa preservar ambos os usos.',y)
y=note('Conferência principal','Altura do piso acabado ao teto, cama/base reais, trilhos e abertura de gavetas. A antiga altura fixa de 240 foi superada.',y)
para('Espelho lateral: 50 × 180 cm, prata 5 mm, sem moldura. Dois apoios pequenos e arandelas brancas independentes compõem a cabeceira.',30,491,520,10)
source('Base: Quarto R03; Guarda-roupa interior R02; Aéreos contínuos 25/09; auditoria de ambientes 06/10.')

start('07 / Escritório','Trabalho no dia a dia, hóspedes quando preciso','Bancada de frente para a janela; sofá-cama na lateral; cadeira permanece no ambiente.')
ox=85;oy=147;s=1.05
rect(ox,oy,230*s,295*s,'#EEEAE2',INK)
rect(ox+15*s,oy,200*s,70*s,WOOD,INK);text('Bancada',ox+22,oy+18,11,'Bold')
rect(ox+2*s,oy+82*s,90*s,140*s,PALE,INK);text('Daiane',ox+10,oy+137*s,10,'Bold')
rect(ox+112*s,oy+80*s,74.5*s,73*s,'#BEC5C2',INK);text('Cadeira',ox+120*s,oy+100*s,9)
rect(ox+218*s,oy+128*s,5*s,97*s,INK)
line(ox+230*s,oy+220*s,ox+155*s,oy+220*s,INK,1,[3,3])
text('Porta: giro a conferir',ox+110*s,oy+267*s,9)
dim(ox,oy+313*s,ox+230*s,oy+313*s,'230 no modelo')
dim(ox+245*s,oy,ox+245*s,oy+295*s,'295')
text('Planta de estudo | modo trabalho',85,126,10,color=MUTED)
y=block('Bancada','70 P | 200 L × 75 A no ensaio',128)
y=block('Aéreo sobre o sofá','200 L × 55 A × 35 P',y)
y=note('Equipamentos e guarda','Notebook à esquerda, dois monitores, gabinete à direita; duas gavetas à esquerda. TV Samsung 43″ existente; console pode circular entre sala e escritório.',y)
y=note('Modo hóspedes pendente','Testar sofá aberto, porta, cadeira e gavetas juntos. O antigo módulo para a caixa do PC foi excluído; volante e caixa ainda sem guarda comprovada.',y)
para('Prateleira dos consoles com topo a 195 cm. Aéreos off-white, bancada e prateleiras Arenza. Dimensões dos equipamentos e ferragens ainda condicionam o desenho.',30,503,515,10)
source('Base: escritório vigente, R09/R10, auditoria de ambientes 06/10 e implantação do modelo R09.')

start('08 / Banheiro','Uma parede verde, bancada clara e metais pretos','Celite VIP; Deca Slim como primeira opção; Arion centralizada atrás da cuba; chuveiro Livo.')
pic('03_Referencias/Banheiro_referencia_aprovada_2026-09-18.png',30,128,300,362)
# Top view of countertop, separate from aesthetic image.
bx=362;by=169;sc=2.6
rect(bx,by,60*sc,45*sc,'#DED6C8',INK)
rect(bx+10*sc,by+10*sc,40*sc,30*sc,PAPER,INK)
c.setFillColor(HexColor(INK));c.circle(bx+30*sc,H-(by+5*sc),3,fill=1,stroke=0)
text('Cuba',bx+21*sc,by+21*sc,10,'Bold');dim(bx,by+45*sc+23,bx+60*sc,by+45*sc+23,'60')
text('Bancada em planta',350,131,10,'Bold')
para('45 P = 10 atrás + cuba 30 + borda 5.<br/>As faixas são hipóteses; não validam furação ou movimento da alavanca.',350,327,190,10)
y=block('Bancada / hipótese','60 × 45',128)
y=block('Alturas de teste','Borda da cuba 90 | tampo 76,5',y)
y=note('Definido visualmente','Só a parede de fundo do chuveiro verde. Gabinete suspenso fechado; espelheira rasa com luz frontal para maquiagem.',y)
y=note('Conferências principais','Giro da porta, alcance/alavanca da Arion, pontos e percurso de água quente, box e espelheira. Medidas finais dependem da vistoria.',y)
para('Imagem de referência, sem validação de encaixe. Espelheira com 12-15 cm externos é estudo; posição das portas e iluminação ainda a detalhar.',30,507,510,9,color=MUTED)
source('Base: decisões do banheiro 18/09; Conferência bancada/porta; auditoria de ambientes 06/10.')

start('09 / Materiais','Uma paleta coerente entre os ambientes','Cores digitais aproximadas: comparar amostras físicas antes de especificar e comprar.')
materials=[('Arenza',WOOD,'Cozinha baixa, lavanderia, quarto e detalhes.'),('Azul Petróleo',BLUE,'Armários superiores da cozinha.'),('Branco Itaúnas','#DED7C7','Bancadas e detalhes de pedra.'),('Algodão Egípcio','#E6DFD1','Direção de pintura; linha e lata a identificar.'),('Off-white fosco','#EEEAE1','Sala e aéreos do escritório.'),('Verde sálvia',GREEN,'Parede focal do chuveiro.'),('Olmo','#C9B99D','Preferência de piso vinílico; amostra a conferir.'),('Preto / grafite','#333D3E','Metais, bases e detalhes.')]
for i,(name,col,desc) in enumerate(materials):
    x=30+(i%2)*266;y=132+(i//2)*92
    rect(x,y,52,58,col,LINE);text(name,x+66,y,11,'Bold');para(desc,x+66,y+20,173,9)
y=note('Pisos','Intenção de LVT colado em sala, circulação, quarto, escritório e cozinha. Banheiro e lavanderia com revestimentos próprios.')
y=note('Base e níveis','Retirada do laminado de entrega, condição do contrapiso, acústica, transições e portas precisam integrar o detalhamento.',y)
y=note('Acabamentos inox','Geladeira IB6S e LG VC4 CV5012PC4 Inox Look, 127 V, conforme atualização vigente. Comparar tonalidades reais entre marcas.',y)
y=note('Iluminação','Cozinha/lavanderia 3000 K; três comandos definidos. Sala/escritório mantêm requisitos próprios de luz inteligente.',y)
source('Base: materiais do modelo R09; revisão de pisos e armários 25/09; auditorias e fechamento atuais.')

start('10 / Próximas entregas','O caminho para tornar executável','Ordem recomendada de trabalho; não representa prazo contratado ou percentual de conclusão.')
rows=[('1','Consolidar o conjunto','Este caderno reúne os ambientes e explicita as cotas de estudo.','ENTREGUE NESTA RODADA'),('2','Compatibilizar os pontos críticos','Forno/cooktop e micro; mesa/banco; cesto/varal; encontro do L; porta do escritório.','PRÓXIMA FRENTE TÉCNICA'),('3','Completar desenhos de detalhamento','Elevações finais, cortes de instalações, ferragens e lista de peças/produtos.','DEPENDÊNCIAS IDENTIFICADAS'),('4','Medir e fechar orçamento','Conferir medidas acabadas; revisar os desenhos; cotar marcenaria, pedra, instalações e acabamentos.','MEDIÇÃO E COTAÇÕES PENDENTES')]
for i,(n,title,body,status) in enumerate(rows):
    y=135+i*96
    text(n,32,y,26,'Bold',BLUE);text(title,75,y,14,'Bold');para(body,75,y+25,475,10);text(status,580,y+9,9,'Bold',MUTED)
source('O apartamento permanece sem levantamento acabado registrado. Não há orçamento global fechado nos arquivos revisados.')

start('11 / Rastreabilidade','Fontes e critérios desta consolidação','Arquivos preservados na pasta do projeto. Referências web e preços não foram atualizados nesta rodada.')
sources=[
('Base geral','README do projeto; Resumo; Registro de decisões; Auditoria ambientes 06/10.'),
('Planta','Estudo_interativo/src/app.js e data.js (R09); Medidas/Dados_das_medidas_R00.json; Planta_oficial.pdf.'),
('Cozinha','Fechamento cozinha/lavanderia 27/09; compatibilizações 28/09 a 09/10; Cozinha e banco 08/10.'),
('Lavanderia','Tanque/cesto R08; Cesto retirada e Operação lavanderia 30/09; Relatório lavanderia 06/10.'),
('Sala / banco','Sala referência aprovada R03; Mesa completa 30/09; Painel sob medida R01; Detalhe banco/conteúdo 08-09/10.'),
('Quarto','Quarto referência aprovada R03; Guarda-roupa interior R02; Aéreos contínuos 25/09; Auditoria ambientes 06/10.'),
('Escritório','Estudos R09/R10; Auditoria ambientes 06/10; geometria de trabalho do modelo R09.'),
('Banheiro / pisos','Decisões banheiro 18/09; Conferência bancada/porta; Auditoria ambientes 06/10; revisão de pisos 25/09.')]
for i,(label,body) in enumerate(sources):
    y=130+i*47;text(label,30,y,10,'Bold');para(body,149,y,403,9)
y=note('Precedência usada','Decisões explícitas posteriores prevalecem sobre trechos históricos. A atualização do banco em 09/10 supera o ensaio inicial de abertura.')
y=note('Desenhos novos','Planta geral, elevação da cozinha, frente da lavanderia, planta do escritório e bancada do banheiro são sínteses gráficas deste caderno.',y)
y=note('Verificação desta entrega','Conferência de conteúdo, páginas renderizadas e legibilidade. Esta revisão não equivale a validação física das soluções.',y)
y=note('Próxima revisão','Incorporar as medidas acabadas e os detalhes técnicos aprovados; manter um único caderno atualizado.',y)
source('Caderno visual de estudo | R00 | 12/10/2026. Imagens anteriores reaproveitadas como referência, sem novas gerações.')
c.save()
print(json.dumps({'output':str(OUT),'pages':page},ensure_ascii=False))
