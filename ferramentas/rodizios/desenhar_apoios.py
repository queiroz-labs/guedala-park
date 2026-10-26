"""Planta esquematica dos contatos e de uma perda de apoio, sem desenho de furacao."""
from pathlib import Path
import json
from PIL import Image,ImageDraw,ImageFont
from conferir_apoios import hull
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'04_Moveis/P08'
d=json.loads((OUT/'Apoios.json').read_text(encoding='utf-8'))
c=next(x for x in d['cases'] if not x['feasible_nonnegative_equilibrium'])
im=Image.new('RGB',(1200,730),'#f6f5ef');draw=ImageDraw.Draw(im)
font=lambda n:ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',n)
draw.text((40,24),'P08 | Seis rodas: contato e estabilidade',font=font(30),fill='#172b35')
draw.text((40,70),'Geometria salva R52. Corpo rígido; sem previsão de flexão ou carga permitida.',font=font(20),fill='#465a64')
def pt(xy):return (70+(xy[0]-1674)*.86,150+(xy[1]-6470)*.86)
draw.rectangle([pt((1674,6470)),pt((2897,6930))],outline='#697983',width=3)
poly=hull([w['contact_XY_mm'] for w in d['wheels'] if w['id']!=c['removed_contact']])
draw.polygon([pt(p) for p in poly],fill='#cce2d9',outline='#27735a',width=3)
for w in d['wheels']:
    x,y=pt(w['contact_XY_mm']);missing=w['id']==c['removed_contact']
    draw.ellipse((x-10,y-10,x+10,y+10),fill='#b93c3c' if missing else '#234b60')
    draw.text((x-15,y+15),w['id'],font=font(20),fill='#172b35')
    if missing:draw.line((x-16,y-16,x+16,y+16),fill='#b93c3c',width=3)
x,y=pt(c['center_XY_mm']);draw.ellipse((x-7,y-7,x+7,y+7),fill='#c45a11')
draw.text((x+14,y-23),'CG total',font=font(20),fill='#9e4709')
draw.text((70,555),'Exemplo: 5 kg no canto frontal esquerdo + madeira a 650 kg/m³; R3 sem contato.',font=font(22),fill='#172b35')
draw.text((70,595),'Centro de gravidade fora do polígono verde: não há equilíbrio vertical nessa hipótese.',font=font(21),fill='#172b35')
draw.text((70,637),'336 cenários | 26 sem equilíbrio após excluir uma roda | 0 ensaios físicos',font=font(22),fill='#172b35')
draw.text((70,679),'Rodas e calços reais, piso, guias, batente, fixação e massas adicionais ainda pendentes.',font=font(18),fill='#465a64')
im.save(OUT/'Apoios.png')
