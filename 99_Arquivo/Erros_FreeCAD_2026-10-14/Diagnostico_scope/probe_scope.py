"""Read-only isolated scope warning probe; touch20 top AppParts only, no save."""
from pathlib import Path
import json,time,hashlib,traceback
import FreeCAD as App
root=Path(__file__).resolve().parent
source=(Path(__file__).resolve().parent / '../../../01_Projeto/Modelo_FreeCAD/02_Revisoes_e_estudos/Programa_R25_2026-10-14/Guedala_Park_R25_Programa_Corrigido.FCStd').resolve()
if not source.exists():
 choices=list(((Path(__file__).resolve().parent / '../../../01_Projeto/Modelo_FreeCAD/02_Revisoes_e_estudos/Programa_R25_2026-10-14').resolve()).glob('*.FCStd'));assert len(choices)==1;source=choices[0]
started=time.monotonic();report={'file':str(source),'sha256_before':hashlib.sha256(source.read_bytes()).hexdigest(),'gui_up':bool(App.GuiUp),'phase':'before_open','objects':[]}
d=None
def parent(o):
 p=o.getParentGeoFeatureGroup();return p.Name if p else None
def groups(o):return [x.Name for x in o.InList if 'Group' in x.PropertiesList and o in x.Group]
try:
 assert not App.GuiUp
 print('SCOPE_PHASE_BEFORE_OPEN',flush=True);d=App.openDocument(str(source));print('SCOPE_PHASE_AFTER_OPEN',flush=True)
 modules=[d.getObject('Modulo'+('%03d'%i if i else '')) for i in range(20)]
 report['doc_objects']=len(d.Objects)
 for o in modules:
  r={'name':o.Name,'label':o.Label,'type':o.TypeId,'geometric_parent':parent(o),'group_parents':groups(o),'parameter_links':[]}
  for p in ['PlanilhaDimensoes','FonteControle']:
   if p in o.PropertiesList:
    v=getattr(o,p);r['parameter_links'].append({'property':p,'property_type':o.getTypeIdOfProperty(p),'target':v.Name if v else None,'target_geometric_parent':parent(v) if v else None,'target_group_parents':groups(v) if v else [],'property_status':list(o.getPropertyStatus(p))})
  report['objects'].append(r)
 print('SCOPE_PHASE_TOUCH20',flush=True)
 for o in modules:o.touch()
 print('SCOPE_PHASE_RECOMPUTE',flush=True);rc=d.recompute();print('SCOPE_PHASE_AFTER_RECOMPUTE',rc,flush=True)
 report.update(phase='complete',recompute_result=rc,invalid=[o.Name for o in d.Objects if 'Invalid' in o.State],touched_after=[o.Name for o in modules if 'Touched' in o.State])
except Exception:report.update(phase='failed',error=traceback.format_exc());print('SCOPE_PROBE_ERROR',report['error'],flush=True)
finally:
 if d is not None:App.closeDocument(d.Name)
 report.update(sha256_after=hashlib.sha256(source.read_bytes()).hexdigest(),elapsed_s=time.monotonic()-started)
 report['source_unchanged']=report['sha256_before']==report['sha256_after']
 (root/'Probe_scope_R25.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
 print('SCOPE_PROBE_END',report['phase'],report['source_unchanged'],flush=True)
