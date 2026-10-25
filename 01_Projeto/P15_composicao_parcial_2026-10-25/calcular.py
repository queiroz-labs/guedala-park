"""Duas laminas isotropicas com deslizamento continuo: estudo, nao produto.
Energia: flexao propria2D18 + membranas2K + ks/2 integral|2u+t gradw|^2.
Condensacao espectral evita subtrair termos quase iguais no limite rigido.
"""
from pathlib import Path
import json,hashlib,importlib.util,math
import numpy as np
from numpy.polynomial.legendre import leggauss
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
hp=ROOT/'Solucoes_marcenaria_sem_tubos_2026-10-25/calcular.py'
spec=importlib.util.spec_from_file_location('helper_partial',hp);helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
L=799.;B=312.;T=17.7;NU=.3;G=9.80665
CACHE={}
def setup(n,E0):
 key=(n,E0)
 if key in CACHE:return CACHE[key]
 E=E0/2;rear=np.linspace(72,L-72,6)
 pts=[(0.,60.),(0.,252.),(L,60.),(L,252.)]+[(float(x),B)for x in rear]
 backmass=L*598*18.3*800/1e9
 bc,v0,info=helper.back_compliance(E=1100,Kg=500,L=L,h=100,t=17.7,back_positions=rear,self_mass_kg=backmass)
 C=np.eye(10)/500.;C[4:,4:]+=bc;v=np.r_[np.zeros(4),v0]
 model=helper.PlateModel(n=n,E=E,L=L,B=B,t=T,supports=pts,C=C,v0=v)
 q,wt=leggauss(n+3);fs=model.fs;values=np.array([f(q)for f in fs]);deriv=np.array([f.deriv()(q)for f in fs])
 def gram(a,b):return (a*wt)@b.T
 M=gram(values,values);P=gram(deriv,values);D=gram(deriv,deriv);fac=L*B/4;fx=2/L;fy=2/B
 xx=fac*fx**2*np.kron(D,M);yy=fac*fy**2*np.kron(M,D)
 xy=fac*fx*fy*np.kron(P,P.T);yx=fac*fx*fy*np.kron(P.T,P)
 A=E*T/(1-NU**2)
 Km=A*np.block([[xx+(1-NU)/2*yy,NU*xy+(1-NU)/2*yx],
               [NU*yx+(1-NU)/2*xy,yy+(1-NU)/2*xx]])
 md=fac*np.diag(np.kron(M,M));massdiag=np.r_[md,md];root=np.sqrt(massdiag)
 H=np.vstack([fac*fx*np.kron(P.T,M),fac*fy*np.kron(M,P.T)])
 Q=H/root[:,None]
 eigen,V=np.linalg.eigh(2*Km/root[:,None]/root[None,:])
 assert min(eigen)>-max(eigen)*1e-10
 eigen[eigen<max(eigen)*1e-11]=0
 assert np.count_nonzero(eigen==0)==3
 Z=V.T@Q;K0=2*model.K
 # Gradiente de w pertence exatamente ao espaco de membrana escolhido.
 grad=xx+yy;assert np.max(np.abs(Q.T@Q-grad))<1e-6
 full=K0+T*T*(Z.T*(eigen/4))@Z
 assert np.max(np.abs(full-8*model.K))/max(abs(full).max(),1)<1e-8
 out=dict(model=model,K0=K0,eigen=eigen,V=V,Z=Z,root=root,backmass=backmass,E=E,full=full,
  membrane=2*Km,massdiag=massdiag,H=H,grad=grad)
 CACHE[key]=out;return out
def case(ks,E0=2200,n=14,kind='mixed',stress=False):
 data=setup(n,E0);m=data['model'];lam=data['eigen'];Z=data['Z']
 factor=lam/4 if math.isinf(ks) else ks*lam/(lam+4*ks) if ks else np.zeros_like(lam)
 m.K=data['K0']+T*T*(Z.T*factor)@Z
 # Forca exata dos modos de corpo rigido nativos.
 for i in (0,1,n+1):m.K[i,:]=0;m.K[:,i]=0
 m.Kaug=np.block([[m.K,m.A.T],[m.A,-m.C]])
 m.scale=np.r_[np.sqrt(np.maximum(np.diag(m.K),1)),np.ones(m.S)]
 m.Kscaled=m.Kaug/m.scale[:,None]/m.scale[None,:]
 own=L*B*36.6*800/1e9;rect=[(15.,0,L,0,B),(5.,L/2-25,L/2+25,0,60)] if kind=='mixed' else [(20.,0,L,0,B)]
 r=helper.solve(m,own,rect)
 # Segunda montagem independente do vetor para recuperar w e a tensao da interface.
 F=np.zeros(m.N);F[0]=own*G
 for kg,x1,x2,y1,y2 in rect:
  ix=np.array([f.integ()(2*x2/L-1)-f.integ()(2*x1/L-1)for f in m.fs])*L/(2*(x2-x1))
  iy=np.array([f.integ()(2*y2/B-1)-f.integ()(2*y1/B-1)for f in m.fs])*B/(2*(y2-y1))
  F+=kg*G*np.kron(ix,iy)
 sol=np.linalg.solve(m.Kscaled,np.r_[F,m.v0]/m.scale)/m.scale;coef=sol[:m.N]
 assert np.max(np.abs(m.K@coef+m.A.T@sol[m.N:]-F))<1e-4
 out=dict(interface_ks_N_mm3=None if math.isinf(ks) else ks,limit='perfect_composite'if math.isinf(ks) else 'no_shear_transfer'if ks==0 else 'partial',
  E_initial_MPa=E0,E_sensitivity_MPa=E0/2,degree=n,kind=kind,**r,
  plus_reserve_mm=r['deflection_mm']+.2,criterion_mm=L/300,
  note='Duas camadas17.7 resistentes/18.3massa, mesmo w e sem separacao normal, interface uniforme elastica. Juntas/fundo iguais ao estudo anterior; sem dano, viscoelasticidade ou resistencia local comprovados.')
 if stress:
  # tau = ks*s = t M^-1/2 V [ks*lambda/(lambda+4ks)] Z w.
  taucoef=T/data['root']*(data['V']@(factor*(Z@coef)))
  xs=np.linspace(0,L,241);ys=np.linspace(0,B,121);tx=m.evaluate(taucoef[:m.N],xs,ys);ty=m.evaluate(taucoef[m.N:],xs,ys)
  tau=np.hypot(tx,ty);XX,YY=np.meshgrid(xs,ys,indexing='ij')
  peaks=[]
  for radius in (30.,50.):
   mask=np.ones(tau.shape,bool)
   for x,y in m.supports:mask&=(XX-x)**2+(YY-y)**2>=radius**2
   masked=np.where(mask,tau,-np.inf);i=np.unravel_index(masked.argmax(),masked.shape)
   peaks.append(dict(exclusion_radius_mm=radius,max_sample_shear_MPa=float(masked.max()),at_mm=[float(xs[i[0]]),float(ys[i[1]])]))
  out['interface_shear_screen']=peaks
  out['max_sample_slip_mm']=None if not ks or math.isinf(ks) else float(tau.max()/ks)
 return out
def direct_uncondensed_check():
 # Montagem dos3 campos antes de condensar; compara uma interface finita.
 n=8;ks=1.;c=case(ks,2200,n=n);data=setup(n,2200);m=data['model'];N=m.N;S=m.S
 Bc=2*ks*T*data['H'];Kww=data['K0']+ks*T*T*data['grad'];Kaa=data['membrane']+np.diag(4*ks*data['massdiag'])
 K=np.block([[Kww,Bc.T,m.A.T],[Bc,Kaa,np.zeros((2*N,S))],[m.A,np.zeros((S,2*N)),-m.C]])
 F=np.zeros(N);F[0]=L*B*36.6*800/1e9*G
 for kg,x1,x2,y1,y2 in [(15.,0,L,0,B),(5.,L/2-25,L/2+25,0,60)]:
  ix=np.array([f.integ()(2*x2/L-1)-f.integ()(2*x1/L-1)for f in m.fs])*L/(2*(x2-x1))
  iy=np.array([f.integ()(2*y2/B-1)-f.integ()(2*y1/B-1)for f in m.fs])*B/(2*(y2-y1))
  F+=kg*G*np.kron(ix,iy)
 rhs=np.r_[F,np.zeros(2*N),m.v0];scale=np.sqrt(np.maximum(abs(np.diag(K)),1.))
 sol=np.linalg.solve(K/scale[:,None]/scale[None,:],rhs/scale)/scale
 w=m.evaluate(sol[:N],np.linspace(0,L,241),np.linspace(0,B,81))
 error=abs(float(w.max())-c['deflection_mm']);reaction=max(abs(sol[-S:]-np.array(c['reactions_N'])))
 assert error<1e-8 and reaction<1e-7,(error,reaction)
 return dict(test='three_fields_direct_vs_condensed_finite_interface',degree=n,ks=ks,deflection_error_mm=error,reaction_error_N=float(reaction))
def main():
 cases=[];checks=[];threshold=[]
 for E0 in (2200.,1600.):
  for ks in (0.,.01,.1,1.,10.,100.,1000.,float('inf')):cases.append(case(ks,E0,n=14,stress=True))
  lo,hi=0.,1000.
  for _ in range(26):
   mid=(lo+hi)/2;r=case(mid,E0,n=14)
   if r['plus_reserve_mm']>L/300:lo=mid
   else:hi=mid
  approximate14=hi;lo,hi=0.,1000.
  for _ in range(26):
   mid=(lo+hi)/2;r=case(mid,E0,n=18)
   if r['plus_reserve_mm']>L/300:lo=mid
   else:hi=mid
  r=case(hi,E0,n=18,stress=True);a=case(hi,E0,n=14)
  checks.append(dict(test='Ritz14vs18_partial_at_threshold',E0=E0,relative_error=abs(a['deflection_mm']/r['deflection_mm']-1)))
  threshold.append(dict(E_initial_MPa=E0,approximate_ks_for_criterion_N_mm3=hi,approximate_degree14_ks_N_mm3=approximate14,degree14= a['plus_reserve_mm'],degree18=r['plus_reserve_mm'],
   note='Intersecao numerica do criterio no modelo uniforme; nao requisito executivo, adesivo recomendado ou margem de projeto.',shear_at_threshold=r['interface_shear_screen']))
 for ks,thickness,label in [(0.,17.7*2**(1/3),'no_composite'),(float('inf'),35.4,'full_composite')]:
  a=case(ks,2200,n=14);b=helper.p15(t=thickness,tm=36.6,E0=2200,n=14,kind='mixed',nominal=36)
  error=abs(a['deflection_mm']-b['deflection_mm']);assert error<1e-7,(label,error)
  checks.append(dict(test='independent_previous_plate_limit_'+label,error_mm=error))
 checks.append(direct_uncondensed_check())
 assert all(c.get('relative_error',0)<.02 for c in checks)
 for c in cases:
  assert max(abs(c[k])for k in ['eq_force_N','eq_moment_x_Nmm','eq_moment_y_Nmm','constraint_error_mm'])<1e-5
 for E0 in (2200.,1600.):
  deltas=[c['deflection_mm']for c in cases if c['E_initial_MPa']==E0]
  assert all(a>b for a,b in zip(deltas,deltas[1:])),deltas
 source=ROOT/'Revisao_sem_tubos_R51_2026-10-25/Guedala_Park_R51_Sem_estudo_tubular.FCStd'
 shear_refinement=[dict(degree=n,peaks=case(1.,2200,n=n,stress=True)['interface_shear_screen'])for n in (14,18,22)]
 assert max(x['peaks'][0]['max_sample_shear_MPa']for x in shear_refinement)/min(x['peaks'][0]['max_sample_shear_MPa']for x in shear_refinement)-1<.05
 out=dict(cases=cases,thresholds=threshold,checks=checks,shear_refinement_one_partial_case=shear_refinement,source=str(source),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
  inputs_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in [HERE/'calcular.py',hp,ROOT/'P11_ligacoes_sem_tubos_2026-10-24/placa_ritz.py']},
  physical_tests=0,status='Modelo de composicao parcial; nao atribui ks, resistencia ou durabilidade a produto comercial. Sem novo CAD ou alteracaoR51.')
 (HERE/'Resultados.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
 print(json.dumps(dict(thresholds=threshold,limits=[(c['E_initial_MPa'],c['interface_ks_N_mm3'],c['plus_reserve_mm'])for c in cases]),ensure_ascii=False))
if __name__=='__main__':main()
