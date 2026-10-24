import FreeCAD as A,pathlib
p=pathlib.Path(__file__).parent
for st in ['FECHADA','ABERTA']:
 d=A.openDocument(str(p/(st+'_400_GUI_INSPECAO.FCStd')))
 print(st)
 for o in d.Objects:
  if hasattr(o,'Shape'):print(o.Name,'local',o.Placement,'global',o.getGlobalPlacement(),'shape',o.Shape.Placement,'BB',o.Shape.BoundBox)
