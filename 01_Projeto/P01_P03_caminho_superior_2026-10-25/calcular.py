"""Triagem local da baseP03; referencia inferior ideal, sem liberar caixa."""
from pathlib import Path
import sys,json,hashlib,importlib.util
import numpy as np
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
helper_path=ROOT/'Solucoes_marcenaria_sem_tubos_2026-10-25/calcular.py'
spec=importlib.util.spec_from_file_location('helper_upper',helper_path);helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
geo_path=ROOT/'P01_massas_equilibrio_2026-10-25/Geometria_R51.json';geo=json.loads(geo_path.read_text(encoding='utf8'))
assert hashlib.sha256(Path(geo['cad']).read_bytes()).hexdigest()==geo['sha256']
L=1314.;G=9.80665;rho=800.;t=17.7
def case(proposed=False,kg=20,kind='uniform',n=18,Kleft=500.):
 B=650. if proposed else 632.
 left=[(0.,y) for y in (72.,230.,402.,560.)]
 middle=[(982.,y) for y in np.linspace(100,614,9)]
 rear=[(float(x),B)for x in np.linspace(36,L-36,19)] if proposed else []
 pts=left+middle+rear;permanent=np.array([True]*len(left)+[False]*(len(middle)+len(rear)))
 active=np.ones(len(pts),bool)
 own=L*B*18.3*rho/1e9
 oldbase=next(r['volume_mm3']*rho/1e9 for r in geo['wood']['P03'] if r['name']=='Peca262')
 otherwood=sum(r['volume_mm3']*rho/1e9 for r in geo['wood']['P03'])-oldbase
 # Orçamento superior distribuido deliberadamente: nao e partilha real das paredes/portas.
 rectangles=[(otherwood,0,L,0,B),(kg,0,L,0,60. if kind=='front' else B)]
 F=None
 for it in range(150):
  indices=np.flatnonzero(active);compliance=[1/Kleft if i<len(left) else 0 for i in indices]
  m=helper.PlateModel(n=n,E=1100,L=L,B=B,t=t,supports=np.array(pts)[indices],C=np.diag(compliance))
  r=helper.solve(m,own,rectangles);reac=np.array(r['reactions_N'])
  negative=[i for i,v in zip(indices,reac) if v< -1e-7 and not permanent[i]]
  if negative:
   # Retira o contato mais tracionado, sem converter apoio em parafuso.
   worst=min(negative,key=lambda i:reac[list(indices).index(i)]);active[worst]=False;continue
  if F is None:
   F=np.zeros(m.N);F[0]=own*G
   for mass,x1,x2,y1,y2 in rectangles:
    ix=np.array([f.integ()(2*x2/L-1)-f.integ()(2*x1/L-1)for f in m.fs])*L/(2*(x2-x1))
    iy=np.array([f.integ()(2*y2/B-1)-f.integ()(2*y1/B-1)for f in m.fs])*B/(2*(y2-y1))
    F+=mass*G*np.kron(ix,iy)
  rhs=np.r_[F,m.v0];solution=np.linalg.solve(m.Kscaled,rhs/m.scale)/m.scale;coef=solution[:m.N]
  inactive=[i for i in range(len(pts)) if not active[i]]
  penetration={i:float(m.phi(*pts[i])@coef)for i in inactive}
  if penetration and max(penetration.values())>1e-7:
   active[max(penetration,key=penetration.get)]=True;continue
  break
 else:raise AssertionError('nao convergiu contato')
 # Verifica tambem que contatos retirados nao penetrariam a referencia ideal.
 inactive=[i for i in range(len(pts)) if not active[i]]
 gap=max([float(m.phi(*pts[i])@coef) for i in inactive]+[0.])
 assert gap<1e-6,(proposed,kg,kind,gap)
 return dict(proposed=proposed,kind=kind,content_only_kg=kg,degree=n,K_left_per_position_N_mm=Kleft,**r,
  base_dims_mm=[L,B,18],extra_upper_wood_uniform_kg=otherwood,plus_reserve_mm=r['deflection_mm']+.2,reference_mm=982/300,
  all_supports_mm=pts,active_indices=indices.tolist(),inactive_indices=inactive,max_removed_contact_penetration_mm=gap,
  support_role=['left_positive_joint'if i<len(left) else 'central_divider_compression'if i<len(left)+len(middle)else 'rear_compression' for i in indices],
  note='Referencia inferior ideal e juntas laterais hipoteticas. Sem credito da travessa frontal1964, topo/fundoP03 ou paredes como vigas/caixa. Orçamento da madeira superior uniformizado; nao carga real por ligacao.')
def main():
 cases=[];checks=[]
 for proposed in (False,True):
  for kg,kind in [(10,'uniform'),(20,'uniform'),(20,'front')]:
   a=case(proposed,kg,kind,n=16);b=case(proposed,kg,kind,n=20)
   err=abs(a['deflection_mm']/b['deflection_mm']-1);assert err<.05,(proposed,kind,err)
   cases.append(b);checks.append(dict(proposed=proposed,kind=kind,kg=kg,degree16vs20_relative=err))
 out=dict(cad=geo['cad'],source_sha256=geo['sha256'],cases=cases,convergence=checks,
  added_wood_nominal_mass_800_kg=(1964*18*18+1314*18*18)*800/1e9,
  proposal=dict(P01_back_height_mm=[2096,2114],P03_base_depth_mm=[632,650],outer_dimensions_and_clear_storage_unchanged=True),
  input_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in [HERE/'calcular.py',helper_path,geo_path,ROOT/'P11_ligacoes_sem_tubos_2026-10-24/placa_ritz.py']},physical_tests=0)
 (HERE/'Resultados.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
 print(json.dumps([dict(proposed=c['proposed'],kg=c['content_only_kg'],kind=c['kind'],deflection_plus_reserve_mm=c['plus_reserve_mm'],active=len(c['active_indices']))for c in cases]))
if __name__=='__main__':main()
