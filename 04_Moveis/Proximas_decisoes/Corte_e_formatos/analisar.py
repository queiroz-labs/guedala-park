"""Triagem e arranjo nominal de envelopes; não modifica fontes, CAD ou lista-base."""
from __future__ import annotations

import csv
import hashlib
import io
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path
from xml.sax.saxutils import escape

HERE = Path(__file__).resolve().parent
BASE = HERE.parents[2]
PARAMS = json.loads((HERE / 'Parametros.json').read_text(encoding='utf-8'))
FICHAS = BASE / '06_Entregas/Fichas_fabricacao'
STUDIES = BASE / '04_Moveis/Quantitativos'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(name, data):
    (HERE / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def csv_out(name, rows, fields):
    with (HERE / name).open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields, delimiter=';', extrasaction='ignore')
        writer.writeheader()
        for row in rows:
            writer.writerow({k: (' | '.join(map(str, v)) if isinstance(v, list) else v) for k, v in row.items()})


def input_paths():
    return [*sorted(FICHAS.glob('P??-pecas.csv')), STUDIES / 'Diferencas_nominais.json',
            STUDIES / 'Formatos_e_pendencias.json', BASE / 'ferramentas/site/src/cad-data.js']


def packing_blockers(row):
    reasons = []
    if row['partial_finish']:
        reasons.append('Faces/composição ainda parciais: ' + row['partial_finish'])
    if 'referência' in row['specification'] or row['specification'].startswith('Ver regra'):
        reasons.append('Padrão ou material aparente não individualizado como produto escolhido')
    if 'Espelho (camada distinta' in row['specification']:
        reasons.append('Espelho é camada distinta; composição do substrato não formalizada')
    if row['thickness_mm'] not in (15, 16, 18):
        reasons.append('Espessura de envelope não tratada como chapa comercial: composição a definir')
    return reasons


def load_base():
    panels = []
    for path in sorted(FICHAS.glob('P??-pecas.csv')):
        with path.open(encoding='utf-8-sig', newline='') as f:
            for line, raw in enumerate(csv.DictReader(f, delimiter=';'), 2):
                names = raw['IDs CAD'].split(' | ')
                assert len(names) == int(raw['Qtd'])
                for name in names:
                    row = dict(id=name, module=path.stem[:3], label=raw['Peça'],
                        C_mm=float(raw['C nominal mm']), L_mm=float(raw['L nominal mm']),
                        thickness_mm=float(raw['Esp. envelope mm']), specification=raw['Especificação documental'],
                        cad_reference=raw['Referência CAD'], contour=raw['Contorno'], partial_finish=raw['Acabamento parcial'],
                        edge_grain_machining=raw['Bordas/veios/usinagem'], source_csv=path.relative_to(BASE).as_posix(),
                        source_line=line, net_area_m2=None, substrate_product=None, grain_axis=None,
                        purchase_ready=False)
                    row['envelope_area_m2'] = row['C_mm'] * row['L_mm'] / 1e6
                    row['packing_blockers'] = packing_blockers(row)
                    row['included_in_virtual_plan'] = not row['packing_blockers']
                    panels.append(row)
    assert len(panels) == 249 and len({p['id'] for p in panels}) == 249
    return panels


def fits(C, L, fmt, trim, allowance=0):
    a, b = C + 2 * allowance, L + 2 * allowance
    x, y = fmt['length_mm'] - 2 * trim, fmt['width_mm'] - 2 * trim
    return {'C_parallel_long': a <= x + 1e-8 and b <= y + 1e-8,
            'L_parallel_long': b <= x + 1e-8 and a <= y + 1e-8,
            'usable_length_mm': x, 'usable_width_mm': y}


def triage_records(panels, proposed):
    result = []
    for scope, rows in [('base_R52', panels), ('proposta_separada', proposed)]:
        for p in rows:
            for fmt in PARAMS['formats']:
                for trim in (0, 10, 20):
                    status = fits(p['C_mm'], p['L_mm'], fmt, trim)
                    result.append(dict(scope=scope, id=p['id'], kit=p.get('kit', ''), format=fmt['id'],
                        trim_per_edge_mm=trim, **status,
                        fits_allow_rotation=status['C_parallel_long'] or status['L_parallel_long']))
    return result


def proposed_records(panels):
    source = json.loads((STUDIES / 'Diferencas_nominais.json').read_text(encoding='utf-8'))
    lookup = {p['id']: p for p in panels}
    rows, mismatch = [], []
    for p in source['rows']:
        t, short, long = p['new_sorted_nominal_dims_mm']
        old = lookup.get(p['source_object'])
        if p['role'] == 'replacement':
            actual = sorted([old['C_mm'], old['L_mm'], old['thickness_mm']]) if old else None
            if actual != p['old_sorted_nominal_dims_mm']:
                mismatch.append(dict(id=p['study_object'], source_object=p['source_object'],
                    current_base_dims=actual, study_old_dims=p['old_sorted_nominal_dims_mm']))
        calculated_area = short * long / 1e6
        assert abs(calculated_area - p['proposed_fabrication_face_area_m2']) < 1e-9
        row = dict(id=p['study_object'], kit=p['kit'], source_object=p['source_object'], role=p['role'],
            C_mm=long, L_mm=short, thickness_mm=t, envelope_area_m2=calculated_area,
            old_area_m2=p['old_face_area_m2'], delta_area_m2=p['delta_face_area_m2'],
            specification_if_replacement=old['specification'] if old else None,
            material_adopted=False, source_file=p['study_file'])
        rows.append(row)
    assert len(rows) == 36
    return rows, mismatch


def p01_requirements():
    rows = []
    for name, C, L in [('Peca208_atual', 2096, 1964), ('Proposta_fundo_P01', 2114, 1964)]:
        for fmt in PARAMS['formats']:
            for allowance in (0, 2):
                for trim in (0, 5, 10, 20, 50, 66, 68, 70):
                    state = fits(C, L, fmt, trim, allowance)
                    rows.append(dict(id=name, C_mm=C, L_mm=L, format=fmt['id'],
                        trim_per_edge_mm=trim, allowance_per_edge_mm=allowance, **state,
                        raw_min_C_parallel_long_mm=[C + 2 * allowance + 2 * trim, L + 2 * allowance + 2 * trim],
                        raw_min_L_parallel_long_mm=[L + 2 * allowance + 2 * trim, C + 2 * allowance + 2 * trim],
                        max_symmetric_trim_C_parallel_mm=min((fmt['length_mm']-C)/2, (fmt['width_mm']-L)/2)-allowance,
                        max_symmetric_trim_L_parallel_mm=min((fmt['length_mm']-L)/2, (fmt['width_mm']-C)/2)-allowance))
    return rows


def pack_group(panels, allow_rotation, trim, kerf, allowance, sort_key):
    ordered = sorted(panels, key=sort_key, reverse=True)
    sheets, unplaced = [], []
    for p in ordered:
        C, L = p['C_mm'] + 2 * allowance, p['L_mm'] + 2 * allowance
        options = [(C, L, False)] + ([(L, C, True)] if allow_rotation and C != L else [])

        def best_existing():
            candidates = []
            for si, sheet in enumerate(sheets):
                for fi, (x, y, w, h) in enumerate(sheet['free_rectangles']):
                    for pw, ph, rotated in options:
                        if pw <= w + 1e-8 and ph <= h + 1e-8:
                            candidates.append(((min(w-pw, h-ph), w*h-pw*ph, si), si, fi, pw, ph, rotated))
            return min(candidates, key=lambda v: v[0]) if candidates else None

        match = best_existing()
        if match is None:
            fmt = next((f for f in PARAMS['formats'] if any(
                pw <= f['length_mm']-2*trim+1e-8 and ph <= f['width_mm']-2*trim+1e-8
                for pw, ph, _ in options)), None)
            if fmt is None:
                unplaced.append(p['id'])
                continue
            sheets.append(dict(format=fmt['id'], stock_length_mm=fmt['length_mm'], stock_width_mm=fmt['width_mm'],
                free_rectangles=[(trim, trim, fmt['length_mm']-2*trim, fmt['width_mm']-2*trim)], placements=[], cuts=[]))
            match = best_existing()
        _, si, fi, pw, ph, rotated = match
        sheet = sheets[si]
        x, y, fw, fh = sheet['free_rectangles'].pop(fi)
        rw, rh = fw-pw, fh-ph
        # Both choices partition the free rectangle and reserve a kerf strip.
        if rw >= rh:
            additions = [(x+pw+kerf, y, rw-kerf, fh), (x, y+ph+kerf, pw, rh-kerf)]
            split = 'vertical_then_horizontal'
        else:
            additions = [(x, y+ph+kerf, fw, rh-kerf), (x+pw+kerf, y, rw-kerf, ph)]
            split = 'horizontal_then_vertical'
        sheet['free_rectangles'].extend(r for r in additions if r[2] > 1e-8 and r[3] > 1e-8)
        sheet['placements'].append(dict(id=p['id'], module=p['module'], x_mm=x, y_mm=y,
            blank_C_along_x_mm=pw, blank_L_along_y_mm=ph, rotated_90=rotated,
            nominal_C_mm=p['C_mm'], nominal_L_mm=p['L_mm'], contour=p['contour'],
            envelope_not_finished_cut=p['contour'] != 'Retangular'))
        sheet['cuts'].append(dict(source_free_rectangle_mm=[x, y, fw, fh], split=split,
            piece_id=p['id'], piece_blank_mm=[pw, ph], kerf_mm=kerf))
    for i, sheet in enumerate(sheets, 1):
        sheet['sheet_in_group'] = i
        sheet['envelope_area_m2'] = sum(p['blank_C_along_x_mm']*p['blank_L_along_y_mm'] for p in sheet['placements']) / 1e6
        sheet['usable_area_m2'] = (sheet['stock_length_mm']-2*trim)*(sheet['stock_width_mm']-2*trim)/1e6
        sheet['envelope_utilization'] = sheet['envelope_area_m2']/sheet['usable_area_m2']
        sheet.pop('free_rectangles')
    return dict(sheets=sheets, unplaced=unplaced)


def make_plan(panels):
    groups = defaultdict(list)
    excluded = []
    for p in panels:
        if p['packing_blockers']:
            excluded.append(p['id'])
        else:
            groups[(p['specification'], p['thickness_mm'])].append(p)
    result = []
    strategies = [('area', lambda p: (p['C_mm']*p['L_mm'], p['C_mm'])),
                  ('long_side', lambda p: (p['C_mm'], p['L_mm'])),
                  ('short_side', lambda p: (p['L_mm'], p['C_mm']))]
    for scenario in PARAMS['packing_scenarios']:
        output = dict(id=scenario['id'], allow_rotation=scenario['allow_rotation'], meaning=scenario['meaning'],
                      groups=[], excluded_ids=excluded)
        for i, ((spec, thick), pieces) in enumerate(sorted(groups.items()), 1):
            trials = [(label, pack_group(pieces, scenario['allow_rotation'], PARAMS['trim_per_edge_mm'],
                PARAMS['kerf_mm'], PARAMS['blank_allowance_per_edge_mm'], key)) for label, key in strategies]
            label, best = min(trials, key=lambda t: (len(t[1]['unplaced']), len(t[1]['sheets']),
                sum(s['stock_length_mm']*s['stock_width_mm'] for s in t[1]['sheets'])))
            output['groups'].append(dict(id=f'G{i:02}', specification=spec, nominal_thickness_mm=thick,
                substrate_product=None, faces_and_stock_availability_confirmed=False,
                pieces=len(pieces), strategy=label, **best))
        output['virtual_sheets'] = sum(len(g['sheets']) for g in output['groups'])
        output['included_panels'] = sum(g['pieces'] for g in output['groups'])
        result.append(output)
    return result


def draw_sheets(plans):
    dest = HERE / 'Planos_svg'
    dest.mkdir(exist_ok=True)
    for scenario in plans:
        if scenario['id'] != 'rotacao_livre':
            continue
        for group in scenario['groups']:
            for sheet in group['sheets']:
                W, H = sheet['stock_length_mm'], sheet['stock_width_mm']
                filename = f"{group['id']}_chapa_{sheet['sheet_in_group']:02}.svg"
                svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-65 -155 {W+130} {H+270}">',
                    '<rect x="-65" y="-155" width="100%" height="100%" fill="white"/>',
                    f'<text x="0" y="-100" font-family="sans-serif" font-size="32">{group["id"]} · {escape(group["specification"])} · {group["nominal_thickness_mm"]:g} mm</text>',
                    f'<text x="0" y="-45" font-family="sans-serif" font-size="27">Chapa virtual {sheet["sheet_in_group"]} · {W:g}×{H:g} · refilo {PARAMS["trim_per_edge_mm"]:g}/borda · serra {PARAMS["kerf_mm"]:g}</text>',
                    f'<rect x="0" y="0" width="{W}" height="{H}" fill="#f5f5f2" stroke="#333" stroke-width="3"/>']
                for p in sheet['placements']:
                    x,y,w,h = p['x_mm'], p['y_mm'], p['blank_C_along_x_mm'], p['blank_L_along_y_mm']
                    svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#dce8df" stroke="#275241" stroke-width="1.2"/>')
                    label = f'{p["id"]} · {w:g}×{h:g}'
                    rotate = h > w*1.2
                    along, across = (h,w) if rotate else (w,h)
                    size = max(8, min(24, (along-8)/(len(label)*0.62), across/3))
                    transform = f'rotate(90 {x+w/2} {y+h/2})' if rotate else ''
                    svg.append(f'<text x="{x+w/2}" y="{y+h/2}" transform="{transform}" text-anchor="middle" font-family="sans-serif" font-size="{size:.1f}">{escape(label)}</text>')
                svg.append(f'<text x="0" y="{H+65}" font-family="sans-serif" font-size="27">Envelopes geométricos; não é corte executivo. Veio/faces/substrato/processo pendentes.</text></svg>')
                (dest / filename).write_text('\n'.join(svg), encoding='utf-8')
                sheet['svg'] = 'Planos_svg/' + filename


def main():
    before = {p.relative_to(BASE).as_posix(): sha(p) for p in input_paths()}
    cad_text = (BASE / 'ferramentas/site/src/cad-data.js').read_text(encoding='utf-8')
    cad = json.loads(re.search(r'const CAD_DATA\s*=\s*(\{.*\});',cad_text,re.S)[1])
    assert cad['current_revision']==PARAMS['cad_revision'], 'Cache não corresponde à revisão declarada'
    panels = load_base()
    proposed, mismatch = proposed_records(panels)
    triage = triage_records(panels, proposed)
    plans = make_plan(panels)
    draw_sheets(plans)
    p01 = p01_requirements()
    summary = dict(date=PARAMS['date'], cad_revision=PARAMS['cad_revision'],
        base_panels=len(panels), base_rectangular=sum(p['contour']=='Retangular' for p in panels),
        base_special=sum(p['contour']!='Retangular' for p in panels),
        base_envelope_area_m2=sum(p['envelope_area_m2'] for p in panels),
        proposal_records=len(proposed), proposal_replacements=sum(p['role']=='replacement' for p in proposed),
        proposal_new=sum(p['role']=='new_wood' for p in proposed), proposal_vs_current_base_mismatches=mismatch,
        kits=sorted({p['kit'] for p in proposed}), grain_axis_defined_panels=0,
        substrate_product_defined_panels=0,
        fit_results=[dict(scope=scope, format=fmt, trim_per_edge_mm=trim,
            not_fitting_ids=[r['id'] for r in triage if r['scope']==scope and r['format']==fmt and r['trim_per_edge_mm']==trim and not r['fits_allow_rotation']])
            for scope in ('base_R52','proposta_separada') for fmt in ('2750x1850','2750x2100') for trim in (0,10,20)],
        plans=[dict(id=p['id'], virtual_sheets=p['virtual_sheets'], included_panels=p['included_panels'],
            excluded_panels=len(p['excluded_ids']), sheets_by_format=dict(Counter(s['format'] for g in p['groups'] for s in g['sheets']))) for p in plans],
        status=PARAMS['plan_status'])
    save('Lista_base_249.json', panels)
    save('Propostas_36.json', proposed)
    kits = []
    for name in sorted({p['kit'] for p in proposed}):
        rows = [p for p in proposed if p['kit']==name]
        kits.append(dict(kit=name,proposed_parts=len(rows),replacements=sum(p['role']=='replacement' for p in rows),
            new_parts=sum(p['role']=='new_wood' for p in rows),
            proposed_envelope_area_m2=sum(p['envelope_area_m2'] for p in rows),
            replaced_area_m2=sum(p['old_area_m2'] for p in rows),
            delta_area_m2=sum(p['delta_area_m2'] for p in rows),
            adopted=False,base_unchanged=True))
    save('Resumo_kits.json',kits)
    save('Triagem_formatos.json', triage)
    save('Requisito_fundo_P01.json', p01)
    save('Planos_preliminares.json', dict(parameters=PARAMS, scenarios=plans))
    save('Resumo.json', summary)
    save('Fontes_e_hashes.json', dict(date=PARAMS['date'], inputs_sha256=before,
        unchanged=before=={p.relative_to(BASE).as_posix():sha(p) for p in input_paths()},
        generator_sha256=sha(HERE/'analisar.py'), parameters_sha256=sha(HERE/'Parametros.json')))
    csv_out('Lista_base_249.csv', panels, ['id','module','label','C_mm','L_mm','thickness_mm','specification',
        'partial_finish','contour','envelope_area_m2','net_area_m2','included_in_virtual_plan','packing_blockers','source_csv','source_line'])
    csv_out('Propostas_36.csv', proposed, ['id','kit','source_object','role','C_mm','L_mm','thickness_mm',
        'envelope_area_m2','old_area_m2','delta_area_m2','specification_if_replacement','material_adopted','source_file'])
    csv_out('Resumo_kits.csv',kits,['kit','proposed_parts','replacements','new_parts','proposed_envelope_area_m2',
        'replaced_area_m2','delta_area_m2','adopted','base_unchanged'])
    csv_out('Peças_sem_definicao_suficiente.csv',[p for p in panels if p['packing_blockers']],
        ['id','module','C_mm','L_mm','thickness_mm','specification','partial_finish','packing_blockers','source_csv','source_line'])
    csv_out('Requisito_fundo_P01.csv',p01,['id','C_mm','L_mm','format','trim_per_edge_mm','allowance_per_edge_mm',
        'C_parallel_long','L_parallel_long','usable_length_mm','usable_width_mm','raw_min_C_parallel_long_mm',
        'raw_min_L_parallel_long_mm','max_symmetric_trim_C_parallel_mm','max_symmetric_trim_L_parallel_mm'])
    placements = [dict(scenario=p['id'], group=g['id'], specification=g['specification'], thickness_mm=g['nominal_thickness_mm'],
        sheet=s['sheet_in_group'], format=s['format'], **row) for p in plans for g in p['groups'] for s in g['sheets'] for row in s['placements']]
    csv_out('Arranjos_preliminares.csv', placements, ['scenario','group','specification','thickness_mm','sheet','format','id','module',
        'x_mm','y_mm','blank_C_along_x_mm','blank_L_along_y_mm','rotated_90','nominal_C_mm','nominal_L_mm','contour','envelope_not_finished_cut'])
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
