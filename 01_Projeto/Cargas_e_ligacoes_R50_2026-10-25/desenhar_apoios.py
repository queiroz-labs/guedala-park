"""Diagramas de engenharia em escala local, sem editar imagem ou modelo."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent
im=Image.new('RGB',(1600,1180),'white');d=ImageDraw.Draw(im)
font=lambda n,b=False:ImageFont.truetype('C:/Windows/Fonts/'+('segoeuib.ttf' if b else 'segoeui.ttf'),n)
ink='#23343b';grey='#aaa9a2';teal='#247f70';red='#af422d'
def text(x,y,s,size=25,fill=ink,b=False):d.text((x,y),s,font=font(size,b),fill=fill)
def line(a,b,fill=ink,w=3):d.line([a,b],fill=fill,width=w)
text(60,35,'APOIOS E CAMINHOS DE CARGA',38,b=True)
text(60,90,'Estudos nominais de 25/10/2026 · dimensões em mm · R50 principal preservada',24)
line((60,138),(1540,138),fill='#d3dada',w=2)
text(60,165,'P15 · seção pela profundidade da lavanderia',29,b=True)
text(60,210,'Base 312 × 18; fundo começa 18 acima da face inferior da base.',24)
# Perfil y-z. Apenas aresta comum na R50.
x0=160;y0=425;s=1.8
def rect_mm(y1,z1,y2,z2,color):d.rectangle([x0+y1*s,y0-z2*s,x0+y2*s,y0-z1*s],fill=color,outline=ink,width=2)
rect_mm(0,0,312,18,'#b4d3ca');rect_mm(312,18,330,100,grey)
d.ellipse([x0+312*s-6,y0-18*s-6,x0+312*s+6,y0-18*s+6],fill=red)
line((x0+312*s,y0-18*s),(1020,325),fill=red)
text(1030,290,'R50: só uma aresta',25,red,b=True)
text(1030,325,'Não conta como apoio traseiro',23,red)
rect_mm(0,-20,30,0,teal);rect_mm(282,-20,312,0,teal)
text(160,480,'Estudo externo: 2 tubos 30 × 20 × 2, com 20 na vertical.',24,teal,b=True)
text(160,518,'Conserva o espaço interno; desce 20 abaixo da base. Terminais por detalhar.',23)
text(160,552,'Carga → base → tubos → quatro terminais → laterais → caixa → suspensão.',23)
line((60,605),(1540,605),fill='#d3dada',w=2)
text(60,630,'P01 · prateleira direita vista de frente',29,b=True)
text(60,676,'A esquerda recebe a solução espelhada. Altura e profundidade ficam iguais.',24)
scale=1.25;origin=260
def shelf(y,extended):
 def box(a,b,top,bottom,fill):d.rectangle([origin+a*scale,y+top,origin+b*scale,y+bottom],fill=fill,outline=ink,width=2)
 box(-18,0,23,120,grey);box(332,350,23,120,grey);box(705,723,-30,120,grey)
 box(-18 if extended else 0,705,0,23,'#8ab7a9' if extended else '#c8d1d5')
 if extended:box(-18,0,20,24,teal)
 else:
  line((origin-7,y+16),(origin+7,y+30),fill=red,w=4);line((origin-7,y+30),(origin+7,y+16),fill=red,w=4)
 text(1210,y,'723 × 550 × 18' if extended else '705 × 550 × 18',23,b=True)
 text(1210,y+38,'apoio de 18 × 550' if extended else 'ponta sem apoio',22,teal if extended else red)
shelf(755,False);text(60,780,'ANTES',23,red,b=True)
shelf(960,True);text(60,982,'ESTUDO',23,teal,b=True)
text(260,892,'Divisória existente   |   apoio interno existente   |   lateral da caixa',22)
text(60,1120,'Geometria de apoio conferida. Juntas, deformação da caixa e montagem ainda condicionam a carga.',23)
im.save(HERE/'Mapa_apoios_e_cargas.png')
