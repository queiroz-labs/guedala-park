from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
p=Path(__file__).parent
im=Image.new('RGB',(1400,1040),'#f7f4ee');d=ImageDraw.Draw(im)
ink='#283d41'
def t(x,y,text,size=24):
 d.text((x,y),text,font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',size),fill=ink)
t(55,35,'COZINHA | Duas gavetas + gavetão',38)
t(55,95,'Distribuição aprovada · 25/09/2026 · alturas brutas de projeto',25)
x,y,w,s=80,190,450,8
for height,label in [(16,'G1 · Talheres e facas'),(16,'G2 · Utensílios'),(40,'G3 · Mantimentos')]:
 d.rectangle((x,y,x+w,y+height*s),fill='#d7bd96',outline=ink,width=3)
 t(x+22,y+24,label,27)
 t(x+w+20,y+height*s/2-15,f'{height} cm',25)
 if height==40:
  t(x+22,y+83,'Bebidas e alimentos abertos',23)
  t(x+22,y+124,'Temperos em pé, na frente',23)
  t(x+22,y+166,'Organizador removível',23)
 y+=height*s
t(80,800,'Total: 72 cm brutos',27)
t(755,195,'TEMPEROS',28)
t(755,245,'No gavetão, com identificação',24)
t(755,280,'nas tampas e acesso pela frente.',24)
t(755,365,'PANOS LIMPOS',28)
t(755,415,'Caixa exclusiva no C3, junto',24)
t(755,450,'dos potes vazios, para reposição.',24)
t(755,485,'Encaixe conjunto a conferir.',24)
t(755,570,'GAVETA BAIXA DE LIMPEZA',26)
t(755,620,'Continua separada, sob a base.',24)
t(755,655,'Frente recuada e rodas preservadas.',24)
t(55,895,'Alturas internas e carga dependem das caixas e ferragens escolhidas.',24)
t(55,940,'Esquema de funções; não comprova cabimento do estoque nem libera fabricação.',23)
im.save(p/'Interior_gavetas_2026-09-25.png')
print('Desenho atualizado: 16 / 16 / 40 cm.')