from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from html import escape
P=Path(__file__).parent
W,H=1500,1180
im=Image.new("RGB",(W,H),"#f7f4ee")
d=ImageDraw.Draw(im)
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1500" height="1180" viewBox="0 0 1500 1180">','<rect width="1500" height="1180" fill="#f7f4ee"/>']
def text(x,y,s,size=20,fill="#34372f",bold=False,anchor="la"):
    f=ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",size)
    d.text((x,y),s,font=f,fill=fill,anchor=anchor)
    align="middle" if anchor=="ma" else "start"
    svg.append(f'<text x="{x}" y="{y+size*.92}" font-family="Arial" font-size="{size}" font-weight="{700 if bold else 400}" text-anchor="{align}" fill="{fill}">{escape(s)}</text>')
def rect(x,y,w,h,fill,outline="#bcb4a5"):
    d.rectangle((x,y,x+w,y+h),fill,outline,width=1)
    svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{outline}"/>')
def line(x,y,x2,y2,fill="#4b5444",width=3):
    d.line((x,y,x2,y2),fill,width)
    svg.append(f'<line x1="{x}" y1="{y}" x2="{x2}" y2="{y2}" stroke="{fill}" stroke-width="{width}"/>')
X,Y,S=115,180,3
def box(x,h,w,ht,fill="#cfb795"):
    rect(X+x*S,Y+(240-h-ht)*S,w*S,ht*S,fill)
def label(x,h,s,size=17,bold=False):
    text(X+x*S,Y+(240-h)*S,s,size,bold=bold,anchor="ma")
def rail(x,h,w):
    line(X+(x+2)*S,Y+(240-h)*S,X+(x+w-2)*S,Y+(240-h)*S,width=5)
text(55,35,"Mais cabides, sapateira compacta",38,bold=True)
text(55,86,"Guarda-roupa R02  |  200 L × 60 P × 240 A cm  |  Proposta de organização",23)
text(260,143,"PESSOA 1",19,bold=True,anchor="ma")
text(570,143,"PESSOA 2",19,bold=True,anchor="ma")
box(0,0,200,240,"#fffdf8")
# full sides and central divider
for x in [0,99.1,198.2]: box(x,6.2,1.8,233.8)
for h in [6.2,213.2,238.2]:box(0,h,200,1.8)
# left storage, shorts, long; right mirrored
for start,storage,short,long,divA,divB,shelfStart in [
    (1.8,1.8,39.1,74.1,37.3,72.3,1.8),
    (100.9,162.7,127.7,100.9,160.9,125.9,127.7)]:
    # full upper rail; lower partitions stop at 110
    for x in [divA,divB]:box(x,8,1.8,102)
    box(shelfStart,108.2,70.5,1.8)
    rail(start,205,97.3)
    rail(short,103,33.2)
    label(start+48.65,194,"Varão superior · 97,3 cm",20,True)
    # cloth zone and long reservation
    label(start+48.65,178,"Camisas, polos, camisetas e casacos",15)
    label(short+16.6,86,"Curtos",17,True)
    label(short+16.6,76,"33,2 cm",16)
    label(short+16.6,66,"queda 95",14)
    label(long+12.5,123,"1 casaco",15,True)
    label(long+12.5,114,"longo",15,True)
    label(long+12.5,99,"25 cm",16)
    label(long+12.5,87,"largura",14)
    line(X+(long+12.5)*S,Y+(240-72)*S,X+(long+12.5)*S,Y+(240-24)*S,"#b9baa9",2)
    # shelves: 2+2+1 pairs, two upper drawers
    for h in [32.2,58.2,78.2]:box(storage,h,35.5,1.8)
    for h,caption in [(8,"2 pares*"),(34,"2 pares*"),(60,"1 par")]:
        label(storage+17.75,h+15,caption,17,True)
    for h in [80,95]:
        box(storage+0.8,h,33.9,14.2,"#dedfcf")
        label(storage+17.75,h+10,"Gaveta",15)
    label(start+48.65,230,"Maleiro · 23,2 cm livres",19)
text(115,925,"35,5  |  33,2  |  25 cm",19)
text(420,925,"25  |  33,2  |  35,5 cm",19)
text(115,959,"Larguras úteis inferiores; divisórias de 1,8 cm.",17)
# right panel
rect(795,155,650,167,"#e8ebdf",outline="#e8ebdf")
text(823,177,"2,61 m de varões nominais",29,bold=True)
text(823,223,"Antes: 1,864 m  →  ganho de aproximadamente 40%",20)
text(823,263,"Mesmo envelope, mesma circulação prevista.",21)
text(815,352,"O QUE CADA PESSOA GANHA",19,bold=True)
for i,s in enumerate(["• Um varão superior de ponta a ponta.","• Um varão inferior para roupas curtas.","• Reserva para um casaco longo.","• Duas gavetas e cinco pares de tênis.","• Metade do maleiro para dobrados e uso eventual."]):
    text(815,392+i*35,s,21)
text(815,590,"SAPATEIRA: 2 + 2 + 1 PARES",19,bold=True)
for i,s in enumerate(["Dois níveis com um tênis acima do outro,","em suportes separados; último nível com par simples.","Prateleiras fixas reguláveis: sem bandeja extraível.","*Capacidade depende dos tênis e dos organizadores."]):
    text(815,629+i*30,s,20)
text(815,775,"TROCAS DO NOVO PLANO",19,bold=True)
for i,s in enumerate(["Gavetas com frentes de 15 cm, para íntimas e meias.","Prateleiras superiores dão lugar aos cabideiros.","Varão a 205 cm: testar alcance dos dois usuários.","Conferir abertura das gavetas e portas de correr."]):
    text(815,814+i*31,s,20)
line(55,1015,1445,1015,"#c7c4b9",1)
text(55,1040,"Circulação preservada: 55–57 cm diante do armário; 45–47 cm nos pés da cama.",22,bold=True)
text(55,1080,"Altura 240 cm e afastamento de 20 cm na janela são hipóteses de estudo. Medir cama e teto acabados.",20)
text(55,1113,"Vista sem portas. Cores ilustrativas. Não é lista de corte; o ganho depende da validação da sapateira.",20)
text(55,1146,"F134 · 13/09/2026",16)
svg.append("</svg>")
im.save(P/"Guarda_roupa_interior_R02.png")
(P/"Guarda_roupa_interior_R02.svg").write_text("\n".join(svg),encoding="utf-8")
assert abs(2*(35.5+1.8+33.2+1.8+25)+3*1.8-200)<1e-8
assert abs(2*(97.3+33.2)-261)<1e-8
print("R02 gerada. Largura total 200 cm; varões 261 cm.")
