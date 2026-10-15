from pathlib import Path
import json
root=Path('C:\\Users\\Elias\\Documents\\PROJETOS\\Guedala park\\guedala-park\\01_Projeto\\Modelo_FreeCAD')
filename=Path('C:\\Users\\Elias\\Documents\\PROJETOS\\Guedala park\\guedala-park\\01_Projeto\\Modelo_FreeCAD\\03_Recursos\\output\\Guedala_Park_R01.FCStd')
if FreeCAD.ActiveDocument:
    FreeCAD.closeDocument(FreeCAD.ActiveDocument.Name)
doc=FreeCAD.openDocument(str(filename))
doc.recompute()
invalid=[o.Name for o in doc.Objects if 'Invalid' in o.State]
FreeCADGui.activeDocument().activeView().viewAxonometric()
FreeCADGui.activeDocument().activeView().fitAll()
FreeCADGui.getMainWindow().show()
FreeCADGui.getMainWindow().raise_()
FreeCADGui.updateGui()
record={'file_reopened':str(filename),'objects':len(doc.Objects),'invalid_objects_after_reopen':invalid,
        'version':FreeCAD.Version()[:3],'mcp_live_call':True}
(Path('C:\\Users\\Elias\\Documents\\PROJETOS\\Guedala park\\guedala-park\\01_Projeto\\Modelo_FreeCAD\\03_Recursos\\output\\Reabertura.json')).write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
result=json.dumps(record,ensure_ascii=False)
