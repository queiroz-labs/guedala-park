"""Read-only, current module projections. No recompute, movement or save."""
import FreeCAD as App
import json, hashlib
from pathlib import Path
p=Path(__file__).resolve().parent
old=p.parent/'Modelo_FreeCAD/02_Revisoes_e_estudos/Detalhamento_documental_R28_2026-10-14/Base_pranchas_R28.json'
d=App.getDocument('Guedala_Park_R30_Juntas_Rotulos')
source=Path(d.FileName)
data=json.loads(old.read_text(encoding='utf-8'))
modules=[]
for prev in data['modules']:
    o=d.getObject(prev['object']); inv=o.getGlobalPlacement().inverse()
    pieces=[]
    # Hardware is described separately; projections do not imply drilling or full hardware inventory.
    for q in prev['pieces']:
        if q['kind']=='metal': continue
        n='FundoTanqueR29' if q['object']=='Peca354' else q['object']
        obj=d.getObject(n)
        assert obj and hasattr(obj,'Shape') and not obj.Shape.isNull(),n
        shape=obj.Shape.copy(); shape.Placement=inv.multiply(obj.getGlobalPlacement()); bb=shape.BoundBox
        lines=[]
        if q['kind']=='panel' and len(shape.Edges)<150:
            for edge in shape.Edges:
                pts=[v.Point for v in edge.Vertexes] if edge.Curve.__class__.__name__ in ('Line','LineSegment') else edge.discretize(Number=16)
                if len(pts)>1: lines.append([[v.x,v.y,v.z] for v in pts])
        pieces.append(dict(object=n,label=obj.Label,kind=q['kind'],local_bbox=[bb.XMin,bb.YMin,bb.ZMin,bb.XMax,bb.YMax,bb.ZMax],lines=lines))
    modules.append(dict(object=o.Name,label=o.Label,body_dimensions_mm={k:float(getattr(o,k).Value) for k in prev['body_dimensions_mm']},pieces=pieces,hinge_references=[]))
assert len(modules)==20
assert modules[6]['body_dimensions_mm']['Comprimento']==613
assert any(q['object']=='FundoTanqueR29' for q in modules[13]['pieces'])
result=dict(document=d.Name,file=str(source),sha256=hashlib.sha256(source.read_bytes()).hexdigest(),modules=modules,doors=data['doors'],method='R28 panel/reservation selection refreshed from live R30 geometry; Peca354 replaced by adopted FundoTanqueR29. Hardware omitted from projections and budgeted separately. No movements, recompute or source save.',objects=len(d.Objects))
(p/'Base_pranchas_R30.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
result={'modules':len(modules),'projected_objects':sum(len(m['pieces']) for m in modules),'sha256':result['sha256']}
