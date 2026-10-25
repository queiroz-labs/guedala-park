"""Prancha vetorial de estudo; posições não são dimensões executivas."""
from pathlib import Path
import json,html
here=Path(__file__).resolve().parent
r=json.loads((here/'Conferencia_Fischer.json').read_text(encoding='utf-8'))
assert r['dimensions']['front_top_mm']==570
s=.75;base=920;ink='#203c38';wood='#c0a47f';teal='#4d9ba9';orange='#bd6c36'
p=['<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1120"><style>text{font-family:Arial,sans-serif;fill:#203c38}</style><rect width="1600" height="1120" fill="#f4f1e9"/><defs><marker id="arr" markerWidth="6" markerHeight="6" refX="3" refY="3" orient="auto-start-reverse"><path d="M0,0L6,3L0,6" fill="#203c38"/></marker></defs>']
def text(x,y,t,size=20,color=ink,anchor='start',weight='normal'):
    for i,l in enumerate(t.split('\n')):p.append(f'<text x="{x}" y="{y+i*(size+7)}" font-size="{size}" style="fill:{color}" text-anchor="{anchor}" font-weight="{weight}">{html.escape(l)}</text>')
def line(x1,y1,x2,y2,color=ink,width=1.5,dash=''):
    p.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}" stroke-dasharray="{dash}"/>')
def rect(o,x,z,w,h,fill,alpha=1,stroke=ink,dash=''):
    p.append(f'<rect x="{o+x*s}" y="{base-(z+h)*s}" width="{w*s}" height="{h*s}" fill="{fill}" fill-opacity="{alpha}" stroke="{stroke}" stroke-dasharray="{dash}"/>')
def dim(x1,y1,x2,y2):p.append(f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{ink}" fill="none" marker-start="url(#arr)" marker-end="url(#arr)"/>')
text(50,48,'GUEDALA PARK  /  COZINHA  /  19.10.2026',18,color='#57756b')
text(50,94,'Fischer escolhido: proposta de encaixe no móvel',36,weight='bold')
text(50,128,'Estudo em milímetros · frente, corpo e apoio são gabaritos; posições finais dependem da montagem real.',20)
p.append('<rect x="45" y="155" width="690" height="795" rx="16" fill="#fffdf7"/><rect x="765" y="155" width="790" height="795" rx="16" fill="#fffdf7"/>')
text(75,194,'FRENTE DO MÓDULO',23,weight='bold');text(795,194,'CORTE LATERAL',23,weight='bold')
o=110
line(90,base,645,base,'#7b8179',3)
rect(o,0,0,18,900,wood);rect(o,595,0,18,900,wood)
rect(o,0,900,613,20,'#b9beb7');rect(o,0,920,600,15,'#253535')
text(o+225,213,'Electrolux KE4GC',18,anchor='middle')
rect(o,18,120,577,18,wood);rect(o,9,123,595,447,'#253535')
rect(o,67,180,478,280,'#52635d',stroke='#98aaa2')
for x in [125,305,485]:p.append(f'<circle cx="{o+x*s}" cy="{base-510*s}" r="8" fill="#bfc8bf"/>')
text(o+306.5*s,base-345*s,'Fischer Infinity\ncom grill, sem turbo',21,color='white',anchor='middle')
rect(o,26.5,710,560,45,teal,.65,teal)
for x in range(45,580,24):line(o+x*s,base-715*s,o+x*s,base-750*s,'#2d6670',1)
text(o+306.5*s,base-795*s,'Saída de ar proposta',20,anchor='middle')
text(o+306.5*s,base-650*s,'Faixa técnica livre\nsem gaveta adotada',18,color='#69776c',anchor='middle')
dim(o,280,o+613*s,280);text(o+306.5*s,271,'613 mm externos',18,anchor='middle')
dim(622,base-570*s,622,base-123*s);text(635,660,'447',18)
text(78,865,'Apoio candidato: topo 138 mm',18);text(78,896,'Frente: margem nominal de 9 mm por lado',18)
line(575,base-570*s,605,base-570*s);text(605,480,'Topo 570',17,anchor='end')
o=855
line(820,base,1420,base,'#7b8179',3);line(o+630*s,base,o+630*s,base-950*s,'#878d85',6)
rect(o,585,120,45,780,teal,.20,teal);rect(o,8,710,622,45,teal,.32,teal)
rect(o,0,900,630,20,'#b9beb7');rect(o,90,920,450,15,'#253535')
rect(o,90,789,450,131,'#dcaa63',.25,orange,'6 5');text(o+100*s,base-845*s,'131 mm abaixo: hipótese',17,color='#855326')
rect(o,34,138,547,432,'#aebbb3');rect(o,8,123,26,447,'#253535');rect(o,40,120,535,18,wood)
rect(o,373,660,212,30,orange);rect(o,400,660,212,30,'none',1,orange,'5 4')
text(o+80*s,base-410*s,'Envelope de encaixe\nL560 × P547 × A432\nPlanos de apoio a conferir',19)
text(805,213,'Bancada preservada: 920 mm',18,weight='bold')
text(805,345,'Travessa candidata: 27 mm para a frente',18,color=orange);line(1200,350,o+480*s,base-690*s,orange,1)
dim(1370,base-570*s,1370,base-789*s);text(1390,410,'219 mm*',20,color=orange)
text(805,base-620*s,'Saída frontal\na detalhar',18,color='#357986');line(880,base-645*s,o+10*s,base-730*s,teal,1)
text(850,865,'Reserva traseira contínua: 45 mm',18,color='#357986');line(1190,855,o+608*s,base-490*s,teal,1)
text(850,896,'Frente do forno 8 mm atrás da borda da pedra',17)
text(50,990,'* Com d = 131 mm, restam 219 mm entre envelopes; com 10 mm de tolerância de estudo, restam 209 mm.',20)
text(50,1026,'Os 131 mm são a altura total publicada aplicada inteira para baixo. Não representam a projeção instalada nem as conexões.',18)
text(50,1062,'Confirmar montagem do forno, corpo/grampos/gás do cooktop, elétrica, grelhas, isolamento e medidas reais antes do corte.',18)
text(50,1096,'Estudo separado da R30 · Sem liberação de fabricação · Janela e comandos do forno apenas ilustrativos',18,color='#65766c')
p.append('</svg>')
(here/'Fischer_no_movel.svg').write_text('\n'.join(p),encoding='utf-8')
print(str(here/'Fischer_no_movel.svg'))
