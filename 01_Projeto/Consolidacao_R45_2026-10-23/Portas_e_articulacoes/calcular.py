import json, math, pathlib, html
P=pathlib.Path(__file__).parent
project=P.parents[1]
families=[('Pia',322,718,18,2,2),('Depurador',322,590,18,2,2),('Uso diário',270.5,1016,18,2,3),('Micro-ondas',345.5,608,18,2,2),('Geladeira',397.5,582,18,2,2),('Lavanderia',414.5,578,18,2,2),('Escritório',496,548,18,4,2),('Cabeceira A',439.75,306,18,2,2),('Cabeceira B',440.25,306,18,2,2),('Gabinete banheiro',297,543,18,2,2),('Espelheiro',297,748,18,2,3),('Roupeiro correr',995,1999,18,2,0),('Maleiro correr',670,237,18,2,0)]
families=[f for f in families if f[0]!='Gabinete banheiro']
families.extend([('Canto A/B',271,306,18,2,2),('Banheiro correr R43',292,500,18,2,0)])
calc=[]
for name,w,h,t,n,hinges in families:
 v=w*h*t/1e9
 glass=w*h*4/1e9*2500 if name=='Espelheiro' else 0
 calc.append(dict(familia=name,dim_mm=[w,h,t],folhas=n,dobradicas_por_folha=hinges,volume_m3=v,vidro_hipotese_kg=glass,massa_650_kg=v*650+glass,massa_750_kg=v*750+glass,massa_900_kg=v*900+glass,momento_peso_eixo_vertical_900_Nm=(v*900+glass)*9.80665*w/2000,formato_altura_maior_largura=h>w))
bank=[]
for w in [971,825]:
 for rho in [650,750,800,900]:
  m=w*448*20/1e9*rho
  bank.append(dict(largura=w,densidade=rho,massa=m,torque_Nm=m*9.80665*.224,S_AT01S_par_entre_12_2_e_17_6=12.2<=m*9.80665*.224<=17.6))
def clip(poly,axis,lim,sign):
 out=[]
 for a,b in zip(poly,poly[1:]+poly[:1]):
  ia=sign*(a[axis]-lim)>=-1e-9;ib=sign*(b[axis]-lim)>=-1e-9
  if ia:out.append(a)
  if ia!=ib:
   t=(lim-a[axis])/(b[axis]-a[axis]);out.append(tuple(a[j]+t*(b[j]-a[j]) for j in range(2)))
 return out
def area(poly):return abs(sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(poly,poly[1:]+poly[:1])))/2 if len(poly)>2 else 0
obstacles=json.loads((P.parent/'Inventario/Folhas_ativas_globais_R44.json').read_text(encoding='utf8'))
tests=[]
excluded=['BancoR43_Almofada1','BancoR43_Almofada2']
for lid,y0,y1 in [('BancoR43_Painel1',3751,4722),('BancoR43_Painel2',4724,5549)]:
 for ax in [548,550]:
  hits=[];surface_hits=[];xmin=1e9;xmax=-1e9;zmax=-1e9
  relevant=[o for o in obstacles if o['name'] not in excluded+[lid] and o.get('volume',0)>1e-6 and o.get('bbox') and max(abs(c) for c in o['bbox'])<1e9 and min(y1,o['bbox'][4])-max(y0,o['bbox'][1])>1e-6]
  surfaces=[o for o in obstacles if o['name']=='Fechada_110Tampo']
  for ai in range(901):
   angle=ai/10;t=math.radians(angle);c=math.cos(t);s=math.sin(t)
   poly=[(ax+(x-ax)*c+(z-400)*s,400-(x-ax)*s+(z-400)*c) for x,z in [(102,400),(550,400),(550,420),(102,420)]]
   xmin=min(xmin,min(q[0] for q in poly));xmax=max(xmax,max(q[0] for q in poly));zmax=max(zmax,max(q[1] for q in poly))
   for ob in relevant:
    b=ob['bbox'];q=poly
    for coord,lim,sign in [(0,b[0],1),(0,b[3],-1),(1,b[2],1),(1,b[5],-1)]:q=clip(q,coord,lim,sign)
    vol=area(q)*(min(y1,b[4])-max(y0,b[1]))
    if vol>1e-4:hits.append(dict(angle=angle,obstacle=ob['name'],label=ob['label'],volume_bbox_intersecao_mm3=vol))
   for ob in surfaces:
    b=ob['bbox'];zz=b[2];xs=[]
    for a,bb in zip(poly,poly[1:]+poly[:1]):
     if min(a[1],bb[1])-1e-8<=zz<=max(a[1],bb[1])+1e-8:
      if abs(a[1]-bb[1])<1e-8:xs.extend([a[0],bb[0]])
      else:xs.append(a[0]+(zz-a[1])*(bb[0]-a[0])/(bb[1]-a[1]))
    if xs:
     width=min(max(xs),b[3])-max(min(xs),b[0]);depth=min(y1,b[4])-max(y0,b[1])
     if width>1e-6 and depth>1e-6:surface_hits.append(dict(angle=angle,obstacle=ob['name'],area_intersecao_mm2=width*depth,largura_intersecao_mm=width))
  tests.append(dict(tampa=lid,eixo=[ax,400],poses=901,obstaculos_bbox=len(relevant),colisoes_bbox=len(hits),primeiras=hits[:10],superficies_fisicas_testadas=[o['name'] for o in surfaces],colisoes_superficie=len(surface_hits),primeira_superficie=surface_hits[0] if surface_hits else None,varredura_x=[xmin,xmax],z_max=zmax,abertura90_x=[ax,ax+20],abertura90_z=[400-(550-ax),400-(102-ax)],natureza='Triagem por retângulo da tampa contra AABB global e superfície física da Berlin. Não CAD Rockler. Não inclui usuário/ferragem/tolerância.'))
data={'premissas':'Massas por volume geométrico bruto, sem descontar canecos; densidades são cenários, não material confirmado. Vidro2500kg/m³ hipotético. Acrescentar acabamento, adesivo, pegas e ferragens móveis.','portas':calc,'banco':bank,'abertura_frontal':tests}
(P/'Calculos.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'portas':len(calc),'ensaios_frente':tests},ensure_ascii=False,indent=2))
