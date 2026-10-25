"""Conservacao de massa, equilibrio e rastreio das fontes; sem ensaio real."""
from pathlib import Path
import json,hashlib,zipfile
from calcular import groups,G
HERE=Path(__file__).resolve().parent
d=json.loads((HERE/'Resultados.json').read_text(encoding='utf8'));h=json.loads((HERE/'Depurador_dados_e_pendencias.json').read_text(encoding='utf8'))
mass={};err=0.
for r in d['cases']:
 key=r['code'],r['rho_kg_m3'],r['payload_case']
 if key in mass:assert abs(mass[key]-r['wood_plus_content_kg'])<1e-9
 mass[key]=r['wood_plus_content_kg']
 assert abs(r['wood_plus_content_kg']-(r['body_mass_proxy_kg']+r['doors_mass_proxy_kg']+r['payload_kg']))<1e-9
 a=groups(r,.5,.8,1.);b=groups(r,.8,.8,1.)
 assert abs(a['total_traction_N']/b['total_traction_N']-1.6)<1e-10
 err=max(err,a['max_equilibrium_residual'],b['max_equilibrium_residual'])
 if r['code']=='P09':assert r['depurador_included'] is False
assert len(d['cases'])==1404 and len(d['envelopes'])==48
assert h['net_mass_manufacturer_kg']==6 and h['cabinet_mass_transfer_kg'] is None
assert h['nominal_interface']['vertical_gap_mm']==42.
assert hashlib.sha256(Path(h['manufacturer_document']).read_bytes()).hexdigest()==h['manual_sha256']
assert hashlib.sha256(Path(d['cad']).read_bytes()).hexdigest()==d['sha256']
assert hashlib.sha256((HERE/'Geometria_R51.json').read_bytes()).hexdigest()==d['geometry_input_sha256']
assert hashlib.sha256((HERE.parent/'Cinematica_offline_2026-10-25/Snapshot_R51.json').read_bytes()).hexdigest()==d['snapshot_input_sha256']
for p,hsh in d['code_sha256'].items():assert hashlib.sha256((HERE.parent/p).read_bytes()).hexdigest()==hsh
with zipfile.ZipFile(d['cad']) as z:assert z.testzip() is None
report=dict(global_cases=len(d['cases']),parametric_envelopes=48,mass_and_h_scaling_checks=len(d['cases']),
 max_force_moment_residual=err,source_sha256=d['sha256'],source_unchanged=True,source_zip_crc=True,input_hashes_passed=True,
 calculation_code_hashes_passed=True,manufacturer_manual_hash_passed=True,hood_transfer_not_assumed=True,physical_tests_performed=0,capacity_released=False,passed=True)
(HERE/'Verificacao.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
print(json.dumps(report,ensure_ascii=False))
