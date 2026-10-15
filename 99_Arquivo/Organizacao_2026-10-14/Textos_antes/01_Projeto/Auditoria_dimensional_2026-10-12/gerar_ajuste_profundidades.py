from pathlib import Path
import json
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'output/pdf/Ajuste_gavetas_e_profundidade_roupeiro_2026-10-12.pdf'
for n, f in [('Reg', 'arial.ttf'), ('Bold', 'arialbd.ttf')]:
    pdfmetrics.registerFont(TTFont(n, str(Path('C:/Windows/Fonts') / f)))
c = canvas.Canvas(str(OUT), pagesize=(842, 595))
c.setTitle('Guedala Park - gavetas de 40 cm e profundidade do roupeiro')
INK = '#263E40'; WOOD = '#C6A77C'; LIGHT = '#E5ECE7'; WARN = '#9A512D'
def txt(x, y, s, size=11, bold=False, color=INK):
    c.setFillColor(HexColor(color)); c.setFont('Bold' if bold else 'Reg', size); c.drawString(x,y,s)
def para(x,y,w,s,size=11):
    st=ParagraphStyle('p',fontName='Reg',fontSize=size,leading=size*1.4,textColor=HexColor(INK))
    p=Paragraph(s,st); _,h=p.wrap(w,500); p.drawOn(c,x,y-h); return y-h
def rect(x,y,w,h,fill):
    c.setFillColor(HexColor(fill));c.setStrokeColor(HexColor(INK));c.setLineWidth(.6);c.rect(x,y,w,h,fill=1)
def line(x1,y1,x2,y2):
    c.setStrokeColor(HexColor(INK));c.setLineWidth(.8);c.line(x1,y1,x2,y2)
def dim(x1,x2,y,s):
    line(x1,y,x2,y);line(x1,y-4,x1,y+4);line(x2,y-4,x2,y+4)
    c.setFont('Reg',10);c.setFillColor(HexColor(INK));c.drawCentredString((x1+x2)/2,y+7,s)
def head(n,title,sub):
    txt(36,557,'GUEDALA PARK  /  12 OUT 2026',10,True)
    txt(36,520,title,24,True);para(36,499,770,sub)
    line(36,34,806,34);txt(36,20,'Estudo dimensional. Cotas em cm, salvo indicação. Não é lista de corte.',8)
    txt(779,20,f'{n} / 3',8)
def source(y,label,url):
    txt(36,y,label,8);c.linkURL(url,(36,y-2,805,y+10),relative=0,thickness=0)

head(1,'Escritório / ajuste adotado','Duas gavetas com corrediças de comprimento nominal 400 mm e abertura total. O módulo externo continua com 40 L × 45 P × 24 A.')
txt(36,436,'PROFUNDIDADE DO MÓDULO',12,True)
x=53;y=289;k=7.8
rect(x,y,45*k,93,LIGHT);rect(x,y,1.8*k,93,WOOD);rect(x+43.2*k,y,1.8*k,93,WOOD)
rect(x+2.4*k,y+29,40*k,18,'#739499')
dim(x,x+45*k,410,'45,0 externo')
dim(x+1.8*k,x+43.2*k,389,'41,4 disponível na hipótese de construção')
txt(x+69,y+55,'Corrediça nominal 40,0',11,True)
txt(x-8,y-20,'Fundo 1,8',9);txt(x+45*k-44,y-20,'Frente 1,8',9)
para(448,438,350,'<b>Compatibilidade em profundidade:</b><br/>45 − 1,8 − 1,8 = <b>41,4 cm disponíveis</b>.<br/>Na referência MOVENTO 400, o espaço indicado é 40,3 cm sem estabilização lateral; 40,4 cm com o acréscimo de montagem indicado no catálogo. Cabe nesta hipótese.',11)
para(448,313,350,'<b>400 mm não são 40 cm úteis.</b> Na construção MOVENTO, a lateral da caixa tem 390 mm. A largura interna seria 32,2 cm se o gabinete tiver 36,4 cm internos. Profundidade e altura úteis dependem da caixa final. Marca e amortecimento não escolhidos.',11)
para(36,196,770,'<b>Uso com a cama aberta:</b> o curso de estudo passa de 45 para 40 cm. A frente sai de y70 e chega a y110, coincidindo com o início da cama no cenário atual. Desaparece a sobreposição nominal de 5 cm, mas não há folga para prometer abertura livre com roupa de cama. O curso real será reconferido com a ferragem escolhida.',10)
para(36,139,770,'As frentes continuam próximas de 12 cm de altura cada. Não confundir altura da frente com espaço útil. A geometria externa do móvel no modelo permanece 40 × 45 × 24 cm.',10)
source(90,'Blum / construção MOVENTO: lateral = NL − 10 mm; largura interna = vão do gabinete − 42 mm.', 'https://ea.blum.com/en/building-a-movento-drawer/')
source(73,'Blum / catálogo p. 422: espaço NL + 3 mm; conferir notas de montagem e estabilização.', 'https://publications.blum.com/2024/catalogue/pt/422/')
c.showPage()

head(2,'Guarda-roupa / espaço para roupa','Proposta técnica: 65 cm de profundidade total do móvel e pelo menos 55 cm livres para cabides com roupa. A ampliação ainda depende da escolha sobre a passagem.')
txt(36,435,'CORTE EM PLANTA / REQUISITO DE ESPAÇO LIVRE',12,True)
x=49;y=277;k=7.5
rect(x,y,1.8*k,100,WOOD);rect(x+1.8*k,y,55*k,100,LIGHT);rect(x+56.8*k,y,8.2*k,100,'#DCCFC4')
rect(x+4.3*k,y+30,50*k,40,'#9BBABD')
axis=x+29.3*k
c.setDash(3,3);line(axis,y-12,axis,y+115);c.setDash()
dim(x,x+65*k,411,'65,0 total do móvel / hipótese proposta')
dim(x+1.8*k,x+56.8*k,389,'55,0 livres mínimos')
dim(x+4.3*k,x+54.3*k,257,'50,0 envelope de roupa de ensaio')
txt(x,y-38,'Fundo: 1,8',9);txt(x+55*k,y-38,'Frente: até 8,2',9)
para(565,434,236,'<b>O que entra nos 8,2 cm?</b><br/>Portas, trilhos, guias, puxadores internos e qualquer ferragem que avance para a roupa, considerando todo o movimento. É um limite de projeto, não uma medida de ferragem já selecionada.',10)
para(565,312,236,'<b>Eixo do varão:</b> 27,5 cm da face interna do fundo no vão mínimo de 55 cm; equivale a 29,3 cm da traseira externa neste corte.',10)
para(36,209,770,'<b>Critério proposto:</b> reservar 50 cm para a roupa no cabide, mais 2,5 cm de folga de cada lado, totalizando 55 cm. Os 50 cm são um gabarito de estudo, não medição das suas roupas nem limite universal. O cabide BUMERANG de referência mede 43 cm sem roupa; tecido e casacos podem ultrapassar esse tamanho.',11)
para(36,135,770,'<b>Para não encostar:</b> a peça pendurada deve ficar dentro do gabarito, sem torcer o cabide, e as portas devem percorrer todo o curso sem tocar tecido. Peças assimétricas exigem conferir cada lado do eixo. Se a roupa exceder o gabarito, ou a ferragem ocupar mais de 8,2 cm, este corte precisa ser revisto antes de fabricar.',10)
source(58,'IKEA / BUMERANG: cabide de 43 cm. Fonte da medida do cabide vazio, não do envelope vestido.', 'https://www.ikea.com/pt/pt/p/bumerang-cabide-preto-20238534/')
c.showPage()

head(3,'A contrapartida / passagem ao lado da cama','A profundidade maior dá margem para roupa e ferragens, mas o corredor já é estreito. A decisão precisa considerar as duas medidas juntas.')
rows=[('Referência atual',60,54),('Proposta para desenvolver',65,49)]
for i,(label,depth,aisle) in enumerate(rows):
    y=361-i*110; x=36; k=2.52
    txt(x,y+67,label,12,True)
    for w,color in [(1,'#C1C7C0'),(depth,WOOD),(aisle,LIGHT),(160,'#BBC9C9'),(20,'#ECE6DC')]:
        rect(x,y,w*k,48,color);x+=w*k
    txt(45,y+18,f'Armário {depth}',10,True)
    txt(36+(depth+1)*k+8,y+18,f'{aisle} livres',10,True)
    txt(36+(depth+1+aisle)*k+90,y+18,'Cama / estrutura: reserva 160',10)
    txt(36,y-18,'Parede a parede: 295 | proteção posterior: 1 | reserva junto à janela: 20',9)
para(36,199,770,'<b>Conta da proposta:</b> 295 − 20 − 160 − 65 − 1 = <b>49 cm de passagem nominal</b>. Com apenas o colchão de 158 cm seriam 51 cm, mas a estrutura da cama pode ser maior. A proteção posterior de 1 cm é o mínimo considerado; espessura maior reduz ainda mais a passagem. Não classificar 49 cm como circulação confortável.',11)
para(36,128,770,'<b>Efeito no L:</b> se o guarda-roupa e maleiro avançarem juntos 5 cm, o início do aéreo lateral passa de y63 para y68, preservando a junta de 3 cm. Com o mesmo término y285, seu comprimento cai de 222 para 217 cm. Divisão e portas serão recalculadas após a escolha; ferragem do maleiro continua pendente.',10)
source(66,'Escala comercial: IKEA PAX / MEHAMN-AULI, 200 L × 66 P × 236 A, portas de correr (mercado português).', 'https://www.ikea.com/pt/pt/p/pax-mehamn-auli-combinacao-de-roupeiro-cinz-esc-dupla-face-cinz-esc-vidro-espelhado-s29561364/')
txt(36,49,'65 cm é proposta de estudo; referência comercial não prova encaixe nem disponibilidade no Brasil.',8)
c.save()
reader=PdfReader(OUT)
assert len(reader.pages)==3
assert round(45-1.8-1.8,1)==41.4
assert round(65-1.8-8.2,1)==55
assert 295-20-160-65-1==49
assert 285-(65+3)==217
data={'office_nominal_runner_mm':400,'office_external_cm':[40,45,24],
      'office_status':'Ajuste nominal adotado; ferragem exata pendente',
      'wardrobe_proposed_total_depth_cm':65,'wardrobe_min_clear_depth_cm':55,
      'wardrobe_max_front_hardware_budget_cm':8.2,'wardrobe_assumed_back_cm':1.8,
      'clothed_hanger_test_envelope_cm':50,'clothed_hanger_envelope_status':'Hipótese, não medição',
      'proposed_aisle_cm':49,'wardrobe_status':'Proposta; escolha de circulação pendente',
      'pdf_pages':3,'checks':'Contas de profundidade, passagem e comprimento do L conferidas'}
(Path(__file__).parent/'Ajuste_profundidades_dados.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
print(OUT)
