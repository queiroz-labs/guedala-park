"""Cenário elétrico nominal: ausência de dado nunca equivale a zero.

Executar na raiz: python -B ferramentas/estudos/quadro_cargas.py
Não dimensiona proteção/cabo nem modifica CAD, orçamento ou site.
"""
from pathlib import Path
import csv
import hashlib
import json
import math

ROOT = Path(__file__).resolve().parents[2]
AREA = ROOT / '03_Ambientes/Planta_pontos'
LIGHT = ROOT / '03_Ambientes/Iluminacao/Correntes_luz.csv'


def current(power, voltage=127, pf=1):
    if power is None:
        return None
    if power < 0 or voltage <= 0 or not 0 < pf <= 1:
        raise ValueError('Potência, tensão ou FP inválido')
    return power / (voltage * pf)


def voltage_drop(amps, length_m, resistance_ohm_km, reactance_ohm_km, pf):
    """Trecho monofásico ida+volta; comprimento simples. Nenhuma rota presumida."""
    if any(v is None for v in (amps, length_m, resistance_ohm_km, reactance_ohm_km, pf)):
        return None
    if min(amps, length_m, resistance_ohm_km, reactance_ohm_km) < 0 or not 0 < pf <= 1:
        raise ValueError('Parâmetro de queda inválido')
    return 2 * amps * length_m / 1000 * (resistance_ohm_km * pf + reactance_ohm_km * math.sqrt(1 - pf * pf))


def read_csv(path):
    with path.open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f, delimiter=';'))


def write_csv(path, rows):
    with path.open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter=';')
        w.writeheader()
        w.writerows(rows)


def build_loads(inputs, lights):
    rows = []
    for r in inputs:
        p = float(r['potencia_W']) if r['potencia_W'] else None
        rows.append(dict(r, simultaneidade_H01=1, FP_real='ausente',
                         I_equivalente_FP1_A=round(current(p), 4) if p is not None else '',
                         I_sensibilidade_FP08_A=round(current(p, pf=.8), 4) if p is not None else ''))
    for r in lights:
        p = float(r['W_entrada_cenario'])
        rows.append(dict(id='LUZ-' + r['grupo_funcional'], ambiente=r['ambiente'],
                         item='Iluminação ' + r['grupo_funcional'], ponto=r['grupo_funcional'],
                         circuito='IL-UM' if r['ambiente'] in ('cozinha', 'lavanderia', 'banho') else 'IL-SE',
                         potencia_W=p, qualidade='cenário H11 iluminação',
                         fonte='Iluminacao/Correntes_luz.csv; Estudo_fotometrico.md H11',
                         observacao='Entrada já inclui fontes/controle quando previstos; não somar potência DC novamente',
                         simultaneidade_H01=1, FP_real='ausente',
                         I_equivalente_FP1_A=round(current(p), 4), I_sensibilidade_FP08_A=round(current(p, pf=.8), 4)))
    ids = [r['id'] for r in rows]
    if len(ids) != len(set(ids)):
        raise ValueError('Carga duplicada')
    return rows


def aggregate(rows):
    circuits = []
    for name in sorted(set(r['circuito'] for r in rows)):
        group = [r for r in rows if r['circuito'] == name]
        known = sum(float(r['potencia_W']) for r in group if r['potencia_W'] != '')
        missing = sum(r['potencia_W'] == '' for r in group)
        light = name.startswith('IL-')
        circuits.append(dict(circuito_cenario=name, cargas=','.join(r['id'] for r in group),
                             P_parcial_W=round(known, 3), cargas_sem_potencia=missing,
                             I_parcial_FP1_A=round(current(known), 4), Ib_dimensionante_A='',
                             disjuntor_referencia='manual ME23P: 20 A curva C; conferir RT' if name == 'TUE-MIC' else 'a determinar pelo RT',
                             secao_minima_mecanica_Cu_mm2=1.5 if light else 2.5,
                             secao_final_mm2='', comprimento_real_m='', queda_V='',
                             DR_cenario='30 mA: verificar aplicação/tipo/coordenação pelo RT',
                             estado='cenário nominal para RT; não circuito existente'))
    return circuits


def main():
    inp = AREA / 'Cargas_entradas.csv'
    rows = build_loads(read_csv(inp), read_csv(LIGHT))
    write_csv(AREA / 'Quadro_cargas.csv', rows)
    write_csv(AREA / 'Circuitos_cenario.csv', aggregate(rows))
    known = sum(float(r['potencia_W']) for r in rows if r['potencia_W'] != '')
    result = {'tensao_cenario_V': 127, 'H01_simultaneidade': 1,
              'cargas': len(rows), 'cargas_sem_potencia': sum(r['potencia_W'] == '' for r in rows),
              'subtotal_referencias_W': round(known, 3), 'I_equivalente_FP1_A': current(known),
              'demanda_total_W': None, 'capacidade_predio_A': None,
              'nota': 'Subtotal mistura potências de manual e referências provisórias; não demanda dimensionante. AC fora da base.',
              'fontes_sha256': {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in (inp, LIGHT)}}
    (AREA / 'Quadro_cargas_resultado.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
