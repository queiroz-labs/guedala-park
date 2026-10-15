"""Build a native, editable FreeCAD apartment from the project's documented studies.

Run inside FreeCAD (macro or execute_python). All native dimensions are millimetres.
No custom feature proxies are required to reopen the FCStd file.
"""
from pathlib import Path
import csv
import json
import math
import traceback
import FreeCAD as App
import FreeCADGui as Gui
import Part

HERE = (Path(__file__).resolve().parent / '..').resolve()
OUT = (Path(__file__).resolve().parent / '../03_Recursos/output').resolve()
OUT.mkdir(exist_ok=True)
BASE = json.loads(((Path(__file__).resolve().parent / 'Base_interativa.json').resolve()).read_text(encoding='utf-8'))
DOC = App.newDocument('Guedala_Park_R01')
DOC.Label = 'Guedala Park · apartamento e armários · estudo R01'
COLORS = {m['id']: m['color'] for m in BASE['project']['materials']}
ROWS, MODULES, FRONTS, ARCH, RESERVES = [], [], [], [], []
DIM_REFS = {}
ROOM_NAMES = {'quarto':'Quarto', 'escritorio':'Escritório', 'sala':'Sala e jantar',
              'cozinha':'Cozinha', 'lavanderia':'Lavanderia', 'banho':'Banheiro', 'circulacao':'Circulação'}
ROOMS = {}

def rgb(material):
    h = COLORS.get(material, material)
    if not h.startswith('#'):
        h = '#b8b6ad'
    return tuple(int(h[i:i+2],16)/255 for i in (1,3,5))

def prop(obj, typ, name, value, group='Projeto'):
    obj.addProperty(typ, name, group)
    setattr(obj, name, value)

def group(name, label, parent=None, part=False):
    o = DOC.addObject('App::Part' if part else 'App::DocumentObjectGroup', name)
    o.Label = label
    if parent:
        parent.addObject(o)
    return o

META = group('Documentacao', '00 · Dados, hipóteses e fontes')
prop(META,'App::PropertyString','Revisao','R01 · 13/10/2026')
prop(META,'App::PropertyString','Escopo','Apartamento inteiro e marcenaria; modelo de estudo, sem liberação de fabricação.')
prop(META,'App::PropertyString','Cinematica','Movimentos por eixos ideais. Ferragens reais, cargas, puxadores e tolerâncias pendentes.')
prop(META,'App::PropertyString','Origem','X = x da base; Y = z da base; Z = y vertical. cm convertidos em mm.')
prop(META,'App::PropertyStringList','Fontes',[
    '../Estudo_interativo/src/app.js e data.js · implantação R09',
    '../Portas_e_quarto/Guarda_roupa_interior_R02.md · organização + decisões 12/10',
    '../Portas_e_quarto/Canto_independente_R01_2026-10-12.json · canto em estudo',
    '../Portas_e_quarto/Conferencia_giro_canto_R02.json · conflitos ainda pendentes',
    '../Cozinha/Aereos_R00.md e Interior_gavetas_2026-09-25.md',
    '../Compatibilizacao_2026-10-08/Cozinha_e_banco.html · banco',
    '../Painel_de_decisoes.md · pendências técnicas vigentes'])
PARAM = DOC.addObject('Spreadsheet::Sheet','Parametros')
META.addObject(PARAM)
PARAM.Label = 'Parâmetros gerais · mm · hipóteses explícitas'
for i,(label,value,alias) in enumerate([
    ('Chapa de estudo',18,'Chapa'),('Fundo de estudo',18,'Fundo'),
    ('Junta nominal das frentes',2,'Junta'),('Teto quarto/escritório: cenário',2470,'TetoQuarto'),
    ('Laje cozinha: hipótese do usuário',2570,'TetoCozinha'),
    ('Proteção posterior mínima do quarto',10,'Protecao'),
    ('Profundidade total roupeiro aceita',650,'ProfRoupeiro'),
    ('Altura face inferior dos aéreos do quarto',2132,'BaseAereo'),
    ('Topo corpo quarto: cenário',2440,'TopoQuarto'),
    ('Curso nominal gavetas escritório aceito',400,'CursoEscritorio')],2):
    PARAM.set('A'+str(i),label)
    PARAM.set('B'+str(i),str(value)+' mm')
    PARAM.setAlias('B'+str(i),alias)
PARAM.setColumnWidth('A',360)
PARAM.setColumnWidth('B',130)
for rid,label in ROOM_NAMES.items():
    ROOMS[rid] = group('Ambiente_'+rid, label)

def box(parent,label,x,y,z,w,d,h,material='wood',role='Painel',expr=None):
    if min(w,d,h) <= 0:
        raise ValueError('Dimensão inválida: '+label)
    o = DOC.addObject('Part::Box','Peca')
    o.Label = label
    o.Length,o.Width,o.Height = w,d,h
    o.Placement.Base = App.Vector(x,y,z)
    parent.addObject(o)
    prop(o,'App::PropertyString','TipoPeca',role)
    prop(o,'App::PropertyString','MaterialReferencia',material)
    prop(o,'App::PropertyString','Status','Estudo dimensional; conferir antes de fabricar')
    o.ViewObject.ShapeColor = rgb(material)
    o.ViewObject.LineColor = (0.25,0.27,0.24)
    for key,value in (expr or {}).items():
        for source,target in DIM_REFS.items():
            value=value.replace(source+'.',target+'.')
        o.setExpression(key,value)
    ROWS.append(o)
    if role in ('Porta','Frente','Tampa','Almofada'):
        FRONTS.append(o)
    return o

def module(rid,name,origin,w,d,h,material='wood',angle=0,note='',source=''):
    o = group('Modulo',name,ROOMS[rid],True)
    dims=DOC.addObject('Spreadsheet::Sheet','Dimensoes')
    dims.Label='Dimensões · '+name
    META.addObject(dims)
    prop(o,'App::PropertyLink','PlanilhaDimensoes',dims)
    for row,(key,value) in enumerate([('Comprimento',w*10),('Profundidade',d*10),('Altura',h*10),
                                     ('Chapa',18),('Fundo',18),('Frente',18),('Junta',2)],2):
        dims.set('A'+str(row),key)
        dims.set('B'+str(row),str(value)+' mm')
        dims.setAlias('B'+str(row),key)
        prop(o,'App::PropertyLength',key,value)
        o.setExpression(key,dims.Name+'.'+key)
    dims.set('B5','=Parametros.Chapa')
    dims.set('B6','=Parametros.Fundo')
    dims.set('B8','=Parametros.Junta')
    dims.setColumnWidth('A',180)
    dims.setColumnWidth('B',130)
    DIM_REFS[o.Name]=dims.Name
    prop(o,'App::PropertyString','Ambiente',rid)
    prop(o,'App::PropertyString','Fonte',source)
    prop(o,'App::PropertyString','Condicoes',note or 'Envelope de estudo; material, ferragens, fixação e medidas acabadas pendentes.')
    o.Placement = App.Placement(App.Vector(*(v*10 for v in origin)),App.Rotation(App.Vector(0,0,1),angle))
    MODULES.append(o)
    return o

def panel(m,label,x,y,z,w,d,h,material='wood',role='Painel',expr=None):
    return box(m,label,x,y,z,w,d,h,material,role,expr)

def carcass(m,material='wood',top=True,bottom=True,front=20):
    W,D,H = float(m.Comprimento),float(m.Profundidade),float(m.Altura)
    N=m.Name
    front_expr=str(front)+' mm'
    panel(m,'Lateral esquerda',0,front,0,18,D-front,H,material,expr={
        'Length':N+'.Chapa','Width':N+'.Profundidade - '+front_expr,'Height':N+'.Altura'})
    panel(m,'Lateral direita',W-18,front,0,18,D-front,H,material,expr={
        'Placement.Base.x':N+'.Comprimento - '+N+'.Chapa','Length':N+'.Chapa',
        'Width':N+'.Profundidade - '+front_expr,'Height':N+'.Altura'})
    panel(m,'Fundo',18,D-18,18,W-36,18,H-36,material,expr={
        'Placement.Base.x':N+'.Chapa','Placement.Base.y':N+'.Profundidade - '+N+'.Fundo',
        'Placement.Base.z':N+'.Chapa','Length':N+'.Comprimento - 2 * '+N+'.Chapa',
        'Width':N+'.Fundo','Height':N+'.Altura - 2 * '+N+'.Chapa'})
    if bottom:
        panel(m,'Base',18,front,0,W-36,D-front-18,18,material,expr={
            'Placement.Base.x':N+'.Chapa','Length':N+'.Comprimento - 2 * '+N+'.Chapa',
            'Width':N+'.Profundidade - '+front_expr+' - '+N+'.Fundo','Height':N+'.Chapa'})
    if top:
        panel(m,'Tampo',18,front,H-18,W-36,D-front-18,18,material,expr={
            'Placement.Base.x':N+'.Chapa','Placement.Base.z':N+'.Altura - '+N+'.Chapa',
            'Length':N+'.Comprimento - 2 * '+N+'.Chapa',
            'Width':N+'.Profundidade - '+front_expr+' - '+N+'.Fundo','Height':N+'.Chapa'})

def shelf(m,height,label='Prateleira',x=18,w=None,depth=None,front=20):
    N=m.Name; W,D=float(m.Comprimento),float(m.Profundidade)
    return panel(m,label,x,front,height,w or W-36,depth or D-front-18,18,'offwhite',expr={
        'Length':N+'.Comprimento - 2 * '+N+'.Chapa'} if w is None else None)

def divider(m,x,z=18,h=None,depth=None,front=20):
    D,H=float(m.Profundidade),float(m.Altura)
    return panel(m,'Divisória',x,front,z,18,depth or D-front-18,h or H-36,'offwhite')

def doors(m,count=2,material='wood'):
    W,H=float(m.Comprimento),float(m.Altura)
    for i in range(count):
        p=group('Folha','Porta '+str(i+1),m,True)
        prop(p,'App::PropertyAngle','Abertura',0)
        prop(p,'App::PropertyString','Movimento','Eixo ideal; dobradiça real e colisões não validadas')
        p.Placement.Base=App.Vector(W*i/count+1,0,1)
        p.setExpression('Placement.Base.x',m.PlanilhaDimensoes.Name+'.Comprimento * '+str(i)+' / '+str(count)+' + 1 mm')
        p.setExpression('Placement.Rotation.Angle','Abertura' if count==2 and i==1 else '-Abertura')
        panel(p,'Frente '+str(i+1),0,0,0,W/count-2,18,H-2,material,'Porta',{
            'Length':m.Name+'.Comprimento / '+str(count)+' - '+m.Name+'.Junta',
            'Height':m.Name+'.Altura - '+m.Name+'.Junta'})
        if count==2 and i==1:
            p.setExpression('Placement.Base.x',m.PlanilhaDimensoes.Name+'.Comprimento - 1 mm')
            p.Group[-1].setExpression('Placement.Base.x','0 mm - Length')

def drawer(m,label,x,z,frontw,fronth,outerw,depth,height,front_material='wood',travel=400,closed_y=0):
    p=group('Gaveta',label,m,True)
    prop(p,'App::PropertyLength','Extensao',0)
    prop(p,'App::PropertyLength','CursoNominal',travel)
    prop(p,'App::PropertyString','Ferragem','Caixa hipotética; folgas, fixação e carga a conferir com a ferragem escolhida')
    p.Placement.Base=App.Vector(x,closed_y,z)
    p.setExpression('Placement.Base.y',str(closed_y)+' mm - Extensao')
    panel(p,'Frente · '+label,0,0,0,frontw,18,fronth,front_material,'Frente')
    dx=(frontw-outerw)/2
    panel(p,'Fundo da caixa',dx,25,20,outerw,depth,15,'offwhite','Caixa de gaveta')
    for px in [dx,dx+outerw-15]:
        panel(p,'Lateral da caixa',px,25,35,15,depth,height-15,'offwhite','Caixa de gaveta')
    for py in [25,25+depth-15]:
        panel(p,'Travessa da caixa',dx+15,py,35,outerw-30,15,height-15,'offwhite','Caixa de gaveta')
    return p

# Architecture: retain full walls; use separate short walls for inspection.
WALLS=group('ParedesInteiras','Paredes inteiras · alturas de cenário')
CUTWALLS=group('ParedesCortadas','Paredes em corte · inspeção')
ARCH += [WALLS,CUTWALLS]
skip_ids={'wardrobe','bedcabinet','mirror','officecab','drawers','kitchenbase','sinkstorage',
          'kitchenupper','laundrybase','laundrybasket','laundryupper','bathvanity','bathmirror',
          'bench','lowdrawer','microwave'}
item_map={i['id']:i for i in BASE['items']}
for n in BASE['nodes']:
    rid=n['room'] if n['room'] in ROOMS else 'circulacao'
    x,y,z,w,d,h=[n[k]*10 for k in ('x','z','y','w','d','h')]
    if n['kind']=='wall':
        ceiling=2570 if rid in ('cozinha','lavanderia') else 2470
        wall=box(WALLS,'Parede · '+ROOM_NAMES[rid],x,y,z,w,d,ceiling-z,n['c'],'Parede')
        prop(wall,'App::PropertyString','Cota','Trechos reconstruídos graficamente; espessura e altura pendentes de levantamento')
        box(CUTWALLS,'Parede em corte · '+ROOM_NAMES[rid],x,y,0,w,d,320,n['c'],'Parede em corte')
        continue
    if n['id'] in skip_ids:
        continue
    label=item_map.get(n['id'],{}).get('name', n['kind'])
    role='Reserva de equipamento ou móvel' if n['id'] else 'Arquitetura de estudo'
    o=box(ROOMS[rid],label,x,y,z,w,d,h,n['c'],role)
    if n.get('yaw'):
        rot=App.Rotation(App.Vector(0,0,1),math.degrees(n['yaw']))
        pivot=App.Vector(n['rootX']*10,n['rootZ']*10,0)
        o.Placement=App.Placement(pivot+rot.multVec(App.Vector(x,y,z)-pivot),rot)
    elif n.get('rot'):
        center=App.Vector(x+w/2,y+d/2,z)
        rot=App.Rotation(App.Vector(0,0,1),math.degrees(n['rot']))
        o.Placement=App.Placement(center-rot.multVec(App.Vector(w/2,d/2,0)),rot)
    if n['id']:
        prop(o,'App::PropertyString','Fonte','Estudo_interativo/src/app.js · R09; forma simplificada')
        prop(o,'App::PropertyString','MedidaOriginal',item_map.get(n['id'],{}).get('measure','Hipótese'))
        RESERVES.append(o)
    if n['kind']=='glass':
        o.ViewObject.Transparency=65

# Quarto: accepted depth and organisation R02. The upper corner is a study variant.
ward=module('quarto','Guarda-roupa · inferior R02',(1,329,0),200,65,213.2,'offwhite',
    note='65 cm totais aceitos; proteção de 1 cm adicional. Meta >=55 cm livres para roupa. Quatro gavetas e dez pares previstos; ferragem real pendente.',
    source='../Portas_e_quarto/Guarda_roupa_interior_R02.md · 12/10/2026')
ward.PlanilhaDimensoes.set('B3','=Parametros.ProfRoupeiro')
ward.PlanilhaDimensoes.set('B4','=Parametros.BaseAereo')
carcass(ward,'offwhite',top=False,bottom=False,front=82)
prop(ward,'App::PropertyLength','ReservaFrontalDeEstudo',82)
prop(ward,'App::PropertyLength','ProfundidadeLivreGeometrica',550)
shelf(ward,62,'Base · topo 80 mm',front=82)
divider(ward,991,z=80,h=2052,front=82)
for dx in [18,1627]:
    for level in [322,582,782]:
        shelf(ward,level,'Sapateira · três níveis',dx,355,400,front=82)
    for level in [800,950]:
        drawer(ward,'Gaveta de roupa',dx+1,level,353,142,329,500,100,'offwhite',400,closed_y=62)
for dx in [373,723,1259,1609]:
    divider(ward,dx,z=80,h=1002,depth=550,front=82)
for dx in [18,1277]:
    shelf(ward,1082,'Prateleira curta · topo 1100',dx,705,550,front=82)
for dx,level,length in [(18,2050,973),(1009,2050,973),(391,1030,332),(1277,1030,332)]:
    rail=DOC.addObject('Part::Cylinder','Varao'); ward.addObject(rail)
    rail.Label='Varão · '+str(length)+' mm nominal'
    rail.Radius=10;rail.Height=length
    rail.Placement=App.Placement(App.Vector(dx,365,level),App.Rotation(App.Vector(0,0,1),App.Vector(1,0,0)))
    rail.ViewObject.ShapeColor=rgb('black')
    prop(rail,'App::PropertyString','Status','Referência geométrica; suporte, carga e alcance pendentes')
    ROWS.append(rail)
for i in range(2):
    leaf=group('PortaCorrer','Porta de correr inferior '+str(i+1),ward,True)
    prop(leaf,'App::PropertyLength','Deslocamento',0)
    prop(leaf,'App::PropertyString','Ferragem','Dois planos nominais; curso e sobreposição não especificados')
    leaf.Placement.Base=App.Vector(i*985,i*20,80)
    leaf.setExpression('Placement.Base.x',str(i*985)+(' mm + Deslocamento' if i==0 else ' mm - Deslocamento'))
    panel(leaf,'Frente inferior '+str(i+1),0,0,0,1015,18,2050,'offwhite','Porta')
box(ROOMS['quarto'],'Proteção posterior · 10 mm adicionais',10,3940,0,2000,10,2440,'#c6c5b9','Proteção')
box(ROOMS['quarto'],'Proteção lateral · reserva de 10 mm',0,1090,0,10,2860,2440,'#c6c5b9','Proteção').ViewObject.Visibility=False

# Native boolean L plates: no artificial fixed post at the access corner.
corner=module('quarto','Canto integrado em L · R01 em estudo',(1,394,213.2),65,105,30.8,'wood',
    note='Conceito acolhido; cotas do canto e ferragens ainda em estudo. Colisão simultânea R01 conhecida. Faixa fixa 15 cm R02 NÃO adotada.',
    source='../../Portas_e_quarto/Canto_independente_R01_2026-10-12.json')
prop(corner,'App::PropertyLength','Retorno',250)
prop(corner,'App::PropertyLength','BracoPrincipal',650)
for level,label in [(0,'Base em L'),(290,'Tampo em L')]:
    a=panel(corner,'Suporte geométrico principal',0,-630,level,650,630,18,'wood')
    b=panel(corner,'Suporte geométrico retorno',0,-1050,level,230,420,18,'wood')
    fused=DOC.addObject('Part::Fuse','PlacaL');corner.addObject(fused)
    fused.Label=label;fused.Base=a;fused.Tool=b
    fused.ViewObject.ShapeColor=rgb('wood')
    a.ViewObject.Visibility=False;b.ViewObject.Visibility=False
    prop(fused,'App::PropertyString','Status','Forma geométrica em L; divisão construtiva e usinagem pendentes')
    ROWS.append(fused)
panel(corner,'Fundo do braço principal',18,-18,18,632,18,272)
panel(corner,'Fundo do retorno',0,-1050,18,18,1032,272)
for label,px,py,w,d in [('Frente articulada A',250,-650,400,18),('Frente articulada B',232,-1050,18,400)]:
    p=panel(corner,label,px,py,1,w,d,306,'wood','Porta')
    prop(p,'App::PropertyString','Alerta','R01 tem interferência em abertura simultânea. Não validado para fabricação.')

maleiro=module('quarto','Maleiro reto · portas de correr',(66,329,213.2),135,65,30.8,'wood',
    note='135×65 e integração com canto são estudo R01. Ferragem do maleiro continua pendente.',source='../../Portas_e_quarto/Canto_independente_R01_2026-10-12.json')
carcass(maleiro,'wood',front=40)
for i in range(2):
    panel(maleiro,'Frente de correr do maleiro '+str(i+1),i*660,i*20,1,690,18,306,'wood','Porta')
aerial=module('quarto','Aéreo raso da cabeceira · alinhado',(26,109,213.2),180,25,30.8,'wood',90,
    note='Profundidade 25 cm e altura inferior 213,2 preservadas. Quatro folhas de estudo R01; faixa fixa R02 não adotada.',source='../../Portas_e_quarto/Canto_independente_R01_2026-10-12.json')
carcass(aerial,'wood');doors(aerial,4,'wood')
box(ROOMS['quarto'],'Espelho lateral · reserva',2010,3350,200,5,500,1800,'#b9d0d3','Espelho').ViewObject.Transparency=15

# Kitchen bodies and drawers. Three fronts: 40 / 16 / 16 from bottom upwards.
sink=module('cozinha','Gabinete da pia',(448,639,18),65,61,72,source='../../Cozinha/Detalhamento_dimensional_R00.md')
carcass(sink,top=False);shelf(sink,302,'Prateleira de estudo · hidráulica a recortar');doors(sink,2)
base=module('cozinha','Gaveteiro G1 / G2 / G3',(513,639,18),61.9,61,72,source='../../Cozinha/Interior_gavetas_2026-09-25.md')
carcass(base,top=False)
for name,z,fh,bh in [('G3 · mantimentos',1,396,300),('G2 · utensílios',401,156,100),('G1 · talheres',561,156,80)]:
    drawer(base,name,1,z,617,fh,557,500,bh,travel=500)
oven=module('cozinha','Estrutura do módulo de cocção',(388,639,0),60,61,90,
    note='Nicho sem liberação. Divergência Venax e envelope inferior cooktop pendentes.',source='../../Compatibilizacao_2026-09-28/Corte_coccao.md')
panel(oven,'Lateral esquerda do forno',0,20,0,18,590,900)
panel(oven,'Lateral direita do forno',582,20,0,18,590,900)
panel(oven,'Travessa superior de estudo',18,380,660,564,212,30)
box(ROOMS['cozinha'],'Bancada cozinha · reserva de recortes',3880,6370,900,1869,630,20,'stone','Pedra a detalhar')
low=module('cozinha','Gaveta baixa de limpeza',(450.3,647,0),122.3,44.2,14.5,
    note='Vassoura e rodo desmontados; envelope, ferragem e carga pendentes.',source='../../Cozinha/Gaveta_baixa_ampliacao_comprimento_2026-09-27.md')
drawer(low,'Gaveta baixa',0,39,1223,106,1190,442,100,travel=400)

specs=[('D · acima do depurador',385.5,65,195.8,59.2,[],True),
       ('C · uso diário',450.5,54.7,153.2,101.8,[198,408,684],False),
       ('B · acima do micro',505.2,69.7,194,61,[276],False),
       ('A · acima da geladeira',574.9,80.1,196.6,58.4,[],True)]
for name,x,w,height,h,shelves,vertical in specs:
    m=module('cozinha',name,(x,665,height),w,35,h,'petrol',
        note='Organização funcional aprovada; cotas sob hipótese de laje 257 cm. Ferragens, ventilação e alcance pendentes.',source='../../Cozinha/Aereos_R00.md')
    carcass(m,'petrol')
    for level in shelves:
        shelf(m,level)
    if vertical:
        divider(m,(w*10-18)/2,depth=118 if name.startswith('D') else None)
    if name.startswith('D'):
        channel=panel(m,'Reserva canal técnico · sem armazenamento',(w*10-196)/2,154,18,196,178,h*10-36,'#dca864','Reserva técnica')
        channel.ViewObject.Transparency=65
        prop(channel,'App::PropertyString','Condicao','Gabarito 19,6×19,6; caminho do ar e saída 2 cm ainda não validados')
    doors(m,2,'petrol')
micro=module('cozinha','Apoio aberto do micro',(505.2,653,153.2),69.7,47,1.8,
    note='Apoio aberto, sem laterais prolongadas. 10 cm acima escolhidos versus 30 cm do manual: instalação pendente.',source='../../Compatibilizacao_2026-09-28/Micro_C2.md')
panel(micro,'Prateleira de apoio · topo 1550',0,0,0,697,470,18)
box(ROOMS['cozinha'],'Micro-ondas · envelope ME23P de referência',5165,6548,1550,461,452,290,'black','Equipamento · ventilação pendente')

# Laundry: sink, basket, washer opening, upper storage and screen for drying rack.
lau=module('lavanderia','Gabinete tanque e cesto',(255,639,18),59,61,72,
    note='Cesto 45×25×45, giro55° e saco removível. Hidráulica, contrapeso e ferragens pendentes.',source='../../Lavanderia/Tanque_cesto_compatibilizacao_R08.md')
carcass(lau,top=False,bottom=False)
panel(lau,'Frente basculante · estudo',18,0,0,554,18,710,'wood','Frente')
basket=panel(lau,'Reserva do cesto removível',70,40,20,450,250,450,'#c4b9a8','Reserva técnica')
basket.ViewObject.Transparency=70
box(ROOMS['lavanderia'],'Bancada lavanderia · tanque a recortar',2550,6250,900,1330,750,20,'stone','Pedra a detalhar')
box(ROOMS['lavanderia'],'Tanque · vazio útil 38×35×20',2630,6500,700,380,350,200,'#9baaa3','Reserva técnica').ViewObject.Transparency=80
upper=module('lavanderia','Aéreo da lavanderia',(302,665,165),83.5,35,58,
    note='Envelope do estudo interativo; divisão interna não escolhida.',source='../../Lavanderia/README.md')
carcass(upper);doors(upper,2)
box(ROOMS['lavanderia'],'Chapa de vista do varal · estudo',3715,5650,2070,18,500,400,'wood','Chapa de vista')

# Office: native drawers with nominal 400-mm travel and upper cabinet.
office=module('escritorio','Gaveteiro do escritório',(310,70,48),40,45,24,angle=180,
    note='Duas gavetas; corrediças nominais 400 mm aceitas. Curso não garante uso com cama aberta.',source='../../Auditoria_dimensional_2026-10-12/Ajuste_profundidades_dados.json')
carcass(office)
for i in range(2):
    drawer(office,'Gaveta escritório '+str(i+1),1,1+i*120,398,118,338,400,80,travel=400)
officeup=module('escritorio','Aéreo principal do escritório',(290,90,192),200,35,55,'offwhite',90,
    note='200×35×55 aprovados. Cinco frentes ilustrativas; quantidade/divisões a detalhar.',source='../../Escritorio/README.md')
carcass(officeup,'offwhite');doors(officeup,5,'offwhite')

# Bathroom: only envelopes and chosen closed fronts; interior programme undecided.
bath=module('banho','Gabinete do banheiro',(404,487,20),60,42,54.5,'bathbeige',
    note='Envelope de estudo. Quantidade/tipo de portas e gavetas e divisórias não escolhidos.',source='../../Banheiro/Medidas_e_encaixe_2026-09-18.md')
carcass(bath,'lightwood',top=False)
panel(bath,'Frente fechada · divisão pendente',1,0,1,598,18,543,'bathbeige','Frente')
box(ROOMS['banho'],'Bancada banheiro · cuba a recortar',4040,4840,745,600,450,20,'stone','Pedra a detalhar')
mirror=module('banho','Armário espelhado raso',(404,514,115),60,15,75,'lightwood',
    note='Profundidade15 é proposta; divisões e tubulação pendentes.',source='../../Banheiro/Medidas_e_encaixe_2026-09-18.md')
carcass(mirror,'lightwood')
panel(mirror,'Frente toda espelhada · divisão pendente',1,0,1,598,6,748,'#b8cdcf','Frente')

# Bench: separate lids and removable cushions; inside organisation from 08/10.
bench=module('sala','Banco baú · 180×55 externo',(685,555,0),180,45,40,'wood',-90,
    note='Assento45 + encosto10 =55 total. Rotina de almofadas removíveis aceita; estrutura e tampas ainda em estudo.',source='../../Compatibilizacao_2026-10-08/Cozinha_e_banco.html')
carcass(bench,top=False,bottom=False)
shelf(bench,82,'Fundo · topo 100 mm',18,1764,390)
for position in [380,748,964]:
    divider(bench,position,z=100,h=300,depth=390)
for i,(start,width) in enumerate([(0,380),(380,368),(748,216),(964,836)]):
    panel(bench,'Tampa independente '+str(i+1),start+1,0,400,width-2,448,20,'wood','Tampa')
    panel(bench,'Almofada removível '+str(i+1),start+1,0,420,width-2,450,50,'head','Almofada')
box(ROOMS['sala'],'Encosto do banco · reserva',7300,3750,400,100,1800,500,'head','Estofado de estudo')

DOC.recompute()
# Native validity and dimension checks; this is not a hinge or load certification.
invalid=[]
for o in DOC.Objects:
    if hasattr(o,'Shape') and not o.Shape.isNull() and not o.Shape.isValid():
        invalid.append(o.Name)
errors=[{'name':o.Name,'state':list(o.State)} for o in DOC.Objects if 'Invalid' in o.State]
report={
    'revision':'R01 · 2026-10-13','units':'mm','objects':len(DOC.Objects),
    'modules':len(MODULES),'parts':len(ROWS),'invalid_shapes':invalid,'invalid_objects':errors,
    'wardrobe_depth':float(ward.Profundidade),'aerial_underside':2132,
    'nominal_bed_to_wardrobe_cm':49,'kitchen_front_bands_cm':[40,16,16],
    'office_drawer_depth_mm':400,
    'not_validated':['medidas acabadas','dobradiças multilink reais','colisões em todo movimento',
                     'resistência/cargas','fixações','ventilação e hidráulica','lista de corte executiva'],
    'known_issue':'Canto R01 tem interferência simultânea conhecida; faixa fixa R02 permanece proposta não adotada.'}
if invalid or errors:
    raise RuntimeError('Geometria ou expressões inválidas: '+json.dumps(report))
((Path(__file__).resolve().parent / '../03_Recursos/output/Verificacao.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
with ((Path(__file__).resolve().parent / '../03_Recursos/output/Pecas_de_estudo.csv').resolve()).open('w',encoding='utf-8-sig',newline='') as f:
    writer=csv.writer(f,delimiter=';')
    writer.writerow(['Objeto','Descrição','Tipo','Comprimento_mm','Profundidade_mm','Altura_mm','Material','Status'])
    for o in ROWS:
        writer.writerow([o.Name,o.Label,getattr(o,'TipoPeca','Forma'),
            float(o.Length) if hasattr(o,'Length') else '',float(o.Width) if hasattr(o,'Width') else '',
            float(o.Height) if hasattr(o,'Height') else '',getattr(o,'MaterialReferencia',''),
            'ESTUDO — NÃO USAR COMO LISTA DE CORTE'])

def default_visibility():
    for r in ROOMS.values():
        r.ViewObject.Visibility=True
    WALLS.ViewObject.Visibility=False
    CUTWALLS.ViewObject.Visibility=True
    for o in FRONTS:
        o.ViewObject.Visibility=True
    # Hide boolean operands, not their fused L plates.
    for o in corner.Group:
        if o.Label.startswith('Suporte geométrico'):
            o.ViewObject.Visibility=False

Gui.activeDocument().activeView().setAnimationEnabled(False) if hasattr(Gui.activeDocument().activeView(),'setAnimationEnabled') else None
Gui.activeDocument().activeView().viewAxonometric()
Gui.activeDocument().activeView().setDrawStyle('Flat Lines') if hasattr(Gui.activeDocument().activeView(),'setDrawStyle') else None
Gui.activeDocument().activeView().setBackgroundColor(0.96,0.95,0.92) if hasattr(Gui.activeDocument().activeView(),'setBackgroundColor') else None
default_visibility()
Gui.activeDocument().activeView().fitAll()
Gui.updateGui()
Gui.activeDocument().activeView().saveImage(str((Path(__file__).resolve().parent / '../03_Recursos/output/Apartamento_fechado.png').resolve()),1800,1200,'White')
for o in FRONTS:
    o.ViewObject.Visibility=False
Gui.updateGui()
Gui.activeDocument().activeView().saveImage(str((Path(__file__).resolve().parent / '../03_Recursos/output/Apartamento_interiores.png').resolve()),1800,1200,'White')
for rid in ['quarto','cozinha','escritorio','lavanderia','banho','sala']:
    CUTWALLS.ViewObject.Visibility=False
    for key,r in ROOMS.items():
        r.ViewObject.Visibility=(key==rid)
    Gui.activeDocument().activeView().viewAxonometric()
    Gui.activeDocument().activeView().fitAll()
    Gui.updateGui()
    Gui.activeDocument().activeView().saveImage(str(OUT/(rid+'_interior.png')),1600,1100,'White')
default_visibility()
Gui.activeDocument().activeView().viewAxonometric()
Gui.activeDocument().activeView().fitAll()
Gui.updateGui()
DOC.recompute()
DOC.saveAs(str((Path(__file__).resolve().parent / '../03_Recursos/output/Guedala_Park_R01.FCStd').resolve()))
result=json.dumps(report,ensure_ascii=False)
App.Console.PrintMessage(result+'\n')
((Path(__file__).resolve().parent / '../03_Recursos/output/Concluido.txt').resolve()).write_text(result,encoding='utf-8')
