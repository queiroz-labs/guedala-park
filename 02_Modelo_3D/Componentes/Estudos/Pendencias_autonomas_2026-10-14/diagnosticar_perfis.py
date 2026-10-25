"""Compare only two invalid baked G2 profiles with their official source; never save CAD."""
from pathlib import Path
import json,traceback,time,hashlib
import FreeCAD as App
root=(Path(__file__).resolve().parent / '.').resolve();base=(Path(__file__).resolve().parent / '../..').resolve()
source=(Path(__file__).resolve().parent / '../Montagem_R07_2026-10-14/Fonte_G2_BlUM.FCStd').resolve()
current=(Path(__file__).resolve().parent / '../Manutencao_R26_2026-10-14/Guedala_Park_R26_Manutencao_Simples.FCStd').resolve()
out={'source':str(source),'current':str(current),'sha256_before':hashlib.sha256(current.read_bytes()).hexdigest(),'rows':[],'errors':[]}
def bb(s):
 b=s.optimalBoundingBox();return [b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]
docs=[]
try:
 assert not App.GuiUp
 src=App.openDocument(str(source));docs.append(src)
 d=App.openDocument(str(current));docs.append(d)
 placement=App.Placement(App.Vector(600,18,3.5),App.Rotation(App.Vector(1,0,0),90))
 for name in ['MontagemG2R007','MontagemG2R014']:
  obj=d.getObject(name);source_name=obj.Fonte.split(' / ')[-1];o=src.getObject(source_name)
  old=obj.Shape.copy();old.Placement=obj.Placement
  mapped=o.Shape.copy();mapped.Placement=placement.multiply(o.getGlobalPlacement())
  baked=o.Shape.copy();baked.transformShape(placement.multiply(o.getGlobalPlacement()).toMatrix(),True)
  r={'name':name,'source_name':source_name,'source_native_valid':o.Shape.isValid(),'old_native_valid':obj.Shape.isValid(),
    'source_vertices':len(o.Shape.Vertexes),'old_vertices':len(old.Vertexes),'mapped_vertices':len(mapped.Vertexes),
    'old_local_optimal_bbox':bb(old),'mapped_local_optimal_bbox':bb(mapped),'mapped_valid':mapped.isValid(),'mapped_placement':list(mapped.Placement.toMatrix().A),
    'transformShape_valid':baked.isValid(),'transformShape_bbox':bb(baked),
    'volumes_mm3':{'old':old.Volume,'mapped':mapped.Volume,'transformShape':baked.Volume}}
  if len(old.Vertexes)==len(mapped.Vertexes):
   r['maximum_corresponding_vertex_distance_mm']=max((a.Point-b.Point).Length for a,b in zip(old.Vertexes,mapped.Vertexes))
  r['mapped_bbox_max_difference_mm']=max(abs(a-b) for a,b in zip(bb(old),bb(mapped)))
  r['old_state']=list(obj.State)
  out['rows'].append(r)
except Exception:out['errors'].append(traceback.format_exc())
finally:
 for d in reversed(docs):App.closeDocument(d.Name)
 out['sha256_after']=hashlib.sha256(current.read_bytes()).hexdigest();out['source_unchanged']=out['sha256_before']==out['sha256_after']
 out['limits']='Pure source/representation diagnosis; no shape repair, tolerance changes, material removal, collision rerun or CAD save.'
 ((Path(__file__).resolve().parent / 'Diagnostico_perfis_G2.json').resolve()).write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
 print('PROFILE_DIAG',[(r['name'],r['source_native_valid'],r['mapped_valid'],r['transformShape_valid']) for r in out['rows']],len(out['errors']))
