from pathlib import Path
import json
import FreeCAD as App
root=(Path(__file__).resolve().parent / '.').resolve()
doc=next(d for d in App.listDocuments().values() if d.FileName and Path(d.FileName).resolve()==(Path(__file__).resolve().parent / 'Guedala_Park_R12_Banheiro_Simples.FCStd').resolve())
assert doc.getObject('PrateleiraEspelhadoR12') is None,'Já aplicada; não duplicar prateleiras'
m=doc.getObject('Modulo018');data=json.loads(((Path(__file__).resolve().parent / 'Montagem_R12.json').resolve()).read_text(encoding='utf-8'));shelves=[]
for i,z in enumerate([244,488],1):
 o=doc.addObject('Part::Box','PrateleiraEspelhadoR12');m.addObject(o);o.Label='Prateleira removível espelhado '+str(i)+' - proposta'
 o.Length=560;o.Width=104;o.Height=18;o.Placement.Base=App.Vector(20,26,z);o.ViewObject.ShapeColor=doc.getObject('Peca402').ViewObject.ShapeColor
 o.addProperty('App::PropertyString','Status');o.Status='Proposta18 com2mm lateral/frente/trás. Quatro apoios comuns por prateleira candidatos, sem modelo de pino/furação/carga liberados.'
 shelves.append(o)
doc.recompute()
def shape(o):
 s=o.Shape.copy();s.Placement=o.getGlobalPlacement();return s
def common(a,b):
 x,y=a.BoundBox,b.BoundBox
 if any(getattr(x,k+'Max')<=getattr(y,k+'Min')+1e-6 or getattr(y,k+'Max')<=getattr(x,k+'Min')+1e-6 for k in ['X','Y','Z']):return 0
 return a.common(b).Volume
static=[]
for o in shelves:
 for t in [v for v in m.Group if v.TypeId=='Part::Box' and v!=o]:
  volume=common(shape(o),shape(t))
  if volume>.1:static.append({'shelf':o.Name,'target':t.Name,'mm3':volume})
cases=[]
for r in data['doors']:
 if r['module']!='Modulo018':continue
 objects=[doc.getObject(r['front']),doc.getObject(r['mirror'])]+[doc.getObject(b['body']) for h in r['hinges'] for b in h['bodies']]+[doc.getObject(h['plate']) for h in r['hinges']]
 c=doc.getObject(r['control'])
 for angle in [0,30,60,86]:
  c.Abertura=angle;doc.recompute();hits=[]
  for o in objects:
   for shelf in shelves:
    volume=common(shape(o),shape(shelf))
    if volume>.1:hits.append({'moving':o.Name,'shelf':shelf.Name,'mm3':volume})
  cases.append({'door':r['door'],'angle':angle,'hits':hits})
 c.Abertura=0;doc.recompute()
doc.save();report={'shelves':[{'name':o.Name,'dimensions_mm':[560,104,18],'position_mm':list(o.Placement.Base),'valid':o.Shape.isValid()} for o in shelves],
 'nominal_clear_height_each_mm':226,'side_front_rear_clearances_mm':2,'static_hits':static,'changed_cases':cases,
 'scope':'Duas prateleiras removíveis propostas, três níveis nominais226. Pinos/furação/carga não modelados nem liberados; não reserva tubulação por assumir rota hidráulica.'}
((Path(__file__).resolve().parent / 'Prateleiras_R12.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
# Add only new shelves to existing static previews; prior hardware poses stay intact.
views=json.loads(((Path(__file__).resolve().parent / 'Vistas_R12.json').resolve()).read_text(encoding='utf-8'))
for view in views:
 preview=App.getDocument(view['document'])
 for o in shelves:
  s=o.Shape.copy();s.Placement=App.Placement(App.Vector(-4040,-4840,0),App.Rotation()).multiply(o.getGlobalPlacement())
  copy=preview.addObject('Part::Feature','PrateleiraVistaR12');copy.Label=o.Label;copy.Shape=s;copy.ViewObject.ShapeColor=o.ViewObject.ShapeColor
 preview.recompute();preview.save();view['pieces']+=len(shelves)
((Path(__file__).resolve().parent / 'Vistas_R12.json').resolve()).write_text(json.dumps(views,ensure_ascii=False,indent=2),encoding='utf-8')
result=json.dumps({'static_hits':static,'changed_cases_with_hits':[r for r in cases if r['hits']],'shelf_count':len(shelves),'clear_height_nominal_mm':226},ensure_ascii=False)
