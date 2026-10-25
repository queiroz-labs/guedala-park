from pathlib import Path
import json,hashlib,zipfile,re
import numpy as np
HERE=Path(__file__).resolve().parent
d=json.loads((HERE/'Resultados.json').read_text(encoding='utf8'));g=json.loads((HERE/'Geometria_R51.json').read_text(encoding='utf8'))
assert d['source_sha256']==g['sha256']==hashlib.sha256(Path(g['cad']).read_bytes()).hexdigest()
for p,sha in d['input_sha256'].items():assert hashlib.sha256((HERE/p).read_bytes()).hexdigest()==sha,p
assert [len(g['wood'][k])for k in ('P01','P03','P02')]==[47,7,10]
assert len(g['upper_contacts'])==8 and all(c['area_mm2']>0 for c in g['upper_contacts'])
assert all(x['nominal_course_mm']==500 and x['extension_mm']==0 for x in g['drawer_groups'].values())
A=np.array(d['cases_rows']);assert A.shape==(4608,len(d['cases_columns'])) and len(d['envelopes'])==72
assert np.isfinite(A).all()
W=A[:,7]*9.80665
assert np.max(np.abs(A[:,11]+A[:,12]-W*.650))<1e-7
assert np.max(np.abs(A[:,13]+A[:,14]-W*2.000))<1e-7
assert np.min(A[:,11:15])>0
assert np.max(np.abs(A[:,15]-W/270720*1000))<1e-9
for env in d['envelopes']:
 mask=(A[:,:5]==[env['rho'],env['level'],env['P02_coupled'],env['mirror_hypothesis'],env['additional_mass_kg']]).all(axis=1)
 subset=A[mask];assert len(subset)==64
 assert max(subset[:,7])-min(subset[:,7])<1e-8
 assert abs(env['worst_front']['resisting_moments_Nm']['front']-min(subset[:,11]))<1e-7
for e in d['contact_examples']:
 assert e['contact_model']['force_moment_residual']<1e-5 and e['contact_convergence_relative']<.03
 assert abs(sum(e['contact_model']['force_by_floor_part_N'].values())-e['weight_N'])<1e-7
with zipfile.ZipFile(g['cad']) as z:assert z.testzip() is None
for p in re.findall(r'\]\(([^)]+)\)',(HERE/'README.md').read_text(encoding='utf8')):
 if p!='Verificacao.json' and not p.startswith(('http','#')):assert (HERE/p).exists(),p
out=dict(cases=4608,envelopes=72,wood_parts_P01_P03_P02=[47,7,10],upper_face_contacts=8,nominal_floor_regions=23,nominal_floor_area_m2=.270720,
 moment_identities_and_movement_mass_checks=True,rigid_bed_examples=3,source_hash_crc=True,input_hashes=True,local_links=True,physical_tests=0,
 status='Conferencia matematica/geometrica aprovada; caixa real, transferencia dos superiores, piso, material e ferragens condicionados')
(HERE/'Verificacao.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf8');print(json.dumps(out,ensure_ascii=False))
