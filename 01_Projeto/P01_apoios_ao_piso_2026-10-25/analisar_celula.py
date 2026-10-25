"""Placa da celula de base apoiada no soco, contato unilateral ideal.
Analise complementar a viga-faixa50, sem creditar tracao do apoio.
"""
from pathlib import Path
import sys,json,hashlib
import numpy as np
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(HERE.parent/'P11_ligacoes_sem_tubos_2026-10-24'))
from placa_ritz import PlateModel
L=355.;B=532.;OWN=L*B*18.3*800/1e9

def case(n,mass,kind,cx=None,cy=None):
 points=sorted(set([(0.,float(y)) for y in np.linspace(0,B,n+1)]+[(L,float(y)) for y in np.linspace(0,B,n+1)]+
  [(float(x),0.) for x in np.linspace(0,L,n+1)]+[(float(x),B) for x in np.linspace(0,L,n+1)]))
 active=list(range(len(points)));seen=set()
 for iteration in range(100):
  key=tuple(active)
  if key in seen:raise AssertionError(('contact_cycle',n,mass,kind))
  seen.add(key)
  model=PlateModel(n=n,E=1100,L=L,B=B,t=17.7,supports=[points[i] for i in active])
  r=model.solve(mass=mass,kind=kind,cx=cx,cy=cy,dead_kg=OWN,grid=(181,151))
  reactions=np.array(r['reactions_N'])
  if reactions.min()<-1e-6:
   active.pop(int(reactions.argmin()));continue
  inactive=[i for i in range(len(points)) if i not in active]
  gaps=[float(model.phi(*points[i])@r['coefficients']) for i in inactive]
  if gaps and max(gaps)>1e-7:
   active.append(inactive[int(np.argmax(gaps))]);active.sort();continue
  break
 else:raise AssertionError('active set did not converge')
 # Pontos intermediarios verificam a aproximacao discreta da linha continua.
 boundary=[(0.,y) for y in np.linspace(0,B,201)]+[(L,y) for y in np.linspace(0,B,201)]+[(x,0.) for x in np.linspace(0,L,201)]+[(x,B) for x in np.linspace(0,L,201)]
 penetration=max(float(model.phi(x,y)@r['coefficients']) for x,y in boundary)
 # Sem tensoes locais no apoio pontual ideal.
 return dict(degree=n,content_kg=mass,kind=kind,cx_mm=cx,cy_mm=cy,self_mass_kg=OWN,
  max_deflection_mm=r['max_deflection_mm'],max_at_mm=r['max_at_mm'],
  plus_reserve_mm=r['max_deflection_mm']+.2,reference_mm=L/300,
  original_boundary_points=len(points),active_compression_contacts=len(active),
  released_lifted_points=len(inactive),iterations=iteration+1,
  min_active_reaction_N=float(reactions.min()),max_active_reaction_N=float(reactions.max()),
  max_discrete_line_penetration_mm=penetration,equilibrium=r['equilibrium_error'],
  scope='Placa355x532 em contato unilateral ideal sobre linhas do soco. Sem resistencia local, piso real, unioes ou durabilidade aprovados.')

results=[];checks=[]
for mass,kind,cx,cy in [(20,'uniform',None,None),(5,'patch',L/2,B/2),(10,'patch',L/2,B/2),(5,'patch',25.,30.)]:
 a=case(12,mass,kind,cx,cy);b=case(16,mass,kind,cx,cy)
 results.append(b);err=abs(a['max_deflection_mm']/b['max_deflection_mm']-1)
 residual=max(abs(v) for v in b['equilibrium'].values())
 assert err<.04,(mass,kind,err)
 assert residual<1e-5 and b['min_active_reaction_N']>=-1e-6
 assert b['max_discrete_line_penetration_mm']<.02
 checks.append(dict(mass=mass,kind=kind,degree12vs16_relative_error=err,max_equilibrium_residual=residual,
  max_line_penetration_mm=b['max_discrete_line_penetration_mm'],passed=True))
data=json.loads((HERE/'Resultados.json').read_text(encoding='utf-8'))
assert hashlib.sha256(Path(data['cad']).read_bytes()).hexdigest()==data['sha256']
(HERE/'Celula_placa_unilateral.json').write_text(json.dumps(dict(cases=results,checks=checks,passed=True,source_unchanged=True,
 note='20kg uniforme e5/10kg localizados sao cenarios independentes de triagem, nao limites de uso cumulativos. A celula e apenas parte da base.'),indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps([{'kg':r['content_kg'],'kind':r['kind'],'position':[r['cx_mm'],r['cy_mm']],'plus_reserve':r['plus_reserve_mm'],'released':r['released_lifted_points']} for r in results]))
