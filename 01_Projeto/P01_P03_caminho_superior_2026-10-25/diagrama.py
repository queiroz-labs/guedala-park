from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent
im=Image.new('RGB',(1280,790),'#f6f4ef');d=ImageDraw.Draw(im)
font=lambda size:ImageFont.truetype('C:/Windows/Fonts/arial.ttf',size)
def txt(x,y,s,size=23,col='#253c39'):d.text((x,y),s,font=font(size),fill=col)
txt(45,30,'P01 / P03 | SEÇÃO DO APOIO TRASEIRO',34)
txt(45,82,'Corte nominal emX6000. Y cresce para o fundo; Z cresce para cima.',23)
for dx,title,proposed in [(80,'ATUAL',False),(700,'ESTUDO SEPARADO',True)]:
 txt(dx,145,title,28)
 sc=3.0;bx=dx;by=570
 def pt(y,z):return bx+(y-3850)*sc,by-(z-2080)*sc
 def rect(y0,z0,y1,z1,fill):d.rectangle([pt(y0,z1),pt(y1,z0)],fill=fill,outline='#253c39',width=2)
 rect(3850,2132,3940 if proposed else 3922,2150,'#d7c8ab')
 rect(3922,2080,3940,2132 if proposed else 2114,'#8bada2')
 rect(3922,2150,3940,2200,'#d7c8ab')
 if proposed:
  rect(3922,2114,3940,2132,'#348273');rect(3922,2132,3940,2150,'#348273')
  x,z=pt(3931,2132);d.line([(x-30,z),(x+30,z)],fill='#d27532',width=5)
 txt(dx,605,'FundoP01 +18 de altura' if proposed else 'FundoP01 termina emZ2114',22)
 txt(dx,638,'BaseP03 +18 para trás' if proposed else 'BaseP03 termina emY3922',22)
 if not proposed:txt(dx,675,'Sem face horizontal comum aqui.',21,'#7b4939')
 else:txt(dx,675,'Contato emZ2132; topoZ2150 mantido.',21)
txt(45,735,'As faixas verdes criam contato; a capacidade da caixa e das juntas continua pendente.',23,'#7b4939')
im.save(HERE/'Secao_apoio.png')
