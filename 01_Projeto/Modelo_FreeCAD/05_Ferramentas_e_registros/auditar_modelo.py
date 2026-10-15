from pathlib import Path
import json
import math
root=Path('C:\\Users\\Elias\\Documents\\PROJETOS\\Guedala park\\guedala-park\\01_Projeto\\Modelo_FreeCAD')
doc=FreeCAD.ActiveDocument
modules=[o for o in doc.Objects if hasattr(o,'PlanilhaDimensoes')]
def descendants(parent):
    for o in parent.Group:
        if o.TypeId=='App::Part':
            yield from descendants(o)
        elif hasattr(o,'Shape'):
            yield o
def world_shape(o):
    s=o.Shape.copy()
    s.Placement=o.getGlobalPlacement()
    return s
collisions=[]
for m in modules:
    solids=[]
    for o in descendants(m):
        if o.Label.startswith('Suporte geométrico') or getattr(o,'TipoPeca','')=='Reserva técnica':
            continue
        solids.append((o,world_shape(o)))
    for i,(a,sa) in enumerate(solids):
        for b,sb in solids[i+1:]:
            ba,bb=sa.BoundBox,sb.BoundBox
            if not (ba.XMin < bb.XMax-.001 and ba.XMax > bb.XMin+.001 and
                    ba.YMin < bb.YMax-.001 and ba.YMax > bb.YMin+.001 and
                    ba.ZMin < bb.ZMax-.001 and ba.ZMax > bb.ZMin+.001):
                continue
            volume=sa.common(sb).Volume
            if volume>1:
                collisions.append({'module':m.Label,'a':a.Label,'b':b.Label,'overlap_mm3':round(volume,3)})

base=next(m for m in modules if m.Label.startswith('Gaveteiro G1'))
sheet=base.PlanilhaDimensoes
piece=next(o for o in base.Group if o.Label.startswith('Lateral direita'))
old=float(piece.Placement.Base.x)
sheet.set('B2','629 mm');doc.recompute()
new=float(piece.Placement.Base.x)
sheet.set('B2','619 mm');doc.recompute()
parametric=(abs(new-old-10)<1e-7 and abs(float(piece.Placement.Base.x)-old)<1e-7)
draw=next(o for o in doc.Objects if o.Label=='Gaveta escritório 1')
draw.Extensao=400;doc.recompute()
drawer=(abs(draw.Placement.Base.y+400)<1e-7)
draw.Extensao=0;doc.recompute()
door=next(o for o in doc.Objects if o.TypeId=='App::Part' and o.Label.startswith('Porta 1') and hasattr(o,'Abertura'))
door.Abertura=30;doc.recompute()
rotation=(abs(math.degrees(door.Placement.Rotation.Angle)-30)<1e-6)
door.Abertura=0;doc.recompute()
report={'static_module_intersections':collisions,'parametric_dimension_edit':parametric,
        'office_400mm_drawer_motion':drawer,'ideal_30deg_door_rotation':rotation,
        'scope':'Interferências de peças fechadas dentro de cada módulo. Não valida a cinemática de ferragens nem movimentos simultâneos.'}
(Path('C:\\Users\\Elias\\Documents\\PROJETOS\\Guedala park\\guedala-park\\01_Projeto\\Modelo_FreeCAD\\03_Recursos\\output\\Auditoria_CAD.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
result=json.dumps(report,ensure_ascii=False)
