"""Planta dos contatos nominais extraidos, sem mudar o modelo."""
from pathlib import Path
import json
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent
data=json.loads((HERE/'Geometria_R51.json').read_text(encoding='utf8'))
im=Image.new('RGB',(1600,730),'#f6f3ed');d=ImageDraw.Draw(im)
font=lambda n:ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',n)
d.text((45,25),'P20 · caminho nominal da carga com as tampas fechadas',fill='#223735',font=font(31))
d.text((45,73),'R51 preservada · almofadas não desenhadas · dimensões nominais em mm',fill='#485956',font=font(21))
scale=.79;ox=72;oy=175
def xy(x,y):return ox+(y-3750)*scale,oy+(550-x)*scale
def rect(b):
 a=xy(b[0],b[3]);c=xy(b[2],b[1]);return [min(a[0],c[0]),min(a[1],c[1]),max(a[0],c[0]),max(a[1],c[1])]
for lid in data['lids']:
 b=lid['box'];d.rectangle(rect([b[0],b[1],b[3],b[4]]),fill='#e9e2d5',outline='#223735',width=3)
for c in data['contacts']:
 color='#b37529' if c['support'].startswith('Ref_Sarrafo') else '#367d75'
 d.rectangle(rect(c['rectangle_global_mm']),fill=color)
for y,label in [(3751,'Tampa maior · 971 × 448'),(4724,'Tampa menor · 825 × 448')]:
 d.text((xy(0,y)[0]+18,137),label,fill='#223735',font=font(22))
for y,text in [(4139,'D1'),(4507,'D2'),(4723,'D3')]:
 x,_=xy(0,y);d.text((x-15,545),text,fill='#223735',font=font(19))
d.text((74,112),'frente ↑',fill='#223735',font=font(17))
d.text((74,537),'trás / fundo',fill='#223735',font=font(17))
d.rectangle((72,594,95,617),fill='#367d75');d.text((108,590),'10 contatos principais: frente, fundo, duas extremidades e divisórias',fill='#223735',font=font(21))
d.rectangle((72,632,95,655),fill='#b37529');d.text((108,628),'8 contatos adicionais nos sarrafos: não creditados no cálculo principal',fill='#223735',font=font(21))
d.text((72,679),'Apoio no desenho ≠ ligação resistente. Corpo, piso, material real e ensaio ainda condicionam o conjunto.',fill='#674a36',font=font(20))
im.save(HERE/'Mapa_contatos.png')
print('Mapa_contatos.png')
