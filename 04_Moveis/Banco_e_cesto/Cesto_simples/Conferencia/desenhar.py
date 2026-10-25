from pathlib import Path
import json, math
from PIL import Image,ImageDraw,ImageFont
P=Path(__file__).resolve().parent
data=json.loads((P/'Resultados.json').read_text(encoding='utf8'))
im=Image.new('RGB',(1600,1000),'#f4f4ef');d=ImageDraw.Draw(im)
font=lambda s,b=False:ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf' if b else 'C:/Windows/Fonts/segoeui.ttf',s)
def txt(pos,s,size=23,fill='#23352f',bold=False):d.text(pos,s,font=font(size,bold),fill=fill)
txt((40,25),'Banco e cesto | conferência nominal',38,bold=True)
txt((40,80),'Barras idealizadas em 3 posições. Terminais, trava e fixações completas ainda pendentes.',23)
for x in (30,815):d.rounded_rectangle((x,130,x+755,895),20,fill='white',outline='#d9ded8',width=2)
txt((55,150),'BANCO · até 90°',29,bold=True);txt((840,150),'CESTO · até 55°',29,bold=True)
def rot(p,axis,t):
 c,s=math.cos(t),math.sin(t);x,z=p[0]-axis[0],p[1]-axis[1]
 return(axis[0]+x*c-z*s,axis[1]+x*s+z*c)
def rect(a,b,c,e):return[(a,b),(c,b),(c,e),(a,e)]
def scene(key,convert):
 samples=data['poses_ilustrativas'][key]
 for sample,col in zip(samples,['#bcc6bf','#6fa19b','#14675c']):
  for poly in sample['polygons']:d.polygon([convert(p) for p in poly],fill=col)
  for k in ('fixed','mobile','joint'):
   x,y=convert(sample[k]);d.ellipse((x-4,y-4,x+4,y+4),fill='#23352f')
 return samples
bc=lambda p:(130+p[0]*.81,800-(p[1]-250)*.81)
d.polygon([bc(p) for p in rect(0,400,100,900)],fill='#eee7dc')
txt((70,205),'Encosto',19)
d.line([bc((140,310)),bc((512,310))],fill='#b9c3bb',width=12)
txt((205,758),'Prateleira preservada (tampa 2)',18)
samples=scene('banco_tampa2',bc)
for s,col in zip(samples,['#dbc6ad','#cb9b68','#aa6e2b']):
 poly=[rot(p,(100,423.1),math.radians(s['angulo'])) for p in rect(102,400,550,420)]
 d.polygon([bc(p) for p in poly],fill=col)
 a=bc(s['mobile']);b=bc(rot((s['fixed'][0],400),(100,423.1),math.radians(s['angulo'])))
 for i in range(0,10,2):
  d.line([(a[0]+(b[0]-a[0])*i/10,a[1]+(b[1]-a[1])*i/10),(a[0]+(b[0]-a[0])*(i+1)/10,a[1]+(b[1]-a[1])*(i+1)/10)],fill='#797f7b',width=2)
txt((65,815),'A montagem alta encostou na tampa a 15°.',20)
txt((65,847),'A posição baixa passou na triagem das barras.',20,bold=True)
cc=lambda p:(850+(p[0]-5970)*.64,795-(p[1]-50)*.64)
d.polygon([cc(p) for p in rect(6400,700,6790,920)],fill='#eee7dc')
txt((1190,215),'Tanque',19)
d.line([cc((6420,98)),cc((6982,98))],fill='#b9c3bb',width=10)
samples=scene('cesto_direito',cc)
for s,col in zip(samples,['#cbd3ce','#84a49d','#277a6d']):
 t=math.radians(s['angulo'])
 poly=[rot(p,(6440,120),t) for p in rect(6465,145,6665,545)]
 d.line([cc(p) for p in poly+[poly[0]]],fill=col,width=3)
 poly=[rot(p,(6440,120),t) for p in rect(6370,150,6388,671)]
 d.polygon([cc(p) for p in poly],fill='#b5834b')
txt((840,815),'Mecanismos nas laterais do saco, em outro plano.',20)
txt((840,847),'Saco e frente mantidos nas dimensões nominais.',20,bold=True)
txt((40,920),'PASSOU NA TRIAGEM ≠ FERRAGEM COMPLETA APROVADA',25,bold=True)
txt((40,960),'Estudo em caixas de referência, passo de 0,1°. Sem autorização de corte ou compra.',21)
im.save(P/'Conferencia_visual.png')
print('Figura salva')
