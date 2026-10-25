"""Equilibrio3D na parada55 e energia gravitacional da geometria nominal.
Reaproveita a montagem candidata do estudo23/10; sem validar ferragens.
"""
from pathlib import Path
import json,math,hashlib,itertools
import numpy as np
HERE=Path(__file__).resolve().parent
G=json.loads((HERE/'Geometria_R51.json').read_text(encoding='utf8'))
OLD=json.loads((HERE.parent/'Banco_cesto_simples_2026-10-23/Conferencia/Resultados.json').read_text(encoding='utf8'))
parts={p['name']:p for p in G['parts']};g=9.80665
origin=np.array([4555.,6440.,120.])
sc=next(c for c in OLD['articuladores'] if c['id']=='cesto_direito')
fixed=np.array(sc['fixed']);mobile=np.array(sc['mobile'])
ANGLE=55.;a=math.radians(ANGLE)
def rot(p,angle):
 x,y,z=np.asarray(p)-origin;t=math.radians(angle);c,s=math.cos(t),math.sin(t)
 return np.array([x,y*c-z*s,y*s+z*c])
mob=rot([4555.,*mobile],ANGLE)
u_yz=(fixed-np.array([mob[1]+origin[1],mob[2]+origin[2]]));distance=float(np.linalg.norm(u_yz));u=np.array([0.,*u_yz/distance])
lever=float(np.cross(mob,u)[0])
def masses(rho,clothes_kg,cloth_relative):
 result=[]
 for i in range(3,17):
  p=parts[f'PecaCestoR{i:03d}'];result.append((p['volume_mm3']*rho/1e9,np.asarray(p['center_mm'])))
 if clothes_kg:result.append((clothes_kg,origin+np.asarray(cloth_relative)))
 return result
def stopped(rho,clothes_kg,cloth_relative,share_left=.5,hinge_planes=(4320.,4790.)):
 ms=masses(rho,clothes_kg,cloth_relative);W=sum(m*g for m,p in ms)
 gravity=np.array([0.,0.,-W]);M=sum((np.cross(rot(p,ANGLE),[0,0,-m*g]) for m,p in ms),np.zeros(3))
 T=-M[0]/lever
 stays=[]
 # O planoX de cada barra e o meio da reserva transversal do estudo.
 for x,share in [(4304.,share_left),(4806.,1-share_left)]:
  r=mob.copy();r[0]=x-origin[0];stays.append((r,T*share*u))
 Fs=sum((v for r,v in stays),np.zeros(3));Ms=sum((np.cross(r,v) for r,v in stays),np.zeros(3))
 x1,x2=np.asarray(hinge_planes)-origin[0]
 Fy=-Fs[1];Fz=W-Fs[2]
 Ry2=(-Ms[2]-x1*Fy)/(x2-x1);Ry1=Fy-Ry2
 Rz2=(M[1]+Ms[1]-x1*Fz)/(x2-x1);Rz1=Fz-Rz2
 hinges=[np.array([0.,Ry1,Rz1]),np.array([0.,Ry2,Rz2])]
 # Momento nominal de excentricidadeX ate a face interna da lateral.
 # Centro real do grupoY/Z e geometria da ferragem continuam pendentes.
 wall_X=(4278.,4832.)
 pin_wall_moments=[np.cross([xp-xw,0,0],-R)/1000 for xp,xw,R in zip(hinge_planes,wall_X,hinges)]
 stay_wall_moments=[np.cross([xs-xw,0,0],-force)/1000 for xs,xw,(r,force) in zip((4304.,4806.),wall_X,stays)]
 residualF=gravity+Fs+sum(hinges,np.zeros(3))
 residualM=M+Ms+np.cross([x1,0,0],hinges[0])+np.cross([x2,0,0],hinges[1])
 assert max(np.max(np.abs(residualF)),np.max(np.abs(residualM)))<1e-7
 assert T>=0
 return dict(rho_kg_m3=rho,clothes_kg=clothes_kg,clothes_center_relative_mm=list(cloth_relative),
  share_left=share_left,hinge_planes_X_mm=list(hinge_planes),weight_N=W,gravity_moment_Nm=float(M[0]/1000),
  stay_total_tension_N=float(T),stay_left_N=float(T*share_left),stay_right_N=float(T*(1-share_left)),
  hinge_left_YZ_N=[float(Ry1),float(Rz1)],hinge_right_YZ_N=[float(Ry2),float(Rz2)],
  hinge_left_resultant_N=float(np.linalg.norm(hinges[0])),hinge_right_resultant_N=float(np.linalg.norm(hinges[1])),
  min_hinge_vertical_N=float(min(Rz1,Rz2)),
  hinge_wall_interface_MYZ_Nm=[m[1:].tolist() for m in pin_wall_moments],
  stay_wall_interface_MYZ_Nm=[m[1:].tolist() for m in stay_wall_moments],
  max_equilibrium_residual=float(max(np.max(np.abs(residualF)),np.max(np.abs(residualM)))))

def operating(rho,clothes_kg,cloth_relative):
 ms=masses(rho,clothes_kg,cloth_relative)
 A=sum(m*(p[1]-origin[1])/1000 for m,p in ms);B=sum(m*(p[2]-origin[2])/1000 for m,p in ms)
 root=math.degrees(math.atan2(A,B))
 # U=max na raiz interna; torque abre acima dela, fecha abaixo.
 def U(angle):t=math.radians(angle);return g*(A*math.sin(t)+B*math.cos(t))
 def M(angle):t=math.radians(angle);return g*(-A*math.cos(t)+B*math.sin(t))
 path=np.linspace(0,ANGLE,551);torques=[M(t) for t in path]
 radius=math.hypot(parts['PecaCestoR003']['center_mm'][1]-origin[1],parts['PecaCestoR003']['box_mm'][5]-origin[2])/1000
 energy=(U(root)-U(ANGLE)) if 0<=root<=ANGLE else None
 # Trabalho gravitacional = -DeltaU, validado independentemente por quadratura.
 theta=np.linspace(0,a,1101);mom=g*(-A*np.cos(theta)+B*np.sin(theta))
 numerical=float(np.trapezoid(mom,theta));exact=U(0)-U(ANGLE)
 assert abs(numerical-exact)<2e-5
 return dict(rho_kg_m3=rho,clothes_kg=clothes_kg,clothes_center_relative_mm=list(cloth_relative),
  zero_torque_angle_deg=root,zero_inside_0_55=0<=root<=ANGLE,
  torque_closed_Nm=M(0),torque55_Nm=M(55),max_abs_torque_0_55_Nm=max(abs(v) for v in torques),
  ideal_top_tangential_force_max_N=max(abs(v) for v in torques)/radius,
  theoretical_grip_radius_m=radius,gravity_energy_from_unstable_balance_to55_J=energy,
  integrated_work_error_J=abs(numerical-exact))

def main():
 assert hashlib.sha256(Path(G['cad']).read_bytes()).hexdigest()==G['sha256']
 assert abs(distance-291)<1e-6 and abs(abs(lever)/1000-OLD['cesto_tracao_estatica']['braco_efetivo_m'])<1e-10
 clothes=[(0,(0.,125.,225.)),(8,(0.,125.,225.))]
 clothes += [(8,tuple(p)) for p in itertools.product((-200.,200.),(25.,225.),(25.,425.))]
 rows=[];operation=[]
 for rho in (650,800,900):
  for kg,cg in clothes:
   operation.append(operating(rho,kg,cg))
   for share in (0.,.5,1.):
    for planes in ((4320.,4790.),(4310.,4800.),(4330.,4780.)):
     rows.append(stopped(rho,kg,cg,share,planes))
 worst=max(rows,key=lambda r:max(r['hinge_left_resultant_N'],r['hinge_right_resultant_N']))
 uplift=min(rows,key=lambda r:r['min_hinge_vertical_N'])
 maxT=max(rows,key=lambda r:r['stay_total_tension_N'])
 maxenergy=max(operation,key=lambda r:r['gravity_energy_from_unstable_balance_to55_J'] or 0)
 # Replica do caso rho900, extremoY25/Z425 do estudo anterior.
 assert abs(maxT['gravity_moment_Nm']-OLD['cesto_tracao_estatica']['torque_Nm'])<1e-9
 template=dict(status='PENDENTE; nao preencher massa desconhecida com zero',included_in_current_calculation=False,
  components=[dict(component=n,mass_kg=None,center_or_trajectory_mm=None,sku=None) for n in
   ['saco/alcas','pega','revestimento_real_da_frente','buchas/pivos_partes_moveis','parafusos_e_terminais_moveis','barras_articuladas_esquerda','barras_articuladas_direita']],
  rule='Massa presa a armacao: CG local real. Barras articuladas: CG por angulo e geometria propria; nao girar toda a barra como se fosse frente. Separar partes fixas. Dados preenchidos nao sao importados automaticamente: revisar e ampliar o modelo antes da rodada completa.')
 if not (HERE/'Componentes_pendentes.json').exists():
  (HERE/'Componentes_pendentes.json').write_text(json.dumps(template,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
 data=dict(cad=G['cad'],sha256=G['sha256'],
  input_sha256={str(p.relative_to(HERE.parent)):hashlib.sha256(p.read_bytes()).hexdigest() for p in
   [HERE/'Geometria_R51.json',HERE.parent/'Banco_cesto_simples_2026-10-23/Conferencia/Resultados.json']},
  angle_deg=ANGLE,stay_axis_distance_mm=distance,
  stay_unit_vector_global_XYZ=u.tolist(),effective_lever_signed_mm=lever,
  cases=rows,operating_cases=operation,worst_pivot=worst,worst_uplift=uplift,worst_tension=maxT,worst_gravity_energy=maxenergy,
  source_unchanged=True,passed=True,
  scope='Corpo movel rigido nominal, frente+13 pecas de armacao e0/8kg roupa. Em cada trajetoria CG da roupa fixo relativamente a armacao; nao simula acomodacao do tecido. Planos de reacao de pivôs assumidos a partir dos pinos ideais; barras travadas tratadas como bielas axiais na parada55. Nao corresponde ao engate comercial comprovado. Exclui saco, ferragens/pega adicionais, atrito, maos, choque, resistencia e flexao de juntas.')
 (HERE/'Resultados.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
 print(json.dumps(dict(cases=len(rows),operation_cases=len(operation),worst_pivot=worst,worst_uplift=uplift,worst_tension=maxT,worst_energy=maxenergy),ensure_ascii=False))
if __name__=='__main__':main()
