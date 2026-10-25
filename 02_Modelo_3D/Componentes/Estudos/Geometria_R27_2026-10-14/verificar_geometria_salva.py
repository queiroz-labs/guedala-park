"""Verify saved restoration and current native shape validity; no pose or collision repeat."""
from pathlib import Path
import json,hashlib,traceback
import FreeCAD as App
root=(Path(__file__).resolve().parent / '.').resolve();base=(Path(__file__).resolve().parent / '../..').resolve()
source=(Path(__file__).resolve().parent / 'Guedala_Park_R27_Geometria_Oficial.FCStd').resolve()
manifest=json.loads(((Path(__file__).resolve().parent / '../Auditoria_implantacao_R23_2026-10-14/Manifesto_implantacao_R23.json').resolve()).read_text(encoding='utf-8'))
change=json.loads(((Path(__file__).resolve().parent / 'Restauracao_R27.json').resolve()).read_text(encoding='utf-8'))
report={'file':str(source),'sha256_before':hashlib.sha256(source.read_bytes()).hexdigest(),'native_shape_invalid':[],'errors':[]}
d=None
try:
 assert not App.GuiUp
 d=App.openDocument(str(source))
 for row in change['restored']:
  o=d.getObject(row['name']);assert o.Shape.isValid()
  assert max(abs(a-b) for a,b in zip(o.Placement.toMatrix().A,row['new_local_matrix']))<1e-8
 names={r['name'] for r in manifest['items'] if r['adoption_scope']=='adopted_result'}
 names.difference_update(['Peca127','Peca128','Peca358','Peca107']);names.update(['PainelCabeceiraR25','PainelCabeceiraR001'])
 for n in sorted(names):
  o=d.getObject(n)
  if o.Shape.isNull() or not o.Shape.isValid():report['native_shape_invalid'].append({'name':n,'label':o.Label})
 report['selected_current_native_shapes']=len(names)
 report['invalid_objects']=[o.Name for o in d.Objects if 'Invalid' in o.State]
 assert not report['native_shape_invalid'] and not report['invalid_objects']
 report['loop_default_mm']=float(d.getObject('ControleLoopManutencaoR26').Afastamento);assert report['loop_default_mm']==0
 report['objects']=len(d.Objects);report['status']='saved_restoration_and_native_shape_health_verified'
except Exception:
 report['status']='failed';report['errors'].append(traceback.format_exc())
finally:
 if d is not None:App.closeDocument(d.Name)
 report['sha256_after']=hashlib.sha256(source.read_bytes()).hexdigest();report['source_unchanged']=report['sha256_before']==report['sha256_after']
 report['limits']='925 current native saved shapes, not transformed diagnostic copies or retired objects; no dynamic paths, booleans or internal STEP-contact certification. Existing physical/commercial limitations remain.'
 ((Path(__file__).resolve().parent / 'Verificacao_R27.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
 print('R27_HEALTH',report['status'],len(report['native_shape_invalid']),len(report['errors']),report['source_unchanged'])
