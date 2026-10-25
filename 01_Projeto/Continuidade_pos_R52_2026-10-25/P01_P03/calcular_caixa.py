"""Equilibrio por painel e envelopes estaticos; nenhuma rigidez/capacidade atribuida.

Requer Python+NumPy. A geometria e extraida por extrair_interfaces.py emFreeCADCmd.
Juntas positivas sao RESULTANTES A PROJETAR, sem resistencia infinita aprovada.
O representante de norma minima so demonstra equilibrio; nao prediz partilha.
"""
from pathlib import Path
import json,hashlib,itertools,csv,time
import numpy as np
HERE=Path(__file__).resolve().parent
G=9.80665
D=json.loads((HERE/'Geometria_interfaces.json').read_text(encoding='utf-8'))
P03={'Peca259','Peca260','Peca261','Peca262','Peca263'}
P01={'Peca206','Peca207','Peca208','Peca209','Peca210','ReferenciaCorrerR14','ReferenciaCorrerR001','ReferenciaCorrerR002','ReferenciaCorrerR003'}
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert sha(D['source'])==D['source_sha256']

def loads(variant,rho,kg,placement,p02=True):
 bodies=variant['bodies'];out={n:[]for n in bodies if p02 or n!='P02_resultante'}
 def add(n,mass,c,label):
  out[n].append({'mass_kg':float(mass),'com_mm':list(map(float,c)),'label':label})
 for n in out:
  r=bodies[n];add(n,r['volume_mm3']*rho/1e9,r['com_mm'],'madeira nominal: '+n)
 # As duas folhas sao transferidas a base pelo seu proprio resultante; nao
 # uniformizadas sobre toda a base ou convertidas em peso de trilho comercial.
 for r in D['doors']:
  c=r['com_global_mm'];add('Peca262',r['volume_mm3']*rho/1e9,c,'folha RO62, equivalente gravitacional: '+r['name'])
 y=3320. if placement=='front60' else 3606.
 add('Peca262',kg,[6065,y,2160],'conteudo hipoteticoP03: '+placement)
 if p02:add('P02_resultante',kg,[7115,3300,2290],'conteudo hipoteticoP02; caixa agregada')
 return out

def aggregate(loadmap,names):
 ll=[r for n in names if n in loadmap for r in loadmap[n]]
 mass=sum(r['mass_kg']for r in ll)
 com=sum((r['mass_kg']*np.array(r['com_mm'])for r in ll),np.zeros(3))/mass
 return {'mass_kg':mass,'weight_N':mass*G,'com_mm':com.tolist()}

def upper_points(v,group):
 rows=[]
 for k,f in enumerate(v['interfaces']):
  if f['axis']!=2:continue
  if f['a']in group and f['b']in P01:upper,lower=f['a'],f['b']
  elif f['b']in group and f['a']in P01:upper,lower=f['b'],f['a']
  else:continue
  # Existing nominal contacts are all atZ2132, with upper above lower.
  if abs(f['center_mm'][2]-2132)>1e-6:continue
  for j,p in enumerate(f['vertices_mm']):rows.append({'point':p,'lower':lower,'upper':upper,'interface':k,'vertex':j})
 return rows

def prepare_cut(v,group):
 pts=upper_points(v,group)
 A=np.array([[1,(r['point'][0]-6390)/1000,(r['point'][1]-3615)/1000]for r in pts]).T
 triples=[];inverses=[]
 for ix in itertools.combinations(range(len(pts)),3):
  a=A[:,ix]
  if abs(np.linalg.det(a))<1e-11:continue
  triples.append(ix);inverses.append(np.linalg.inv(a))
 return {'points':pts,'A':A,'triples':np.array(triples,int),'inv':np.array(inverses)}

def cut_solutions(cut,total):
 b=total['weight_N']*np.array([1,(total['com_mm'][0]-6390)/1000,(total['com_mm'][1]-3615)/1000])
 rs=np.einsum('kij,j->ki',cut['inv'],b)
 ok=np.min(rs,axis=1)>=-1e-7
 rs=rs[ok];triples=cut['triples'][ok]
 if not len(rs):return {'feasible':False,'reason':'CG fora do fecho convexo dos contatos nominais; contato sozinho nao equilibra o conjunto.'},None
 assert np.max(abs(np.einsum('kij,kj->ki',np.transpose(cut['A'][:,triples],(1,0,2)),rs)-b))<1e-5
 lower=sorted(set(r['lower']for r in cut['points']))
 env={};extremes={}
 for n in lower:
  mask=np.array([r['lower']==n for r in cut['points']])
  values=np.sum(rs*mask[triples],axis=1)
  lo,hi=int(np.argmin(values)),int(np.argmax(values))
  env[n]={'min_N':float(values[lo]),'max_N':float(values[hi])}
  extremes[n]={}
  for label,i in [('min',lo),('max',hi)]:
   x=np.zeros(len(cut['points']));x[triples[i]]=rs[i];extremes[n][label]=x
 return {'feasible':True,'feasible_basic_solutions':len(rs),'contact_vertex_count':len(cut['points']),'reactions_by_lower':env,'total':total},extremes

def skew(v):
 x,y,z=v;return np.array([[0,-z,y],[z,0,-x],[-y,x,0.]])

def network(v,loadmap,cut_fixed=None,bear_only=False,allow_cross_joint=False):
 names=list(loadmap);ix={n:i for i,n in enumerate(names)};N=len(names)*6
 cols=[];meta=[];positive=[];fixed={}
 def add_column(a,b,point,force,couple,description,nonnegative):
  col=np.zeros(N)
  for n,sign in [(a,1),(b,-1)]:
   if n=='PISO':continue
   k=6*ix[n];lever=(np.array(point)-v['bodies'][n]['com_mm'])/1000
   col[k:k+3]+=sign*np.array(force)
   col[k+3:k+6]+=sign*(skew(lever)@force+np.array(couple))
  meta.append(description);cols.append(col)
  if nonnegative:positive.append(len(cols)-1)
 def add_face(f,k,is_floor=False):
  a,b=f['a'],f['b']
  if a not in ix or (b!='PISO'and b not in ix):return
  axis=f['axis'];p=np.array(f['center_mm'])
  aabove=b=='PISO' or v['bodies'][a]['com_mm'][axis]>v['bodies'][b]['com_mm'][axis]
  signed=1 if aabove else -1
  # Nao atribuir implicitamente uma juntaP02/P03 pela mera proximidade emX6740.
  if not allow_cross_joint and ((a=='P02_resultante'and b in P03)or(b=='P02_resultante'and a in P03)):return
  if axis==2 or bear_only:
   for j,point in enumerate(f['vertices_mm']):
    force=np.eye(3)[axis]*signed
    add_column(a,b,point,force,np.zeros(3),{'kind':'floor'if is_floor else 'compression','interface':k,'a':a,'b':b,'point_mm':point,'axis':axis,'sign_on_a':signed,'vertex':j},True)
    if cut_fixed and (k,j)in cut_fixed:
     fixed[len(cols)-1]=float(cut_fixed[k,j])
  else:
   for component in range(6):
    force=np.eye(3)[component]if component<3 else np.zeros(3)
    couple=np.eye(3)[component-3]if component>=3 else np.zeros(3)
    add_column(a,b,p,force,couple,{'kind':'joint_to_design','interface':k,'a':a,'b':b,'point_mm':p.tolist(),'component':component},False)
 for k,f in enumerate(v['interfaces']):add_face(f,k)
 for k,f in enumerate(v['floor_faces']):add_face(f,-k-1,True)
 A=np.array(cols).T;b=np.zeros(N)
 for n,rows in loadmap.items():
  ref=np.array(v['bodies'][n]['com_mm']);k=6*ix[n]
  for r in rows:
   ff=np.array([0,0,-r['mass_kg']*G]);b[k:k+3]-=ff;b[k+3:k+6]-=skew((np.array(r['com_mm'])-ref)/1000)@ff
 return A,b,meta,np.array(positive,int),fixed,names

def equilibrium(A,b,positive,fixed):
 """Ativacao de limites no representante de norma minima, sem lei material.
 Se falhar, nao converte resultado aproximado em equilibrio ou aprovacao.
 """
 mask=np.ones(A.shape[1],bool);rhs=b.copy();x=np.zeros(A.shape[1])
 for k,value in fixed.items():mask[k]=False;x[k]=value;rhs-=A[:,k]*value
 bounded=set(positive)-set(fixed);clamped=set();history=set()
 for it in range(1000):
  free=np.flatnonzero(mask);Af=A[:,free]
  # Pseudoinversa: nao ha rigidez ou deslocamento implicito nesta solucao.
  lagrange=-np.linalg.lstsq(Af@Af.T,rhs,rcond=1e-11)[0]
  x[free]=-Af.T@lagrange
  err=float(np.max(abs(A@x-b)))
  negative=[k for k in bounded if mask[k] and x[k]<-1e-7]
  if negative:
   worst=min(negative,key=lambda k:x[k]);mask[worst]=False;x[worst]=0;clamped.add(worst);continue
  violation=[k for k in clamped if A[:,k]@lagrange < -1e-7]
  if violation:
   worst=min(violation,key=lambda k:A[:,k]@lagrange);mask[worst]=True;clamped.remove(worst)
   key=tuple(sorted(clamped))
   if key in history:return None,{'feasible':False,'reason':'ativacao ciclou; nao certificado','residual_N_equivalent':err,'iterations':it+1}
   history.add(key);continue
  if err>1e-5:return None,{'feasible':False,'reason':'equacoes incompativeis no conjunto ativo','residual_N_equivalent':err,'iterations':it+1}
  assert min([x[k]for k in positive]+[0])>=-1e-6
  return x,{'feasible':True,'max_force_or_moment_over1000_residual':err,'minimum_compression_N':float(min(x[positive])),'iterations':it+1,'clamped_contacts':len(clamped)}
 return None,{'feasible':False,'reason':'limite iteracoes'}

def joint_report(x,meta):
 rows={}
 for value,m in zip(x,meta):
  if m['kind']!='joint_to_design':continue
  k=str(m['interface'])
  if k not in rows:rows[k]={'a':m['a'],'b':m['b'],'point_mm':m['point_mm'],'force_N':[0.]*3,'moment_Nmm':[0.]*3}
  c=m['component']
  if c<3:rows[k]['force_N'][c]=float(value)
  else:rows[k]['moment_Nmm'][c-3]=float(value*1000)
 return rows

def main():
 started=time.perf_counter();cases=[];examples=[];verification=[];interfaces=[]
 for variant,v in D['variants'].items():
  cuts={'P03':prepare_cut(v,P03),'P02':prepare_cut(v,{'P02_resultante'}),'coupled':prepare_cut(v,P03|{'P02_resultante'})}
  for k,f in enumerate(v['interfaces']):interfaces.append({'variant':variant,'index':k,**f})
  for rho,kg,place in itertools.product([650,800,900],[0,10,20],['distributed','front60']):
   lm=loads(v,rho,kg,place)
   summaries={};ext={}
   for code,group in [('P03',P03),('P02',{'P02_resultante'})]:
    summaries[code],ext[code]=cut_solutions(cuts[code],aggregate(lm,group))
   coupled,coupled_ext=cut_solutions(cuts['coupled'],aggregate(lm,P03|{'P02_resultante'}))
   assert all(r['feasible']for r in summaries.values())
   front='ReferenciaCorrerR003';back='Peca208'
   shared={}
   for target in [front,back]:
    shared[target]={bound+'_N':sum(summaries[c]['reactions_by_lower'].get(target,{}).get(bound+'_N',0)for c in summaries)for bound in ['min','max']}
   # Equilibrio global no corte e exato; extremos individuais nao sao simultaneos.
   caseid=f'{variant}_rho{rho}_kg{kg}_{place}'
   cases.append({'id':caseid,'variant':variant,'rho_hypothesis_kg_m3':rho,'content_each_upper_kg':kg,'content_P03_placement':place,'upper_modules':summaries,'shared_P01_receivers':shared,'if_P02_P03_positive_cross_joint_is_designed':coupled})
   if rho==800 and kg==20 and place=='front60':
    for route in ['front_min','front_max','back_max','coupled_front_min']:
     target=back if route=='back_max'else front;direction='min'if route=='front_min'else'max'
     prescribed={}
     if route=='coupled_front_min':
      vals=coupled_ext[front]['min']
      for r,value in zip(cuts['coupled']['points'],vals):prescribed[r['interface'],r['vertex']]=float(value)
     else:
      for code in ['P03','P02']:
       target2=target if target in ext[code]else front
       vals=ext[code][target2][direction]
       for r,value in zip(cuts[code]['points'],vals):prescribed[r['interface'],r['vertex']]=float(value)
     A,b,meta,nn,fixed,names=network(v,lm,prescribed,allow_cross_joint=route=='coupled_front_min')
     x,check=equilibrium(A,b,nn,fixed)
     ex={'case':caseid,'route':route,'equilibrium':check,'body_count':len(names),'equations':A.shape[0],'unknowns':A.shape[1]}
     if x is not None:
      ex['load_map']=lm;ex['variables']=meta;ex['solution']=x.tolist()
      ex['joints_to_design']=joint_report(x,meta)
      ex['floor_total_N']=float(sum(value for value,m in zip(x,meta)if m['kind']=='floor'))
      ex['total_model_weight_N']=aggregate(lm,set(lm))['weight_N']
      assert abs(ex['floor_total_N']-ex['total_model_weight_N'])<1e-4
      # Prova de nao unicidade: projetar coordenada de junta no nucleo deA.
      j=next(i for i,m in enumerate(meta)if m['kind']=='joint_to_design'and m['component']==2 and m['a']in P03 and m['b']in P03)
      e=np.zeros(A.shape[1]);e[j]=1
      # Fixar todos os contatos mantem reacoes de apoio identicas. Ainda ha
      # autoequilibrios internos que alteram solicitacao da junta sem alterarpeso.
      js=[i for i,m in enumerate(meta)if m['kind']=='joint_to_design'];Aj=A[:,js]
      ej=np.zeros(len(js));ej[js.index(j)]=1
      z=ej-Aj.T@np.linalg.lstsq(Aj@Aj.T,Aj@ej,rcond=1e-11)[0]
      ex['internal_selfstress']={'residual':float(np.max(abs(Aj@z))),'norm':float(np.linalg.norm(z)),'selected_joint_component':meta[j],'variable_indices':js,'null_vector':z.tolist()}
      assert ex['internal_selfstress']['residual']<1e-6
     examples.append(ex)
  # Sem juntas tangenciais/positivas, teste somente superficies sem atrito.
  lm=loads(v,800,0,'distributed');A,b,meta,nn,fixed,names=network(v,lm,bear_only=True)
  trial=np.linalg.lstsq(A,b,rcond=1e-11)[0];res=A@trial-b
  # Mesmo liberando o sinal de TODAS as normais, o residuo prova incompatibilidade.
  verification.append({'variant':variant,'frictionless_normal_contacts_only':{'algebraic_residual_norm':float(np.linalg.norm(res)),'max_force_or_moment_over1000_residual':float(np.max(abs(res))),'feasible_even_with_tension':bool(np.max(abs(res))<1e-5)},'bodies':len(names),'interfaces':len(v['interfaces']),'floor_patches':len(v['floor_faces'])})
 assert all(not r['frictionless_normal_contacts_only']['feasible_even_with_tension']for r in verification)
 assert all(r['equilibrium']['feasible']for r in examples),[(r['case'],r['route'],r['equilibrium'])for r in examples if not r['equilibrium']['feasible']]
 assert sha(D['source'])==D['source_sha256']
 out={'source_sha256':D['source_sha256'],'input_sha256':{p.name:sha(p)for p in [HERE/'calcular_caixa.py',HERE/'extrair_interfaces.py',HERE/'Geometria_interfaces.json']},'method':'equilibrio6porcorpo + envelope exato de3equacoes no corte superior; sem E,nu,K,resistencia ou carga liberada','g_m_s2':G,'cases':cases,'panel_equilibrium_examples':examples,'frictionless_checks':verification,'runtime_s':time.perf_counter()-started,'physical_tests':0,'source_unchanged':True}
 (HERE/'Resultados_caixa.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 (HERE/'Interfaces_nominais.json').write_text(json.dumps(interfaces,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 with (HERE/'Envelopes_superiores.csv').open('w',encoding='utf-8-sig',newline='')as f:
  writer=csv.writer(f,delimiter=';');writer.writerow(['case','module','receiver','minimum_N','maximum_N','meaning'])
  for c in cases:
   for code,r in c['upper_modules'].items():
    for receiver,env in r['reactions_by_lower'].items():writer.writerow([c['id'],code,receiver,env['min_N'],env['max_N'],'limites estaticos;semcapacidade;extremosnaosimultaneos'])
 print(json.dumps({'cases':len(cases),'panel_examples':len(examples),'runtime_s':out['runtime_s'],'verification':verification,'examples':[{'case':r['case'],'route':r['route'],'equilibrium':r['equilibrium']}for r in examples]},ensure_ascii=False))
if __name__=='__main__':main()
