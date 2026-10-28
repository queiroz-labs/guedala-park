"""Audit the documented schedule without inventing triangular modes or durations.

Outputs go to an explicit external directory. No CAD, budget or source mutation.
Week N is the elapsed-time boundary N after the keys; calendar slots are not
silently converted into stochastic task durations.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import random
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / '05_Orcamento_e_cronograma/Cronograma_obra_e_compras.md'


def topological(nodes):
    by_id = {n['id']: n for n in nodes}
    if len(by_id) != len(nodes):
        raise ValueError('IDs duplicados')
    result, active, done = [], set(), set()

    def visit(key):
        if key not in by_id:
            raise ValueError('Dependência ausente: ' + key)
        if key in active:
            raise ValueError('Ciclo: ' + key)
        if key in done:
            return
        active.add(key)
        for predecessor in by_id[key]['depends']:
            visit(predecessor)
        active.remove(key)
        done.add(key)
        result.append(by_id[key])

    for key in by_id:
        visit(key)
    return result


def duration_errors(nodes):
    errors = []
    for n in topological(nodes):
        if n.get('fixed') is not None:
            if n['fixed'] < 0:
                errors.append(n['id'] + ': duração fixa negativa')
            continue
        a, m, b = (n.get(k) for k in ('minimum', 'mode', 'maximum'))
        if a is None or b is None:
            errors.append(n['id'] + ': faixa/duração a confirmar')
        elif m is None:
            errors.append(n['id'] + ': moda triangular não informada')
        elif not 0 <= a <= m <= b or a == b:
            errors.append(n['id'] + ': parâmetros triangulares inválidos')
    return errors


def percentile(values, q):
    ordered = sorted(values)
    x = (len(ordered) - 1) * q
    lo, hi = math.floor(x), math.ceil(x)
    return ordered[lo] + (ordered[hi] - ordered[lo]) * (x - lo)


def simulate(nodes, terminal, count=5000, seed=20261028):
    """Strict engine; caller must provide a complete network and sourced modes.

    Independent sampling is an explicit model assumption, not inferred evidence.
    The project source currently fails validation, so no project samples are made.
    """
    errors = duration_errors(nodes)
    if errors:
        raise ValueError('; '.join(errors))
    ordered = topological(nodes)
    if terminal not in {n['id'] for n in nodes}:
        raise ValueError('Marco terminal ausente')
    if count < 1:
        raise ValueError('Quantidade de cenários inválida')
    rng, values, paths = random.Random(seed), [], Counter()
    for _ in range(count):
        finish, path = {}, {}
        for n in ordered:
            previous = max(n['depends'], key=lambda p: (finish[p], p), default=None)
            start = finish[previous] if previous else 0
            d = n.get('fixed')
            if d is None:
                d = rng.triangular(n['minimum'], n['maximum'], n['mode'])
            finish[n['id']] = start + d
            path[n['id']] = (path[previous] if previous else ()) + (n['id'],)
        values.append(finish[terminal])
        paths[path[terminal]] += 1
    return {'scenarios': count, 'P50': percentile(values, .5),
            'P80': percentile(values, .8),
            'probability_by_week_8': sum(v <= 8 for v in values) / count,
            'critical_paths': [{'path': list(k), 'count': v} for k, v in paths.most_common()],
            'ties': 'deterministic ID tie-break; ties are not unique critical paths',
            'sampling': 'independent; only usable when this assumption is accepted'}


def purchase_limit(needed_week, maximum_lead_weeks):
    if needed_week is None or maximum_lead_weeks is None:
        return None
    return needed_week - maximum_lead_weeks


def source_model(text):
    # These exact phrases bind every hand-transcribed value to this source revision.
    for phrase in ['leva de 5 a 6 semanas', 'pedras (7–10 dias)',
                   '1–2 semanas **após o gabarito**', '1–3 semanas **após a medição**',
                   '3–10 dias', 'Semana 3–4', 'Entrega na semana 8–9']:
        if phrase not in text:
            raise ValueError('Fonte alterada; revisar extração: ' + phrase)

    def node(key, deps, ref, fixed=None, minimum=None, maximum=None):
        return dict(id=key, depends=deps, source_section=ref, fixed=fixed,
                    minimum=minimum, mode=None, maximum=maximum)

    nodes = [
        node('chaves', [], 'introdução: marco de origem', fixed=0),
        node('vistoria_medicao', ['chaves'], 'seção 2, semana 0'),
        node('executivo', ['vistoria_medicao'], 'seção 1, semanas 0/1'),
        node('fabricacao', ['executivo'], 'introdução/seção 1', minimum=5, maximum=6),
        node('inferiores', ['fabricacao'], 'seção 1, semana 7'),
        node('gabarito', ['inferiores'], 'seção 3, pedras'),
        node('pedras', ['gabarito'], 'seção 3, pedras; seção 1 mais estreita', minimum=1, maximum=2),
        node('rt', [], 'seção 2, contratado antes'),
        node('protocolo', ['rt'], 'seção 2, semana 0–1'),
        node('analise_condominio', ['protocolo'], 'seção 2, prazo a confirmar'),
        node('eletrica_hidraulica', ['analise_condominio'], 'seção 2, semana 1–2'),
        node('impermeabilizacao_cura', ['eletrica_hidraulica'], 'seção 2, semana 2, se refeita'),
        node('revestimentos', ['impermeabilizacao_cura'], 'seção 2, semana 2–4'),
        node('pintura_base', ['revestimentos'], 'seção 2, semana 4–5'),
        node('vinilico', ['pintura_base'], 'seção 2, semana 5–6'),
        node('medicao_box', ['revestimentos'], 'seção 3, só depois do revestimento'),
        node('fornecimento_box', ['medicao_box'], 'seção 3, box', minimum=1, maximum=3),
        node('instalacoes_box_e21_luz', ['revestimentos'], 'seção 2, semana 6'),
        node('marcenaria_pedras_loucas_metais_eletros', ['fabricacao'], 'seção 2, semana 7–8; agregado, não somar às etapas detalhadas'),
        node('retoques_limpeza_testes', [], 'seção 2, semana 8; predecessor não preenchido'),
        node('mudanca', [], 'introdução/seção 1; dependências e duração não fechadas'),
    ]
    # These are backward dates against named calendar slots, NOT a full CPM schedule.
    purchases = [
        ('RT', None, None, None, 'Antes da semana 0', 'Sem duração de contratação; não há data-limite numérica.'),
        ('Ferragens', 1, 3, 2, 'Após cotação; se a marcenaria não fornecer', 'Necessidade na semana 2 é condição de abastecer o início da fabricação; confirmar marco da oficina.'),
        ('Porcelanatos', 1, 4, 2, '-4', 'Marco: início previsto dos revestimentos; pedido -4 oferece 2 semanas frente ao limite calculado -2.'),
        ('Vinílico', 1, 3, 5, '-3', 'Marco: início previsto semana 5; pedido -3 antecipa 5 semanas frente ao limite +2.'),
        ('Louças/metais', 1, 2, 7, '2–4', 'Marco: início do agregado da semana 7; montagem ainda sem duração própria.'),
        ('E21 para gás', 1, 2, 1, '2', 'A fonte exige presença para o gás (semanas 1–2), mas manda pedir na semana 2: incompatibilidade a confirmar.'),
        ('Eletrodomésticos', 3/7, 10/7, 7, '5–6', 'Limite só para montagem na semana 7; forno pode ser exigido antes para conferir nicho, sem data na fonte.'),
        ('Luminárias', 1, 3, 6, '3', 'Marco: instalação de teto na semana 6; sem folga usando prazo máximo.'),
        ('Estofados', 2, 4, 7, 'Com o pedido da marcenaria', 'Marco condicional: início da montagem do agregado na semana 7; confirmar integração com oficina.'),
        ('Sofás/Berlin/cadeiras', 2, 6, 8, '3–4', 'Marco: primeira semana de entrega desejada (8); pedir 3–4 com 6 semanas entrega 9–10.'),
        ('Box', 1, 3, 6, 'Medir 4–5', 'O limite +3 exigiria medição +3; a fonte prevê 4–5, portanto entrega 5–8. Não é compra possível antes da medição.'),
        ('Pedras para terminar na semana 8', 1, 2, 8, 'Gabarito 7', 'Limite +6 exigiria inferiores/gabarito +6; gabarito +7 termina +8 a +9, sem instalação/limpeza. Não é compra antes das chaves.'),
    ]
    rows = []
    for item, low, high, need, stated, note in purchases:
        rows.append(dict(item=item, minimum_lead_weeks=low, maximum_lead_weeks=high,
                         mode_weeks=None, needed_week_conditional=need,
                         latest_order_week_conditional=purchase_limit(need, high),
                         source_order_week=stated, condition=note))
    return nodes, rows


def build(output):
    text = SOURCE.read_text(encoding='utf-8')
    nodes, purchases = source_model(text)
    errors = duration_errors(nodes)
    gaps = errors + [p['item'] + ': moda de entrega ausente' for p in purchases if p['minimum_lead_weeks'] is not None]
    report = dict(source=SOURCE.relative_to(ROOT).as_posix(), source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
                  unit='semanas corridas; dias convertidos por 7, natureza útil/corrida a confirmar',
                  requested_scenarios=5000, executed_scenarios=0,
                  status='bloqueado por parâmetros ausentes; não foi substituído por distribuição uniforme ou moda central',
                  P50=None, P80=None, probability_by_week_8=None, most_frequent_critical_path=None,
                  missing_parameters=gaps, nodes=nodes, purchases=purchases,
                  known_chain=dict(fabrication_start_from_diagram=2, fabrication_finish_interval=[7, 8],
                                   known_fabrication_plus_stone_duration=[6, 8],
                                   start_plus_known_durations=[8, 10],
                                   warning='8–10 NÃO é intervalo da mudança: omite montagem, gabarito, instalações, limpeza e demais esperas sem duração.',
                                   stone_from_week_7_by_section_1=[8, 7+10/7],
                                   stone_from_week_7_by_section_3=[8, 9]),
                  network_limits=['Não há rede completa até a mudança.',
                                  'O agregado da semana 7–8 não deve ser somado a seus componentes.',
                                  'A fonte chama marcenaria de caminho crítico, mas não há dados para frequência probabilística.',
                                  'Fila de 2–4 semanas é risco separado, sem probabilidade/moda; não somado automaticamente.',
                                  'Retoques na semana 8 versus limpeza/mudança na semana 9: metas diferentes, não duração triangular.'])
    output.mkdir(parents=True, exist_ok=True)
    result = output / 'Cronograma_risco.json'
    result.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    with (output / 'Limites_compras.csv').open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(purchases[0]), delimiter=';')
        writer.writeheader(); writer.writerows(purchases)
    return {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in [result, output / 'Limites_compras.csv']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--saida', type=Path, required=True)
    args = parser.parse_args()
    if args.saida.resolve().is_relative_to(ROOT):
        parser.error('Escolha uma pasta externa ao repositório para os dados gerados.')
    print(json.dumps(build(args.saida), ensure_ascii=False))
