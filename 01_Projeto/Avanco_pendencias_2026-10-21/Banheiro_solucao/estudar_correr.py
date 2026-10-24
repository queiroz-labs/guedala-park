import FreeCAD as A, FreeCADGui as G, Part, pathlib, json, hashlib
P=pathlib.Path(__file__).resolve().parent
d=A.getDocument('Guedala_Park_R42_Consolidado')
sha=hashlib.sha256(pathlib.Path(d.FileName).read_bytes()).hexdigest()
def world(o):
 s=o.Shape.copy(); s.Placement=o.getGlobalPlacement(); return s
def box(x,y,z,a,b,c): return Part.makeBox(a,b,c,A.Vector(x,y,z))
def vis(o):
 while o:
  if not o.ViewObject.Visibility:return False
  o=o.getParentGeoFeatureGroup() if hasattr(o,'getParentGeoFeatureGroup') else None
 return True
def descendants(o):
 out={o.Name}
 for c in getattr(o,'Group',[]):out.update(descendants(c))
 return out
excluded=set()
for n in ['FolhaBanheiroR12','FolhaBanheiroR001','DobradicaComumR12','DobradicaComumR037','DobradicaComumR038','DobradicaComumR039']:
 if d.getObject(n) is None:continue
 excluded.update(descendants(d.getObject(n)))
if 'Banheiro_Correr_Estudo_R01' in A.listDocuments():A.closeDocument('Banheiro_Correr_Estudo_R01')
study=A.newDocument('Banheiro_Correr_Estudo_R01')
def add(n,label,s,col):
 o=study.addObject('PartDesign::Feature',n);o.Label=label;o.Shape=s;o.ViewObject.ShapeColor=col;return o
for n in ['Peca394','Peca395','Peca396','Peca397','Peca399','Peca075','Peca051']:
 o=d.getObject(n);add('Base_'+n,o.Label,world(o),(0.65,0.70,0.63) if n!='Peca075' else (0.90,0.57,0.18))
frame=[box(2760,4820,200,600,70,18),box(2760,4820,727,600,70,18),box(2760,4820,218,18,70,509),box(3342,4820,218,18,70,509)]
# RM026: envelopes of 8x8 grooves only; not manufacturer profile CAD.
for i,z in enumerate([210,727]):
 for j,y in enumerate([4836,4866]):
  groove=box(2778,y,z,564,8,8)
  frame[i]=frame[i].cut(groove)
  rail=add('Trilho%d%d'%(i,j),'RM026 — envelope do rasgo, perfil a detalhar',groove,(0.62,0.64,0.67));rail.ViewObject.Transparency=45
for i,s in enumerate(frame):add('Apoio%d'%i,'Moldura externa — fixação a detalhar',s,(0.65,0.46,0.28))
ctrl=study.addObject('App::FeaturePython','Controle')
for n in ['CursoEsquerda','CursoDireita']:
 ctrl.addProperty('App::PropertyFloatConstraint',n,'Movimento');setattr(ctrl,n,(0,0,270,1))
panels=[]
for n,x,y in [('Esquerda',2780,4840),('Direita',3050,4870)]:
 o=add(n,'Porta '+n.lower()+' 290 × 502 × 18 — estudo',box(0,0,0,290,18,502),(0.86,0.79,0.65))
 o.Placement.Base=A.Vector(x,y,221.5)
 o.setExpression('Placement.Base.x',str(x)+(' + ' if n=='Esquerda' else ' - ')+'Controle.Curso'+n)
 panels.append(o)
storage=box(2778,4890,218,564,382,509)
obs=[]
for o in d.Objects:
 if o.Name in excluded or hasattr(o,'Group') or not hasattr(o,'Shape') or not hasattr(o,'getGlobalPlacement') or o.Shape.isNull() or not o.Shape.Solids or not vis(o):continue
 s=world(o);b=s.BoundBox
 if b.XMax>=2760 and b.XMin<=3360 and b.YMax>=4820 and b.YMin<=4890 and b.ZMax>=200 and b.ZMin<=745:obs.append((o.Name,s))
hits=[]
def check(n,s):
 for name,t in obs:
  if s.BoundBox.intersect(t.BoundBox) and s.common(t).Volume>0.1:hits.append([n,name,s.common(t).Volume])
for i,s in enumerate(frame):check('Apoio%d'%i,s)
# Swept rectangular solids prove every translation in 0..270, not only sampled poses.
sweeps=[box(2780,4840,221.5,560,18,502),box(2780,4870,221.5,560,18,502)]
for i,s in enumerate(sweeps):check('CursoCompleto%d'%i,s)
result={'status':'ESTUDO — não liberado para fabricação ou incorporação','source_sha256':sha,'source_unchanged':hashlib.sha256(pathlib.Path(d.FileName).read_bytes()).hexdigest()==sha,'collisions_with_visible_source_leaves':hits,'obstacles_checked':[n for n,s in obs],'storage_envelope_mm':[564,382,509],'storage_gross_litres':storage.Volume/1e6,'new_parts_intrusion_mm3':sum(s.common(storage).Volume for s in frame+sweeps),'door_width_height_thickness_mm':[290,502,18],'overlap_mm':20,'travel_mm':270,'clear_access_each_side_mm':272,'front_projection_vs_old_mm':50,'projection_vs_countertop_mm':20,'entry_leaf_static_clearance_mm':min(s.distToShape(world(d.getObject('Peca075')))[0] for s in frame+sweeps),'panel_gap_mm':12,'pending':['Fixação estrutural da moldura externa e proteção contra umidade','Perfis reais, carros, guias, batentes e puxadores embutidos; CAD atual só contém envelopes de rasgos','Confirmar porta de entrada real: largura, eixo e maçaneta; R42 representa folha ideal de 700 mm','Conferir manutenção da cuba/sifão pelo acesso parcial; hidráulica não detalhada neste estudo'],'sensitivity_static_leaf_extension_mm':{'0':70,'50':20,'100':-30}}
study.recompute()
result['invalid_shapes']=[o.Name for o in study.Objects if hasattr(o,'Shape') and not o.Shape.isValid()]
(P/'Verificacao.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
study.saveAs(str(P/'Banheiro_Correr_ESTUDO_R01.FCStd'))
G.activeDocument().activeView().viewAxonometric();G.activeDocument().activeView().fitAll();G.updateGui()
