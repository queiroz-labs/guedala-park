"""Checagem independente dos arquivos de resultado, sem importar o resolvedor."""
from pathlib import Path
import json,hashlib,csv
import numpy as np
HERE=Path(__file__).resolve().parent
D=json.loads((HERE/'Geometria_interfaces.json').read_text(encoding='utf-8'))
R=json.loads((HERE/'Resultados_caixa.json').read_text(encoding='utf-8'))
G=9.80665
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert sha(D['source'])==D['source_sha256']==R['source_sha256']
for name,value in R['input_sha256'].items():assert sha(HERE/name)==value
checks=[];csvrows=[]
for ex in R['panel_equilibrium_examples']:
 lm=ex['load_map'];names=list(lm)
 def balance(solution):
  F={n:np.zeros(3)for n in names};M={n:np.zeros(3)for n in names}
  for n,rows in lm.items():
   for r in rows:
    force=np.array([0.,0.,-r['mass_kg']*G]);F[n]+=force;M[n]+=np.cross(r['com_mm'],force)
  for value,m in zip(solution,ex['variables']):
   force=np.zeros(3);couple=np.zeros(3)
   if m['kind']=='joint_to_design':
    component=m['component']
    if component<3:force[component]=value
    else:couple[component-3]=value*1000
   else:
    assert value>=-1e-6,(ex['case'],m,value)
    force[m['axis']]=value*m['sign_on_a']
   moment=np.cross(m['point_mm'],force)+couple
   for n,sign in [(m['a'],1),(m['b'],-1)]:
    if n=='PISO':continue
    F[n]+=sign*force;M[n]+=sign*moment
  return max(np.max(abs(f))for f in F.values()),max(np.max(abs(m))for m in M.values())
 base=np.array(ex['solution']);force_error,moment_error=balance(base)
 assert force_error<1e-5 and moment_error<.01
 null=ex['internal_selfstress'];ids=null['variable_indices'];z=np.array(null['null_vector'])
 assert np.linalg.norm(z)>.01
 varied=base.copy();varied[ids]+=1000*z
 varied_force_error,varied_moment_error=balance(varied)
 assert varied_force_error<1e-5 and varied_moment_error<.01
 assert all(varied[i]==base[i]for i,m in enumerate(ex['variables'])if m['kind']!='joint_to_design')
 assert max(abs(varied-base))>10
 checks.append({'case':ex['case'],'route':ex['route'],'max_body_force_residual_N':force_error,'max_body_moment_residual_Nmm':moment_error,'selfstress_1000_passed':True,'selfstress_max_component_delta':float(max(abs(varied-base)))})
 for k,j in ex['joints_to_design'].items():csvrows.append([ex['case'],ex['route'],k,j['a'],j['b'],*j['point_mm'],*j['force_N'],*j['moment_Nmm'],'representante algebraico;nao envelope;demanda real depende da junta'])
# Prova local simples: topoP03 so teria apoio vertical traseiro emY3922..3940
# se todas as ligacoes laterais fossem contatos normais sem atrito. SeuCGY3606
# fica fora dessa faixa; equilibrio exige acao tangencial/casal nao presumido.
v=D['variants']['R52_sem_soco'];top=v['bodies']['Peca263']
weight=top['volume_mm3']*800/1e9*G
unbalanced=weight*(3922-top['com_mm'][1])/1000
assert unbalanced>0
legacy=json.loads((HERE.parents[1]/'P01_massas_equilibrio_2026-10-25/Geometria_R51.json').read_text(encoding='utf-8'))
included=set(v['bodies'])
missing=[r for r in legacy['wood']['P01']if r['name']not in included]
assert len(missing)==38
for c in R['cases']:
 # O envelope de um corte simples nao pode ter reacao negativa ou maior quepeso.
 for group,r in c['upper_modules'].items():
  for receiver,e in r['reactions_by_lower'].items():
   assert -1e-6<=e['min_N']<=e['max_N']+1e-6<=r['total']['weight_N']+1e-5
 # Somar as duas caixas e preciso no receptor compartilhado.
 e=c['shared_P01_receivers']['ReferenciaCorrerR003']
 for bound in ['min_N','max_N']:
  expected=sum(r['reactions_by_lower'].get('ReferenciaCorrerR003',{}).get(bound,0)for r in c['upper_modules'].values())
  assert abs(e[bound]-expected)<1e-7
with(HERE/'Ligacoes_exemplos.csv').open('w',encoding='utf-8-sig',newline='')as f:
 w=csv.writer(f,delimiter=';');w.writerow(['case','route','interface','a','b','x_mm','y_mm','z_mm','Fx_N','Fy_N','Fz_N','Mx_Nmm','My_Nmm','Mz_Nmm','meaning']);w.writerows(csvrows)
out={'source_unchanged':True,'source_sha256':D['source_sha256'],'body_equilibrium_cases':len(checks),'checks':checks,'upper_cut_cases':len(R['cases']),'top_P03_only_own_weight_at_rho800':{'weight_N':weight,'cgY_mm':top['com_mm'][1],'rear_support_minY_mm':3922,'minimum_missing_balance_about_rear_edge_Nm':unbalanced,'meaning':'necessidade de cisalhamento/casal nas ligacoes;nao momento de uma ferragem especifica'},'excluded_lower_P01_wood':{'count':len(missing),'mass_at_rho800_kg':sum(r['volume_mm3']for r in missing)*800/1e9,'names':[r['name']for r in missing],'meaning':'nao incluidos no caminho local por painel;usar inventario global anterior;nao tratar reacao de piso deste submodelo como total do roupeiro'},'physical_tests':0,'finite_joint_design_envelope':False}
(HERE/'Verificacao_caixa.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'body_equilibrium_cases':len(checks),'max_force_error_N':max(r['max_body_force_residual_N']for r in checks),'max_moment_error_Nmm':max(r['max_body_moment_residual_Nmm']for r in checks),'top_needed_Nm':unbalanced,'excluded_P01_mass_kg':out['excluded_lower_P01_wood']['mass_at_rho800_kg'],'source_unchanged':True}))
