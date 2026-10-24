"""Triagem nominal 2D extrudida. Não é CAD completo do fabricante nem projeto executivo."""
import json, math
from pathlib import Path

P=Path(__file__).resolve().parent
ROOT=P.parents[1]
source=ROOT/'Consolidacao_R45_2026-10-23/Inventario/Folhas_ativas_globais_R44.json'
all_objects=json.loads(source.read_text(encoding='utf8'))
objects=[o for o in all_objects if o.get('bbox') and max(map(abs,o['bbox']))<1e6 and (o.get('volume',0)>1e-6 or o['name']=='Fechada_110Tampo')]
lookup={o['name']:o for o in objects}
def rect(a,b,c,d): return [(a,b),(c,b),(c,d),(a,d)]
def rotate(p,axis,t):
 c,s=math.cos(t),math.sin(t); x,z=p[0]-axis[0],p[1]-axis[1]
 return axis[0]+x*c-z*s,axis[1]+x*s+z*c
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def overlap(a,b):
 for poly in (a,b):
  for p,q in zip(poly,poly[1:]+poly[:1]):
   n=(q[1]-p[1],p[0]-q[0]); va=[dot(x,n) for x in a];vb=[dot(x,n) for x in b]
   if min(max(va),max(vb))-max(min(va),min(vb))<=1e-6:return False
 return True
def arm(start,joint,r=7.3,overhang=35):
 dx,dz=joint[0]-start[0],joint[1]-start[1];L=math.hypot(dx,dz);u=(dx/L,dz/L);v=(-u[1],u[0])
 a=(start[0]-u[0]*r,start[1]-u[1]*r);b=(joint[0]+u[0]*overhang,joint[1]+u[1]*overhang)
 return [(a[0]+v[0]*r,a[1]+v[1]*r),(b[0]+v[0]*r,b[1]+v[1]*r),(b[0]-v[0]*r,b[1]-v[1]*r),(a[0]-v[0]*r,a[1]-v[1]*r)]
def joint(a,b,sign):
 dx,dz=b[0]-a[0],b[1]-a[1];D=math.hypot(dx,dz)
 if D>291+1e-6 or D<1e-6:raise ValueError(D)
 h=math.sqrt(max(0,145.5**2-D**2/4))
 return ((a[0]+b[0])/2-sign*dz/D*h,(a[1]+b[1])/2+sign*dx/D*h)

# Distância limite de 291 = 2 x 145,5 mm. A retenção real NÃO é definida na ficha.
# 35 mm além do joelho é reserva conservadora para pontas e alavanca, não peça real.
axis_b=(100,423.1)
lo,hi=250,350
for _ in range(70):
 x=(lo+hi)/2; opened=rotate((x,370),axis_b,math.pi/2)
 if math.dist((x,350),opened)>291:hi=x
 else:lo=x
bx=(lo+hi)/2
def bx_for(mz):
 lo,hi=250,350
 for _ in range(70):
  x=(lo+hi)/2
  if math.dist((x,mz-20),rotate((x,mz),axis_b,math.pi/2))>291:hi=x
  else:lo=x
 return (lo+hi)/2
axis_c=(6440,120);cm=(6440,450);cmo=rotate(cm,axis_c,math.radians(55))
cf=(cmo[0]+math.sqrt(291**2-(440-cmo[1])**2),440)
scenarios=[
 dict(id='banco_rejeitado_tampa1',axis=axis_b,fixed=(291.203603347455,370),mobile=(291.203603347455,390),side=(4470,4498),axes=(0,2,1),angle=90,sign=-1,lid='BancoR43_Painel1'),
 dict(id='banco_rejeitado_jarra',axis=axis_b,fixed=(bx,350),mobile=(bx,370),side=(4148,4176),axes=(0,2,1),angle=90,sign=-1,lid='BancoR43_Painel1'),
 dict(id='banco_tampa1',axis=axis_b,fixed=(bx_for(378),358),mobile=(bx_for(378),378),side=(4148,4176),axes=(0,2,1),angle=90,sign=-1,lid='BancoR43_Painel1'),
 dict(id='banco_tampa2',axis=axis_b,fixed=(bx,350),mobile=(bx,370),side=(4732,4760),axes=(0,2,1),angle=90,sign=-1,lid='BancoR43_Painel2'),
 dict(id='cesto_direito',axis=axis_c,fixed=cf,mobile=cm,side=(4792,4820),axes=(1,2,0),angle=55,sign=-1),
 dict(id='cesto_esquerdo',axis=axis_c,fixed=cf,mobile=cm,side=(4290,4318),axes=(1,2,0),angle=55,sign=-1),
]
moving_c={f'PecaCestoR{i:03d}' for i in range(3,17)}|{'PecaCestoR021'}
results=[];poses={}
for sc in scenarios:
 a1,a2,extr=sc['axes']; relevant=[]
 for o in objects:
  b=o['bbox']
  if min(sc['side'][1],b[extr+3])-max(sc['side'][0],b[extr])<=1e-6:continue
  if 'banco' in sc['id'] and o['name'] in ('BancoR43_Almofada1','BancoR43_Almofada2'):continue
  relevant.append(o)
 hit={};bounds=[1e9,1e9,-1e9,-1e9]; samples=[]
 for i in range(sc['angle']*10+1):
  deg=i/10;t=math.radians(deg);m=rotate(sc['mobile'],sc['axis'],t);j=joint(sc['fixed'],m,sc['sign'])
  polygons=[arm(sc['fixed'],j),arm(m,j)]
  for polygon in polygons:
   for x,z in polygon:bounds=[min(bounds[0],x),min(bounds[1],z),max(bounds[2],x),max(bounds[3],z)]
  for o in relevant:
   name=o['name']; b=o['bbox'];poly=rect(b[a1],b[a2],b[a1+3],b[a2+3])
   if name==sc.get('lid') or ('cesto' in sc['id'] and name in moving_c):poly=[rotate(p,sc['axis'],t) for p in poly]
   if b[a2+3]-b[a2]<1e-6:poly=rect(b[a1],b[a2]-.01,b[a1+3],b[a2]+.01)
   if name not in hit and any(overlap(p,poly) for p in polygons):hit[name]=dict(angulo=deg,label=o['label'])
  if i in (0,sc['angle']*5,sc['angle']*10):samples.append(dict(angulo=deg,fixed=sc['fixed'],mobile=m,joint=j,polygons=polygons))
 results.append(dict(**sc,poses=sc['angle']*10+1,primeiras_colisoes=hit,envelope=bounds,distancia_fechada=math.dist(sc['fixed'],sc['mobile'])))
 poses[sc['id']]=samples

# Tampa sem ferragens: triagem de posições possíveis do eixo, 0..90, passo 0,1°.
lid_results=[]
for name in ('BancoR43_Painel1','BancoR43_Painel2'):
 b=lookup[name]['bbox'];hits={}
 for i in range(901):
  t=math.radians(i/10);poly=[rotate(p,axis_b,t) for p in rect(b[0],b[2],b[3],b[5])]
  for o in objects:
   if o['name'] in (name,'BancoR43_Almofada1','BancoR43_Almofada2'):continue
   q=o['bbox']
   if min(b[4],q[4])-max(b[1],q[1])<=1e-6:continue
   if overlap(poly,rect(q[0],q[2]-.001,q[3],q[5]+.001)) and o['name'] not in hits:
    # Contatos de apoio em 0° são intencionais, não penetração.
    if i==0:continue
    hits[o['name']]=i/10
 lid_results.append(dict(tampa=name,eixo=axis_b,poses=901,colisoes=hits))

data=dict(escopo='Triagem de barras idealizadas do Bigfer 04.03.185/183 e dos painéis, contra caixas do inventário. NÃO comprova trava, capacidade nem montagem comercial.',
 premissas=['Duas barras de 145,5 mm entre eixos; limite cinemático 291 mm assumido, não curso de trava certificado.','Barras: largura 14,6 mm, projeção transversal reservada 28 mm, extensão de 35 mm além do joelho.','Excluídos: placas dos terminais, parafusos, mão, deformação, tolerâncias, eixo real da piano, rebaixos e resistência.','Almofadas retiradas para giro; corpo do saco mantido sem alteração.'],
 articuladores=results,tampas=lid_results,poses_ilustrativas=poses,
 pivo=dict(modelo='Omega OMPCR 1020',ombro=20,rosca=13.25,cabeca=7,total_axial=40.25,faixa_lateral=52,sobra_bruta=11.75,
 limite='Só envelope do parafuso, sem suporte/bucha/folgas nem acesso de ferramenta; não é pivô completo.'))
lever=abs((cmo[0]-6440)*(cf[1]-cmo[1])-(cmo[1]-120)*(cf[0]-cmo[0]))/291/1000
data['cesto_tracao_estatica']=dict(braco_efetivo_m=lever,torque_Nm=38.72533663933748,
 um_limitador_recebendo_tudo_N=38.72533663933748/lever,
 cada_um_divisao_ideal_N=38.72533663933748/lever/2,
 limite='Sem coeficiente de projeto, impacto, saco e metais adicionais. Não é capacidade exigida final nem valida a alegação comercial de 20 kg.')
(P/'Resultados.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(dict(articuladores=[dict(id=r['id'],fixed=r['fixed'],mobile=r['mobile'],hits=r['primeiras_colisoes'],envelope=r['envelope']) for r in results],tampas=lid_results),ensure_ascii=True,indent=2))
