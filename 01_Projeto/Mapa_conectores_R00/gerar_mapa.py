"""Mapa de conectores proposto R00 para P01, P04, P12 e P17.

Lê as interfaces sem mapa das fichas R14 (technical-r14.json) e os nomes das peças
(05_Entregas/Fichas_fabricacao_R13/Pxx-pecas.csv) e propõe a quantidade de conectores
por encontro, segundo a estratégia já escolhida em cada ficha:
  - encontro com o fundo  -> Confirmat 7x50 + cavilha Ø8x30 (fundo oculto)
  - demais encontros de 18 -> Minifix 15 + cavilha Ø8x30
Regra de espaçamento (proposta, a validar em oficina): 2 conectores até 400 mm de
contato, 3 até 700 mm e, acima disso, um a cada ~350 mm. Não altera fichas nem CAD.
Uso: python gerar_mapa.py
"""
from pathlib import Path
import csv, json, math, re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
TECH = json.loads((ROOT / '01_Projeto/Estudo_interativo/fabrication/technical-r14.json').read_text(encoding='utf-8'))['modules']
MODULES = ['P01', 'P04', 'P12', 'P17']


def names(mod):
    out = {}
    with open(ROOT / f'05_Entregas/Fichas_fabricacao_R13/{mod}-pecas.csv', encoding='utf-8-sig') as f:
        for row in csv.DictReader(f, delimiter=';'):
            ids = row.get('ID CAD') or row.get('IDs CAD') or ''
            parts = [p.strip() for p in row['Peça'].split('/')]
            for i, pid in enumerate(x.strip() for x in ids.split('|')):
                out[pid] = parts[min(i, len(parts) - 1)]
    return out


def count(length):
    if length <= 400:
        return 2
    if length <= 700:
        return 3
    return math.ceil(length / 350) + 1


rows, totals = [], {}
for mod in MODULES:
    nm = names(mod)
    t = totals.setdefault(mod, {'Minifix 15': 0, 'Confirmat 7×50': 0, 'Cavilha Ø8×30': 0, 'encontros': 0})
    for s in TECH[mod]['unmappedInterfaces']:
        m = re.match(r'(\S+) ↔ (\S+) \((\w); ([\d.]+)×([\d.]+) mm\)', s)
        a, b, axis, d1, d2 = m.groups()
        length = max(float(d1), float(d2))
        na = nm.get(a, 'Apoio / divisória interna' if a.startswith('Apoio') else '?')
        nb = nm.get(b, 'Apoio / divisória interna' if b.startswith('Apoio') else '?')
        face = float(d1) != 18 and float(d2) != 18
        back = 'fundo' in (na + nb).lower()
        if face:  # dois painéis encostados face com face (divisor duplo de 36 mm)
            kind, n = 'Parafuso 4×30 face a face', 4
        else:
            kind = 'Confirmat 7×50' if back else 'Minifix 15'
            n = count(length)
        t[kind] = t.get(kind, 0) + n
        t['Cavilha Ø8×30'] += 0 if face else n
        t['encontros'] += 1
        rows.append([mod, a, na, b, nb, f'{length:.0f}', kind, n, 0 if face else n])

with open(HERE / 'Mapa_conectores_R00.csv', 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.writer(f, delimiter=';')
    w.writerow(['Módulo', 'Peça A', 'Nome A', 'Peça B', 'Nome B', 'Contato mm', 'Conector', 'Qtd conector', 'Qtd cavilha'])
    w.writerows(rows)

lines = ['| Módulo | Encontros | Minifix 15 | Confirmat 7×50 | Cavilhas Ø8×30 | Parafusos 4×30 (face a face) |', '|---|---:|---:|---:|---:|---:|']
g = {'Minifix 15': 0, 'Confirmat 7×50': 0, 'Cavilha Ø8×30': 0, 'Parafuso 4×30 face a face': 0, 'encontros': 0}
for mod, t in totals.items():
    lines.append(f"| {mod} · {TECH[mod]['name']} | {t['encontros']} | {t['Minifix 15']} | {t['Confirmat 7×50']} | {t['Cavilha Ø8×30']} | {t.get('Parafuso 4×30 face a face', 0)} |")
    for k in g:
        g[k] += t.get(k, 0)
lines.append(f"| **Total** | **{g['encontros']}** | **{g['Minifix 15']}** | **{g['Confirmat 7×50']}** | **{g['Cavilha Ø8×30']}** | **{g['Parafuso 4×30 face a face']}** |")
md = HERE / 'README.md'
head = md.read_text(encoding='utf-8').split('<!-- TOTAIS -->')[0]
tail = (f"\n## Efeito no orçamento\n\nSomando os 40 Minifix já definidos (P10, P11, P15), o projeto teria cerca de **{g['Minifix 15'] + 40} Minifix**, "
        "contra 20 na memória do orçamento. Em custo, a diferença é pequena: a R$1,50–3,00 por conjunto, mais Confirmat e cavilhas, "
        "fica em cerca de **R$250–550** no total. Isso cabe na verba de conectores e fixadores (R$650–1.200) da "
        "[revisão de ferragens](../Orcamento_R43_2026-10-22/Marcenaria_35mil/Revisao_ferragens_servicos_2026-10-23.md). "
        "O impacto maior é em **horas de furação**, que a oficina deve considerar.\n")
md.write_text(head + '<!-- TOTAIS -->\n\n' + '\n'.join(lines) + '\n' + tail, encoding='utf-8')
print(g)
