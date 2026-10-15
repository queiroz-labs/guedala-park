from pathlib import Path
import json
import FreeCAD as App
root=(Path(__file__).resolve().parent / '.').resolve();path=(Path(__file__).resolve().parent / 'Guedala_Park_R12_Banheiro_Simples.FCStd').resolve()
docs=[d for d in App.listDocuments().values() if d.FileName and Path(d.FileName).resolve()==path];assert len(docs)==1
d=docs[0];data=json.loads(((Path(__file__).resolve().parent / 'Montagem_R12.json').resolve()).read_text(encoding='utf-8'))
for r in data['doors']:
 c=d.getObject(r['control'])
 for n in ['JuntaExternaProposta','JuntaCentralProposta']:c.setEditorMode(n,1)
d.save();assert d.isSaved() and path.exists() and path.stat().st_size>1000000
App.closeDocument(d.Name);d=App.openDocument(str(path));checks=[]
for r in [data['doors'][0],data['doors'][-1]]:
 c=d.getObject(r['control']);c.Abertura=30;d.recompute();front=d.getObject(r['front'])
 checks.append({'door':r['door'],'input_deg':float(c.Abertura),'front_valid':front.Shape.isValid(),'front_state':list(front.State),'mirror_valid':d.getObject(r['mirror']).Shape.isValid() if 'mirror' in r else None})
 c.Abertura=0;d.recompute()
e=d.getObject('PortaEntradaBanheiroR12');entry=[]
for angle in [0,90]:
 e.Abertura=angle;d.recompute();p=d.getObject('Peca075');s=p.Shape.copy();s.Placement=p.getGlobalPlacement();b=s.optimalBoundingBox();entry.append({'input_deg':angle,'bbox':[b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax],'valid':s.isValid()})
rest=[float(d.getObject(r['control']).Abertura) for r in data['doors']];assert all(v==0 for v in rest)
d.save();report={'file':str(path),'checks':checks,'entry_control':entry,'resting_cabinet_controls':rest,'resting_entry_deg':float(e.Abertura),'saved':d.isSaved()}
((Path(__file__).resolve().parent / 'Reabertura_R12.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');result=report
