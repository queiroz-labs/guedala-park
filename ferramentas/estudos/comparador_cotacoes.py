"""Comparação documental, sem escolher fornecedor. Biblioteca padrão; fontes preservadas."""
import argparse
import csv
from datetime import date
from decimal import Decimal, InvalidOperation
import hashlib
import json
from pathlib import Path
import re
import sys
import unicodedata

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
AREA = ROOT / '05_Orcamento_e_cronograma/Orcamento/Cotacoes'
OUT = ROOT.parent / 'outputs/Codex_cotacao_e_chaves'
RAW = ROOT.parent / 'outputs/Propostas_recebidas'
REF = '06_Entregas/Cotacao/Quantidades_referencia.csv'
CUT = '04_Moveis/Plano_de_corte/'
CSV_FIELDS = ['fornecedor', 'linha', 'campo', 'valor', 'unidade', 'origem']
META = ['data', 'validade', 'escopo', 'preco_total', 'fabricacao', 'entrega',
        'montagem', 'medicao_in_loco', 'retirada', 'frete_incluso', 'frete',
        'impostos_inclusos', 'impostos', 'pagamento', 'sinal_percentual',
        'garantia_meses', 'exclusoes', 'premissas', 'reajuste', 'multa',
        'producao_dias', 'entrega_dias', 'montagem_dias', 'inicio_semana_chaves',
        'calendario', 'gatilho_prazo', 'risco_reajuste', 'observacoes']
LINE = ['situacao', 'quantidade', 'preco_unitario', 'preco_total_linha',
        'marca_modelo', 'sku', 'cor', 'espessura_mm', 'formato', 'regra_borda',
        'tipo_fita', 'equivalencia', 'observacoes']
WEIGHTS = {'preco': 35, 'cobertura': 25, 'reajuste': 15, 'prazo': 10,
           'garantia': 10, 'substituicoes': 5}


def read_csv(path, delimiter=';'):
    with Path(path).open(encoding='utf-8-sig', newline='') as stream:
        return list(csv.DictReader(stream, delimiter=delimiter))


def write_csv(path, rows, fields):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, delimiter=';', extrasaction='ignore')
        writer.writeheader()
        writer.writerows(rows)


def dump(path, data):
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2, default=str) + '\n', encoding='utf-8')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def key(value):
    return ''.join(c for c in unicodedata.normalize('NFKD', str(value)).lower() if not unicodedata.combining(c))


def number(value):
    """Vazio é None; decimal brasileiro e ponto de milhar são aceitos."""
    if value is None or str(value).strip() == '':
        return None
    text = str(value).strip().replace('R$', '').replace(' ', '')
    if ',' in text:
        text = text.replace('.', '').replace(',', '.')
    try:
        result = Decimal(text)
    except InvalidOperation as exc:
        raise ValueError('Número inválido: ' + str(value)) from exc
    if not result.is_finite() or result < 0:
        raise ValueError('Número negativo/não finito: ' + str(value))
    return result


def quantity(value, unit, expected):
    result = number(value)
    if result is None:
        return None
    aliases = {'un': 'unidade', 'unidades': 'unidade', 'chapa': 'chapa', 'chapas': 'chapa',
               'metros': 'm', 'metro': 'm', 'pares': 'par', 'paineis': 'painel'}
    unit, expected = key(unit).strip(), key(expected).strip()
    unit, expected = aliases.get(unit, unit), aliases.get(expected, expected)
    if expected == 'm' and unit in {'mm', 'cm', 'm'}:
        return result * {'mm': Decimal('.001'), 'cm': Decimal('.01'), 'm': Decimal(1)}[unit]
    if unit != expected:
        raise ValueError(f'Unidade {unit!r} incompatível com {expected!r}')
    return result


def references():
    return {f'L{i:03}': row for i, row in enumerate(read_csv(ROOT / REF), 1)}


def gaps():
    result = {}
    for row in read_csv(ROOT / (CUT + 'Lista_de_corte.csv')):
        if row['variante'] == 'base' and row['bloqueios']:
            result['CORTE-' + row['id']] = dict(grupo='lacuna_corte', item=row['id'],
                movel=row['movel'], quantidade='', unidade='', fonte=CUT + 'Lista_de_corte.csv')
    for i, row in enumerate(read_csv(ROOT / '04_Moveis/Furacao/Ferragens_pendentes.csv'), 1):
        result[f'FER-PEND-{i:02}'] = dict(grupo='lacuna_ferragem', item=row.get('item', str(row)),
            movel=row.get('movel', ''), quantidade='', unidade='', fonte='04_Moveis/Furacao/Ferragens_pendentes.csv')
    result['P19-MINIFIX'] = dict(grupo='divergencia', item='P19: 12 documentais versus 8 no mapa',
        movel='P19', quantidade='', unidade='', fonte='06_Entregas/Cotacao/README.md')
    return result


def value(record, field):
    return record.get(field, {}).get('valor')


def load_proposals(path):
    if not path:
        return []
    path = Path(path)
    if path.suffix.lower() == '.json':
        proposals = json.loads(path.read_text(encoding='utf-8-sig'))['propostas']
    else:
        codes = {}
        for row in read_csv(path):
            if not row['fornecedor'].strip():
                if row['valor'].strip():
                    raise ValueError('Valor preenchido sem fornecedor')
                continue
            supplier = row['fornecedor']
            proposal = codes.setdefault(supplier, dict(fornecedor=supplier, campos={}, linhas={}))
            fields = proposal['campos'] if not row['linha'] else proposal['linhas'].setdefault(row['linha'], {})
            if row['campo'] in fields:
                raise ValueError('Campo duplicado: ' + str((supplier, row['linha'], row['campo'])))
            fields[row['campo']] = {k: row[k] for k in ['valor', 'unidade', 'origem']}
        proposals = list(codes.values())
    known = set(references()) | set(gaps())
    seen = set()
    for proposal in proposals:
        supplier = proposal['fornecedor']
        if not re.fullmatch(r'F\d{2,}', supplier) or supplier in seen:
            raise ValueError('Fornecedor deve ser código Fxx único')
        seen.add(supplier)
        for line, fields in [('', proposal['campos']), *proposal['linhas'].items()]:
            if line and line not in known:
                raise ValueError('Linha desconhecida: ' + line)
            for name, sourced in fields.items():
                if name not in (LINE if line else META):
                    raise ValueError('Campo desconhecido: ' + name)
                if not isinstance(sourced, dict) or 'valor' not in sourced:
                    raise ValueError('Cada campo exige valor/unidade/origem')
                if sourced['valor'] not in (None, '') and not sourced.get('origem'):
                    raise ValueError('Campo sem origem: ' + name)
            if line and value(fields, 'situacao') not in (None, '', 'incluida', 'excluida', 'esclarecer'):
                raise ValueError('Situação inválida: ' + line)
    return proposals


def coverage(ref, line):
    status = value(line, 'situacao')
    if status == 'excluida':
        return 'excluída', None
    if status != 'incluida':
        return 'não mencionada', None
    qty = quantity(value(line, 'quantidade'), line.get('quantidade', {}).get('unidade', ''), ref['unidade'])
    expected = number(ref.get('quantidade_com_perda') or ref.get('quantidade'))
    return ('coberta com quantidade diferente' if expected is not None and qty != expected else 'coberta'), qty


def substituted(ref, line):
    if ref['grupo'] != 'ferragens' or value(line, 'situacao') != 'incluida':
        return False
    model = value(line, 'marca_modelo')
    return bool(model and key(model).strip() != key(ref['item']).strip())


def unit_price(line):
    price = number(value(line, 'preco_unitario'))
    qty = number(value(line, 'quantidade'))
    total = number(value(line, 'preco_total_linha'))
    if price is None and total is not None and qty and line['quantidade'].get('unidade'):
        price = total / qty
    return price


def project_range(ref):
    # Só o mesmo padrão, espessura E formato. Custos históricos são para 1850.
    if ref['grupo'] == 'chapas' and ref['formato'] == '2750x1850':
        matches = [r for r in read_csv(ROOT / (CUT + 'Custos_chapas.csv'))
                   if r['cenario'] == 'refilo10_serra4' and r['opcao_offwhite'] == 'Lume'
                   and r['padrao'] == ref['padrao'] and number(r['espessura_mm']) == number(ref['espessura_mm'])]
        if matches and matches[0]['preco_unit_baixo']:
            r = matches[0]
            # Lume é opção, não produto escolhido: não usar como substituto de Off-white.
            if ref['padrao'] == 'Off-white fosco':
                return None
            return number(r['preco_unit_baixo']), number(r['preco_unit_alto']), CUT + 'Custos_chapas.csv: ' + r['padrao']
    return None


def missing_cost(code, ref, proposal, proposals, missing):
    prices, sources = [], []
    for other in proposals:
        if other is proposal or value(other['campos'], 'escopo') != value(proposal['campos'], 'escopo'):
            continue
        line = other['linhas'].get(code, {})
        if value(line, 'situacao') != 'incluida' or substituted(ref, line):
            continue
        # Comparabilidade exige especificação coincidente, não apenas ID atribuído.
        if ref['grupo'] == 'chapas':
            if (value(line, 'formato') != ref['formato']
                    or number(value(line, 'espessura_mm')) != number(ref['espessura_mm'])
                    or key(value(line, 'cor') or '') != key(ref['padrao'])):
                continue
        if ref['grupo'] == 'ferragens' and key(value(line, 'marca_modelo') or '') != key(ref['item']):
            continue
        price = unit_price(line)
        if price is not None:
            factor = quantity(1, line.get('quantidade', {}).get('unidade', ''), ref['unidade'])
            prices.append(price / factor)
            sources.append(other['fornecedor'] + '/' + code + ': ' + line.get('preco_unitario', line.get('preco_total_linha', {})).get('origem', ''))
    if prices:
        return min(prices) * missing, max(prices) * missing, 'estimado com base em outra proposta', ' | '.join(sources)
    interval = project_range(ref)
    if interval:
        low, high, source = interval
        return low * missing, high * missing, 'estimado por referência do projeto', source
    return None, None, 'sem base', ''


def schedule(fields):
    names = ['producao_dias', 'entrega_dias', 'montagem_dias', 'inicio_semana_chaves']
    values = [number(value(fields, name)) for name in names]
    if any(v is None for v in values) or value(fields, 'calendario') != 'corridos' or not value(fields, 'gatilho_prazo'):
        return None, 'indeterminado: faltam durações/gatilho/calendário; alvo mudança até semana 12'
    finish = values[3] + sum(values[:3]) / 7
    status = 'revisar: cadeia excede semana 12' if finish > 12 else 'atenção: cabe só esta cadeia; pedras, RT e conclusão da obra pendentes'
    return finish, status


def compare(proposals, as_of, weights, dependencies=None):
    refs, holes = references(), gaps()
    matrix, estimates, questions, summary = [], [], [], []
    dep_codes = {r['linha'] for r in dependencies or []}
    scenarios = { (r['padrao'], number(r['espessura_mm'])): r
        for r in read_csv(ROOT / (CUT + 'Resumo_chapas.csv'))
        if r['variante'] == 'base' and r['cenario'] == 'refilo10_serra4'}
    for proposal in proposals:
        supplier, fields = proposal['fornecedor'], proposal['campos']
        declared = number(value(fields, 'preco_total'))
        low = high = declared
        unknown, covered, substitutions = [], 0, 0
        def ask(code, text):
            questions.append(dict(fornecedor=supplier, numero=1 + sum(q['fornecedor'] == supplier for q in questions), linha=code, pergunta=text))
        for code, ref in {**refs, **holes}.items():
            line = proposal['linhas'].get(code, {})
            status, qty = coverage(ref, line)
            swap = substituted(ref, line)
            expected = number(ref.get('quantidade_com_perda') or ref['quantidade'])
            alerts = []
            if swap:
                substitutions += 1
                alerts.append('substituição; equivalência ' + str(value(line, 'equivalencia') or 'pendente'))
                ask(code, f"A troca de {ref['item']} por {value(line, 'marca_modelo')} preserva montagem/desempenho? Informar custo da especificação original e crédito da troca.")
            if code in refs and status == 'coberta' and not swap:
                covered += 1
            if ref['grupo'] == 'ferragens' and value(line, 'situacao') == 'incluida' and not value(line, 'marca_modelo'):
                alerts.append('marca/modelo ausente; equivalência pendente')
                unknown.append(code + ': especificação pendente')
            if ref['grupo'] == 'chapas' and value(line, 'situacao') == 'incluida':
                if value(line, 'formato') != ref['formato']:
                    alerts.append('formato diferente/ausente; 14 misto ≠ 15 em 1850 (215 painéis; Peca208 fora)')
                if expected != qty:
                    alerts.append(f'divergência de chapas: misto {expected}; confirmar cenário/LI por grupo')
                if not value(line, 'sku'):
                    alerts.append('SKU/processo a confirmar')
                    unknown.append(code + ': SKU/processo pendente')
                if (number(value(line, 'espessura_mm')) != number(ref['espessura_mm'])
                        or key(value(line, 'cor') or '') != key(ref['padrao'])):
                    alerts.append('cor/espessura diferente ou ausente; não demonstra mesmo escopo')
                    unknown.append(code + ': cor/espessura pendente')
            if ref['grupo'] == 'fita':
                if qty is not None and expected and abs(qty / expected - 1) > Decimal('.10'):
                    alerts.append('metragem diverge mais de 10% da referência com perda')
                if not value(line, 'regra_borda'):
                    alerts.append('regra de borda ausente; comparar com C0/C1/L0/L1')
            if expected is not None and value(line, 'situacao') == 'incluida' and qty is None:
                alerts.append('quantidade ausente ≠ zero')
            if status != 'coberta' or alerts or ref['grupo'].startswith('lacuna') or ref['grupo'] in {'limite', 'fita_sem_regra', 'divergencia'}:
                ask(code, f"{ref['item']}: confirmar inclusão, quantidade/especificação e preço no escopo {value(fields, 'escopo') or 'a definir'}. Situação: {status}; {'; '.join(alerts) or value(line, 'situacao') or 'não respondida'}.")
            matrix.append(dict(fornecedor=supplier, linha=code, grupo=ref['grupo'], item=ref['item'], movel=ref['movel'],
                quantidade_referencia=expected, quantidade_proposta=qty, cobertura=status,
                substituicao='sim' if swap else '', lacuna_resposta=value(line, 'situacao'),
                premissa_medida_in_loco='sim' if code in dep_codes else 'a conferir',
                alertas=' | '.join(alerts), origem=json.dumps(line, ensure_ascii=False)))
            if ref['grupo'] == 'chapas':
                scenario = scenarios.get((ref['padrao'], number(ref['espessura_mm'])), {})
                matrix[-1].update(chapas_cenario1850=scenario.get('chapas_subconjunto'),
                    limite_inferior1850=scenario.get('limite_inferior_subconjunto'),
                    ressalva_cenario1850=scenario.get('nao_cabem'))
            # Painéis são custo agregado: nunca somar de novo com chapas/fita.
            if ref['grupo'] in {'paineis', 'comparacao_nao_somar'}:
                if status != 'coberta':
                    unknown.append(code + ': cobertura/agregado pendente')
                continue
            if expected is None and status == 'coberta':
                continue  # inclusão explícita da lacuna no preço, a conferir na origem
            missing = None if expected is None else max(Decimal(0), expected - (qty or 0))
            if swap or (ref['grupo'] == 'chapas' and value(line, 'situacao') == 'incluida' and value(line, 'formato') != ref['formato']):
                missing = None  # falta crédito e solução compatível; não somar troca integral por cima
            if expected is not None and qty is None and value(line, 'situacao') == 'incluida':
                missing = None
            if missing == 0 and not swap:
                continue
            cost = missing_cost(code, ref, proposal, proposals, missing) if missing is not None else (None, None, 'sem base', '')
            a, b, basis, origin = cost
            estimates.append(dict(fornecedor=supplier, linha=code, quantidade_faltante=missing,
                categoria=basis, minimo=a, maximo=b, origem=origin, motivo='lacuna/substituição/quantidade; não é desconto'))
            if a is None:
                unknown.append(code)
            elif low is not None:
                low, high = low + a, high + b
        for name in ['frete', 'impostos']:
            included = value(fields, name + '_incluso' if name == 'frete' else 'impostos_inclusos')
            amount = number(value(fields, name))
            if included == 'nao' and amount is not None:
                if low is not None:
                    low, high = low + amount, high + amount
                estimates.append(dict(fornecedor=supplier, linha=name, quantidade_faltante='', categoria='declarado', minimo=amount, maximo=amount, origem=fields[name]['origem'], motivo='fora do total declarado'))
            elif included not in {'sim', 'nao'} or (included == 'nao' and amount is None):
                unknown.append(name)
        risks = []
        for name in META:
            if value(fields, name) in (None, ''):
                risks.append(name + ' ausente')
        for name in ['fabricacao', 'entrega', 'montagem', 'medicao_in_loco', 'retirada']:
            if value(fields, name) != 'sim':
                unknown.append(name)
                ask(name, 'O total inclui ' + name.replace('_', ' ') + '? Informar preço separado e condições.')
        expiry = value(fields, 'validade')
        if expiry and date.fromisoformat(expiry) < as_of:
            risks.append('validade vencida')
        signal = number(value(fields, 'sinal_percentual'))
        if signal is not None and signal > 100:
            raise ValueError('Sinal deve estar entre 0 e 100')
        if signal is not None and signal > 30:
            risks.append('sinal acima da hipótese de triagem 30%; avaliar pagamento/multa')
        guarantee = number(value(fields, 'garantia_meses'))
        if guarantee is not None and guarantee < 12:
            risks.append('garantia abaixo da hipótese de triagem 12 meses; conferir cobertura')
        end, timing = schedule(fields)
        ask('condicoes', 'Confirmar reajuste após medição, validade, sinal/saldo, multa, garantia e exclusões. Premissa: medidas reais após chaves; quais linhas têm preço firme?')
        ask('cronograma', 'Qual início relativo às chaves, duração de produção, entrega e montagem, calendário útil/corrido e gatilho contratual? ' + timing)
        full = declared is not None and not unknown
        summary.append(dict(fornecedor=supplier, escopo=value(fields, 'escopo'), declarado=declared,
            parcial_equivalente_min=low, parcial_equivalente_max=high,
            equivalente_min=low if full else None, equivalente_max=high if full else None,
            delta_meta35mil_min=low - 35000 if low is not None else None,
            delta_meta35mil_max=high - 35000 if high is not None else None,
            delta_provisao46500_min=low - 46500 if low is not None else None,
            delta_provisao46500_max=high - 46500 if high is not None else None,
            folga_meta35mil=35000 - high if full else None,
            execucao_R44_cenario_min=Decimal('137748.11') - 46500 + low if full and value(fields, 'escopo') == 'integral' else None,
            execucao_R44_cenario_max=Decimal('137748.11') - 46500 + high if full and value(fields, 'escopo') == 'integral' else None,
            cobertura_pct=round(100 * covered / len(refs), 2), substituicoes=substitutions,
            sem_base=' | '.join(unknown), riscos=' | '.join(risks), fim_semana=end, prazo=timing,
            garantia_meses=guarantee, risco_reajuste=value(fields, 'risco_reajuste'),
            decisao='PENDENTE de Elias', pontuacao=None))
    # Escopos diferentes e custos incompletos não recebem posição numérica enganosa.
    for row in summary:
        peers = [r for r in summary if r['escopo'] == row['escopo'] and r['equivalente_max'] is not None]
        if row['equivalente_max'] is None or row['garantia_meses'] is None or row['fim_semana'] is None or row['risco_reajuste'] not in {'baixo', 'medio', 'alto'}:
            continue
        price = min(r['equivalente_max'] for r in peers)
        scores = dict(preco=float(price / row['equivalente_max']) * 100 if row['equivalente_max'] else 100,
            cobertura=row['cobertura_pct'], reajuste={'baixo': 100, 'medio': 50, 'alto': 0}[row['risco_reajuste']],
            prazo=100 if row['fim_semana'] <= 8 else 50 if row['fim_semana'] <= 12 else 0,
            garantia=min(float(row['garantia_meses']) / 12, 1) * 100,
            substituicoes=max(0, 100 - row['substituicoes'] * 20))
        row['pontuacao'] = round(sum(scores[k] * float(weights[k]) for k in weights) / sum(float(w) for w in weights.values()), 2)
        row['criterios'] = scores
    return dict(resumo=summary, matriz=matrix, custos=estimates, perguntas=questions, pesos=weights)


def templates(dest):
    dest.mkdir(parents=True, exist_ok=True)
    refs = references()
    rows = [dict(fornecedor='', linha='', campo=f, valor='', unidade='', origem='') for f in META]
    rows += [dict(fornecedor='', linha=code, campo=f, valor='', unidade=ref['unidade'] if f == 'quantidade' else '', origem='')
             for code, ref in {**refs, **gaps()}.items() for f in LINE]
    write_csv(dest / 'Modelo_entrada.csv', rows, CSV_FIELDS)
    write_csv(dest / 'Linhas_referencia.csv', [dict(linha=code, **r) for code, r in {**refs, **gaps()}.items()], ['linha', 'grupo', 'item', 'movel', 'padrao', 'espessura_mm', 'formato', 'quantidade', 'unidade', 'quantidade_com_perda', 'base', 'fonte', 'observacao'])
    dump(dest / 'Modelo_entrada.json', dict(propostas=[], instrucao='Preencher CSV ou JSON com campos {valor, unidade, origem}; nenhum dado real.'))
    dump(dest / 'Pesos.json', WEIGHTS)
    write_csv(dest / 'Matriz_cobertura_modelo.csv', [dict(linha=code, grupo=r['grupo'], item=r['item'], quantidade_referencia=r.get('quantidade_com_perda') or r['quantidade'], cobertura='', fornecedor='') for code, r in {**refs, **gaps()}.items()], ['fornecedor', 'linha', 'grupo', 'item', 'quantidade_referencia', 'cobertura'])
    write_csv(dest / 'Perguntas_modelo.csv', [], ['fornecedor', 'numero', 'linha', 'pergunta'])


def inventory(folder, output):
    folder.mkdir(parents=True, exist_ok=True)
    files = [p for p in sorted(folder.rglob('*')) if p.is_file()]
    rows = [dict(arquivo=str(p.relative_to(folder)), bytes=p.stat().st_size, sha256=sha(p),
                 estado='leitura/extração e anonimização pendentes; OCR não executado') for p in files]
    dump(output / 'Inventario_propostas.json', dict(arquivos=rows, propostas_reais_comparadas=0,
         aviso='Brutos e correspondência Fxx ficam fora do git; normalização exige conferência humana.'))
    return rows


def run(args):
    output = args.saida.resolve()
    if output == ROOT or ROOT in output.parents:
        raise ValueError('Resultados de propostas devem ficar fora do repositório público')
    output.mkdir(parents=True, exist_ok=True)
    inv = inventory(args.recebidas, output)
    if args.modelos:
        templates(args.modelos)
    proposals = load_proposals(args.entrada)
    weights = json.loads(args.pesos.read_text(encoding='utf-8')) if args.pesos else WEIGHTS
    if set(weights) != set(WEIGHTS) or any(number(v) is None for v in weights.values()) or sum(number(v) for v in weights.values()) <= 0:
        raise ValueError('Pesos inválidos')
    dependencies = read_csv(args.dependencias) if args.dependencias else []
    result = compare(proposals, date.fromisoformat(args.data), weights, dependencies)
    dump(output / 'Propostas_normalizadas.json', dict(propostas=proposals))
    result['fontes_sha256'] = {p: sha(ROOT / p) for p in [REF, CUT + 'Custos_chapas.csv', CUT + 'Resumo_chapas.csv',
        CUT + 'Custos_cenarios.csv', CUT + 'Custos_propostas.csv', CUT + 'Fita_custo_hipotese.csv',
        '05_Orcamento_e_cronograma/Orcamento/Orcamento_R43.md', '05_Orcamento_e_cronograma/Cronograma_obra_e_compras.md']}
    if args.entrada:
        result['entrada_sha256'] = sha(args.entrada)
    if args.dependencias:
        result['dependencias_sha256'] = sha(args.dependencias)
    result['data_comparacao'] = args.data
    result['inventario_arquivos'] = len(inv)
    dump(output / 'Comparacao.json', result)
    write_csv(output / 'Matriz_cobertura.csv', result['matriz'], ['fornecedor', 'linha', 'grupo', 'item', 'movel', 'quantidade_referencia', 'quantidade_proposta', 'cobertura', 'substituicao', 'lacuna_resposta', 'premissa_medida_in_loco', 'chapas_cenario1850', 'limite_inferior1850', 'ressalva_cenario1850', 'alertas', 'origem'])
    write_csv(output / 'Perguntas.csv', result['perguntas'], ['fornecedor', 'numero', 'linha', 'pergunta'])
    write_csv(output / 'Custos_equivalentes.csv', result['custos'], ['fornecedor', 'linha', 'quantidade_faltante', 'categoria', 'minimo', 'maximo', 'origem', 'motivo'])
    write_csv(output / 'Ranking_condicional.csv', result['resumo'], list(result['resumo'][0]) if result['resumo'] else ['fornecedor', 'declarado', 'equivalente_min', 'equivalente_max', 'pontuacao', 'decisao'])
    report = ['# Comparador de cotações', '', f"Data de referência: {args.data}. Propostas normalizadas: {len(proposals)}.",
        'Decisão PENDENTE de Elias. Nenhuma proposta real foi comparada.' if not proposals else 'Conferir as origens antes de usar. Não há seleção automática.',
        '', 'Parcial equivalente não é custo completo. Sem base impede total equivalente e ranking; vazio não é zero.',
        'A matriz inclui 101 linhas, 33 lacunas de corte, 40 de ferragens e P19; 23 lacunas de fita já estão nas 101.',
        'Referências sobrepostas de painéis/chapas e linhas de comparação não se somam.',
        '14 chapas do misto (8 de 1850 + 6 de 2100) não têm o mesmo escopo de 15 em 1850: Peca208 não cabe.',
        'Fita: 191,136 m; 210,2496 m com perda; confirmar regra, SKU e largura. Parciais de cenários não são custo de escopo completo.',
        'A meta histórica 35 mil não substitui D05-C (pacote 37 mil condicionado). O arquivo Orcamento_R43.md contém a base R44 137.748,11 e provisão 46.500.',
        'Prazo: alvo obra semana 8, mudança até 12; cabimento da cadeia do fornecedor não comprova ocupação.', '',
        '| Código | Declarado | Parcial mínimo | Parcial máximo | Pontuação | Decisão |', '|---|---:|---:|---:|---:|---|']
    report += [f"| {r['fornecedor']} | {r['declarado']} | {r['parcial_equivalente_min']} | {r['parcial_equivalente_max']} | {r['pontuacao']} | PENDENTE |" for r in result['resumo']]
    (output / 'Relatorio_cotacoes.md').write_text('\n'.join(report) + '\n', encoding='utf-8')
    print(json.dumps(dict(propostas=len(proposals), arquivos_recebidos=len(inv), matriz=len(result['matriz']), sha256=sha(output / 'Comparacao.json')), ensure_ascii=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--entrada', type=Path)
    parser.add_argument('--recebidas', type=Path, default=RAW)
    parser.add_argument('--saida', type=Path, default=OUT)
    parser.add_argument('--modelos', type=Path)
    parser.add_argument('--dependencias', type=Path)
    parser.add_argument('--pesos', type=Path)
    parser.add_argument('--data', default=date.today().isoformat(), help='Data explícita recomendada, YYYY-MM-DD')
    try:
        run(parser.parse_args())
    except (ValueError, KeyError) as error:
        parser.exit(2, str(error) + '\n')
