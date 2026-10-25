from pathlib import Path
import json
root=Path('C:\\Users\\Elias\\Documents\\PROJETOS\\Guedala park\\guedala-park\\02_Modelo_3D\\Componentes\\Estudos\\Canto_2026-10-13')
doc=FreeCAD.ActiveDocument
controls=next(o for o in doc.Objects if o.Name.startswith('ControleCanto'))
controls.set('B2','0 deg');controls.set('B3','0 deg');controls.set('B4','0 deg')
controls.set('B5','150 mm');controls.set('B8','40 mm')
A=next(o for o in doc.Objects if o.Label.startswith('Frente articulada A'))
B=next(o for o in doc.Objects if o.Label.startswith('Frente articulada B'))
A.ViewObject.ShapeColor=(.17,.47,.57);B.ViewObject.ShapeColor=(.81,.55,.25)
doc.recompute()
solids_bad=[o.Name for o in doc.Objects if hasattr(o,'Shape') and not o.Shape.isNull() and not o.Shape.isValid()]
doc.save()
filename=doc.FileName
FreeCAD.closeDocument(doc.Name)
doc=FreeCAD.openDocument(filename);doc.recompute()
invalid=[o.Name for o in doc.Objects if 'Invalid' in o.State]
controls=next(o for o in doc.Objects if o.Name.startswith('ControleCanto'))
controls.set('B2','23.75 deg');controls.set('B3','0 deg');controls.set('B4','24 deg');doc.recompute()
FreeCADGui.activeDocument().activeView().viewAxonometric();FreeCADGui.activeDocument().activeView().fitAll()
FreeCADGui.getMainWindow().show();FreeCADGui.getMainWindow().raise_();FreeCADGui.updateGui()
report={'reopened':True,'invalid_after_reopen':invalid,'invalid_solids_before_save':solids_bad,
        'saved_pose':'Fechada; faixa 150, recuo40, proposta',
        'display_pose':'Principal23.75, articulação0, vizinha24; vista não salva, para revisão',
        'source_R01_preserved':True}
(Path('C:\\Users\\Elias\\Documents\\PROJETOS\\Guedala park\\guedala-park\\02_Modelo_3D\\Componentes\\Estudos\\Canto_2026-10-13\\Reabertura.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
result=json.dumps(report,ensure_ascii=False)
