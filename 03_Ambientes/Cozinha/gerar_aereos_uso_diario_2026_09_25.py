from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
p=Path(__file__).parent
im=Image.new('RGB',(1400,1110),'#f7f4ee');d=ImageDraw.Draw(im)
ink='#293d42';blue='#3d6872';cream='#eee2cd'
def f(n):return ImageFont.truetype('C:/Windows/Fonts/arial.ttf',n)
def t(x,y,s,n=22,c=ink):d.text((x,y),s,font=f(n),fill=c)
t(55,35,'AÉREO SOBRE A PIA | Uso diário',35)
t(55,90,'Proposta para avaliação · vista de cima · gabaritos hipotéticos, sem produtos escolhidos',22)
t(55,135,'Cada nível: 48,6 × 31,4 cm de teste, antes das interferências das dobradiças.',22)
s=11
def shelf(x,y,title):
 t(x,y,title,26);y+=60
 d.rectangle((x,y,x+48.6*s,y+31.4*s),fill=cream,outline=blue,width=3)
 t(x+170,y+31.4*s+16,'FRENTE / ACESSO',18)
 return x,y
x,y=shelf(65,220,'C1 · Pratos | apoio a 155 cm')
for cx,r in [(12.8,12),(37.3,10.5)]:d.ellipse((x+(cx-r)*s,y+(15.7-r)*s,x+(cx+r)*s,y+(15.7+r)*s),fill='#faf7f1',outline=blue,width=3)
d.ellipse((x+(37.3-9.5)*s,y+(15.7-9.5)*s,x+(37.3+9.5)*s,y+(15.7+9.5)*s),outline=blue,width=2)
t(x+58,y+140,'4 rasos',23);t(x+56,y+178,'Ø 24 cm',20)
t(x+310,y+117,'4 sobremesa',20);t(x+342,y+148,'sobre',20);t(x+330,y+178,'4 fundos',20)
x,y=shelf(790,220,'C2 · Copos e canecas | apoio a 174,8 cm')
for depth in [3,12,23]:
 for left in [4,13]:
  a=x+left*s;b=y+depth*s
  d.ellipse((a+4,b+4,a+7*s-4,b+7*s-4),fill='#faf7f1',outline=blue,width=2)
for depth in [10,21]:
 for left in [24,36]:
  a=x+left*s;b=y+depth*s
  d.rectangle((a+2,b,a+11*s-2,b+9*s),fill='#faf7f1',outline=blue,width=2)
  t(a+15,b+35,'Caneca',18)
t(65,735,'Pratos: a pilha mista precisa ser testada.',24)
t(65,778,'Para pegar os fundos, é preciso levantar',22)
t(65,810,'os pratos de sobremesa.',22)
t(65,860,'Vão vertical de 18 cm; altura das pilhas',21)
t(65,893,'e espaço para a mão ainda não comprovados.',21)
t(790,735,'Frente: 2 copos + 2 canecas.',24)
t(790,778,'Conferir alças, altura dos objetos e alcance',22)
t(790,810,'à fila traseira antes de fechar.',22)
t(790,860,'Vão vertical de 19,2 cm.',21)
t(790,893,'Não representa acesso confortável já validado.',21)
t(55,990,'Os níveis altos e os demais módulos ainda não têm capacidade demonstrada para todo o inventário.',22)
t(55,1040,'Nenhuma mudança de prateleira aprovada · estudo de organização, não desenho de fabricação',21)
im.save(p/'Aereos_uso_diario_2026-09-25.png')
