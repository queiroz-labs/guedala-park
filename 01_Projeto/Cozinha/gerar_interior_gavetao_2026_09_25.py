from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
p=Path(__file__).parent
im=Image.new('RGB',(1400,1060),'#f7f4ee');d=ImageDraw.Draw(im)
ink='#283d41'
def t(x,y,s,n=24): d.text((x,y),s,font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',n),fill=ink)
t(55,30,'GAVETÃO | Organização interna aprovada',38)
t(55,91,'Vista de cima · referência interna de teste: 52,7 × 47 cm',26)
x,y,k=80,205,12
d.rectangle((x,y,x+52.7*k,y+47*k),fill='#d7bd96',outline=ink,width=3)
def zone(a,b,w,h,color,lines):
 d.rectangle((x+a*k,y+b*k,x+(a+w)*k,y+(b+h)*k),fill=color,outline=ink,width=2)
 for i,line in enumerate(lines):t(x+a*k+15,y+b*k+22+i*38,line,23)
zone(1,1,27.7,25,'#eee6d7',['ALIMENTOS ABERTOS','Arroz / feijão','Café / açúcar','27,7 × 25 cm'])
zone(1,27,27.7,19,'#ecd5a9',['TEMPEROS EM PÉ','Organizador removível','27,7 × 19 cm'])
zone(29.7,1,22,45,'#cbdcdf',['EMBALAGENS EM PÉ','Leite e sucos','Óleo e azeite','22 × 45 cm (teste)','Encaixe a conferir'])
t(80,160,'FUNDO',22)
t(225,794,'FRENTE / PUXADOR',25)
t(790,220,'Uma caixa, três setores',29)
t(790,280,'Separadores removíveis',25)
t(790,322,'Abertura total',25)
t(790,364,'Base antiderrapante lavável',25)
t(790,460,'Ainda sem espaço comprovado:',24)
t(790,505,'molhos e enlatados.',24)
t(790,592,'40 cm = altura bruta do módulo.',24)
t(790,635,'Altura livre depende da montagem.',24)
t(55,895,'As áreas são reservas de espaço: embalagens e recipientes ainda precisam ser testados.',24)
t(55,946,'Não representa capacidade comprovada nem medidas para compra de organizadores.',24)
im.save(p/'Interior_gavetao_2026-09-25.png')