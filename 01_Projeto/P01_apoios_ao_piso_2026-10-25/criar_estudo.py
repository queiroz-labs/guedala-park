"""Estudo separado P01: soco sob base+extensao dos trilhos, sem editarR51."""
from pathlib import Path
import json,hashlib
import FreeCAD as App,FreeCADGui as Gui,Part
HERE=Path(__file__).resolve().parent
data=json.loads((HERE/'Resultados.json').read_text(encoding='utf-8'))
cad=Path(data['cad'])
assert hashlib.sha256(cad.read_bytes()).hexdigest()==data['sha256']
src=next(d for d in App.listDocuments().values() if Path(d.FileName).resolve()==cad.resolve())
assert not Gui.getDocument(src.Name).Modified
assert 'P01_estudo_soco_marcenaria_R01' not in App.listDocuments()
doc=App.newDocument('P01_estudo_soco_marcenaria_R01')
doc.Label='P01 soco de marcenaria - estudo separado condicionado'
context=doc.addObject('App::DocumentObjectGroup','Contexto');context.Label='Caixa e trilhos nominais preservados'
plinth=doc.addObject('App::DocumentObjectGroup','Soco');plinth.Label='Soco18 de marcenaria, altura62 - proposta'
def world(o):
 s=o.Shape.copy();s.Placement=o.getGlobalPlacement().multiply(o.Placement.inverse()).multiply(s.Placement);return s
def bb(s):
 b=s.BoundBox;return [b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]
for name in ['Peca206','Peca207','Peca208','Peca209','Peca210','Peca241','Peca242','Peca243','Peca244',
 'ReferenciaCorrerR002','ReferenciaCorrerR004','ReferenciaCorrerR008','ReferenciaCorrerR14','ReferenciaCorrerR001']:
 original=src.getObject(name)
 o=doc.addObject('PartDesign::Feature','Ref_'+name);o.Label=original.Label;o.Shape=world(original);context.addObject(o)
 o.ViewObject.ShapeColor=(.77,.76,.69);o.ViewObject.Transparency=70
 # Esconder pecas altas so na vista inferior de apresentacao, ficam no estudo.
 if name in ['Peca206','Peca207','Peca208','Peca210','Peca241','Peca242','Peca243','Peca244']:o.ViewObject.Visibility=False
new=[]
for p in data['new_boards']:
 o=doc.addObject('PartDesign::Feature',p['id']);o.Label=p['label'];o.Shape=Part.makeBox(*p['size_mm'],App.Vector(*p['origin_mm']));plinth.addObject(o)
 o.ViewObject.ShapeColor=(.28,.59,.47);o.ViewObject.Transparency=0
 o.addProperty('App::PropertyString','Situacao').Situacao='ESTUDO: apoio nivelado/piso e juntas pendentes; nao aprovado'
 new.append(o)
def area_at_z(a,b,z):
 def faces(s):return [f for f in s.Faces if abs(f.BoundBox.ZMin-z)<1e-6 and abs(f.BoundBox.ZMax-z)<1e-6]
 return sum(f.common(g).Area for f in faces(a) for g in faces(b))
base=world(src.getObject('Peca209'));extension=world(src.getObject('ReferenciaCorrerR002'))
targets={'base':(base,62),'extension':(extension,62),'back':(world(src.getObject('Peca208')),18),
 'side_front_E':(world(src.getObject('ReferenciaCorrerR001')),62),'side_front_D':(world(src.getObject('ReferenciaCorrerR14')),62)}
areas={k:0. for k in targets};contacts=[]
for o in new:
 for label,(target,z) in targets.items():
  a=area_at_z(o.Shape,target,z)
  if a>1e-5:contacts.append({'support':o.Name,'target':label,'area_mm2':a});areas[label]+=a
assert abs(areas['base']-data['contact_main_base_mm2'])<1e-4
assert abs(areas['extension']-data['contact_front_extension_mm2'])<1e-4
assert abs(areas['back']-data['contact_back_mm2'])<1e-4
assert abs(areas['side_front_E']+areas['side_front_D']-data['contact_front_sides_mm2'])<1e-4
assert abs(sum(o.Shape.Volume for o in new)-data['volume_mm3'])<1e-3
# Auditoria de sobreposicao dos21 apoios entre si.
inter=[]
for i,a in enumerate(new):
 for b in new[i+1:]:
  ba,bc=bb(a.Shape),bb(b.Shape)
  if all(min(ba[k+3],bc[k+3])-max(ba[k],bc[k])>1e-6 for k in range(3)):
   vol=a.Shape.common(b.Shape).Volume
   if vol>1e-5:inter.append([a.Name,b.Name,vol])
assert not inter,inter
# Fonte visivel: transformacoes e pais, nao confundir estudo oculto com modelo ativo.
parents={o.Name:[p for p in o.InList if 'Group' in p.PropertiesList and o in p.Group] for o in src.Objects}
memo={}
def visible(o):
 if o.Name not in memo:memo[o.Name]=bool(o.ViewObject.Visibility) and all(visible(p) for p in parents[o.Name])
 return memo[o.Name]
candidates=[];overlaps=[];screened=0
for original in src.Objects:
 if not original.isDerivedFrom('Part::Feature') or original.Shape.isNull() or not visible(original):continue
 screened+=1;s=world(original);bc=bb(s)
 for o in new:
  ba=bb(o.Shape)
  if all(min(ba[k+3],bc[k+3])-max(ba[k],bc[k])>1e-6 for k in range(3)):
   vol=o.Shape.common(s).Volume;candidates.append([o.Name,original.Name,vol])
   if vol>1e-5:overlaps.append([o.Name,original.Name,vol])
assert not overlaps,overlaps
doc.recompute();Gui.activeDocument().activeView().viewAxonometric();Gui.activeDocument().activeView().fitAll()
Gui.activeDocument().activeView().saveImage(str(HERE/'Soco_P01_estudo.png'),1400,850,'White')
doc.saveAs(str(HERE/'P01_soco_sem_tubos_R01_ESTUDO.FCStd'))
assert hashlib.sha256(cad.read_bytes()).hexdigest()==data['sha256']
out=dict(source_R51_unchanged=True,source_visible_shapes_screened=screened,contacts=contacts,
 contact_area=areas,source_overlap_candidates=candidates,source_positive_interferences=overlaps,
 self_interferences=inter,added_wood_parts=len(new),file=doc.FileName,
 scope='Somente geometria nominal; nao valida piso real, nivelamento, juntas, resistencia ou anti-tombamento. Nao incorporado ao modelo completo.')
(HERE/'Verificacao_BREP.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
App.setActiveDocument(src.Name)
print(json.dumps({'contacts':len(contacts),'visible_source_shapes':screened,'interferences':len(overlaps),'area':areas}))
