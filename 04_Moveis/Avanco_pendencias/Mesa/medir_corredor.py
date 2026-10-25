import FreeCAD as A, Part, pathlib,json,hashlib
out=pathlib.Path(__file__).parent
src=out.parents[1]/'Modelo_FreeCAD/01_Atual/Consolidacao_R42_2026-10-22/Guedala_Park_R42_Consolidado.FCStd'
d=A.openDocument(str(src));rows=[]
for o in d.Objects:
 if not hasattr(o,'Shape') or not hasattr(o,'getGlobalPlacement') or o.Shape.isNull():continue
 s=o.Shape.copy();s.Placement=o.getGlobalPlacement();b=s.BoundBox
 if b.XMax<1485 or b.XMin>3600 or b.YMax<3800 or b.YMin>5500 or b.ZMin>2100 or b.ZMax<1:continue
 rows.append({'name':o.Name,'label':o.Label,'bbox':[b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax],'visible':getattr(o,'Visibility',None),'parents':[(p.Name,p.Label,getattr(p,'Visibility',None)) for p in o.InList]})
(out/'obstaculos_candidatos.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(rows,ensure_ascii=False))

