"""Planta de trajetoria e apoios do estudo; nenhuma edicao do projeto."""
from pathlib import Path
import json,math
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent
g=json.loads((HERE/'Geometria_R51.json').read_text(encoding='utf8'))
s=json.loads((HERE.parent/'Bancada_marcenaria_2026-10-25/Resultados.json').read_text(encoding='utf8'))
r=json.loads((HERE/'Estabilidade.json').read_text(encoding='utf8'))
im=Image.new('RGB',(1580,1030),'#f5f2ec');d=ImageDraw.Draw(im)
font=lambda n:ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',n)
d.text((45,25),'P16 · curso das gavetas e apoios da bancada',fill='#233e39',font=font(32))
d.text((45,77),'Planta nominal · estudo de marcenaria separado · duas gavetas projetadas na mesma faixa, em alturas diferentes',fill='#4f635a',font=font(21))
def xy(x,y):return 75+(x-2700)*.58,165+y*.58
def rectangle(x,y,sx,sy,**kw):d.rectangle([xy(x,y),xy(x+sx,y+sy)],**kw)
rectangle(2700,0,2000,700,fill='#e0d7c5',outline='#6c7769',width=2)
h=r['hulls_mm']['whole'];d.line([xy(*p) for p in h]+[xy(*h[0])],fill='#397c68',width=4)
for p in s['panels']:
 if p['origin_mm'][2]==0:rectangle(*p['origin_mm'][:2],*p['size_mm'][:2],fill='#397c68')
rectangle(4300,250,400,430,fill='#b7bfb5',outline='#526d62',width=2)
rectangle(4301,292,398,808,outline='#ad7927',width=4)
rectangle(4301,1082,398,18,fill='#ad7927')
for y in (0,700):
 a=xy(2700,y);d.text((a[0]+15,a[1]+10),'fundo' if y==0 else 'frente do tampo · Y700',fill='#415c52',font=font(20))
d.text((xy(4315,320)[0],xy(4315,320)[1]),'fechadas',fill='#334f45',font=font(20))
d.text((xy(4315,940)[0],xy(4315,940)[1]),'abertas',fill='#885b1e',font=font(20))
aa=xy(4770,682);bb=xy(4770,1082);d.line((aa,bb),fill='#ad7927',width=4)
d.polygon([bb,(bb[0]-8,bb[1]-15),(bb[0]+8,bb[1]-15)],fill='#ad7927')
d.text((aa[0]+18,(aa[1]+bb[1])/2-15),'400 mm',fill='#885b1e',font=font(23))
d.text((45,850),'Verde: contatos nominais no piso e seu polígono. Âmbar: volume de varredura projetado do curso0–400 mm.',fill='#425d51',font=font(22))
d.text((45,892),'18.480 pares de caixas varridas +64 pares entre gavetas: separados no escopo testado.',fill='#425d51',font=font(22))
d.text((45,934),'Guias telescópicas reais, tolerâncias, juntas, massa do tampo e estabilidade ainda condicionam o conjunto.',fill='#805733',font=font(22))
im.save(HERE/'Planta_movimento_apoios.png');print('Planta_movimento_apoios.png')
