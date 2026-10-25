"""Diagrama de resultantes; nao e detalhamento de suspensor ou furo."""
from pathlib import Path
import json,math
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent
r=json.loads((HERE/'Resultados.json').read_text(encoding='utf8'))
case=next(e for e in r['examples'] if e['case']['code']=='P04' and e['case']['payload_case']=='front' and e['case']['door_angles_deg']==[86]*4)
V=case['case']['weight_N'];M=case['case']['wall_normal_gravity_moment_Nm'];T=case['groups_equal']['total_tension_N']
im=Image.new('RGB',(1480,880),'#f5f2ec');d=ImageDraw.Draw(im)
font=lambda n:ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',n)
d.text((42,25),'Suspensão · o fundo reforçado também precisa chegar à parede',font=font(31),fill='#233e39')
d.text((42,78),'Esquema de forças sobre a caixa inteira · não são furos, ferragens reais ou capacidades',font=font(22),fill='#4f635a')
d.rectangle((85,165,135,720),fill='#bdc2b8')
for y in range(180,705,25):d.line((85,y,135,y-25),fill='#889283',width=2)
d.rectangle((135,190,540,682),outline='#876f51',width=5)
d.text((225,202),'caixa nominal',font=font(21),fill='#7c694e')
def arrow(a,b,color):
 d.line((a,b),fill=color,width=5);ang=math.atan2(b[1]-a[1],b[0]-a[0]);s=15
 d.polygon([b,(b[0]-s*math.cos(ang-.5),b[1]-s*math.sin(ang-.5)),(b[0]-s*math.cos(ang+.5),b[1]-s*math.sin(ang+.5))],fill=color)
arrow((150,260),(65,260),'#a74332');d.text((180,275),f'T = {T:.1f} N',fill='#a74332',font=font(25))
arrow((135,580),(245,580),'#288276');d.text((275,562),f'C = {T:.1f} N',fill='#288276',font=font(25))
cgx=135+M/V*1000*1.6
arrow((cgx,365),(cgx,505),'#285f9d');d.text((cgx+18,435),f'V = {V:.1f} N',fill='#285f9d',font=font(25))
d.line((58,260,58,580),fill='#7d795e',width=2)
d.text((20,390),'h',fill='#7d795e',font=font(27))
d.text((170,630),'h = 200 mm é parâmetro entre resultantes',fill='#7d795e',font=font(18))
d.line((650,170,650,730),fill='#c6cbbe',width=2)
lines=[
 'Exemplo P04 de estudo,ρ900:',
 '10 kg de conteúdo frontal; quatro portas a86°.',
 '',
 f'Peso conhecido: {V:.1f} N.',
 f'Momento para fora da parede: {M:.2f} Nm.',
 f'Tração superior: 1000 × M(Nm) / h(mm) = {T:.1f} N.',
 '',
 'A compressão inferior fecha o binário.',
 'A tração pode repartir-se de modo desigual.',
 'Nenhum valor é capacidade por parafuso.',
 '',
 'Caixa, suspensor, trilho e parede precisam',
 'transmitir o mesmo caminho de cargas.'
]
y=180
for line in lines:d.text((700,y),line,font=font(22),fill='#3e554b');y+=39
d.text((42,775),'Forças sem majoração, mãos, impacto ou ferragens adicionais. Parede e conjunto reais ainda não validados.',font=font(21),fill='#805733')
d.text((42,820),'R51 preservada · caixa mostrada apenas para explicar o equilíbrio · sem escala de forças',font=font(21),fill='#805733')
im.save(HERE/'Binario_suspensao.png');print('Binario_suspensao.png')
