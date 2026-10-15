from pathlib import Path
import json,shutil,hashlib,runpy
import FreeCAD as App,FreeCADGui as Gui
root=(Path(__file__).resolve().parent / '.').resolve();base=(Path(__file__).resolve().parent / '../..').resolve()
src=(Path(__file__).resolve().parent / '../Controles_R21_2026-10-14/Guedala_Park_R21_Controles_Organizados.FCStd').resolve();dst=(Path(__file__).resolve().parent / 'Guedala_Park_R22_Visibilidade_Atual.FCStd').resolve()
assert not dst.exists(),'Revisão existente; não reconstruir'
sha=hashlib.sha256(src.read_bytes()).hexdigest();shutil.copy2(src,dst);d=App.openDocument(str(dst));App.setActiveDocument(d.Name)
d.Label='Guedala Park — R22 — espelhado / peças atuais visíveis'
before={o.Name:{'parent':o.getParentGeoFeatureGroup().Name if o.getParentGeoFeatureGroup() else None,'placement':list(o.Placement.Matrix.A) if 'Placement' in o.PropertiesList else None,'expressions':[list(x) for x in o.ExpressionEngine] if 'ExpressionEngine' in o.PropertiesList else None} for o in d.Objects}
types={(o.Name,p):o.getTypeIdOfProperty(p) for o in d.Objects for p in ['PlanilhaDimensoes','FonteControle'] if p in o.PropertiesList}
modules=['Modulo'+('%03d'%i if i else '') for i in range(20)]+['PortaEntradaBanheiroR12']
report=runpy.run_path(str((Path(__file__).resolve().parent / '../Vistas_R21_2026-10-14/expor_geometria_atual.py').resolve()))['show_current'](d,modules)
d.recompute()
for n,r in before.items():
 o=d.getObject(n);assert (o.getParentGeoFeatureGroup().Name if o.getParentGeoFeatureGroup() else None)==r['parent']
 if r['placement'] is not None:assert max(abs(x-y) for x,y in zip(r['placement'],o.Placement.Matrix.A))<1e-9,n
 if r['expressions'] is not None:assert r['expressions']==[list(x) for x in o.ExpressionEngine],n
assert all(d.getObject(n).getTypeIdOfProperty(p)==t for (n,p),t in types.items())
assert hashlib.sha256(src.read_bytes()).hexdigest()==sha
assert not [o.Name for o in d.Objects if 'Invalid' in o.State]
Gui.activeDocument().activeView().viewAxonometric();Gui.updateGui();d.save()
report.update(file=str(dst),source=str(src),source_sha256=sha,objects_compared=len(before),parents_placements_expressions_parameter_types_unchanged=True,invalid=[],scope='Display correction only: expose current cabinet bodies in adopted modules; keep retired/historical objects and boolean operands hidden. No geometry, formulas, directions, course or hardware changes.')
((Path(__file__).resolve().parent / 'Visibilidade_R22.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
result={k:v for k,v in report.items() if k not in ['changed','excluded','boolean_operands_hidden']};result['display_changes']=len(report['changed'])
