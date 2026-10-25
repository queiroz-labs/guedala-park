"""Bancada: apoio esquerdo e pedestal do gaveteiro em marcenaria, sem tubos.
Modelo de placa sobre linhas de compressao e travessa traseira flexivel.
Unidades N,mm,MPa,kg. Requisitos e hipoteses, nao capacidade liberada.
"""
from pathlib import Path
import sys,json,hashlib
import numpy as np
from numpy.polynomial.legendre import leggauss
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(HERE.parent/'P11_ligacoes_sem_tubos_2026-10-24'))
from placa_ritz import PlateModel
CAD=ROOT/'01_Projeto/Revisao_sem_tubos_R51_2026-10-25/Guedala_Park_R51_Sem_estudo_tubular.FCStd'
SHA='ab5323bb12f8eca40b25bdfe4eadc8a3221c82b0646f354cd1f2832acfb27c16'
assert hashlib.sha256(CAD.read_bytes()).hexdigest()==SHA
G=9.80665;RHO=800.;Ebody=1100.;Tbody=17.7
panels=[
 dict(id='Apoio_esquerdo',source_replaces='Peca112',origin_mm=[2720.,20.,0.],size_mm=[18.,650.,720.],role='painel lateral de apoio ate o piso'),
 dict(id='Pedestal_lateral_E',source_replaces='Peca367',origin_mm=[4300.,40.,0.],size_mm=[18.,640.,720.],role='lateral atual ampliada para tras/baixo; gavetas mantidas'),
 dict(id='Pedestal_lateral_D',source_replaces='Peca368',origin_mm=[4682.,40.,0.],size_mm=[18.,640.,720.],role='lateral atual ampliada para tras/baixo; gavetas mantidas'),
 dict(id='Pedestal_posterior',source_replaces='',origin_mm=[4318.,70.,0.],size_mm=[364.,18.,720.],role='fechamento traseiro estrutural de estudo, fora do fundo atual das gavetas'),
 dict(id='Travessa_traseira',source_replaces='',origin_mm=[2738.,70.,540.],size_mm=[1562.,18.,180.],role='travessa de madeira somente atras, sem travessa frontal sob entrada da cadeira')]

def beam_green(x,a,L,EI,Kg):
 bend=(L-a)*x*(L*L-(L-a)**2-x*x)/(6*L*EI) if x<=a else a*(L-x)*(L*L-a*a-(L-x)**2)/(6*L*EI)
 return bend+((1-x/L)*(1-a/L)+(x/L)*(a/L))/Kg

def support_system(points_per_line):
 pts=[];Cblocks=[];Vblocks=[];types=[]
 # Colunas equivalentes ao longo das bordas dos paineis. Kcontato por mm de linha.
 kcontact=5. # requisito diferido de contato/apoio, nao dado de fabricante.
 for x,y0,y1,label in [(29.,20.,670.,'esquerdo'),(1609.,40.,680.,'pedestalE'),(1991.,40.,680.,'pedestalD')]:
  length=y1-y0;ys=y0+(np.arange(points_per_line)+.5)*length/points_per_line
  trib=length/points_per_line
  pts += [(x,float(y)) for y in ys];types += [label]*len(ys)
  Cblocks.append(np.eye(len(ys))*(720/(Ebody*Tbody*trib)+1/(kcontact*trib)))
  # Peso proprio da faixa vertical, deformacao axial+acomodacao do contato.
  mass=18.3*trib*720*RHO/1e9
  Vblocks.append(np.full(len(ys),mass*G*(720/(2*Ebody*Tbody*trib)+1/(kcontact*trib))))
 # Traseira do pedestal (entre suas laterais), coluna equivalente apoiada ao piso.
 length=364.;xs=1618+(np.arange(max(4,points_per_line//2))+.5)*length/max(4,points_per_line//2)
 trib=length/len(xs);pts += [(float(x),79.) for x in xs];types += ['pedestal_fundo']*len(xs)
 Cblocks.append(np.eye(len(xs))*(720/(Ebody*Tbody*trib)+1/(kcontact*trib)))
 mass=18.3*trib*720*RHO/1e9
 Vblocks.append(np.full(len(xs),mass*G*(720/(2*Ebody*Tbody*trib)+1/(kcontact*trib))))
 # Travessa traseira180: flexao no plano, extremos em grupos flexiveis.
 La=1562.;h=179.7;EI=Ebody*Tbody*h**3/12;Kg=500.
 xx=(np.arange(points_per_line)+.5)*La/points_per_line
 pts += [(38+float(x),79.) for x in xx];types += ['travessa_traseira']*len(xx)
 block=np.array([[beam_green(x,a,La,EI,Kg) for a in xx] for x in xx])
 block+=np.eye(len(xx))/(kcontact*La/len(xx))
 Cblocks.append(block)
 weight=La*18.3*180*RHO/1e9*G;q=weight/La
 Vblocks.append(np.array([q*x*(La**3-2*La*x*x+x**3)/(24*EI)+weight/(2*Kg) for x in xx]))
 S=len(pts);C=np.zeros((S,S));v=np.concatenate(Vblocks);offset=0
 for b in Cblocks:
  C[offset:offset+len(b),offset:offset+len(b)]=b;offset+=len(b)
 return np.array(pts),C,v,types

def load_vector(m,own,rects):
 F=np.zeros(m.N);F[0]=own*G;mx=own*G*1000;my=own*G*350;total=own
 for kg,x1,x2,y1,y2 in rects:
  assert 0<=x1<x2<=2000 and 0<=y1<y2<=700
  ix=np.array([f.integ()(2*x2/2000-1)-f.integ()(2*x1/2000-1) for f in m.fs])*2000/(2*(x2-x1))
  iy=np.array([f.integ()(2*y2/700-1)-f.integ()(2*y1/700-1) for f in m.fs])*700/(2*(y2-y1))
  F+=kg*G*np.kron(ix,iy);mx+=kg*G*(x1+x2)/2;my+=kg*G*(y1+y2)/2;total+=kg
 return F,mx,my,total

def case(label,rects,n=16,point_count=8,top_E_initial=2100.,retain_bound=False):
 pts,C,v,types=support_system(point_count);active=list(range(len(pts)));seen=set();own=2000*700*30.3*RHO/1e9
 for iteration in range(120):
  key=tuple(active)
  if key in seen:raise AssertionError(('contact cycle',label))
  seen.add(key)
  model=PlateModel(n=n,E=top_E_initial/2,L=2000,B=700,t=29.7,supports=pts[active],C=C[np.ix_(active,active)],v0=v[active])
  F,mx,my,total=load_vector(model,own,rects)
  rhs=np.r_[F,model.v0];u=np.linalg.solve(model.Kscaled,rhs/model.scale)/model.scale
  coef=u[:model.N];R=u[model.N:]
  if R.min()<-1e-5 and not retain_bound:
   active.pop(int(R.argmin()));continue
  inactive=[i for i in range(len(pts)) if i not in active]
  # Suporte inativo ainda se deforma por peso proprio e cargas dos outros pontos.
  gaps=[float(model.phi(*pts[i])@coef-C[i,active]@R-v[i]) for i in inactive]
  if gaps and max(gaps)>1e-6:
   active.append(inactive[int(np.argmax(gaps))]);active.sort();continue
  break
 else:raise AssertionError('contact no converge')
 xs=np.linspace(0,2000,241);ys=np.linspace(0,700,101);W=model.evaluate(coef,xs,ys)
 idx=np.unravel_index(W.argmax(),W.shape)
 eq=[float(R.sum()-total*G),float(pts[active,0]@R-mx),float(pts[active,1]@R-my)]
 assert max(abs(x) for x in eq)<1e-4
 grouped={s:float(sum(R[j] for j,i in enumerate(active) if types[i]==s)) for s in set(types)}
 apron_idx=[(j,i) for j,i in enumerate(active) if types[i]=='travessa_traseira']
 apron_self=1562*18.3*180*RHO/1e9*G
 apron_ends=[apron_self/2+sum(R[j]*(1-(pts[i,0]-38)/1562) for j,i in apron_idx),
             apron_self/2+sum(R[j]*(pts[i,0]-38)/1562 for j,i in apron_idx)]
 return dict(case=label,degree=n,points_per_line=point_count,E_top_initial_MPa=top_E_initial,
  top_structural_t_mm=29.7,own_top_mass_kg=own,content_mass_kg=total-own,
  max_deflection_mm=float(W.max()),at_local_mm=[float(xs[idx[0]]),float(ys[idx[1]])],
  min_deflection_mm=float(W.min()),plus_reserve_mm=float(W.max())+.2,
  reference_largest_support_span_mm=1580,reference_deflection_mm=1580/300,
  reactions_by_group_N=grouped,max_contact_reaction_N=float(R.max()),min_contact_reaction_N=float(R.min()),
  rear_apron_end_group_reactions_N=[float(x) for x in apron_ends],
  idealized_distributed_retention=retain_bound,
  total_retention_demand_N=float(-sum(x for x in R if x<0)),
  original_contacts=len(pts),active_compression_contacts=len(active),iterations=iteration+1,equilibrium_error=eq,
  patch_rectangles=rects,
  scope='Somente tampo30 homogeneo e apoios equivalentes. Juntas/fundacao/rigidez de paineis sao requisitos; gaveteiro movel/cargas horizontais e estabilidade global nao liberados.')

def patch(kg,x,y,w=100.,d=100.):return (kg,x-w/2,x+w/2,y-d/2,y+d/2)
if __name__=='__main__':
 specs=[('distribuido25',[(25.,0.,2000.,0.,700.)]),('distribuido50',[(50.,0.,2000.,0.,700.)]),
  ('equipamentos_teste34',[patch(15,160,350),patch(8,650,350),patch(8,1290,350),patch(3,1800,350)]),
  ('frente20',[patch(20,1000,650,50,60)]),('extremo_direito50',[patch(50,1970,650,50,60)])]
 rows=[case(label,rects) for label,rects in specs]
 checks=[]
 for label,rects in [specs[0],specs[3]]:
  a=next(r for r in rows if r['case']==label);b=case(label,rects,n=20,point_count=12)
  err=abs(a['max_deflection_mm']/b['max_deflection_mm']-1)
  checks.append(dict(case=label,degree16_8points_mm=a['max_deflection_mm'],degree20_12points_mm=b['max_deflection_mm'],relative_change=err,passed=bool(err<.08)))
 # Comparacao de requisito de rigidez do material, sem escolher novo produto.
 rows += [case('material_mais_rigido_E6000_frente20',specs[3][1],top_E_initial=6000),
          case('material_mais_rigido_E8000_frente20',specs[3][1],top_E_initial=8000),
          case('limite_retencao_distribuida25',specs[0][1],retain_bound=True),
          case('limite_retencao_distribuida_frente20',specs[3][1],retain_bound=True),
          case('limite_retencao_distribuida_equipamentos34',specs[2][1],retain_bound=True)]
 floorarea=18*650+2*18*640+364*18
 gross=sum(np.prod(p['size_mm']) for p in panels)*RHO/1e9
 removed_side=(2*18*430*240)*RHO/1e9
 assert hashlib.sha256(CAD.read_bytes()).hexdigest()==SHA
 result=dict(cad=str(CAD),sha256=SHA,panels=panels,retire_proxies_in_study=['Peca111','Peca112'],
  top_bounds_mm=[2700,0,720,4700,700,750],drawer_original_bounds_mm=[4300,250,480,4700,680,720],
  clear_between_left_and_pedestal_mm=1562.,nominal_floor_area_mm2=floorarea,
  new_panel_gross_mass_kg=gross,replaced_original_side_mass_kg=removed_side,
  results=rows,convergence_checks=checks,
  assumptions=['Tampo homogeneo estrutural29.7 com massa30.3; MDF30E2100 e sensibilidade E6000 nao sao produto comprado',
   'Paineis18E2200; sensibilidade diferida divideE por2','Contato distribuido requerido5N/mm2 na sensibilidade diferida',
   'Grupos de extremidade da travessa K500N/mm diferido requeridos; nao capacidade de dois parafusos',
   'Nos modelos sem retencao os contatos so comprimem; comparacoes de retencao distribuida admitem tracao hipotetica e nao especificam fixadores',
   'Massas de equipamentos15+8+8+3 e posicoesY350 sao casos de teste, nao pesagens ou setup validado',
   'Massa/carga das gavetas vao ao pedestal, nao foram adicionadas ao tampo; verificar pedestal/piso/estabilidade separadamente'],
  status='ESTUDO: altera apoios e aparencia externa, nunca incorporado automaticamente. Sem tubos e sem travessa frontal no vao central.')
 (HERE/'Resultados.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 (HERE/'Verificacao_calculo.json').write_text(json.dumps(dict(checks=checks,all_passed=all(c['passed'] for c in checks),source_unchanged=True),indent=2)+'\n',encoding='utf-8')
 print(json.dumps([{'case':r['case'],'delta_reserve':r['plus_reserve_mm'],'limit':r['reference_deflection_mm'],'contacts':r['active_compression_contacts']} for r in rows]))
