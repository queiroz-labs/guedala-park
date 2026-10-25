"""Disposable visual-only scene, based exclusively on the current adopted-result inventory."""
import FreeCAD as App, FreeCADGui as Gui
from pivy import coin
from pathlib import Path
import json
root=(Path(__file__).resolve().parent / '.').resolve()
data=json.loads(((Path(__file__).resolve().parent / 'Medidas_atual_R28.json').resolve()).read_text(encoding='utf-8'))
source=App.getDocument('Guedala_Park_R28_Folga_Teto_Proposta')
scene_name=globals().get('scene','cozinha')
scenes={
 'cozinha':{'roots':['Modulo'+str(i).zfill(3) for i in range(4,13)],'objects':['Peca133','Peca134','Peca135','Peca136','Peca137','Peca138','Peca139','Peca140','Peca141','Peca351','Peca308'],'camera':[.12,-1,.3]},
 'lavanderia':{'roots':['Modulo013','Modulo014'],'objects':['Peca147','Peca148','Peca149','Peca152','Peca154','Peca155','Peca156','Peca157','Peca357'],'camera':[.12,-1,.3]},
 'quarto':{'roots':['Modulo','Modulo001','Modulo002','Modulo003','CabeceiraDoisPaineisR25'],'objects':['Peca275'],'camera':[-1,-.8,.45]},
 'escritorio':{'roots':['Modulo015','Modulo016'],'objects':['Peca122','Peca123','Peca124','Peca125','Peca126'],'camera':[-1,-.2,.35]},
 'banheiro':{'roots':['Modulo017','Modulo018'],'objects':['Peca075','Peca185','Peca186','Peca187','Peca188','Peca189','Peca399'],'camera':[.12,-1,.3]},
 'banco':{'roots':['Modulo019'],'objects':['Peca'+str(i).zfill(3) for i in range(91,102)],'camera':[1,-.4,.6]}
}
cfg=scenes[scene_name]
old=App.getDocument('RevisaoVisualR28') if 'RevisaoVisualR28' in App.listDocuments() else None
if old:App.closeDocument(old.Name)
d=App.newDocument('RevisaoVisualR28');d.Label='REVISÃO VISUAL TEMPORÁRIA — '+scene_name
ref=App.Matrix();ref.A11=-1;ref.A14=7400
names=[]
for row in data['items']:
 if row['root'] not in cfg['roots'] and row['object'] not in cfg['objects']:continue
 o=source.getObject(row['object']);s=o.Shape.copy();s.Placement=o.getGlobalPlacement()
 p=d.addObject('Part::Feature','Vista_'+o.Name);p.Label=o.Label;p.Shape=s.transformGeometry(ref)
 p.ViewObject.ShapeColor=o.ViewObject.ShapeColor;p.ViewObject.LineColor=o.ViewObject.LineColor
 p.ViewObject.Transparency=o.ViewObject.Transparency
 if (scene_name=='banheiro' and o.Name=='Peca075') or (scene_name=='banco' and o.Name in ['Peca099','Peca100','Peca101']):p.ViewObject.Transparency=75
 names.append(o.Name)
d.recompute();v=Gui.activeDocument().activeView()
rot=App.Rotation(App.Vector(1,0,0),App.Vector(0,0,1),App.Vector(*cfg['camera']),'ZYX')
v.setCameraOrientation(rot.Q)
boxes=[o.Shape.BoundBox for o in d.Objects if 'Shape' in o.PropertiesList]
lo=App.Vector(min(b.XMin for b in boxes),min(b.YMin for b in boxes),min(b.ZMin for b in boxes))
hi=App.Vector(max(b.XMax for b in boxes),max(b.YMax for b in boxes),max(b.ZMax for b in boxes));center=(lo+hi)*.5
points=[rot.inverted().multVec(App.Vector(x,y,z)-center) for x in [lo.x,hi.x] for y in [lo.y,hi.y] for z in [lo.z,hi.z]]
w=max(p.x for p in points)-min(p.x for p in points);h=max(p.y for p in points)-min(p.y for p in points)
cam=v.getCameraNode();pos=center+rot.multVec(App.Vector(0,0,10000));cam.position.setValue(pos.x,pos.y,pos.z)
cam.nearDistance.setValue(1);cam.farDistance.setValue(30000);cam.focalDistance.setValue(10000);cam.height.setValue(max(h,w/(1700/1100))*1.15)
(root/('Vista_'+scene_name+'_selecao.json')).write_text(json.dumps({'scene':scene_name,'source':source.Name,'objects':names,'limits':'Closed-state visual extraction. Nonselected context omitted and explicitly listed. No change to source CAD, controls, visibility or topology. Auxiliary reflected copies are for display only, not new BRep validity evidence.'},ensure_ascii=False,indent=2),encoding='utf-8')
result={'scene':scene_name,'parts':len(names),'ready':True}
