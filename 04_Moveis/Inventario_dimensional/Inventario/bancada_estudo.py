import FreeCAD as App, Part, json, os, math
P=r'C:\Users\Elias\Documents\PROJETOS\Guedala park\guedala-park\04_Moveis\Inventario_dimensional\Inventario'
S=App.getDocument('Guedala_Park_R44_Consolidado')
N='Bancada_Estrutura_R45_ESTUDO'
if N in App.listDocuments():
 raise RuntimeError('Documento de estudo já existe; não sobrescrever silenciosamente.')
D=App.newDocument(N)
ctx=D.addObject('App::DocumentObjectGroup','Contexto');ctx.Label='01 Contexto R44 preservado'
steel=D.addObject('App::DocumentObjectGroup','Estrutura');steel.Label='02 Estrutura de estudo — não fabricável sem ligações'
wood=D.addObject('App::DocumentObjectGroup','Tampo');wood.Label='03 Tampo mesmo envelope — bolsões inferiores propostos'
tests=D.addObject('App::DocumentObjectGroup','Reservas');tests.Label='04 Reservas de uso — ocultas'
def obj(name,label,shape,group,color):
 o=D.addObject('PartDesign::Feature',name);o.Label=label;o.Shape=shape;group.addObject(o);o.ViewObject.ShapeColor=color;return o
def glob(o):
 s=o.Shape.copy();s.Placement=o.getGlobalPlacement().multiply(o.Placement.inverse()).multiply(s.Placement);return s
data=json.load(open(P+'\\Solidos_finitos_ativos_R44.json',encoding='utf-8'))
context=[]
for r in data:
 b=r['bbox']
 if b[0]>=2600 and b[3]<=4800 and b[1]>=-1 and b[4]<=750 and b[2]<1200 and r['name'] not in ['Peca110','Peca111','Peca112']:
  o=obj('Ref_'+r['name'],r['label'],glob(S.getObject(r['name'])),ctx,(0.73,0.65,0.5));context.append(o)
raw=glob(S.getObject('Peca110'))
original=obj('Original','Tampo R44 original — comparação oculta',raw,tests,(0.7,0.5,0.3));original.ViewObject.Visibility=False
members=[];cutters=[]
def rhs(name,start,dim,t,axis):
 x,y,z=start;dx,dy,dz=dim
 outer=Part.makeBox(dx,dy,dz,App.Vector(x,y,z))
 innerstart=[x+t,y+t,z+t];innerdim=[dx-2*t,dy-2*t,dz-2*t]
 innerstart[axis]=start[axis]-1;innerdim[axis]=dim[axis]+2
 shape=outer.cut(Part.makeBox(*innerdim,App.Vector(*innerstart)))
 o=obj(name,name+' — seção nominal, cantos idealizados',shape,steel,(0.22,0.27,0.3));members.append(o)
 return o
# Four longitudinal rectangular tubes, 40 mm horizontal x 20 mm vertical x 3 mm wall.
for i,y in enumerate([60,100,580,620]):
 rhs('Longarina_%d'%(i+1),(2730,y,720),(1940,40,20),3,0)
 cutters.append(Part.makeBox(1941,40.5,20.5,App.Vector(2729.5,y-.25,720)))
# End crossmembers are inside the top, no apron below the entry zone.
for i,x in enumerate([2765,4230]):
 rhs('Travessa_embutida_%d'%(i+1),(x,140,720),(40,440,20),3,1)
 cutters.append(Part.makeBox(40.5,440.5,20.5,App.Vector(x-.25,139.75,720)))
# Four legs replace the two schematic R44 supports only within this separate study.
for i,x in enumerate([2765,4230]):
 for j,y in enumerate([80,600]):
  rhs('Pe_%d_%d'%(i+1,j+1),(x,y,10),(40,40,710),3,2)
  o=obj('Sapata_%d_%d'%(i+1,j+1),'Sapata 40×40×10 — interface, SKU não definido',Part.makeBox(40,40,10,App.Vector(x,y,0)),steel,(0.08,0.08,0.08));members.append(o)
# Cross-bracing behind the working clearance; 30 x 3 flat stock envelopes.
def flatdiag(name,p1,p2,width=30,thick=3):
 v=App.Vector(*p2)-App.Vector(*p1);length=v.Length
 sh=Part.makeBox(length,thick,width,App.Vector(0,-thick/2,-width/2))
 sh.Placement=App.Placement(App.Vector(*p1),App.Rotation(App.Vector(1,0,0),v))
 o=obj(name,name+' — união soldada a dimensionar',sh,steel,(0.25,0.3,0.33));members.append(o)
flatdiag('Diagonal_posterior_A',(2805,100,100),(4230,100,670))
flatdiag('Diagonal_posterior_B',(2805,105,670),(4230,105,100))
for i,x in enumerate([2785,4250]):
 flatdiag('Diagonal_lateral_%d'%(i+1),(x,120,100),(x,600,670))
cut=Part.makeCompound(cutters)
newtop=raw.cut(cut)
top=obj('Tampo_usinado','Tampo 2000×700×30 preservado; bolsões20,5 deixam9,5 nominal',newtop,wood,(0.72,0.55,0.35))
top.ViewObject.Transparency=35
chair=Part.makeBox(800,500,720,App.Vector(3100,200,0))
res=obj('Faixa_cadeira','Reserva central800×500×720; não é cadeira real',chair,tests,(0.3,0.7,0.9));res.ViewObject.Visibility=False
hits=[]
for a in members:
 for b in context+[top]:
  if a.Shape.BoundBox.intersect(b.Shape.BoundBox):
   vol=a.Shape.common(b.Shape).Volume
   if vol>0.01:hits.append([a.Name,b.Name,vol])
chairhits=[]
for a in members:
 v=a.Shape.common(chair).Volume
 if v>0.01:chairhits.append([a.Name,v])
out=dict(scope='Estudo separado de estrutura, não altera R44 nem armazenamento',members=len(members),context=len(context),intersections=hits,chair_reserve_intersections=chairhits,top_bbox_mm=[newtop.BoundBox.XLength,newtop.BoundBox.YLength,newtop.BoundBox.ZLength],top_original_volume_mm3=raw.Volume,top_recessed_volume_mm3=newtop.Volume,remaining_top_skin_mm=9.5,leg_free_width_mm=1425,drawer_clearance_to_frame_mm=30,steel_ideal_volume_mm3=sum(x.Shape.Volume for x in members if not x.Name.startswith('Sapata')),valid_shapes=all(o.Shape.isValid() for o in context+members+[top]),source_file=S.FileName)
D.recompute()
D.saveAs(P+'\\Bancada_Estrutura_R45_ESTUDO.FCStd')
with open(P+'\\Bancada_geometria.json','w',encoding='utf-8') as f:json.dump(out,f,ensure_ascii=False,indent=2)
result=out

