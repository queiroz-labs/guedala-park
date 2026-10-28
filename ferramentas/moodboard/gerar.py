"""Compose approved images; never regenerate or upscale scenes. Python + Pillow/ReportLab + Poppler."""
from pathlib import Path
import hashlib
import html
import json
import shutil
import subprocess
import tempfile
from io import BytesIO
from functools import lru_cache
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A3, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
import reportlab

FONT_DIR = Path(reportlab.__file__).parent / 'fonts'
pdfmetrics.registerFont(TTFont('Mood', str(FONT_DIR/'Vera.ttf')))
pdfmetrics.registerFont(TTFont('Mood-Bold', str(FONT_DIR/'VeraBd.ttf')))

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / '09_Referencias'
NOTICE = 'Imagens ilustrativas de aparência; medidas nas plantas e fichas.'
ROOMS = [
    dict(id='Sala', name='Sala e jantar', caption='Arenza liso, suede areia e piso em tom mel.',
         light='Jabuticaba sobre a mesa; Jurerê suave e indireta sobre a TV.',
         materials=[('Arenza liso','#b8aa94'),('Suede Areia','#c9bda8'),('Vinílico Olmo','#b98b59'),('Algodão Egípcio','#e9e0ce')]),
    dict(id='Cozinha', name='Cozinha', caption='Azul Petróleo fechado, Arenza e Branco Itaúnas.',
         light='Plafon e luz de bancada sob os aéreos, aproximadamente 3000 K.',
         materials=[('Azul Petróleo','#344c4e'),('Arenza liso','#b8aa94'),('Branco Itaúnas','#e4dbca'),('Inox Look','#a9aaa7')]),
    dict(id='Lavanderia', name='Lavanderia', caption='Arenza liso, pedra clara e cerâmica no piso.',
         light='Plafon como única fonte, aproximadamente 3000 K.',
         materials=[('Arenza liso','#b8aa94'),('Branco Itaúnas','#e4dbca'),('Cerâmica clara','#ddd8cd'),('Inox Look','#a9aaa7')]),
    dict(id='Quarto', name='Quarto', caption='Arenza e suede areia; queen com baú no cenário futuro.',
         light='Plafon Elgin, indireta sob o aéreo e duas arandelas, ~3000 K.',
         materials=[('Arenza liso','#b8aa94'),('Suede Areia','#c9bda8'),('Vinílico Olmo','#b98b59'),('Tecido oliva','#777c5d')]),
    dict(id='Escritorio', name='Escritório', caption='Aéreo Marfim O2, Arenza e sofá Daiane cinza-claro.',
         light='Geral ~3000 K; indireta nos consoles e leve azul atrás da TV.',
         materials=[('Marfim O2','#e8e2d2'),('Arenza liso','#b8aa94'),('Tecido cinza','#bcbcb6'),('Azul Petróleo','#344c4e')]),
    dict(id='Banheiro', name='Banheiro', caption='Beige Matt e Freijó; verde apenas na parede do chuveiro.',
         light='Teto e indireta 3000 K; espelho 4000 K, três comandos.',
         materials=[('Beige Matt','#c4b49d'),('Louro Freijó','#b08a62'),('Vivant Sauge','#73765b'),('Travertino Greige','#c6b8a2')]),
]
PALETTE = [('Off-white','#e9e0ce'),('Areia','#c9bda8'),('Arenza','#b8aa94'),('Petróleo','#344c4e'),('Sauge','#73765b'),('Mel / Freijó','#b98b59'),('Preto fosco','#292b29')]

@lru_cache(maxsize=12)
def pdf_image(path):
    # Preserve all 1536 x 1024 pixels; JPEG avoids oversized PDF lossless streams.
    data=BytesIO()
    with Image.open(path) as im:
        im.convert('RGB').save(data,format='JPEG',quality=95,subsampling=0,optimize=True)
    data.seek(0)
    return ImageReader(data)

class Sheet:
    def __init__(self, c, width, height):
        self.c, self.w, self.h = c, width, height
    def text(self, x, y, value, size=24, bold=False, color='#252b28'):
        self.c.setFillColor(HexColor(color))
        self.c.setFont('Mood-Bold' if bold else 'Mood', size)
        self.c.drawString(x, self.h-y-size*.82, value)
    def rect(self, x, y, w, h, color):
        self.c.setFillColor(HexColor(color))
        self.c.rect(x,self.h-y-h,w,h,fill=1,stroke=0)
    def picture(self, p, x, y, w, h):
        self.c.drawImage(pdf_image(p),x,self.h-y-h,width=w,height=h)
    def swatches(self, items, x, y, width, size=22, height=30, gap=14):
        slot=(width-gap*(len(items)-1))/len(items)
        for i,(label,color) in enumerate(items):
            self.rect(x+i*(slot+gap),y,slot,height,color)
            self.text(x+i*(slot+gap),y+height+8,label,size)

def panels():
    path=OUT/'Moodboard_paineis.pdf'
    c=canvas.Canvas(str(path),pagesize=(1280,720),pageCompression=1)
    c.setTitle('Guedala Park | Moodboard Dia e Noite')
    for mode in ['dia','noite']:
        c.saveState(); c.scale(1/3,1/3)
        s=Sheet(c,3840,2160)
        s.rect(0,0,3840,2160,'#fafaf7')
        s.text(96,66,'GUEDALA PARK',70,True)
        s.text(96,154,'MOODBOARD  /  '+mode.upper(),30)
        s.text(96,202,'Aparência aprovada em 28/10/2026',24)
        s.swatches(PALETTE,1740,94,2004,24,46,20)
        s.text(1740,192,'Amostras de cor aproximadas.',24)
        for i,r in enumerate(ROOMS):
            x=96+(i%3)*1248; y=280+(i//3)*920
            s.text(x,y,f'{i+1:02d}  {r["name"]}',36,True)
            s.picture(OUT/f'{r["id"]}_{mode}.png',x+67,y+54,1050,700)
            s.swatches(r['materials'],x+67,y+770,1050,21,24)
            s.text(x+67,y+830,r['caption'],22)
        s.rect(96,2080,3648,2,'#bcbeb7')
        s.text(96,2110,NOTICE,26)
        c.restoreState(); c.showPage()
    c.save()
    poppler=shutil.which('pdftoppm')
    if not poppler: raise RuntimeError('Instale Poppler e adicione pdftoppm ao PATH.')
    with tempfile.TemporaryDirectory(prefix='guedala_moodboard_') as temp:
        for page,mode in enumerate(['Dia','Noite'],1):
            prefix=Path(temp)/mode
            subprocess.run([poppler,'-f',str(page),'-l',str(page),'-scale-to-x','3840','-scale-to-y','2160','-png','-singlefile',str(path),str(prefix)],check=True)
            with Image.open(prefix.with_suffix('.png')) as im:
                im.save(OUT/f'Moodboard_{mode}.png',optimize=True)
                im.resize((2000,1125),Image.Resampling.LANCZOS).save(OUT/f'Moodboard_{mode}_leve.png',optimize=True)

def a3():
    w,h=A3
    c=canvas.Canvas(str(OUT/'Moodboard_ambientes_A3.pdf'),pagesize=(w,h),pageCompression=1)
    c.setTitle('Guedala Park | Seis ambientes | Dia e noite | A3')
    for i,r in enumerate(ROOMS):
        s=Sheet(c,w,h);s.rect(0,0,w,h,'#fafaf7')
        s.text(36,20,'GUEDALA PARK / MOODBOARD',10,True)
        s.text(36,39,r['name'],28,True)
        s.text(w-152,24,f'{i+1:02d} / 06    •    A3',12)
        imagew=680; imageh=imagew*2/3
        for j,mode in enumerate(['dia','noite']):
            x=(w-imagew)/2; y=89+j*480
            s.text(x,y-19,mode.upper(),12,True)
            s.picture(OUT/f'{r["id"]}_{mode}.png',x,y,imagew,imageh)
        x=(w-imagew)/2
        s.swatches(r['materials'],x,1036,imagew,11,23,16)
        s.text(x,1090,r['caption'],17)
        s.text(x,1117,r['light'],14)
        s.text(x,1145,'Aparência aprovada em 28/10/2026',11)
        s.text(w-260,1145,'Amostras de cor aproximadas.',10)
        s.rect(36,h-29,w-72,.7,'#bcbeb7')
        s.text(36,h-20,NOTICE,10)
        c.showPage()
    c.save()

def gallery():
    template=(Path(__file__).parent/'galeria.html').read_text(encoding='utf-8')
    cards=[]
    for i,r in enumerate(ROOMS):
        key=r['id']; esc=html.escape
        samples=''.join(f'<li><span style="background:{color}"></span>{esc(label)}</li>' for label,color in r['materials'])
        cards.append(f'''<article aria-labelledby="title-{key}">
<h2 id="title-{key}"><small>{i+1:02d}</small> {esc(r['name'])}</h2>
<div class="compare" style="--split:50%" id="view-{key}">
<img src="{key}_noite_web.webp" alt="{esc(r['name'])}: noite aprovada" width="1536" height="1024" loading="lazy">
<img class="day" src="{key}_dia_web.webp" alt="{esc(r['name'])}: dia aprovado" width="1536" height="1024" loading="lazy">
<span class="tag daytag" aria-hidden="true">Dia</span><span class="tag nighttag" aria-hidden="true">Noite</span><span class="divider" aria-hidden="true">↔</span></div>
<label class="control" for="range-{key}"><span>Dia / Noite</span><input id="range-{key}" type="range" min="0" max="100" value="50" aria-label="Comparar dia e noite: {esc(r['name'])}" aria-controls="view-{key}" aria-valuetext="50% dia, 50% noite"><output for="range-{key}">50% dia</output></label>
<ul class="samples">{samples}</ul><p>{esc(r['caption'])}</p><p class="lighting">{esc(r['light'])}</p>
<div class="originals"><a href="{key}_dia.png">Abrir dia completo</a><a href="{key}_noite.png">Abrir noite completa</a></div></article>''')
    palette=''.join(f'<span><i style="background:{color}"></i>{html.escape(label)}</span>' for label,color in PALETTE)
    (OUT/'Moodboard.html').write_text(template.replace('{{CARDS}}','\n'.join(cards)).replace('{{PALETTE}}',palette).replace('{{NOTICE}}',NOTICE),encoding='utf-8')

def main():
    records=[]
    for r in ROOMS:
        for mode in ['dia','noite']:
            p=OUT/f'{r["id"]}_{mode}.png'
            with Image.open(p) as im:
                if im.size != (1536,1024): raise ValueError(f'Dimensões inesperadas: {p.name} {im.size}')
                im.convert('RGB').save(OUT/f'{r["id"]}_{mode}_web.webp',quality=90,method=6)
            records.append(dict(arquivo=p.name,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),largura=1536,altura=1024))
    panels();a3();gallery()
    manifest=dict(aprovacao=dict(data='28/10/2026',rotulo='Aparência aprovada em 28/10/2026',fonte='Conversa do moodboard; citações específicas no README.md'),aviso=NOTICE,cenas=records,paineis=dict(largura=3840,altura=2160,cena_largura=1050,cena_altura=700,ampliacao=False),amostras='Cores digitais aproximadas, não amostras comerciais',ambientes=ROOMS)
    (OUT/'Moodboard.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('2 painéis 4K + 2 PNG leves + PDF de 2 painéis + 6 páginas A3 + galeria gerados.')

if __name__=='__main__': main()
