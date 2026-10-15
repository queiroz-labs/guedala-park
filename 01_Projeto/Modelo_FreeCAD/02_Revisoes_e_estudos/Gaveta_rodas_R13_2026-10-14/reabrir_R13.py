from pathlib import Path
import json
import FreeCAD as App
root=(Path(__file__).resolve().parent / '.').resolve();path=(Path(__file__).resolve().parent / 'Guedala_Park_R13_Gaveta_Rodas.FCStd').resolve()
docs=[d for d in App.listDocuments().values() if d.FileName and Path(d.FileName).resolve()==path];assert len(docs)==1
d=docs[0];d.save();assert d.isSaved() and path.exists() and path.stat().st_size>1000000
App.closeDocument(d.Name);d=App.openDocument(str(path));r=json.loads(((Path(__file__).resolve().parent / 'Montagem_R13.json').resolve()).read_text(encoding='utf-8'));g=d.getObject(r['drawer']);g.Extensao=400;d.recompute()
checks=[{'name':n,'valid':d.getObject(n).Shape.isValid(),'state':list(d.getObject(n).State)} for n in r['moving_names']]
position=str(g.Placement);g.Extensao=0;d.recompute();d.save()
report={'file':str(path),'extension400_placement':position,'checks':checks,'resting_extension':float(g.Extensao),'resting_placement':str(g.Placement),'saved':d.isSaved()}
((Path(__file__).resolve().parent / 'Reabertura_R13.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');result={'saved':d.isSaved(),'checks':len(checks),'invalid':[r for r in checks if not r['valid']],'resting_extension':float(g.Extensao)}
