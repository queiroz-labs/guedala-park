"""Demanda gravitacional da caixa inteira; resultantes, nao furos ou buchas.
UnidadesN,mm,kg. A distribuicao da tracao entre lados e parametrica.
"""
from pathlib import Path
import json,math,itertools,hashlib
import numpy as np
HERE=Path(__file__).resolve().parent
G=json.loads((HERE/'Geometria_e_portas_R51.json').read_text(encoding='utf8'))
grav=9.80665;mass_factor=18.3/18
def body(code,variant,rho):
 rows=[]
 for p in G['modules'][code]['body']:
  vol=p['volume_mm3'];cg=list(p['center_uvz_mm'])
  if variant=='wood_study':
   if code=='P04' and p['name']=='Peca268':vol*=308/272
   if code=='P15' and p['name'] in ('Peca359','Peca360'):vol*=598/580;cg[2]-=9
   if code=='P15' and p['name']=='Peca361':vol*=598/544;cg[2]-=9
  rows.append((vol*rho/1e9*mass_factor,cg,p['name']))
  if variant=='wood_study' and code=='P15' and p['name']=='Peca362':
   extra=list(cg);extra[2]-=18;rows.append((vol*rho/1e9*mass_factor,extra,'P15_segunda_camada18'))
 return rows
def patterns(code):
 doors=G['modules'][code]['doors'];patterns=set(itertools.product((0,86),repeat=len(doors)))
 patterns.add(tuple(45 for d in doors))
 for axis,sign in ((1,1),(0,1),(0,-1)):
  patterns.add(tuple(max(d['samples'],key=lambda s:sign*s['center_uvz_mm'][axis])['angle_deg'] for d in doors))
 return sorted(patterns)
def payloads(code):
 L=G['modules'][code]['width_mm'];D=G['modules'][code]['body_depth_mm'];total=10. if code=='P04' else 20.
 u=(5*(25+876.5)/2+2.5*(912.5+1320.25)/2+2.5*(1338.25+1764)/2)/10 if code=='P04' else L/2
 return [('empty',0.,u,(18+D)/2),('distributed',total,u,(18+D)/2),
  ('front',total,u,D-25),('near_u0',total,.05*L,D-25),('near_uL',total,.95*L,D-25)]
def global_case(code,variant,rho,angles,pload):
 items=body(code,variant,rho);woodbody=sum(m for m,c,n in items)
 doors=G['modules'][code]['doors']
 for d,angle in zip(doors,angles):
  pos=next(s['center_uvz_mm'] for s in d['samples'] if s['angle_deg']==angle)
  items.append((d['volume_mm3']*rho/1e9*mass_factor,pos,d['name']))
 label,mass,u,v=pload;items.append((mass,[u,v,0.],'contents'))
 M=sum(m for m,c,n in items);first=np.sum([m*np.array(c) for m,c,n in items],axis=0)
 return dict(code=code,variant=variant,rho_kg_m3=rho,door_angles_deg=list(angles),payload_case=label,payload_kg=mass,
  nominal_body_mass_proxy_kg=woodbody,door_mass_proxy_kg=sum(d['volume_mm3'] for d in doors)*rho/1e9*mass_factor,
  total_wood_plus_content_kg=M,center_uvz_mm=(first/M).tolist(),weight_N=M*grav,
  wall_normal_gravity_moment_Nm=float(first[1]*grav/1000),lateral_first_moment_Nmm=float(first[0]*grav))
def groups(r,h,span_ratio,share_u0):
 L=G['modules'][r['code']]['width_mm'];a=(1-span_ratio)*L/2;b=L-a
 right=(r['lateral_first_moment_Nmm']-a*r['weight_N'])/(b-a);left=r['weight_N']-right
 T=r['wall_normal_gravity_moment_Nm']*1000/h;t0=T*share_u0;tL=T-t0
 # Mesmo valor de compressao inferior em cada lado fecha o equilibrio normal/torsao.
 err=max(abs(left+right-r['weight_N']),abs(a*left+b*right-r['lateral_first_moment_Nmm']),abs((t0+tL)*h-r['wall_normal_gravity_moment_Nm']*1000))
 assert err<1e-7
 return dict(h_resultant_couple_mm=h,span_ratio=span_ratio,group_u_coordinates_mm=[a,b],
  tension_share_u0=share_u0,total_tension_N=T,total_lower_compression_N=T,
  group_vertical_N=[left,right],group_upper_tension_N=[t0,tL],group_lower_compression_N=[t0,tL],
  group_upper_resultant_N=[math.hypot(left,t0),math.hypot(right,tL)],max_equilibrium_residual=err)
def main():
 assert hashlib.sha256(Path(G['cad']).read_bytes()).hexdigest()==G['sha256']
 rows=[]
 for code in ('P04','P15'):
  for variant,rho,angles,pload in itertools.product(('current','wood_study'),(650,800,900),patterns(code),payloads(code)):
   r=global_case(code,variant,rho,angles,pload);r['id']=len(rows);rows.append(r)
 envelopes=[]
 for code,variant in itertools.product(('P04','P15'),('current','wood_study')):
  subset=[r for r in rows if r['code']==code and r['variant']==variant]
  heights=(100.,200.,272.) if code=='P04' else (200.,400.,544.)
  for h,span,share in itertools.product(heights,(1.,.8),(0.,.5,1.)):
   candidates=[(r,groups(r,h,span,share)) for r in subset]
   r,q=max(candidates,key=lambda pair:max(pair[1]['group_upper_resultant_N']))
   envelopes.append(dict(code=code,variant=variant,controls=dict(h_mm=h,span_ratio=span,tension_share_u0=share),
    case_id_max_upper_resultant=r['id'],demands=q,
    max_total_tension_N=max(p[1]['total_tension_N'] for p in candidates),
    max_vertical_per_group_N=max(max(p[1]['group_vertical_N']) for p in candidates),
    min_vertical_per_group_N=min(min(p[1]['group_vertical_N']) for p in candidates)))
 examples=[]
 for code in ('P04','P15'):
  for case in ('distributed','front'):
   for opened in (0,86):
    r=next(r for r in rows if r['code']==code and r['variant']=='wood_study' and r['rho_kg_m3']==900 and r['payload_case']==case and all(a==opened for a in r['door_angles_deg']))
    h=200 if code=='P04' else 400
    examples.append(dict(case=r,groups_equal=groups(r,h,1.,.5),groups_all_tension_u0=groups(r,h,1.,1.)))
 out=dict(cad=G['cad'],sha256=G['sha256'],mass_volume_factor=mass_factor,
  case_count=len(rows),cases=rows,envelopes=envelopes,examples=examples,
  geometry_input_sha256=hashlib.sha256((HERE/'Geometria_e_portas_R51.json').read_bytes()).hexdigest(),
  source_unchanged=True,scope='Peso proprio de madeira e conteudo nominal. Toda ferragem/adesivo/acabamento real deve ser reconciliado. VolumesBREP18 escalados18.3/18 como aproximacao de massa, nao dimensao de corte. Grupos/h/span/share sao resultantes parametrizadas, nao montagem de suspensor. Sem resistencia da caixa/parede, cargas de mao, impacto ou ensaio.')
 (HERE/'Resultados.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
 print(json.dumps([dict(code=e['case']['code'],payload=e['case']['payload_case'],doors=e['case']['door_angles_deg'],kg=e['case']['total_wood_plus_content_kg'],V=e['case']['weight_N'],M=e['case']['wall_normal_gravity_moment_Nm'],T=e['groups_equal']['total_tension_N']) for e in examples],ensure_ascii=False))
if __name__=='__main__':main()
