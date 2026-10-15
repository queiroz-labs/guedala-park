from pathlib import Path
import json,hashlib,traceback
import FreeCAD as App
root=(Path(__file__).resolve().parent / '.').resolve()
source=(Path(__file__).resolve().parent / 'Guedala_Park_R28_Folga_Teto_Proposta.FCStd').resolve()
audit=json.loads(((Path(__file__).resolve().parent / 'Conferencia_folga_R28.json').resolve()).read_text(encoding='utf-8'))
report={'file':str(source),'sha256_before':hashlib.sha256(source.read_bytes()).hexdigest(),'errors':[]};d=None
def bb(s):
 b=s.BoundBox;return [b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]
try:
 assert not App.GuiUp
 d=App.openDocument(str(source));m=d.getObject('Modulo016');s=m.Shape.copy();s.Placement=m.getGlobalPlacement()
 assert abs(m.Placement.Base.z-1900)<1e-8
 assert max(abs(a-b) for a,b in zip(bb(s),audit['after_module_bbox_source_mm']))<1e-6
 for row in audit['parts']:
  o=d.getObject(row['name']);t=o.Shape.copy();t.Placement=o.getGlobalPlacement()
  assert max(abs(a-b) for a,b in zip(bb(t),row['after_bbox_source_mm']))<1e-5
 link=next(o for o in d.Objects if o.TypeId=='App::Link' and o.Name.startswith('EspelhoPecaR') and o.LinkedObject==m)
 bounds=bb(link.Shape);raw=bb(s);expected=[7400-raw[3],raw[1],raw[2],7400-raw[0],raw[4],raw[5]]
 assert max(abs(a-b) for a,b in zip(bounds,expected))<1e-6
 report.update(status='saved_gap_and_61_global_positions_verified',module=m.Name,link=link.Name,source_bbox_mm=raw,current_bbox_mm=bounds,
  height_mm=float(m.Altura),proposed_gap_mm=float(m.FolgaTetoProposta),parts_checked=len(audit['parts']),objects=len(d.Objects),
  invalid=[o.Name for o in d.Objects if 'Invalid' in o.State])
 assert not report['invalid']
except Exception:report.update(status='failed');report['errors'].append(traceback.format_exc())
finally:
 if d is not None:App.closeDocument(d.Name)
 report['sha256_after']=hashlib.sha256(source.read_bytes()).hexdigest();report['source_unchanged']=report['sha256_before']==report['sha256_after']
 ((Path(__file__).resolve().parent / 'Verificacao_R28.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
 print('R28_GAP',report['status'],len(report['errors']),report['source_unchanged'])
