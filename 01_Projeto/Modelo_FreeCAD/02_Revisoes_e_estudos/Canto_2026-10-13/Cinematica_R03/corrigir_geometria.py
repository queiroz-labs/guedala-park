from pathlib import Path
import json
import FreeCAD as App
root=(Path(__file__).resolve().parent / '.').resolve()
doc=next(d for d in App.listDocuments().values() if d.FileName and Path(d.FileName).name=='Guedala_Park_R03_Ferragens_Canto.FCStd')
doc.save()
inspection=App.getDocument('Blum_Inspecao_Articulacoes')
count=0
for o in doc.Objects:
    source=None;angle=90
    if o.Label.startswith('71T7550 - corpo '):
        i=o.IndiceCorpo;source=inspection.getObject('Part__Feature'+('' if i==0 else str(i).zfill(3)))
    elif o.Label.startswith('79T8500 - corpo '):
        source=inspection.getObject('Part__Feature'+str(7+o.IndiceCorpo).zfill(3));angle=-90
    elif o.Label.startswith('173H7100 - calco 0 mm'):source=inspection.getObject('Part__Feature011')
    elif o.Label.startswith('173H7100 - calco sobre B'):source=inspection.getObject('Part__Feature011');angle=-90
    elif o.Label.startswith('70T7553.09 - montagem'):source=inspection.getObject('Part__Feature012')
    if source:
        shape=source.Shape.transformGeometry(source.Shape.Placement.toMatrix());shape.Placement=App.Placement()
        shape=shape.transformGeometry(App.Rotation(App.Vector(1,0,0),angle).toMatrix())
        o.Shape=shape;o.Placement=App.Placement();count+=1
doc.recompute();doc.save()
result=json.dumps({'normalized_shape_frames':count,'invalid':[o.Name for o in doc.Objects if 'Invalid' in o.State]})
