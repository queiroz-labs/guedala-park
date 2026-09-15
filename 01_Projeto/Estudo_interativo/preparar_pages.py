"""Build a small, explicit GitHub Pages artifact from the project sources."""
from pathlib import Path
import json
import os
import runpy
import shutil

study = Path(__file__).resolve().parent
root = study.parent.parent
site = root / '.site'
runpy.run_path(str(study / 'construir.py'), run_name='__main__')
site.mkdir(exist_ok=True)
(site / 'moodboard').mkdir(exist_ok=True)

for source, destination, image_path in [
    (study / 'Guedala_Park_Interativo.html', site / 'index.html', 'moodboard.png'),
    (root / '03_Referencias/Moodboard_atualizado_R01.html', site / 'moodboard/index.html', '../moodboard.png'),
]:
    html = source.read_text(encoding='utf-8')
    marker = '<h2 class="material-title">Biblioteca de materiais</h2>'
    assert marker in html
    html = html.replace(marker, '<p><a href="'+image_path+'" target="_blank" rel="noopener">Abrir painel visual de materiais</a></p>'+marker)
    destination.write_text(html, encoding='utf-8')

shutil.copyfile(root / '03_Referencias/Moodboard_visual_atualizado_R01.png', site / 'moodboard.png')
(site / '.nojekyll').write_text('', encoding='utf-8')
(site / 'versao.json').write_text(json.dumps({'revisao':'R04','commit':os.environ.get('GITHUB_SHA','local')}, indent=2)+'\n', encoding='utf-8')

expected = {'index.html', 'moodboard/index.html', 'moodboard.png', '.nojekyll', 'versao.json'}
actual = {p.relative_to(site).as_posix() for p in site.rglob('*') if p.is_file()}
if actual != expected:
    raise SystemExit('A pasta .site contem arquivos inesperados; revisar antes de publicar.')
print('Pages preparado: HTML, moodboard e imagem de materiais.')
