"""Triagem de envelopes nominais; não calcula capacidade ou massa final montada."""
import argparse
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = 'https://greenplac.com.br/products/mdf-arenza-linha-colore'
DENSITY = 63.2 / (2.750 * 1.850 * .018)  # densidade equivalente da chapa acabada


def calculate(module, row):
    ids = [s.strip() for s in row['IDs CAD'].split('|')]
    if len(ids) != int(row['Qtd']):
        raise ValueError('Quantidade diferente dos IDs: ' + str(ids))
    c, l, t = (float(row[k]) for k in ['C nominal mm', 'L nominal mm', 'Esp. envelope mm'])
    if min(c, l, t) <= 0:
        raise ValueError('Dimensão não positiva')
    volume = c * l * t / 1e9
    spec = row['Especificação documental']
    candidate = 'Greenplac Arenza' in spec and t == 18
    mass = volume * DENSITY if candidate else None
    return [dict(movel=module, id=i, peca=row['Peça'], c_mm=c, l_mm=l, esp_mm=t,
                 especificacao=spec, contorno=row['Contorno'], volume_envelope_m3=volume,
                 densidade_equivalente_kg_m3=DENSITY if candidate else '',
                 massa_envelope_cenario_kg=mass if candidate else '',
                 densidade_limiar_25kg_kg_m3=25 / volume,
                 maior_2200mm='sim' if max(c, l, t) > 2200 else 'nao',
                 envelope_cenario_maior_25kg='sim' if mass is not None and mass > 25 else
                 ('nao' if mass is not None else 'indeterminado'),
                 status='equivalência condicional Greenplac MDF BP 18; confirmar SKU/substrato' if candidate
                 else 'massa indeterminada: produto/substrato e massa de catálogo sem vínculo suficiente',
                 fonte=SOURCE if candidate else '') for i in ids]


def write_csv(path, rows):
    with path.open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter=';')
        writer.writeheader()
        writer.writerows(rows)


def generate(out):
    out.mkdir(parents=True, exist_ok=True)
    paths = sorted((ROOT / '06_Entregas/Fichas_fabricacao').glob('P*-pecas.csv'))
    rows = []
    for path in paths:
        with path.open(encoding='utf-8-sig', newline='') as f:
            for row in csv.DictReader(f, delimiter=';'):
                rows.extend(calculate(path.name.split('-')[0], row))
    if len(set(r['id'] for r in rows)) != len(rows):
        raise ValueError('IDs duplicados')
    hardware_path = ROOT / '04_Moveis/Furacao/Ferragens_por_movel.csv'
    with hardware_path.open(encoding='utf-8-sig', newline='') as f:
        hardware = list(csv.DictReader(f, delimiter=';'))
    summaries = []
    for module in sorted(set(r['movel'] for r in rows)):
        panels = [r for r in rows if r['movel'] == module]
        known = [r for r in panels if r['massa_envelope_cenario_kg'] != '']
        biggest = max(known, key=lambda r: r['massa_envelope_cenario_kg']) if known else None
        summaries.append(dict(movel=module, paineis=len(panels), volume_envelope_m3=sum(r['volume_envelope_m3'] for r in panels),
            paineis_com_cenario_catalogo=len(known), subtotal_envelopes_cenario_kg=sum(r['massa_envelope_cenario_kg'] for r in known) if known else '',
            maior_massa_entre_paineis_com_cenario_id=biggest['id'] if biggest else '',
            maior_massa_entre_paineis_com_cenario_kg=biggest['massa_envelope_cenario_kg'] if biggest else '',
            paineis_maiores_2200mm=' | '.join(r['id'] for r in panels if r['maior_2200mm'] == 'sim'),
            envelopes_cenario_maiores_25kg=' | '.join(r['id'] for r in known if r['envelope_cenario_maior_25kg'] == 'sim'),
            linhas_ferragens_sem_massa=sum(r['movel'] == module for r in hardware),
            massa_total_montada_kg='', status_total='incompleta: não somar como massa final'))
    write_csv(out / 'Massas_por_peca.csv', rows)
    write_csv(out / 'Ferragens_sem_massa.csv', [dict(r, massa_unitaria_kg='', status_massa='não publicada nas fontes consultadas; não representa zero') for r in hardware])
    write_csv(ROOT / '04_Moveis/Quantitativos/Massas_por_movel.csv', summaries)
    meta = dict(escopo='envelopes das fichas vigentes, sem abrir CAD; cenário de equivalência não confirmado',
                fonte=SOURCE, consulta='2026-10-28', densidade_equivalente_kg_m3=DENSITY,
                entradas_sha256={str(p.relative_to(ROOT)).replace('\\', '/'): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths + [hardware_path]},
                paineis=len(rows), paineis_com_cenario=sum(r['massa_envelope_cenario_kg'] != '' for r in rows),
                volume_envelope_total_m3=sum(r['volume_envelope_m3'] for r in rows),
                maiores_2200mm=[r['id'] for r in rows if r['maior_2200mm'] == 'sim'],
                envelopes_cenario_maiores_25kg=[r['id'] for r in rows if r['envelope_cenario_maior_25kg'] == 'sim'])
    (out / 'Resumo.json').write_text(json.dumps(meta, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k:v for k,v in meta.items() if k != 'entradas_sha256'}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT.parent / 'outputs/Massas_manuseio')
    generate(parser.parse_args().output)
