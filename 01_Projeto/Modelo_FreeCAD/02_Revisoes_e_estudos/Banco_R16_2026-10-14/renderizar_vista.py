from pathlib import Path
import json
import FreeCAD as App,FreeCADGui as Gui
root=(Path(__file__).resolve().parent / '.').resolve()
def render(index):
 record=json.loads(((Path(__file__).resolve().parent / 'Vistas_R16.json').resolve()).read_text(encoding='utf-8'))[index];d=App.getDocument(record['document']);v=Gui.getDocument(d.Name).activeView();rot=v.getCameraOrientation();inv=rot.inverted();pts=[]
 for o in d.Objects:
  if 'Shape' in o.PropertiesList:
   b=o.Shape.optimalBoundingBox();pts.extend(App.Vector(x,y,z) for x in [b.XMin,b.XMax] for y in [b.YMin,b.YMax] for z in [b.ZMin,b.ZMax])
 center=App.Vector(sum(q.x for q in pts)/len(pts),sum(q.y for q in pts)/len(pts),sum(q.z for q in pts)/len(pts));proj=[inv.multVec(q-center) for q in pts];center+=rot.multVec(App.Vector((min(q.x for q in proj)+max(q.x for q in proj))/2,(min(q.y for q in proj)+max(q.y for q in proj))/2,0))
 height=max(max(q.y for q in proj)-min(q.y for q in proj),(max(q.x for q in proj)-min(q.x for q in proj))/(1600/1000))*1.4
 cam=v.getCameraNode();pos=center+rot.multVec(App.Vector(0,0,5000));cam.position.setValue(pos.x,pos.y,pos.z);cam.height.setValue(height);cam.nearDistance.setValue(1);cam.farDistance.setValue(20000);cam.focalDistance.setValue(5000)
 Gui.updateGui();out=root/(record['label']+'_R16.png');v.saveImage(str(out),1600,1000,'White');d.save();return str(out)
