import numpy as np, json, pathlib
P=pathlib.Path(__file__).parent
g=json.loads((P/'Bancada_geometria_R02.json').read_text(encoding='utf-8'))
def beam(nrails,udl_kg=0,pointloads=(),share_dead=1):
 # Euler-Bernoulli 1D, simply supported at x2785/4250, overhangs included.
 xs=sorted(set([2730.,4670.,2785.,4250.]+list(np.arange(2730,4671,20,dtype=float))+[float(x) for x,m in pointloads]))
 xs=[x for x in xs if x<=4670];N=len(xs);K=np.zeros((2*N,2*N));F=np.zeros(2*N)
 Irect=(40*20**3-34*14**3)/12
 I=.8*Irect*nrails # explicit 20% scenario reduction, not claimed catalogue property
 E=200000.
 wood=g['top_recessed_volume_mm3']/1e9*750
 topsteel=(5*1.94+2*.4)*(14.897/6)
 dead=(wood+topsteel)*share_dead
 q=(udl_kg+dead)*9.80665/(4670-2730)
 for i in range(N-1):
  L=xs[i+1]-xs[i]
  k=E*I/L**3*np.array([[12,6*L,-12,6*L],[6*L,4*L*L,-6*L,2*L*L],[-12,-6*L,12,-6*L],[6*L,2*L*L,-6*L,4*L*L]])
  f=q*L/2*np.array([1,L/6,1,-L/6]);dofs=[2*i,2*i+1,2*i+2,2*i+3]
  K[np.ix_(dofs,dofs)]+=k;F[dofs]+=f
 for x,m in pointloads:F[2*xs.index(float(x))]+=m*9.80665
 fixed=[2*xs.index(2785.),2*xs.index(4250.)];free=[i for i in range(2*N) if i not in fixed]
 u=np.zeros(2*N);u[free]=np.linalg.solve(K[np.ix_(free,free)],F[free]);R=K@u-F
 idx=int(np.argmax(abs(u[::2])))
 return dict(rails=nrails,udl_additional_kg=udl_kg,points_kg=pointloads,dead_top_kg=dead,I_effective_scenario_mm4=I,max_abs_deflection_mm=float(max(abs(u[::2]))),at_x_mm=xs[idx],right_tip_deflection_mm=float(u[-2]),support_upward_reactions_N=[float(-R[k]) for k in fixed],loss_of_contact=any(R[k]>0 for k in fixed),model='1D ideal beam; assumed equal load sharing between stated rails; no joint compliance, no 3D torsion')
cases=[beam(5,25),beam(5,50),beam(5,pointloads=[(2860,15),(3350,8),(3990,8),(4500,3)]),beam(5,pointloads=[(4670,50)]),beam(3,pointloads=[(3650,20)],share_dead=.6),beam(3,pointloads=[(3650,50)],share_dead=.6)]
(P/'Bancada_flexao_R02.json').write_text(json.dumps(dict(cases=cases,assumptions=['E steel200000 N/mm2 assumed','RHS40x20x3 catalogue existence verified; ideal geometric I reduced20% as sensitivity only','Equal sharing is not proven by this 1D analysis','No safe working load assigned']),ensure_ascii=False,indent=2),encoding='utf-8')
for c in cases:print(c)
