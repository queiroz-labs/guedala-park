"""BaseP17: placa e caminhos axiais para referencia superior condicional.
Juntas/retencao sao requisitos a ensaiar, nao propriedades de fabricante.
"""
from pathlib import Path
import json,sys,hashlib,importlib.util
import numpy as np
HERE=Path(__file__).resolve().parent
helper_path=HERE.parent/'Solucoes_marcenaria_sem_tubos_2026-10-25/calcular.py'
spec=importlib.util.spec_from_file_location('funcoes_placa_existentes',helper_path)
helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
PlateModel=helper.PlateModel
GEO=json.loads((HERE.parent/'Aereos_suspensao_P09_P11_P12_P17_2026-10-25/Geometria_R51.json').read_text(encoding='utf8'))
M=GEO['modules']['P17'];L=M['width_mm'];B=312.;H=550.;DIVH=514.;t=17.7;tm=18.3;rho=800.;g=9.80665
DIVS=sorted(r['center_uvz_mm'][0] for r in M['body'] if r['name'].startswith('Apoio'))
assert np.allclose(DIVS,[473,973,991,1473])
BAYS=[(0.,464.),(482.,964.),(1000.,1464.),(1482.,1964.)]
def content(kind,kg):
 if kind=='one_bay':return [(kg,482.,964.,0.,B)]
 return [(kg/4,x0,x1,0.,60. if kind=='front' else B) for x0,x1 in BAYS]
def case(kind='uniform',kg=20.,n=18,E0=2200.,K0=500.,mode='full',rear_width=100.):
 E=E0/2;kd=K0/2;points=[(0.,72.),(0.,240.),(L,72.),(L,240.)]
 compliance=[1/kd]*4;v0=[0.]*4;mass_path=[0.]*4;roles=['side_path']*4
 divmass=18.3*B*DIVH*rho/1e9
 if mode=='full':
  A=t*(B/2)
  for x in DIVS:
   for y in (72.,240.):
    points.append((float(x),y));compliance.append(2/kd+DIVH/(E*A))
    mass_path.append(divmass/2);v0.append(divmass/2*g*(1/kd+DIVH/(2*E*A)));roles.append('divider_path')
 backmass=L*H*tm*rho/1e9
 if mode!='sides_only':
  rear=np.linspace(72,L-72,12);tributary=np.diff(np.r_[0,(rear[:-1]+rear[1:])/2,L])
  for x,w in zip(rear,tributary):
   A=t*min(rear_width,w);length=H-18;mass=backmass*w/L
   points.append((float(x),B));compliance.append(2/kd+length/(E*A))
   mass_path.append(mass);v0.append(mass*g*(1/kd+length/(2*E*A)));roles.append('back_path')
 model=PlateModel(n=n,E=E,L=L,B=B,t=t,supports=points,C=np.diag(compliance),v0=v0)
 own=L*B*tm*rho/1e9;rects=content(kind,kg)
 if mode!='full':
  # Sem credito da suspensao positiva das divisorias: peso delas sobre a base.
  rects += [(divmass,x-9,x+9,0,B) for x in DIVS]
 r=helper.solve(model,own,rects);R=np.array(r['reactions_N']);mass_path=np.array(mass_path)
 upper=R+mass_path*g
 total=own+kg+sum(mass_path)+(4*divmass if mode!='full' else 0)
 assert abs(upper.sum()-total*g)<1e-6
 return dict(kind=kind,content_only_kg=kg,degree=n,E_initial_MPa=E0,E_sensitivity_MPa=E,
  joint_K_initial_per_position_N_mm=K0,joint_K_sensitivity_per_position_N_mm=kd,mode=mode,rear_effective_width_mm=rear_width,
  **r,deflection_plus_reserve_mm=r['deflection_mm']+.2,reference_mm=500/300,
  own_divider_total_kg=4*divmass,own_back_kg=backmass if mode!='sides_only' else None,
  points_xy_mm=points,path_roles=roles,path_C_mm_N=compliance,path_v0_mm=v0,
  upper_group_force_N=upper.tolist(),modeled_top_force_sum_N=float(upper.sum()),
  local_total_mass_in_path_kg=total,min_base_reaction_N=float(R.min()),max_base_reaction_N=float(R.max()),
  max_abs_path_upper_N=float(np.max(np.abs(upper))),top_force_equilibrium_error_N=float(upper.sum()-total*g),
  scope='Referencia superior rigida condicional; reserva0.20 a comprovar na caixa/suspensao real. Caminhos axiais independentes, sem espalhamento/cisalhamento3D ou resistencia local aprovados.')
def main():
 assert hashlib.sha256(Path(GEO['cad']).read_bytes()).hexdigest()==GEO['sha256']
 cases=[];checks=[]
 for mode,kind,kg in [('sides_only','uniform',10.),('rear_only','uniform',20.),
                       ('full','uniform',10.),('full','uniform',20.),('full','front',20.),('full','one_bay',10.)]:
  a=case(mode=mode,kind=kind,kg=kg,n=16);b=case(mode=mode,kind=kind,kg=kg,n=20)
  rel=abs(a['deflection_mm']/b['deflection_mm']-1)
  assert rel<.05,(mode,kind,rel)
  residual=max(abs(b[k]) for k in ['eq_force_N','eq_moment_x_Nmm','eq_moment_y_Nmm','constraint_error_mm','top_force_equilibrium_error_N'])
  assert residual<1e-5,(mode,kind,residual)
  cases.append(b);checks.append(dict(mode=mode,kind=kind,kg=kg,degree16vs20_relative_error=rel,max_residual=residual,passed=True))
 for E0,K0,width in [(2200,250,100),(2200,1000,100),(1600,500,100),(1600,250,100),(1600,500,50)]:
  r=case(kind='front',kg=20,n=20,E0=E0,K0=K0,rear_width=width);cases.append(r)
  assert max(abs(r[k]) for k in ['eq_force_N','eq_moment_x_Nmm','eq_moment_y_Nmm','constraint_error_mm'])<1e-5
 delta=L*(550-514)*tm*rho/1e9
 data=dict(cad=GEO['cad'],sha256=GEO['sha256'],cases=cases,checks=checks,divisions_mm=DIVS,
  base_mm=[L,B,18],back_proposed_mm=[L,18,550],back_current_height_mm=514,
  extra_back_mass_kg_at800=delta,extra_back_mass_kg_at900=delta*900/800,
  inputs_sha256={p.relative_to(HERE.parent).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in
   [HERE/'calcular.py',helper_path,HERE.parent/'P11_ligacoes_sem_tubos_2026-10-24/placa_ritz.py',HERE.parent/'Aereos_suspensao_P09_P11_P12_P17_2026-10-25/Geometria_R51.json']},
  source_unchanged=True,scope='Estudo separado sem tubos. Fundo550 cria faces de base/tampo. Modelo parcial nao libera armazenamento/carga, resistencia, juntas ou suspensao. ReferenciaL500/300 e escolha de triagem, nao norma.')
 (HERE/'Resultados.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
 print(json.dumps([dict(mode=c['mode'],kind=c['kind'],kg=c['content_only_kg'],E0=c['E_initial_MPa'],K0=c['joint_K_initial_per_position_N_mm'],rear_width=c['rear_effective_width_mm'],deflection=c['deflection_plus_reserve_mm'],Rmax=c['max_base_reaction_N']) for c in cases]))
if __name__=='__main__':main()
