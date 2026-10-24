import FreeCAD as A,json,pathlib
p=pathlib.Path(__file__).parent
d=A.openDocument(str(p/'FECHADA_400_GUI_INSPECAO.FCStd'))
o=d.getObject('Part__Feature')
for f in sorted(o.Shape.Faces,key=lambda f:f.Area,reverse=True)[:12]:
 print(round(f.Area,1),f.CenterOfMass,f.normalAt(0,0))
s=A.openDocument(str(p.parents[2]/'Avanco_pendencias_2026-10-21/Gavetas/Fixacao_simples_R04/Escritorio_fixacao_simples_R04_ESTUDO.FCStd'))
for n in ['Carcaca_470x248','Caixa_Gaveta008','Caixa_Gaveta009']:
 for o in s.getObject(n).Group:
  if hasattr(o,'Shape'):print(o.Name,o.Label,o.Shape.BoundBox)

