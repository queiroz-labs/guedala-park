"""Corte esquematico dos envelopes atuais, sem propor suporte ou fixadores."""
from pathlib import Path
import json
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent
g=json.loads((HERE/'Geometria_R51.json').read_text(encoding='utf8'))
im=Image.new('RGB',(1500,930),'#f5f2ec');d=ImageDraw.Draw(im)
font=lambda n:ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',n)
d.text((40,25),'P09 · interface entre gabinete e depurador',fill='#233e39',font=font(32))
d.text((40,78),'Corte dos envelopes atuais · cotas nominais do CAD · sem alterar posições ou representar montagem aprovada',fill='#526458',font=font(21))
def xy(v,z):return 710-1.2*v,800-.75*(z-1650)
def rect(v0,v1,z0,z1,**kw):
 a=xy(v1,z1);b=xy(v0,z0);d.rectangle([a,b],**kw)
d.line([xy(0,1700),xy(0,2550)],fill='#929c8e',width=7)
rect(0,330,1958,2550,outline='#8e7757',width=4)
rect(0,330,1958,1976,fill='#bbab8e')
rect(332,350,1959,2549,outline='#8e7757',width=2)
rect(0,300,1740,1916,fill='#bac5c0',outline='#60776c',width=3)
rect(0,300,1916,1958,fill='#ead8b6')
d.text((385,180),'Gabinete P09',fill='#6c5b43',font=font(24))
d.text((375,670),'Gabarito DE61IX',fill='#355949',font=font(23))
y1=xy(0,1958)[1];y2=xy(0,1916)[1]
d.line((240,y1,240,y2),fill='#ad7927',width=3)
for y in (y1,y2):d.line((225,y,325,y),fill='#ad7927',width=2)
d.text((78,(y1+y2)/2-17),'42 mm',fill='#98651e',font=font(29))
d.text((375,y1-33),'base inferior Z1958',fill='#6b5b43',font=font(19))
d.text((375,y2+8),'topo do gabarito Z1916',fill='#355949',font=font(19))
d.line((810,155,810,775),fill='#c5cbbb',width=2)
lines=[
 'Massa conhecida; ligação ainda pendente',
 '',
 'ManualREV.0025, família60 cm:',
 'peso sem embalagem = 6,00 kg.',
 '',
 'O documento prevê fixação à parede',
 'e fixação superior ao gabinete.',
 '',
 'A transferência de esforços entre elas',
 'não foi presumida como50/50 ou100%.',
 '',
 'A faixa42 não tem adaptação modelada.',
 'Confirmar abas, apoios e ventilação',
 'antes de fechar essa interface.'
]
y=175
for i,line in enumerate(lines):
 d.text((850,y),line,font=font(24 if i==0 else 21),fill='#3b584a');y+=37
d.text((40,820),'Peca139 é uma caixa de planejamento: abas, parafusos e detalhes comerciais não estão representados.',fill='#805733',font=font(21))
d.text((40,863),'Preservar retorno de ar20 mm, filtros e acesso. R51 intacta; nenhuma solução de apoio foi incorporada.',fill='#805733',font=font(21))
im.save(HERE/'Interface_depurador_42mm.png');print('Interface_depurador_42mm.png')
