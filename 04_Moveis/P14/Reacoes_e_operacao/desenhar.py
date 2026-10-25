"""Esquema tecnico da parada55, sem desenho comercial nem prova de folga."""
from pathlib import Path
import json,math
from PIL import Image,ImageDraw,ImageFont
from calcular import parts,rot,origin,masses
HERE=Path(__file__).resolve().parent
dta=json.loads((HERE/'Resultados.json').read_text(encoding='utf8'));case=dta['worst_uplift']
im=Image.new('RGB',(1580,900),'#f5f2ec');d=ImageDraw.Draw(im)
font=lambda n:ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',n)
d.text((40,25),'P14 · reações no cesto travado a 55°',font=font(32),fill='#243b39')
d.text((40,75),'Hipótese de montagem · frente550 × 521 × 18 e saco400 × 200 × 400 preservados',font=font(21),fill='#4f5d59')
def yz(y,z):return 60+(y+540)*1.07,740-(z+60)*1.07
def polygon(name,fill):
 b=parts[name]['box_mm'];ps=[rot([4555,y,z],55) for y,z in [(b[1],b[2]),(b[4],b[2]),(b[4],b[5]),(b[1],b[5])]]
 d.polygon([yz(p[1],p[2]) for p in ps],fill=fill,outline='#58766c')
for i in range(3,17):polygon(f'PecaCestoR{i:03d}','#b8c9bd')
polygon('PecaCestoR021','#ddc8a0')
o=yz(0,0);d.ellipse((o[0]-7,o[1]-7,o[0]+7,o[1]+7),fill='#285f9d')
mobile=rot([4555,6440,450],55);mp=yz(mobile[1],mobile[2])
fixed=dta['stay_unit_vector_global_XYZ'];old=json.loads((HERE.parent/'Banco_cesto_simples_2026-10-23/Conferencia/Resultados.json').read_text(encoding='utf8'))
sc=next(r for r in old['articuladores'] if r['id']=='cesto_direito');fp=yz(sc['fixed'][0]-6440,sc['fixed'][1]-120)
d.line((mp,fp),fill='#288276',width=6)
for p in (mp,fp):d.ellipse((p[0]-5,p[1]-5,p[0]+5,p[1]+5),fill='#288276')
d.text((fp[0]-65,fp[1]-36),'terminal fixo candidato',font=font(17),fill='#288276')
def arrow(a,b,color,label,offset=(10,0)):
 d.line((a,b),fill=color,width=4);ang=math.atan2(b[1]-a[1],b[0]-a[0]);r=13
 d.polygon([b,(b[0]-r*math.cos(ang-.5),b[1]-r*math.sin(ang-.5)),(b[0]-r*math.cos(ang+.5),b[1]-r*math.sin(ang+.5))],fill=color)
 d.text((b[0]+offset[0],b[1]+offset[1]),label,fill=color,font=font(20))
ms=masses(case['rho_kg_m3'],case['clothes_kg'],case['clothes_center_relative_mm']);mt=sum(m for m,p in ms)
cg=sum((rot(p,55)*m for m,p in ms))/mt;cp=yz(cg[1],cg[2])
arrow(cp,(cp[0],cp[1]+100),'#a74332',f"P = {case['weight_N']:.1f} N",(12,-10))
arrow(mp,(mp[0]+95*fixed[1],mp[1]-95*fixed[2]),'#288276',f"T = {case['stay_total_tension_N']:.1f} N",(-35,-35))
d.text((o[0]-55,o[1]+20),'pivôs · eixo ideal',font=font(20),fill='#285f9d')
d.text((50,785),'ProjeçãoYZ ilustrativa; não verifica colisões, terminais ou trava comercial.',font=font(19),fill='#5d6158')
d.line((850,135,850,825),fill='#c9cec4',width=2)
d.text((895,145),'A carga não se divide sempre em duas metades',font=font(24),fill='#243b39')
lines=[
 'Exemplo de retenção vertical necessária:',
 'ρ650; roupa8 kg com CG deslocado200 mm à direita;',
 'só o articulador esquerdo recebe a retenção.',
 '',
 'Forças do pivô sobre o conjunto móvel:',
 f"Esquerdo: Y = {case['hinge_left_YZ_N'][0]:+.1f} N; Z = {case['hinge_left_YZ_N'][1]:+.1f} N",
 f"Direito:     Y = {case['hinge_right_YZ_N'][0]:+.1f} N; Z = {case['hinge_right_YZ_N'][1]:+.1f} N",
 '',
 'Z negativo no móvel significa solicitação para cima',
 'no suporte fixo. Apoio solto por baixo não a retém.',
 '',
 '270 cenários estáticos; forças sem impacto,',
 'mãos, saco e ferragens adicionais.',
 '',
 'Capacidade e fixações continuam pendentes.'
]
y=198
for line in lines:
 d.text((895,y),line,font=font(20),fill='#3e524b');y+=35
d.text((40,850),'R51 intacta · forças não estão em escala · posições de pivôs e articuladores são hipóteses nominais',font=font(21),fill='#805733')
im.save(HERE/'Reacoes_parada_55.png');print('Reacoes_parada_55.png')
