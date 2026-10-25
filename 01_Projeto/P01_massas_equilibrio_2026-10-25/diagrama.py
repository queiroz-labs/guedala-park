from pathlib import Path
import json
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;d=json.loads((HERE/'Resultados.json').read_text(encoding='utf8'))
im=Image.new('RGB',(1400,900),'#f5f3ed');dr=ImageDraw.Draw(im)
font=lambda size:ImageFont.truetype('C:/Windows/Fonts/arial.ttf',size)
def txt(p,s,size=24,color='#243d3b'):dr.text(p,s,font=font(size),fill=color)
txt((60,38),'P01 | APOIOS NOMINAIS E MASSAS',36)
txt((60,92),'Estudo separado: soco R01 + prateleiras723. Sem alteração da R51.',23)
txt((60,148),'PLANTA DO CONTATO COM O PISO — 23 REGIÕES',22)
x0,y0,scale=95,210,.57
def point(x,y):return x0+(x-5390)*scale,y0+(3940-y)*scale
dr.rectangle([point(5390,3940),point(7390,3290)],outline='#b5bab2',width=2)
for r in d['nominal_floor_parts']:
 x,y=r['xy_mm'];a,b=r['size_mm'];col='#b47b40' if r['name'].startswith('Peca') else '#337d70'
 dr.rectangle([point(x,y+b),point(x+a,y)],fill=col)
txt((x0+440,y0-36),'FUNDO / PAREDE NOMINAL',20)
txt((x0+430,y0+650*scale+16),'FRENTE / PORTAS',20)
dr.line([(x0,y0+650*scale+67),(x0+2000*scale,y0+650*scale+67)],fill='#243d3b',width=2)
txt((x0+480,y0+650*scale+72),'2000 mm',20)
txt((60,690),'0,250272 m² do soco  +  0,020448 m² das duas laterais  =  0,270720 m²',27)
txt((60,744),'Madeira nominal a800 kg/m³: P01 265,0 kg | P03 39,4 kg | P02 27,8 kg',25)
txt((60,790),'P01 + P03 + soco + extensões723: 315,9 kg, antes de conteúdo e acessórios.',25)
txt((60,839),'Área desenhada não comprova contato, nivelamento ou resistência real do piso.',22,'#7c4535')
im.save(HERE/'Apoios_e_massas.png')
