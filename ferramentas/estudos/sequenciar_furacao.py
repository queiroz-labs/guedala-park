"""Grafo nominal de instalar/apertar; não altera coordenadas nem o modelo.

As arestas de acesso vêm do auditor existente. Uma ordem topológica resolve
apenas essas precedências, não demonstra encaixe, estabilidade ou uso real.
"""
import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path

from gerar_furacao import ROOT, OUT, panels, write_csv
from conferir_furacao import audit, read


def build_graph(parts, holes, access):
    """Instalar ambos os painéis antecede apertar; apertar antecede bloqueador.

    O grupo identifica um conjunto Minifix, não uma junta inteira. Apenas
    arestas aperto→bloqueador são removíveis no estudo de troca de conector.
    """
    nodes = {'instalar:' + p for p in parts}
    edges = set()
    groups = defaultdict(set)
    for h in holes:
        if h['tipo'].startswith('Minifix') and h['grupo']:
            groups[h['grupo']].add(h['peca'])
    for group, members in groups.items():
        event = 'apertar:' + group
        nodes.add(event)
        if len(members) != 2:
            raise ValueError(f'{group}: esperado par de painéis, recebido {sorted(members)}')
        for p in members:
            edges.add(('instalar:' + p, event, ''))
    for row in access:
        g = row['grupo']
        if g not in groups or row['antes_de_instalar'] not in parts:
            raise ValueError('Restrição sem grupo/painel: ' + str(row))
        edges.add(('apertar:' + g, 'instalar:' + row['antes_de_instalar'], g))
    return nodes, sorted(edges)


def order_or_cycle(nodes, edges, removed=frozenset()):
    adjacency = defaultdict(list)
    for a, b, label in edges:
        if label and label in removed:
            continue
        adjacency[a].append((b, label))
    state, stack, trail, ordered = {}, [], [], []

    def visit(a):
        state[a] = 1
        stack.append(a)
        for b, label in sorted(adjacency[a]):
            if state.get(b) == 1:
                i = stack.index(b)
                return trail[i:] + [(a, b, label)]
            if not state.get(b):
                trail.append((a, b, label))
                cycle = visit(b)
                trail.pop()
                if cycle:
                    return cycle
        stack.pop()
        state[a] = 2
        ordered.append(a)
        return None

    for a in sorted(nodes):
        if not state.get(a):
            cycle = visit(a)
            if cycle:
                return None, cycle
    return list(reversed(ordered)), None


def minimum_relaxation(nodes, edges):
    """Busca exata por ramificação nos rótulos de um ciclo; sem heurística.

    Qualquer solução tem de remover ao menos um rótulo do ciclo encontrado.
    Retorna um mínimo e testemunho de ordem, não a viabilidade da ferragem
    substituta. Empates são resolvidos deterministicamente.
    """
    best, seen, visits = None, set(), 0

    def search(removed):
        nonlocal best, visits
        if removed in seen or (best is not None and len(removed) >= len(best)):
            return
        seen.add(removed)
        visits += 1
        order, cycle = order_or_cycle(nodes, edges, removed)
        if cycle is None:
            best = removed
            return
        options = sorted({label for _, _, label in cycle if label})
        if not options:
            return
        for label in options:
            search(removed | {label})

    search(frozenset())
    if best is None:
        return None, None, visits
    return sorted(best), order_or_cycle(nodes, edges, best)[0], visits


def run(destination):
    destination = destination.resolve()
    if destination.is_relative_to(ROOT.resolve()):
        raise ValueError('Dados completos devem ficar fora do projeto')
    destination.mkdir(parents=True, exist_ok=True)
    ps = panels(ROOT / '06_Entregas/Fichas_fabricacao')
    files = sorted(OUT.glob('P??-coordenadas.csv'))
    holes = [h for p in files for h in read(p)]
    issues, _, access = audit(holes, ps)
    summaries, sequences, constraints, cycles = [], [], [], []
    for module in sorted({p['mod'] for p in ps.values()}):
        parts = {p for p in ps if ps[p]['mod'] == module}
        hs = [h for h in holes if h['movel'] == module]
        restrictions = [a for a in access if a['movel'] == module]
        nodes, edges = build_graph(parts, hs, restrictions)
        order, cycle = order_or_cycle(nodes, edges)
        change, alternative, searched = minimum_relaxation(nodes, edges)
        summaries.append(dict(movel=module,paineis=len(parts),eventos=len(nodes),
            restricoes=len(restrictions),arestas=len(edges),ciclo=bool(cycle),
            minimo_trocas_no_grafo=None if change is None else len(change),
            conjuntos_propostos=change,estados_busca=searched,
            ordem_vigente_existe=order is not None,
            validacao_fisica=False))
        for a,b,label in edges:
            constraints.append(dict(movel=module,antes=a,depois=b,conjunto_removivel=label))
        for mode, seq in [('vigente',order),('proposta_sem_arestas_selecionadas',alternative if change else None)]:
            for i, event in enumerate(seq or [],1):
                sequences.append(dict(movel=module,cenario=mode,passo=i,evento=event))
        if cycle:
            cycles.append(dict(movel=module,primeiro_ciclo=cycle,
                minimo_trocas_no_grafo=len(change) if change is not None else None,
                conjuntos_propostos=change))
    write_csv(destination/'Ordem_eventos.csv',sequences)
    write_csv(destination/'Arestas.csv',constraints)
    (destination/'Ciclos.json').write_text(json.dumps(cycles,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    sources=files+[ROOT/'06_Entregas/Caderno_pranchas/Geometria.json',
        ROOT/'ferramentas/site/fabrication/technical-r14.json',
        ROOT/'ferramentas/site/fabrication/r14/hinge-drilling-maps.json',
        ROOT/'ferramentas/estudos/gerar_furacao.py',ROOT/'ferramentas/estudos/conferir_furacao.py']
    sources += sorted((ROOT/'06_Entregas/Fichas_fabricacao').glob('P??-pecas.csv'))
    report=dict(centros_antes=len(holes),centros_depois=len(holes),
        restricoes_estaticas_antes=len(access),restricoes_estaticas_depois=len(access),
        conflitos_geometricos=sum(i['tipo'] not in ['ACESSO','PARAMETRO'] for i in issues),
        modulos=summaries,geometria_e_coordenadas_alteradas=False,
        criterio='Grafo instalar ambos os painéis → apertar conjunto → instalar bloqueador; raio10/curso100 mm nominais. Troca remove só restrições de acesso desse conjunto, sem escolher conector.',
        fontes_sha256={str(p.relative_to(ROOT)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
        externos_sha256={name:hashlib.sha256((destination/name).read_bytes()).hexdigest() for name in ['Ordem_eventos.csv','Arestas.csv','Ciclos.json']})
    (destination/'Resumo_montagem.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps({k:v for k,v in report.items() if k not in ['fontes_sha256']},ensure_ascii=False))
    return report


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--saida',type=Path,required=True)
    run(parser.parse_args().saida)
