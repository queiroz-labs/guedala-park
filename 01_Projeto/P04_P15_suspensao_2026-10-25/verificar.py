"""Equilibrio, conservacao de massa nas portas, escala de h e fonte."""
from pathlib import Path
import json,hashlib,zipfile
from calcular import groups
HERE=Path(__file__).resolve().parent
d=json.loads((HERE/'Resultados.json').read_text(encoding='utf8'))
g=json.loads((HERE/'Geometria_e_portas_R51.json').read_text(encoding='utf8'))
assert d['case_count']==660 and len(d['envelopes'])==72
mass_groups={};checks=0
for r in d['cases']:
 key=r['code'],r['variant'],r['rho_kg_m3'],r['payload_case']
 if key in mass_groups:assert abs(mass_groups[key]-r['total_wood_plus_content_kg'])<1e-10
 mass_groups[key]=r['total_wood_plus_content_kg']
 a=groups(r,200.,.8,1.);b=groups(r,400.,.8,1.)
 assert abs(a['total_tension_N']-2*b['total_tension_N'])<1e-9
 assert abs(sum(a['group_vertical_N'])-r['weight_N'])<1e-9
 checks+=1
for code,m in g['modules'].items():
 for door in m['doors']:
  assert len(door['samples'])==87
  assert max(abs(a-b) for a,b in zip(door['samples'][0]['center_uvz_mm'],door['center_closed_uvz_mm']))<1e-7
  assert all(abs(s['center_uvz_mm'][2]-door['center_closed_uvz_mm'][2])<1e-7 for s in door['samples'])
  checks+=1
assert g['source_controllers_unchanged']
session=json.loads((HERE/'Confirmacao_sessao.json').read_text(encoding='utf8'))
assert not session['temporary_document_present'] and session['source_angles']==[0.]*6 and session['source_object_count']==5833
assert hashlib.sha256(Path(d['cad']).read_bytes()).hexdigest()==d['sha256']
assert hashlib.sha256((HERE/'Geometria_e_portas_R51.json').read_bytes()).hexdigest()==d['geometry_input_sha256']
with zipfile.ZipFile(d['cad']) as z:assert z.testzip() is None
report=dict(global_load_cases=660,parametric_group_envelopes=72,independent_checks=checks,
 door_leaves=6,poses_per_leaf=87,source_controller_states_unchanged=True,
 source_sha256=d['sha256'],source_unchanged=True,source_zip_crc=True,input_unchanged=True,
 physical_tests_performed=0,wall_substrate_known=False,manufacturer_capacity_verified=False,passed=True)
(HERE/'Verificacao.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
print(json.dumps(report,ensure_ascii=False))
