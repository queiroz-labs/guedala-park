"""Caminhos e cortes P17/P12 a partir de fontes salvas; sem abrir CAD.

As resultantes de corte sao demandas do grupo inteiro. Nao se resolve a
partilha hiperestatica nem se atribui resistencia/rigidez aos conectores.
"""
from pathlib import Path
import argparse, csv, itertools, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from fontes import sha, HASH_RULE

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / '04_Moveis/Aereos_suspensao'
META = {
    'P17': dict(base='Peca387', top='Peca388', back='Peca386', left='Peca385', right='Peca384'),
    'P12': dict(base='Peca345', top='Peca346', back='Peca344', left='Peca343', right='Peca342'),
}
G = 9.80665


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def write_csv(path, rows):
    with path.open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter=';')
        writer.writeheader()
        for row in rows:
            writer.writerow({k: json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v for k, v in row.items()})


def overlap(a, b):
    return all(min(a[i+3], b[i+3]) - max(a[i], b[i]) > 1e-7 for i in range(3))


def segment_box(a, b, radius):
    a, b = np.array(a, float), np.array(b, float)
    lo, hi = np.minimum(a, b), np.maximum(a, b)
    for i in range(3):
        if abs(a[i]-b[i]) < 1e-8:
            lo[i] -= radius
            hi[i] += radius
    return np.r_[lo, hi].tolist()


def rank_of_points(points):
    """Postos apenas cinematicos: tres componentes livres por ponto ideal."""
    p = np.array(points, float)
    center = p.mean(0)
    scale = max(float(np.max(np.linalg.norm(p-center, axis=1))), 1.)
    blocks = []
    for x, y, z in (p-center)/scale:
        cross = np.array([[0, -z, y], [z, 0, -x], [-y, x, 0]])
        blocks.append(np.vstack([np.eye(3), cross]))
    return int(np.linalg.matrix_rank(np.hstack(blocks), tol=1e-9))


def main(code):
    geo = read(OUT/'Lote_B_geometria.json')
    detail = read(OUT/'Lote_B_detalhamento.json')
    susp = read(OUT/f'{code}_suspensao.json')
    release = read(ROOT/'ferramentas/site/current_release.json')
    assert sha(ROOT/release['cadPath']) == geo['cad_sha256'] == susp['cad_sha256']
    mod = next(m for m in geo['modules'] if m['code'] == code)
    variant = next(v for v in mod['variants'] if v['preferred_for_study'])
    boxes = variant['boxes_uvz_mm']
    meta = META[code]
    divs = [n for n in boxes if n not in meta.values()]
    h, w = mod['height_mm'], mod['width_internal_mm']
    mounts = {f'suporte_{m["side"]}': m['envelope_uvz_mm'] for m in susp['mounts']}
    obstacles = {**boxes, **{r['name']: r['box_uvz_mm'] for r in susp['static_calcos']}, **mounts}
    groups, axes = [], []
    historical = [r for r in geo['historical_map'] if r['code'] == code]

    def add_group(a, b, family, points, qty, source, force_path, placement='NOMINAL'):
        lo = np.maximum(boxes[a][:3], boxes[b][:3])
        hi = np.minimum(boxes[a][3:], boxes[b][3:])
        spans = hi-lo
        assert min(spans) >= -1e-6 and sum(spans > 1e-6) == 2
        gid = f'{code}_J{len(groups)+1:02}'
        groups.append(dict(id=gid, a=a, b=b, family=family, candidate_count=qty,
            contact_area_mm2=float(np.prod(spans[spans > 1e-6])),
            interface_points_uvz_mm=points, ideal_point_force_rank=rank_of_points(points) if points else None,
            position_status=placement, source=source, load_path=force_path,
            capacity_demonstrated=False, stiffness_demonstrated=False,
            qualification='Painel real, junta completa, retencao e curva forca/deslocamento; a contagem nao reparte forcas.'))
        return gid

    for r in historical:
        a, b = r['a'], r['b']
        if r['family'].startswith('Minifix'):
            js = [j for j in detail['joints'] if j['code'] == code and {j['a'], j['b']} == {a, b}]
            assert len(js) == r['old_connector_qty']
            vertical = a if a not in [meta['base'], meta['top']] else b
            horizontal = b if b in [meta['base'], meta['top']] else a
            is_side = vertical in [meta['left'], meta['right']]
            mode = 'Cortante vertical no pino horizontal, retencao transversal e rotacao da junta.' if is_side else 'Tracao/retencao axial do pino vertical no caminho de suspensao da base; compressao por contato conforme o sinal.'
            gid = add_group(a, b, 'Minifix15 + pino B34 candidatos', [j['interface_uvz_mm'] for j in js], len(js), 'R00 reconciliado com Lote_B_detalhamento.json', mode)
            for j in js:
                hits = [n for n, box in obstacles.items() if overlap(j['tool_corridor_bbox_mm'], box)]
                bore_hits = [n for n, box in mounts.items() if overlap(j['blind_bore_bbox_mm'], box)]
                assert not hits and not bore_hits
                axes.append(dict(group=gid, id=j['id'], family='Minifix', interface_uvz_mm=j['interface_uvz_mm'],
                    entry_uvz_mm=j['cam_access_uvz_mm'], tip_uvz_mm=None,
                    access_bbox_mm=j['tool_corridor_bbox_mm'], nominal_body_bbox_mm=j['blind_bore_bbox_mm'],
                    access_hits=hits, other_body_hits=bore_hits, source='Caneco/furo cego e corredor herdados do lote B',
                    access_stage='Antes das portas; canecos nas faces internas livres; calcos fixos incluidos.',
                    actual_tool_verified=False, actual_head_pilot_torque_selected=False))
        elif r['family'].startswith('Confirmat'):
            side = next((n for n in [a, b] if n in [meta['left'], meta['right']]), None)
            vertical = next(n for n in [a, b] if n != meta['back'])
            # P17 herda marcadores salvos; P12 recebe proposta simetrica de
            # estacoes, sem inferir capacidade, distancia minima ou piloto.
            zlist = [70., h/2, h-70] if side else [88., h/2, h-88]
            u = (boxes[vertical][0]+boxes[vertical][3])/2
            points = [[0 if side == meta['left'] else w, 9., z] if side else [u, 18., z] for z in zlist]
            source = 'P17: eixos laterais70/275/480 e divisores88/275/462 do estudo salvo' if code == 'P17' else 'P12: proposta geometrica26/10; laterais70/292/514 e divisor88/292/496, ainda sem gabarito de produto'
            gid = add_group(a, b, 'Confirmat7x50 candidato', points, r['old_connector_qty'], source,
                'Fundo troca cortante vertical e esforcos fora do plano com a caixa. Coluna de pontos nao fecha sozinha torcao em z.')
            for i, (u0, v0, z) in enumerate(points):
                if side:
                    sign = 1 if side == meta['left'] else -1
                    entry = [u0-sign*18, 9., z]
                    tip = [entry[0]+sign*50, 9., z]
                    outside = [entry[0]-sign*100, 9., z]
                else:
                    entry, tip, outside = [u0, 0., z], [u0, 50., z], [u0, -100., z]
                body = segment_box(entry, tip, 3.5)
                corridor = segment_box(outside, entry, 10.)
                # A cabeca/corpo real nao esta contido no eixo7 hipotetico.
                hits = [n for n, bx in obstacles.items() if overlap(corridor, bx)]
                body_hits = [n for n, bx in obstacles.items() if n not in [a, b] and overlap(body, bx)]
                assert not hits and not body_hits, (code, gid, hits, body_hits)
                axes.append(dict(group=gid, id=f'{gid}_{i+1}', family='Confirmat', interface_uvz_mm=[u0, v0, z],
                    entry_uvz_mm=entry, tip_uvz_mm=tip, access_bbox_mm=corridor, nominal_body_bbox_mm=body,
                    access_hits=hits, other_body_hits=body_hits, source=source,
                    access_stage='Bancada antes da instalacao; lateral externa' if side else 'Bancada antes da instalacao; traseira externa',
                    actual_tool_verified=False, actual_head_pilot_torque_selected=False))
        else:
            assert code == 'P17' and r['old_connector_qty'] == 4
            left, right = sorted([a, b], key=lambda n: boxes[n][0])
            face = boxes[left][3]
            points = [[face, v, z] for v in [120., 240.] for z in [150., 400.]]
            gid = add_group(a, b, 'Parafuso4x30 face a face candidato', points, 4,
                'R00: quantidade4; proposta26/10 de centros v120/240,z150/400, entrada pela face livre esquerdau964',
                'Amarracao dos divisores pareados; sem credito de composicao36mm ou capacidade.')
            for i, point in enumerate(points):
                entry = [boxes[left][0], point[1], point[2]]
                tip = [entry[0]+30., point[1], point[2]]
                corridor = segment_box([entry[0]-100., *entry[1:]], entry, 10.)
                body = segment_box(entry, tip, 2.)
                hits = [n for n, bx in obstacles.items() if overlap(corridor, bx)]
                other = [n for n, bx in obstacles.items() if n not in [a, b] and overlap(body, bx)]
                assert not hits and not other and abs(boxes[right][3]-tip[0]-6.) < 1e-6
                axes.append(dict(group=gid, id=f'{gid}_{i+1}', family='Face4x30', interface_uvz_mm=point,
                    entry_uvz_mm=entry, tip_uvz_mm=tip, access_bbox_mm=corridor, nominal_body_bbox_mm=body,
                    access_hits=hits, other_body_hits=other, source='Proposta26/10 de quatro centros;12mm nominais na segunda chapa,6mm ate a face oposta',
                    access_stage='Face livre esquerda do par central,antes das portas;cabeca/piloto/torque pendentes.',
                    actual_tool_verified=False, actual_head_pilot_torque_selected=False))

    for horizontal in [meta['base'], meta['top']]:
        rs = [r for r in detail['rear_joints'] if r['code'] == code and r['b'] == horizontal]
        if not rs:
            continue
        gid = add_group(meta['back'], horizontal, 'Confirmat7x50 candidato', [r['interface_uvz_mm'] for r in rs], len(rs),
            '24 posicoes adicionais de estudo ja reconciliadas no lote B',
            'Base transmite cortante vertical ao fundo; fundo deve levar a resultante aos cantos e/ou tampo. Sem apoio superior rigido presumido.')
        for i, r in enumerate(rs):
            entry, tip = r['rear_entry_uvz_mm'], r['nominal_tip_uvz_mm']
            corridor = segment_box([entry[0], -100., entry[2]], entry, 10.)
            body = segment_box(entry, tip, 3.5)
            hits = [n for n, bx in obstacles.items() if overlap(corridor, bx)]
            other = [n for n, bx in obstacles.items() if n not in [meta['back'], horizontal] and overlap(body, bx)]
            assert not hits and not other
            axes.append(dict(group=gid, id=f'{gid}_{i+1}', family='Confirmat', interface_uvz_mm=r['interface_uvz_mm'],
                entry_uvz_mm=entry, tip_uvz_mm=tip, access_bbox_mm=corridor, nominal_body_bbox_mm=body,
                access_hits=hits, other_body_hits=other, source='Lote_B_detalhamento.json:rear_joints',
                access_stage='Bancada antes da instalacao; traseira externa', actual_tool_verified=False,
                actual_head_pilot_torque_selected=False))

    # Cortes fechados: demandas que o conjunto de juntas de fronteira tem
    # de transmitir. Nao existe partilha por conector sem compatibilidade.
    cases = {(c['rho_kg_m3'], c['payload_kg'], c['payload_case']): c for c in detail['cases'] if c['code'] == code}
    cuts = []
    cut_defs = [('base', [meta['base']]), ('base_e_divisorias', [meta['base'], *divs])]
    for cut_name, members in cut_defs:
        boundary = [r for r in groups if (r['a'] in members) != (r['b'] in members)]
        points = [p for r in boundary for p in r['interface_points_uvz_mm']]
        assert rank_of_points(points) == 6
        for key, c in sorted(cases.items()):
            rho, payload, kind = key
            u = .05*w if 'near_u0' in kind else .95*w if 'near_uL' in kind else w/2
            v = 305. if 'front' in kind or 'near_' in kind else 174.
            items = []
            for name in members:
                box = np.array(boxes[name]);mass = np.prod(box[3:]-box[:3])*rho/1e9*18.3/18
                items.append(dict(part=name, mass_kg=float(mass), center_uvz_mm=((box[:3]+box[3:])/2).tolist()))
            items.append(dict(part='conteudo', mass_kg=payload, center_uvz_mm=[u, v, 0.]))
            force = np.array([0., 0., -sum(r['mass_kg'] for r in items)*G])
            moment = sum((np.cross(r['center_uvz_mm'], [0., 0., -r['mass_kg']*G]) for r in items), np.zeros(3))
            cuts.append(dict(cut=cut_name, rho_kg_m3=rho, payload_kg=payload, payload_case=kind,
                members=members, load_items=items, boundary_groups=[r['id'] for r in boundary],
                ideal_boundary_rank=6, required_force_N=(-force).tolist(), required_moment_origin_Nmm=(-moment).tolist(),
                connector_force_distribution=None, scope='Resultante sobre toda a fronteira; portas/fundo/tampo fora deste corte. Nao somar ao caso global que ja contem estas massas.'))

    compat = None
    if code == 'P17':
        plate = read(ROOT/'04_Moveis/P17/Base_fundo_ligacoes/Resultados.json')
        sample = next(c for c in plate['cases'] if c['mode'] == 'full')
        reference = [[round(x, 6), round(330-y, 6)] for x, y in sample['points_xy_mm']]
        base_points = []
        for gr in groups:
            if meta['base'] in [gr['a'], gr['b']]:
                base_points.extend([[round(p[0], 6), round(p[1], 6)] for p in gr['interface_points_uvz_mm']])
        assert sorted(reference) == sorted(base_points)
        compat = dict(coordinate_transform='u=x;v=330-y; y antigo mede da frente da base, v atual da traseira da caixa',
            matched_positions=len(reference), geometric_match=True, physical_stiffness_match=False,
            reason='As mesmas24 posicoes verticais nao validam K500/250 para Minifix; juntas antigas eram requisitos abstratos. Reserva superior0.20mm continua sem prova.')

    pair_hits = [[a['id'], b['id']] for a, b in itertools.combinations(axes, 2)
                 if overlap(a['nominal_body_bbox_mm'], b['nominal_body_bbox_mm'])]
    assert not pair_hits, pair_hits
    totals = {f: sum(g['candidate_count'] for g in groups if g['family'] == f) for f in sorted(set(g['family'] for g in groups))}
    limits = [
        'Geometria nominal de caixas persistidas; nenhum CAD aberto ou alterado. Sem furos, tolerancias e corpos reais completos.',
        'Pontos e grafos descrevem conectividade, nao demonstram resistencia, rigidez ou estabilidade do conjunto.',
        'Posto6 de uma fronteira e condicao algebrica necessaria do modelo de forcas livres; nao prova capacidade das juntas reais.',
        'Par de Minifix colinear tem posto5: momento em torno da linha exige face de contato/rigidez ou outros caminhos. Tres Confirmat em coluna nao reagem sozinhos ao momento emz.',
        'Corredores Confirmat20x100 sao reservas externas de bancada; nao incluem mao, cabeca, bit, mandril ou paredes. SKU/piloto/escareamento/torque pendentes.',
        'Confirmat7x50 deixa32mm nominais alem da primeira chapa18; cilindro7 nao e especificacao de piloto. Cabecas laterais aparentes e traseiras junto a parede requerem detalhe.',
        'Bigfer permanece candidata; ferramenta auxiliar12 e demais acessos herdados nao comprovam a montagem real.',
        'P17: quatro4x30 com centros candidatos;cabeca/piloto/torque pendentes,12mm nominais na segunda chapa e6mm restantes. Sem composicao36mm. Cavilhas sem credito de resistencia e sem novo mapa.',
        'P12: base e tampo tocam o fundo apenas por aresta; nao ha ligacao traseira direta creditada.',
        'Sem carga de prova, protocolo de laboratorio, ensaio fisico ou capacidade de uso demonstrada.',
    ]
    paths = [OUT/n for n in ['Lote_B_geometria.json', 'Lote_B_detalhamento.json', f'{code}_suspensao.json', 'Lote_B_fontes_Minifix.json']]
    if code == 'P17':
        paths += [ROOT/'04_Moveis/P17/Base_fundo_ligacoes/Resultados.json', ROOT/'04_Moveis/P17/Base_fundo_ligacoes/Conferencia_geometrica.json']
    result = dict(code=code, status='MAPA_NOMINAL_E_CORTES_SEM_CAPACIDADE', cad_sha256=geo['cad_sha256'],
        cad_opened=False, cad_changed=False, physical_tests_executed=0, variant=variant['variant'],
        boxes_uvz_mm=boxes, pieces=meta, dividers=divs, groups=groups, fastener_axes=axes,
        candidate_totals=totals, cuts=cuts, plate_compatibility=compat, limits=limits,
        nominal_body_pair_checks=len(axes)*(len(axes)-1)//2, nominal_body_pair_interferences=pair_hits,
        assembly=['Em bancada apoiada: inserir divisorias na base pelos pinos verticais; acesso pelas faces livres.',
            'Aproximar tampo emz sobre divisorias; fechar juntas verticais sem presumir translacao simultanea com laterais.',
            'Aproximar cada lateral emu, encaixando seus quatro pinos horizontais; conferir apertos internos.',
            'Posicionar fundo pela traseira; executar/apertar juntas traseiras e laterais com acesso externo. Validar sequencia com ferragens reais.',
            'Conferir esquadro, diagonais, abertura das juntas e acesso dos suspensores antes das portas.',
            'Montagem Bigfer com caixa sustentada e aperto pela frente depende de produto/fixadores; a instalacao exige parede conhecida.'],
        hash_rule=HASH_RULE, sources_sha256={p.relative_to(ROOT).as_posix(): sha(p) for p in paths},
        script_sha256=sha(Path(__file__)), hash_helper_sha256=sha(Path(__file__).with_name('fontes.py')))
    (OUT/f'{code}_caminho_caixa.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    write_csv(OUT/f'{code}_mapa_juntas.csv', groups)
    write_csv(OUT/f'{code}_eixos_fixadores.csv', axes)
    write_csv(OUT/f'{code}_cortes_carga.csv', cuts)
    draw(result)
    print(json.dumps(dict(code=code, groups=len(groups), axes=len(axes), cuts=len(cuts), totals=totals, plate=compat), ensure_ascii=False))


def draw(d):
    im = Image.new('RGB', (1500, 940), '#f6f3ed'); q = ImageDraw.Draw(im)
    def text(x, y, s, size=23, bold=False, color='#263d35'):
        font = ImageFont.truetype('C:/Windows/Fonts/'+('arialbd.ttf' if bold else 'arial.ttf'), size)
        q.text((x, y), s, font=font, fill=color)
    def arrow(a, b, color):
        q.line([a, b], fill=color, width=5)
        v = np.array(b, float)-a; v /= np.linalg.norm(v); n = np.array([-v[1], v[0]])
        q.polygon([tuple(b), tuple(np.array(b)-15*v+7*n), tuple(np.array(b)-15*v-7*n)], fill=color)
    text(45, 24, d['code']+' | caminhos da carga e juntas da caixa', 36, True)
    text(45, 78, 'Estudo nominal · 26/10/2026 · caixas, conectores e suspensão ainda precisam de comprovação', 23)
    boxes = d['boxes_uvz_mm'];meta = d['pieces']; h = boxes[meta['left']][5];w = boxes[meta['right']][0]
    sx = min(1300/(w+36), 470/h); x0 = (1500-w*sx)/2; z0 = 625
    def px(u): return x0+u*sx
    def pz(z): return z0-z*sx
    for name, b in boxes.items():
        fill = '#dfe9e2' if name == meta['back'] else '#a9b6a8'
        if name == meta['back']:
            q.rectangle((px(b[0]), pz(b[5]), px(b[3]), pz(b[2])), fill=fill)
    for name, b in boxes.items():
        if name != meta['back']:
            q.rectangle((px(b[0]), pz(b[5]), px(b[3]), pz(b[2])), fill='#b8ab96', outline='#665c4a', width=2)
    for name in [meta['left'], *d['dividers'], meta['right']]:
        b = boxes[name];u = (b[0]+b[3])/2
        arrow((px(u), pz(70)), (px(u), pz(h-85)), '#326c58')
    for a in d['fastener_axes']:
        u,v,z = a['interface_uvz_mm']; r = 5 if a['family']=='Minifix' else 4
        q.ellipse((px(u)-r,pz(z)-r,px(u)+r,pz(z)+r), fill='#b36b29' if a['family']=='Minifix' else '#4a6c95')
    for u in [40.5,w-40.5]:
        q.rectangle((px(u)-10,pz(h-36)-10,px(u)+10,pz(h-36)+10),fill='#a4483f')
    text(45, 116, 'Vista frontal esquemática. Pontos em profundidades diferentes se sobrepõem nesta vista.', 21)
    text(45, 662, 'Laranja: Minifix internos   •   Azul: parafusos candidatos   •   Vermelho: suspensão candidata', 23, True)
    text(45, 708, 'Base → laterais/divisórias → tampo e fundo → cantos da suspensão.', 25, True)
    text(45, 751, 'P17: o fundo inteiro também recebe a base diretamente por 12 ligações.' if d['code']=='P17' else 'P12: o fundo recebe carga pelas laterais/divisória; não há ligação direta à base.', 23)
    text(45, 798, 'Setas indicam caminhos possíveis; a divisão das forças depende da rigidez real das juntas.', 23)
    text(45, 841, 'Cortes CSV: resultantes por conjunto de juntas. Não dividir pelo número de parafusos.', 23)
    text(45, 886, 'Fixadores traseiros/laterais exigem acesso na bancada. Imagem não serve como gabarito de furação.', 21)
    im.save(OUT/f'{d["code"]}_caminho_caixa.png')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--movel', required=True, choices=META)
    main(parser.parse_args().movel)
