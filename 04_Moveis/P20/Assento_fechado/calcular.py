"""Tampas fechadas em apoios unilaterais; triagem nominal, nao capacidade.
Ritz Kirchhoff isotropico equivalente. N, mm, MPa. Cargas200x200 do
estudo historico, sem as transformar em ensaio de norma ou limite de uso.
"""
from pathlib import Path
import json,sys,hashlib
import numpy as np
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'P11_ligacoes_sem_tubos_2026-10-24'))
from placa_ritz import PlateModel,GRAVITY
G=json.loads((HERE/'Geometria_R51.json').read_text(encoding='utf8'))

def patch_vector(model,kg,cx,cy,width=200.,height=200.):
 assert width/2<=cx<=model.L-width/2 and height/2<=cy<=model.B-height/2
 def integ(center,size,span):
  return np.array([f.integ()(2*(center+size/2)/span-1)-f.integ()(2*(center-size/2)/span-1) for f in model.fs])*span/(2*size)
 return kg*GRAVITY*np.kron(integ(cx,width,model.L),integ(cy,height,model.B))

def solve(lid,n,E,patches,cleats=False):
 b=lid['box'];L=b[3]-b[0];B=b[4]-b[1]
 # Linhas no centro de cada face de contato, sem engaste nem tracao.
 points={}
 for c in G['contacts']:
  if c['lid']!=lid['name'] or (c['support'].startswith('Ref_Sarrafo') and not cleats):continue
  x0,y0,x1,y1=c['rectangle_global_mm'];x0-=b[0];x1-=b[0];y0-=b[1];y1-=b[1]
  if x1-x0>y1-y0: line=[(x,(y0+y1)/2) for x in np.linspace(x0,x1,n+1)]
  else:line=[((x0+x1)/2,y) for y in np.linspace(y0,y1,n+1)]
  for x,y in line:points[round(x,8),round(y,8)]=c['support']
 p=list(points);owners=list(points.values());active=list(range(len(p)));seen=set()
 # Massa proxy do envelope acabado20 a900kg/m3; nucleo resistente17,1.
 own=lid['volume_mm3']*900/1e9
 for iteration in range(160):
  key=tuple(active)
  if key in seen:raise AssertionError(('active_set_cycle',lid['name'],n,E,patches))
  seen.add(key)
  m=PlateModel(n=n,E=E,L=L,B=B,t=17.1,supports=[p[i] for i in active])
  F=np.zeros(m.N);F[0]=own*GRAVITY
  for kg,cx,cy in patches:F+=patch_vector(m,kg,cx,cy)
  sol=np.linalg.solve(m.Kscaled,np.r_[F,m.v0]/m.scale)/m.scale
  coeff=sol[:m.N];R=sol[m.N:]
  if R.min() < -1e-6:active.pop(int(R.argmin()));continue
  inactive=[i for i in range(len(p)) if i not in active]
  gaps=[float(m.phi(*p[i])@coeff) for i in inactive]
  if gaps and max(gaps)>1e-7:
   active.append(inactive[int(np.argmax(gaps))]);active.sort();continue
  break
 else:raise AssertionError('contact not converged')
 xs=np.linspace(0,L,161);ys=np.linspace(0,B,241);W=m.evaluate(coeff,xs,ys);idx=np.unravel_index(W.argmax(),W.shape)
 expected=[(own+sum(x[0] for x in patches))*GRAVITY,
   (own*L/2+sum(kg*x for kg,x,y in patches))*GRAVITY,
   (own*B/2+sum(kg*y for kg,x,y in patches))*GRAVITY]
 equilibrium=np.array([R.sum(),m.supports[:,0]@R,m.supports[:,1]@R])-expected
 groups={}
 for i,r in zip(active,R):groups[owners[i]]=groups.get(owners[i],0)+float(r)
 # Verifica as linhas entre os pontos de contato, sem creditar apoio tracionado.
 penetration=-float('inf')
 for c in G['contacts']:
  if c['lid']!=lid['name'] or (c['support'].startswith('Ref_Sarrafo') and not cleats):continue
  x0,y0,x1,y1=c['rectangle_global_mm'];x0-=b[0];x1-=b[0];y0-=b[1];y1-=b[1]
  if x1-x0>y1-y0:v=m.evaluate(coeff,np.linspace(x0,x1,201),[(y0+y1)/2])
  else:v=m.evaluate(coeff,[(x0+x1)/2],np.linspace(y0,y1,201))
  penetration=max(penetration,float(v.max()))
 return dict(lid=lid['name'],degree=n,E_equivalent_MPa=E,core_min_mm=17.1,
  patches_kg_xy_mm=patches,patch_size_mm=[200,200],self_mass_proxy_kg=own,
  credit_cleats=cleats,max_deflection_mm=float(W.max()),max_at_mm=[float(xs[idx[0]]),float(ys[idx[1]])],
  min_deflection_mm=float(W.min()),plus_body_reserve_mm=float(W.max()+.2),
  reference_project_mm=2.,initial_contact_points=len(p),active_contact_points=len(active),iterations=iteration+1,
  min_compression_reaction_N=float(R.min()),reactions_by_part_N=groups,
  max_equilibrium_residual=float(np.max(np.abs(equilibrium))),equilibrium_residual_N_Nmm=equilibrium.tolist(),
  max_constraint_error_mm=float(np.max(np.abs(m.A@coeff))),max_line_penetration_mm=penetration,
  scope='Modelo de chapa com apoios rigidos condicionais; sem fixacoes, estabilidade, ortotropia ou ensaio aprovados.')

def main():
 assert hashlib.sha256(Path(G['cad']).read_bytes()).hexdigest()==G['sha256']
 a,b=G['lids'];cases=[
 ('maior_centro_setor_potes',a,[(80,224,198)]),
 ('maior_frente_setor_potes',a,[(80,348,198)]),
 ('maior_duas_pessoas_nominais',a,[(80,224,198),(80,224,572)]),
 ('menor_centro',b,[(80,224,412.5)]),
 ('menor_frente',b,[(80,348,412.5)])]
 results=[];checks=[]
 for label,lid,patches in cases:
  low=solve(lid,14,5500,patches);high=solve(lid,18,5500,patches)
  err=abs(low['max_deflection_mm']/high['max_deflection_mm']-1)
  assert err<.07,(label,err)
  assert high['max_equilibrium_residual']<1e-4 and high['max_constraint_error_mm']<1e-6
  assert high['max_line_penetration_mm']<.02,(label,high['max_line_penetration_mm'])
  high['case']=label;results.append(high)
  checks.append(dict(case=label,degree14vs18_relative_error=err,passed=True))
 # Sensibilidades: sem escolher MDF ou transferir E de compensado isotropico.
 for label,lid,patches in [cases[2],cases[3],cases[4]]:
  for E in (2200,2750):
   r=solve(lid,18,E,patches);r['case']=label+'_sensibilidade';results.append(r)
 # Sarrafos antigos sao avaliados somente como teto otimista condicionado.
 r=solve(b,18,5500,cases[4][2],cleats=True);r['case']='menor_frente_com_sarrafos_condicionais';results.append(r)
 data=dict(cad=G['cad'],sha256=G['sha256'],cases=results,checks=checks,passed=True,
  source_unchanged=True,note='80kg e200x200mm sao hipoteses herdadas para triagem. Nao sao carga normativa nem capacidade liberada. E isotropico equivalente nao e automaticamente MOE longitudinal/transversal do compensado.')
 (HERE/'Resultados.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
 print(json.dumps([dict(case=r['case'],E=r['E_equivalent_MPa'],mm=r['plus_body_reserve_mm'],R=r['reactions_by_part_N']) for r in results],ensure_ascii=False))
if __name__=='__main__':main()
