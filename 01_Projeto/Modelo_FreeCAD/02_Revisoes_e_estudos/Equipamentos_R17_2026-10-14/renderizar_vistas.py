from pathlib import Path
import json
import FreeCAD as App,FreeCADGui as Gui
root=(Path(__file__).resolve().parent / '.').resolve();out=[]
for r in json.loads(((Path(__file__).resolve().parent / 'Vistas_R17.json').resolve()).read_text(encoding='utf-8')):
 d=App.getDocument(r['document']);App.setActiveDocument(d.Name);v=Gui.getDocument(d.Name).activeView();rot=v.getCameraOrientation();inv=rot.inverted();pts=[]
 for o in d.Objects:
  if hasattr(o,'Shape') and not o.Shape.isNull():
   b=o.Shape.optimalBoundingBox();pts.extend(App.Vector(x,y,z) for x in [b.XMin,b.XMax] for y in [b.YMin,b.YMax] for z in [b.ZMin,b.ZMax])
 proj=[inv.multVec(q) for q in pts];cx=(min(q.x for q in proj)+max(q.x for q in proj))/2;cy=(min(q.y for q in proj)+max(q.y for q in proj))/2;cz=(min(q.z for q in proj)+max(q.z for q in proj))/2
 center=rot.multVec(App.Vector(cx,cy,cz));height=max(max(q.y for q in proj)-min(q.y for q in proj),(max(q.x for q in proj)-min(q.x for q in proj))/1.6)*1.25
 cam=v.getCameraNode();pos=center+rot.multVec(App.Vector(0,0,5000));cam.position.setValue(pos.x,pos.y,pos.z);cam.height.setValue(height);cam.nearDistance.setValue(1);cam.farDistance.setValue(20000);cam.focalDistance.setValue(5000)
 Gui.updateGui();png=root/(r['label']+'_R17.png');v.saveImage(str(png),1600,1000,'White');d.save();out.append(str(png))
result=out
