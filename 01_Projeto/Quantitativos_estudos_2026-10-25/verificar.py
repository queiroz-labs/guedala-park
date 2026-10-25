from pathlib import Path
import json,hashlib,zipfile,re
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
d=json.loads((HERE/'Diferencas_nominais.json').read_text(encoding='utf8'));f=json.loads((HERE/'Formatos_e_pendencias.json').read_text(encoding='utf8'))
assert hashlib.sha256((HERE/'extrair.py').read_bytes()).hexdigest()==d['script_sha256']
assert hashlib.sha256((HERE/'Diferencas_nominais.json').read_bytes()).hexdigest()==f['source_quantities_sha256']
assert len(d['rows'])==36 and sum(r['role']=='replacement'for r in d['rows'])==11 and len(d['kits'])==7
assert len(d['persisted_archives_sha256'])==7
for p,sha in d['persisted_archives_sha256'].items():
 path=ROOT/p;assert hashlib.sha256(path.read_bytes()).hexdigest()==sha,p
 with zipfile.ZipFile(path)as z:assert z.testzip()is None
for r in d['rows']:
 assert abs(r['delta_volume_mm3']-(r['new_volume_mm3']-r['old_volume_mm3']))<1e-7
 assert abs(r['delta_face_area_m2']*18*1e6-r['delta_volume_mm3'])<1e-6
 assert abs(r['delta_mass_kg_at650_800_900'][1]-r['delta_volume_mm3']*800/1e9)<1e-9
for kit in d['kits']:
 rows=[r for r in d['rows']if r['kit']==kit['kit']]
 assert abs(sum(r['delta_mass_kg_at650_800_900'][1]for r in rows)-kit['delta_mass_800_kg'])<1e-9
assert len(f['oversize_for2750x1850'])==1 and f['oversize_for2750x1850'][0]['old_source_object']=='Peca208'
assert all(r['wood_mass_credit_kg']is None for r in d['retired_schematic_supports_only_if_bench_adopted'])
for p in re.findall(r'\]\(([^)]+)\)',(HERE/'README.md').read_text(encoding='utf8')):
 if p!='Verificacao.json'and not p.startswith(('http','#')):assert (HERE/p).exists(),p
out=dict(wood_records=36,replacements=11,new_wood=25,kits=7,persisted_fcstd_files_including_source=7,hashes_crc=True,rectangle_volume_area_mass_identities=True,
 source_unchanged=True,purchase_sheet_count=None,budget_change=False,links=True,physical_tests=0,
 status='Quantitativos nominais separados conferidos; padroes/formato util/corte/fornecimento e adocao das propostas pendentes')
(HERE/'Verificacao.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf8');print(json.dumps(out,ensure_ascii=False))
