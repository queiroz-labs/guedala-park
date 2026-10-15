from pathlib import Path
import json
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
data = json.loads((ROOT / 'Detalhe_banco_resultados.json').read_text(encoding='utf-8'))
im = Image.new('RGB', (1800, 1180), '#f5f2e9')
d = ImageDraw.Draw(im)
def font(size, bold=False):
    return ImageFont.truetype('C:/Windows/Fonts/' + ('segoeuib.ttf' if bold else 'segoeui.ttf'), size)
ink='#263e35'; line='#56695c'; wood='#d5b98f'; blue='#adcddc'; orange='#aa7046'
def text(x,y,t,size=28,bold=False,fill=ink):
    d.text((x,y),t,font=font(size,bold),fill=fill)
text(65,38,'Acesso ao balde: separar a almofada da tampa',48,True)
text(65,105,'Mesmo banco e mesma guarda • mecanismo proposto, ainda sem ferragem definida',28)

def scene(left, new):
    s=5; X=lambda u:left+190+u*s; Y=lambda z:820-z*s
    text(left+30,180,'Tampa fina + almofada removível' if new else 'Assento inteiro de 7 cm aberto',33,True)
    text(left+30,230,'37,8 cm de passagem • 2,4 cm por lado' if new else '33 cm de passagem • nenhuma folga',27,fill=line if new else orange)
    def rect(u,z,w,h,color,outline=line):
        d.rectangle((X(u),Y(z+h),X(u+w),Y(z)),fill=color,outline=outline,width=2)
    # Section at the bucket bay; table and backrest retain their actual model locations.
    rect(-19,72,24,3,'#839689')
    rect(45,40,10,50,'#c4b69d')
    rect(0,0,1.8,40,wood);rect(40.8,0,4.2,40,wood);rect(1.8,8.2,39,1.8,wood)
    if new:
        rect(42.8,42,2,44.8,wood)
        u=7.4; gap=data['bucket']['perSideExtra']; end=42.8
    else:
        rect(38,47,7,45,'#c4b69d')
        u=5;gap=0;end=38
    rect(u,52,33,25,blue)
    # Stored body and direction of extraction. The handle is intentionally not invented.
    d.rectangle((X(5.5),Y(35.3),X(38.5),Y(10.3)),outline='#94a69e',width=2)
    d.line((X(22),Y(39),X(22),Y(48)),fill=line,width=4)
    d.polygon([(X(22),Y(49)),(X(21),Y(47)),(X(23),Y(47))],fill=line)
    text(left+30,850,'Corpo de teste: 33 × 25 cm neste corte',26)
    # Opening dimension, above the obstructions.
    yy=Y(96)
    d.line((X(5),yy,X(end),yy),fill=ink,width=3)
    for xx in [X(5),X(end)]:d.line((xx,yy-9,xx,yy+9),fill=ink,width=3)
    label='37,8 cm' if new else '33 cm'
    d.text(((X(5)+X(end))/2,yy-35),label,font=font(27,True),fill=ink,anchor='mm')
    # Direct labels avoid scale-dependent small text inside objects.
    text(left+15,355,'Mesa',25)
    d.line((left+94,377,X(-9),Y(73.5)),fill=line,width=2)
    text(left+560,315,'Encosto',25)
    d.line((left+630,349,X(50),Y(85)),fill=line,width=2)
    text(left+560,450,'Tampa 2 cm' if new else 'Assento 7 cm',25)
    d.line((left+560,483,X(43.8 if new else 41.5),Y(64)),fill=line,width=2)
    text(left+45,680,'Balde em elevação',25)
    d.line((left+190,705,X(u+8),Y(56)),fill=line,width=2)
    text(left+30,895,'Alça, mãos e ferragens reais ainda precisam de conferência.',24)

scene(45,False);scene(925,True)
d.line((900,175,900,935),fill='#d0d7cb',width=2)
text(65,975,'Como usar a alternativa',32,True)
text(65,1028,'1  Apoiar a almofada no assento da ponta     2  Abrir e reter a tampa fina     3  Retirar o balde',28)
text(65,1095,'Banco externo: 180 × 55 cm • assento: 45 cm de profundidade, topo a 47 cm • cotas de estudo',26,fill=line)
im.save(ROOT / 'Detalhe_acesso_balde.png')
print('Detalhe_acesso_balde.png')
