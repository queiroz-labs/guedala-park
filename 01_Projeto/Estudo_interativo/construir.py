from pathlib import Path
import base64

root=Path(__file__).resolve().parent
src=root/'src'
html=(src/'shell.html').read_text(encoding='utf-8')
for name,token in [('app.css','/*CSS*/'),('data.js','/*DATA*/'),('depth-renderer.js','/*DEPTH*/'),('app.js','/*APP*/')]:
    html=html.replace(token,(src/name).read_text(encoding='utf-8'))
wardrobe=root.parent/'Portas_e_quarto'/'Guarda_roupa_interior_R02.svg'
ward='data:image/svg+xml;base64,'+base64.b64encode(wardrobe.read_bytes()).decode('ascii')
html=html.replace('/*WARDROBE*/',ward)
(root/'Guedala_Park_Interativo.html').write_text(html,encoding='utf-8')
# Same self-contained artifact with the moodboard active after initialization.
board=html.replace('init();\n','init();\ntab("mood");\n')
(root.parent.parent/'03_Referencias'/'Moodboard_atualizado_R01.html').write_text(board,encoding='utf-8')
print(f'HTML principal: {len(html.encode("utf-8")):,} bytes; moodboard atualizado.')
