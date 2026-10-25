"""Verificador de consistência do projeto Guedala Park.

Compara as fontes vigentes e aponta divergências. Não corrige nada.
Uso: python verificar_consistencia.py   (gera Verificacao_consistencia.md ao lado)
"""
from pathlib import Path
import json, re, sys

HERE = Path(__file__).resolve().parent          # ferramentas
ROOT = HERE.parent                              # guedala-park
sys.stdout.reconfigure(encoding='utf-8')
results = []  # (situação, verificação, detalhe)


def check(ok, name, detail=''):
    results.append(('OK' if ok else 'ATENÇÃO', name, detail))


def obsolete_bench_fields(value, path=''):
    """Procura a cadeia superada em todos os campos operacionais, inclusive montagem.

    Evidências e fontes guardam a origem histórica; não são uma especificação ativa.
    """
    found = []
    if isinstance(value, dict):
        for key, item in value.items():
            if key not in {'sources', 'evidence', 'sourcePaths', 'historicalAlternatives'}:
                found.extend(obsolete_bench_fields(item, f'{path}.{key}' if path else key))
    elif isinstance(value, list):
        for i, item in enumerate(value):
            found.extend(obsolete_bench_fields(item, f'{path}[{i}]'))
    elif isinstance(value, str) and re.search(r'southco|\be6-10-', value, re.I):
        found.append(path)
    return found


def main():
    results.clear()
    # 1. Termos superados não devem voltar ao site
    data_js = (HERE / 'site/src/data.js').read_text(encoding='utf-8')
    app_js = (HERE / 'site/src/app.js').read_text(encoding='utf-8')
    superados = {
        "Apoios de celular retirados (22/10)": "add('ledges'" in app_js,
        "Varal sem placa de ocultação (R35)": '"Varal vertical com chapa de ocultação"' in data_js and 'Varal vertical · quadro inteiro manual' not in data_js,
        "Nota geral sem 'apartamento espelhado'": "all:'Apartamento espelhado" in data_js,
        "Banco sem Southco como candidata": 'Southco candidata no estudo' in data_js,
    }
    for name, bad in superados.items():
        check(not bad, f'Site: {name}')

    # 2. Caderno de especificações gerado depois da última mudança nos dados
    cad = ROOT / '01_Programa_e_decisoes/Caderno_de_especificacoes.md'
    src = HERE / 'site/src/data.js'
    check(cad.exists() and cad.stat().st_mtime >= src.stat().st_mtime - 1,
          'Caderno de especificações atualizado em relação a data.js',
          'Rode site/gerar_caderno.cjs' if cad.exists() and cad.stat().st_mtime < src.stat().st_mtime - 1 else '')

    # 3. Site gerado depois das fontes
    html = HERE / 'site/Guedala_Park_Interativo.html'
    newest = max(p.stat().st_mtime for p in (HERE / 'site/src').glob('*.js'))
    check(html.stat().st_mtime >= newest - 1, 'Site local reconstruído depois da última alteração em src/',
          '' if html.stat().st_mtime >= newest - 1 else 'Rode site/construir.py')

    # 4. Ferragens: fichas R14 × reconciliação
    tech = json.loads((HERE / 'site/fabrication/technical-r14.json').read_text(encoding='utf-8'))['modules']
    def qty(pred):
        return sum((r['quantity'] or 0) for m in tech.values() for r in m['hardwareRows'] if pred(r))
    hinges = qty(lambda r: r['item'].startswith('Dobradiças das portas de abrir'))
    fgv = qty(lambda r: 'FGVTN54FGOC12500' in str(r['reference']).replace(' ', ''))
    minifix = qty(lambda r: r['item'] == 'Caixas Minifix')
    check(hinges == 52, 'Dobradiças de abrir nas fichas = 52 do orçamento', f'fichas: {hinges}')
    check(fgv == 7, 'Pares FGVTN 500 nas fichas = 7 do orçamento', f'fichas: {fgv}')
    check(minifix == 52, 'Minifix com quantidade definida nas fichas = 52 da reconciliação', f'fichas: {minifix}')
    southco = [f'{code}.{path}' for code, module in tech.items() for path in obsolete_bench_fields(module)]
    check(not southco, 'Fichas sem Southco (diretriz: piano + trava)',
          f"cadeia histórica ainda ativa: {', '.join(southco)}" if southco else '')
    limiters = [row for row in tech['P20']['hardwareRows'] if row['item'] == 'Limitação independente da abertura das tampas']
    check(len(limiters) == 1 and limiters[0]['quantity'] is None,
          'Banco mantém limitação de abertura necessária sem inventar componente/quantitativo',
          'Definir produto, geometria e fixação no protótipo; não reutilizar batente histórico.')

    # 5. Planta de pontos cobre os aparelhos com ponto dedicado
    pontos = (HERE / '../03_Ambientes/Planta_pontos/gerar_planta_pontos.py').read_text(encoding='utf-8')
    for termo in ['Forno', 'cooktop', 'Lavadora', 'E21', 'Geladeira', 'Micro-ondas', 'Torre']:
        check(termo.lower() in pontos.lower(), f'Planta de pontos inclui {termo}')

    # 6. Links relativos dos documentos vigentes
    vigentes = ['README.md', 'ESTADO_ATUAL.md', '01_Programa_e_decisoes/Roteiro_para_projeto_oficial.md',
                '01_Programa_e_decisoes/Programa_de_necessidades.md', '05_Orcamento_e_cronograma/Cronograma_obra_e_compras.md',
                '01_Programa_e_decisoes/Plano_de_reforma_NBR16280.md', '03_Ambientes/Iluminacao/Lista_curta_luminarias_e_madeira.md',
                '06_Entregas/README.md', '07_Imovel/Roteiro_dia_das_chaves_R01.md',
                '05_Orcamento_e_cronograma/Orcamento/Marcenaria_35mil/Pacote_cotacao_marcenaria_R01.md']
    broken = []
    for f in vigentes:
        p = ROOT / f
        for link in re.findall(r'\]\(([^)#h][^)#]*)', p.read_text(encoding='utf-8')):
            if not (p.parent / link).exists():
                broken.append(f'{f} → {link}')
    check(not broken, 'Links dos documentos vigentes', '; '.join(broken))

    lines = ['# Verificação de consistência', '', 'Gerado por `verificar_consistencia.py`. Não corrige nada; só aponta.', '',
             '| Situação | Verificação | Detalhe |', '|---|---|---|']
    lines += [f'| {s} | {n} | {d} |' for s, n, d in results]
    (HERE / 'Verificacao_consistencia.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    warn = sum(1 for r in results if r[0] != 'OK')
    print(f'{len(results)} verificações, {warn} com atenção')
    for s, n, d in results:
        if s != 'OK':
            print('-', n, '|', d)

    return int(warn > 0)


if __name__ == '__main__':
    raise SystemExit(main())
