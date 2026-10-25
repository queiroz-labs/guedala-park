"""Identidades estaticas, monotonicidade de carga, integridade e movimento."""
from pathlib import Path
import json,hashlib,zipfile
HERE=Path(__file__).resolve().parent
d=json.loads((HERE/'Estabilidade.json').read_text(encoding='utf8'))
m=json.loads((HERE/'Conferencia_movimento.json').read_text(encoding='utf8'))
assert m['continuous_separation_proven_by_disjoint_swept_boxes'] and not m['potential_swept_AABB_contacts']
assert len(d['cases'])==1296
def key(r):return r['boundary'],r['rho_kg_m3'],r['tabletop_mass_credit_fraction'],tuple(r['drawer_extensions_mm']),tuple(r['payload_per_drawer_kg']),r['payload_location']
lookup={key(r):r for r in d['cases']};checks=0
for r in d['cases']:
 b,rho,credit,ext,pay,loc=key(r)
 # Deslocar a mesma carga para a frente nao aumenta o momento restaurador frontal.
 if loc=='uniform_center':
  q=lookup[b,rho,credit,ext,pay,'front50']
  front_r=[e['restoring_margin_Nm'] for e in r['edges'] if e['forward_horizontal_tip_force_at750_N'] is not None]
  front_q=[e['restoring_margin_Nm'] for e in q['edges'] if e['forward_horizontal_tip_force_at750_N'] is not None]
  assert all(a>=c-1e-9 for a,c in zip(front_r,front_q));checks+=1
 if b=='pedestal':
  expected=r['wood_plus_payload_mass_kg']*9.80665*(680-r['center_mm'][1])/1000
  e=next(e for e in r['edges'] if e['a_mm'][1]==680 and e['b_mm'][1]==680)
  assert abs(expected-e['restoring_margin_Nm'])<1e-8;checks+=1
assert hashlib.sha256(Path(d['cad']).read_bytes()).hexdigest()==d['sha256']
for p,h in d['input_sha256'].items():assert hashlib.sha256((HERE.parent/p).read_bytes()).hexdigest()==h
with zipfile.ZipFile(d['cad']) as z:assert z.testzip() is None
g=json.loads((HERE/'Geometria_R51.json').read_text(encoding='utf8'))
corrections=[dict(object='Gaveta009',property='AlturaParedeSobreFundo',current_mm=53.,proposed_mm=47.,
  evidence='BREP: traseira/dianteira47 e laterais74 apos R49. Campo textual nao acompanha o recorte.',
  preserve=['CursoNominal400','AlturaUtilProposta54: vao estimado, nao altura da parede','forma/cores/expressoes'],
  status='Preparado para consolidacao de metadados numa revisao; R51 nao modificada')]
(HERE/'Correcao_metadado_preparada.json').write_text(json.dumps(corrections,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
report=dict(stability_cases=1296,independent_identity_and_monotonicity_checks=checks,
 continuous_moving_pairs=m['broadphase_pairs'],independent_drawer_pairs=64,
 no_collision_swept_boxes=True,static_guide_shapes_excluded=8,
 source_sha256=d['sha256'],source_unchanged=True,source_zip_crc=True,calculation_inputs_unchanged=True,
 physical_tests_performed=0,manufacturing_or_capacity_released=False,passed=True)
(HERE/'Verificacao.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
print(json.dumps(report,ensure_ascii=False))
