"""Liga a proposta723 ao soco pelo fundo/laterais/divisorias em faixas axiais.
Modelo equivalente de requisitos, nao analise3D nem capacidade real liberada.
"""
from pathlib import Path
import sys,json,hashlib
import numpy as np
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'P11_ligacoes_sem_tubos_2026-10-24'))
from placa_ritz import PlateModel
G=9.80665;E=1100.;T=17.7;TM=18.3;RHO=800.;WIDTH=100.;KF=500.

def axial(h,H):
 A=T*WIDTH;q=TM*WIDTH*RHO*G/1e9
 return h/(E*A)+1/KF,q*(H*h-h*h/2)/(E*A)+q*H/KF,q*H

def run(n,kg,kind,cx=None,cy=None):
 L=723.;B=550.;joints=[(72.,B),(265.,B),(458.,B),(651.,B),(L,70.),(L,480.)]
 bearings=[(x,y) for x in [9.,359.] for y in [70.,275.,480.]]
 cb,vb,wb=axial(1073.,2096.) # fundo apoiado diretamente no calco18.
 cs,vs,ws=axial(1091.,2132.) # laterais em pe ate o piso.
 cd,vd,wd=axial(1002.,1002.) # divisoria apoiada na base+soco.
 active=list(bearings);seen=set()
 for iteration in range(12):
  key=tuple(active)
  if key in seen:raise AssertionError('contact cycle')
  seen.add(key)
  C=np.diag([1/500+cb]*4+[1/500+cs]*2+[cd]*len(active))
  v0=np.array([vb]*4+[vs]*2+[vd]*len(active))
  model=PlateModel(n=n,E=1100,L=L,B=B,t=T,supports=joints+active,C=C,v0=v0)
  r=model.solve(mass=kg,kind=kind,cx=cx,cy=cy,dead_kg=L*B*TM*RHO/1e9,grid=(181,121))
  contact=np.array(r['reactions_N'][6:]);negative=[i for i,v in enumerate(contact) if v<-1e-6]
  if not negative:break
  active=[p for i,p in enumerate(active) if i not in negative]
 else:raise AssertionError('contact set did not converge')
 floorforces=np.array(r['reactions_N'])+np.array([wb]*4+[ws]*2+[wd]*len(active))
 assert floorforces.min()>0, 'Modelo de apoio ao piso requer contato sem retencao por baixo'
 assert max(abs(v) for v in r['equilibrium_error'].values())<1e-5
 del r['coefficients'];del r['support_deflection_mm']
 return dict(**r,content_kg=kg,active_bearings_mm=active,
  reference_mm=364/300,plus_reserve_mm=r['max_deflection_mm']+.2,
  min_floor_branch_force_N=float(floorforces.min()),model_degree=n,
  body_equivalent=dict(axial_strip_width_mm=WIDTH,structural_t_mm=T,E_differed_MPa=E,
   floor_and_bearing_branch_K_required_N_mm=KF,
   back_C_mm_N=cb,side_C_mm_N=cs,divider_C_mm_N=cd,
   back_own_settlement_mm=vb,side_own_settlement_mm=vs,divider_own_settlement_mm=vd),
  scope='Somente uma prateleira723 e caminho equivalente, outra espelhada. Faixa axial100 e K500 do contato de cada ramo sao hipoteses/requisitos. Nao incluem todos os carregamentos do roupeiro, acoplamentos, juntas locais ou piso real.')

rows=[run(14,m,k,cx,cy) for m,k,cx,cy in [(5.,'uniform',None,None),(10.,'uniform',None,None),(20.,'uniform',None,None),(5.,'patch',25.,30.)]]
probe=run(18,20.,'uniform');error=abs(probe['max_deflection_mm']/rows[2]['max_deflection_mm']-1)
assert error<.02
base=json.loads((HERE/'Resultados.json').read_text(encoding='utf-8'))
assert hashlib.sha256(Path(base['cad']).read_bytes()).hexdigest()==base['sha256']
(HERE/'Prateleiras_caixa_soco.json').write_text(json.dumps(dict(cases=rows,convergence14vs18=error,
 passed=True,source_unchanged=True,
 limitations=['Faixas axiais sao participacao minima hipotetica, nao dado de fabricante','Rigidez contato500N/mm por ramo requerida, nao medicao',
 'Rugosidade/nivel do piso e compressao perpendicular/encaixes das chapas devem ser provados',
 'Carga de outras prateleiras/varoes/gavetas e portas nao foi acoplada neste submodelo',
 'Nao aprova apoio ao piso nem anti-tombamento/parede e nao libera carga real']),indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps([{'kg':r['content_kg'],'kind':r['kind'],'plus_reserve_mm':r['plus_reserve_mm'],'reference_mm':r['reference_mm']} for r in rows]))
