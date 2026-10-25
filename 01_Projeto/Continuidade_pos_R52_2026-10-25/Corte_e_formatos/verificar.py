"""Confere cobertura, margens, serra e separação dos planos nominais persistidos."""
from copy import deepcopy
from collections import Counter, defaultdict
import csv
import hashlib
import itertools
import json
from pathlib import Path

import analisar

HERE = Path(__file__).resolve().parent
BASE = HERE.parents[2]
EPS = 1e-7


def read(name):
    return json.loads((HERE / name).read_text(encoding='utf-8'))


def validate(scenarios, panels, trim, kerf, allowance):
    errors, pair_checks = [], 0
    lookup = {p['id']: p for p in panels}
    included = {p['id'] for p in panels if not p['packing_blockers']}
    excluded = {p['id'] for p in panels if p['packing_blockers']}
    for scenario in scenarios:
        seen = []
        if set(scenario['excluded_ids']) != excluded:
            errors.append('Exclusões não correspondem às pendências de material/faces')
        for group in scenario['groups']:
            if group['unplaced']:
                errors.append('Peças não alocadas: ' + ','.join(group['unplaced']))
            for sheet in group['sheets']:
                W, H = sheet['stock_length_mm'], sheet['stock_width_mm']
                actual_area = 0
                for p in sheet['placements']:
                    seen.append(p['id'])
                    source = lookup[p['id']]
                    x,y,w,h = p['x_mm'], p['y_mm'], p['blank_C_along_x_mm'], p['blank_L_along_y_mm']
                    if min(w,h) <= 0 or x < trim-EPS or y < trim-EPS or x+w > W-trim+EPS or y+h > H-trim+EPS:
                        errors.append('Retângulo fora da janela útil: ' + p['id'])
                    if source['specification'] != group['specification'] or source['thickness_mm'] != group['nominal_thickness_mm']:
                        errors.append('Material/espessura trocados: ' + p['id'])
                    if p['rotated_90'] and not scenario['allow_rotation']:
                        errors.append('Rotação proibida no cenário: ' + p['id'])
                    nominal = [source['C_mm'] + 2*allowance, source['L_mm'] + 2*allowance]
                    if p['rotated_90']:
                        nominal.reverse()
                    if max(abs(w-nominal[0]),abs(h-nominal[1])) > EPS:
                        errors.append('Dimensão do blank alterada: ' + p['id'])
                    actual_area += w*h/1e6
                if abs(actual_area-sheet['envelope_area_m2']) > EPS:
                    errors.append('Área de envelopes não reconciliada')
                for a,b in itertools.combinations(sheet['placements'],2):
                    pair_checks += 1
                    xgap = max(b['x_mm']-(a['x_mm']+a['blank_C_along_x_mm']),
                               a['x_mm']-(b['x_mm']+b['blank_C_along_x_mm']))
                    ygap = max(b['y_mm']-(a['y_mm']+a['blank_L_along_y_mm']),
                               a['y_mm']-(b['y_mm']+b['blank_L_along_y_mm']))
                    if max(xgap,ygap) < kerf-EPS:
                        errors.append('Sobreposição ou intervalo menor que a serra: '+a['id']+'/'+b['id'])
        if set(seen) != included or len(seen) != len(included):
            errors.append('Plano perdeu, duplicou ou acrescentou IDs')
    return errors, pair_checks


def main():
    panels = read('Lista_base_249.json')
    proposals = read('Propostas_36.json')
    plans = read('Planos_preliminares.json')
    params = plans['parameters']
    errors, pairs = validate(plans['scenarios'],panels,params['trim_per_edge_mm'],params['kerf_mm'],params['blank_allowance_per_edge_mm'])
    assert not errors, errors
    assert len(panels)==249 and len({p['id'] for p in panels})==249
    assert len(proposals)==36 and len({(p['kit'],p['id']) for p in proposals})==36
    assert Counter(p['role'] for p in proposals)=={'replacement':11,'new_wood':25}
    assert not read('Resumo.json')['proposal_vs_current_base_mismatches']
    # Independent total from the grouped source CSVs, before expansion by ID.
    area = 0
    count = 0
    for path in sorted((BASE/'05_Entregas/Fichas_fabricacao_R13').glob('P??-pecas.csv')):
        for row in csv.DictReader(path.open(encoding='utf-8-sig',newline=''),delimiter=';'):
            qty = int(row['Qtd'])
            count += qty
            area += qty*float(row['C nominal mm'])*float(row['L nominal mm'])/1e6
    assert count==249 and abs(area-sum(p['envelope_area_m2'] for p in panels))<EPS
    original = json.loads((BASE/'01_Projeto/Quantitativos_estudos_2026-10-25/Diferencas_nominais.json').read_text(encoding='utf-8'))
    for kit in original['kits']:
        parts = [p for p in proposals if p['kit']==kit['kit']]
        assert len(parts)==kit['proposed_wood_parts']
        assert abs(sum(p['envelope_area_m2'] for p in parts)-kit['proposed_fabrication_face_area_m2'])<EPS
        assert abs(sum(p['delta_area_m2'] for p in parts)-kit['delta_face_area_m2'])<EPS
    # Boundary tests close the precise P01 format requirement.
    big = params['formats'][1]
    assert analisar.fits(2096,1964,big,68)['C_parallel_long']
    assert not analisar.fits(2096,1964,big,68.001)['C_parallel_long']
    assert analisar.fits(2096,1964,big,2)['L_parallel_long']
    assert not analisar.fits(2096,1964,big,2.001)['L_parallel_long']
    assert not analisar.fits(2114,1964,big,0)['L_parallel_long']
    assert analisar.fits(2114,1964,big,66,2)['C_parallel_long']
    assert not analisar.fits(2114,1964,big,66.001,2)['C_parallel_long']
    # Perturbations ensure that the checker detects the actual placement defects.
    corrupted = deepcopy(plans['scenarios'])
    sheet = next(s for g in corrupted[0]['groups'] for s in g['sheets'] if len(s['placements'])>1)
    sheet['placements'][1]['x_mm']=sheet['placements'][0]['x_mm']
    sheet['placements'][1]['y_mm']=sheet['placements'][0]['y_mm']
    assert validate(corrupted,panels,params['trim_per_edge_mm'],params['kerf_mm'],params['blank_allowance_per_edge_mm'])[0]
    corrupted = deepcopy(plans['scenarios'])
    corrupted[0]['groups'][0]['sheets'][0]['placements'].append(deepcopy(corrupted[0]['groups'][0]['sheets'][0]['placements'][0]))
    assert validate(corrupted,panels,params['trim_per_edge_mm'],params['kerf_mm'],params['blank_allowance_per_edge_mm'])[0]
    # Repack in memory with different saw allowances and verify each geometry.
    sensitivity = []
    for kerf in (0,3.2,6.4):
        groups = []
        for g in plans['scenarios'][0]['groups']:
            subset = [p for p in panels if p['specification']==g['specification'] and p['thickness_mm']==g['nominal_thickness_mm'] and not p['packing_blockers']]
            packed = analisar.pack_group(subset,True,params['trim_per_edge_mm'],kerf,params['blank_allowance_per_edge_mm'],lambda p:(p['C_mm']*p['L_mm'],p['C_mm']))
            groups.append(dict(g,**packed))
        scenario=dict(plans['scenarios'][0],groups=groups)
        err,checks=validate([scenario],panels,params['trim_per_edge_mm'],kerf,params['blank_allowance_per_edge_mm'])
        assert not err,err
        sensitivity.append(dict(kerf_mm=kerf,pair_checks=checks,virtual_sheets=sum(len(g['sheets']) for g in groups),valid=True))
    sources = read('Fontes_e_hashes.json')
    assert sources['unchanged']
    for name,expected in sources['inputs_sha256'].items():
        assert hashlib.sha256((BASE/name).read_bytes()).hexdigest()==expected, name
    assert sources['generator_sha256']==analisar.sha(HERE/'analisar.py')
    assert sources['parameters_sha256']==analisar.sha(HERE/'Parametros.json')
    report = dict(base_panels=249,proposals=36,proposal_replacements=11,proposal_new=25,
        current_base_compatible_with_old_study_dimensions=True,
        base_area_from_independent_grouped_csv=area,nominal_pair_checks=pairs,
        no_overlap_or_kerf_violation=True,inside_usable_sheets=True,IDs_exactly_once_per_scenario=True,
        group_material_and_thickness_consistent=True,scenario_rotation_policy_respected=True,
        P01_boundary_tests=True,overlap_and_duplicate_mutations_detected=True,
        kerf_sensitivity=sensitivity,source_hashes_unchanged=True,
        purchase_release=False,physical_tests=0,
        limits='Somente envelopes e separação geométrica. Cortes especiais, fita/selagem, face útil, veio, substrato, manuseio, ferramenta e sequência real da oficina não demonstrados.')
    analisar.save('Verificacao.json',report)
    print(json.dumps(report,ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
