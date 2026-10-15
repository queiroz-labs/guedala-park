"""Bounded affected-shape equivalence check; official profiles against old spline copies."""
from pathlib import Path
import json,time,traceback
import FreeCAD as App,Part
root=(Path(__file__).resolve().parent / '.').resolve();base=(Path(__file__).resolve().parent / '../..').resolve()
out={'rows':[],'errors':[],'sampling_only':True};docs=[];start=time.monotonic()
try:
 src=App.openDocument(str((Path(__file__).resolve().parent / '../Montagem_R07_2026-10-14/Fonte_G2_BlUM.FCStd').resolve()));docs.append(src)
 d=App.openDocument(str((Path(__file__).resolve().parent / '../Manutencao_R26_2026-10-14/Guedala_Park_R26_Manutencao_Simples.FCStd').resolve()));docs.append(d)
 mapping=App.Placement(App.Vector(600,18,3.5),App.Rotation(App.Vector(1,0,0),90))
 for name in ['MontagemG2R007','MontagemG2R014']:
  o=d.getObject(name);q=src.getObject(o.Fonte.split(' / ')[-1]);old=o.Shape.copy()
  new=q.Shape.copy();new.Placement=mapping.multiply(q.getGlobalPlacement())
  assert len(old.Edges)==len(new.Edges) and len(old.Faces)==len(new.Faces)
  row={'name':name,'old_edges':len(old.Edges),'old_faces':len(old.Faces),'edge_samples':0,'max_edge_sample_distance_mm':0,'face_samples':0,'max_face_sample_distance_mm':0,'native_new_valid':new.isValid()}
  for a,b in zip(old.Edges,new.Edges):
   assert time.monotonic()-start<90
   for fraction in [.25,.5,.75]:
    for source,target in [(a,b),(b,a)]:
     p=source.valueAt(source.FirstParameter+fraction*(source.LastParameter-source.FirstParameter))
     delta=target.distToShape(Part.Vertex(p))[0]
     row['edge_samples']+=1;row['max_edge_sample_distance_mm']=max(row['max_edge_sample_distance_mm'],delta)
  for a,b in zip(old.Faces,new.Faces):
   assert time.monotonic()-start<90
   for source,target in [(a,b),(b,a)]:
    u0,u1,v0,v1=source.ParameterRange
    for fu,fv in [(.25,.25),(.5,.5),(.75,.75)]:
     p=source.valueAt(u0+fu*(u1-u0),v0+fv*(v1-v0))
     if not source.isInside(p,1e-7,True):continue
     delta=target.distToShape(Part.Vertex(p))[0]
     row['face_samples']+=1;row['max_face_sample_distance_mm']=max(row['max_face_sample_distance_mm'],delta)
  out['rows'].append(row)
except Exception:out['errors'].append(traceback.format_exc())
finally:
 for d in reversed(docs):App.closeDocument(d.Name)
 out['elapsed_s']=time.monotonic()-start
 ((Path(__file__).resolve().parent / 'Equivalencia_perfis_G2.json').resolve()).write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
 print('PROFILE_SAMPLING',out['rows'],len(out['errors']))
