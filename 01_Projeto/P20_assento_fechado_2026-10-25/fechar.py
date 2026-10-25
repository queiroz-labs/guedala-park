"""Combina solicitacoes independentes e registra massa/perguntas, nao capacidade."""
from pathlib import Path
import json,hashlib,zipfile
HERE=Path(__file__).resolve().parent
g=json.loads((HERE/'Geometria_R51.json').read_text(encoding='utf8'))
r=json.loads((HERE/'Resultados.json').read_text(encoding='utf8'))
selected=[c for c in r['cases'] if c['case'] in ('maior_duas_pessoas_nominais','menor_centro')]
assert len(selected)==2
forces={}
for c in selected:
 for name,N in c['reactions_by_part_N'].items():forces[name]=forces.get(name,0)+N
body={x['name']:x for x in g['body']}
extra=['PecaBancoR029','PecaBancoR030','PecaBancoR007AtualR31','PecaBancoR006AtualR31']
volume=sum(body[n]['volume_mm3'] for n in g['structural_names']+extra)+sum(x['volume_mm3'] for x in g['lids'])
combined=dict(case='Duas massas80 na maior + uma80 no centro da menor, patches200x200',
  live_total_kg=240,self_mass_lids_proxy_kg=sum(c['self_mass_proxy_kg'] for c in selected),
  vertical_N_by_part=forces,body_group_K_required_N_mm_for_0_2mm={n:N/.2 for n,N in forces.items()},
  note='Requisito de grupo e caminho ate o piso; nao e rigidez/capacidade de parafuso. Exclui peso proprio do corpo, conteudo e excentricidades.')
mass=dict(parts=27,body_wood_names=g['structural_names']+extra,lid_names=[x['name'] for x in g['lids']],
  volume_m3=volume/1e9,sensitivity_kg_by_density={str(rho):volume*rho/1e9 for rho in (650,800,900)},
  excluded=['almofadas','tecido e espuma de encosto','saco/acessorios','ferragens e fixadores','itens guardados','diferencas reais do acabamento/composicao'],
  note='Volumes CAD vezes densidade hipotetica uniforme. Tampas20 sao envelope acabado: rever por camadas reais, nao somar acabamentos de novo sem decompor. Nao e pesagem nem lista final de corte.')
assert abs(sum(forces.values())-(240+combined['self_mass_lids_proxy_kg'])*9.80665)<1e-5
assert len(g['contacts'])==18 and len(g['floor_contacts'])==7
assert sum(c['state']=='face' for c in g['internal_interfaces'])==42
assert all(c['max_equilibrium_residual']<1e-4 and c['max_constraint_error_mm']<1e-6 and c['max_line_penetration_mm']<.02 and c['min_compression_reaction_N']>=-1e-6 for c in r['cases'])
assert hashlib.sha256(Path(g['cad']).read_bytes()).hexdigest()==g['sha256']
with zipfile.ZipFile(g['cad']) as z:assert z.testzip() is None
(HERE/'Caminho_e_massas.json').write_text(json.dumps(dict(combined=combined,mass_ledger=mass),indent=2,ensure_ascii=False)+'\n',encoding='utf8')
checks=dict(source_sha256=g['sha256'],source_unchanged=True,source_zip_crc=True,contact_lid_faces=18,
 floor_nominal_contacts=7,internal_face_interfaces=42,numeric_convergence_cases=len(r['checks']),
 max_degree14vs18_error=max(c['degree14vs18_relative_error'] for c in r['checks']),
 max_force_moment_residual=max(c['max_equilibrium_residual'] for c in r['cases']),
 max_support_line_penetration_mm=max(c.get('max_line_penetration_mm',0) for c in r['cases']),
 physical_tests_performed=0,passed=True)
(HERE/'Verificacao.json').write_text(json.dumps(checks,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
print(json.dumps(dict(checks=checks,mass=mass['sensitivity_kg_by_density'],groups=combined['body_group_K_required_N_mm_for_0_2mm']),ensure_ascii=False))
