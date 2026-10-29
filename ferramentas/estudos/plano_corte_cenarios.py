"""Extensão de cenários do motor vigente; somente CSV/JSON persistidos, sem CAD."""
from pathlib import Path
from collections import defaultdict
import argparse
import copy
import csv
import hashlib
import json
import math
from xml.sax.saxutils import escape
import corte_guilhotina as motor

ROOT = motor.ROOT
AREA = ROOT / '04_Moveis/Plano_de_corte'
SCENARIOS = [('refilo10_serra4', 10, 4), ('refilo0_serra3', 0, 3), ('refilo20_serra4', 20, 4)]


def csv_write(path, rows):
    with path.open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter=';')
        w.writeheader(); w.writerows(rows)


def reconcile_mass(panels, rows):
    """Não dividir volume total de móvel por uma espessura: ele pode misturar chapas."""
    volumes = defaultdict(float)
    for p in panels:
        volumes[p['module']] += p['w'] * p['h'] * p['thickness_mm'] / 1e9
    assert len(panels) == len({p['id'] for p in panels}) == 249
    for r in rows:
        assert abs(volumes[r['movel']] - float(r['volume_envelope_m3'])) <= 5.1e-9, r['movel']
    return volumes


def alternatives(base, persisted):
    byid = {p['id']: p for p in base}
    groups = defaultdict(list)
    proposal_rows = []
    for row in persisted['rows']:
        t, h, w = row['new_sorted_nominal_dims_mm']
        original = byid.get(row['source_object']) if row['role']=='replacement' else None
        p = copy.deepcopy(original) if original else dict(module=row['kit'].split('_')[0], pattern='Indefinido', directional=True, packing_blockers=['Produto das peças acrescentadas não individualizado; sem chapa comercial presumida'])
        p.update(id=row['study_object'], C_mm=w, L_mm=h, w=w, h=h, thickness_mm=t, envelope_area_m2=w*h/1e6)
        assert abs(w*h/1e6-row['proposed_fabrication_face_area_m2']) < 1e-7
        groups[row['kit']].append((row, p))
        proposal_rows.append((row['kit'], p, row['role'], row['source_object'] or '', 'Material da substituta herdado apenas como hipótese' if original else 'Material ausente; não adotar Branco TX automaticamente'))
    assert len(proposal_rows) == 36 and len(groups) == 7
    variants = {}
    for kit, members in groups.items():
        retired = {r['source_object'] for r, p in members if r['role']=='replacement' and r['source_object']}
        variants[kit] = [copy.deepcopy(p) for p in base if p['id'] not in retired] + [p for r,p in members]
    return variants, proposal_rows


def solve(panels, variant, scenario, trim, kerf):
    old = motor.TRIM, motor.KERF
    motor.TRIM, motor.KERF = trim, kerf
    summaries, details = [], []
    try:
        groups = defaultdict(list)
        for p in panels:
            if not p['packing_blockers']: groups[p['pattern'], p['thickness_mm']].append(p)
        W, H = 2750-2*trim, 1850-2*trim
        for (pattern, thickness), ps in sorted(groups.items()):
            plan = motor.optimize(ps, W, H)
            motor.validate(plan, ps, W, H)
            fitted = [p for p in ps if p['id'] not in plan['oversized']]
            area = sum(p['w']*p['h'] for p in fitted)/1e6
            full_area = sum(p['w']*p['h'] for p in ps)/1e6
            n = len(plan['sheets']); useful = n*W*H/1e6; gross = n*2750*1850/1e6
            free = [r for s in plan['sheets'] for r in s['free']]
            free_area = sum(r[2]*r[3] for r in free)/1e6
            reusable = [r for r in free if r[2]>300 and r[3]>300]
            reuse_area = sum(r[2]*r[3] for r in reusable)/1e6
            saw = useful-area-free_area
            assert saw >= -1e-8
            assert abs(gross-(area+free_area+saw+gross-useful)) < 1e-8
            lower = math.ceil(area/(W*H/1e6))
            row = dict(variante=variant, cenario=scenario, formato_mm='2750x1850', refilo_mm=trim, serra_mm=kerf,
                padrao=pattern, espessura_mm=thickness, paineis_grupo=len(ps), paineis_cortaveis=len(fitted),
                nao_cabem=' | '.join(plan['oversized']), grupo_completo_viavel=not plan['oversized'],
                chapas_subconjunto=n, limite_inferior_subconjunto=lower, lacuna=n-lower,
                limite_area_grupo_inteiro=math.ceil(full_area/(W*H/1e6)), area_grupo_inteiro_m2=round(full_area,8),
                area_paineis_cortaveis_m2=round(area,8), area_comprada_subconjunto_m2=round(gross,8),
                aproveitamento_util_pct=round(100*area/useful,4) if useful else 0,
                area_refilo_m2=round(gross-useful,8), area_serra_m2=round(saw,8),
                sobras_uteis_qtd=len(reusable), sobras_uteis_m2=round(reuse_area,8),
                sobras_menores_m2=round(free_area-reuse_area,8),
                perda_sem_sobras_uteis_m2=round(gross-area-reuse_area,8),
                escopo='subconjunto sem oversize; integral impossível' if plan['oversized'] else 'grupo materialmente classificável; nominal')
            summaries.append(row); details.append(dict(resumo=row, plano=plan))
        return summaries, details
    finally:
        motor.TRIM, motor.KERF = old


def list_row(variant, p, role='', replaces='', note='', tape=None):
    # Bordas são fonte da base; substituição/espessura diferente não herda metragem antiga.
    tape = tape if variant=='base' and tape is not None else {}
    return dict(variante=variant, movel=p['module'], id=p['id'], quantidade=1, substitui=replaces, papel=role,
        comprimento_mm=p['w'], largura_mm=p['h'], espessura_mm=p['thickness_mm'], padrao=p['pattern'],
        C_ficha_mm=p.get('C_mm',p['w']), L_ficha_mm=p.get('L_mm',p['h']),
        especificacao_ficha=p.get('specification',''),
        C0=tape.get('C0',''), C1=tape.get('C1',''), L0=tape.get('L0',''), L1=tape.get('L1',''),
        espessura_fita_mm=tape.get('espessura_fita_mm',''), metros_fita_definidos=tape.get('metros_fita_definidos',''),
        metros_fita_propostos=tape.get('metros_propostos_retos',''), metros_fita_com_perda=tape.get('metros_propostos_com_perda',''),
        situacao_fita=tape.get('situacao','pendente; variante não herda bordas nem metragem'), detalhe_fita=tape.get('detalhe',''),
        area_envelope_m2=round(p['w']*p['h']/1e6,8), volume_envelope_m3=round(p['w']*p['h']*p['thickness_mm']/1e9,10),
        rotacao_permitida=not p['directional'], bloqueios=' | '.join(p['packing_blockers']),
        cabe_sem_refilo=any(w<=2750 and h<=1850 for w,h,_ in motor.orientations(p)),
        cabe_refilo10=any(w<=2730 and h<=1830 for w,h,_ in motor.orientations(p)),
        cabe_refilo20=any(w<=2710 and h<=1810 for w,h,_ in motor.orientations(p)), hipotese=note)


def write_svg(path, sheet, title):
    body=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2750 1950">', '<rect width="2750" height="1850" fill="white" stroke="black"/>']
    for p in sheet['placements']:
        body.append(f'<rect x="{p["x"]}" y="{p["y"]}" width="{p["w"]}" height="{p["h"]}" fill="#dae8df" stroke="#345"/><text x="{p["x"]+4}" y="{p["y"]+18}" font-size="15">{escape(p["id"])}</text>')
    for x,y,w,h in sheet['free']:
        if w>300 and h>300: body.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#fff0c0" stroke="#987"/>')
    body.append(f'<text x="20" y="1900" font-size="20">{escape(title)} — hipótese, não fabricação</text></svg>')
    path.write_text(''.join(body),encoding='utf-8')


def main(out):
    out = out.resolve()
    if out.is_relative_to(ROOT): raise ValueError('Desenhos/detalhes devem ficar fora do Git')
    AREA.mkdir(exist_ok=True); out.mkdir(parents=True,exist_ok=True)
    source_paths = [*sorted((ROOT/'06_Entregas/Fichas_fabricacao').glob('P??-pecas.csv')),
        ROOT/'04_Moveis/Acabamentos_por_peca.csv', ROOT/'04_Moveis/Furacao/Fita_por_peca.csv', ROOT/'04_Moveis/Quantitativos/Diferencas_nominais.json',
        ROOT/'04_Moveis/Quantitativos/Massas_por_movel.csv', motor.AREA/'analisar.py', motor.AREA/'Parametros.json', Path(motor.__file__),Path(__file__)]
    hashes = {p.relative_to(ROOT).as_posix():motor.sha(p) for p in source_paths}
    base = motor.load_panels()
    with (ROOT/'04_Moveis/Quantitativos/Massas_por_movel.csv').open(encoding='utf-8-sig') as f:
        volumes = reconcile_mass(base,list(csv.DictReader(f,delimiter=';')))
    persisted = json.loads((ROOT/'04_Moveis/Quantitativos/Diferencas_nominais.json').read_text(encoding='utf-8'))
    proposals, proposed = alternatives(base,persisted)
    sens = copy.deepcopy(base)
    piece = next(p for p in sens if p['id']=='Peca245')
    assert piece['thickness_mm']==18
    piece['thickness_mm']=15
    variants = {'base':base,'sensibilidade_Peca245_18_para15':sens,**proposals}
    with (ROOT/'04_Moveis/Furacao/Fita_por_peca.csv').open(encoding='utf-8-sig') as f:
        tape_rows=list(csv.DictReader(f,delimiter=';'))
    tapes={r['peca']:r for r in tape_rows}
    assert len(tapes)==len(tape_rows)==249 and set(tapes)=={p['id'] for p in base}
    rows=[list_row('base',p,tape=tapes[p['id']]) for p in base]+[list_row(kit,p,role,replaces,note) for kit,p,role,replaces,note in proposed]
    rows.append(list_row('sensibilidade_Peca245_18_para15',piece,'hipotese','Peca245','Somente agrupamento de corte; C/L constantes; não verifica rigidez, furação ou ligações'))
    summaries, details = [], []
    for variant, ps in variants.items():
        for scenario,trim,kerf in SCENARIOS:
            summary, detail=solve(ps,variant,scenario,trim,kerf)
            summaries.extend(summary);details.extend(detail)
    csv_write(AREA/'Lista_de_corte.csv',rows)
    csv_write(AREA/'Resumo_chapas.csv',summaries)
    for i,d in enumerate(details,1):
        for si,sheet in enumerate(d['plano']['sheets'],1):
            r=d['resumo'];write_svg(out/f'G{i:03d}_chapa{si:02d}.svg',sheet,f'{r["variante"]} / {r["cenario"]} / {r["padrao"]} {r["espessura_mm"]} mm')
    areas_by_module_thickness=defaultdict(float)
    for p in base:
        areas_by_module_thickness[p['module'],p['thickness_mm']]+=p['w']*p['h']/1e6
    reconciliation=[dict(movel=m,espessura_mm=t,area_envelope_m2=a,volume_m3=a*t/1000) for (m,t),a in sorted(areas_by_module_thickness.items())]
    data=dict(source_sha256=hashes,volumes_conferidos_m3=volumes,areas_por_movel_espessura=reconciliation,
        variants={k:dict(total=len(v),sem_bloqueio_material=sum(not p['packing_blockers'] for p in v),bloqueados=[p['id'] for p in v if p['packing_blockers']]) for k,v in variants.items()},plans=details)
    (out/'Planos.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    manifest={p.name:motor.sha(p) for p in sorted(out.glob('G*_chapa*.svg'))}
    (out/'Hashes_desenhos.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    assert all(motor.sha(ROOT/p)==h for p,h in hashes.items())
    print(json.dumps(dict(variantes=data['variants'],resumos=len(summaries),planos_sha256=motor.sha(out/'Planos.json'),manifesto_sha256=motor.sha(out/'Hashes_desenhos.json'),desenhos=len(manifest)),ensure_ascii=False,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--saida',type=Path,default=ROOT.parent/'outputs/Plano_de_corte')
    main(parser.parse_args().saida)
