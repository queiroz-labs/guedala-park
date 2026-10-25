from pathlib import Path
import json,hashlib,zipfile,re
HERE=Path(__file__).resolve().parent
d=json.loads((HERE/'Resultados.json').read_text(encoding='utf8'))
geo=json.loads((HERE/'Conferencia_geometrica.json').read_text(encoding='utf8'))
assert hashlib.sha256(Path(d['cad']).read_bytes()).hexdigest()==d['sha256']==geo['source_sha256']
for p,sha in d['inputs_sha256'].items():assert hashlib.sha256((HERE.parent/p).read_bytes()).hexdigest()==sha,p
assert len(d['cases'])==11 and len(d['checks'])==6 and all(c['passed'] for c in d['checks'])
for c in d['cases']:
 assert max(abs(c[k]) for k in ['eq_force_N','eq_moment_x_Nmm','eq_moment_y_Nmm','constraint_error_mm','top_force_equilibrium_error_N'])<1e-5
 assert abs(sum(c['upper_group_force_N'])-c['local_total_mass_in_path_kg']*9.80665)<1e-6
assert len(geo['contacts'])==16 and len(geo['nominal_axes'])==58 and not geo['added_material_interferences']
assert all(abs(c['area_mm2']-c['expected_mm2'])<.01 for c in geo['contacts'])
study=Path(geo['study']);assert hashlib.sha256(study.read_bytes()).hexdigest()==geo['study_sha256']
for p in [study,Path(d['cad'])]:
 with zipfile.ZipFile(p) as z:assert z.testzip() is None
for target in re.findall(r'\]\(([^)]+)\)',(HERE/'README.md').read_text(encoding='utf8')):
 if target!='Verificacao.json' and not target.startswith(('http','#')):assert (HERE/target).exists(),target
out=dict(convergences=len(d['checks']),equilibrium_cases=len(d['cases']),max_relative_change_16_20=max(c['degree16vs20_relative_error'] for c in d['checks']),
 contacts=16,nominal_axes=58,source_shapes_interference_scope=geo['visible_source_shapes_tested'],source_sha256=d['sha256'],
 input_hashes=True,source_unchanged=True,zip_crc=True,local_links=True,physical_tests=0,status='Verificacoes numericas e de integridade aprovadas; hipoteses, produto e capacidade real nao validados')
(HERE/'Verificacao.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf8');print(json.dumps(out,ensure_ascii=False))
