from pathlib import Path
import json
import FreeCAD as App
root=(Path(__file__).resolve().parent / '.').resolve()
doc=next(d for d in App.listDocuments().values() if d.FileName and Path(d.FileName).resolve()==(Path(__file__).resolve().parent / 'Guedala_Park_R12_Banheiro_Simples.FCStd').resolve())
data=json.loads(((Path(__file__).resolve().parent / 'Montagem_R12.json').resolve()).read_text(encoding='utf-8'))
def shape(o):
 s=o.Shape.copy();s.Placement=o.getGlobalPlacement();return s
def common(a,b):
 x,y=a.BoundBox,b.BoundBox
 if any(getattr(x,k+'Max')<=getattr(y,k+'Min')+1e-6 or getattr(y,k+'Max')<=getattr(x,k+'Min')+1e-6 for k in ['X','Y','Z']):return 0
 return a.common(b).Volume
cases=[];targets_report={};native110=[]
walls=doc.getObject('ParedesInteiras')
for r in data['doors']:
 module=doc.getObject(r['module']);room=next(p for p in module.InList if p.Name.startswith('Ambiente_'))
 targets=[o for o in room.Group if hasattr(o,'Shape') and o.TypeId!='App::Part']+list(walls.Group)
 targets_report[module.Name]=[{'name':o.Name,'label':o.Label} for o in targets]
 cached=[(o,shape(o)) for o in targets]
 fronts=[doc.getObject(r['front'])]+([doc.getObject(r['mirror'])] if 'mirror' in r else [])
 objects=fronts+[doc.getObject(b['body']) for h in r['hinges'] for b in h['bodies']]+[doc.getObject(h['plate']) for h in r['hinges']]
 control=doc.getObject(r['control']);control.CursoEstudo=110
 for angle in [0,30,60,86,110]:
  control.Abertura=angle;doc.recompute();hits=[]
  for o in objects:
   moving=shape(o)
   for target,ts in cached:
    v=common(moving,ts)
    if v>.1:hits.append({'moving':o.Name,'target':target.Name,'target_label':target.Label,'mm3':v})
  cases.append({'door':r['door'],'angle_deg':angle,'hits':hits})
  if angle==110:
   wood=[o for o in module.Group if o.TypeId=='Part::Box']
   adjacent=[doc.getObject(x['front']) for x in data['doors'] if x['door']!=r['door'] and x['module']==r['module']]+[doc.getObject(x['mirror']) for x in data['doors'] if x['door']!=r['door'] and x['module']==r['module'] and 'mirror' in x]
   nh=[]
   for o in objects:
    for target in wood+adjacent:
     v=common(shape(o),shape(target))
     if v>.1:nh.append({'moving':o.Name,'target':target.Name,'mm3':v})
   native110.append({'door':r['door'],'angle_deg':110,'hits':nh})
 control.Abertura=0;control.CursoEstudo=86;doc.recompute()
doc.save()
report={'cases':cases,'target_inventory':targets_report,'supplemental_native110':native110,
 'scope':'Quatro folhas R12 e ferragens contra paredes inteiras/volumes diretos do banheiro;110 é estudo adicional antes de decidir curso. Não valida medidas físicas, alavanca real, sifão, tubulação ou todas as poses da porta de entrada.'}
((Path(__file__).resolve().parent / 'Entorno_R12.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
result=json.dumps({'cases_with_hits':[r for r in cases if r['hits']],'native110_hits':[r for r in native110 if r['hits']],'targets_per_module':{k:len(v) for k,v in targets_report.items()}},ensure_ascii=False)
