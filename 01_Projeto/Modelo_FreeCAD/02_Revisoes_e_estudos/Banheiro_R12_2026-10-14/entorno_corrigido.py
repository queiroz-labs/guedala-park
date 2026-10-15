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
entry=doc.getObject('PortaEntradaBanheiroR12');entry.Abertura=0;doc.recompute()
room=next(p for p in doc.getObject('Modulo018').InList if p.Name.startswith('Ambiente_'))
targets=[o for o in room.Group if hasattr(o,'Shape') and o.TypeId!='App::Part']+list(doc.getObject('ParedesInteiras').Group)+[doc.getObject('Peca075')]
cached=[(o,shape(o)) for o in targets];cases=[]
for r in data['doors']:
 objects=[doc.getObject(r['front'])]+([doc.getObject(r['mirror'])] if 'mirror' in r else [])+[doc.getObject(b['body']) for h in r['hinges'] for b in h['bodies']]+[doc.getObject(h['plate']) for h in r['hinges']]
 control=doc.getObject(r['control'])
 for angle in [0,30,60,86]:
  control.Abertura=angle;doc.recompute();hits=[]
  for o in objects:
   for target,ts in cached:
    v=common(shape(o),ts)
    if v>.1:hits.append({'moving':o.Name,'target':target.Name,'target_label':target.Label,'mm3':v})
  cases.append({'door':r['door'],'angle_deg':angle,'entry_study_deg':0,'hits':hits})
 control.Abertura=0;doc.recompute()
entry.Abertura=90;doc.recompute();doc.save()
report={'cases':cases,'targets':[{'name':o.Name,'label':o.Label} for o in targets],
 'scope':'R12 com luzes frontais fixas propostas acima/abaixo e porta de entrada ideal fechada. Curso86 de estudo não comprova batente. Preservada pose original de entrada90 e armários0 após teste; não libera hidráulica, fotometria ou cotas de porta real.'}
((Path(__file__).resolve().parent / 'Entorno_corrigido_R12.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
result=json.dumps({'cases_with_hits':[r for r in cases if r['hits']],'target_count':len(targets),'resting_entry_input':float(entry.Abertura)},ensure_ascii=False)
