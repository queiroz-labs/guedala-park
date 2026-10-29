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
QUOTE = ROOT / '05_Orcamento_e_cronograma/Orcamento/Marcenaria_35mil/Pacote_cotacao_marcenaria_R01.md'
PROGRAM = ROOT / '01_Programa_e_decisoes/Programa_de_necessidades.md'


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


def network_errors(nodes):
    """Missing predecessors and time origins must not masquerade as zero slack."""
    return duration_errors(nodes) + [
        n['id'] + ': predecessores ainda incompletos'
        for n in nodes if n.get('dependencies_complete') is False
    ] + [
        n['id'] + ': data de início relativa às chaves ausente'
        for n in nodes if n.get('origin_missing')
    ]


def ancestors(nodes, terminal):
    ordered = topological(nodes)
    by_id = {n['id']: n for n in ordered}
    if terminal not in by_id:
        raise ValueError('Marco terminal ausente')
    wanted = set()

    def visit(key):
        wanted.add(key)
        for parent in by_id[key]['depends']:
            if parent not in wanted:
                visit(parent)

    visit(terminal)
    return [n for n in ordered if n['id'] in wanted]


def percentile(values, q):
    ordered = sorted(values)
    x = (len(ordered) - 1) * q
    lo, hi = math.floor(x), math.ceil(x)
    return ordered[lo] + (ordered[hi] - ordered[lo]) * (x - lo)


def simulate(nodes, terminal, count=5000, seed=20261028, deadline=8):
    """Strict engine; caller must provide a complete network and sourced modes.

    Independent sampling is an explicit model assumption, not inferred evidence.
    The project source currently fails validation, so no project samples are made.
    """
    errors = network_errors(nodes)
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
            'deadline_week': deadline,
            'probability_by_deadline': sum(v <= deadline for v in values) / count,
            'critical_paths': [{'path': list(k), 'count': v} for k, v in paths.most_common()],
            'ties': 'deterministic ID tie-break; ties are not unique critical paths',
            'sampling': 'independent; only usable when this assumption is accepted'}


def milestone_results(nodes, milestones):
    """Assess only ancestors of each milestone; unknown is never zero probability."""
    rows = []
    for m in milestones:
        chain = ancestors(nodes, m['terminal'])
        missing = network_errors(chain)
        if m.get('deadline_week') is None:
            missing.append('Marco absoluto sem data das chaves/ponte de calendário')
        result = None if missing else simulate(chain, m['terminal'], deadline=m['deadline_week'])
        rows.append(dict(marco=m['id'], alvo=m['target'],
                         prazo_semana=m.get('deadline_week'),
                         probabilidade=None if result is None else result['probability_by_deadline'],
                         cenarios=0 if result is None else result['scenarios'],
                         status='dado ausente' if missing else 'simulação condicional',
                         lacunas=' | '.join(missing)))
    return rows


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
    for n in nodes:
        if n['id'] in ('retoques_limpeza_testes', 'mudanca'):
            n['dependencies_complete'] = False
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


def current_model(text, quote, program):
    """Add only documented procurement gates and dated scope, not supplier promises."""
    checks = [(quote, 'Preparado para Elias revisar e enviar; não enviado.'),
              (quote, '30/10/2026 às 18 h, Brasília'),
              (quote, 'sem P16/P17/C01/C03/C04/C05'),
              (quote, 'E06 não é instalada nesta etapa'),
              (program, 'Philips 50PUG8100/78'), (program, 'TAB4000'),
              (program, '128 × 188 × 64'), (program, 'ASUS TUF VG27AQ5A'),
              (program, 'AOC 24″ existente'), (program, 'Volante e pedais: retirados')]
    for source, phrase in checks:
        if phrase not in source:
            raise ValueError('Fonte corrente alterada; revisar escopo: ' + phrase)
    nodes, purchases = source_model(text)

    def gate(key, deps, source, low=None, high=None):
        return dict(id=key, depends=deps, source_section=source, fixed=None,
                    minimum=low, mode=None, maximum=high)

    gates = [
        gate('envio_cotacao', [], 'Pedido R02/29-10: preparado, não enviado'),
        gate('retornos_cotacao', ['envio_cotacao'], 'Pedido R02: prazo solicitado 30/10 18h, não compromisso'),
        gate('comparacao_propostas', ['retornos_cotacao'], 'R00 seção 4; pedido R02: integral/etapa, inclusões e créditos'),
        gate('contratacao_marcenaria', ['comparacao_propostas'], 'R00 seção 4: escolher oficina antes das chaves; não contratada'),
        gate('definicoes_marcenaria', [], 'R00 seção 4: banco/cesto antes do executivo; pedido R02: produtos/ensaios pendentes'),
        gate('pedido_ferragens', ['contratacao_marcenaria'], 'R00 seção 3: após cotação, conferir fornecimento no pacote'),
        gate('abastecimento_ferragens', ['pedido_ferragens'], 'R00 seção 3: 1–3 semanas típicas, não cotadas', 1, 3),
    ]
    # These roots can precede the keys, but no calendar origin was supplied.
    for n in gates:
        if not n['depends']:
            n['origin_missing'] = True
    by_id = {n['id']: n for n in nodes}
    by_id['executivo']['depends'] += ['contratacao_marcenaria', 'definicoes_marcenaria']
    by_id['fabricacao']['depends'] += ['abastecimento_ferragens']
    by_id['fabricacao']['source_section'] += '; abastecimento no início: condição a confirmar com oficina'
    # A zero-duration junction is a milestone, not a missing service duration.
    gates.append(dict(id='inicio_fabricacao', depends=by_id['fabricacao']['depends'][:], fixed=0,
                      source_section='marco lógico: executivo e abastecimento completos; não é serviço de duração zero'))
    by_id['fabricacao']['depends'] = ['inicio_fabricacao']
    nodes += gates
    topological(nodes)
    decisions = [
        dict(item='Marcenaria D05-C/D06-B', status='etapa inicial sem P16/P17/C01/C03/C04/C05; E06 adiada; E05 mantida',
             effect='não inferir redução de prazo proporcional a preço, módulos ou chapas', source='Pedido R02, escopo vigente'),
        dict(item='TV/soundbar sala', status='Philips 50PUG8100/78 e TAB4000, decisões 29/10',
             effect='modelos identificados, prazo de entrega por SKU ausente; sem compra registrada', source='Programa, sala'),
        dict(item='Cama', status='viúva com baú atual; queen futura',
             effect='queen não é predecessora da mudança; transporte da cama atual não tem duração informada', source='Programa, quarto'),
        dict(item='Setup escritório', status='ASUS a comprar; AOC e TV existentes; cadeira fora da verba; volante/pedais retirados',
             effect='não duplicar compra de existentes nem prazo para itens retirados; fora da verba não significa comprado', source='Programa, escritório'),
        dict(item='Braços F80N', status='um comprado, um a comprar',
             effect='somente unidade adicional requer prazo comercial; sem prazo registrado', source='Programa, escritório'),
    ]
    return nodes, purchases, decisions


def known_chain_sensitivity():
    """A conditional two-link chain, never a whole-project critical path."""
    durations = {'fabricacao': (5, 6), 'pedras': (1, 2)}
    rows = []
    for key, (low, high) in durations.items():
        reduction = high - low
        rows.append(dict(item=key, intervalo_semanas=[low, high],
                         reducao_max_para_min_semanas=reduction,
                         ganho_na_cadeia_conhecida_semanas=reduction,
                         ganho_na_mudanca=None))
    return dict(base_known_duration=[6, 8], sensitivity=rows,
                global_best_item=None,
                first_action='Revisar/enviar cotação e obter escopo, prazo e vaga da oficina; envio continua pendente.',
                largest_avoided_risk=dict(item='fila da marcenaria', range_weeks=[2, 4],
                                         probability=None, avoided_weeks_guaranteed=None),
                limit='Empate de 1 semana por elo na cadeia conhecida. Fila 2–4 é risco textual separado, não ganho assegurado nem prazo somado.')


def build(output):
    text = SOURCE.read_text(encoding='utf-8')
    nodes, purchases, decisions = current_model(text, QUOTE.read_text(encoding='utf-8'), PROGRAM.read_text(encoding='utf-8'))
    errors = network_errors(nodes)
    milestones = [
        dict(id='respostas_cotacao', terminal='retornos_cotacao', deadline_week=None, target='30/10/2026 18h America/Sao_Paulo, solicitado'),
        dict(id='oficina_escolhida', terminal='contratacao_marcenaria', deadline_week=0, target='antes das chaves'),
        dict(id='inicio_fabricacao', terminal='inicio_fabricacao', deadline_week=2, target='executivo e abastecimento completos, marco nominal semana 2'),
        dict(id='box', terminal='fornecimento_box', deadline_week=6, target='semana 6, janela R00'),
        dict(id='pedras', terminal='pedras', deadline_week=8, target='semana 8, sem instalação incluída'),
        dict(id='obra', terminal='retoques_limpeza_testes', deadline_week=8, target='oito semanas'),
        dict(id='mudanca', terminal='mudanca', deadline_week=12, target='até semana 12, terceiro mês'),
    ]
    milestone_rows = milestone_results(nodes, milestones)
    gaps = errors + [p['item'] + ': moda de entrega ausente' for p in purchases if p['minimum_lead_weeks'] is not None]
    report = dict(source=SOURCE.relative_to(ROOT).as_posix(), source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
                  unit='semanas corridas; dias convertidos por 7, natureza útil/corrida a confirmar',
                  requested_scenarios=5000, executed_scenarios=0,
                  status='bloqueado por parâmetros ausentes; não foi substituído por distribuição uniforme ou moda central',
                  P50=None, P80=None, probability_by_week_8=None, most_frequent_critical_path=None,
                  missing_parameters=gaps, nodes=nodes, purchases=purchases,
                  sources_sha256={p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                                  for p in (SOURCE, QUOTE, PROGRAM)},
                  dated_scope=decisions, milestones=milestone_rows,
                  shortening=known_chain_sensitivity(),
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
    files = [result]
    for name, rows in [('Limites_compras.csv', purchases), ('Marcos_cronograma.csv', milestone_rows), ('Escopo_cronograma.csv', decisions)]:
        path = output / name
        with path.open('w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter=';')
            writer.writeheader(); writer.writerows(rows)
        files.append(path)
    return {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in files}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--saida', type=Path, required=True)
    args = parser.parse_args()
    if args.saida.resolve().is_relative_to(ROOT):
        parser.error('Escolha uma pasta externa ao repositório para os dados gerados.')
    print(json.dumps(build(args.saida), ensure_ascii=False))
