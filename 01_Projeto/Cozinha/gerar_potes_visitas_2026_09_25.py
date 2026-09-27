from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
p=Path(__file__).parent
im=Image.new('RGB',(1500,1360),'#f7f4ee');d=ImageDraw.Draw(im)
ink='#293d42';blue='#3d6872';fill='#eee2cd';obj='#faf7f1';s=7.8
def f(n):return ImageFont.truetype('C:/Windows/Fonts/arial.ttf',n)
def t(x,y,label,n=22):d.text((x,y),label,font=f(n),fill=ink)
t(55,30,'AÉREOS | Potes, reservas e visitas',36)
t(55,86,'Posições propostas · vista de cima · gabaritos hipotéticos, não produtos selecionados',22)
def level(x,y,w,title,sub):
 t(x,y,title,26);t(x,y+38,sub,20);y+=83
 d.rectangle((x,y,x+w*s,y+31.4*s),fill=fill,outline=blue,width=3)
 t(x+95,y+31.4*s+12,'FRENTE / ACESSO',17)
 return x,y
def rect(x,y,a,b,w,h,label):
 d.rectangle((x+a*s,y+b*s,x+(a+w)*s,y+(b+h)*s),fill=obj,outline=blue,width=2)
 for i,line in enumerate(label):t(x+a*s+10,y+b*s+12+i*24,line,19)
x,y=level(65,170,66.1,'B1 · Pratos + mantimentos','Apoio a 195,8 cm · duas zonas, sem nova divisória')
for dia in [26,23,20]:
 d.ellipse((x+(16.525-dia/2)*s,y+(15.7-dia/2)*s,x+(16.525+dia/2)*s,y+(15.7+dia/2)*s),fill=obj,outline=blue,width=2)
t(x+60,y+103,'18 pratos',21);t(x+56,y+137,'1 só pilha',21)
d.line((x+33.05*s,y,x+33.05*s,y+31.4*s),fill=blue,width=1)
t(x+36*s,y+110,'Mantimentos',21);t(x+37*s,y+146,'Meia largura',19)
x,y=level(820,170,66.1,'B2 · Mantimentos','Apoio a 223,4 cm · nível inteiro destinado à despensa')
rect(x,y,2,2,62,27,['Mantimentos — largura inteira','Cestos e embalagens a dimensionar'])
t(65,560,'Pilha única: altura e estabilidade pendentes.',21)
t(65,596,'Metade nominal para mantimentos: 33,05 cm.',21)
t(820,560,'Organizar por frequência, peso e alcance.',21)
t(820,596,'Capacidade para o estoque ainda a conferir.',21)
x,y=level(65,695,48.6,'C3 · 10 potes de feijão vazios','Apoio a 195,8 cm · duas pilhas encaixadas')
rect(x,y,1,1,34,10,['Tampas separadas'])
rect(x,y,1,13,16,16,['5 potes','16 × 16']);rect(x,y,19,13,16,16,['5 potes','16 × 16'])
x,y=level(820,695,48.6,'C4 · Xícaras, pires e taças','Apoio a 223,4 cm · conferir acesso a itens frágeis')
for row in range(2):
 for col in range(3):
  a=1+col*7;b=1+row*7
  d.ellipse((x+a*s+2,y+b*s+2,x+(a+7)*s-2,y+(b+7)*s-2),fill=obj,outline=blue,width=2)
rect(x,y,26,1,20,24,['6 xícaras','com alças'])
d.ellipse((x+4*s,y+16*s,x+18*s,y+30*s),fill=obj,outline=blue,width=2)
t(x+5*s,y+21*s,'6 pires',18)
t(65,1090,'Dimensões e altura das pilhas a verificar.',21)
t(65,1126,'Não inclui potes de vidro de refeições.',21)
t(820,1090,'6 taças em pé + 6 xícaras + 6 pires.',21)
t(820,1126,'Planta não comprova manuseio em altura.',21)
t(55,1210,'Atenção: esta distribuição ainda não acomoda todo o inventário da cozinha.',25)
t(55,1255,'Alimentos de uso diário, bebidas e pequenos aparelhos continuam em compatibilização.',22)
t(55,1300,'Divisões dos móveis preservadas · conteúdo proposto para avaliação · sem liberação para fabricação',20)
im.save(p/'Potes_mantimentos_visitas_2026-09-25.png')
