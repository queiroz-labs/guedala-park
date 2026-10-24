import FreeCAD as A, json, pathlib, hashlib
root=pathlib.Path(__file__).resolve().parent;base=root.parents[1]
src=base/'Modelo_FreeCAD/01_Atual/Consolidacao_R42_2026-10-22/Guedala_Park_R42_Consolidado.FCStd'
d=A.openDocument(str(src));names=['Gaveta','Gaveta001','Gaveta002','Gaveta003','Gaveta004','Gaveta005','Gaveta006','Gaveta008','Gaveta009']
def info(o):
 r={'name':o.Name,'label':o.Label,'type':o.TypeId,'parents':[(x.Name,x.Label) for x in o.InList],'children':[(x.Name,x.Label) for x in o.OutList],'placement':str(o.getGlobalPlacement()) if hasattr(o,'getGlobalPlacement') else '', 'props':{p:str(getattr(o,p)) for p in o.PropertiesList if any(t in p.lower() for t in ['profund','largura','altura','vao','curso','ferrag','extensao','local','comprimento']) and not p.startswith('_')}}
 if hasattr(o,'Shape') and not o.Shape.isNull():
  s=o.Shape.copy()
  if hasattr(o,'getGlobalPlacement'):s.Placement=o.getGlobalPlacement()
  b=s.BoundBox;r['bbox_world']=[b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]
 return r
rows={};focus={}
for n in names:
 o=d.getObject(n);focus[n]=info(o)
 targets=set([o]+o.OutList+o.InList)
 for p in o.InList:
  targets.update(p.OutList)
  for pp in p.InList:targets.update(pp.OutList)
 for t in targets:
  rows[t.Name]=info(t)
  if t.Name.startswith(('Modulo','Gaveta','MontagemG2')):
   for c in t.OutList:rows[c.Name]=info(c)
out={'source':str(src),'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'focus':focus,'objects':rows}
(root/'Geometria_extraida_R42.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(focus,ensure_ascii=True))
