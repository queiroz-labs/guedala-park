"""Verificacao independente dos cortes, contatos, acessos e reconciliacao."""
from pathlib import Path
from collections import Counter
import argparse, csv, itertools, json
import numpy as np
from fontes import sha, HASH_RULE

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT/'04_Moveis/Aereos_suspensao'


def read(p):
    return json.loads(p.read_text(encoding='utf-8'))


def main(code):
    d = read(OUT/f'{code}_caminho_caixa.json')
    geo = read(OUT/'Lote_B_geometria.json')
    source = read(OUT/'Lote_B_detalhamento.json')
    susp = read(OUT/f'{code}_suspensao.json')
    assert d['hash_rule'] == HASH_RULE
    assert d['script_sha256'] == sha(Path(__file__).with_name('mapear_caminho_caixa.py'))
    assert d['hash_helper_sha256'] == sha(Path(__file__).with_name('fontes.py'))
    for p, h in d['sources_sha256'].items():
        assert sha(ROOT/p) == h, p
    release = read(ROOT/'ferramentas/site/current_release.json')
    assert sha(ROOT/release['cadPath']) == d['cad_sha256']
    assert d['physical_tests_executed'] == 0 and not d['cad_changed'] and not d['cad_opened']
    boxes = d['boxes_uvz_mm']; meta = d['pieces']; groups = {r['id']: r for r in d['groups']}
    expected = (21, 70, 42, 24, 4) if code == 'P17' else (9, 21, 9, 12, 0)
    assert (len(groups), len(d['fastener_axes'])) == expected[:2]
    count = Counter()
    for r in groups.values():
        count[r['family'].split()[0]] += r['candidate_count']
        a, b = np.array(boxes[r['a']]), np.array(boxes[r['b']])
        lo, hi = np.maximum(a[:3], b[:3]), np.minimum(a[3:], b[3:])
        delta = hi-lo
        assert min(delta) >= -1e-6 and sum(delta > 1e-6) == 2
        assert abs(np.prod(delta[delta > 1e-6])-r['contact_area_mm2']) < 1e-6
        for p in r['interface_points_uvz_mm']:
            assert np.all(np.array(p) >= lo-1e-6) and np.all(np.array(p) <= hi+1e-6)
        assert len(r['interface_points_uvz_mm']) == r['candidate_count']
        # Todos estes grupos sao linhas de pontos. A linha nao fornece
        # um binario independente em torno de si sem rigidez adicional.
        pts = np.array(r['interface_points_uvz_mm'])
        paired = r['family'].startswith('Parafuso4x30')
        assert np.linalg.matrix_rank(pts-pts[0], tol=1e-7) == (2 if paired else 1)
        assert r['ideal_point_force_rank'] == (6 if paired else 5)
        assert not r['capacity_demonstrated'] and not r['stiffness_demonstrated']
    assert (count['Confirmat7x50'], count['Minifix15'], count['Parafuso4x30']) == expected[2:]
    original = [r for r in geo['historical_map'] if r['code'] == code]
    for r in original:
        match = [g for g in groups.values() if {g['a'], g['b']} == {r['a'], r['b']}]
        assert len(match) == 1 and match[0]['candidate_count'] == r['old_connector_qty']
    if code == 'P12':
        assert not any({r['a'], r['b']} == {meta['back'], v} for r in groups.values() for v in [meta['base'], meta['top']])
    obstacles = dict(boxes)
    obstacles.update({r['name']: r['box_uvz_mm'] for r in susp['static_calcos']})
    obstacles.update({f'support_{r["side"]}': r['envelope_uvz_mm'] for r in susp['mounts']})
    def intersect_volume(a, b):
        spans = np.minimum(a[3:], b[3:])-np.maximum(a[:3], b[:3])
        return float(np.prod(np.maximum(0., spans)))
    for a in d['fastener_axes']:
        gr = groups[a['group']]
        assert a['interface_uvz_mm'] in gr['interface_points_uvz_mm']
        assert not a['actual_tool_verified'] and not a['actual_head_pilot_torque_selected']
        assert all(intersect_volume(a['access_bbox_mm'], box) < 1e-8 for box in obstacles.values())
        if a['family'] in ['Confirmat', 'Face4x30']:
            expected_length = 50. if a['family'] == 'Confirmat' else 30.
            assert abs(np.linalg.norm(np.array(a['tip_uvz_mm'])-a['entry_uvz_mm'])-expected_length) < 1e-6
            b = np.array(a['nominal_body_bbox_mm'])
            assert abs(sum(intersect_volume(b, boxes[n]) for n in [gr['a'], gr['b']])-np.prod(b[3:]-b[:3])) < 1e-6
            assert all(intersect_volume(b, box) < 1e-8 for n, box in obstacles.items() if n not in [gr['a'], gr['b']])
            if a['family'] == 'Face4x30':
                assert code == 'P17' and a['entry_uvz_mm'][0] == 964 and a['tip_uvz_mm'][0] == 994
                assert max(boxes[n][3] for n in [gr['a'], gr['b']])-a['tip_uvz_mm'][0] == 6
        else:
            ref = next(j for j in source['joints'] if j['code'] == code and j['id'] == a['id'])
            assert a['entry_uvz_mm'] == ref['cam_access_uvz_mm']
            assert a['nominal_body_bbox_mm'] == ref['blind_bore_bbox_mm']
    pair_count = 0
    for a, b in itertools.combinations(d['fastener_axes'], 2):
        assert intersect_volume(a['nominal_body_bbox_mm'], b['nominal_body_bbox_mm']) < 1e-8
        pair_count += 1
    assert pair_count == d['nominal_body_pair_checks']
    max_error = 0.
    for cut in d['cuts']:
        members = cut['members']
        expected_boundary = {r['id'] for r in groups.values() if sum(n in members for n in [r['a'], r['b']]) == 1}
        assert set(cut['boundary_groups']) == expected_boundary
        points = np.array([p for gid in expected_boundary for p in groups[gid]['interface_points_uvz_mm']])
        # Tres pontos nao colineares permitem fechar seis resultantes
        # no modelo de forcas3D livres, sem demonstracao fisica.
        assert np.linalg.matrix_rank(points-points[0], tol=1e-7) >= 2
        assert cut['connector_force_distribution'] is None
        mass, first_u, first_v = 0., 0., 0.
        for n in members:
            b = np.array(boxes[n]);dm = np.prod(b[3:]-b[:3])*cut['rho_kg_m3']/1e9*61/60
            mass += dm;first_u += dm*(b[0]+b[3])/2;first_v += dm*(b[1]+b[4])/2
        width = boxes[meta['right']][0]
        kind = cut['payload_case']; payload = cut['payload_kg']
        payload_u = {'20_near_u0': .05*width, '20_near_uL': .95*width,
                     '10_near_u0': .05*width, '10_near_uL': .95*width}.get(kind, width/2)
        payload_v = 305 if ('front' in kind or 'near_' in kind) else 174
        mass += payload;first_u += payload*payload_u;first_v += payload*payload_v
        expected_wrench = np.array([0, 0, mass*9.80665, first_v*9.80665, -first_u*9.80665, 0])
        saved = np.r_[cut['required_force_N'], cut['required_moment_origin_Nmm']]
        error = float(np.max(np.abs(expected_wrench-saved)));max_error = max(error, max_error)
        assert error < 1e-7
        assert meta['back'] not in members and meta['top'] not in members
    assert len(d['cuts']) == 30
    if code == 'P17':
        assert d['plate_compatibility']['matched_positions'] == 24
        assert not d['plate_compatibility']['physical_stiffness_match']
        old = read(ROOT/'04_Moveis/P17/Base_fundo_ligacoes/Conferencia_geometrica.json')
        prior = read(OUT/'Geometria_R51.json')['modules']['P17']['canonical_origin']
        for marker in old['nominal_axes']:
            if marker['interface'] not in ['lateral/fundo', 'divisoria/fundo']:
                continue
            u, y, z = marker['module_xyz_mm']
            converted = [u-prior['u0_module_mm'], prior['rear_module_mm']-y, z]
            # Marcador antigo de fundo/divisor fica no meio do fundo(v9),
            # enquanto a interface fisica atual esta na facev18. Mesmo eixoY.
            dims = [0, 2] if marker['interface'] == 'divisoria/fundo' else [1, 2]
            assert any(np.linalg.norm(np.array(converted)[dims]-np.array(a['interface_uvz_mm'])[dims]) < 1e-6
                       and a['family'] == 'Confirmat' for a in d['fastener_axes'])
    for suffix, rows in [('mapa_juntas', d['groups']), ('eixos_fixadores', d['fastener_axes']), ('cortes_carga', d['cuts'])]:
        with (OUT/f'{code}_{suffix}.csv').open(encoding='utf-8-sig', newline='') as f:
            saved = list(csv.DictReader(f, delimiter=';'))
        assert len(saved) == len(rows)
        for a, b in zip(saved, rows):
            for k, v in b.items():
                expected_value = json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else '' if v is None else str(v)
                assert a[k] == expected_value, (suffix, k)
    report = dict(code=code, status='OK_MAPA_NOMINAL', groups=len(groups), axes=len(d['fastener_axes']),
        cuts=len(d['cuts']), body_pair_checks=pair_count, max_wrench_error_N_or_Nmm=max_error,
        physical_tests_executed=0, capacity_demonstrated=False, cad_preserved=True,
        sources_sha256={f'{code}_caminho_caixa.json': sha(OUT/f'{code}_caminho_caixa.json')},
        verifier_sha256=sha(Path(__file__)), hash_rule=HASH_RULE)
    (OUT/f'{code}_verificacao_caminho.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser();parser.add_argument('--movel', choices=['P17', 'P12'], required=True)
    main(parser.parse_args().movel)
