"""Verificador de consistência do projeto Guedala Park.

Compara as fontes vigentes e aponta divergências. Não corrige nada.
Uso: python verificar_consistencia.py   (gera Verificacao_consistencia.md ao lado)
"""
from pathlib import Path
import json, re, sys

HERE = Path(__file__).resolve().parent          # 01_Projeto
ROOT = HERE.parent                              # guedala-park
sys.stdout.reconfigure(encoding='utf-8')
results = []  # (situação, verificação, detalhe)


def check(ok, name, detail=''):
    results.append(('OK' if ok else 'ATENÇÃO', name, detail))


# 1. Termos superados não devem voltar ao site
data_js = (HERE / 'Estudo_interativo/src/data.js').read_text(encoding='utf-8')
app_js = (HERE / 'Estudo_interativo/src/app.js').read_text(encoding='utf-8')
superados = {
    "Apoios de celular retirados (22/10)": "add('ledges'" in app_js,
    "Varal sem placa de ocultação (R35)": '"Varal vertical com chapa de ocultação"' in data_js and 'Varal vertical · quadro inteiro manual' not in data_js,
    "Nota geral sem 'apartamento espelhado'": "all:'Apartamento espelhado" in data_js,
    "Banco sem Southco como candidata": 'Southco candidata no estudo' in data_js,
}
for name, bad in superados.items():
    check(not bad, f'Site: {name}')

# 2. Caderno de especificações gerado depois da última mudança nos dados
cad = HERE / 'Caderno_de_especificacoes_R01.md'
src = HERE / 'Estudo_interativo/src/data.js'
check(cad.exists() and cad.stat().st_mtime >= src.stat().st_mtime - 1,
      'Caderno de especificações atualizado em relação a data.js',
      'Rode Estudo_interativo/gerar_caderno.cjs' if cad.exists() and cad.stat().st_mtime < src.stat().st_mtime - 1 else '')

# 3. Site gerado depois das fontes
html = HERE / 'Estudo_interativo/Guedala_Park_Interativo.html'
newest = max(p.stat().st_mtime for p in (HERE / 'Estudo_interativo/src').glob('*.js'))
check(html.stat().st_mtime >= newest - 1, 'Site local reconstruído depois da última alteração em src/',
      '' if html.stat().st_mtime >= newest - 1 else 'Rode Estudo_interativo/construir.py')

# 4. Ferragens: fichas R14 × reconciliação
tech = json.loads((HERE / 'Estudo_interativo/fabrication/technical-r14.json').read_text(encoding='utf-8'))['modules']
def qty(pred):
    return sum((r['quantity'] or 0) for m in tech.values() for r in m['hardwareRows'] if pred(r))
hinges = qty(lambda r: r['item'].startswith('Dobradiças das portas de abrir'))
fgv = qty(lambda r: 'FGVTN54FGOC12500' in str(r['reference']).replace(' ', ''))
minifix = qty(lambda r: r['item'] == 'Caixas Minifix')
check(hinges == 52, 'Dobradiças de abrir nas fichas = 52 do orçamento', f'fichas: {hinges}')
check(fgv == 7, 'Pares FGVTN 500 nas fichas = 7 do orçamento', f'fichas: {fgv}')
check(minifix == 40, 'Minifix com quantidade definida nas fichas = 40 da reconciliação', f'fichas: {minifix}')
southco = [k for k, m in tech.items() if any('Southco' in r['item'] for r in m['hardwareRows'])]
check(not southco, 'Fichas sem Southco (diretriz: piano + trava)',
      f"ainda citam Southco: {', '.join(southco)} — revisar quando a ferragem do banco for selecionada" if southco else '')

# 5. Planta de pontos cobre os aparelhos com ponto dedicado
pontos = (HERE / 'Planta_pontos_R00/gerar_planta_pontos.py').read_text(encoding='utf-8')
for termo in ['Forno', 'cooktop', 'Lavadora', 'E21', 'Geladeira', 'Micro-ondas', 'Torre']:
    check(termo.lower() in pontos.lower(), f'Planta de pontos inclui {termo}')

# 6. Links relativos dos documentos vigentes
vigentes = ['README.md', '01_Projeto/Estado_atual.md', '01_Projeto/Roteiro_para_projeto_oficial.md',
            '01_Projeto/Programa_de_necessidades_R01.md', '01_Projeto/Cronograma_obra_e_compras_R00.md',
            '01_Projeto/Plano_de_reforma_NBR16280_rascunho.md', '01_Projeto/Lista_curta_luminarias_e_madeira_R00.md',
            '05_Entregas/README.md', '04_Visita_ao_apartamento/Roteiro_dia_das_chaves_R01.md',
            '01_Projeto/Orcamento_R43_2026-10-22/Marcenaria_35mil/Pacote_cotacao_marcenaria_R01.md']
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
