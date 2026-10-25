from pathlib import Path
import html,json
here=Path(__file__).resolve().parent
r=json.loads((here/'Conferencia.json').read_text(encoding='utf-8'))
assert r['air_solid_count']==1 and not r['overlaps']
p=['<svg xmlns="http://www.w3.org/2000/svg" width="1540" height="1250"><style>text{font-family:Arial,sans-serif;fill:#233e38}</style><rect width="1540" height="1250" fill="#f4f1e9"/><defs><marker id="arrow" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0,0L6,3L0,6" fill="#218da1"/></marker></defs>']
ink='#233e38';wood='#c0a078';air='#69b7c3'
def text(x,y,t,size=19,color=ink,weight='normal',anchor='start'):
 for i,line in enumerate(t.split('\n')):p.append(f'<text x="{x}" y="{y+i*(size+7)}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" style="fill:{color}">{html.escape(line)}</text>')
def rawrect(x,y,w,h,fill,stroke=ink,dash=''):
 p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-dasharray="{dash}"/>')
def line(x1,y1,x2,y2,color=ink,width=1.5):p.append(f'<path d="M{x1} {y1}L{x2} {y2}" fill="none" stroke="{color}" stroke-width="{width}"/>')
def box(ox,base,scale,x,z,w,h,fill,stroke=ink,dash=''):
 rawrect(ox+x*scale,base-(z+h)*scale,w*scale,h*scale,fill,stroke,dash)
def flow(d):p.append(f'<path d="{d}" fill="none" stroke="#218da1" stroke-width="5" marker-end="url(#arrow)"/>')
text(50,43,'GUEDALA PARK  /  COZINHA  /  APOIOS E VENTILAÇÃO R01  /  19.10.2026',17,color='#537568')
text(50,88,'KE4GC + Fischer com grill: apoio e caminho do ar',33,weight='bold')
text(50,122,'Solução de projeto em milímetros · Medidas finais, materiais, fixações e instalação ainda precisam de conferência.',19)
rawrect(45,148,625,650,'#fffdf7',stroke='#e6e1d5');rawrect(695,148,800,650,'#fffdf7',stroke='#e6e1d5')
text(70,185,'FRENTE',22,weight='bold');text(720,185,'CORTE PELO CANAL DE AR',22,weight='bold')
s=.53;ox=115;base=750
box(ox,base,s,0,0,18,900,wood);box(ox,base,s,595,0,18,900,wood)
box(ox,base,s,0,900,613,20,'#b6bcb4');box(ox,base,s,0,920,600,15,'#263b35')
box(ox,base,s,18,120,577,18,wood)
for x in [18,297.5,577]:box(ox,base,s,x,0,18,120,wood)
box(ox,base,s,9,123,595,447,'#263b35')
box(ox,base,s,65,200,480,265,'#536b60',stroke='#8ba79a')
text(ox+306.5*s,base-360*s,'Fischer Infinity',20,color='white',anchor='middle')
text(ox+306.5*s,base-308*s,'grill · sem turbo',18,color='white',anchor='middle')
for x in [125,305,485]:p.append(f'<circle cx="{ox+x*s}" cy="{base-515*s}" r="5" fill="#c4d0c7"/>')
for z in [30,705]:
 box(ox,base,s,26.5,z,560,60,air,stroke='#328094')
 for x in [138,250,362,474]:box(ox,base,s,x,z,4,60,'#3b5a52',stroke='none')
text(78,232,'Módulo 613 · bancada 920',19)
text(78,305,'Cooktop no eixo atual',18);line(260,310,ox+310*s,base-920*s)
text(455,351,'Saída superior\n560 ×60',18,color='#287c8c');line(445,367,ox+580*s,base-735*s,'#287c8c')
text(455,516,'Topo 570*',18);line(450,506,ox+590*s,base-570*s)
text(455,685,'Entrada inferior\n560 ×60',18,color='#287c8c');line(447,710,ox+580*s,base-60*s,'#287c8c')
text(80,781,'Frentes de ventilação removíveis · sem gaveta na faixa técnica',16,color='#617367')

ox=805;base=750;s=.53
box(ox,base,s,585,30,45,870,'#c1e0e6',stroke='#6cacb8')
box(ox,base,s,8,705,622,60,'#c1e0e6',stroke='#6cacb8')
box(ox,base,s,38,30,592,60,'#c1e0e6',stroke='#6cacb8')
box(ox,base,s,0,900,630,20,'#b6bcb4');box(ox,base,s,90,920,450,15,'#263b35')
box(ox,base,s,90,789,450,131,'#efd8ae',stroke='#b17a3b',dash='5 4')
box(ox,base,s,34,138,547,432,'#a4b5a9')
box(ox,base,s,8,123,26,447,'#263b35')
box(ox,base,s,40,120,535,18,wood)
box(ox,base,s,373,660,212,30,'#c38b56')
line(ox+630*s,750,ox+630*s,245,'#848f83',4)
flow(f'M{ox+50*s} {base-60*s} L{ox+604*s} {base-60*s} L{ox+604*s} {base-470*s}')
flow(f'M{ox+604*s} {base-470*s} L{ox+604*s} {base-735*s} L{ox+15*s} {base-735*s}')
text(735,233,'Canal traseiro 45 ×560',19,color='#287c8c');line(1020,240,ox+605*s,470,'#287c8c')
text(1150,324,'131 para baixo:\nteste de envelope,\nsem conexões',17,color='#92612f')
text(1150,444,'Travessa avança 27\npara liberar o fundo',18);line(1140,450,ox+490*s,base-675*s)
text(1150,596,'Base plana 18\nApoio candidato 138*',18);line(1140,610,ox+350*s,base-138*s)
text(735,781,'Ar entra por baixo, sobe atrás e sai acima · grelha fora da saída do próprio forno',16,color='#617367')

rawrect(45,821,625,262,'#fffdf7',stroke='#e6e1d5');rawrect(695,821,800,262,'#fffdf7',stroke='#e6e1d5')
text(70,855,'DETALHE DO APOIO ATÉ O PISO',21,weight='bold')
ox=105;base=1037;s=.76
box(ox,base,s,0,120,577,18,wood)
for x in [0,279.5,559]:box(ox,base,s,x,0,18,120,wood)
for center in [148.75,428.25]:
 text(ox+center*s,base-55*s,'261,5',18,anchor='middle')
text(80,895,'Três nervuras de 18 · dois canais livres sob a base',17)
text(80,1070,'Vão livre reduzido de 577 para 261,5 · material/carga a dimensionar',16,color='#617367')
text(720,855,'ÁREAS LIVRES PARA ESPECIFICAR',21,weight='bold')
for y,a,b in [(899,'Traseira45 ×560','252 cm²'),(937,'Dois canais261,5 ×60','313,8 cm²'),(975,'Cada abertura frontal560 ×60','336 cm² brutos'),(1013,'Cada grelha escolhida: mínimo efetivo','252 cm² (75%)')]:
 text(725,y,a,19);text(1465,y,b,19,anchor='end',weight='bold')
text(725,1060,'Áreas e conexão geométrica verificadas; desempenho térmico não homologado.',16,color='#617367')
text(50,1122,'90 pares sem sobreposição · percurso de ar conectado · R30 preservada · CAD desta proposta salvo separadamente',20,weight='bold')
text(50,1158,'* Topo570 e apoio138 são referências conservadoras. Confirmar relação entre frente, corpo, base e recorte440 no forno real.',18)
text(50,1190,'Faltam: parte inferior/conexões do cooktop, fixação/material/capacidade do apoio, grelhas, elétrica e medidas da unidade.',18)
text(50,1222,'Manuais: Electrolux A29498601/A, p.5/8/9 · Fischer32305 rev.00, p.5–8 · Estudo de detalhamento, sem liberação de fabricação.',17,color='#617367')
p.append('</svg>')
(here/'Apoios_ventilacao.svg').write_text('\n'.join(p),encoding='utf-8')
print(str(here/'Apoios_ventilacao.svg'))
