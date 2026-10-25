from pathlib import Path
import json
import FreeCAD as App,FreeCADGui as Gui
root=(Path(__file__).resolve().parent / '.').resolve()
records=json.loads(((Path(__file__).resolve().parent / 'Vistas_R14.json').resolve()).read_text(encoding='utf-8'))
for record in records[:1]:
 d=App.getDocument(record['document']);App.setActiveDocument(d.Name);v=Gui.getDocument(d.Name).activeView();rot=v.getCameraOrientation();inv=rot.inverted();pts=[]
 for o in d.Objects:
  if 'Shape' in o.PropertiesList:
   b=o.Shape.optimalBoundingBox();pts.extend(App.Vector(x,y,z) for x in [b.XMin,b.XMax] for y in [b.YMin,b.YMax] for z in [b.ZMin,b.ZMax])
 center=App.Vector(sum(q.x for q in pts)/len(pts),sum(q.y for q in pts)/len(pts),sum(q.z for q in pts)/len(pts));proj=[inv.multVec(q-center) for q in pts]
 center+=rot.multVec(App.Vector((min(q.x for q in proj)+max(q.x for q in proj))/2,(min(q.y for q in proj)+max(q.y for q in proj))/2,0))
 height=max(max(q.y for q in proj)-min(q.y for q in proj),(max(q.x for q in proj)-min(q.x for q in proj))/(1400/1000))*1.15
 cam=v.getCameraNode();pos=center+rot.multVec(App.Vector(0,0,5000));cam.position.setValue(pos.x,pos.y,pos.z);cam.height.setValue(height);cam.nearDistance.setValue(1);cam.farDistance.setValue(20000);cam.focalDistance.setValue(5000)
 Gui.updateGui();v.saveImage(str(root/(record['title']+'_R14.png')),1400,1000,'White');d.save()
result={'images':[str(root/(r['title']+'_R14.png')) for r in records]}
