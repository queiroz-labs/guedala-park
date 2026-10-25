"""Equilibrio de corpo rigido sobre poligono nominal; nao certifica o movel.
Calculo separado para bancada inteiramente ligada e pedestal independente.
"""
from pathlib import Path
import json,math,itertools,hashlib
import numpy as np
HERE=Path(__file__).resolve().parent
G=json.loads((HERE/'Geometria_R51.json').read_text(encoding='utf8'))
S=json.loads((HERE.parent/'Bancada_marcenaria_2026-10-25/Resultados.json').read_text(encoding='utf8'))
grav=9.80665
def hull(points):
 p=sorted(set(tuple(x) for x in points))
 def cross(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
 lo=[];hi=[]
 for q in p:
  while len(lo)>=2 and cross(lo[-2],lo[-1],q)<=0:lo.pop()
  lo.append(q)
 for q in reversed(p):
  while len(hi)>=2 and cross(hi[-2],hi[-1],q)<=0:hi.pop()
  hi.append(q)
 return np.array(lo[:-1]+hi[:-1],float)
def panels(boundary):
 return [p for p in S['panels'] if boundary=='whole' or p['id'].startswith('Pedestal_')]
def footprint(boundary):
 pts=[]
 for p in panels(boundary):
  x,y,z=p['origin_mm'];sx,sy,sz=p['size_mm']
  if z!=0:continue
  pts.extend([(x,y),(x+sx,y),(x+sx,y+sy),(x,y+sy)])
 return hull(pts)
def fixed_parts(boundary,rho,top_credit):
 a=[]
 for p in panels(boundary):
  s=np.array(p['size_mm'],float);c=np.array(p['origin_mm'])+s/2
  a.append((float(np.prod(s))*rho/1e9,c,p['id']))
 for p in G['fixed_original']:
  factor=top_credit if p['name']=='Peca110' else 1.
  if p['name']=='Peca110' and boundary=='pedestal':continue
  a.append((p['volume_mm3']*rho/1e9*factor,np.array(p['center_mm']),p['name']))
 return a
def solve(boundary,rho,top_credit,extensions,payloads,location):
 items=fixed_parts(boundary,rho,top_credit)
 for dr,ext,payload in zip(G['drawers'],extensions,payloads):
  for p in dr['wood']:
   cg=np.array(p['center_mm'])+[0.,ext,0.];items.append((p['volume_mm3']*rho/1e9,cg,p['name']))
  # Interior realY307..666: centro486,5 ou faixa frontal50, CGY641.
  front=dr['wood'][4]['box_mm'][1];rear=dr['wood'][3]['box_mm'][4]
  y=(front+rear)/2 if location=='uniform_center' else front-25
  x=(dr['wood'][0]['box_mm'][3]+dr['wood'][1]['box_mm'][0])/2
  items.append((payload,np.array([x,y+ext,dr['wood'][2]['box_mm'][5]+25]),'payload'))
 poly=footprint(boundary);M=sum(m for m,c,n in items);cg=sum((m*c for m,c,n in items),np.zeros(3))/M
 edges=[]
 for i,(aa,bb) in enumerate(zip(poly,np.roll(poly,-1,axis=0))):
  e=(bb-aa)/np.linalg.norm(bb-aa);normal=np.array([-e[1],e[0]])
  distances=[float((c[:2]-aa)@normal) for m,c,n in items]
  margin=sum(m*grav*d/1000 for (m,c,n),d in zip(items,distances))
  edges.append(dict(edge=i,a_mm=aa.tolist(),b_mm=bb.tolist(),restoring_margin_Nm=margin,
   min_rigid_CG_inside_distance_mm=float((cg[:2]-aa)@normal),
   forward_horizontal_tip_force_at750_N=margin/(.75*(-e[0])) if e[0]<-1e-12 else None))
 front=[e for e in edges if e['forward_horizontal_tip_force_at750_N'] is not None]
 critical=min(edges,key=lambda e:e['restoring_margin_Nm']);fe=min(front,key=lambda e:e['forward_horizontal_tip_force_at750_N'])
 # Forca de retencao traseira equivalente apenas no pedestal, vao40..680.
 hold=max(0.,-min(e['restoring_margin_Nm'] for e in front))/.640 if boundary=='pedestal' else None
 return dict(boundary=boundary,rho_kg_m3=rho,tabletop_mass_credit_fraction=top_credit,
  drawer_extensions_mm=list(extensions),payload_per_drawer_kg=list(payloads),payload_location=location,
  wood_plus_payload_mass_kg=M,center_mm=cg.tolist(),min_restoring_margin_Nm=critical['restoring_margin_Nm'],
  rigid_vertical_equilibrium_inside_hull=all(e['restoring_margin_Nm']>=0 for e in edges),
  signed_forward_moment_ratio_N=fe['forward_horizontal_tip_force_at750_N'],
  forward_tip_horizontal_force_at750_N=max(0.,fe['forward_horizontal_tip_force_at750_N']),
  pedestal_equivalent_rear_hold_down_N=hold,edges=edges)

def main():
 assert hashlib.sha256(Path(G['cad']).read_bytes()).hexdigest()==G['sha256']
 rows=[]
 for boundary in ('whole','pedestal'):
  for rho in (650,800,900):
   for credit in ((0.,.5,1.) if boundary=='whole' else (0.,)):
    for ext in itertools.product((0.,200.,400.),repeat=2):
     for pay in ((0.,0.),(5.,5.),(10.,10.),(20.,20.),(0.,20.),(20.,0.)):
      for location in ('uniform_center','front50'):
       rows.append(solve(boundary,rho,credit,ext,pay,location))
 # Calcula tambem por momento independente sobreY680 do pedestal.
 for r in rows:
  total=r['wood_plus_payload_mass_kg'];Y=r['center_mm'][1]
  for e in r['edges']:
   if e['a_mm'][1]==680 and e['b_mm'][1]==680:
    assert abs(e['restoring_margin_Nm']-total*grav*(680-Y)/1000)<1e-8
 examples=[r for r in rows if r['rho_kg_m3']==650 and r['drawer_extensions_mm']==[400.,400.] and r['payload_per_drawer_kg'] in [[10.,10.],[20.,20.]] and r['tabletop_mass_credit_fraction'] in (0.,1.)]
 data=dict(cad=G['cad'],sha256=G['sha256'],case_count=len(rows),cases=rows,examples=examples,
  hulls_mm={b:footprint(b).tolist() for b in ('whole','pedestal')},
  input_sha256={str(p.relative_to(HERE.parent)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [HERE/'Geometria_R51.json',HERE.parent/'Bancada_marcenaria_2026-10-25/Resultados.json']},
  source_unchanged=True,scope='Triagem de corpo rigido, paineis da proposta ligados. Exclui ferragens/equipamentos, atrito, deformacao, juntas, nivelamento, ancoragens e norma de ensaio. Payload e massa de conteudo; nao e capacidadeMOVENTO. Credito0/.5/1 do tampo e sensibilidade ao peso, sem retirar tampo da geometria ou definir constituicao.')
 (HERE/'Estabilidade.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
 print(json.dumps([dict(boundary=r['boundary'],credit=r['tabletop_mass_credit_fraction'],payload=r['payload_per_drawer_kg'],loc=r['payload_location'],margin=r['min_restoring_margin_Nm'],H=r['forward_tip_horizontal_force_at750_N'],hold=r['pedestal_equivalent_rear_hold_down_N']) for r in examples],ensure_ascii=False))
if __name__=='__main__':main()
