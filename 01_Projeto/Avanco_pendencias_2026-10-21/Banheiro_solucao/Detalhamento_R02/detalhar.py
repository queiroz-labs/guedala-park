"""R02: construction and service study. Supplier hardware is schematic, not factory CAD."""
import FreeCAD as A, FreeCADGui as G, Part, pathlib, json, hashlib, math
P=pathlib.Path(__file__).resolve().parent
d=A.getDocument('Guedala_Park_R42_Consolidado')
sha=hashlib.sha256(pathlib.Path(d.FileName).read_bytes()).hexdigest()
def box(x,y,z,a,b,c):return Part.makeBox(a,b,c,A.Vector(x,y,z))
def cyl(r,h,x,y,z,axis=(0,0,1)):return Part.makeCylinder(r,h,A.Vector(x,y,z),A.Vector(*axis))
def world(o):
 s=o.Shape.copy();s.Placement=o.getGlobalPlacement();return s
def descendants(o):
 out={o.Name}
 for q in getattr(o,'Group',[]):out.update(descendants(q))
 return out
def visible(o):
 while o:
  if not o.ViewObject.Visibility:return False
  o=o.getParentGeoFeatureGroup() if hasattr(o,'getParentGeoFeatureGroup') else None
 return True
name='Banheiro_Detalhamento_R02'
if name in A.listDocuments():A.closeDocument(name)
s=A.newDocument(name)
def add(name,label,shape,color=(.77,.67,.51),kind='proposta'):
 o=s.addObject('PartDesign::Feature',name);o.Label=label;o.Shape=shape;o.ViewObject.ShapeColor=color
 o.addProperty('App::PropertyString','Natureza','Rastreabilidade');o.Natureza=kind
 return o
def group(name,label):
 g=s.addObject('App::DocumentObjectGroup',name);g.Label=label;return g
context=group('Contexto','Contexto R42 — cópias sem alterações no principal')
for n in ['Peca075','Peca051','Peca399','Peca185']:
 o=d.getObject(n);q=add('Original_'+n,o.Label,world(o),(.65,.70,.63),'cópia R42');context.addObject(q)
 if n in ['Peca075','Peca051','Peca185']:q.ViewObject.Visibility=False
wood=group('Madeira','Caixa original + conjunto frontal removível')
left=box(2760,4820,200,18,70,543)
right=box(3342,4820,200,18,70,543)
base=box(2778,4820,200,564,70,18)
cap=box(2778,4820,725,564,70,18)
original_left=world(d.getObject('Peca395'));original_right=world(d.getObject('Peca394'))
original_base=world(d.getObject('Peca397'))
back=world(d.getObject('Peca396'))
# Plumbing opening is proposed only for the explicit reference scenario.
back=back.cut(cyl(50,18,3060,5272,609,(0,1,0)))
for y in [4840,4870]:
 base=base.cut(box(2778,y-4,210,564,8,8))
 cap=cap.cut(box(2778,y-4,725,564,8,8))
fix=group('Fixacoes','Conjunto frontal: 4 M6×100 + porcas transversais; uniões da moldura')
fasteners=[]
for side,x,axis in [('E',2760,(1,0,0)),('D',3360,(-1,0,0))]:
 for i,z in enumerate([209,734]):
  y=4855
  hole=cyl(3.5,50,x,y,z,axis)
  if side=='E':left=left.cut(hole)
  else:right=right.cut(hole)
  base=base.cut(hole);cap=cap.cut(hole)
  o=add('ConfirmatBase'+side+str(i),'Confirmat 7×50 — base / '+side,hole,(.48,.50,.52),'envelope nominal, rosca não modelada');fix.addObject(o);fasteners.append(o.Shape)
  peg=cyl(4,30,x+(3 if side=='E' else -3),4882,z,axis)
  left=left.cut(peg);right=right.cut(peg);base=base.cut(peg);cap=cap.cut(peg)
  o=add('CavilhaQuadro'+side+str(i),'Cavilha8×30 — união permanente do quadro',peg);fix.addObject(o)
attachment_pegs=[]
for side,x,inner,axis in [('E',2771,2778,(-1,0,0)),('D',3349,3342,(1,0,0))]:
 for i,z in enumerate([260,680]):
  shank=cyl(3.25,106,x,4820,z,(0,1,0));head=cyl(5.5,6,x,4820,z,(0,1,0))
  barrel_hole=cyl(5,14,inner,4915,z,axis)
  if side=='E':left=left.cut(shank.fuse(head));original_left=original_left.cut(shank.fuse(barrel_hole))
  else:right=right.cut(shank.fuse(head));original_right=original_right.cut(shank.fuse(barrel_hole))
  bolt=cyl(3,100,x,4826,z,(0,1,0)).fuse(cyl(5,6,x,4820,z,(0,1,0)))
  o=add('M6'+side+str(i),'M6×100 — desmontagem frontal; cabeça rebaixada',bolt,(.40,.43,.46),'parafuso tipo cabeça cilíndrica; conferir rosca útil até a porca');fix.addObject(o);fasteners.append(o.Shape)
  nut=barrel_hole.cut(cyl(3,12,x,4909,z,(0,1,0)))
  o=add('Porca'+side+str(i),'Porca transversal M6 Ø10×14 — embutida, face interna rente',nut,(.40,.43,.46),'referência dimensional Häfele264.82.014; não afirma estoque local');fix.addObject(o);fasteners.append(o.Shape)
 for i,z in enumerate([350,560]):
  peg=cyl(4,30,x,4875,z,(0,1,0));attachment_pegs.append((x,z))
  if side=='E':left=left.cut(peg);original_left=original_left.cut(peg)
  else:right=right.cut(peg);original_right=original_right.cut(peg)
  o=add('CavilhaRemovivel'+side+str(i),'Cavilha8×30 — colada só no quadro; encaixe seco na caixa',peg);fix.addObject(o);fasteners.append(o.Shape)
wood_shapes=[]
for n,l,sh in [('LateralE','Montante frontal esquerdo18×70×543',left),('LateralD','Montante frontal direito18×70×543',right),('Base','Base do quadro564×70×18',base),('Travessa','Topo do quadro564×70×18',cap),('CaixaE','Lateral original esquerda com furos de união',original_left),('CaixaD','Lateral original direita com furos de união',original_right),('CaixaBase','Base original preservada',original_base),('Fundo','Fundo original com recorte hidráulico hipotético Ø100',back)]:
 o=add(n,l,sh);wood.addObject(o);wood_shapes.append(sh)
rails=group('Trilhos','4 RM026, 564 mm cada — seção simplificada')
rail_shapes=[]
for top in [False,True]:
 for j,y in enumerate([4840,4870]):
  # Published: overall width12, height6.5, slot3.15. Unpublished wall/stem thickness is schematic.
  r=box(2778,y-3.75,212.3,564,7.5,5.7).fuse(box(2778,y-6,218,564,12,.8)).cut(box(2778,y-1.575,213.1,564,3.15,5.7))
  if top:r=r.mirror(A.Vector(0,0,471.5),A.Vector(0,0,1))
  o=add('RM026'+str(int(top))+str(j),'RM026 '+('superior' if top else 'inferior'),r,(.68,.70,.72),'seção simplificada: largura12/altura6,5/ranhura3,15 oficiais; espessuras não cotadas são hipótese');rails.addObject(o);rail_shapes.append(r)
ctrl=s.addObject('App::FeaturePython','Controle')
for n,maximum in [('CursoEsquerda',268),('CursoDireita',233)]:
 ctrl.addProperty('App::PropertyFloatConstraint',n,'Movimento');setattr(ctrl,n,(0,0,maximum,1))
door_groups=[];panel_shapes=[];moving=[];drill=[]
for side,x,y,travel,sign in [('Esquerda',2780,4822,268,1),('Direita',3048,4852,233,-1)]:
 g=s.addObject('App::Part','Folha'+side);g.Label='Folha '+side+' — ferragens internas';g.Placement.Base=A.Vector(x,y,221.5)
 g.setExpression('Placement.Base.x',str(x)+('+' if sign==1 else '-')+'Controle.Curso'+side)
 panel=box(0,0,0,292,18,500)
 for end in [0,1]:
  xx=lambda a:a if end==0 else 292-a
  panel=panel.cut(cyl(16,10,xx(45),18,11,(0,-1,0)))
  for a,z in [(13,12),(22,16),(67.5,16),(77,12),(45,500-19),(45,500-44)]:
   panel=panel.cut(cyl(1.25,10,xx(a),18,z,(0,-1,0)))
   drill.append({'leaf':side,'from_left_mm':xx(a),'from_bottom_mm':z,'type':'piloto ilustrativo Ø2,5 ×10; ajustar à chapa/parafuso; cota de centro do manual'})
  # Conservative fitting envelopes; not manufacturer solid CAD.
  ex=0 if end==0 else 202
  body=box(ex,18,3.5,90,9,36.5)
  peg=cyl(1.25,9.5,xx(45),18,-6)
  o=add('Carro'+side+str(end),'Carro RO25 — envelope 90×9×40, hipótese',body.fuse(peg),(.25,.30,.34),'envelope de conferência, não modelo oficial');g.addObject(o)
  guide=box(xx(45)-6,18,450,12,3,50).fuse(cyl(1.25,8,xx(45),18,500))
  o=add('Guia'+side+str(end),'Guia superior — envelope e pino de teste',guide,(.25,.30,.34),'projeção superior8 e pino2,5 são hipóteses');g.addObject(o)
  for k,(a,z) in enumerate([(13,12),(22,16),(67.5,16),(77,12),(45,500-19),(45,500-44)]):
   screw=cyl(1.75,12,xx(a),21,z,(0,-1,0))
   o=add('Parafuso'+side+str(end)+str(k),'3,5×12 CF — face interna',screw,(.45,.46,.47),'comprimento e diâmetro nominais; cabeça simplificada');g.addObject(o)
 # Blind, vertical finger recess, no projecting handle and no intrusion into storage.
 hx=20 if side=='Esquerda' else 272
 recess=box(hx-9,0,220,18,6,62).fuse(cyl(9,6,hx,0,220,(0,1,0))).fuse(cyl(9,6,hx,0,282,(0,1,0)))
 panel=panel.cut(recess)
 o=add('Painel'+side,'Folha 292×500×18 — cava18×80×6',panel,(.86,.80,.68));g.addObject(o)
 panel_shapes.append(panel);door_groups.append(g)
 moving.extend(g.Group)
stops=group('Batentes','Batentes propostos: curso e acesso ao puxador')
# Thin compliant stops at extreme edges; own receiving recess on side permits2 mm gap.
for i,(x,y,z,a,b,c) in enumerate([(2778,4824,460,2,12,20),(3340,4824,460,2,12,20),(3340,4854,460,2,12,20),(2778,4854,460,37,12,20)]):
 sh=box(x,y,z,a,b,c)
 if i==3:
  for zz in [465,475]:sh=sh.cut(cyl(2,50,2813,4860,zz,(-1,0,0)))
 o=add('Batente'+str(i),'Batente de curso '+str(i+1),sh,(.20,.23,.25),'3 pads resilientes2mm colados; batente traseiro: calço35 + pad2, fixado com2 parafusos4×50');stops.addObject(o)
 if i==3:
  for k,zz in enumerate([465,475]):
   o=add('ParafusoBatente'+str(k),'4×50 — cabeça escareada sob pad removível',cyl(2,50,2813,4860,zz,(-1,0,0)),(.45,.46,.47),'fixação proposta do calço; pré-furo e capacidade na chapa a conferir');stops.addObject(o)
hydro=group('Hidraulica','Cenário hidráulico de referência — não existente nem aprovado')
trap=cyl(24.5,105,3060,5040,516).fuse(cyl(16,124,3060,5040,621)).fuse(cyl(20,250,3060,5040,609,(0,1,0)))
o=add('Sifao','Sifão: referência Deca1680 / posição hipotética',trap,(.30,.58,.68),'Ø49/queda229/93 abaixo eixo conforme ficha; tubos simplificados, eixo esgoto609 e posição são hipóteses');hydro.addObject(o)
o=add('Canopla','Canopla — envelope Ø80 no recorte Ø100',cyl(40,3,3060,5287,609,(0,1,0)),(.30,.58,.68),'envelope da largura total publicada80');hydro.addObject(o)
service=group('Acesso','Volumes de teste de manutenção — ocultos na vista normal')
access=box(2960,4750,450,200,390,220)
cup_sweep=cyl(40,173,3060,5040,436)
for n,l,sh in [('Maos','Acesso frontal 200×220 — hipótese, não prova ergonômica',access),('Desmontagem','Descida de80 mm da tampa/corpo — teste',cup_sweep)]:
 o=add(n,l,sh,(.22,.67,.42),'envelope de ensaio');o.ViewObject.Transparency=75;o.ViewObject.Visibility=False;service.addObject(o)
s.recompute()
excluded=set(['Peca394','Peca395','Peca396','Peca397'])
for n in ['FolhaBanheiroR12','FolhaBanheiroR001','DobradicaComumR12','DobradicaComumR037','DobradicaComumR038','DobradicaComumR039']:
 excluded.update(descendants(d.getObject(n)))
obstacles=[]
for o in d.Objects:
 if o.Name in excluded or hasattr(o,'Group') or not hasattr(o,'Shape') or not hasattr(o,'getGlobalPlacement') or o.Shape.isNull() or not o.Shape.Solids:continue
 if not visible(o) and o.Name not in ['Peca075','Peca051','Peca399','Peca185']:continue
 q=world(o);b=q.BoundBox
 if b.XMax>=2740 and b.XMin<=3980 and b.YMax>=4400 and b.YMin<=5310 and b.ZMax>=190 and b.ZMin<=850:obstacles.append((o.Name,q))
def hits(shape,targets):
 out=[]
 for n,q in targets:
  if shape.BoundBox.intersect(q.BoundBox):
   volume=shape.common(q).Volume
   if volume>.1:out.append({'target':n,'volume_mm3':round(volume,4)})
 return out
struct=[(o.Name,o.Shape) for o in wood.Group]
storage=box(2778,4890,218,564,382,509)
result={'source_sha256':sha,'status':'Detalhamento de estudo; não liberar fabricação/incorporação','assumptions':['Hardware RO25 em envelopes, não CAD real','Sifão e ponto de esgoto posicionados apenas para cenário de manutenção','Conexões, válvula e flexíveis não definidos'],'operation':[],'service':{},'storage':{},'fixings':{},'invalid_shapes':[]}
# Continuous sweeps of complete conservative moving envelopes, not just panels.
for side,xmin,y,width in [('Esquerda',2780,4822,560),('Direita',2815,4852,525)]:
 envelope=box(xmin,y,221.5,width,27,500)
 result['operation'].append({'leaf':side,'against_R42':hits(envelope,obstacles),'against_new_wood':hits(envelope,struct),'intrusion_mm3':envelope.common(storage).Volume})
result['operation_gap_hardware_to_other_panel_mm']=3
result['rear_handle_visible_strip_mm']=35
result['clear_openings_mm']={'left':270,'right':235,'both_leaves_removed':564,'service_height_under_stone':527}
result['storage']={'gross_original_litres':storage.Volume/1e6,'new_wood_intrusion_mm3':sum(q.common(storage).Volume for n,q in struct),'hardware_fixings_intrusion_mm3':sum(q.common(storage).Volume for q in fasteners),'note':'Hidráulica não contada como armazenamento; mesmo envelope bruto preservado, não109,66L úteis.'}
fixed_targets=obstacles+[(n,q) for n,q in struct if n in ['CaixaE','CaixaD','CaixaBase','Fundo']]
# Remove4 bolts, support whole frame, keep both leaves closed/secured, withdraw20,
# shift120 right, then withdraw330. Pins/rails remain assembled; no assumed lift clearance.
result['service']['front_module_steps']=[]
for label,sh in [('Retirar20_frente',box(2760,4800,200,600,90,543)),('Deslocar120_direita',box(2760,4800,200,720,85,543)),('Retirar330_frente',box(2880,4470,200,600,415,543))]:
 result['service']['front_module_steps'].append({'step':label,'hits':hits(sh,fixed_targets)})
result['service']['withdraw_dowels']=[]
for x,z in attachment_pegs:result['service']['withdraw_dowels']+=hits(cyl(4,50,x,4855,z,(0,1,0)),fixed_targets)
result['service']['hands_with_front_removed']=hits(access,fixed_targets)
result['service']['cup_descent80']=hits(cup_sweep,fixed_targets)
# Detached trap envelope (80 wide x250deep x229 high), translated forward after disconnection.
result['service']['detached_trap_straight_front']=hits(box(3020,4700,516,80,550,229),fixed_targets)
result['service']['hydraulics_vs_wood']=hits(trap,struct)
result['service']['clearance_trap_bottom_to_base_mm']=516-218
result['service']['clearance_after_drop80_mm']=436-218
result['fixings']={'module_M6x100':4,'cross_nuts_M6_d10_L14':4,'frame_confirmat_7x50':4,'frame_alignment_dowels_8x30':4,'removable_interface_dowels_8x30':4,'ro25_screws_3_5x12':24,'module_bolt_axes_X':[2771,3349],'module_bolt_axes_Z':[260,680],'cross_nut_axis_Y':4915,'nut_hole_remaining_outer_skin_mm':4,'residual_board_behind_cup_bore_mm':8,'pilot_diameter_status':'2,5 no modelo é hipótese; adequar ao material e parafuso escolhido','load_status':'Ligação detalhada geometricamente, sem cálculo/ensaio da chapa e suspensão.30kg é limite publicado do kit, não da união.'}
result['fixings']['stop_screws_4x50']=2
module_volume=sum(q.Volume for n,q in struct if n in ['LateralE','LateralD','Base','Travessa'])+sum(q.Volume for q in panel_shapes)
result['front_module']={'wood_mass_kg_density650_900':[round(module_volume/1e9*650,2),round(module_volume/1e9*900,2)],'hardware_mass':'adicionar; não determinada','removal':'Manter folhas fechadas e imobilizadas; apoiar conjunto antes de retirar os4 M6. Não depende de levantar folhas ou soltar guias.','retention':'Batentes limitam deslocamento; antidescarrilamento e regulagem reais do RO25 continuam a conferir no kit.'}
result['source_unchanged']=hashlib.sha256(pathlib.Path(d.FileName).read_bytes()).hexdigest()==sha
result['final_dimensions']={'leaf':[292,500,18],'front_module':[600,70,543],'overlap_mm':24,'front_travel_mm':268,'rear_travel_mm':233,'gap_below_stone_mm':2}
result['invalid_shapes']=[o.Name for o in s.Objects if hasattr(o,'Shape') and not o.Shape.isNull() and not o.Shape.isValid()]
(P/'Verificacao_R02.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
(P/'Furacao_referencia.json').write_text(json.dumps(drill,ensure_ascii=False,indent=2),encoding='utf-8')
s.saveAs(str(P/'Banheiro_Detalhamento_R02.FCStd'))
A.setActiveDocument(s.Name)
v=G.getDocument(s.Name).activeView();v.setCamera('#Inventor V2.1 ascii\nOrthographicCamera { position 3060 3500 480 orientation 1 0 0 1.57079632679 nearDistance 1 farDistance 4000 focalDistance 1500 height 800 }');G.updateGui()
