from pathlib import Path
import json
import FreeCAD as App
root=(Path(__file__).resolve().parent / '.').resolve()
doc=next(d for d in App.listDocuments().values() if d.FileName and Path(d.FileName).resolve()==(Path(__file__).resolve().parent / 'Guedala_Park_R11_Apoios_Simples.FCStd').resolve())
old=next(d for d in App.listDocuments().values() if d.FileName and Path(d.FileName).resolve()==(Path(__file__).resolve().parent / '../Dobradicas_R10_2026-10-14/Guedala_Park_R10_Dobradicas_Comuns.FCStd').resolve())
data=json.loads(((Path(__file__).resolve().parent / 'Montagem_R11.json').resolve()).read_text(encoding='utf-8'))
def shape(o):
 s=o.Shape.copy();s.Placement=o.getGlobalPlacement();return s
def common(a,b):
 x,y=a.BoundBox,b.BoundBox
 if any(getattr(x,k+'Max')<=getattr(y,k+'Min')+1e-6 or getattr(y,k+'Max')<=getattr(x,k+'Min')+1e-6 for k in ['X','Y','Z']):return 0
 return a.common(b).Volume
cases=[];targets_report={}
walls=doc.getObject('ParedesInteiras')
for r in data['doors']:
 module=doc.getObject(r['module']);room=next(p for p in module.InList if p.Name.startswith('Ambiente_'))
 targets=[o for o in room.Group if hasattr(o,'Shape') and o.TypeId!='App::Part']+list(walls.Group)
 targets_report[module.Name]=[{'name':o.Name,'label':o.Label} for o in targets]
 objects=[doc.getObject(r['front'])]+[doc.getObject(b['body']) for h in r['hinges'] for b in h['bodies']]+[doc.getObject(h['plate']) for h in r['hinges']]
 control=doc.getObject(r['control'])
 for angle in [0,30,60,86]:
  control.Abertura=angle;doc.recompute();hits=[]
  for o in objects:
   for target in targets:
    v=common(shape(o),shape(target))
    if v>.1:hits.append({'moving':o.Name,'target':target.Name,'target_label':target.Label,'mm3':v})
  cases.append({'door':r['door'],'angle_deg':angle,'hits':hits})
 control.Abertura=0;doc.recompute()
supports=[doc.getObject(r['name']) for r in data['supports']];static=[]
for o in supports:
 module=next(p for p in o.InList if p.TypeId=='App::Part')
 targets=[p for p in module.Group if p.TypeId=='Part::Box' and p!=o]
 if module.Name=='Modulo003':targets.append(doc.getObject('DivisorApoioVizinhaR03'))
 for p in targets:
  v=common(shape(o),shape(p))
  if v>.1:static.append({'support':o.Name,'target':p.Name,'mm3':v})
preserved=[]
for n in ['VizinhaComCanecosR03','DivisorApoioVizinhaR03','FaixaFixaEstudo']:
 a,b=shape(old.getObject(n)),shape(doc.getObject(n));ba,bb=a.optimalBoundingBox(),b.optimalBoundingBox()
 delta=max(abs(getattr(ba,k)-getattr(bb,k)) for k in ['XMin','YMin','ZMin','XMax','YMax','ZMax'])
 preserved.append({'object':n,'bbox_delta_mm':delta,'volume_delta_mm3':abs(a.Volume-b.Volume)})
doc.save()
report={'cases':cases,'target_inventory':targets_report,'support_wood_intersections':static,'preserved_neighbor_and_strip':preserved,
 'scope':'Somente folhas/ferragens novas R11 contra paredes inteiras e volumes diretos de seu ambiente. Não inventário completo dos demais módulos, pessoas, tolerâncias ou cargas.'}
((Path(__file__).resolve().parent / 'Entorno_R11.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
result=json.dumps({'cases_with_hits':[r for r in cases if r['hits']],'support_hits':static,'preserved':preserved,'targets_per_module':{k:len(v) for k,v in targets_report.items()}},ensure_ascii=False)
