from pathlib import Path
import json
import math
import Import
import Part
import FreeCAD as App
import FreeCADGui as Gui

root = (Path(__file__).resolve().parent / '.').resolve()
root.mkdir(parents=True, exist_ok=True)
base = (Path(__file__).resolve().parent / '../Blum_oficial').resolve()
name='Blum_Inspecao_Articulacoes'
if name in App.listDocuments(): App.closeDocument(name)
doc=App.newDocument(name)
report={}
palette=[(.84,.24,.20),(.20,.55,.83),(.30,.72,.43),(.91,.68,.19),(.63,.32,.81),(.12,.70,.69),(.78,.48,.30)]
for family in ['71T7550','79T8500']:
    before={o.Name for o in doc.Objects}
    source=next((base/family).glob('*.step'))
    Import.insert(str(source),doc.Name);doc.recompute()
    leaves=[o for o in doc.Objects if o.Name not in before and o.TypeId=='Part::Feature' and len(o.Shape.Solids)==1]
    parts=[]
    for index,o in enumerate(leaves):
        o.ViewObject.ShapeColor=palette[index%len(palette)]
        cylinders=[]
        for fi,face in enumerate(o.Shape.Faces):
            s=face.Surface
            if isinstance(s,Part.Cylinder):
                c=s.Center; a=s.Axis; box=face.BoundBox
                if abs(a.y)>.99 and s.Radius<=7.5:
                    cylinders.append({'face':fi+1,'radius':s.Radius,'center':[c.x,c.y,c.z],
                        'axis':[a.x,a.y,a.z],'area':face.Area,
                        'bounds':[box.XMin,box.YMin,box.ZMin,box.XMax,box.YMax,box.ZMax]})
        parts.append({'name':o.Name,'label':o.Label,'cylinders_Y':cylinders,'volume':o.Shape.Volume})
    report[family]={'source':str(source),'parts':parts}
    for o in doc.Objects:
        if o.TypeId=='App::Part': o.ViewObject.Visibility=any(p in o.Group for p in leaves)
    for o in leaves: o.ViewObject.Visibility=True
    Gui.activeDocument().activeView().viewRear()
    Gui.activeDocument().activeView().fitAll()
    Gui.updateGui()
    Gui.activeDocument().activeView().saveImage(str(root/(family+'_planar.png')),1600,1000,'White')
    for o in leaves: o.ViewObject.Visibility=False
doc.saveAs(str((Path(__file__).resolve().parent / 'Inspecao_Articulacoes.FCStd').resolve()))
((Path(__file__).resolve().parent / 'Geometria_articulacoes.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
result=json.dumps({f:[{'name':p['name'],'label':p['label'],'cylinders_Y':len(p['cylinders_Y'])} for p in v['parts']] for f,v in report.items()})
