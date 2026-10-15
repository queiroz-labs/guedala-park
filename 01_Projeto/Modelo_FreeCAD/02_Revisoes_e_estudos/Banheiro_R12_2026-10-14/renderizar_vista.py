from pathlib import Path
import json
import FreeCAD as App, FreeCADGui as Gui
root=(Path(__file__).resolve().parent / '.').resolve()
def render(index):
 reports=json.loads(((Path(__file__).resolve().parent / 'Vistas_R12.json').resolve()).read_text(encoding='utf-8'));record=reports[index];d=App.getDocument(record['document']);v=Gui.getDocument(d.Name).activeView();rot=v.getCameraOrientation();inv=rot.inverted();pts=[]
 for o in d.Objects:
  if hasattr(o,'Shape'):
   b=o.Shape.optimalBoundingBox();pts.extend(App.Vector(x,y,z) for x in [b.XMin,b.XMax] for y in [b.YMin,b.YMax] for z in [b.ZMin,b.ZMax])
 center=App.Vector(sum(p.x for p in pts)/len(pts),sum(p.y for p in pts)/len(pts),sum(p.z for p in pts)/len(pts));proj=[inv.multVec(q-center) for q in pts]
 height=max(max(q.y for q in proj)-min(q.y for q in proj),(max(q.x for q in proj)-min(q.x for q in proj))/(900/1200))*1.2
 cam=v.getCameraNode();pos=center+rot.multVec(App.Vector(0,0,5000));cam.position.setValue(pos.x,pos.y,pos.z);cam.height.setValue(height);cam.nearDistance.setValue(1);cam.farDistance.setValue(20000);cam.focalDistance.setValue(5000)
 Gui.updateGui();v.saveImage(str(root/('Banheiro_'+record['label']+'_R12.png')),900,1200,'White');d.save()
 return {'image':str(root/('Banheiro_'+record['label']+'_R12.png')),'height':height}
