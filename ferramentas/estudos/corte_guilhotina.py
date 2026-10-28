"""Envelopes nominais para cotação; guilhotina, veio conservador e refilo.

Não é programa de seccionadora nem demonstra ótimo global. Nenhum CAD é aberto.
Dados de posicionamento/SVG são escritos somente no diretório externo solicitado.
"""
from pathlib import Path
import argparse, csv, hashlib, importlib.util, json, math, random
from collections import defaultdict
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[2]
AREA = ROOT / '04_Moveis/Proximas_decisoes/Corte_e_formatos'
PARAMS = json.loads((AREA / 'Parametros.json').read_text(encoding='utf-8'))
KERF, TRIM = PARAMS['kerf_mm'], PARAMS['trim_per_edge_mm']


def load_panels():
    spec = importlib.util.spec_from_file_location('base_corte', AREA / 'analisar.py')
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    panels = mod.load_base()
    with (ROOT / '04_Moveis/Acabamentos_por_peca.csv').open(encoding='utf-8-sig') as f:
        audit = {r['id']: r for r in csv.DictReader(f, delimiter=';')}
    for p in panels:
        a = audit[p['id']]
        assert a['face_1'] == a['face_2'], p['id']
        if p['id'] == 'Peca350':
            assert 'Arenza liso' in p['specification'] and p['thickness_mm'] == 18
            assert 'Escolha das duas faces encerrada' in p['partial_finish']
            # F13=A encerra a escolha de acabamento, não SKU/processo/bordas.
            p['packing_blockers'] = []
        text = p['specification']
        p['pattern'] = next((name for token, name in [
            ('Arenza', 'Arenza'), ('Louro Freijó', 'Louro Freijo Poro'),
            ('Branco TX', 'Branco TX'), ('Azul Petróleo', 'Azul Petroleo'),
            ('Beige Matt', 'Beige Matt'), ('Off-white', 'Off-white fosco')]
            if token in text), 'Indefinido')
        p['directional'] = p['pattern'] in ('Arenza', 'Louro Freijo Poro')
        p['w'], p['h'] = max(p['C_mm'], p['L_mm']), min(p['C_mm'], p['L_mm'])
        # Fichas atuais não individualizam veio. Maior dimensão paralela a 2750:
        # hipótese explícita do pedido de 28/10; não prova textura linear do Arenza.
        if p['pattern'] == 'Indefinido' and not p['packing_blockers']:
            p['packing_blockers'] = ['Padrão não individualizado']
    return panels


def orientations(p):
    return [(p['w'], p['h'], False)] + ([] if p['directional'] or p['w'] == p['h']
        else [(p['h'], p['w'], True)])


def partition(rect, w, h, vertical):
    x, y, rw, rh = rect
    if vertical:
        children = [(x+w+KERF, y, rw-w-KERF, rh), (x, y+h+KERF, w, rh-h-KERF)]
    else:
        children = [(x, y+h+KERF, rw, rh-h-KERF), (x+w+KERF, y, rw-w-KERF, h)]
    return [r for r in children if r[2] > 1e-8 and r[3] > 1e-8]


def pack(ordered, W, H, split_mode, score_mode):
    sheets, oversized = [], []
    for p in ordered:
        options = orientations(p)
        if not any(w <= W and h <= H for w, h, _ in options):
            oversized.append(p['id']); continue
        choices = []
        for si, sheet in enumerate(sheets):
            for fi, rect in enumerate(sheet['free']):
                for w, h, rotated in options:
                    if w <= rect[2]+1e-8 and h <= rect[3]+1e-8:
                        a, b = rect[2]-w, rect[3]-h
                        score = (min(a,b), rect[2]*rect[3]-w*h) if score_mode == 0 else (rect[2]*rect[3]-w*h, min(a,b))
                        choices.append((score, si, fi, w, h, rotated))
        if choices:
            _, si, fi, w, h, rotated = min(choices)
        else:
            si, fi = len(sheets), 0
            sheets.append({'free': [(TRIM, TRIM, W, H)], 'placements': [], 'cuts': []})
            w, h, rotated = next(o for o in options if o[0] <= W and o[1] <= H)
        sheet = sheets[si]; rect = sheet['free'].pop(fi)
        vertical = (rect[2]-w >= rect[3]-h) if split_mode == 0 else (w*(rect[3]-h) <= h*(rect[2]-w))
        children = partition(rect, w, h, vertical)
        sheet['free'].extend(children)
        sheet['placements'].append(dict(id=p['id'], module=p['module'], x=rect[0], y=rect[1], w=w, h=h, rotated=rotated))
        sheet['cuts'].append(dict(parent=rect, vertical_first=vertical, piece=p['id'], w=w, h=h, children=children))
    return dict(sheets=sheets, oversized=sorted(oversized))


def optimize(panels, W, H):
    orders = [sorted(panels, key=key, reverse=True) for key in [
        lambda p:(p['w']*p['h'],p['w'],p['id']), lambda p:(p['w'],p['h'],p['id']),
        lambda p:(p['h'],p['w'],p['id']), lambda p:(p['w']+p['h'],p['w'],p['id'])]]
    for seed in range(8):
        rng = random.Random(seed)
        keys = {p['id']: p['w']*p['h']*rng.uniform(.7,1.3) for p in panels}
        orders.append(sorted(panels, key=lambda p:keys[p['id']], reverse=True))
    candidates = [pack(order,W,H,split,score) for order in orders for split in (0,1) for score in (0,1)]
    def cost(plan):
        reusable = sum(w*h for s in plan['sheets'] for _,_,w,h in s['free'] if w>300 and h>300)
        return len(plan['oversized']),len(plan['sheets']),-reusable
    return min(candidates,key=cost)


def validate(plan, panels, W, H):
    byid={p['id']:p for p in panels}; seen=[]
    for sheet in plan['sheets']:
        free=[(TRIM,TRIM,W,H)]
        for cut in sheet['cuts']:
            parent=tuple(cut['parent']); assert parent in free
            free.remove(parent)
            assert cut['w'] <= parent[2]+1e-8 and cut['h'] <= parent[3]+1e-8
            children=partition(parent,cut['w'],cut['h'],cut['vertical_first'])
            assert children == [tuple(x) for x in cut['children']]
            free.extend(children)
        assert free == [tuple(x) for x in sheet['free']]
        assert len(sheet['cuts']) == len(sheet['placements'])
        cuts = {c['piece']:c for c in sheet['cuts']}
        for i,a in enumerate(sheet['placements']):
            seen.append(a['id']); p=byid[a['id']]
            c=cuts[a['id']]
            assert (a['x'],a['y'],a['w'],a['h']) == (*c['parent'][:2],c['w'],c['h'])
            assert (a['w'],a['h'],a['rotated']) in orientations(p)
            assert TRIM<=a['x'] and a['x']+a['w']<=TRIM+W+1e-8
            assert TRIM<=a['y'] and a['y']+a['h']<=TRIM+H+1e-8
            for b in sheet['placements'][i+1:]:
                dx=max(b['x']-a['x']-a['w'],a['x']-b['x']-b['w'])
                dy=max(b['y']-a['y']-a['h'],a['y']-b['y']-b['h'])
                assert max(dx,dy)>=KERF-1e-7
    assert len(seen)==len(set(seen)) and set(seen)|set(plan['oversized'])==set(byid)
    assert not set(seen)&set(plan['oversized'])


def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def main(out):
    out=Path(out).resolve()
    if out.is_relative_to(ROOT): raise ValueError('Use saída externa ao repositório')
    out.mkdir(parents=True,exist_ok=True)
    panels=load_panels(); groups=defaultdict(list)
    for p in panels:
        if not p['packing_blockers']: groups[(p['pattern'],p['thickness_mm'])].append(p)
    summaries=[]; detail=[]
    for gi,((pattern,t),ps) in enumerate(sorted(groups.items()),1):
        for width in (1850,2100):
            W,H=2750-2*TRIM,width-2*TRIM;plan=optimize(ps,W,H);validate(plan,ps,W,H)
            fitted=[p for p in ps if p['id'] not in plan['oversized']]
            area=sum(p['w']*p['h'] for p in fitted);lb=math.ceil(area/(W*H));n=len(plan['sheets'])
            scrap=[r for s in plan['sheets'] for r in s['free'] if r[2]>300 and r[3]>300]
            row=dict(padrao=pattern,espessura_mm=t,formato=f'2750x{width}',pecas=len(fitted),
                chapas_encontradas=n,limite_inferior_area=lb,lacuna_chapas=n-lb,
                aproveitamento_util_pct=round(100*area/(n*W*H),2) if n else 0,
                aproveitamento_bruto_pct=round(100*area/(n*2750*width),2) if n else 0,
                sobras_maiores_300x300=len(scrap),area_sobras_m2=round(sum(r[2]*r[3] for r in scrap)/1e6,4),
                nao_cabem=' | '.join(plan['oversized']),escopo='subconjunto; grupo integral inviavel' if plan['oversized'] else 'grupo completo')
            summaries.append(row);detail.append(dict(summary=row,plan=plan))
            for si,s in enumerate(plan['sheets'],1):
                body=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2750 {width+100}"><rect width="2750" height="{width}" fill="white" stroke="black"/>']
                for p in s['placements']:
                    body.append(f'<rect x="{p["x"]}" y="{p["y"]}" width="{p["w"]}" height="{p["h"]}" fill="#d9e6db" stroke="#395344"/><text x="{p["x"]+4}" y="{p["y"]+20}" font-size="16">{escape(p["module"]+"/"+p["id"])}</text>')
                for x,y,w,h in s['free']:
                    if w>300 and h>300:body.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#fff2c9" stroke="#aa8b22"/><text x="{x+5}" y="{y+20}" font-size="16">Sobra {w:.1f} x {h:.1f}</text>')
                body.append(f'<text x="20" y="{width+50}" font-size="22">{escape(pattern)} {t:g} mm · nominal, não fabricação · serra 3,2 / refilo 10</text></svg>')
                (out/f'G{gi:02d}_{width}_{si:02d}.svg').write_text(''.join(body),encoding='utf-8')
    with (out/'Chapas.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(summaries[0]),delimiter=';');w.writeheader();w.writerows(summaries)
    exclusions=[dict(id=p['id'],module=p['module'],motivos=p['packing_blockers']) for p in panels if p['packing_blockers']]
    sources=[*sorted((ROOT/'06_Entregas/Fichas_fabricacao').glob('P??-pecas.csv')), ROOT/'04_Moveis/Acabamentos_por_peca.csv',ROOT/'04_Moveis/Furacao/Fita_por_peca.csv',AREA/'Parametros.json',Path(__file__)]
    result=dict(cad_reference='R54',panels=249,included=sum(map(len,groups.values())),excluded=exclusions,
        source_sha256={p.relative_to(ROOT).as_posix():sha(p) for p in sources},summaries=summaries,plans=detail,
        method='48 heurísticas determinísticas por grupo/formato; cortes recursivos guilhotinados; limite inferior só por área útil',
        assumptions=['Arenza e Louro Freijo: maior dimensão paralela a 2750, sem rotação; hipótese pedida em 28/10, não textura comprovada de Arenza liso.',
        'Branco TX/Beige Matt/Azul Petroleo/Off-white: rotação permitida; mesmo padrão nas duas faces.',
        'Envelopes nominais não descontam fita; 23 IDs sem regra de borda não recebem espessura inventada; contornos especiais ocupam blank inteiro.',
        'SKU/substrato, disponibilidade de formato e processo não confirmados; 36 alternativas não somadas.'])
    (out/'Planos.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(included=result['included'],excluded=len(exclusions),summaries=summaries,sha256=sha(out/'Planos.json')),ensure_ascii=False))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--saida',required=True);main(parser.parse_args().saida)
