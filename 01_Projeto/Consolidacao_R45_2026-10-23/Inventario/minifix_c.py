import FreeCAD as App,Part,json
P=r'C:\Users\Elias\Documents\PROJETOS\Guedala park\guedala-park\01_Projeto\Consolidacao_R45_2026-10-23\Inventario'
S=App.getDocument('Guedala_Park_R44_Consolidado');N='AereoC_Minifix_R45_ESTUDO'
if N in App.listDocuments():raise RuntimeError('Documento já existe')
D=App.newDocument(N);G=D.addObject('App::DocumentObjectGroup','Madeira');H=D.addObject('App::DocumentObjectGroup','Gabaritos');C=D.addObject('App::DocumentObjectGroup','Contexto')
def glob(o):
 s=o.Shape.copy();s.Placement=o.getGlobalPlacement().multiply(o.Placement.inverse()).multiply(s.Placement);return s
def add(n,l,s,g,color):
 o=D.addObject('PartDesign::Feature',n);o.Label=l;o.Shape=s;g.addObject(o);o.ViewObject.ShapeColor=color;return o
boards=[('Peca327',1532,True),('Peca328',2532,False),('Peca329',1730,False),('Peca330',1940,False),('Peca331',2216,False)]
sideholes={0:[],1:[]};positions=[];physical=[]
for name,z,topaccess in boards:
 holes=[]
 for side,edge,sign in [(0,2366,1),(1,2877,-1)]:
  for y in [6730,6922]:
   x=edge+sign*34;entry=z+18 if topaccess else z;vz=-1 if topaccess else 1
   holes.append(Part.makeCylinder(7.5,14,App.Vector(x,y,entry),App.Vector(0,0,vz)))
   holes.append(Part.makeCylinder(3.5,34,App.Vector(edge,y,z+9),App.Vector(sign,0,0)))
   sideholes[side].append(Part.makeCylinder(2.5,8.5,App.Vector(edge,y,z+9),App.Vector(-sign,0,0)))
   # Cylinders show reserved drill envelope, not proprietary cam/bolt geometry.
   cam=add('Cam_'+name+'_'+str(side)+'_'+str(y),'Minifix262.26.034 — gabarito Ø15 × 14',holes[-2],H,(.85,.65,.2));cam.ViewObject.Transparency=55
   positions.append(dict(board=name,cam_axis=[x,y,entry],access='top' if topaccess else 'bottom',cam_diameter=15,cam_depth=14,bolt_axis=[edge,y,z+9],pilot_diameter=5,pilot_depth=8.5,B=34))
 sh=glob(S.getObject(name)).cut(Part.makeCompound(holes));physical.append(add('Furada_'+name,name+' — proposta Minifix, prateleira fixa',sh,G,(.85,.85,.8)))
for side,name in [(0,'Peca325'),(1,'Peca324')]:
 sh=glob(S.getObject(name)).cut(Part.makeCompound(sideholes[side]));physical.append(add('Furada_'+name,name+' — dez furos cegos',sh,G,(.85,.85,.8)))
add('Fundo','Peca326 — contexto',glob(S.getObject('Peca326')),C,(.75,.75,.72))
D.recompute();D.saveAs(P+'\\AereoC_Minifix_R45_ESTUDO.FCStd')
result=dict(document=N,cam_qty=20,bolt_qty=20,panels_valid=all(o.Shape.isValid() for o in physical),positions=positions,limits=['Furação candidata sem aprovação estrutural','Prateleiras tratadas como fixas somente nesta alternativa','Gabaritos não são STEP; colisão com ferragem móvel ainda não testada','Parede externa nominal remanescente cam4mm, piloto9.5mm; ponta de broca e tolerâncias não incluídas'])
open(P+'\\Minifix_C.json','w',encoding='utf-8').write(json.dumps(result,ensure_ascii=False,indent=2))
