import FreeCAD as App
from pathlib import Path
import json
root=(Path(__file__).resolve().parent / '.').resolve()
path=(Path(__file__).resolve().parent / 'Guedala_Park_R11_Apoios_Simples.FCStd').resolve()
docs=[d for d in App.listDocuments().values() if d.FileName and Path(d.FileName).resolve()==path]
assert len(docs)==1
d=docs[0];d.save();assert d.isSaved() and path.exists() and path.stat().st_size>1000000
App.closeDocument(d.Name);d=App.openDocument(str(path))
data=json.loads(((Path(__file__).resolve().parent / 'Montagem_R11.json').resolve()).read_text(encoding='utf-8'));checks=[]
for r in [data['doors'][0],data['doors'][-1]]:
 c=d.getObject(r['control']);c.Abertura=30;d.recompute();f=d.getObject(r['front'])
 checks.append({'door':r['door'],'input':str(c.Abertura),'valid_front':f.Shape.isValid(),'state':list(f.State),'placement':str(d.getObject(r['door']).Placement)})
 c.Abertura=0;d.recompute()
rest=[float(d.getObject(r['control']).Abertura) for r in data['doors']];assert all(a==0 for a in rest)
d.save();report={'file':str(path),'checks':checks,'resting_controls':rest,'saved':d.isSaved()}
((Path(__file__).resolve().parent / 'Reabertura_R11.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
result=report
