"""Verify deliverable dimensions, original hashes, PDF text/images and gallery links."""
from pathlib import Path
from hashlib import sha256
from html.parser import HTMLParser
import json
from PIL import Image
from pypdf import PdfReader

OUT=Path(__file__).resolve().parents[2]/'09_Referencias'
m=json.loads((OUT/'Moodboard.json').read_text(encoding='utf-8'))
assert len(m['cenas'])==12
for scene in m['cenas']:
    p=OUT/scene['arquivo']
    assert sha256(p.read_bytes()).hexdigest()==scene['sha256'],p
    for q in [p,p.with_name(p.stem+'_web.webp')]:
        with Image.open(q) as im: assert im.size==(1536,1024),q
for mode in ['Dia','Noite']:
    for suffix,size in [('',(3840,2160)),('_leve',(2000,1125))]:
        with Image.open(OUT/f'Moodboard_{mode}{suffix}.png') as im: assert im.size==size
for filename,count in [('Moodboard_paineis.pdf',2),('Moodboard_ambientes_A3.pdf',6)]:
    pdf=PdfReader(OUT/filename);assert len(pdf.pages)==count
    for page in pdf.pages:
        text=page.extract_text();assert m['aviso'] in text
        assert 'GUEDALA PARK' in text
        assert 'Aparência aprovada em 28/10/2026' in text
        assert not any(note in text for note in ['Todos os seis ambientes aprovados','Cenas nativas','Cenas completas','1536'])
        images=[obj.get_object() for obj in page['/Resources']['/XObject'].values()]
        assert len(images)==(6 if count==2 else 2)
        assert all((im['/Width'],im['/Height'])==(1536,1024) for im in images)
        if count==6:
            assert abs(float(page.mediabox.width)-841.89)<.01
            assert abs(float(page.mediabox.height)-1190.551)<.01
class Links(HTMLParser):
    sliders=0
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if tag=='input' and attrs.get('type')=='range':self.sliders+=1
        for key in ['src','href']:
            value=attrs.get(key,'')
            if value and not value.startswith(('#','http')):assert (OUT/value).exists(),value
p=Links();p.feed((OUT/'Moodboard.html').read_text(encoding='utf-8'));assert p.sliders==6
print('OK: 12 cenas e hashes; PNG 4K/2000 px; 2 painéis PDF; 6 páginas A3, texto vetorial e imagens originais; 6 controles e links locais.')
