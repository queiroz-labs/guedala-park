"""Planta de pontos preliminar R00: elétrica, iluminação, água, esgoto e gás.

Paredes e pisos vêm de Estudo_interativo/src/app.js (mesma base do site, em cm).
Posições dos pontos derivam dos aparelhos do modelo R45; onde o modelo não tem
aparelho, a posição é marcada como "a definir". Não altera CAD nem site.
Uso: python gerar_planta_pontos.py
"""
from pathlib import Path
from html import escape
import json, re

HERE = Path(__file__).resolve().parent
APP = (HERE.parent / 'Estudo_interativo/src/app.js').read_text(encoding='utf-8')


def literal(name):
    m = re.search(r'const ' + name + r'=(\[.*?\]);', APP)
    return json.loads(m[1].replace("'", '"'))


walls, floors = literal('walls'), literal('floors')
FLOOR_FILL = {'vinyl': '#efe7da', 'ivory': '#ece6da', 'greige': '#e4ddd0'}

# Contorno dos aparelhos/móveis de referência (x, z, largura em x, profundidade em z), em cm.
FOOTPRINTS = [
    ('Geladeira', 584.9, 615.25, 60.1, 74.75), ('Forno + cooktop', 388, 637, 60, 61.5),
    ('Pia', 459, 650, 43, 37), ('Lavadora', 320, 628, 60, 62), ('Tanque', 263, 650, 38, 35),
    ('Vaso', 350.75, 470, 37.5, 59), ('Lavatório', 414, 489, 40, 30), ('Box', 255, 405, 80, 124),
    ('Bancada', 270, 0, 200, 70), ('Sofá-cama', 400, 190, 85, 140), ('Cama queen', 5, 120, 200, 160),
    ('Roupeiro', 0, 329, 200, 65), ('Bonnie', 630, 190, 110, 180), ('Mesa', 620, 400, 80, 110),
]

# (código, tipo, x, z, altura cm ou None, descrição, situação)
# Tipos: T tomada, T20 tomada 20 A, D circuito dedicado, L luz no teto, A arandela/luz de parede,
# AF água fria, AQ água quente, E esgoto, G gás, X exaustão.
P = [
    # Cozinha
    ('C01', 'D', 418, 695, 30, 'Forno Fischer 127 V · 2061 W / 16,2 A · circuito exclusivo', 'Aparelho escolhido; circuito a dimensionar'),
    ('C02', 'G', 405, 695, 50, 'Gás GN do cooktop KE4GC', 'GN confirmado; posição real a levantar'),
    ('C03', 'T', 432, 695, 50, 'Ignição do cooktop', 'A confirmar no manual'),
    ('C04', 'T', 418, 695, 200, 'Depurador DE61IX · 127 V', 'Aparelho escolhido'),
    ('C05', 'AF', 470, 698, 55, 'Água fria da pia', 'Existente; conferir posição'),
    ('C06', 'AQ', 486, 698, 55, 'Água quente da pia', 'Não confirmada no memorial'),
    ('C07', 'E', 478, 690, 45, 'Esgoto da pia', 'Existente; conferir posição'),
    ('C08', 'T20', 528, 690, 92, 'Torre automática de tomadas 20 A na bancada (área seca)', 'Posição a definir'),
    ('C09', 'T', 539, 695, 190, 'Micro-ondas ME23P · 127 V', 'Aparelho escolhido'),
    ('C10', 'T', 560, 695, 110, 'Purificador PE12G', 'Aparelho escolhido'),
    ('C11', 'AF', 552, 698, 110, 'Água fria do purificador', 'Derivação a confirmar'),
    ('C12', 'T', 615, 695, 200, 'Geladeira IB6S', 'Aparelho escolhido'),
    ('C13', 'L', 521, 591, None, 'Plafon quadrado branco 3000 K', 'Formato aprovado; posição de estudo'),
    ('C14', 'A', 515, 680, 150, 'Luz regulável da bancada 3000 K, sob os aéreos', 'Comando independente com regulagem'),
    # Lavanderia
    ('L01', 'T', 350, 695, 110, 'Lavadora LG VC4 · 127 V', 'Aparelho escolhido'),
    ('L02', 'AF', 340, 698, 90, 'Água fria da lavadora', 'Existente; conferir posição'),
    ('L03', 'E', 362, 698, 80, 'Esgoto da lavadora', 'Existente; conferir posição'),
    ('L04', 'AF', 276, 698, 60, 'Água fria do tanque', 'Conferir posição'),
    ('L05', 'E', 288, 690, 40, 'Esgoto do tanque', 'Conferir posição'),
    ('L06', 'G', 268, 698, 140, 'Gás GN do aquecedor Rinnai E21', 'Aparelho escolhido; instalação a projetar'),
    ('L07', 'T', 290, 698, 150, 'Aquecedor E21 · alimentação elétrica', 'Conferir no manual'),
    ('L08', 'X', 279, 699, 215, 'Exaustão do aquecedor E21', 'Duto e saída a projetar'),
    ('L09', 'AQ', 284, 698, 140, 'Saída de água quente do E21 → banheiro e cozinha', 'Percurso oculto em estudo'),
    ('L10', 'T20', 305, 695, 100, 'Tomada fixa 20 A para air fryer e cafeteira', 'Posição a definir'),
    ('L11', 'L', 320, 595, None, 'Plafon branco 3000 K, fora da sombra do varal', 'Posição a testar'),
    # Banheiro
    ('B01', 'AF', 426, 526, 55, 'Água fria do lavatório', 'Existente; conferir'),
    ('B02', 'AQ', 442, 526, 55, 'Água quente do lavatório', 'Novo ramal; percurso em estudo'),
    ('B03', 'E', 434, 515, 45, 'Esgoto do lavatório', 'Existente; conferir'),
    ('B04', 'AF', 369, 526, 20, 'Água fria do vaso', 'Existente'),
    ('B05', 'AF', 396, 526, 60, 'Ducha higiênica · fria', 'Posição ilustrativa'),
    ('B06', 'AQ', 404, 526, 60, 'Ducha higiênica · quente', 'Novo ramal; E21 exige 3,9 L/min para ligar'),
    ('B07', 'AQ', 290, 526, 120, 'Chuveiro / misturador Livo (quente e fria)', 'Ponto existente; conferir'),
    ('B08', 'E', 295, 470, 0, 'Ralo do box', 'Existente'),
    ('B09', 'A', 434, 513, 190, 'Espelho 4000 K: Cristallux COB 2x550 mm /13,2 W', 'L02: Opus OPS31002 e perfil MOV; posição/montagem a validar'),
    ('B10', 'A', 434, 510, 230, 'Indireta 3000 K: Cristallux SMD até 2 m /9,6 W', 'L02: Opus OPS31002, comando próprio; trecho real a medir'),
    ('B11', 'L', 395, 450, None, 'Teto 3000 K: Galaxy Firefly 9605 /25 W /IP44', 'Selecionado L02; ponto e volumes a conferir'),
    # Sala
    ('S01', 'T', 505, 200, 30, 'Régua no compartimento ventilado: TV, PS5, soundbar', 'Posição de estudo'),
    ('S02', 'T', 505, 250, 120, 'TV 50″ atrás do painel', 'Altura a conferir'),
    ('S03', 'L', 617, 375, None, 'Luz geral da sala', 'Modelo a definir'),
    ('S04', 'L', 660, 455, None, 'Luz sobre a mesa Berlin', 'Modelo a definir'),
    # Escritório
    ('E01', 'T', 300, 5, 85, 'Bancada · notebook', 'Quantidade a definir'),
    ('E02', 'T', 440, 5, 85, 'Bancada · PC CH360, monitores', 'Quantidade a definir'),
    ('E03', 'T', 480, 176, 100, 'TV 43″ existente', 'Conferir'),
    ('E04', 'L', 370, 150, None, 'Luz geral do escritório', 'Modelo a definir'),
    # Quarto
    ('Q01', 'A', 5, 112, 110, 'Arandela branca compacta · lado 1', 'Comando independente'),
    ('Q02', 'A', 5, 288, 110, 'Arandela branca compacta · lado 2', 'Comando independente'),
    ('Q03', 'T', 5, 105, 60, 'Tomada de cabeceira · lado 1', 'Conferir'),
    ('Q04', 'T', 5, 295, 60, 'Tomada de cabeceira · lado 2', 'Conferir'),
    ('Q05', 'L', 122, 248, None, 'Plafon branco discreto 3000 K regulável', 'Escolhido'),
    ('Q06', 'A', 100, 330, 213, 'LED indireto nos aéreos', 'Perfil e fonte a definir'),
]

ROOM_LABEL = {'quarto': 'QUARTO', 'escritorio': 'ESCRITÓRIO', 'sala': 'SALA', 'cozinha': 'COZINHA', 'lavanderia': 'LAVANDERIA', 'banho': 'BANHEIRO'}

STYLE = {  # cor, rótulo da legenda
    'T': ('#2b6cb0', 'Tomada 127 V'), 'T20': ('#1a365d', 'Tomada 20 A'), 'D': ('#742a2a', 'Circuito exclusivo'),
    'L': ('#b7791f', 'Luz no teto'), 'A': ('#d69e2e', 'Luz de parede / indireta'),
    'AF': ('#3182ce', 'Água fria'), 'AQ': ('#e53e3e', 'Água quente'), 'E': ('#4a5568', 'Esgoto / ralo'),
    'G': ('#d69e2e', 'Gás GN'), 'X': ('#718096', 'Exaustão'),
}


def symbol(t, x, z):
    c = STYLE[t][0]
    if t in ('L',):
        return f'<circle cx="{x}" cy="{z}" r="7" fill="#fff" stroke="{c}" stroke-width="2"/><path d="M{x-5},{z-5}L{x+5},{z+5}M{x+5},{z-5}L{x-5},{z+5}" stroke="{c}" stroke-width="1.5"/>'
    if t == 'A':
        return f'<path d="M{x-6},{z+4}L{x},{z-6}L{x+6},{z+4}Z" fill="{c}"/>'
    if t in ('T', 'T20', 'D'):
        r = 5 if t == 'T' else 6
        extra = '' if t == 'T' else f'<circle cx="{x}" cy="{z}" r="2" fill="#fff"/>'
        return f'<rect x="{x-r}" y="{z-r}" width="{2*r}" height="{2*r}" fill="{c}"/>{extra}'
    if t == 'G':
        return f'<path d="M{x},{z-6}L{x+6},{z}L{x},{z+6}L{x-6},{z}Z" fill="{c}" stroke="#744210"/>'
    if t == 'X':
        return f'<circle cx="{x}" cy="{z}" r="5" fill="none" stroke="{c}" stroke-width="2" stroke-dasharray="2 2"/>'
    return f'<circle cx="{x}" cy="{z}" r="4.5" fill="{c}"/>'  # AF, AQ, E


def build():
    s = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="-40 -40 950 900" font-family="Arial, sans-serif">',
         '<rect x="-40" y="-40" width="950" height="900" fill="#fff"/>']
    for room, x, z, w, d, mat in floors:
        s.append(f'<rect x="{x}" y="{z}" width="{w}" height="{d}" fill="{FLOOR_FILL.get(mat, "#eee")}"/>')
    for name, x, z, w, d in FOOTPRINTS:
        s.append(f'<rect x="{x}" y="{z}" width="{w}" height="{d}" fill="none" stroke="#b9b2a6" stroke-dasharray="4 3"/>'
                 f'<text x="{x + w / 2}" y="{z + d / 2 + 3}" font-size="9" fill="#9a9285" text-anchor="middle">{escape(name)}</text>')
    for wall in walls:
        _, x, z, w, d = wall[:5]
        s.append(f'<rect x="{x}" y="{z}" width="{w}" height="{d}" fill="#4a5550"/>')
    seen = set()
    for room, x, z, w, d, _ in floors:
        if room in ROOM_LABEL and room not in seen:
            seen.add(room)
            s.append(f'<text x="{x + w / 2}" y="{z + d / 2 + 22}" font-size="13" font-weight="bold" fill="#a39a8c" text-anchor="middle" opacity=".8">{ROOM_LABEL[room]}</text>')
    taken = []  # caixas de rótulo já usadas (x0, y0, x1, y1)

    def free(b):
        return all(b[2] < o[0] or b[0] > o[2] or b[3] < o[1] or b[1] > o[3] for o in taken)

    strip = sorted((q for q in P if q[3] >= 685), key=lambda q: q[2])
    next_x = -1e9
    for i, (code, t, x, z, h, desc, st) in enumerate(strip):  # parede da cozinha/lavanderia: rótulos na faixa inferior
        lx = max(x - 11, next_x + 13)
        row = i % 2
        ly = 730 + row * 12
        next_x = lx
        s.append(f'<g><title>{code} · {escape(desc)} · {escape(st)}</title>{symbol(t, x, z)}'
                 f'<path d="M{x},{z + 5}L{lx + 11},{ly - 9}" stroke="#999" stroke-width=".6"/>'
                 f'<text x="{lx}" y="{ly}" font-size="9" font-weight="bold" fill="#222">{code}</text></g>')
    offsets = [(8, -6), (8, 12), (-30, -6), (-30, 12), (8, -18), (-30, -18), (8, 24), (-30, 24), (-11, -14), (-11, 22)]
    for code, t, x, z, h, desc, st in P:
        if z >= 685:
            continue
        taken.append((x - 6, z - 6, x + 6, z + 6))
    for code, t, x, z, h, desc, st in P:
        if z >= 685:
            continue
        for dx, dy in offsets:
            b = (x + dx, z + dy - 9, x + dx + 24, z + dy + 1)
            if free(b):
                break
        taken.append(b)
        s.append(f'<g><title>{code} · {escape(desc)} · {escape(st)}</title>{symbol(t, x, z)}'
                 f'<text x="{b[0]}" y="{b[3] - 1}" font-size="9" font-weight="bold" fill="#222">{code}</text></g>')
    # Legenda
    ly = 790
    s.append(f'<text x="0" y="{ly - 12}" font-size="13" font-weight="bold">Planta de pontos preliminar R00 · Guedala Park · sem escala de execução</text>')
    for i, (t, (c, label)) in enumerate(STYLE.items()):
        lx = (i % 5) * 180
        y = ly + 10 + (i // 5) * 22
        s.append(symbol(t, lx + 6, y) + f'<text x="{lx + 18}" y="{y + 4}" font-size="11">{label}</text>')
    s.append(f'<text x="0" y="{ly + 62}" font-size="10" fill="#7a2e2e">Estudo para o responsável técnico. Posições derivadas do modelo R45, não do apartamento. Não executar.</text>')
    s.append('</svg>')
    svg = '\n'.join(s)
    (HERE / 'Planta_pontos_R00.svg').write_text(svg, encoding='utf-8')

    rows = '\n'.join(f'| {c} | {STYLE[t][1]} | {escape(d)} | {"teto" if h is None else f"{h} cm"} | {escape(st)} |' for c, t, x, z, h, d, st in P)
    md = (HERE / 'README.md')
    head = md.read_text(encoding='utf-8').split('<!-- TABELA -->')[0]
    md.write_text(head + '<!-- TABELA -->\n\n| Código | Tipo | Ponto | Altura de referência | Situação |\n|---|---|---|---|---|\n' + rows + '\n', encoding='utf-8')
    print(len(P), 'pontos')


if __name__ == '__main__':
    build()
