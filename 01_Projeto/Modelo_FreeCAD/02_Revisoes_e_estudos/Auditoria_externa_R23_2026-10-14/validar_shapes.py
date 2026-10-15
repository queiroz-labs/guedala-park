"""Validate participant BRep forms at saved pose only, no new poses/booleans/save."""
from pathlib import Path
import json,hashlib,time
import FreeCAD as App
root=(Path(__file__).resolve().parent / '.').resolve()
a=json.loads(((Path(__file__).resolve().parent / 'Auditoria_externa_R23.json').resolve()).read_text(encoding='utf-8'))
source=Path(a['file']);before=hashlib.sha256(source.read_bytes()).hexdigest();started=time.monotonic()
names=[r['name'] for r in a['manifest']['stationary_targets']]+a['manifest']['neighbor_fronts']
for r in a['manifest']['changed']:names+=r['hardware']
rows=json.loads(((Path(__file__).resolve().parent / '../Portas_opostas_R18_2026-10-14/Montagem_R18.json').resolve()).read_text(encoding='utf-8'))['doors']
for r in rows:names += [b['body'] for h in r['hinges'] for b in h['bodies']]+[h['plate'] for h in r['hinges']]
names+=['FerragemSimplesR04']+['FerragemSimplesR%03d'%i for i in range(1,24)]
names=list(dict.fromkeys(names))
d=App.openDocument(str(source));checks=[]
for n in names:
 o=d.getObject(n);s=o.Shape
 r={'name':n,'label':o.Label,'type':o.TypeId,'null':s.isNull(),'valid':s.isValid(),'solid_count':len(s.Solids),'volume_mm3':s.Volume}
 r['ok']=not r['null'] and r['valid'] and r['solid_count']>0 and r['volume_mm3']>0
 r['scope']='historical_additional_conservative' if n=='DivisorApoioVizinhaR03' else 'adopted_participant'
 checks.append(r)
report={'file':str(source),'gui_up':bool(App.GuiUp),'scope':'Saved pose0 only, no new poses or boolean computations', 'checks':checks,
 'controls':[{'control':r['control'],'opening_deg':float(d.getObject(r['control']).Abertura)} for r in rows]}
App.closeDocument(d.Name)
report.update(sha256_before=before,sha256_after=hashlib.sha256(source.read_bytes()).hexdigest(),elapsed_s=time.monotonic()-started)
report['source_unchanged']=report['sha256_before']==report['sha256_after'];report['all_ok']=all(x['ok'] for x in checks)
((Path(__file__).resolve().parent / 'Shape_validacao_R23.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('SHAPE_VALIDATION',len(checks),report['all_ok'],[x['name'] for x in checks if not x['ok']])
