from pathlib import Path
import json,hashlib
import FreeCAD as App
root=(Path(__file__).resolve().parent / '.').resolve();p=(Path(__file__).resolve().parent / 'Guedala_Park_R17_Equipamentos.FCStd').resolve()
a=json.loads(((Path(__file__).resolve().parent / 'Conferencia_R17.json').resolve()).read_text(encoding='utf-8'))
src=Path(a['source']);prev=next(x for x in App.listDocuments().values() if x.FileName and Path(x.FileName).resolve()==src)
d=next(x for x in App.listDocuments().values() if x.FileName and Path(x.FileName).resolve()==p)
assert d.isSaved() and p.exists() and p.stat().st_size>100000
App.closeDocument(d.Name);d=App.openDocument(str(p));d.recompute();App.setActiveDocument(d.Name)
assert abs(float(d.getObject('Peca351').Width)-352)<1e-6
assert abs(d.getObject('Peca140').Placement.Base.y-6460)<1e-6
assert d.getObject('ReferenciasEquipamentosR17').Visibility==False
changes=[]
for old in prev.Objects:
 o=d.getObject(old.Name);assert o is not None
 if o.TypeId in ['Part::Box','Part::Feature','Part::Cut','PartDesign::Feature']:
  fields=[]
  for f in ['Length','Width','Height']:
   if f in old.PropertiesList and abs(float(getattr(old,f))-float(getattr(o,f)))>1e-7:fields.append(f)
  if any(abs(x-y)>1e-7 for x,y in zip(old.Placement.Matrix.A,o.Placement.Matrix.A)):fields.append('Placement')
  if fields:changes.append({'name':o.Name,'fields':fields})
assert {x['name'] for x in changes}=={'Peca140','Peca351'}, str(changes)
invalid=[{'name':o.Name,'state':list(o.State)} for o in d.Objects if 'Invalid' in o.State]
assert not invalid,str(invalid)
assert hashlib.sha256(src.read_bytes()).hexdigest()==a['source_sha256']
controls=[]
for o in d.Objects:
 if o.Name.startswith('Controle'):
  fields={q:float(getattr(o,q)) for q in ['Abertura','Deslocamento','RetiradaSaco','EndireitarSaco','RetiradaConjunto','RetiradaPainelSuperior','ElevarAlmofada','DeslocamentoAlmofada'] if q in o.PropertiesList}
  if fields:controls.append({'name':o.Name,'values':fields})
# Read controls as saved; do not exercise old mechanisms or overwrite their valid baseline.
report={'file':str(p),'persisted_micro_depth':float(d.getObject('Peca351').Width),'persisted_purifier_y':d.getObject('Peca140').Placement.Base.y,'source_R16_unchanged':True,'inherited_geometry_changes':changes,'invalid_expressions':invalid,'controls_read_only':controls,'new_boxes_valid':all(d.getObject(z['name']).Shape.isValid() for z in a['zones'])}
assert report['new_boxes_valid']
d.save();((Path(__file__).resolve().parent / 'Reabertura_R17.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
result={k:v for k,v in report.items() if k!='controls_read_only'}
