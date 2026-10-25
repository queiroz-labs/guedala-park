"""Quatro caixas atuais: demanda global, usando a cinematica ja validada."""
from pathlib import Path
import sys,json,itertools,math,hashlib
import numpy as np
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'Cinematica_offline_2026-10-25'))
from cinematica import Engine
G=json.loads((HERE/'Geometria_R51.json').read_text(encoding='utf8'))
engine=Engine();grav=9.80665;factor=18.3/18
def canonical(code,world):
 m=G['modules'][code];p=(np.array(m['module_inverse_matrix']).reshape(4,4)@np.r_[world,1])[:3];o=m['canonical_origin']
 return [float(p[0]-o['u0_module_mm']),float(o['rear_module_mm']-p[1]),float(p[2]-o['z0_module_mm'])]
poses={}
for code,m in G['modules'].items():
 for d in m['leaves']:
  n=d['leaf'];poses[n]={}
  for angle in range(87):poses[n][angle]={f:canonical(code,c) for f,c in engine.centers(n,angle).items() if f in d['fronts']}
def patterns(code):
 leaves=G['modules'][code]['leaves'];a=set(itertools.product((0,86),repeat=len(leaves)));a.add(tuple(45 for d in leaves))
 for axis,sign in ((1,1),(0,1),(0,-1)):
  a.add(tuple(max(poses[d['leaf']],key=lambda angle:sign*poses[d['leaf']][angle][d['fronts'][0]][axis]) for d in leaves))
 return sorted(a)
def payloads(code):
 m=G['modules'][code];L,D=m['width_mm'],m['body_depth_mm'];rows=[('empty',0.,L/2,(18+D)/2)]
 for kg in (5.,10.,20.):
  rows.extend([(f'{kg:g}_center',kg,L/2,(18+D)/2),(f'{kg:g}_front',kg,L/2,D-25),
   (f'{kg:g}_near_u0',kg,.05*L,D-25),(f'{kg:g}_near_uL',kg,.95*L,D-25)])
 return rows
def global_case(code,rho,angles,pload):
 m=G['modules'][code];items=[]
 for p in m['body']:
  dims=np.array(p['box_module_mm'][3:])-p['box_module_mm'][:3]
  massfactor=factor if abs(min(dims)-18)<1e-6 else 1.
  items.append((p['volume_mm3']*rho/1e9*massfactor,p['center_uvz_mm']))
 bodymass=sum(w for w,c in items);doormass=0.
 for d,angle in zip(m['leaves'],angles):
  leaf=engine.data['leaves'][d['leaf']]
  for f in leaf['fronts']:
   if f['name'] not in d['fronts']:continue
   mass=f['volume_mm3']*rho/1e9*factor;doormass+=mass;items.append((mass,poses[d['leaf']][angle][f['name']]))
 label,kg,u,v=pload;items.append((kg,[u,v,0.]))
 total=sum(w for w,c in items);first=sum((w*np.array(c) for w,c in items),np.zeros(3))
 return dict(code=code,rho_kg_m3=rho,door_angles_deg=list(angles),payload_case=label,payload_kg=kg,
  body_mass_proxy_kg=bodymass,doors_mass_proxy_kg=doormass,wood_plus_content_kg=total,
  center_uvz_mm=(first/total).tolist(),weight_N=total*grav,
  wall_normal_moment_Nm=float(first[1]*grav/1000),lateral_first_moment_Nmm=float(first[0]*grav),
  depurador_included=False if code=='P09' else None)
def groups(r,h_ratio,span_ratio,share):
 m=G['modules'][r['code']];h=m['height_mm']*h_ratio;L=m['width_mm'];a=L*(1-span_ratio)/2;b=L-a
 R1=(r['lateral_first_moment_Nmm']-r['weight_N']*a)/(b-a);R0=r['weight_N']-R1
 T=r['wall_normal_moment_Nm']*1000/h;tt=[share*T,(1-share)*T]
 err=max(abs(R0+R1-r['weight_N']),abs(R0*a+R1*b-r['lateral_first_moment_Nmm']),abs(sum(tt)*h-r['wall_normal_moment_Nm']*1000))
 assert err<1e-7
 return dict(h_ratio=h_ratio,h_mm=h,span_ratio=span_ratio,group_u_mm=[a,b],traction_share_u0=share,
  total_traction_N=T,lower_total_compression_N=T,upper_vertical_N=[R0,R1],upper_traction_N=tt,
  upper_resultant_N=[math.hypot(R0,tt[0]),math.hypot(R1,tt[1])],max_equilibrium_residual=err)
def main():
 assert hashlib.sha256(Path(G['cad']).read_bytes()).hexdigest()==G['sha256']==engine.data['sha256']
 assert hashlib.sha256((HERE.parent/'Cinematica_offline_2026-10-25/Snapshot_R51.json').read_bytes()).hexdigest()==G['snapshot_sha256']
 rows=[]
 for code in G['modules']:
  for rho,angles,pload in itertools.product((650,800,900),patterns(code),payloads(code)):
   r=global_case(code,rho,angles,pload);r['id']=len(rows);rows.append(r)
 envelopes=[]
 for code in G['modules']:
  subset=[r for r in rows if r['code']==code]
  for h,span,share in itertools.product((.5,.8),(1.,.8),(0.,.5,1.)):
   all_cases=[(r,groups(r,h,span,share)) for r in subset]
   r,q=max(all_cases,key=lambda pair:max(pair[1]['upper_resultant_N']))
   envelopes.append(dict(code=code,case_id=r['id'],groups=q,
    max_total_traction_N=max(q['total_traction_N'] for r,q in all_cases),
    min_vertical_per_group_N=min(min(q['upper_vertical_N']) for r,q in all_cases)))
 examples=[]
 for code in G['modules']:
  for label in ('10_center','10_front','20_front'):
   r=next(r for r in rows if r['code']==code and r['rho_kg_m3']==900 and r['payload_case']==label and all(a==86 for a in r['door_angles_deg']))
   examples.append(dict(case=r,groups=groups(r,.8,1.,1.)))
 data=dict(cad=G['cad'],sha256=G['sha256'],cases=rows,case_count=len(rows),envelopes=envelopes,examples=examples,
  code_sha256={p.relative_to(HERE.parent).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in [HERE/'calcular.py',HERE.parent/'Cinematica_offline_2026-10-25/cinematica.py']},
  geometry_input_sha256=hashlib.sha256((HERE/'Geometria_R51.json').read_bytes()).hexdigest(),
  snapshot_input_sha256=G['snapshot_sha256'],source_unchanged=True,
  scope='Caixas atuais de madeira, sem tubos e sem adotar reforcos. Conteudo0/5/10/20kg total por movel e parametrico; nao capacidade ou por prateleira. h/span/share sao resultantes, nao furos. Exclui ferragens, equipamentos, esforcos de mao, resistencia da caixa/parede e ensaio. P09 nao inclui depurador: transferencia real desconhecida.')
 (HERE/'Resultados.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
 manual=HERE.parents[1]/'02_Plantas_e_manuais/Manuais/Suggar_DE61IX_DE62IX.pdf'
 hood=dict(model='SuggarDE61IX, familia60cm',manufacturer_document=str(manual),manual_sha256=hashlib.sha256(manual.read_bytes()).hexdigest(),
  source='Manual arquivadoREV.0025, pagina1, tabela de caracteristicas e figuras5..8; imagem arquivada conferida.',
  net_mass_manufacturer_kg=6.,weight_N=6*grav,not_measured=True,
  manual_fixing_path='Primeiro apoio/fixacao a parede; fixacao superior ao gabinete com quatro parafusos4.2x30. Tipos e quantidades citados como documento, nao ancoragem aprovada no substrato real.',
  cabinet_mass_transfer_kg=None,cabinet_force_transfer=None,
  nominal_interface=G['depurador_interface_nominal'],
  unit_extra_global_wall_moment_Nm_for_CG_v_m={str(v):6*grav*v for v in (0.,.15,.30,.488)},
  limit='CG nao publicado;v sao sensibilidades, nao posicoes medidas. Casos de armario nao somam6kg a um grupo sem conhecer partilha, excentricidades e rigidez. Produto e caixa sao um sistema com fixacoes redundantes.')
 (HERE/'Depurador_dados_e_pendencias.json').write_text(json.dumps(hood,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
 print(json.dumps(dict(cases=len(rows),envelopes=len(envelopes),examples=[dict(code=e['case']['code'],kg=e['case']['payload_kg'],case=e['case']['payload_case'],V=e['case']['weight_N'],M=e['case']['wall_normal_moment_Nm'],h=e['groups']['h_mm'],T=e['groups']['total_traction_N']) for e in examples]),ensure_ascii=False))
if __name__=='__main__':main()
