from pathlib import Path
import json,hashlib,zipfile,re
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
d=json.loads((HERE/'Resultados.json').read_text(encoding='utf8'));g=json.loads((HERE/'Conferencia_geometrica.json').read_text(encoding='utf8'))
assert hashlib.sha256(Path(d['cad']).read_bytes()).hexdigest()==d['source_sha256']==g['source_sha256']
for p,sha in d['input_sha256'].items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==sha,p
assert len(d['cases'])==len(d['convergence'])==6
for c in d['cases']:
 assert max(abs(c[k])for k in ['eq_force_N','eq_moment_x_Nmm','eq_moment_y_Nmm','constraint_error_mm'])<1e-5
 assert c['max_removed_contact_penetration_mm']<1e-6
 for role,R in zip(c['support_role'],c['reactions_N']):
  if role!='left_positive_joint':assert R> -1e-7
 assert c['plus_reserve_mm']>c['reference_mm']
assert max(c['degree16vs20_relative']for c in d['convergence'])<.05
assert len(g['contacts'])==4 and not g['added_material_interferences']
assert abs(g['added_nominal_mass_800_kg']-d['added_wood_nominal_mass_800_kg'])<1e-8
study=Path(g['study']);assert hashlib.sha256(study.read_bytes()).hexdigest()==g['study_sha256']
for p in (study,Path(d['cad'])):
 with zipfile.ZipFile(p)as z:assert z.testzip() is None
for p in re.findall(r'\]\(([^)]+)\)',(HERE/'README.md').read_text(encoding='utf8')):
 if p!='Verificacao.json' and not p.startswith(('http','#')):assert (HERE/p).exists(),p
out=dict(plate_cases=6,convergences=6,max_relative_change16_20=max(c['degree16vs20_relative']for c in d['convergence']),
 unilateral_contact_equilibrium=True,new_interfaces_checked=4,source_shapes_interference_scope=g['visible_source_shapes_tested'],
 source_hash_crc=True,input_hashes=True,local_links=True,physical_tests=0,source_unchanged=True,
 status='Conferido. Contato traseiro geometricamente possivel; modelo reduzido excede referencia e nao libera base/caixa.')
(HERE/'Verificacao.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf8');print(json.dumps(out,ensure_ascii=False))
