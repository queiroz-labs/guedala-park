from pathlib import Path
import json,hashlib,zipfile,re
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
d=json.loads((HERE/'Resultados.json').read_text(encoding='utf8'))
assert hashlib.sha256(Path(d['source']).read_bytes()).hexdigest()==d['source_sha256']=='ab5323bb12f8eca40b25bdfe4eadc8a3221c82b0646f354cd1f2832acfb27c16'
for p,sha in d['inputs_sha256'].items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==sha,p
assert len(d['cases'])==16 and len(d['checks'])==5
for c in d['cases']:
 assert max(abs(c[k])for k in ['eq_force_N','eq_moment_x_Nmm','eq_moment_y_Nmm','constraint_error_mm'])<1e-5
 assert c['interface_shear_screen'][1]['max_sample_shear_MPa']<=c['interface_shear_screen'][0]['max_sample_shear_MPa']+1e-10
for E in (2200,1600):
 cases=[c for c in d['cases'] if c['E_initial_MPa']==E]
 assert all(a['deflection_mm']>b['deflection_mm']for a,b in zip(cases,cases[1:]))
for c in d['checks']:
 assert c.get('relative_error',0)<.02
 assert c.get('error_mm',0)<1e-7 and c.get('deflection_error_mm',0)<1e-8 and c.get('reaction_error_N',0)<1e-7
assert len(d['shear_refinement_one_partial_case'])==3
for r in d['thresholds']:assert abs(r['degree18']-799/300)<.0001
with zipfile.ZipFile(d['source'])as z:assert z.testzip()is None
for p in re.findall(r'\]\(([^)]+)\)',(HERE/'README.md').read_text(encoding='utf8')):
 if p!='Verificacao.json' and not p.startswith(('http','#')):assert (HERE/p).exists(),p
out=dict(response_cases=16,numerical_main_checks=5,partial_case_shear_refinement_degrees=[14,18,22],source_hash_crc=True,input_hashes=True,links=True,
 physical_tests=0,source_unchanged=True,adhesive_selected=None,
 status='Modelo parcial conferido. Nenhum ks/resistencia/durabilidade comercial atribuido. TitebondMelamine excluida por limitacao expressa do fabricante.')
(HERE/'Verificacao.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf8');print(json.dumps(out,ensure_ascii=False))
