"""Continua P15/P04 pela caixa de marcenaria, sem tubos. N,mm,MPa,kg.
Hipoteses de juntas sao requisitos; nao ha capacidade real liberada.
python calcular.py (NumPy; reutiliza placa Ritz local)
"""
from pathlib import Path
import sys,json,math,hashlib
import numpy as np
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(HERE.parent/'P11_ligacoes_sem_tubos_2026-10-24'))
from placa_ritz import PlateModel,back_compliance
G=9.80665;RHO=800.
CAD=ROOT/'01_Projeto/Revisao_sem_tubos_R51_2026-10-25/Guedala_Park_R51_Sem_estudo_tubular.FCStd'
SHA='ab5323bb12f8eca40b25bdfe4eadc8a3221c82b0646f354cd1f2832acfb27c16'
assert hashlib.sha256(CAD.read_bytes()).hexdigest()==SHA
def save(n,r):(HERE/n).write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def solve(m,own,rectangles):
 """Retangulos (kg,x1,x2,y1,y2), uniformes em cada area. Downward positive."""
 F=np.zeros(m.N);F[0]=own*G
 mx=own*G*m.L/2;my=own*G*m.B/2;total=own
 for kg,x1,x2,y1,y2 in rectangles:
  assert 0<=x1<x2<=m.L and 0<=y1<y2<=m.B
  ix=np.array([f.integ()(2*x2/m.L-1)-f.integ()(2*x1/m.L-1) for f in m.fs])*m.L/(2*(x2-x1))
  iy=np.array([f.integ()(2*y2/m.B-1)-f.integ()(2*y1/m.B-1) for f in m.fs])*m.B/(2*(y2-y1))
  F+=kg*G*np.kron(ix,iy);mx+=kg*G*(x1+x2)/2;my+=kg*G*(y1+y2)/2;total+=kg
 rhs=np.r_[F,m.v0];u=np.linalg.solve(m.Kscaled,rhs/m.scale)/m.scale
 coef=u[:m.N];R=u[m.N:]
 xs=np.linspace(0,m.L,241);ys=np.linspace(0,m.B,81);w=m.evaluate(coef,xs,ys)
 where=np.unravel_index(np.argmax(w),w.shape)
 return dict(deflection_mm=float(w.max()),at_mm=[float(xs[where[0]]),float(ys[where[1]])],
  min_deflection_mm=float(w.min()),reactions_N=R.tolist(),content_kg=total-own,own_kg=own,
  eq_force_N=float(R.sum()-total*G),eq_moment_x_Nmm=float(m.supports[:,0]@R-mx),
  eq_moment_y_Nmm=float(m.supports[:,1]@R-my),constraint_error_mm=float(abs(m.A@coef-m.C@R-m.v0).max()))

def multi_beam(L,E,t,h,loadx,groundx,Kg,dead):
 """Faixa analitica de fundo em seu plano; nao recorte fisico. Apoios em molas.
 Retorna compliance entrepontos e recalque proprio; groundx em referencia fixa.
 Nao comprova a rigidez real do restante da caixa.
 """
 xs=np.unique(np.r_[np.linspace(0,L,81),loadx,groundx]);n=len(xs)
 K=np.zeros((2*n,2*n));F=np.zeros(2*n);I=t*h**3/12
 for j,l in enumerate(np.diff(xs)):
  ix=np.arange(2*j,2*j+4)
  k=E*I/l**3*np.array([[12,6*l,-12,6*l],[6*l,4*l*l,-6*l,2*l*l],[-12,-6*l,12,-6*l],[6*l,2*l*l,-6*l,4*l*l]])
  K[np.ix_(ix,ix)]+=k;F[ix]+=dead*G/L*l/12*np.array([6,l,6,-l])
 gi=[2*int(np.argmin(abs(xs-x))) for x in groundx];li=[2*int(np.argmin(abs(xs-x))) for x in loadx]
 for i in gi:K[i,i]+=Kg
 scale=np.sqrt(np.maximum(np.diag(K),1));ks=K/scale[:,None]/scale[None,:]
 B=np.zeros((2*n,len(li)+1));B[:,0]=F
 for j,i in enumerate(li):B[i,j+1]=1
 sol=np.linalg.solve(ks,B/scale[:,None])/scale[:,None]
 return sol[li,1:],sol[li,0],dict(ground_x_mm=list(groundx),group_K_N_mm=Kg,self_mass_kg=dead,
        assumption='Faixa100 de fundo em flexao no plano; engastes de rotacao nao creditados. Apoios de referencia da caixa precisam de comprovacao.')

def p15(t=17.7,tm=18.3,E0=2200,n=16,kind='uniform',mass=20,label=None,nominal=None):
 L=799.;B=312.;E=E0/2;rear=np.linspace(72,L-72,6)
 pts=[(0.,60.),(0.,252.),(L,60.),(L,252.)]+[(float(x),B) for x in rear]
 # Fundo18 de altura total; base25 e laterais estendidas7 para preservar topoZ18.
 nominal=t+.3 if nominal is None else nominal
 height=580+max(0,nominal-18)
 own=L*B*tm*RHO/1e9;backmass=L*height*18.3*RHO/1e9
 bc,v0,info=back_compliance(E=1100,Kg=500,L=L,h=100,t=17.7,back_positions=rear,self_mass_kg=backmass)
 C=np.eye(10)/500.;C[4:,4:]+=bc
 v=np.r_[np.zeros(4),v0]
 model=PlateModel(n=n,E=E,L=L,B=B,t=t,supports=pts,C=C,v0=v)
 rect=[(mass,0,L,0,B)] if kind=='uniform' else [(15,0,L,0,B),(5,L/2-25,L/2+25,0,60)]
 r=solve(model,own,rect);R=np.array(r['reactions_N'])
 groups=[backmass*G/2+float((1-rear/L)@R[4:]),backmass*G/2+float((rear/L)@R[4:])]
 return dict(case=(label or 'P15_'+str(round(t+.3))+'mm')+'_'+kind,degree=n,E_initial_MPa=E0,thickness_structural_mm=t,
   thickness_for_mass_mm=tm,back_height_mm=height,back_mass_kg=backmass,**r,
   side_base_joint_reactions_N=r['reactions_N'][:4],rear_joint_reactions_N=r['reactions_N'][4:],
   back_side_group_reactions_N=groups,back_model=info,joint_K_initial_required_N_mm=1000,
   deflection_plus_reserve_mm=r['deflection_mm']+.2,criterion_mm=L/300,
   load_system_eq_error_N=float(sum(R[:4])+sum(groups)-(own+mass+backmass)*G),
   status='Caixa nominal condicional. Fundo/laterais e juntas modelados por referencia de rigidez; suspensao e comportamento local nao liberados.')

def p04(n=16):
 L=1764.;B=212.;rear=np.linspace(72,L-72,12)
 div=[16.,885.5,903.5,1329.25]
 # Cada posicao y: duas juntas K1000 iniciais em serie ->K500; diferido250.
 # Duas posicoes por divisoria: grupo inferior2000, superior2000 iniciais;
 # caminho completo paralelo1000 inicial/500 diferido. Nao e dado de produto.
 pts=[(0.,60.),(0.,152.),(L,60.),(L,152.)]+[(x,y) for x in div for y in [72.,140.]]+[(float(x),B) for x in rear]
 C=np.diag([1/500.]*4+[1/250.]*8+[1/500.]*12)
 backmass=L*308*18.3*RHO/1e9
 bc,v0,info=multi_beam(L,1100,17.7,100,rear,[0.,16.,885.5,903.5,1329.25,L],250,backmass)
 C[12:,12:]+=bc;v=np.r_[np.zeros(12),v0]
 model=PlateModel(n=n,E=1100,L=L,B=B,t=17.7,supports=pts,C=C,v0=v)
 own=L*B*18.3*RHO/1e9
 divmass=18.3*212*272*RHO/1e9
 r=solve(model,own,[(5.,25.,876.5,0.,B),(2.5,912.5,1320.25,0.,B),(2.5,1338.25,L,0.,B)]+
   [(divmass,x-9,x+9,0.,B) for x in div])
 r['applied_mass_including_dividers_kg']=r['content_kg'];r['content_kg']=10.
 return dict(case='P04_fundo308_e_unioes_positivas',degree=n,**r,back_mass_kg=backmass,divider_self_mass_kg=4*divmass,
    joint_positions_mm=pts,joint_K_base_initial_required_N_mm=1000,
    division_path_K_differed_N_mm=250,division_path_value_scope='Por ramo/posicao y; dois ramos por divisoria',
    joint_K_base_value_scope='Por junta/posicao y, nao grupo de dois pontos',
    joint_lower_or_upper_group_initial_required_N_mm=2000,
    whole_divider_path_K_initial_required_N_mm=1000,whole_divider_path_K_differed_N_mm=500,
    back_model=info,
    max_abs_internal_joint_demand_N=max(abs(x) for x in r['reactions_N'][4:12]),
    deflection_plus_reserve_mm=r['deflection_mm']+.2,
    criterion_mm=float(max(np.diff(sorted([0.,*div,L]))))/300,
    criterion_max_individual_axis_spacing_mm=float(max(np.diff(sorted([0.,*div,L])))),
    previous_group_center_reference_mm=878.5/300,
    status='Transferencia em tracao via unioes inferiores/superiores das divisorias e grupos no fundo. K de conjunto exigido, nao capacidade publicada. Apoios da caixa/suspensao por demonstrar.')

def rotational():
 rows=[]
 for E0 in [2200.,1600.]:
  E=E0/2;L=799.;B=312.;t=17.7;I=B*t**3/12;mass=20+L*B*18.3*RHO/1e9;W=mass*G
  simple=5*W*L**3/(384*E*I);limit=L/300-.2
  rr=(1-limit/simple)/.8
  needed=None if rr>=1 else 2*E*I/L*rr/(1-rr)
  endmoment=None if needed is None else W*L/12*rr
  rows.append(dict(E_initial_MPa=E0,simple_deferred_mm=simple,fixed_deferred_lower_bound_mm=simple/5,
    reserve_mm=.2,criterion_mm=L/300,required_rotational_K_per_end_Nmm_rad=needed,
    end_moment_Nm=None if endmoment is None else endmoment/1000,
    approximate_couple_tension_at_9mm_N=None if endmoment is None else endmoment/9,
    note='Somente laterais; teoria de viga com molas de rotacao. Nao atribuir esteK ao Minifix; nem mesmo engaste perfeito resolve se limite teorico excede criterio.'))
 return rows

if __name__=='__main__':
 cases=[p15(),p15(kind='mixed'),p15(t=24.7,tm=25.3,E0=2100),p15(t=24.7,tm=25.3,E0=2100,kind='mixed'),
  p15(t=24.7,tm=25.3,E0=1600),p15(t=24.7,tm=25.3,E0=1600,kind='mixed'),
  p15(t=35.4,tm=36.6,E0=2200,label='P15_18mais18_composicao_integral',nominal=36),
  p15(t=35.4,tm=36.6,E0=2200,label='P15_18mais18_composicao_integral',kind='mixed',nominal=36),
  p15(t=35.4,tm=36.6,E0=1600,label='P15_18mais18_composicao_integral_adversa',kind='mixed',nominal=36),
  # I equivalente de duas camadas18 sem transferencia de cisalhamento entre elas.
  p15(t=17.7*2**(1/3),tm=36.6,E0=2200,label='P15_18mais18_sem_acao_composta',kind='mixed',nominal=36),p04()]
 checks=[]
 for c in cases:
  err=max(abs(c[k]) for k in ['eq_force_N','eq_moment_x_Nmm','eq_moment_y_Nmm','constraint_error_mm'])
  assert err<1e-5,(c['case'],err)
  checks.append(dict(case=c['case'],test='equilibrio+compatibilidade',max_residual=err,passed=True))
 for label,a,b in [('P15_25_misto',cases[3],p15(t=24.7,tm=25.3,E0=2100,n=18,kind='mixed')),
   ('P15_36_misto_adverso',cases[8],p15(t=35.4,tm=36.6,E0=1600,n=18,kind='mixed',nominal=36)),('P04',cases[-1],p04(n=18))]:
  err=abs(a['deflection_mm']/b['deflection_mm']-1)
  assert err<.02,(label,err)
  checks.append(dict(case=label,test='Ritz16vs18',relative_error=err,passed=True))
 # Conferencia integracao retangular contra solve uniforme da rotina anterior.
 m=PlateModel(n=12,E=1100,L=799,B=312,t=17.7,supports=[(0,60),(0,252),(799,60),(799,252),(72,312),(727,312)])
 ref=m.solve(mass=20,dead_kg=3.65,grid=(241,81));probe=solve(m,3.65,[(20,0,799,0,312)])
 err=abs(ref['max_deflection_mm']-probe['deflection_mm']);assert err<1e-8
 checks.append(dict(test='retangulo versus carga uniforme independente',absolute_error_mm=err,passed=True))
 assert hashlib.sha256(CAD.read_bytes()).hexdigest()==SHA
 save('Resultados.json',dict(cad=str(CAD),sha256=SHA,cases=cases,rotational_end_only=rotational(),
  scope='Estudos sem tubos; interfaces e material condicionais. Nao libera carga/fabricacao. Fundoh100 analitico nao e corte na chapa.'))
 save('Verificacao_numerica.json',dict(checks=checks,all_passed=True,cad_unchanged=True))
 print(json.dumps([{'case':c['case'],'E':c.get('E_initial_MPa',2200),'delta_plus_reserve':c['deflection_plus_reserve_mm'],'criterion':c['criterion_mm']} for c in cases]))
