from pathlib import Path
import json,html
here=Path(__file__).resolve().parent
r=json.loads((here/'Conferencia.json').read_text(encoding='utf-8'))
g=r['grille']; assert g['free_area_cm2']>252
def plate(x,y,s,fill='#334c43',line='#233e38'):
 a=[f'<rect x="{x}" y="{y}" width="{600*s}" height="{90*s}" rx="{2*s}" fill="{fill}" stroke="{line}"/>']
 for xx in [23,163,303,443]:
  for zz in [17,36.5,56]:
   a.append(f'<rect x="{x+xx*s}" y="{y+(90-zz-17)*s}" width="{134*s}" height="{17*s}" rx="{3*s}" fill="#eff7f4" stroke="none"/>')
 for xx in [100,500]:
  for zz in [7.5,82.5]:a.append(f'<circle cx="{x+xx*s}" cy="{y+(90-zz)*s}" r="{2.25*s}" fill="#eff7f4"/>')
 return '\n'.join(a)
# Contornos puros para troca com fornecedor. Cotação, não liberação industrial.
q=['<svg xmlns="http://www.w3.org/2000/svg" width="600mm" height="90mm" viewBox="0 0 600 90"><title>Grelha R02 — gabarito de cotação, conferir antes de cortar</title><g fill="none" stroke="black" stroke-width="0.1">','<rect x="0" y="0" width="600" height="90" rx="2"/>']
for x in g['slot_x_mm']:
 for z in g['slot_z_mm']:
  q.append(f'<rect x="{x}" y="{90-z-17}" width="134" height="17" rx="3"/>')
for x in g['mount_holes_x_mm']:
 for z in g['mount_holes_z_mm']:q.append(f'<circle cx="{x}" cy="{90-z}" r="2.25"/>')
q.append('</g></svg>');(here/'Gabarito_cotacao_grelha_1a1.svg').write_text('\n'.join(q),encoding='utf-8')
p=['<svg xmlns="http://www.w3.org/2000/svg" width="1510" height="1110"><style>text{font-family:Arial,sans-serif;fill:#233e38}</style><rect width="1510" height="1110" fill="#f4f1e9"/>']
def text(x,y,t,size=19,color='#233e38',weight='normal',anchor='start'):
 for i,l in enumerate(t.split('\n')):p.append(f'<text x="{x}" y="{y+i*(size+7)}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" style="fill:{color}">{html.escape(l)}</text>')
def rect(x,y,w,h,fill,stroke='#233e38'):p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}"/>')
def line(x,y,xx,yy,stroke='#63897e',width=1.5):p.append(f'<path d="M{x} {y}L{xx} {yy}" fill="none" stroke="{stroke}" stroke-width="{width}"/>')
text(48,43,'GUEDALA PARK  /  COZINHA  /  GRELHAS E MANUTENÇÃO R02  /  20.10.2026',17,color='#537568')
text(48,90,'Grelhas removíveis para o conjunto Fischer + KE4GC',33,weight='bold')
text(48,125,'Proposta dimensionada para cotação · sem nova escolha de aparelho · sem liberação de fabricação',19)
rect(43,150,555,738,'#fffdf7','#e6e1d5');rect(622,150,845,440,'#fffdf7','#e6e1d5');rect(622,612,845,276,'#fffdf7','#e6e1d5')
text(68,189,'COMO FICA NA FRENTE DO MÓVEL',21,weight='bold')
s=.55;ox=110;base=812
def box(x,z,w,h,fill):rect(ox+x*s,base-(z+h)*s,w*s,h*s,fill)
box(0,0,18,900,'#c0a078');box(595,0,18,900,'#c0a078');box(0,900,613,20,'#b6bcb4')
box(0,920,600,15,'#273b35');box(18,120,577,18,'#c0a078')
for x in [18,297.5,577]:box(x,0,18,120,'#c0a078')
box(9,123,595,447,'#273b35');box(65,200,480,265,'#536b60')
text(ox+306.5*s,base-365*s,'Fischer Infinity',20,color='white',anchor='middle');text(ox+306.5*s,base-314*s,'grill · sem turbo',18,color='white',anchor='middle')
for x in [125,305,485]:p.append(f'<circle cx="{ox+x*s}" cy="{base-515*s}" r="5" fill="#c4d0c7"/>')
for z in [15,690]:p.append(plate(ox+6.5*s,base-(z+90)*s,s))
text(ox+306.5*s,458,'Faixa técnica',16,color='#617367',anchor='middle')
text(ox+306.5*s,482,'frentes a detalhar',16,color='#617367',anchor='middle')
text(70,238,'Módulo 613 · bancada 920',18)
text(462,389,'Saída',18);line(451,395,ox+604*s,base-735*s)
text(462,786,'Entrada',18);line(452,791,ox+604*s,base-60*s)
text(73,854,'Cor ilustrativa; acabamento acompanha a marcenaria aprovada.',16,color='#617367')
text(648,190,'DUAS PEÇAS IGUAIS',22,weight='bold')
text(648,226,'600 ×90 mm · chapa candidata de inox 1,5 mm',20)
p.append(plate(686,283,1.12))
text(1022,269,'600',18,anchor='middle');line(686,274,1358,274)
text(1380,342,'90',18);line(1372,283,1372,384)
text(650,428,'12 rasgos de 134 ×17, com cantos R3',20)
text(650,462,'Quatro furos Ø4,5 para fixação removível M4',20)
text(650,496,'Área aberta por peça:',20);text(1025,496,'272,43 cm²',27,weight='bold')
text(650,535,'8,1% acima dos 252 cm² adotados no projeto',21,color='#287c8c')
text(650,570,'Área geométrica, sem tela. Vazão e temperatura ainda precisam de verificação.',16,color='#617367')
text(648,651,'SUPORTES FORA DA PASSAGEM DE AR',21,weight='bold')
# Corte abstrato da grelha; régua não atravessa o vão útil.
rect(688,693,32,154,'#334c43');rect(720,693,120,32,'#c0a078');rect(720,815,120,32,'#c0a078')
rect(720,725,120,90,'#b8dde3','#6cacb8');line(747,772,831,772,'#218da1',5)
text(870,714,'Duas réguas de acabamento por grelha',19)
text(870,748,'Fixação nas bordas; não recebe peso do forno',19)
text(870,782,'Parafusos acessíveis pela frente',19)
text(870,816,'Sem colar a grelha nem fechar os rasgos',19)
text(648,871,'A união das réguas e a retenção da rosca dependem do material final.',16,color='#617367')
text(48,935,'Manutenção: retirada frontal de 600 mm testada com os envelopes do estudo.',22,weight='bold')
text(48,974,'195 pares sem sobreposição · passagem de ar atravessa os rasgos reais · R30 e R01 preservadas',20)
text(48,1013,'Acesso às conexões: desenvolver pelo gabinete da pia à esquerda, após compatibilizar hidráulica e área seca. Gás GN já confirmado.',18)
text(48,1050,'Pendentes: apoio e furos reais dos aparelhos, material/ligações do móvel, elétrica e medidas da unidade. Nenhum contato ou compra realizado.',17)
text(48,1086,'Gabarito 1:1 separado para cotação · Sem confirmação de circulação de pessoas, comprimentos de cabos ou resistência/temperatura.',17,color='#617367')
p.append('</svg>');(here/'Grelhas_manutencao.svg').write_text('\n'.join(p),encoding='utf-8')
print('Desenhos SVG gravados.')
