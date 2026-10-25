import FreeCAD as App,Part,json
P=r'C:\Users\Elias\Documents\PROJETOS\Guedala park\guedala-park\04_Moveis\Inventario_dimensional\Inventario'
S=App.getDocument('Guedala_Park_R44_Consolidado');N='Espelheiro_Pinos_R45_ESTUDO'
if N in App.listDocuments():raise RuntimeError('Documento já existe; não sobrescrever')
D=App.newDocument(N);C=D.addObject('App::DocumentObjectGroup','Contexto');F=D.addObject('App::DocumentObjectGroup','Pinos');M=D.addObject('App::DocumentObjectGroup','Laterais_furadas')
tree=json.load(open(P+'\\Arvore_R44.json',encoding='utf-8'));T={x['name']:x for x in tree};names=set();queue=['Modulo018']
while queue:
 n=queue.pop();names.add(n);queue.extend(T[n]['group'])
data=json.load(open(P+'\\Solidos_finitos_ativos_R44.json',encoding='utf-8'));ctx=[]
def glob(o):
 s=o.Shape.copy();s.Placement=o.getGlobalPlacement().multiply(o.Placement.inverse()).multiply(s.Placement);return s
def obj(n,l,s,g,col):
 o=D.addObject('PartDesign::Feature',n);o.Label=l;o.Shape=s;g.addObject(o);o.ViewObject.ShapeColor=col;return o
for r in data:
 if r['name'] in names and r['name'] not in ['Peca400','Peca401']:
  ctx.append(obj('Ref_'+r['name'],r['label'],glob(S.getObject(r['name'])),C,(.78,.75,.68)))
pins=[];holes={0:[],1:[]};coords=[]
for k,z in enumerate([1394,1638]):
 for j,y in enumerate([5184,5250]):
  for side,x,direction in [(0,2778,1),(1,3342,-1)]:
   # Catalogue spoon head: 10 projection,7.5 width,2.7 thickness; pin5x8.
   # Flattened rectangular head is conservative envelope, not manufacturer's STEP.
   sh=Part.makeBox(10,7.5,2.7,App.Vector(x if side==0 else x-10,y-3.75,z-2.7))
   pin=Part.makeCylinder(2.5,8,App.Vector(x,y,z),App.Vector(-direction,0,0))
   shape=sh.fuse(pin)
   pins.append(obj('Pino_%d_%d_%d'%(k,j,side),'Häfele282.04.711 — envelope dimensional, não STEP',shape,F,(.65,.69,.72)))
   holes[side].append(Part.makeCylinder(2.5,8.5,App.Vector(x,y,z),App.Vector(-direction,0,0)))
   coords.append(dict(side='left' if side==0 else 'right',axis_mm=[x,y,z],diameter_mm=5,proposed_blind_depth_mm=8.5))
panels=[]
for side,n in [(0,'Peca401'),(1,'Peca400')]:
 sh=glob(S.getObject(n)).cut(Part.makeCompound(holes[side]));panels.append(obj('Lateral_'+str(side),n+' — quatro furos cegos propostos',sh,M,(.75,.73,.66)))
hits=[]
for p in pins:
 for c in ctx+panels:
  if p.Shape.BoundBox.intersect(c.Shape.BoundBox):
   v=p.Shape.common(c.Shape).Volume
   if v>.01:hits.append([p.Name,c.Name,v])
out=dict(status='Compatibilidade nominal de envelope/furação; resistência e tolerâncias não aprovadas',pin_quantity=8,pin_projection_mm=10,shelf_side_gap_mm=2,nominal_bearing_overlap_mm=8,shelf_dimensions_unchanged=[560,104,18],wall_thickness_mm=18,blind_depth_proposed_mm=8.5,remaining_wall_nominal_mm=9.5,hole_axes=coords,intersections=hits,context=len(ctx),valid=all(o.Shape.isValid() for o in ctx+panels+pins),source_note='Catálogo Häfele2018 p7.154; 282.04.711 tem10/2.7/8. Não copiar11/2.5/8.5 do282.04.712 adjacente.')
D.recompute();D.saveAs(P+'\\Espelheiro_Pinos_R45_ESTUDO.FCStd')
json.dump(out,open(P+'\\Espelheiro_pinos.json','w',encoding='utf-8'),ensure_ascii=False,indent=2)
result=out
