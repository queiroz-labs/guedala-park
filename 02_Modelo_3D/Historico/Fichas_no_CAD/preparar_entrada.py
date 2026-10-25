"""Extrai das fichas R14 os dados que a macro grava no CAD R46. Não abre o FreeCAD."""
from pathlib import Path
import csv, json

HERE = Path(__file__).resolve().parent
PROJ = HERE.parent
STUDY = PROJ / 'Estudo_interativo'
fd = (STUDY / 'src/fabrication-data.js').read_text(encoding='utf-8')
fd = json.loads(fd[fd.index('{'):fd.rindex('}') + 1])
geometry = json.loads((STUDY / 'fabrication/r14/joinery-geometry.json').read_text(encoding='utf-8'))
joinery = json.loads((STUDY / 'fabrication/r14/joinery.json').read_text(encoding='utf-8'))


def qty(r):
    q = r.get('quantity')
    return (f"{q:g} {r.get('unit', '')}".strip() if isinstance(q, (int, float)) else 'qtd. a definir')


modules = {}
for i, (code, m) in enumerate(sorted(fd['modules'].items())):
    modules[code] = dict(
        cadModule='Modulo' + ('' if i == 0 else f'{i:03}'), name=m['name'], summary=m['technicalSummary'],
        sheet=m['sheetPath'],
        hardware=[f"{qty(r)} · {r['item']} — {r.get('reference') or 'referência na ficha'} [{r['status']}]" for r in m['hardwareRows']],
        panels={p['id']: dict(name=p['name'], spec=p['specifiedMaterial'] or 'Ver regra de acabamento da ficha', dims=p['dimensions']) for p in m['panels']})

# Minifix: pontos na face de acesso; o eixo entra na peça.
minifix = []
for code, rows in [('P10', joinery['modules']['P10']['nominalPositions']),
                   ('P11', geometry['modules']['P11']['positions']),
                   ('P15', geometry['modules']['P15']['positions'])]:
    for r in rows:
        minifix.append(dict(module=code, board=r['board'], frame='global', point=r['cam_axis_global_mm'],
                            axis=[0, 0, -1] if r['access'] == 'top' else [0, 0, 1], depth=14))
with open(PROJ / 'Banheiro/Fechamento_pre_entrega_2026-10-24/P19_Unioes_nominais.csv', encoding='utf-8-sig') as f:
    for r in csv.DictReader(f):
        if r['operation'] == 'Caixa Minifix':
            minifix.append(dict(module='P19', board=r['part'], frame='Modulo018',
                                point=[float(r['x']), float(r['y']), float(r['z'])],
                                axis=[float(r['axis_x']), float(r['axis_y']), float(r['axis_z'])], depth=float(r['depth_mm'])))

expected = {'P10': 20, 'P11': 12, 'P15': 8, 'P19': 12}
counts = {c: sum(1 for p in minifix if p['module'] == c) for c in expected}
assert counts == expected, counts
(HERE / 'Entrada_R46.json').write_text(json.dumps(dict(modules=modules, minifix=minifix), ensure_ascii=False, indent=1), encoding='utf-8')
print('Entrada R46:', len(modules), 'módulos,', sum(len(m['panels']) for m in modules.values()), 'peças,', len(minifix), 'Minifix')
