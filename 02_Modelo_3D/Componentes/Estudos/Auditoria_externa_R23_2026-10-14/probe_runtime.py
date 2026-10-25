from pathlib import Path
import json, time, traceback
root=(Path(__file__).resolve().parent / '.').resolve()
started=time.monotonic()
report={'started':time.time(),'scope':'Isolated console runtime feasibility only; no GUI/document save'}
try:
 import FreeCAD as App
 import Part
 report.update(version=list(App.Version()), gui_up=bool(App.GuiUp))
 assert not App.GuiUp
 a=Part.makeBox(2,2,2)
 b=Part.makeBox(2,2,2,App.Vector(1,1,1))
 report['probe_common_volume_mm3']=a.common(b).Volume
 source=json.loads(((Path(__file__).resolve().parent / '../Rotulos_R23_2026-10-14/Rotulos_R23.json').resolve()).read_text(encoding='utf-8'))['file']
 d=App.openDocument(source)
 report.update(file=source,objects=len(d.Objects),sample_shape_valid=d.getObject('FerragemComumR11').Shape.isValid(),sample_global_matrix=d.getObject('FerragemComumR11').getGlobalPlacement().toMatrix().A)
 App.closeDocument(d.Name)
 report['ok']=True
except Exception:
 report.update(ok=False,error=traceback.format_exc())
report['elapsed_s']=time.monotonic()-started
((Path(__file__).resolve().parent / 'Viabilidade_runtime.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('PROBE_RESULT',json.dumps(report,ensure_ascii=False))
