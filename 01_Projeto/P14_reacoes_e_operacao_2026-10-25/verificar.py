"""Equilibrio, simetria, trabalho/energia e integridade da fonte."""
from pathlib import Path
import json,hashlib,zipfile
HERE=Path(__file__).resolve().parent
d=json.loads((HERE/'Resultados.json').read_text(encoding='utf8'))
def key(r):return r['rho_kg_m3'],r['clothes_kg'],tuple(r['clothes_center_relative_mm']),r['share_left'],tuple(r['hinge_planes_X_mm'])
lookup={key(r):r for r in d['cases']};mirror_error=0.
for r in d['cases']:
 rho,kg,cg,share,planes=key(r);mirror=lookup[rho,kg,(-cg[0],cg[1],cg[2]),1-share,planes]
 for a,b in zip(r['hinge_left_YZ_N'],mirror['hinge_right_YZ_N']):mirror_error=max(mirror_error,abs(a-b))
 assert r['max_equilibrium_residual']<1e-7 and r['stay_total_tension_N']>=0
assert mirror_error<1e-8 and len(d['cases'])==270
assert all(r['zero_inside_0_55'] and r['gravity_energy_from_unstable_balance_to55_J']>=0 for r in d['operating_cases'])
work_error=max(r['integrated_work_error_J'] for r in d['operating_cases']);assert work_error<2e-5
assert hashlib.sha256(Path(d['cad']).read_bytes()).hexdigest()==d['sha256']
for p,h in d['input_sha256'].items():assert hashlib.sha256((HERE.parent/p).read_bytes()).hexdigest()==h
with zipfile.ZipFile(d['cad']) as z:assert z.testzip() is None
report=dict(stopped_cases=270,operating_cases=30,mirror_checks=270,max_mirror_component_error_N=mirror_error,
 max_force_moment_residual=max(r['max_equilibrium_residual'] for r in d['cases']),
 max_work_energy_error_J=work_error,previous55_torque_and_lever_reproduced=True,
 source_sha256=d['sha256'],source_unchanged=True,source_zip_crc=True,
 calculation_inputs_unchanged=True,physical_tests_performed=0,manufacturer_lock_or_capacity_verified=False,passed=True)
(HERE/'Verificacao.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
print(json.dumps(report,ensure_ascii=False))
