"""Dependências geométricas sem FreeCAD; cenários nunca sobrescrevem fontes."""
import argparse
import ast
import copy
import csv
import hashlib
import json
import math
from pathlib import Path
import sys
import tempfile

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'ferramentas/pranchas'))
from medidas import carregar, resolver


def ler_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def entradas(root=ROOT, cenario=None, nominal=False):
    rows = carregar(root)
    if nominal:
        for row in rows.values():
            row['valor_medido'] = ''
    if cenario:
        seen = set()
        with Path(cenario).open(encoding='utf-8-sig', newline='') as f:
            reader = csv.DictReader(f)
            if not {'codigo_medida', 'valor_medido'} <= set(reader.fieldnames or []):
                raise ValueError('Cenário exige codigo_medida e valor_medido')
            for row in reader:
                code = row['codigo_medida']
                if code not in rows or code in seen:
                    raise ValueError('Código desconhecido/duplicado no cenário: ' + code)
                if not row['valor_medido'].strip():
                    raise ValueError('Valor vazio no cenário: ' + code)
                seen.add(code)
                rows[code]['valor_medido'] = row['valor_medido']
                rows[code]['evidencia_campo'] = row.get('evidencia_campo', 'Cenário externo')
                # Também validar medidas não utilizadas nas regras de móveis.
                if code.startswith('DIM-'):
                    resolver(rows, code + '/0')
                    if code in {'DIM-01', 'DIM-02', 'DIM-05', 'DIM-06', 'DIM-07', 'DIM-08'}:
                        resolver(rows, code + '/1')
                else:
                    resolver(rows, code)
    return rows


def avaliar(formula, rows, constantes, medidas):
    """Linguagem restrita: números, constantes, +/− e m(código). Sem eval."""
    usados = set()
    def visit(node):
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value
        if isinstance(node, ast.Name) and node.id in constantes:
            return constantes[node.id]
        if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Add, ast.Sub)):
            a, b = visit(node.left), visit(node.right)
            return a + b if isinstance(node.op, ast.Add) else a - b
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.USub, ast.UAdd)):
            return -visit(node.operand) if isinstance(node.op, ast.USub) else visit(node.operand)
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                and node.func.id == 'm' and len(node.args) == 1 and not node.keywords
                and isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str)):
            code = node.args[0].value
            if code not in medidas:
                raise ValueError('Dependência não declarada: ' + code)
            usados.add(code)
            value = resolver(rows, code).mm
            if value is None:
                raise ValueError('Medida pendente: ' + code)
            return value
        raise ValueError('Expressão não permitida: ' + formula)
    value = visit(ast.parse(formula, mode='eval').body)
    if not math.isfinite(value):
        raise ValueError('Resultado não finito')
    return value


def base(root=ROOT):
    doc = ler_json(root / '04_Moveis/Dependencias/regras.json')
    geo = ler_json(root / doc['exportacao'])
    if doc['cad_sha256'] != geo['cad_sha256']:
        raise ValueError('Regras e exportação pertencem a revisões CAD diferentes')
    if hashlib.sha256((root / geo['cad_path']).read_bytes()).hexdigest() != doc['cad_sha256']:
        raise ValueError('Exportação R53 desatualizada')
    objects = {o['id']: o for o in geo['objects']}
    for name, target in doc['alvos'].items():
        actual = geo['modules'][name] if target['tipo'] == 'modulo' else objects[name]
        if actual['box'] != target['box']:
            raise ValueError('Envelope não reproduz a R53: ' + name)
    return doc


def calcular(rows, doc):
    result = []
    boxes = {n: list(t['box_planta']) for n, t in doc['alvos'].items()}
    seen = set()
    for rule in doc['regras']:
        name, cota = rule['movel'], rule['cota']
        if (name, cota) in seen:
            raise ValueError('Regra duplicada: ' + name + '/' + cota)
        seen.add((name, cota))
        mode = rule['modo']
        if mode not in {'segue_parede', 'fixa_com_folga_variavel'}:
            raise ValueError('Modo inválido: ' + mode)
        values = {code: resolver(rows, code) for code in rule['medidas']}
        if any(v.mm is None for v in values.values()):
            raise ValueError('Medida pendente: ' + name + '/' + cota)
        theoretical = avaliar(rule['formula'], rows, rule['folgas'], rule['medidas'])
        before = rule['atual_mm']
        after = before if mode == 'fixa_com_folga_variavel' else theoretical
        changed = abs(after - before) > 1e-6
        status = 'OK'
        gaps = {}
        box = doc['alvos'][name]['box_planta']
        axis = rule.get('eixo')
        if axis is not None:
            span = values[rule['dimensao']].mm
            if span <= 0:
                raise ValueError('Dimensão do ambiente não positiva: ' + rule['dimensao'])
            if axis < 2:
                origin = values[rule['origem']].mm
                gaps = {'inicio': box[axis] - origin, 'fim': origin + span - box[axis] - after}
                if rule.get('prumo'):
                    gaps['fim'] -= max(0, values[rule['prumo']].mm)
                gap_changed = (abs(gaps['inicio'] - rule['folgas']['folga_inicio']) > 1e-6
                               or abs(gaps['fim'] - rule['folgas']['folga_fim']) > 1e-6)
            else:
                gaps = {'topo': span - box[2] - after}
                gap_changed = abs(gaps['topo'] - rule['folgas']['folga_topo']) > 1e-6
            status = 'ajuste de fabricação' if changed else 'ajuste de arremate' if gap_changed else 'OK'
            if after <= 0 or min(gaps.values()) < -1e-6:
                status = 'NÃO CABE'
            boxes[name][axis + 3] = box[axis] + after
        elif rule.get('representacao') == 'fechamento':
            gaps = {'topo': after}
            status = 'NÃO CABE' if after < 0 else 'ajuste de arremate' if changed else 'OK'
        elif changed:
            status = 'ajuste de fabricação'
        low, high = rule['limites']['min'], rule['limites']['max']
        outside = (low is not None and after < low) or (high is not None and after > high)
        if outside and status != 'NÃO CABE':
            status = 'fora do limite'
        result.append(dict(movel=name, cota=cota, antes_mm=before, depois_mm=round(after, 6),
                           delta_mm=round(after-before, 6), candidato_formula_mm=round(theoretical, 6),
                           folgas_mm=gaps, status=status, fora_do_limite=outside, modo=mode,
                           tipo='envelope' if axis is not None else rule.get('representacao', 'referencia'),
                           medidas={k:dict(mm=v.mm, origem=v.origem) for k,v in values.items()},
                           fonte=rule['fonte'], fichas=rule['fichas'], pranchas=rule['pranchas']))
    return dict(schema=1, cad_sha256=doc['cad_sha256'], resultados=result, envelopes=boxes,
                limites='Geometria de estudo; sem recortes, corte, colisões 3D ou atualização do FCStd')


def saida_segura(path, root=ROOT):
    path = Path(path).resolve()
    if path == root.resolve() or root.resolve() in path.parents:
        raise ValueError('Saída de cenário/medidas reais deve ficar fora do repositório')
    return path


def escrever(report, output):
    output.mkdir(parents=True, exist_ok=True)
    (output / 'Impacto.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    rows = report['resultados']
    lines = ['# Impacto dimensional', '', 'ESTUDO — NÃO EXECUTAR. '+report['limites'], '',
             'Base: R53. '+report.get('cenario', 'Valores nominais atuais.'), '',
             f'{len(rows)} regras; {sum(r["delta_mm"] != 0 for r in rows)} cotas/referências alteradas. '
             f'{sum(r["status"] != "OK" for r in rows)} avisos (inclui conflitos nominais).', '',
             'Interfaces inalteradas ficam somente no JSON. “Ajuste de fabricação” em referência exige revisão de implantação/recorte; não manda deslocar a caixa.', '',
             '| Alvo/cota | Antes → depois (mm) | Folgas (mm) | Status | Fichas / folhas |',
             '|---|---:|---|---|---|']
    for r in rows:
        if r['tipo'] == 'referencia' and r['status'] == 'OK':
            continue
        gaps = ', '.join(f'{k}={v:g}' for k,v in r['folgas_mm'].items()) or '—'
        lines.append(f'| {r["movel"]}/{r["cota"]} | {r["antes_mm"]:g} → {r["depois_mm"]:g} | {gaps} | {r["status"]} | '
                     + (r['movel']+' R15; ' if r['fichas'] else 'bancada; ') + ', '.join(r['pranchas']) + ' |')
    (output / 'Impacto.md').write_text('\n'.join(lines)+'\n', encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cenario', type=Path)
    parser.add_argument('--saida', type=Path)
    parser.add_argument('--nominal', action='store_true', help='Ignorar valores medidos; não combinar com cenário')
    args = parser.parse_args()
    if args.nominal and args.cenario:
        parser.error('--nominal não combina com --cenario')
    rows = entradas(cenario=args.cenario, nominal=args.nominal)
    report = calcular(rows, base())
    external = args.cenario or any(r['valor_medido'].strip() for r in rows.values())
    if args.saida:
        output = saida_segura(args.saida)
    elif external:
        output = Path(tempfile.mkdtemp(prefix='guedala-impacto-'))
    else:
        output = ROOT / '04_Moveis/Dependencias'
    report['cenario'] = 'CENÁRIO EXTERNO — conferir evidência; não é levantamento incorporado.' if args.cenario else 'CSV real, campo vence nominal.' if external else 'Valores nominais atuais.'
    escrever(report, output)
    print(f'{len(report["resultados"])} regras; relatório: {output / "Impacto.md"}')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, SyntaxError) as exc:
        raise SystemExit('ERRO: '+str(exc))
