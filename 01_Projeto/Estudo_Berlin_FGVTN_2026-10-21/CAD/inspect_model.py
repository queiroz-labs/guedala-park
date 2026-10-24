import FreeCAD as A, Part, json, pathlib, hashlib
root=pathlib.Path(__file__).parent
src=root.parent.parent/'Modelo_FreeCAD/01_Atual/Cesto_R41_2026-10-20/Guedala_Park_R41_Estudo_Frente500.FCStd'
doc=A.openDocument(str(src))
rows=[]
for o in doc.Objects:
    if any(w in o.Label.lower() for w in ['mesa','cadeira','sof','geladeira','ib6','banco','encosto','almofada']):
        row={'name':o.Name,'label':o.Label,'type':o.TypeId,'parents':[p.Name for p in o.InList],'properties':{p:str(getattr(o,p)) for p in o.PropertiesList if p in ['Visibility','Extensao','Comprimento','Largura','Altura','LocalX','LocalY','LocalZ']}}
        if hasattr(o,'Shape') and not o.Shape.isNull():
            s=o.Shape.copy();s.Placement=o.getGlobalPlacement();b=s.BoundBox
            row['bbox']=[b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]
        rows.append(row)
(root/'inspection.json').write_text(json.dumps({'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'rows':rows},ensure_ascii=False,indent=2),encoding='utf-8')
print('objects',len(doc.Objects),'relevant',len(rows))
