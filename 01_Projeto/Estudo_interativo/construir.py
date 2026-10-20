from pathlib import Path
import base64

root=Path(__file__).resolve().parent
src=root/'src'
html=(src/'shell.html').read_text(encoding='utf-8')
for name,token in [('app.css','/*CSS*/'),('experience.css','/*EXPERIENCE_CSS*/'),('experience.js','/*EXPERIENCE_JS*/'),('data.js','/*DATA*/'),('cad-data.js','/*CAD_DATA*/'),('cad-sync.js','/*CAD_SYNC*/'),('lighting.js','/*LIGHTING*/'),('depth-renderer.js','/*DEPTH*/'),('app.js','/*APP*/')]:
    html=html.replace(token,(src/name).read_text(encoding='utf-8'))
wardrobe=root/'Consolidacao_R11_2026-10-20/Guarda_roupa_R31.svg'
ward='data:image/svg+xml;base64,'+base64.b64encode(wardrobe.read_bytes()).decode('ascii')
html=html.replace('/*WARDROBE*/',ward)
details={}
for key,path in [('oven',root.parent/'Cozinha/Fischer_Grill_2026-10-19/Grelhas_manutencao_R02/Grelhas_manutencao.png'),('bench',root.parent/'Sala_e_jantar/Retirada_ponta_R30/R02_pagina.png')]:
    details[key]='data:image/png;base64,'+base64.b64encode(path.read_bytes()).decode('ascii')
html=html.replace('/*DETAILS_IMAGES*/','globalThis.GUEDALA_DETAILS='+__import__('json').dumps(details)+';')
(root/'Guedala_Park_Interativo.html').write_text(html,encoding='utf-8')
# Same self-contained artifact with the moodboard active after initialization.
board=html.replace('init();\n','init();\ntab("mood");\n')
(root.parent.parent/'03_Referencias'/'Moodboard_atualizado_R01.html').write_text(board,encoding='utf-8')
print(f'HTML principal: {len(html.encode("utf-8")):,} bytes; moodboard atualizado.')
