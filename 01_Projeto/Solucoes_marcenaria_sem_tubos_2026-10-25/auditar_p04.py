"""Conferencia com eixos extraidos nativamente, distinguindo ponto e grupo."""
from pathlib import Path
import json,hashlib
import numpy as np
HERE=Path(__file__).resolve().parent
native=json.loads((HERE/'P04_eixos_conferidos_R51.json').read_text(encoding='utf8'))
d=json.loads((HERE/'Resultados.json').read_text(encoding='utf8'));c=next(x for x in d['cases']if x['case'].startswith('P04_'))
axes=np.array(native['individual_axes_mm']);L=native['base_length_mm']
assert np.allclose(axes,[16,885.5,903.5,1329.25]) and abs(L-1764)<1e-8
individual=np.diff(np.r_[0,axes,L]);group=np.array([axes[0],np.mean(axes[1:3]),axes[3],L])
group_spans=np.diff(group)
assert abs(max(individual)-869.5)<1e-8 and abs(max(group_spans)-878.5)<1e-8
assert abs(c['criterion_mm']-max(individual)/300)<1e-8
assert c['joint_K_base_initial_required_N_mm']==1000
assert c['joint_lower_or_upper_group_initial_required_N_mm']==2000
assert c['whole_divider_path_K_differed_N_mm']==2*c['division_path_K_differed_N_mm']==500
source=Path(d['cad']);assert hashlib.sha256(source.read_bytes()).hexdigest()==d['sha256']==native['source_sha256']
out=dict(individual_axes_mm=axes.tolist(),max_individual_axis_spacing_mm=float(max(individual)),active_criterion_mm=c['criterion_mm'],
 previous_group_center_mm=float(group[1]),previous_three_group_spacings_mm=group_spans.tolist(),previous_criterion_mm=c['previous_group_center_reference_mm'],
 deflection_plus_reserve_unchanged_mm=c['deflection_plus_reserve_mm'],
 joint_per_position_initial_N_mm=1000,two_position_lower_or_upper_group_initial_N_mm=2000,
 one_series_path_initial_N_mm=500,one_series_path_sensitivity_N_mm=250,two_path_divider_initial_N_mm=1000,two_path_divider_sensitivity_N_mm=500,
 status='Eixos nativos/criterio e escopo das rigidezes conferidos. Texto anterior por grupo corrigido sem mudar matriz/flecha. Modelo de referencias equivalentes nao valida acoplamento da caixa real.',
 source_unchanged=True,physical_tests=0)
(HERE/'P04_auditoria_referencias.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf8');print(json.dumps(out,ensure_ascii=False))
