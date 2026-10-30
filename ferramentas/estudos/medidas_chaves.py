"""Campo → diferenças/impactos externos, sem escrever CAD, orçamento ou plano de corte."""
import argparse
import copy
from datetime import datetime
import fnmatch
import importlib.util
import json
import math
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
import comparador_cotacoes as cot

ROOT, OUT = cot.ROOT, cot.OUT
HERE = Path(__file__).resolve().parent
MODEL = HERE / 'modelos'
SOURCE = '07_Imovel/Medidas_e_impactos.csv'
DEPS = '04_Moveis/Dependencias/'
FIELDS = ['codigo_medida', 'descricao', 'valor_nominal', 'unidade', 'valor_medido', 'data_hora', 'foto/arquivo', 'obs']
NOTICE = 'hipótese de trabalho — a confirmar com RT/oficina'
ROOMS = {'QUA': 'Quarto', 'COZ': 'Cozinha', 'LAV': 'Lavanderia', 'ESC': 'Escritório',
         'BAN': 'Banheiro', 'SAL': 'Sala/jantar', 'CIR': 'Circulação'}


def room_names(text):
    aliases = {cot.key(v): v for v in ROOMS.values()}
    aliases.update(banho='Banheiro', sala='Sala/jantar')
    parts = [text] if cot.key(text) == 'sala/jantar' else re.split(r'[|/]', text)
    return [aliases.get(cot.key(p), p) for p in parts]


def chain():
    spec = importlib.util.spec_from_file_location('cadeia_chaves', ROOT / (DEPS + 'orquestrar.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def catalog():
    rows = cot.read_csv(ROOT / SOURCE, ',')
    result = {r['codigo_medida']: r for r in rows}
    doc = json.loads((ROOT / (DEPS + 'regras.json')).read_text(encoding='utf-8'))
    for code, room in ROOMS.items():
        for kind in ['ESQUADRO', 'PISO']:
            result[f'CAMPO-{code}-{kind}'] = dict(codigo_medida=f'CAMPO-{code}-{kind}', ambiente=room,
                medida_ou_verificacao='Desvio absoluto de 90° no canto' if kind == 'ESQUADRO' else 'Elevação do piso desde a referência (não descontar duas vezes do pé-direito)',
                valor_nominal_atual='0 grau' if kind == 'ESQUADRO' else '0 mm', valor_medido='',
                natureza_do_valor='referência geométrica, não medição', moveis_afetados='|'.join(n for n, v in doc['alvos'].items() if v['room'] == {'Banheiro': 'banho', 'Sala/jantar': 'sala', 'Escritório': 'escritorio', 'Circulação': 'circulacao'}.get(room, room.lower()) and re.fullmatch(r'P\d{2}', n)),
                fonte_nominal=DEPS + 'orquestrar.py', quem_valida='RT/oficina', impacto='Conferir intrusão no canto/nível de apoio; não redimensiona caixas.')
    ranking = cot.read_csv(ROOT / (DEPS + 'Ranking_15.csv'))
    for row in ranking:
        code = row['codigo_medida']
        if code not in result:
            affected = '|'.join(re.findall(r'\bP\d{2}\b', row['modulos']))
            names = sorted({doc['alvos'][m]['room'] for m in affected.split('|') if m in doc['alvos']})
            result[code] = dict(codigo_medida=code, ambiente='/'.join(names) or 'Datum',
                medida_ou_verificacao=row['descricao_fisica'] + ' Parâmetro derivado: deslocamento normal assinado/ângulo; exige datum, não é leitura absoluta do laser.',
                valor_nominal_atual='0 grau' if code.endswith('ANGULO') else '0 mm', valor_medido='',
                natureza_do_valor='parâmetro nominal; vínculo físico pendente', moveis_afetados=affected,
                fonte_nominal=DEPS + 'Ranking_15.csv', quem_valida='levantamento e RT', impacto='Reconstrução de reta exige marcos comuns documentados.')
    result['BOX-VERDE'] = dict(codigo_medida='BOX-VERDE', ambiente='Banheiro',
        medida_ou_verificacao='Largura x altura da parede verde do chuveiro; código legado, identificar a parede na foto',
        valor_nominal_atual='800 x 2250 mm', valor_medido='', natureza_do_valor='referência gráfica conflitante com orçamento 1240 x 2470 mm',
        moveis_afetados='P18|P19', fonte_nominal='03_Ambientes/Acabamentos/README.md',
        quem_valida='RT/oficina', impacto='Rever paginação, área e compra; não escolher parede/altura pelo cálculo.')
    result['BOX-VERDE-JANELA'] = dict(codigo_medida='BOX-VERDE-JANELA', ambiente='Banheiro',
        medida_ou_verificacao='Largura x altura da parede verde da janela; registrar abertura separadamente',
        valor_nominal_atual='800 x 2470 mm', valor_medido='',
        natureza_do_valor='hipótese do orçamento adicional, sem descontar janela; não é medida real',
        moveis_afetados='P18|P19', fonte_nominal='05_Orcamento_e_cronograma/Orcamento/Pisos_e_revestimentos/Analise_pisos.md',
        quem_valida='RT/oficina', impacto='Conferir área, abertura e paginação das duas paredes; não altera orçamento automaticamente.')
    # Preserva exatamente os 15 itens do roteiro vigente; demais registros são complemento.
    order = [r['codigo_medida'] for r in ranking]
    for row in result.values():
        row['ambiente'] = '|'.join(room_names(row['ambiente']))
    return {code: result[code] for code in order + [c for c in result if c not in order]}


def unit(row):
    code, nominal = row['codigo_medida'], row.get('valor_nominal_atual', '')
    if code.endswith(('ANGULO', 'ESQUADRO')):
        return 'grau'
    if code.startswith(('DIM-', 'BOX-VERDE')) or re.fullmatch(r'\s*-?\d+(?:[.,]\d+)?\s*(?:mm|cm|m)\s*', nominal) or code.startswith(('PR-', 'PAREDE-', 'CAMPO-')) or code == 'DEP-COZ-PRUMO':
        return 'mm'
    return 'texto'


def nominal_values(row, engine):
    if unit(row) == 'texto':
        return None
    if unit(row) == 'grau':
        return [0.0]
    code = row['codigo_medida']
    try:
        if code.startswith(('DIM-', 'BOX-VERDE')):
            count = 2 if code.startswith('BOX-VERDE') or code in {'DIM-01', 'DIM-02', 'DIM-05', 'DIM-06', 'DIM-07', 'DIM-08', 'BOX-VERDE'} else 1
            return [engine.dimensional.resolver({code: row}, code + '/' + str(i)).mm for i in range(count)]
        val = engine.dimensional.resolver({code: row}, code).mm
        return None if val is None else [val]
    except (ValueError, KeyError):
        return None


def parse_measured(row, incoming, engine):
    code = row['codigo_medida']
    text = incoming.get('valor_medido', '').strip()
    expected = unit(row)
    supplied = incoming.get('unidade', expected).strip()
    if expected == 'texto':
        if supplied != 'texto':
            raise ValueError(code + ': unidade deve ser texto; separar medições numéricas nos códigos próprios')
        return (text or None), text
    allowed = {'mm', 'cm', 'm'} if expected == 'mm' else {'grau', 'graus', 'deg', '°'}
    if supplied not in allowed:
        raise ValueError(code + ': unidade incompatível: ' + supplied)
    if not text:
        return None, ''
    if not re.search(r'(?:mm|cm|m|grau|graus|deg|°)\s*$', text):
        text += ' ' + supplied
    if expected == 'grau':
        match = re.fullmatch(r'\s*(-?\d+(?:[.,]\d+)?)\s*(grau|graus|deg|°)\s*', text)
        if not match:
            raise ValueError(code + ': ângulo inválido')
        val = float(match[1].replace(',', '.'))
        if not math.isfinite(val) or (code.endswith('ESQUADRO') and (val < 0 or val >= 45)):
            raise ValueError(code + ': desvio angular inválido')
        return [val], f'{val} grau'
    # Unidade na célula deve concordar com a coluna para evitar troca silenciosa.
    units_in_cell = re.findall(r'mm|cm|(?<![a-z])m(?![a-z])', text)
    if units_in_cell and any(u != supplied for u in units_in_cell):
        raise ValueError(code + ': unidade na célula difere da coluna')
    working = dict(row, valor_medido=text)
    if code.startswith(('DIM-', 'BOX-VERDE')):
        count = 2 if code.startswith('BOX-VERDE') or code in {'DIM-01', 'DIM-02', 'DIM-05', 'DIM-06', 'DIM-07', 'DIM-08', 'BOX-VERDE'} else 1
        if len(re.findall(r'-?\d+(?:[.,]\d+)?', text)) != count:
            raise ValueError(code + ': informar todos os eixos, separados por x')
        values = [engine.dimensional.resolver({code: working}, code + '/' + str(i)).mm for i in range(count)]
    else:
        values = [engine.dimensional.resolver({code: working}, code).mm]
    if any(v is None or not math.isfinite(v) for v in values):
        raise ValueError(code + ': valor não finito')
    if code.startswith(('PD-', 'DIM-')) and min(values) <= 0:
        raise ValueError(code + ': dimensão deve ser positiva')
    if code.endswith('-PISO') and values[0] < 0:
        raise ValueError(code + ': elevação do piso não negativa')
    return values, ' x '.join(f'{v:g}' for v in values) + ' mm'


def hypothesis():
    rows = []
    for pattern, units, ok, attention in [('PD-*', 'mm', 0, 5), ('DIM-*', 'mm', 2, 5),
        ('PR-*', 'mm', 2, 5), ('PAREDE-*-DESLOCAMENTO', 'mm', 2, 5),
        ('PAREDE-*-ANGULO', 'grau', .1, .3), ('CAMPO-*-ESQUADRO', 'grau', .1, .3),
        ('CAMPO-*-PISO', 'mm', 1, 3), ('DEP-COZ-PRUMO', 'mm', 1, 3)]:
        rows.append(dict(codigo_medida=pattern, unidade=units, ok_ate=ok, atencao_ate=attention,
            natureza=NOTICE, fonte='referência usual, não verificada; sem norma invocada', quem_confirma='RT/oficina'))
    return rows


def thresholds(path, mode):
    if mode == 'bruto':
        return []
    rows = cot.read_csv(path) if path else hypothesis()
    seen = set()
    for row in rows:
        pattern = row['codigo_medida']
        if pattern in seen or row['unidade'] not in {'mm', 'grau'} or not row.get('fonte') or not row.get('natureza'):
            raise ValueError('Tabela de tolerâncias inválida: ' + pattern)
        seen.add(pattern)
        a, b = cot.number(row['ok_ate']), cot.number(row['atencao_ate'])
        if a is None or b is None or a > b:
            raise ValueError('Limites de tolerância inválidos: ' + pattern)
    return rows


def classify(code, values, nominal, table):
    if values is None:
        return 'sem medida', None, 'valor vazio ≠ zero'
    if isinstance(values, str) or nominal is None or any(v is None for v in nominal):
        return 'atenção', None, 'sem nominal numérico; registro exige validação'
    delta = [round(a - b, 6) for a, b in zip(values, nominal)]
    candidates = [r for r in table if fnmatch.fnmatchcase(code, r['codigo_medida'])]
    exact = [r for r in candidates if r['codigo_medida'] == code]
    rule = (exact or candidates or [None])[0]
    if rule is None:
        return 'sem tolerância', delta, 'só diferença bruta; tolerância não informada'
    biggest = max(abs(d) for d in delta)
    status = 'ok' if biggest <= float(cot.number(rule['ok_ate'])) else 'atenção' if biggest <= float(cot.number(rule['atencao_ate'])) else 'revisar'
    return status, delta, rule['natureza'] + '; ' + rule['fonte']


def furniture(row, doc):
    code = row['codigo_medida']
    explicit = row.get('moveis_afetados', '')
    result = set(re.findall(r'\bP\d{2}\b', explicit))
    if cot.key(explicit) == 'todos':
        result.update(f'P{i:02}' for i in range(1, 21))
    for rule in doc['regras']:
        if any(c.partition('/')[0] == code for c in rule['medidas']) and re.fullmatch(r'P\d{2}', rule['movel']):
            result.add(rule['movel'])
    return sorted(result)


def quote_dependencies(rows, doc):
    refs = cot.references()
    # Origem do vínculo para agregados de chapas, fita e ferragens, sem rateio de preço.
    panels = [r for r in cot.read_csv(ROOT / (cot.CUT + 'Lista_de_corte.csv')) if r['variante'] == 'base']
    tape = cot.read_csv(ROOT / '04_Moveis/Furacao/Fita_por_peca.csv')
    hardware = cot.read_csv(ROOT / '04_Moveis/Furacao/Ferragens_por_movel.csv')
    line_modules = {}
    for line, ref in refs.items():
        mods = set(re.findall(r'\bP\d{2}\b', ref['movel']))
        if ref['grupo'] == 'chapas':
            mods.update(r['movel'] for r in panels if r['padrao'] == ref['padrao'] and cot.number(r['espessura_mm']) == cot.number(ref['espessura_mm']))
        elif ref['grupo'] == 'fita':
            mods.update(r['movel'] for r in tape if r['cor'] == ref['padrao'] and cot.number(r['espessura_fita_mm']) == cot.number(ref['espessura_mm']))
        elif ref['grupo'] == 'ferragens':
            mods.update(r['movel'] for r in hardware if cot.key(r['familia']) == cot.key(ref['item']) or cot.key(r['item']) == cot.key(ref['item']))
        if not mods and ref['grupo'] in {'chapas', 'fita', 'ferragens', 'limite', 'comparacao_nao_somar'}:
            mods.update(f'P{i:02}' for i in range(1, 21))
            basis = 'agregado sem vínculo individual suficiente; precaução, não rateio'
        else:
            basis = 'móvel explícito ou inventário de painéis/fita/ferragens'
        line_modules[line] = (mods, basis)
    result = []
    for code, row in rows.items():
        if code.startswith(('LOG-', 'POS-')):
            continue
        affected = set(furniture(row, doc))
        for line, (mods, basis) in line_modules.items():
            common = sorted(affected & mods)
            if common:
                result.append(dict(linha=line, codigo_medida=code, moveis='|'.join(common),
                    premissa='medida in loco; preço firme a confirmar', vinculo=basis, fonte=SOURCE + ' + ' + DEPS + 'regras.json'))
    return result


def generate_models(dest=MODEL):
    engine = chain()
    rows = catalog()
    dest.mkdir(parents=True, exist_ok=True)
    model = [dict(codigo_medida=code, descricao=r['medida_ou_verificacao'],
        valor_nominal=r.get('valor_nominal_atual', ''), unidade=unit(r), valor_medido='', data_hora='', **{'foto/arquivo': ''}, obs='') for code, r in rows.items()]
    cot.write_csv(dest / 'medidas_reais_modelo.csv', model, FIELDS)
    cot.write_csv(dest / 'Tolerancias_trabalho.csv', hypothesis(), list(hypothesis()[0]))
    return rows, engine


def read_input(path, rows, engine):
    with path.open(encoding='utf-8-sig') as stream:
        first = stream.readline()
    data = cot.read_csv(path, ';' if ';' in first else ',')
    seen, measured = set(), {}
    for incoming in data:
        code = incoming['codigo_medida']
        if code not in rows or code in seen:
            raise ValueError('Código desconhecido/duplicado: ' + code)
        seen.add(code)
        values, normalized = parse_measured(rows[code], incoming, engine)
        stamp = incoming.get('data_hora', '')
        if stamp:
            datetime.fromisoformat(stamp)
        measured[code] = dict(valores=values, normalizado=normalized,
            data_hora=stamp, evidencia=incoming.get('foto/arquivo', ''), obs=incoming.get('obs', ''))
    return measured


def impacts(rows, measured, table, engine, datum=None):
    doc = engine.document()
    known = set(engine.dimensional.entradas())
    working = copy.deepcopy({k: v for k, v in rows.items() if k in known})
    physical = {r['codigo_medida']: r for r in cot.read_csv(ROOT / (DEPS + 'Descricao_fisica.csv'))}
    aux, numeric, results = {}, set(), []
    for code, row in rows.items():
        reading = measured.get(code, dict(valores=None, normalizado='', data_hora='', evidencia='', obs=''))
        nominal = nominal_values(row, engine)
        if any(r['unidade'] != unit(row) for r in table if fnmatch.fnmatchcase(code, r['codigo_medida'])):
            raise ValueError(code + ': unidade da tolerância incompatível com a medida')
        status, delta, basis = classify(code, reading['valores'], nominal, table)
        descriptor = physical.get(code, {}).get('situacao', '')
        unanchored = code.startswith(('PR-', 'PAREDE-')) and not datum
        if reading['valores'] is not None and (unanchored or 'pendente' in descriptor):
            if status not in {'revisar', 'sem tolerância'}:
                status = 'atenção'
            basis += '; datum/descrição física pendente, não demonstra conformidade'
        if code == 'BOX-VERDE' and reading['valores'] is not None:
            status, basis = 'revisar', basis + '; duas bases documentais diferentes: confirmar parede/altura antes da compra'
        if isinstance(reading['valores'], list):
            if code in working and not unanchored:
                working[code]['valor_medido'] = reading['normalizado']
                numeric.add(code)
            elif code.startswith(('CAMPO-', 'PAREDE-')) and not unanchored:
                aux[code] = reading['valores'][0]
        affected = furniture(row, doc)
        files = set(filter(None, row.get('arquivos_ficha', '').split('|')))
        files.discard('não se aplica')
        files.update('06_Entregas/Fichas_fabricacao/' + m + '.html' for m in affected)
        boards = set(filter(None, row.get('arquivos_prancha', '').split('|')))
        boards.discard('não se aplica')
        for rule in doc['regras']:
            if any(c.partition('/')[0] == code for c in rule['medidas']):
                boards.update(rule['pranchas'])
        results.append(dict(codigo_medida=code, ambiente=row['ambiente'], nominal=nominal, medido=reading['valores'],
            delta=delta, unidade=unit(row), classificacao=status, criterio=basis,
            moveis='|'.join(affected), fichas='|'.join(sorted(files)), pranchas='|'.join(sorted(boards)),
            impacto=row.get('impacto', 'Revisar referências/folgas com RT/oficina'), quem_valida=row.get('quem_valida', 'RT/oficina'),
            fonte=row.get('fonte_nominal', SOURCE), data_hora=reading['data_hora'], evidencia=reading['evidencia'], obs=reading['obs']))
        results[-1]['efeito_quantidade'] = ''
        if isinstance(reading['valores'], list) and len(reading['valores']) == 2:
            area = reading['valores'][0] * reading['valores'][1] / 1e6
            results[-1]['efeito_quantidade'] = f'Retângulo medido: {area:.6f} m²; não inclui recortes/paginação/perdas, rever compra.'
        if code == 'BOX-VERDE' and isinstance(reading['valores'], list):
            results[-1]['criterio'] += '; delta vs orçamento 1240×2470 mm: ' + str([reading['valores'][0] - 1240, reading['valores'][1] - 2470])
            results[-1]['efeito_quantidade'] += f' Delta vs gráfico 1,80 m²: {area - 1.8:.6f} m²; vs orçamento 3,0628 m²: {area - 3.0628:.6f} m². Não desconta compra automaticamente.'
        if code == 'BOX-VERDE-JANELA' and isinstance(reading['valores'], list):
            results[-1]['efeito_quantidade'] += f' Delta vs hipótese adicional 1,976 m²: {area - 1.976:.6f} m²; janela ainda não descontada. Não altera compra.'
    # Reutiliza o motor vigente. Valores não medidos continuam nominal, explicitamente.
    evaluated = engine.evaluate(working, doc, aux)
    selected = []
    for record in evaluated['resultados']:
        parents = {c.partition('/')[0] for c in record['medidas']}
        room = doc['alvos'][record['movel']]['room']
        aux_for_room = [c for c in aux if c.startswith('PAREDE-') or engine.AUX.get(c, {}).get('room') == room]
        if not (parents & numeric or aux_for_room):
            continue
        record['nao_medidas'] = '|'.join(sorted(parents - numeric))
        record['estado_geometrico'] = record.pop('status')
        if record['estado_geometrico'] == 'OK':
            record['estado_geometrico'] = 'sem conflito neste cenário; não valida tolerância'
        selected.append(record)
    conflict_modules = {r['movel'] for r in selected if r['estado_geometrico'] == 'NÃO CABE'}
    for row in results:
        if row['medido'] is not None and conflict_modules & set(row['moveis'].split('|')):
            row['classificacao'] = 'revisar'
            row['criterio'] += '; conflito geométrico no cenário, inclusive bases nominais'
    return results, selected, evaluated.get('menor_folga_paredes_medidas_mm', {})


def warnings():
    return [
        dict(codigo='DIM-06', destino='RT/oficina', pergunta='Conferir o eixo de 1540 mm da lavanderia versus 1610 mm do desenho histórico; identificar faces e espessuras acabadas.', fonte='07_Imovel/README.md'),
        dict(codigo='COMP-03', destino='RT/oficina', pergunta='Qual parede verde e altura do box: 0,80×2,25 m do site ou 1,24×2,47 m do orçamento? Teto nominal atual 2,50 m; não adotar cenário antigo. Medir ambas as faces e decidir paginação antes da compra.', fonte='03_Ambientes/Acabamentos/README.md'),
        dict(codigo='COMP-04', destino='construtora/oficina', pergunta='Qual largura real da folha/vão, eixo, maçaneta e giro? Não há largura documental de porta; fotos não são cota.', fonte='07_Imovel/Checklist_vistoria_dia_das_chaves.md'),
        dict(codigo='PD-*', destino='RT/oficina', pergunta='Qual altura livre mínima acabada e desnível nos encontros até o teto? Qual detalhe de arremate sem aumentar caixas automaticamente?', fonte='04_Moveis/Dependencias/README.md'),
        dict(codigo='CAMPO-*-ESQUADRO', destino='RT/oficina', pergunta='Qual desvio absoluto de 90° e prumo em cada canto? Definir calços/folgas/ancoragem com faces identificadas.', fonte=DEPS + 'orquestrar.py'),
        dict(codigo='SAL-COND', destino='RT/construtora', pergunta='O ponto de TV e conduíte entrada–painel existem e permitem a ligação? Identificar neutro, retornos e caixa; não assumir infraestrutura.', fonte='07_Imovel/README.md'),
        dict(codigo='COMP-06', destino='RT/construtora', pergunta='As tampas cegas do quadro escondem posições úteis? Conferir circuitos, proteção e capacidade; tampas não demonstram disponibilidade elétrica.', fonte='07_Imovel/Complemento/Complemento_da_visita_R02.md'),
        dict(codigo='GER-ID', destino='RT/condomínio', pergunta='Quais marcos M0/M1/E1/E2 e vínculo ao datum nominal, documentação como construído e restrições para reforma? Registrar antes de converter coordenadas.', fonte=DEPS + 'README.md')]


def reports(output, results, geometry, pieces, questions, table, dependency_count):
    counts, rooms = {}, {}
    priority = {'ok': 0, 'sem medida': 1, 'sem tolerância': 2, 'atenção': 3, 'revisar': 4}
    for row in results:
        status = row['classificacao']
        counts[status] = counts.get(status, 0) + 1
        for name in room_names(row['ambiente']):
            room = rooms.setdefault(name, dict(status='ok', medidos=0, faltantes=0))
            if priority[status] > priority[room['status']]:
                room['status'] = status
            room['faltantes' if row['medido'] is None else 'medidos'] += 1
    header = ['# Medidas do dia das chaves', '',
        'Triagem documental; tolerâncias de trabalho são hipóteses, a confirmar com RT/oficina. Nenhuma fonte vigente foi alterada.',
        'Sem tolerância nunca significa ok. Ok numérico não confirma datum, substrato, ligação, infraestrutura ou fabricação.',
        'Os 15 primeiros códigos seguem a folha prioritária vigente; os demais complementam o índice de campo. Não há roteiro espacial completo documentado.',
        '', '| Ambiente | Semáforo | Medidos | Sem medida |', '|---|---|---:|---:|']
    header += [f"| {room} | {r['status']} | {r['medidos']} | {r['faltantes']} |" for room, r in rooms.items()]
    changes = [r for r in results if r['medido'] is not None]
    details = ['', '## O que muda', '',
        f'Marcenaria: {len(geometry)} relações afetadas recalculadas pelo motor existente. {len(pieces)} painéis listados para revisão de corte; dimensões mantidas, sem vínculo executivo por eixo/peça.',
        f'Compra: {dependency_count} vínculos linha×medida em Linhas_dependentes_medidas.csv; preço firme depende de confirmar medidas e escopo.',
        'Obra: ancoragens, substrato, instalações, pisos, box e documentação requerem RT/construtora/condomínio conforme Perguntas_RT.csv.',
        'Folgas em Impactos_geometria.json são do cenário: combinam medidas informadas e bases nominais identificadas. Não comprovam folga mínima real integral.',
        '', '| Código | Delta | Estado | Móveis |', '|---|---|---|---|']
    details += [f"| {r['codigo_medida']} | {r['delta']} {r['unidade']} | {r['classificacao']} | {r['moveis']} |" for r in changes]
    details += ['', *[r['codigo_medida'] + ': ' + r['efeito_quantidade'] for r in changes if r['efeito_quantidade']]]
    missing = [r['codigo_medida'] for r in results if r['medido'] is None]
    full = header + details + ['', '## Perguntas pendentes', ''] + [f"- {q['codigo']} / {q['destino']}: {q['pergunta']}" for q in questions]
    full += ['', f'## Sem medida ({len(missing)})', '', ', '.join(missing), '', 'Detalhes, fichas, pranchas, origens e evidências: Impactos_medidas.csv. Tolerâncias usadas: Tolerancias_usadas.csv.']
    (output / 'Relatorio_medidas.md').write_text('\n'.join(full) + '\n', encoding='utf-8')
    # Uma linha por ambiente, sem duplicar capitalizações da base histórica.
    phone = ['# Chaves — consulta rápida', '', f"Medidos: {len(changes)}. Sem medida: {len(missing)}. Revisar: {counts.get('revisar', 0)}.",
        'Tolerâncias são hipóteses; sem tolerância não é ok. Nenhuma alteração automática.', '']
    phone += [f"- {room}: {r['status']} ({r['faltantes']} sem medida)" for room, r in rooms.items()]
    phone += ['', 'Prioridades: conferir lavanderia 1540/1610; box/forro; porta; teto; cantos; TV/conduíte; quadro; datum.',
        f'Marcenaria: {len(geometry)} relações afetadas; reabrir os cortes indicados em Pecas_afetadas.csv.',
        'Compra: confirmar preços condicionados em Linhas_dependentes_medidas.csv.', 'RT/construtora/condomínio: perguntas em Perguntas_RT.csv.',
        'Pendências e outros ambientes: Relatorio_medidas.md / Impactos_medidas.csv.']
    (output / 'Relatorio_medidas_celular.md').write_text('\n'.join(phone) + '\n', encoding='utf-8')
    return counts


def run(args):
    output = args.saida.resolve()
    if output == ROOT or ROOT in output.parents:
        raise ValueError('Saída deve ficar fora do repositório público')
    output.mkdir(parents=True, exist_ok=True)
    rows, engine = generate_models() if args.gerar_modelo else (catalog(), chain())
    if args.gerar_modelo:
        (output / 'medidas_reais_modelo.csv').write_bytes((MODEL / 'medidas_reais_modelo.csv').read_bytes())
    measured = read_input(args.entrada, rows, engine) if args.entrada else {}
    if args.datum and not args.datum.is_file():
        raise ValueError('Arquivo de referência do datum não existe')
    table = thresholds(args.tolerancias, args.modo)
    # Uma tabela própria substitui a hipótese inteira, sem fallback para códigos omitidos.
    results, geometry, wall_gaps = impacts(rows, measured, table, engine, args.datum)
    doc = engine.document()
    dependencies = quote_dependencies(rows, doc)
    cot.write_csv(output / 'Linhas_dependentes_medidas.csv', dependencies,
        ['linha', 'codigo_medida', 'moveis', 'premissa', 'vinculo', 'fonte'])
    affected = {m for r in results if r['medido'] is not None and r['delta'] is not None and any(abs(d) > 1e-6 for d in r['delta']) for m in r['moveis'].split('|') if m}
    pieces = [dict(movel=r['movel'], id=r['id'], C_atual_mm=r['C_ficha_mm'], L_atual_mm=r['L_ficha_mm'],
        C_revisado_mm='', L_revisado_mm='', acao='reabrir corte do móvel ' + r['movel'],
        motivo='vínculo executivo medida→eixo da peça pendente; não aumentar caixa automaticamente')
        for r in cot.read_csv(ROOT / (cot.CUT + 'Lista_de_corte.csv')) if r['variante'] == 'base' and r['movel'] in affected]
    cot.write_csv(output / 'Pecas_afetadas.csv', pieces, ['movel', 'id', 'C_atual_mm', 'L_atual_mm', 'C_revisado_mm', 'L_revisado_mm', 'acao', 'motivo'])
    cot.write_csv(output / 'Impactos_medidas.csv', results, list(results[0]))
    cot.dump(output / 'Impactos_geometria.json', dict(resultados=geometry, folgas_paredes=wall_gaps,
        aviso='Valores ausentes continuam nominais. Sem novas dimensões de corte ou validação de fabricação.'))
    cot.write_csv(output / 'Tolerancias_usadas.csv', table, list(hypothesis()[0]))
    questions = warnings()
    cot.write_csv(output / 'Perguntas_RT.csv', questions, ['codigo', 'destino', 'pergunta', 'fonte'])
    counts = reports(output, results, geometry, pieces, questions, table, len(dependencies))
    sources = [SOURCE, DEPS + 'regras.json', DEPS + 'Ranking_15.csv', DEPS + 'Descricao_fisica.csv',
        cot.REF, cot.CUT + 'Lista_de_corte.csv', 'ferramentas/fatos.json']
    manifest = dict(contagens=counts, medidos=sum(r['medido'] is not None for r in results),
        modo='bruto' if args.modo == 'bruto' else 'tabela própria' if args.tolerancias else NOTICE,
        fontes_sha256={p: cot.sha(ROOT / p) for p in sources},
        entrada_sha256=cot.sha(args.entrada) if args.entrada else None,
        datum_sha256=cot.sha(args.datum) if args.datum else None,
        tolerancias_sha256=cot.sha(args.tolerancias) if args.tolerancias else None,
        saidas_sha256={p.name: cot.sha(p) for p in output.iterdir() if p.is_file() and p.name in ['Relatorio_medidas.md', 'Relatorio_medidas_celular.md', 'Impactos_medidas.csv', 'Linhas_dependentes_medidas.csv', 'Impactos_geometria.json', 'Pecas_afetadas.csv']})
    cot.dump(output / 'Manifesto_medidas.json', manifest)
    print(json.dumps(dict(codigos=len(rows), medidos=manifest['medidos'], relacoes=len(geometry), contagens=counts), ensure_ascii=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--entrada', type=Path)
    parser.add_argument('--saida', type=Path, default=OUT)
    parser.add_argument('--modo', choices=['hipotese', 'bruto'], default='hipotese')
    parser.add_argument('--tolerancias', type=Path)
    parser.add_argument('--datum', type=Path, help='Arquivo externo com vínculo ao datum nominal; não valida o levantamento')
    parser.add_argument('--gerar-modelo', action='store_true')
    try:
        run(parser.parse_args())
    except (ValueError, KeyError) as error:
        parser.exit(2, str(error) + '\n')
