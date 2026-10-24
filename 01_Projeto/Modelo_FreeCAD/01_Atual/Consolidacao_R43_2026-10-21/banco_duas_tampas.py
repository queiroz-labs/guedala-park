import FreeCAD as A,FreeCADGui as G,Part,pathlib,json
P=pathlib.Path(__file__).resolve().parent;d=A.getDocument('Guedala_Park_R43_Consolidado')
root=d.addObject('App::DocumentObjectGroup','BancoDuasTampasR43');root.Label='Banco R43 — somente duas tampas e duas almofadas'
root.addProperty('App::PropertyString','Status','Rastreabilidade');root.Status='Duas tampas sobre apoios existentes; interior preservado. Retirar almofadas antes de abrir. Ferragens, retenção, massa e resistência por dimensionar.'
old=['TampaBancoR16','TampaBancoR001','TampaBancoR002','TampaBancoR003','PecaBancoR011','PecaBancoR013','PecaBancoR015']
def descendants(o):
 a=[o]
 for q in getattr(o,'Group',[]):a+=descendants(q)
 return a
hidden=[]
for n in old:
 o=d.getObject(n)
 for q in descendants(o):q.ViewObject.Visibility=False;hidden.append(q.Name)
ctrl=d.addObject('App::FeaturePython','BancoR43_Controle');root.addObject(ctrl)
for i in [1,2]:ctrl.addProperty('App::PropertyFloatConstraint','Abertura'+str(i),'Movimento');setattr(ctrl,'Abertura'+str(i),(0,0,90,1))
for i,y,length,cy,clen in [(1,3751,971,3750,972),(2,4724,825,4724,826)]:
 g=d.addObject('App::Part','BancoR43_Tampa'+str(i));root.addObject(g);g.Label='Tampa '+str(i)+' — '+str(length)+' × 448 × 20 mm';g.Placement.Base=A.Vector(102,y,420)
 g.Placement.Rotation=A.Rotation(A.Vector(0,1,0),0);g.setExpression('Placement.Rotation.Angle','-BancoR43_Controle.Abertura'+str(i)+' * 1 deg')
 o=d.addObject('PartDesign::Feature','BancoR43_Painel'+str(i));g.addObject(o);o.Shape=Part.makeBox(448,length,20,A.Vector(0,0,-20));o.ViewObject.ShapeColor=(.70,.62,.49)
 o=d.addObject('PartDesign::Feature','BancoR43_Almofada'+str(i));root.addObject(o);o.Label='Almofada '+str(i)+' — retirar antes de abrir';o.Shape=Part.makeBox(450,clen,50,A.Vector(100,cy,420));o.ViewObject.ShapeColor=(.72,.70,.65)
d.recompute()
def w(o):
 s=o.Shape.copy();s.Placement=o.getGlobalPlacement();return s
def visible(o):return o.ViewObject.Visibility and all(visible(p) for p in o.InList if hasattr(p,'Group') and o in p.Group)
region=Part.makeBox(450,1800,500,A.Vector(100,3750,400)).BoundBox
obstacles=[]
for o in d.Objects:
 if o.Name.startswith('BancoR43_') or hasattr(o,'Group') or not hasattr(o,'Shape') or o.Shape.isNull() or not visible(o):continue
 s=w(o)
 if region.intersect(s.BoundBox):obstacles.append((o.Name,s))
r={'hidden':hidden,'lid_sizes_mm':[[971,448,20],[825,448,20]],'joint_y_mm':[4722,4724],'support_y_mm':[4714,4732],'internal_parts_changed':False,'checks':[],'limits':'Movimento nominal sem almofadas. Eixo ilustrativo; ferragens, retenção e resistência não dimensionadas.'}
for i in [1,2]:
 for angle in range(0,91,5):
  setattr(ctrl,'Abertura'+str(i),angle);d.recompute();s=w(d.getObject('BancoR43_Painel'+str(i)));hits=[]
  for n,t in obstacles:
   if s.BoundBox.intersect(t.BoundBox):
    vol=s.common(t).Volume
    if vol>.1:hits.append([n,vol])
  r['checks'].append({'lid':i,'angle':angle,'hits':hits})
 setattr(ctrl,'Abertura'+str(i),0);d.recompute()
d.save();G.updateGui();(P/'Banco_duas_tampas.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
