import FreeCAD as A, FreeCADGui as G, Part, pathlib, json, shutil, hashlib
ROOT=pathlib.Path(__file__).resolve().parent
OUT=ROOT/'Escritorio_fixacao_simples_R04_ESTUDO.FCStd'
shutil.copyfile(ROOT.parent/'Montagem_vertical_R02/Escritorio_montagem_vertical_R02_ESTUDO.FCStd',OUT)
d=A.openDocument(str(OUT));d.Label='R04 — frentes com parafusos; engates FGVTN por validar'
src=A.getDocument('Guedala_Park_R42_Consolidado')
def s(o):
 q=o.Shape.copy();q.Placement=o.getGlobalPlacement();return q
def b(q):
 v=q.BoundBox;return [v.XMin,v.YMin,v.ZMin,v.XMax,v.YMax,v.ZMax]
def box(v):return Part.makeBox(v[3]-v[0],v[4]-v[1],v[5]-v[2],A.Vector(*v[:3]))
def cyl(r,y,length,x,z):return Part.makeCylinder(r,length,A.Vector(x,y,z),A.Vector(0,1,0))
def add(g,name,q,label):
 o=d.addObject('PartDesign::Feature',name);o.Shape=q;o.Label=label;g.addObject(o);o.ViewObject.ShapeColor=(.65,.68,.72);return o
for n in ['Gaveta008','Gaveta009']:d.getObject('Caixa_'+n).Extensao=0
d.recompute()
hardware=[];drills=[];metrics=[];fix_tests=[]
for i,n in enumerate(['Gaveta008','Gaveta009']):
 floor=[536,644][i];height=[60.4,54][i];g=d.getObject('Caixa_'+n)
 front=d.getObject(n+'_Frente');board=d.getObject(n+'_Dianteira');original_front=s(front)
 for j,(x,zlocal) in enumerate([(4400,13),(4600,13),(4400,40),(4600,40)]):
  zhole=floor+zlocal;z=zhole+1.5
  hole=cyl(4,666,16,x,zhole);board.Shape=board.Shape.cut(hole)
  washer=cyl(7.5,664.8,1.2,x,z).cut(cyl(2.65,664.8,1.2,x,z))
  # Simplified documented nominal envelopes; no helical thread fabrication model.
  screw=cyl(4,661.9,2.9,x,z).fuse(cyl(2,664.8,28,x,z)).fuse(Part.makeCone(2,0,2,A.Vector(x,692.8,z),A.Vector(0,1,0)))
  for kind,q in [('Arruela',washer),('Parafuso',screw)]:
   o=add(g,n+'_'+kind+'_'+str(j),q,kind+' — fixação direta, geometria nominal');hardware.append(o.Name)
  drills.append({'drawer':n,'x':x,'passage_z_at_rail_zero':zhole,'front_screw_z':z,'passage_diameter_mm':8,
   'front_marking':'Mark through aligned assembly. Pilot diameter/depth per actual board and screw supplier; not automatically cut in this study.',
   'screw_nominal':'Wood/particleboard screw4x30 pan head, nominal head8x2.9','washer_nominal_mm':[5.3,15,1.2],
   'penetration_in_front_mm':12.8,'remaining_front_skin_mm':5.2})
  # Full 0..3 range: shaft max4.3, passage8; offset envelope1.5 vertical +0.5 horizontal.
  offset=(1.5**2+.5**2)**.5
  fix_tests.append({'radial_clearance_min_mm':4-2.15-offset,'washer_cover_min_mm':14.4/2-4-offset,
   'head_overlap_washer_hole_min_mm':7.5/2-5.6/2,'head_reserved_depth_clearance_mm':5-1.4-2.9})
 assert original_front.cut(front.Shape).Volume<.001
 util=box([4338.5,297,floor,4661.5,661,floor+height]);d.getObject('Util_'+n).Shape=util
 d.getObject('Util_'+n).Label='Prisma útil após fixação direta — '+n
 metrics.append({'drawer':n,'before_mm':[322,359,height],'after_mm':[323,364,height],'before_l':322*359*height/1e6,'after_l':util.Volume/1e6})
d.recompute()
car={o.Name:s(o) for o in d.getObject('Carcaca_470x248').Group}
draw=[{o.Name:s(o) for o in d.getObject('Caixa_'+n).Group} for n in ['Gaveta008','Gaveta009']]
def stays_aligned(name):return name.endswith('_Frente') or name in hardware
envs=[];cargo=[]
for i,n in enumerate(['Gaveta008','Gaveta009']):
 e={}
 for name,q in draw[i].items():
  v=b(q);v[4]+=378
  if not stays_aligned(name):v[5]+=3
  e[name]=box(v)
 envs.append(e);v=b(s(d.getObject('Util_'+n)));v[4]+=378;v[5]+=3;cargo.append(box(v))
hits=[];checks=0
def test(kind,na,q,nb,r):
 global checks
 checks+=1;v=b(q);w=b(r)
 if all(min(v[k+3],w[k+3])-max(v[k],w[k])>1e-7 for k in range(3)):
  vol=q.common(r).Volume
  if vol>.001:hits.append({'kind':kind,'a':na,'b':nb,'volume_mm3':vol})
for i in range(2):
 for name,q in envs[i].items():
  for name2,r in car.items():test('moving_vs_carcass',name,q,name2,r)
  for name2,r in envs[1-i].items():test('independent_drawers',name,q,name2,r)
 for name,r in car.items():test('cargo_vs_carcass',str(i),cargo[i],name,r)
 for name,r in envs[1-i].items():test('cargo_vs_other_drawer',str(i),cargo[i],name,r)
 for a in [0,1.5,3]:
  q=s(d.getObject('Util_'+['Gaveta008','Gaveta009'][i]));q.translate(A.Vector(0,0,a))
  for name,r0 in draw[i].items():
   r=r0.copy()
   if not stays_aligned(name):r.translate(A.Vector(0,0,a))
   test('cargo_own_parts',str((i,a)),q,name,r)
  board=s(d.getObject(['Gaveta008','Gaveta009'][i]+'_Dianteira'));board.translate(A.Vector(0,0,a))
  for name,r in draw[i].items():
   if name in hardware:test('hardware_through_passage',str(a),board,name,r)
# Interference of screw thread with front is intentional purchase in wood, not a clearance joint.
intentional=[]
for i,n in enumerate(['Gaveta008','Gaveta009']):
 for name,r in draw[i].items():
  if '_Parafuso_' in name:intentional.append({'name':name,'purchase_volume_mm3':r.common(s(d.getObject(n+'_Frente'))).Volume})
exclude=set()
def visit(o):
 if o.Name in exclude:return
 exclude.add(o.Name)
 for c in getattr(o,'Group',[]):visit(c)
visit(src.getObject('Modulo015'))
outer=Part.makeCompound(list(car.values())+[q for e in envs for q in e.values()]+cargo)
for o in src.Objects:
 if o.Name in exclude or hasattr(o,'Group') or not hasattr(o,'Shape') or o.Shape.isNull() or not o.Shape.Solids:continue
 test('external_R42','R04',outer,o.Name,s(o))
invalid=[o.Name for o in d.Objects if hasattr(o,'Shape') and not o.Shape.isNull() and not o.Shape.isValid()]
assert not invalid and not hits
assert all(all(v>0 for v in t.values()) for t in fix_tests)
assert all(m['after_l']>m['before_l'] for m in metrics)
sha=hashlib.sha256(pathlib.Path(src.FileName).read_bytes()).hexdigest()
assert sha=='b30ae9ab9c82620ecdab26b2cfae589037954356d515b483b5b6849f76e4bc26'
result={'status':'FIXACAO_SIMPLIFICADA_GEOMETRIA_CONFERIDA_ENGATES_PENDENTES','source_sha256':sha,'checks':checks,'collisions':hits,'invalid_shapes':invalid,
 'storage':metrics,'drilling':drills,'fixation_tolerance_checks':fix_tests,'intentional_screw_front_intersections':intentional,
 'method':'Continuous conservative individual bounding envelopes Y0..378; wood/cargo Z0..3; front and tightened screw/washer assembly vertically aligned. Nominal passage intersections at0/1.5/3; analytical shaft+hole and washer coverage throughout adjustment incl0.5 horizontal.',
 'assembly_sequence':['Fit and adjust FGVTN rails/box first, using verified manufacturer jig','Clamp front with2mm joint and reference alignment','Mark pilot positions through clearance holes; drill with depth stop according to actual board/screw supplier','Install four4x30 pan-head screws and wide washers per front, tighten evenly','If changing box height: loosen front screws, realign front, retighten; do not force adjustment while clamped','Check retention and loaded travel on real material'],
 'not_validated':['FGVTN exact clip envelope, fasteners and rear cuts','Actual board material/retention, pilot drilling and tightening torque','As-built tolerance stack for1/1.6mm cargo clearance','Physical loaded movement'],
 'main_model_modified':False}
(ROOT/'Auditoria_R04.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
d.getObject('Limites_do_estudo').Escopo='R04: frentes com4 parafusos4x30 e arruelas largas por gaveta; passagemØ8; sem reguladores Blum. Pilotos dependem da chapa real. Engates FGVTN ainda não validados.'
d.getObject('Limites_do_estudo').ResultadoAuditoria='Fixação simplificada conferida geometricamente; NÃO LIBERADO para incorporação como montagem concluída: engates/perfil, recortes e tolerâncias pendentes.'
d.recompute();d.save();G.activeDocument().activeView().viewAxonometric();G.activeDocument().activeView().fitAll();G.updateGui()
