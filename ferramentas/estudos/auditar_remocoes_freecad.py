"""Inventaria uso antes de remover objetos de uma copia externa do FreeCAD.

Somente leitura do FCStd, base, regras e fontes. Nao remove objetos nem muda regras.
O plano conservador distingue filiação comum de dependencia funcional/nativa.
Saidas obrigatoriamente fora do repositorio. Referencias de auditorias anteriores
na pasta temporaria nao sao consideradas uso funcional (evita prova circular).
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
import fnmatch
import datetime as dt
import gzip
import hashlib
import html
import json
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET
import zipfile


TOKEN = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
TEXT = {'.py', '.js', '.html', '.json', '.csv', '.svg', '.md', '.txt', '.fcmacro', '.css', '.map'}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def gravar(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=1), encoding='utf-8')


def ler_modelo(path):
    with zipfile.ZipFile(path) as z:
        root = ET.fromstring(z.read('Document.xml'))
        types = {o.get('name'): o.get('type') for o in root.findall('./Objects/Object')}
        objects = {}
        for o in root.findall('./ObjectData/Object'):
            props = {p.get('name'): p for p in o.findall('./Properties/Property')}
            label = props['Label'].find('String').get('value')
            group = []
            if 'Group' in props:
                group = [v.get('value') for v in props['Group'].iter('Link')]
            objects[o.get('name')] = dict(tipo=types[o.get('name')], label=label,
                                           props=props, membros=group, visivel=None)
        gui = ET.fromstring(z.read('GuiDocument.xml'))
        for vp in gui.iter('ViewProvider'):
            for p in vp.iter('Property'):
                if p.get('name') == 'Visibility':
                    objects[vp.get('name')]['visivel'] = p.find('Bool').get('value') == 'true'
        return objects


def descendentes(objects, root):
    seen, todo = set(), [root] if root in objects else []
    while todo:
        n = todo.pop()
        if n in seen:
            continue
        seen.add(n)
        todo.extend(objects[n]['membros'])
    return seen


def valores_json(value, path='$'):
    if isinstance(value, str):
        yield path, value
    elif isinstance(value, dict):
        for k, v in value.items():
            yield from valores_json(v, path + '.' + str(k))
    elif isinstance(value, list):
        for i, v in enumerate(value):
            yield from valores_json(v, path + '[' + str(i) + ']')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--modelo', type=Path, required=True)
    ap.add_argument('--runtime', type=Path, required=True,
                    help='Dependencias exportadas pela instancia grafica, somente leitura')
    ap.add_argument('--saida', type=Path, required=True)
    ap.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[2])
    ap.add_argument('--preparar-limpeza-real', action='store_true',
                    help='Propoe exclusoes externas; base e regra historicos_ocultos ficam pendentes')
    ap.add_argument('--liberar', action='append', default=[], metavar='NOME_OU_GLOB',
                    help='Retira a protecao explicita de objetos aprovados por Elias (repetivel); '
                         'nao afeta uso funcional, expressoes ou referencias')
    ap.add_argument('--planilhas-arquivadas', type=Path,
                    help='JSON externo {Name: {celulas}} que arquiva o conteudo das planilhas liberadas')
    args = ap.parse_args()
    repo, model, out = args.repo.resolve(), args.modelo.resolve(), args.saida.resolve()
    if model.is_relative_to(repo) or out.is_relative_to(repo):
        ap.error('Modelo e saidas devem estar fora do repositorio')
    out.mkdir(parents=True, exist_ok=True)
    original_sha = sha(model)
    objects = ler_modelo(model)
    names = set(objects)
    runtime_file = json.loads(args.runtime.read_text(encoding='utf-8'))
    if runtime_file.get('arquivo_sha256') != original_sha:
        raise ValueError('Runtime nao esta vinculado ao SHA256 do modelo auditado')
    runtime = runtime_file['objetos']
    if set(runtime) != names:
        raise ValueError('Runtime nao corresponde ao conjunto de Names do arquivo salvo')
    if any(runtime[n]['tipo'] != objects[n]['tipo'] for n in names):
        raise ValueError('Tipos do runtime divergem do arquivo salvo')
    references = defaultdict(lambda: defaultdict(list))
    counts = defaultdict(Counter)
    manifest, coverage_errors, corpus_text = [], [], {}
    labels = defaultdict(set)
    for n, o in objects.items():
        labels[o['label']].add(n)

    def hit(category, target, evidence):
        counts[category][target] += 1
        if len(references[category][target]) < 12:
            references[category][target].append(evidence)

    def scan(text, category, evidence, owner=None):
        decoded = html.unescape(text)
        for m in TOKEN.finditer(decoded):
            n = m.group()
            if n in names and n != owner:
                hit(category, n, dict(evidence, deslocamento=m.start()))
        for label in re.findall(r'<<([^<>]+)>>', decoded):
            for n in labels.get(label, set()):
                hit(category, n, dict(evidence, referencia_label=label))

    structural = defaultdict(list)
    own_expr = Counter()
    sheet_cells = Counter()
    intrinsic = defaultdict(list)
    for owner, o in objects.items():
        for pn, p in o['props'].items():
            typ = p.get('type', '')
            if pn in ('Label', 'Label2'):
                continue  # declarations are not references to their own object
            if pn == 'ExpressionEngine':
                for v in p.iter('Expression'):
                    own_expr[owner] += 1
                    scan(v.get('expression', ''), 'expressoes',
                         {'objeto': owner, 'propriedade': v.get('path')})
            elif o['tipo'] == 'Spreadsheet::Sheet' and pn == 'cells':
                for cell in p.iter('Cell'):
                    sheet_cells[owner] += 1
                    scan(cell.get('content', ''), 'planilhas',
                         {'objeto': owner, 'celula': cell.get('address')})
                for link in p.iter():
                    if 'Link' in link.tag:
                        for value in link.attrib.values():
                            scan(value, 'planilhas', {'objeto': owner, 'campo': link.tag})
            elif 'Link' in typ:
                for v in p.iter():
                    for key, value in v.attrib.items():
                        if key in ('count', 'name', 'type', 'status'):
                            continue
                        for n in set(TOKEN.findall(value)) & names:
                            ev = {'objeto': owner, 'propriedade': pn}
                            if pn == 'Group' and o['tipo'] == 'App::DocumentObjectGroup':
                                structural[n].append(owner)
                            else:
                                hit('dependentes_funcionais', n, ev)
            elif any(v in typ for v in ('String', 'Map', 'File', 'Path')):
                for v in p.iter():
                    for key, value in v.attrib.items():
                        if key not in ('name', 'type', 'status', 'count'):
                            scan(value, 'textos_nativos', {'objeto': owner, 'propriedade': pn}, owner)
            if pn == 'Camera' and any('Camera' in value for v in p.iter() for value in v.attrib.values()):
                intrinsic[owner].append('camera Coin salva; restauracao por selecao/propriedade Camera')
        for parent in runtime[owner]['dependentes']:
            is_plain_parent = (objects[parent]['tipo'] == 'App::DocumentObjectGroup'
                               and owner in objects[parent]['membros'])
            if not is_plain_parent:
                hit('dependentes_runtime', owner, {'objeto': parent})

    inv_path = repo / 'ferramentas/verificar_modelo/invariantes.json'
    mov_path = repo / 'ferramentas/verificar_modelo/movimentos.json'
    base_path = repo / '02_Modelo_3D/Base_verificacao.json.gz'
    rules = json.loads(inv_path.read_text(encoding='utf-8'))
    protected_rules = defaultdict(list)
    proposed_historic = set()
    for i, rule in enumerate(rules['regras']):
        if args.preparar_limpeza_real and rule.get('id') == 'historicos_ocultos' and rule.get('tipo') == 'oculto':
            proposed_historic.update(rule['objetos'])
            continue  # unica regra cuja lista pode ser proposta para reducao, sem gravar o oficial
        for path, value in valores_json(rule):
            scan(value, 'invariantes', {'arquivo': str(inv_path.relative_to(repo)),
                                      'regra': rule.get('id', i), 'campo': path})
        if rule.get('tipo') in ('oculto', 'existe'):
            for _, value in valores_json(rule):
                for n in set(TOKEN.findall(value)) & names:
                    protected_rules[n].append({'id': rule.get('id', i), 'tipo': rule['tipo']})
    movements = json.loads(mov_path.read_text(encoding='utf-8'))
    for path, value in valores_json(movements):
        scan(value, 'movimentos', {'arquivo': str(mov_path.relative_to(repo)), 'campo': path})
    with gzip.open(base_path, 'rt', encoding='utf-8') as f:
        base_names = set(json.load(f)['objetos'])
    for p, cat in [(inv_path, 'invariantes'), (mov_path, 'movimentos'), (base_path, 'base')]:
        manifest.append({'arquivo': str(p.relative_to(repo)), 'categoria': cat,
                         'sha256': sha(p), 'estado': 'lido'})

    # Scan canonical R15, current site sources/builds and supporting project code.
    corpus = {}
    for folder, category in [('06_Entregas/Fichas_fabricacao', 'fichas_R15'),
                             ('ferramentas/site', 'site_fontes'), ('.site', 'site_build_local'),
                             ('ferramentas', 'codigo_apoio')]:
        for p in (repo / folder).rglob('*'):
            if p.is_file() and p.suffix.lower() in TEXT and p.resolve() != Path(__file__).resolve():
                corpus.setdefault(p, category)
    required = [repo / '06_Entregas/Fichas_fabricacao/Tecnica_R15.json',
                repo / '06_Entregas/Fichas_fabricacao/index.html',
                repo / 'ferramentas/site/src/cad-data.js']
    for p in required:
        if not p.is_file():
            coverage_errors.append('Fonte obrigatoria ausente: ' + str(p.relative_to(repo)))
    for p, category in sorted(corpus.items()):
        try:
            raw = p.read_bytes()
            try:
                text = raw.decode('utf-8-sig')
                encoding = 'utf-8-sig'
            except UnicodeDecodeError:
                text, encoding = raw.decode('cp1252'), 'cp1252'
            evidence = {'arquivo': str(p.relative_to(repo))}
            corpus_text[p] = html.unescape(text)
            scan(text, category, evidence)
            if p.suffix.lower() == '.json':
                # Decodes JSON escaping too; retains location evidence for IDs/labels.
                for path, value in valores_json(json.loads(text)):
                    for n in labels.get(value, set()):
                        hit(category, n, dict(evidence, campo=path, referencia_label=value))
            manifest.append(dict(evidence, categoria=category, sha256=hashlib.sha256(raw).hexdigest(),
                                 bytes=len(raw), codificacao=encoding, estado='lido'))
        except (OSError, UnicodeError, json.JSONDecodeError) as e:
            coverage_errors.append(str(p.relative_to(repo)) + ': ' + str(e))

    historical = descendentes(objects, 'Historico_Oculto')
    superseded = descendentes(objects, 'Legados_Etapas_A_B')
    protected = set()
    if args.preparar_limpeza_real:
        for n, o in objects.items():
            if (o['tipo'] in ('App::Origin', 'App::Point', 'App::Part') or
                n.startswith(('Camera_', 'BC43_', 'BancoDuasTampasR43', 'BanheiroCorrerR43')) or
                'minifix' in (n + ' ' + o['label']).lower() or
                n in ('QuadroAreas', 'Materiais_Nomeados')):
                protected |= descendentes(objects, n)
    liberados = {n for n in objects if any(fnmatch.fnmatchcase(n, g) for g in args.liberar)}
    protected -= liberados
    arquivadas = set()
    if args.planilhas_arquivadas:
        arq = json.loads(args.planilhas_arquivadas.read_text(encoding='utf-8'))
        arquivadas = {n for n, v in arq.items() if v.get('celulas')}
    candidates, removal = [], []
    categories = ['expressoes', 'invariantes', 'movimentos', 'fichas_R15', 'planilhas',
                  'site_fontes', 'site_build_local', 'codigo_apoio', 'textos_nativos',
                  'dependentes_funcionais', 'dependentes_runtime']
    for n, o in objects.items():
        kinds = []
        if o['visivel'] is False:
            kinds.append('oculto')
            if not counts['dependentes_funcionais'][n] and not counts['dependentes_runtime'][n]:
                kinds.append('oculto_sem_dependente_funcional')
        if n in historical:
            kinds.append('Historico_Oculto')
        if n in superseded:
            kinds.append('superado_A_B')
        if re.fullmatch(r'Origin\d*', n):
            kinds.append('Origin_a_conferir')
        if not kinds:
            continue
        reasons = []
        if TOKEN.fullmatch(n) is None:
            reasons.append('Name fora do alfabeto de identificadores auditado; exclusao nao provada')
        if protected_rules[n]:
            reasons.append('invariante oculto/existe: exige proposta de regra e aprovacao, inexistentes')
        if n in base_names and not args.preparar_limpeza_real:
            reasons.append('ID consta da base; exclusao reprovaria --completo sem decisao sobre a base')
        if n in protected:
            reasons.append('protecao explicita: montagem/origem/camera/quadro/material/BC43/banco/Minifix')
        if args.preparar_limpeza_real:
            if o['visivel'] and 'Shape' in o['props']:
                reasons.append('geometria visivel: remocao proibida')
            functional_out = [v for v in runtime[n]['dependencias'] if v not in o['membros']]
            if functional_out:
                reasons.append('dependencias funcionais de saida: ' + ', '.join(functional_out))
        for category in categories:
            if counts[category][n]:
                reasons.append(category + ': ' + str(counts[category][n]) + ' ocorrencia(s)')
        if own_expr[n]:
            reasons.append('possui ' + str(own_expr[n]) + ' expressoes proprias')
        if sheet_cells[n] and not (n in liberados and n in arquivadas):
            reasons.append('planilha nativa com celulas/documentacao')
        reasons.extend(intrinsic[n])
        if o['membros'] and not args.preparar_limpeza_real:
            reasons.append('container organiza ' + str(len(o['membros'])) + ' objetos; conteudo nao pode ser descartado')
        if coverage_errors:
            reasons.append('cobertura incompleta: nenhuma exclusao permitida')
        # No incoming Name reference is insufficient if consumers could use the Label.
        alias_checked = False
        if not reasons:
            alias_checked = True
            alias = o['label']
            for p, category in corpus.items():
                text = corpus_text.get(p, '')
                if alias and alias != n and alias in text:
                    hit(category, n, {'arquivo': str(p.relative_to(repo)), 'referencia_label': alias})
                    reasons.append('referencia pelo Label em ' + str(p.relative_to(repo)))
            if not reasons:
                removal.append(n)
        origin_owners = references['dependentes_funcionais'][n] if 'Origin_a_conferir' in kinds else []
        row = {'Name': n, 'Label': o['label'], 'tipo': o['tipo'], 'categorias': kinds,
               'visivel_salvo': o['visivel'], 'grupos_estruturais': structural[n],
               'vinculos_da_origem': origin_owners,
               'base_protege': n in base_names, 'regras_oculto_existe': protected_rules[n] +
                    ([{'id': 'historicos_ocultos', 'tipo': 'oculto', 'proposta_permitida': True}]
                     if n in proposed_historic else []),
               'expressoes_proprias': own_expr[n], 'uso_intrinseco': intrinsic[n],
               'referencias': {c: {'contagem': counts[c][n], 'amostras': references[c][n]}
                               for c in categories}, 'aliases_verificados_para_exclusao': alias_checked,
               'decisao': 'mantido' if reasons else 'remocao_provada',
               'motivos': reasons or ['nenhuma referencia funcional no corpus auditado; sem uso intrinseco; '
                                      'membros de Group comum, se houver, tambem passam no plano']}
        row['membros'] = o['membros']
        row['InList'] = runtime[n]['dependentes']
        row['OutList'] = runtime[n]['dependencias']
        candidates.append(row)

    if args.preparar_limpeza_real:
        # Uma lista Group comum pode perder apenas membros tambem aprovados.
        # Ponto fixo preserva qualquer container com descendente mantido.
        allowed = set(removal)
        while True:
            blocked = {v['Name'] for v in candidates if v['Name'] in allowed
                       and any(n not in allowed for n in v['membros'])}
            if not blocked:
                break
            allowed -= blocked
        rows = {v['Name']: v for v in candidates}
        for n in set(removal) - allowed:
            rows[n]['decisao'] = 'mantido'
            rows[n]['motivos'] = ['container ainda organiza objetos mantidos']
        # Folhas antes dos pais. Nao ha dependencia funcional em nenhum aprovado.
        removal = []
        while allowed:
            batch = sorted(n for n in allowed if not set(objects[n]['membros']) & allowed)
            if not batch:
                raise ValueError('Ciclo de containers no plano')
            removal.extend(batch)
            allowed -= set(batch)

    summary = {'schema': 1, 'gerado_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
               'modelo_sha256': original_sha, 'objetos_antes': len(objects),
               'candidatos': len(candidates), 'mantidos': len(candidates) - len(removal),
               'remocoes_provadas': removal, 'objetos_depois_planejado': len(objects) - len(removal),
               'invariantes_oculto_existe_protegidos': sum(bool(v['regras_oculto_existe']) for v in candidates),
               'candidatos_na_base': sum(v['base_protege'] for v in candidates),
               'origins': sum('Origin_a_conferir' in v['categorias'] for v in candidates),
               'origins_por_tipo': dict(Counter(v['tipo'] for v in candidates
                                                if 'Origin_a_conferir' in v['categorias'])),
               'origins_sem_vinculo_funcional': [v['Name'] for v in candidates
                                                if 'Origin_a_conferir' in v['categorias']
                                                and not v['vinculos_da_origem']],
               'expressoes_nativas': sum(own_expr.values()),
               'planilhas_nativas': sum(v['tipo'] == 'Spreadsheet::Sheet' for v in objects.values()),
               'cameras_nativas_protegidas': sum(bool(v['uso_intrinseco']) for v in candidates),
               'categorias': dict(Counter(c for v in candidates for c in v['categorias'])),
               'corpus_arquivos': len(manifest), 'erros_cobertura': coverage_errors,
               'limites': ['Busca de Names e Labels nas fontes locais congeladas; nao consulta publicacao remota.',
                          'Filiação a Group comum separada de dependencia funcional; containers com conteudo mantidos.',
                          'Sistemas de origem nativos nao sao duplicatas apenas por coincidirem em coordenadas.',
                          'Auditor e artefatos temporarios de auditorias anteriores excluidos para evitar prova circular.',
                          'Binarios/imagens/pacotes historicos nao sao tratados como codigo de vistas; fontes textuais canonicas auditadas.'],
               'candidatos_detalhados': candidates}
    if sha(model) != original_sha:
        raise RuntimeError('O modelo mudou durante a auditoria; inventario invalidado')
    gravar(out / 'Inventario_antes.json', summary)
    gravar(out / 'Corpus_conferido.json', manifest)
    trimmed = json.loads(json.dumps(rules))
    for rule in trimmed['regras']:
        if rule.get('id') == 'historicos_ocultos' and rule.get('tipo') == 'oculto':
            for key in ('objetos', 'nomes'):
                if isinstance(rule.get(key), list):
                    rule[key] = [n for n in rule[key] if n not in removal]
    gravar(out / 'Invariantes_propostas.json', trimmed)
    gravar(out / 'Plano_remocoes.json', {'schema': 2, 'modelo_sha256': original_sha,
        'modelo_origem': str(model), 'repositorio_auditado': str(repo),
        'inventario_sha256': sha(out / 'Inventario_antes.json'),
        'inventario_csv_sha256': sha(out / 'Inventario_candidatos.csv') if (out / 'Inventario_candidatos.csv').exists() else None,
        'script_sha256': sha(Path(__file__)), 'remover': removal,
        'provas': [v for v in candidates if v['Name'] in removal],
        'mantidos': [v for v in candidates if v['Name'] not in removal],
        'aprovacao': 'PENDENTE', 'revisao': 'PENDENTE',
        'mudar_invariantes': trimmed != rules, 'mudar_base': False})
    gravar(out / 'Invariantes_protegidas.json', {
        'propostas_aplicadas': [], 'aprovacao_para_excluir':
            'PENDENTE para oficial; preparacao externa autorizada na conversa, 31/10/2026'
            if args.preparar_limpeza_real else 'NAO SOLICITADA',
        'objetos_mantidos': {v['Name']: v['regras_oculto_existe'] for v in candidates
                            if v['regras_oculto_existe'] and v['Name'] not in removal},
        'criterio': 'Nenhuma regra alterada; candidatos protegidos permanecem no modelo.'})
    with (out / 'Inventario_candidatos.csv').open('w', encoding='utf-8-sig', newline='') as f:
        fields = ['Name', 'Label', 'tipo', 'categorias', 'decisao', 'motivos', 'base_protege',
                  'grupos_estruturais', 'regras_oculto_existe', 'referencias']
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for v in candidates:
            w.writerow({k: json.dumps(v[k], ensure_ascii=False) if isinstance(v[k], (dict, list))
                        else v[k] for k in fields})
    plan_path = out / 'Plano_remocoes.json'
    plan = json.loads(plan_path.read_text(encoding='utf-8'))
    plan['inventario_csv_sha256'] = sha(out / 'Inventario_candidatos.csv')
    plan['corpus_sha256'] = sha(out / 'Corpus_conferido.json')
    plan['runtime_sha256'] = sha(args.runtime)
    gravar(plan_path, plan)
    printable = {k: v for k, v in summary.items() if k not in ('candidatos_detalhados', 'limites')}
    print(json.dumps(printable, ensure_ascii=True))
    return 1 if coverage_errors else 0


if __name__ == '__main__':
    sys.exit(main())
