"""Caderno de pranchas R01: HTML para imprimir em A3 paisagem, com carimbo.

Reúne desenhos já gerados no projeto; não desenha nada novo. Para atualizar, gere
os desenhos de origem e rode: python gerar_caderno_pranchas.py
"""
from pathlib import Path
from html import escape
from datetime import date

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent  # guedala-park
DATA = date.today().strftime('%d/%m/%Y')

# (número, título, conteúdo, arquivo relativo a guedala-park, observação)
PRANCHAS = [
    ('01', 'Planta cotada — paredes e medidas da planta oficial', 'img', '06_Entregas/Planta_cotada/Planta_cotada.svg',
     'Cotas da planta oficial da Cury; paredes e aberturas reconstituídas. Medidas não conferidas no imóvel.'),
    ('02', 'Planta de layout — mobiliário', 'img', '03_Ambientes/Planta_mobiliada/Planta_mobiliada_R02.png',
     'Geometria FreeCAD R45, cores aproximadas.'),
    ('03', 'Planta de pontos — elétrica, iluminação, água, esgoto e gás', 'img', '03_Ambientes/Planta_pontos/Planta_pontos_R00.svg',
     'R01: 50 pontos auditados +3 funções; D03/D04/D06 integradas. E06 adiada; Q06/S05/E05 sem posição. Circuitos e implantação pelo RT.'),
    ('04', 'Vistas — sala e jantar · quarto', 'pair', ('03_Ambientes/Planta_mobiliada/Vistas/01_Sala_e_jantar.png', '03_Ambientes/Planta_mobiliada/Vistas/02_Quarto.png'),
     'Perspectivas isométricas do modelo R45.'),
    ('05', 'Vistas — escritório · cozinha', 'pair', ('03_Ambientes/Planta_mobiliada/Vistas/03_Escritorio.png', '03_Ambientes/Planta_mobiliada/Vistas/04_Cozinha.png'),
     'Perspectivas isométricas do modelo R45.'),
    ('06', 'Vistas — lavanderia · banheiro', 'pair', ('03_Ambientes/Planta_mobiliada/Vistas/05_Lavanderia.png', '03_Ambientes/Planta_mobiliada/Vistas/06_Banheiro.png'),
     'Perspectivas isométricas do modelo R45.'),
]


def rel(path):
    return '../../' + path


def carimbo(num, titulo, obs):
    return f'''<div class="carimbo">
  <div class="c-proj"><b>GUEDALA PARK</b><span>Projeto de interiores · Cury Guedala Park III · Torre 2 · final 06 · 40,18 m²</span></div>
  <div class="c-tit"><small>Prancha</small><b>{escape(titulo)}</b><span>{escape(obs)}</span></div>
  <div class="c-meta">
    <div><small>Nº</small><b>{num}/{len(PRANCHAS):02d}</b></div>
    <div><small>Revisão</small><b>R01</b></div>
    <div><small>Data</small><b>{DATA}</b></div>
    <div><small>Escala</small><b>Sem escala</b></div>
  </div>
  <div class="c-rt"><small>Responsável técnico</small><b>[nome · CAU/CREA · RRT/ART]</b><span class="aviso">ESTUDO — NÃO EXECUTAR</span></div>
</div>'''


def build():
    pages = []
    for num, titulo, kind, src, obs in PRANCHAS:
        if kind == 'img':
            body = f'<div class="desenho"><img src="{rel(src)}" alt="{escape(titulo)}"></div>'
        else:
            body = '<div class="desenho par">' + ''.join(f'<img src="{rel(s)}" alt="">' for s in src) + '</div>'
        pages.append(f'<section class="prancha">{body}{carimbo(num, titulo, obs)}</section>')
    indice = ''.join(f'<tr><td>{n}</td><td>{escape(t)}</td></tr>' for n, t, *_ in PRANCHAS)
    capa = f'''<section class="prancha capa">
  <div class="capa-txt"><h1>Guedala Park</h1><p>Projeto de interiores · caderno de pranchas R01 · {DATA}</p>
  <table><thead><tr><th>Nº</th><th>Prancha</th></tr></thead><tbody>{indice}</tbody></table>
  <p class="nota">Documentos complementares: programa de necessidades R01, caderno de especificações R01, fichas de fabricação R15,
  cronograma R00 e plano de reforma (rascunho), na pasta do projeto. Estudo preliminar para o responsável técnico:
  medidas a conferir no imóvel; não executar. Esta revisão integra a planta de pontos R01 e as decisões D03/D04/D06 de 27/10. Layout e vistas permanecem referências R45; não representam a geometria R53. Modelo FCStd preservado.</p></div>
  {carimbo('00', 'Capa e índice', 'R01 parcial: planta de pontos atualizada; layout e vistas continuam R45, sem validação contra R53.')}
</section>'''
    html = f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Guedala Park · Pranchas R01</title>
<style>
@page {{ size: A3 landscape; margin: 8mm; }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; font-family: Arial, Helvetica, sans-serif; color: #222; background: #ddd; }}
.prancha {{ width: 404mm; height: 281mm; margin: 10mm auto; background: #fff; border: 1.5px solid #222; padding: 6mm;
  display: flex; flex-direction: column; page-break-after: always; break-after: page; }}
.desenho {{ flex: 1; display: flex; align-items: center; justify-content: center; min-height: 0; }}
.desenho img {{ max-width: 100%; max-height: 100%; object-fit: contain; }}
.desenho.par img {{ max-width: 49%; margin: 0 .5%; }}
.carimbo {{ display: grid; grid-template-columns: 2fr 3fr 2.2fr 2fr; border: 1.2px solid #222; height: 30mm; font-size: 9pt; }}
.carimbo > div {{ border-left: 1px solid #222; padding: 2mm 3mm; display: flex; flex-direction: column; gap: 1mm; }}
.carimbo > div:first-child {{ border-left: 0; }}
.carimbo small {{ color: #666; font-size: 7pt; text-transform: uppercase; letter-spacing: .05em; }}
.carimbo b {{ font-size: 11pt; }}
.c-proj b {{ font-size: 15pt; letter-spacing: .08em; }}
.c-meta {{ display: grid !important; grid-template-columns: 1fr 1fr; }}
.c-meta div {{ display: flex; flex-direction: column; }}
.aviso {{ color: #9b1c1c; font-weight: bold; margin-top: auto; }}
.capa-txt {{ flex: 1; padding: 20mm 30mm; }}
.capa h1 {{ font-size: 40pt; letter-spacing: .1em; margin: 0 0 4mm; }}
.capa table {{ border-collapse: collapse; margin: 10mm 0; font-size: 13pt; }}
.capa td, .capa th {{ border-bottom: 1px solid #aaa; padding: 2mm 8mm 2mm 0; text-align: left; }}
.nota {{ max-width: 220mm; color: #444; line-height: 1.5; }}
@media print {{ body {{ background: #fff; }} .prancha {{ margin: 0; width: auto; height: 277mm; border: 1.5px solid #222; }} }}
</style></head><body>
{capa}
{''.join(pages)}
</body></html>'''
    (HERE / 'index.html').write_text(html, encoding='utf-8')
    missing = [s for *_, src, _ in PRANCHAS for s in ([src] if isinstance(src, str) else src) if not (ROOT / s).exists()]
    print('pranchas:', len(PRANCHAS) + 1, 'faltando:', missing)


if __name__ == '__main__':
    build()
