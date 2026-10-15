from pathlib import Path
import json,math
import FreeCAD as App,Part
root=(Path(__file__).resolve().parent / '.').resolve();data=json.loads(((Path(__file__).resolve().parent / 'Montagem_R16.json').resolve()).read_text(encoding='utf-8'))
d=next(d for d in App.listDocuments().values() if d.FileName and Path(d.FileName).resolve()==(Path(__file__).resolve().parent / 'Guedala_Park_R16_Banco_Simples.FCStd').resolve())
def shape(o):
 s=o.Shape.copy();s.Placement=o.getGlobalPlacement();return s
def vol(a,b):
 x,y=a.BoundBox,b.BoundBox
 if any(getattr(x,k+'Max')<=getattr(y,k+'Min')+1e-6 or getattr(y,k+'Max')<=getattr(x,k+'Min')+1e-6 for k in ['X','Y','Z']):return 0
 return a.common(b).Volume
def reset():
 for row in data['lids']:
  c=d.getObject(row['control']);c.Abertura=0
  if row['separate_cushion']:c.ElevarAlmofada=0;c.DeslocamentoAlmofada=0
 d.recompute()
external=[o for o in d.getObject('Ambiente_sala').Group if o.TypeId=='Part::Box']+list(d.getObject('ParedesInteiras').Group)
fixed=external+[d.getObject(n) for n in data['structure']+data['content']+data['panels']+data['ledges']+[data['containment'],data['leaf']]]
lids=[d.getObject(r['lid']) for r in data['lids']];pads=[d.getObject(r['cushion']) for r in data['lids']]
cushions=[]
for row in data['lids'][1:3]:
 reset();c=d.getObject(row['control']);pad=d.getObject(row['cushion']);shift=row['parking_source_v']-row['pad_v'];nodes=[(0,0),(60,0),(60,shift),(50,shift)]
 for start,end in zip(nodes,nodes[1:]):
  c.ElevarAlmofada,c.DeslocamentoAlmofada=start;d.recompute();b1=shape(pad).BoundBox;c.ElevarAlmofada,c.DeslocamentoAlmofada=end;d.recompute();b2=shape(pad).BoundBox
  mins=[min(getattr(b1,k+'Min'),getattr(b2,k+'Min')) for k in ['X','Y','Z']];maxs=[max(getattr(b1,k+'Max'),getattr(b2,k+'Max')) for k in ['X','Y','Z']]
  swept=Part.makeBox(*[hi-lo for lo,hi in zip(mins,maxs)],App.Vector(*mins));hits=[]
  for q in fixed+lids+[q for q in pads if q!=pad]:
   v=vol(swept,shape(q))
   if v>.1:hits.append({'target':q.Name,'mm3':v})
  cushions.append({'sector':row['id'],'start_lift_shift_mm':start,'end_lift_shift_mm':end,'hits':hits})
# New leaf envelope: move16 mm forward, then lift. Pads must have returned first.
reset();d.getObject(data['lids'][3]['control']).Abertura=90;d.recompute();leaf=d.getObject(data['leaf']);orig=leaf.Placement.copy();p=orig.Base
leafNodes=[p,App.Vector(p.x,p.y-16,p.z),App.Vector(p.x,p.y-16,970)];leafRoute=[]
for p1,p2 in zip(leafNodes,leafNodes[1:]):
 leaf.Placement.Base=p1;d.recompute();b1=shape(leaf).BoundBox;leaf.Placement.Base=p2;d.recompute();b2=shape(leaf).BoundBox
 mins=[min(getattr(b1,k+'Min'),getattr(b2,k+'Min')) for k in ['X','Y','Z']];maxs=[max(getattr(b1,k+'Max'),getattr(b2,k+'Max')) for k in ['X','Y','Z']]
 swept=Part.makeBox(*[hi-lo for lo,hi in zip(mins,maxs)],App.Vector(*mins));hits=[]
 for q in fixed+lids+pads:
  if q==leaf:continue
  v=vol(swept,shape(q))
  if v>.1:hits.append({'target':q.Name,'label':q.Label,'mm3':v})
 leafRoute.append({'from_mm':list(p1),'to_mm':list(p2),'hits':hits})
leaf.Placement=orig
# Negative functional test: opening the leaf seat while a pad is parked must be disallowed in use.
reset();row=data['lids'][1];c=d.getObject(row['control']);c.ElevarAlmofada=50;c.DeslocamentoAlmofada=row['parking_source_v']-row['pad_v'];d.getObject(data['lids'][3]['control']).Abertura=15;d.recompute();negative=[]
for o in [d.getObject(data['lids'][3]['lid']),d.getObject(data['lids'][3]['cushion'])]:
 v=vol(shape(o),shape(d.getObject(row['cushion'])))
 if v>.1:negative.append({'pair':[o.Name,row['cushion']],'mm3':v})
# Analytic clearance to the table in (u,Z), for modified whole-seat70 and thin20.
table=[(-700,720),(50,720),(50,750),(-700,750)]
def intersects(A,B):
 for poly in [A,B]:
  for p,q in zip(poly,poly[1:]+poly[:1]):
   n=(-(q[1]-p[1]),q[0]-p[0]);aa=[x*n[0]+y*n[1] for x,y in A];bb=[x*n[0]+y*n[1] for x,y in B]
   if max(aa)<min(bb)-1e-8 or max(bb)<min(aa)-1e-8:return False
 return True
def segment(P,A,B):
 dx,dy=B[0]-A[0],B[1]-A[1];t=max(0,min(1,((P[0]-A[0])*dx+(P[1]-A[1])*dy)/(dx*dx+dy*dy)))
 return math.hypot(P[0]-A[0]-t*dx,P[1]-A[1]-t*dy)
def distance(A,B):
 if intersects(A,B):return 0
 return min(segment(p,a,b) for X,Y in [(A,B),(B,A)] for p in X for a,b in zip(Y,Y[1:]+Y[:1]))
proof=[]
for thick,pivot in [(20,420),(70,470)]:
 dist=[]
 for deg in range(0,91,5):
  t=math.radians(deg);c,s=math.cos(t),math.sin(t);poly=[(448+u*c+z*s,pivot-u*s+z*c) for u,z in [(-448,-thick),(0,-thick),(0,0),(-448,0)]]
  dist.append((deg,distance(poly,table)))
 bound=math.hypot(448,thick)*math.radians(2.5)
 proof.append({'thickness_mm':thick,'pivot_height_mm':pivot,'new_2D_samples':19,'min_sample_mm':min(v for _,v in dist),'half_step_displacement_bound_mm':bound,'continuous_ideal_table_gap_lower_bound_mm':min(v for _,v in dist)-bound,'limitations':'Somente retângulo ideal da tampa/assento e tampo, não ferragem/mãos/deformação/outros objetos. Faixa70 usa envelope conservador por448; almofada tem2 mm adicionais para trás do eixo, limitados a u450 e abaixo470, fora do tampo720–750.'})
reset();d.save()
report={'cushion_continuous_segments':cushions,'leaf_advance16_then_lift':leafRoute,'negative_leaf_open_with_parked_pad_hits':negative,'table_ideal_bounds':proof,'analytic_own_body_separation':'Tampa20: Z>=420-20*cos(theta)>=400; madeira do assento70: Z>=470-70*cos(theta)>=400. Corpo/programa até400 não são penetrados em0–90; Xlongitudinal constante e juntas1/2 separam folhas/setores. Para encosto, madeira u<=448; almofada integral u<=448+2*cos(theta)<=450. Contato macio no fechado não é folga física certificada.','limits':'Novos caminhos geométricos com banco R16. Folha800x350x70 é reserva; não prova peça/estrutura real, transporte ou implantação na mesa. Teste negativo impõe sequência de uso, sem intertravamento físico.'}
((Path(__file__).resolve().parent / 'Complemento_R16.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');result=report
