import json, math
from pathlib import Path
P=Path(__file__).parent
obs=json.loads((P.parent/'Inventario/Folhas_ativas_globais_R44.json').read_text(encoding='utf8'))
def clip(poly,k,v,sign):
 out=[]
 for a,b in zip(poly,poly[1:]+poly[:1]):
  ia=sign*(a[k]-v)>=-1e-9; ib=sign*(b[k]-v)>=-1e-9
  if ia:out.append(a)
  if ia!=ib:
   t=(v-a[k])/(b[k]-a[k]);out.append(tuple(a[j]+t*(b[j]-a[j]) for j in [0,1]))
 return out
def area(p):return abs(sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(p,p[1:]+p[:1])))/2 if len(p)>2 else 0
tests=[]
for lid,y0,y1 in [('BancoR43_Painel1',3751,4722),('BancoR43_Painel2',4724,5549)]:
 relevant=[o for o in obs if o['name'] not in [lid,'BancoR43_Almofada1','BancoR43_Almofada2'] and o.get('bbox') and max(abs(c) for c in o['bbox'])<1e9 and min(y1,o['bbox'][4])-max(y0,o['bbox'][1])>1e-6 and (o.get('volume',0)>1e-6 or o['name']=='Fechada_110Tampo')]
 for ax in [100,102,110]:
  for az in [425,430,435]:
   hit={}; minx=1e9;minz=1e9;maxx=-1e9;maxz=-1e9
   for step in range(901):
    deg=step/10;t=math.radians(deg);c=math.cos(t);s=math.sin(t)
    p=[(ax+(x-ax)*c-(z-az)*s,az+(x-ax)*s+(z-az)*c) for x,z in [(102,400),(550,400),(550,420),(102,420)]]
    minx=min(minx,*[v[0] for v in p]);maxx=max(maxx,*[v[0] for v in p]);minz=min(minz,*[v[1] for v in p]);maxz=max(maxz,*[v[1] for v in p])
    for o in relevant:
     if o['name'] in hit:continue
     b=o['bbox'];q=p
     if b[5]-b[2]>1e-6:
      for k,v,sg in [(0,b[0],1),(0,b[3],-1),(1,b[2],1),(1,b[5],-1)]:q=clip(q,k,v,sg)
      val=area(q)*(min(y1,b[4])-max(y0,b[1]))
     else:
      xs=[]
      for a,bb in zip(p,p[1:]+p[:1]):
       if min(a[1],bb[1])-1e-8<=b[2]<=max(a[1],bb[1])+1e-8:
        if abs(a[1]-bb[1])<1e-8:xs.extend([a[0],bb[0]])
        else:xs.append(a[0]+(b[2]-a[1])*(bb[0]-a[0])/(bb[1]-a[1]))
      val=max(0,min(max(xs),b[3])-max(min(xs),b[0])) if xs else 0
     if val>1e-4:hit[o['name']]={'angle':deg,'label':o['label'],'intersecao_bbox_ou_superficie':val}
   tests.append(dict(tampa=lid,eixo_xz=[ax,az],poses=901,primeiras_colisoes=hit,varredura_x=[minx,maxx],varredura_z=[minz,maxz],tampa90_x=[ax+az-420,ax+az-400],tampa90_z=[az+102-ax,az+550-ax]))
out={'limites':'Triagem 2D extrudida contra AABB R44 e tampo Berlin como superfície. Eixo abstrato, não CAD da Southco. Almofadas removidas antes do giro. Não inclui ferragens, suportes, pessoas, deformação ou tolerâncias. Eixos positivos para frente acima da tampa não garantem folga da quina inferior.','testes':tests}
(P/'Banco_eixo_superior.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps([{'tampa':x['tampa'],'eixo':x['eixo_xz'],'hits':list(x['primeiras_colisoes'])} for x in tests],indent=2))
