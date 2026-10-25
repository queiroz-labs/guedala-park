"""Inventario de massa e equilibrio rigido condicional; nao capacidade de piso."""
from pathlib import Path
import json,hashlib,itertools
import numpy as np
HERE=Path(__file__).resolve().parent
geo_path=HERE/'Geometria_R51.json';soco_path=HERE.parent/'P01_apoios_ao_piso_2026-10-25/Resultados.json'
D=json.loads(geo_path.read_text(encoding='utf8'));S=json.loads(soco_path.read_text(encoding='utf8'));G=9.80665
assert hashlib.sha256(Path(D['cad']).read_bytes()).hexdigest()==D['sha256']
GROUPS=['Gaveta','Gaveta001','Gaveta002','Gaveta003']
def centroid(rows):
 v=sum(r['volume_mm3'] for r in rows)
 return dict(count=len(rows),volume_m3=v/1e9,com_mm=(sum((r['volume_mm3']*np.array(r['com_global_mm']) for r in rows),np.zeros(3))/v).tolist(),mass_at650_800_900_kg=[v*rho/1e9 for rho in (650,800,900)])
inventory={k:centroid(v) for k,v in D['wood'].items()}
floor=[dict(name=p['id'],xy_mm=p['origin_mm'][:2],size_mm=p['size_mm'][:2]) for p in S['new_boards']]
for r in D['wood']['P01']:
 b=r['bbox_global_mm']
 if abs(b[2])<1e-8:floor.append(dict(name=r['name'],xy_mm=b[:2],size_mm=[b[3]-b[0],b[4]-b[1]]))
assert len(floor)==23
area=sum(np.prod(r['size_mm']) for r in floor);assert abs(area-270720)<1e-6
for i,a in enumerate(floor):
 for b in floor[i+1:]:
  overlap=[min(a['xy_mm'][j]+a['size_mm'][j],b['xy_mm'][j]+b['size_mm'][j])-max(a['xy_mm'][j],b['xy_mm'][j]) for j in range(2)]
  assert not all(v>1e-6 for v in overlap)
# Referencias de conjunto: 4 extremos do retangulo que e o fecho convexo dos apoios.
XMIN,XMAX,YMIN,YMAX=5390.,7390.,3290.,3940.
def load_rows(rho,level,p02,mirror,hardware,opened,doors):
 loads=[]
 def add(mass,com,label):
  if mass:loads.append((float(mass),np.array(com,float),label))
 for code in ['P01','P03']+(['P02'] if p02 else []):
  for r in D['wood'][code]:
   c=np.array(r['com_global_mm']);m=r['volume_mm3']*rho/1e9
   if code=='P01':
    parent=next((n for n in GROUPS if n in r['parents']),None)
    if parent:c[1]-=opened[GROUPS.index(parent)]*500
    if r['name']=='Peca247':c[0]-=doors[0]*965
    if r['name']=='Peca248':c[0]+=doors[1]*965
   add(m,c,r['name'])
 for p in S['new_boards']:
  size=np.array(p['size_mm']);add(float(np.prod(size))*rho/1e9,np.array(p['origin_mm'])+size/2,p['id'])
 # Duas extensoes18x550x18 da proposta723, sem mover o restante da prateleira.
 for x in (6649.,6113.):add(18*550*18*rho/1e9,[x+9,3647,1091],'extensao723')
 if mirror:add(D['mirror_reservation']['volume_mm3']*2500/1e9,D['mirror_reservation']['com_global_mm'],'vidro2500_hipotese')
 add(hardware,[6390,3615,1100],'massa_adicional_parametrica_nao_medida')
 # Niveis0/1/2 sao cenarios simultaneos, nao recomendacao de armazenamento.
 for x in (5594.5,7194.5):
  for z in (340,600,800):add(5*level,[x,3572,z+50],'sapateira_conteudo')
 for x in (5769.5,7010.5):add(10*level,[x,3647,1150],'prateleira723_conteudo')
 for x in (5894.5,6885.5):add(10*level,[x,3655,1850],'varao_alto_conteudo')
 for x in (5947.,6833.):add(5*level,[x,3655,950],'varao_baixo_conteudo')
 for i,(x,z) in enumerate([(7194.5,870),(7194.5,1020),(5585.5,870),(5585.5,1020)]):
  add(5*level,[x,3420-opened[i]*500,z],'gaveta_conteudo_frontal')
 add(10*level,[6065,3606,2290],'maleiro_conteudo')
 if p02:add(10*level,[7115,3300,2290],'P02_conteudo_parametrico')
 return loads
def summarize(loads):
 m=sum(r[0] for r in loads);cg=sum((mass*c for mass,c,_ in loads),np.zeros(3))/m;W=m*G
 moments=np.array([cg[1]-YMIN,YMAX-cg[1],cg[0]-XMIN,XMAX-cg[0]])*W/1000
 return dict(mass_kg=m,cg_mm=cg.tolist(),weight_N=W,resisting_moments_Nm=dict(zip(['front','rear','left','right'],moments.tolist())),
  horizontal_force_at2440_to_zero_front_moment_N=float(moments[0]/2.440),
  nominal_area_m2=float(area/1e6),average_pressure_kPa=float(W/area*1000),
  pressure_if25percent_kPa=float(W/(area*.25)*1000),pressure_if5percent_kPa=float(W/(area*.05)*1000))
def floor_grid(n=24):
 # Amostragem de leito de contato uniforme por area sob corpo rigido; sem rigidez fisica atribuida.
 xy=[];areas=[];ids=[]
 for i,r in enumerate(floor):
  x,y=r['xy_mm'];a,b=r['size_mm'];nx=max(1,round(n*a/1964));ny=max(1,round(n*b/1964))
  for ix in range(nx):
   for iy in range(ny):xy.append([x+(ix+.5)*a/nx,y+(iy+.5)*b/ny]);areas.append(a*b/(nx*ny));ids.append(i)
 return np.array(xy),np.array(areas),np.array(ids)
def pressure_model(c,n=48):
 xy,A,ids=floor_grid(n);V=np.column_stack([np.ones(len(A)),xy[:,0]-6390,xy[:,1]-3615]);rhs=c['weight_N']*np.array([1,c['cg_mm'][0]-6390,c['cg_mm'][1]-3615])
 active=np.ones(len(A),bool)
 for it in range(100):
  coeff=np.linalg.solve((V[active].T*A[active])@V[active],rhs);pressure=V@coeff;new=pressure>0
  if np.array_equal(new,active):break
  active=new
 else:raise AssertionError('contato unilateral sem convergencia')
 R=A*np.maximum(pressure,0);error=V.T@R-rhs;assert abs(error).max()<1e-5
 forces=[float(R[ids==i].sum()) for i in range(len(floor))]
 return dict(grid_degree=n,active_fraction_area=float(A[active].sum()/area),max_sample_pressure_kPa=float(max(pressure)*1000),
  force_by_floor_part_N=dict(zip([r['name'] for r in floor],forces)),force_moment_residual=float(abs(error).max()),
  note='Corpo rigido e leito uniforme por area, somente compressao. Nao prediz pressao real de calcos/vinil nem flexibilidade da caixa. Maximo e amostrado.')
def main():
 cols=['rho','content_level','P02_coupled','mirror_hypothesis','additional_mass_kg','drawer_bits','door_bits','total_kg','cgX','cgY','cgZ','front_Nm','rear_Nm','left_Nm','right_Nm','average_kPa']
 rows=[];envelopes=[]
 for rho,level,p02,mirror,hardware in itertools.product((650,800,900),(0,1,2),(0,1),(0,1),(0,10)):
  candidates=[]
  for opened in itertools.product((0,1),repeat=4):
   for doors in itertools.product((0,1),repeat=2):
    c=summarize(load_rows(rho,level,p02,mirror,hardware,opened,doors));db=sum(v<<i for i,v in enumerate(opened));pb=sum(v<<i for i,v in enumerate(doors))
    row=[rho,level,p02,mirror,hardware,db,pb,c['mass_kg'],*c['cg_mm'],*c['resisting_moments_Nm'].values(),c['average_pressure_kPa']];rows.append(row)
    candidates.append(dict(drawer_bits=db,door_bits=pb,**c))
  worst=min(candidates,key=lambda c:c['resisting_moments_Nm']['front'])
  closed=next(c for c in candidates if c['drawer_bits']==0 and c['door_bits']==0)
  assert abs(closed['mass_kg']-worst['mass_kg'])<1e-8
  assert worst['resisting_moments_Nm']['front']<=closed['resisting_moments_Nm']['front']+1e-7
  envelopes.append(dict(rho=rho,level=level,P02_coupled=p02,mirror_hypothesis=mirror,additional_mass_kg=hardware,worst_front=worst))
 assert len(rows)==4608
 examples=[]
 for rho,level,p02,mirror,hardware in [(650,0,0,0,0),(800,0,0,0,0),(900,2,1,1,10)]:
  c=summarize(load_rows(rho,level,p02,mirror,hardware,(1,1,1,1),(0,0)))
  a=pressure_model(c,48);b=pressure_model(c,96)
  assert abs(a['max_sample_pressure_kPa']/b['max_sample_pressure_kPa']-1)<.03
  examples.append(dict(rho=rho,level=level,P02_coupled=p02,mirror_hypothesis=mirror,additional_mass_kg=hardware,all_drawers_open=True,**c,contact_model=b,contact_convergence_relative=abs(a['max_sample_pressure_kPa']/b['max_sample_pressure_kPa']-1)))
 out=dict(source_sha256=D['sha256'],inventory=inventory,plinth_mass_800_kg=S['mass_nominal_kg_at_rho800'],shelf_extension_mass_800_kg=2*18*550*18*800/1e9,
  nominal_floor_parts=floor,nominal_floor_area_m2=float(area/1e6),added_plinth_area_m2=S['total_top_and_floor_nominal_area_mm2']/1e6,
  cases_columns=cols,cases_rows=rows,envelopes=envelopes,contact_examples=examples,
  input_sha256={p.name if p.parent==HERE else '../'+p.parent.name+'/'+p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [geo_path,soco_path,HERE/'calcular.py']},
  physical_tests=0,status='Massa nominal de madeiras e equilibrio rigido condicionado. Nao capacidade de piso, junta, ferragem ou armazenamento; conjuntos superiores e massas reais pendentes.')
 (HERE/'Resultados.json').write_text(json.dumps(out,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8')
 print(json.dumps(dict(inventory=inventory,case_count=len(rows),examples=examples),ensure_ascii=False))
if __name__=='__main__':main()
