from pathlib import Path
import base64
import runpy
from plain_language import plain_html
from height_data import build as build_heights
from build_field_data import build as build_field_data
from build_work_data import build as build_work_data

root=Path(__file__).resolve().parent
src=root/'src'
height_text=build_heights()
build_field_data()
build_work_data()
runpy.run_path(str(root/'build_floorplan.py'))['build']()
runpy.run_path(str(root/'build_visual_finishes.py'))['build']()
html=plain_html((src/'shell.html').read_text(encoding='utf-8')).replace('{{HEIGHT_STUDY}}',height_text)
html=html.replace('</style>',(src/'workshop.css').read_text(encoding='utf-8')+'\n</style>')
html=html.replace('</style>',(src/'field.css').read_text(encoding='utf-8')+'\n</style>')
html=html.replace('</style>',(src/'work.css').read_text(encoding='utf-8')+'\n</style>')
html=html.replace('</body>', '<script>'+(src/'workshop-docs.js').read_text(encoding='utf-8')+'\n'+(src/'workshop.js').read_text(encoding='utf-8')+'\n'+(src/'fabrication-ui.js').read_text(encoding='utf-8')+'\n'+(src/'floorplan-ui.js').read_text(encoding='utf-8')+'</script></body>')
html=html.replace('</body>','<script>'+ '\n'.join((src/n).read_text(encoding='utf-8') for n in ('field-data.js','field-core.js','field-ui.js'))+'</script></body>')
html=html.replace('</body>','<script>'+ '\n'.join((src/n).read_text(encoding='utf-8') for n in ('work-data.js','work-core.js','work-ui.js'))+'</script></body>')
for name,token in [('app.css','/*CSS*/'),('experience.css','/*EXPERIENCE_CSS*/'),('experience.js','/*EXPERIENCE_JS*/'),('data.js','/*DATA*/'),('cad-data.js','/*CAD_DATA*/'),('cad-sync.js','/*CAD_SYNC*/'),('lighting.js','/*LIGHTING*/'),('depth-renderer.js','/*DEPTH*/'),('app.js','/*APP*/')]:
    content=(src/name).read_text(encoding='utf-8')
    if name=='cad-sync.js':content=(src/'visual-finishes.js').read_text(encoding='utf-8')+'\n'+(src/'site-copy.js').read_text(encoding='utf-8')+'\n'+content
    html=html.replace(token,content)

details={}
for key,path in [('oven',root.parent.parent/'03_Ambientes/Cozinha/Fischer_Grill/Grelhas_manutencao/Grelhas_manutencao.png')]:
    details[key]='data:image/png;base64,'+base64.b64encode(path.read_bytes()).decode('ascii')
html=html.replace('/*DETAILS_IMAGES*/','globalThis.GUEDALA_DETAILS='+__import__('json').dumps(details)+';')
(root/'Guedala_Park_Interativo.html').write_text(html,encoding='utf-8')
# Same self-contained artifact with the moodboard active after initialization.
board=html.replace('init();\n','init();\ntab("mood");\n')
(root.parent.parent/'09_Referencias'/'Moodboard_atualizado_R01.html').write_text(board,encoding='utf-8')
print(f'HTML principal: {len(html.encode("utf-8")):,} bytes; moodboard atualizado.')
