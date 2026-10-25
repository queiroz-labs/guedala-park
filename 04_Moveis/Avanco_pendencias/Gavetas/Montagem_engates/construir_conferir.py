"""Estudo separado. Não libera usinagem nem substitui engates FGVTN por Blum."""
import FreeCAD as A, FreeCADGui as G, Part, pathlib, json, shutil, hashlib, itertools
ROOT=pathlib.Path(__file__).resolve().parent
BASE=ROOT.parent/'Montagem_vertical_R02'/'Escritorio_montagem_vertical_R02_ESTUDO.FCStd'
OUT=ROOT/'Escritorio_fixacao_frentes_R03_ESTUDO.FCStd'
shutil.copyfile(BASE,OUT)
d=A.openDocument(str(OUT));d.Label='R03 — fixação das frentes em estudo; engates pendentes'
src=A.getDocument('Guedala_Park_R42_Consolidado')
original_hash=hashlib.sha256(pathlib.Path(src.FileName).read_bytes()).hexdigest()
def bbox(q):
 b=q.BoundBox;return [b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]
def block(b):return Part.makeBox(b[3]-b[0],b[4]-b[1],b[5]-b[2],A.Vector(*b[:3]))
def shape(o):
 q=o.Shape.copy();q.Placement=o.getGlobalPlacement();return q
def feature(group,name,q,label,color):
 o=d.addObject('PartDesign::Feature',name);o.Shape=q;o.Label=label;group.addObject(o);o.ViewObject.ShapeColor=color;return o
template=Part.Shape();template.read(str(ROOT/'Fontes'/'295.1000_45225749.step'))
fixings=[];drills=[];storage=[];head_envelopes=[]
for idx,n in enumerate(['Gaveta008','Gaveta009']):
 group=d.getObject('Caixa_'+n);group.Extensao=0
d.recompute()
for idx,n in enumerate(['Gaveta008','Gaveta009']):
 group=d.getObject('Caixa_'+n);floor=[536,644][idx];h=[60.4,54][idx]
 front=d.getObject(n+'_Frente');board=d.getObject(n+'_Dianteira');front_original=shape(front);board_original=shape(board)
 for j,x in enumerate([4400,4600]):
  # Cup center halfway through the rail's assumed 0..3 mm vertical adjustment.
  z=floor+28;axisz=floor+26.5
  bore=Part.makeCylinder(10,10.5,A.Vector(x,682,z),A.Vector(0,1,0))
  through=Part.makeCylinder(2.5,16,A.Vector(x,666,axisz),A.Vector(0,1,0))
  front.Shape=front.Shape.cut(bore);board.Shape=board.Shape.cut(through)
  # Exact official geometry; this is one static centered STEP, not an articulated nut.
  plug=template.copy();plug.translate(A.Vector(73,-31,-37));plug.rotate(A.Vector(),A.Vector(1,0,0),-90);plug.translate(A.Vector(x,682,z))
  o=feature(group,n+'_Regulador_'+str(j),plug,'Blum 295.1000 — STEP estático; orientação axial a confirmar',(0.9,0.9,0.83))
  # Conservative reserved space for head + washer. No invented thread geometry.
  env=Part.makeCylinder(5,5,A.Vector(x,661,axisz),A.Vector(0,1,0))
  e=feature(group,n+'_Cabeca_limite_'+str(j),env,'RESERVA Ø10 × 5 — cabeça/arruela, produto pendente',(0.95,0.55,0.15))
  e.ViewObject.Transparency=35;head_envelopes.append(e.Name)
  fixings.append({'name':o.Name,'cup_center':[x,682,z],'screw_axis_at_zero':[x,666,axisz],
   'nominal_cup_hole_diameter_mm':20,'blind_depth_mm':10.5,'remaining_front_thickness_mm':7.5,
   'screw_clearance_hole_diameter_proposed_mm':5,'screw_center_offset_z_at_rail_0_and_3_mm':[-1.5,1.5],
   'documented_adjustment_mm':2,'adjustment_reserve_mm':0.5,
   'step_valid':plug.isValid(),'step_volume_difference_mm3':abs(plug.Volume-template.Volume),
   'pressfit_interference_with_front_mm3':plug.common(front.Shape).Volume,
   'pressfit_note':'STEP outside diameter20.8 vs official bore20: interference ribs; do not enlarge bore from STEP.',
   'axial_orientation':'Provisional: local Z37 at back face. Reversing axial orientation also fits the blind pocket; thread engagement not released.'})
  drills.append({'drawer':n,'x':x,'cup_z':z,'screw_z_at_zero':axisz})
 # Verify the exposed decorative skin is unchanged, despite blind bores.
 skin=block([4301,692.5,[481,601][idx],4699,700,[599,719][idx]])
 assert front_original.common(skin).cut(front.Shape.common(skin)).Volume<.001
 assert len(front.Shape.Solids)==1 and len(board.Shape.Solids)==1
 util=block([4338.5,297,floor,4661.5,661,floor+h]);d.getObject('Util_'+n).Shape=util
 d.getObject('Util_'+n).Label='Prisma útil após reserva de fixação — '+n
 storage.append({'drawer':n,'original_mm':[322,359,h],'after_head_reserve_mm':[323,364,h],
  'before_l':322*359*h/1e6,'after_l':util.Volume/1e6,'gain_percent':(323*364/(322*359)-1)*100})
d.getObject('Limites_do_estudo').Escopo='R03: quatro reguladores Blum 295.1000 oficiais; furos cegos e reservas de cabeça. Estudo condicional, sem engates FGVTN dimensionados. Parafuso, orientação do regulador, engajamento e resistência pendentes.'
d.getObject('Limites_do_estudo').ResultadoAuditoria='NÃO INCORPORAR À R42: conferir relatório R03. Geometria condicional não equivale a montagem liberada.'
d.recompute()
car={o.Name:shape(o) for o in d.getObject('Carcaca_470x248').Group}
draw=[{o.Name:shape(o) for o in d.getObject('Caixa_'+n).Group} for n in ['Gaveta008','Gaveta009']]
# Bounding boxes of individual solids, swept continuously. Conservative for holes,
# ribs and cylindrical heads. Cup follows aligned front; wood/head follow rail height.
envs=[];cargo=[]
for i,n in enumerate(['Gaveta008','Gaveta009']):
 e={}
 for name,q in draw[i].items():
  b=bbox(q);b[4]+=378
  if not (name.endswith('_Frente') or '_Regulador_' in name):b[5]+=3
  e[name]=block(b)
 envs.append(e)
 b=bbox(shape(d.getObject('Util_'+n)));b[4]+=378;b[5]+=3;cargo.append(block(b))
checks=0;hits=[]
def test(kind,na,q,nb,s):
 global checks
 checks+=1
 a=bbox(q);b=bbox(s)
 if all(min(a[k+3],b[k+3])-max(a[k],b[k])>1e-7 for k in range(3)):
  v=q.common(s).Volume
  if v>.001:hits.append({'kind':kind,'a':na,'b':nb,'volume_mm3':v})
for i in range(2):
 for name,q in envs[i].items():
  for name2,s in car.items():test('moving_vs_carcass',name,q,name2,s)
  for name2,s in envs[1-i].items():test('independent_drawers',name,q,name2,s)
 for name,s in car.items():test('payload_vs_carcass',str(i),cargo[i],name,s)
 for name,s in envs[1-i].items():test('payload_vs_other_drawer',str(i),cargo[i],name,s)
 # Within one drawer all parts share travel; test payload/head through regulation.
 for a in [0,1.5,3]:
  q=shape(d.getObject('Util_'+['Gaveta008','Gaveta009'][i]));q.translate(A.Vector(0,0,a))
  for name,s0 in draw[i].items():
   s=s0.copy()
   if not(name.endswith('_Frente') or '_Regulador_' in name):s.translate(A.Vector(0,0,a))
   test('payload_vs_own_parts',str((i,a)),q,name,s)
exclude=set()
def visit(o):
 if o.Name in exclude:return
 exclude.add(o.Name)
 for c in getattr(o,'Group',[]):visit(c)
visit(src.getObject('Modulo015'))
outer=Part.makeCompound(list(car.values())+[q for e in envs for q in e.values()]+cargo)
external=[]
for o in src.Objects:
 if o.Name in exclude or hasattr(o,'Group') or not hasattr(o,'Shape') or o.Shape.isNull() or not o.Shape.Solids:continue
 before=len(hits);test('external_R42', 'R03_envelope',outer,o.Name,shape(o))
 if len(hits)>before:external.append(o.Name)
invalid=[o.Name for o in d.Objects if hasattr(o,'Shape') and not o.Shape.isNull() and not o.Shape.isValid()]
assert not hits and not invalid
assert all(x['after_l']>=x['before_l'] for x in storage)
assert all(x['step_volume_difference_mm3']<.001 for x in fixings)
assert original_hash=='b30ae9ab9c82620ecdab26b2cfae589037954356d515b483b5b6849f76e4bc26'
result={'status':'ESTUDO_CONDICIONAL_NAO_LIBERADO','source_sha256':original_hash,'checks':checks,'collisions':hits,'invalid_shapes':invalid,
 'method':'Conservative individual bounding solids swept Y0..378, Z0..3 for box/head; fascia and cup vertically fixed. Payload vs own parts at Z0,1.5,3; geometry translates together. Thread/nut motion not modeled.',
 'fixings':fixings,'drilling_proposal':drills,'storage':storage,
 'clearances_mm':{'lower_payload_to_upper_front_at_max_regulation':1.6,'upper_payload_to_top_at_max_regulation':1,'fascia_joint':2},
 'blockers':['FGVTN conventional clip and rail exact dimensional profile, hole pattern and release travel missing',
 'Blum cup axial insertion orientation and compatible screw thread, length, head, washer and engagement require confirmation',
 'Static STEP does not articulate nut adjustment; +/-2 mm is documented range, not CAD joint validation',
 'Rear drill/notch geometry and screw fixation depend on exact FGVTN assembly sheet',
 'Nominal margins of1/1.6 mm require manufacturing tolerance allocation and physical fitting',
 'Wood joints, screw retention, loaded movement and strength not certified']}
(ROOT/'Auditoria_R03.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
d.recompute();d.save()
G.activeDocument().activeView().viewAxonometric();G.activeDocument().activeView().fitAll();G.updateGui()
