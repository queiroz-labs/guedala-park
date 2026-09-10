from pathlib import Path
import json, math, sys
import numpy as np
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader

sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path(__file__).resolve().parents[3]
WORK = Path(__file__).resolve().parent
OUT = ROOT/'02_Projeto_em_desenvolvimento'/'A01.2_Base_dimensional'
OUT.mkdir(parents=True, exist_ok=True)
BASE = ROOT/'04_Levantamento'/'levantamento'
fontdir = Path('C:/Windows/Fonts')
pdfmetrics.registerFont(TTFont('Segoe',str(fontdir/'segoeui.ttf')))
pdfmetrics.registerFont(TTFont('SegoeB',str(fontdir/'segoeuib.ttf')))
W,H = 841.89,595.28
INK = colors.HexColor('#183742')
TEXT = colors.HexColor('#26343B')
BLUE = colors.HexColor('#286D94')
AMBER = colors.HexColor('#A56324')
GREEN = colors.HexColor('#297366')
PALE = colors.HexColor('#F1F4F3')
MUTED = colors.HexColor('#627176')
PDF = OUT/'A01.2_Base_dimensional_Cozinha_Lavanderia_R00.pdf'
c = canvas.Canvas(str(PDF),pagesize=(W,H))
c.setTitle('A01.2 - Base dimensional e instalações | Cozinha e lavanderia | R00')
c.setAuthor('Projeto Apartamento Elias')

def p(text,x,top,width,size=10,color=TEXT,bold=False):
    style=ParagraphStyle('p',fontName='SegoeB' if bold else 'Segoe',fontSize=size,leading=size*1.35,textColor=color)
    obj=Paragraph(text,style);_,h=obj.wrap(width,1000)
    obj.drawOn(c,x,H-top-h)
    return h

def line(x1,y1,x2,y2,color=INK,width=1,dash=None):
    c.setStrokeColor(color);c.setLineWidth(width);c.setDash(dash or [])
    c.line(x1,H-y1,x2,H-y2);c.setDash([])

def box(x,top,w,h,fill=PALE,stroke=None):
    c.setFillColor(fill)
    if stroke:c.setStrokeColor(stroke)
    c.rect(x,H-top-h,w,h,fill=1,stroke=int(stroke is not None))

def heading(num,title,subtitle):
    box(0,0,W,8,INK)
    p('GUEDALA PARK  /  ELIAS',34,22,500,10,INK,True)
    p('A01.2  •  R00  •  08/09/2026',608,22,200,9,MUTED)
    p(title,34,45,780,23,INK,True)
    p(subtitle,34,81,772,10,MUTED)
    line(34,554,808,554,colors.HexColor('#CBD4D3'),.7)
    p('ESTUDO PRELIMINAR • Cotas documentais e estimativas identificadas • Sem liberação para fabricação',34,563,735,8,MUTED)
    p(str(num).zfill(2),786,560,24,10,INK,True)

def table(headers,rows,widths,x,top,size=9):
    def cell(v,head=False):
        return Paragraph(str(v),ParagraphStyle('t',fontName='SegoeB' if head else 'Segoe',fontSize=size,leading=size*1.22,textColor=colors.white if head else TEXT))
    data=[[cell(v,True) for v in headers]]+[[cell(v) for v in row] for row in rows]
    tb=Table(data,colWidths=widths,hAlign='LEFT')
    tb.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),INK),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,PALE]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),3 if size < 9 else 5),('BOTTOMPADDING',(0,0),(-1,-1),3 if size < 9 else 5),('LINEBELOW',(0,-1),(-1,-1),.5,colors.HexColor('#CBD4D3'))]))
    _,th=tb.wrap(sum(widths),1000)
    if top+th>547:raise ValueError(f'Tabela fora da página: top={top}, height={th}')
    tb.drawOn(c,x,H-top-th)
    return th

def photo(path,x,top,w,h):
    im=Image.open(path)
    iw,ih=im.size;scale=min(w/iw,h/ih);dw=iw*scale;dh=ih*scale
    c.drawImage(ImageReader(im),x,H-top-dh,dw,dh)
    return lambda u,v:(x+u*scale,top+v*scale),dh

def pin(x,y,label,color=BLUE):
    # Ponteiro no elemento; etiqueta deslocada para não encobrir o registro.
    cx,cy=x+16,y-16
    line(x,y,cx,cy,color,1.2)
    c.setFillColor(color);c.circle(cx,H-cy,9,fill=1,stroke=0)
    c.setFont('SegoeB',8);c.setFillColor(colors.white);c.drawCentredString(cx,H-cy-3,str(label))

def tag(label,tx,ty,px,py,color=BLUE):
    tw=pdfmetrics.stringWidth(label,'SegoeB',8)+12
    line(tx+tw/2,ty+8,px,py,color,.9)
    box(tx,ty,tw,16,color)
    p(label,tx+6,ty+2,tw-8,8,colors.white,True)

# ETAPA 1 - base original ampliada com orientação preservada.
heading(1,'Cozinha e lavanderia: base de trabalho','Etapa 1 • Planta oficial na orientação original; identificação dos trechos e das faces a estudar.')
src=Image.open(WORK/'planta_300.png')
# Recorte da folha P01, sem redesenhar ou espelhar as paredes.
crop=src.crop((1180,1230,2200,1610))
c.drawImage(ImageReader(crop),48,H-151-228,612,228)
def planxy(px,py):return 48+(px*300/72-1180)*.6,151+(py*300/72-1230)*.6
for label,pt,labelpos in [
    ('J / L3',(298,334),(35,120)),
    ('L1 / L2',(328,358),(180,400)),
    ('K1',(417,372),(445,400)),
    ('E',(517,348),(627,400)),
    ('F',(358.34,310),(255,120))]:
    px,py=planxy(*pt);tag(label,*labelpos,px,py)
p('J',679,123,25,11,BLUE,True);p('Parede da janela',700,123,102,10)
p('K1',679,168,30,11,BLUE,True);p('Parede da pia e equipamentos',710,168,94,10)
p('L1/L2',679,227,65,11,BLUE,True);p('Face do tanque e retorno técnico',679,248,123,10)
p('F',679,304,25,11,BLUE,True);p('Faixa desenhada entre os setores. Tipo a confirmar.',701,304,105,10)
p('E',679,374,25,11,BLUE,True);p('Entrada',701,374,105,10)
box(34,434,774,106)
p('Leitura consolidada das cotas',46,444,730,12,INK,True)
p('<b>1,29 m:</b> área de serviço na direção J → E, paralela à frente da cozinha. <b>1,54 m:</b> direção perpendicular, junto ao limite com a cozinha. <b>3,52 m:</b> trecho da cozinha, após a faixa F até a lateral da entrada. <b>1,55 m:</b> cota transversal indicada na cozinha.',46,466,742,10)
p('A soma 1,29 + 3,52 = 4,81 m reúne dois trechos cotados; não define o comprimento da bancada. A faixa F, os ressaltos, os equipamentos e o giro da entrada precisam ser considerados.',46,510,742,9,MUTED)
c.showPage()

# ETAPA 2 - estimativas com origem reproduzível.
scales=[(357.56-300.68)/1.29,(513.92-359.12)/3.52,(373.52-305)/1.55]
S=float(np.median(scales))
estimates=[
    ['G-01','Vão desenhado da janela de serviço',43.56,'0,99 m','0,96-1,01 m','Extremos da abertura em P01; não é passagem livre de ar.'],
    ['G-02','Abertura representada da entrada',35.64,'0,81 m','0,78-0,83 m','Representação do vão; não comprova largura útil entre batentes.'],
    ['G-03','Largura do símbolo da pia',52.80,'1,20 m','1,17-1,22 m','Dimensão do símbolo em P01; não identifica a pia entregue.'],
    ['G-04','Profundidade do símbolo da pia',23.28,'0,53 m','0,50-0,55 m','Dimensão gráfica; não especifica a bancada futura.'],
    ['G-05','Entre contorno do ressalto e início da pia',50.52,'1,15 m','1,12-1,17 m','Trecho gráfico; tem instalações no vídeo e não está livre para móveis.'],
    ['G-06','Extensão transversal entre faces laterais',213.24,'4,84 m','4,80-4,87 m','Inclui a faixa F; projeção entre faces, não percurso de pedra.'],
    ['G-07','Recuo do contorno estrutural junto ao tanque',8.76,'0,20 m','0,17-0,22 m','Apenas a linha de contorno de P01; não é a profundidade total do shaft.'],
]
heading(2,'O que já pode ser estimado','Etapa 2 • Valores extraídos do desenho, separados de medidas reais e dos modelos de equipamento.')
table(['ID / trecho','Estimativa','Sensibilidade gráfica*','Limite de uso'],[[f'<b>{a}</b> • {b}',d,e,f] for a,b,_,d,e,f in estimates],[275,80,110,309],34,115,9)
box(34,414,774,127)
p('Como os valores foram calculados',46,423,742,12,INK,True)
p(f'Foram comparadas três cotas de P01: 1,29 m, 3,52 m e 1,55 m. As escalas gráficas ficaram entre {min(scales):.2f} e {max(scales):.2f} pontos de PDF por metro; foi usada a mediana de {S:.2f}. Diferença relativa de aproximadamente 0,52%.',46,446,742,9.5)
p('* As faixas mostram a sensibilidade a ±0,4 ponto em cada extremidade e à variação entre as três escalas, arredondadas para fora. Não são intervalos estatísticos, tolerâncias de obra nem precisão garantida no apartamento. Em caso de divergência, prevalece a cota escrita.',46,484,742,9.5)
c.showPage()

# ETAPA 3 - mapa fotográfico da parede de equipamentos.
heading(3,'Mapa de instalações: cozinha','Etapa 3 • Fotografias da unidade espelhada. Marcadores identificam elementos; não fornecem coordenadas de execução.')
panels=[
    ('AD-0166',34,115,[(398,478,'4'),(835,485,'2'),(1115,504,'1')],'1 K-E01 • 2 K-E02 (dupla) • 4 K-E04'),
    ('AD-0178',430,115,[(850,347,'3')],'3 K-E03 • tomada alta; função elétrica a confirmar'),
    ('AD-0206',34,329,[(544,811,'5')],'5 K-E05 • tomada sob a pia; suportes e sifão visíveis'),
    ('AD-0246',430,329,[(913,490,'6'),(913,660,'7'),(1104,859,'G')],'6 K-E06 (dupla) • 7 K-E07 • G K-G01 (gás)'),
]
for name,x,t,pins,cap in panels:
    fn=BASE/'adicional'/'frames'/f'{name}.jpg'
    xy,dh=photo(fn,x,t,378,188)
    for u,v,s in pins:
        xx,yy=xy(u,v);pin(xx,yy,s)
    p(f'<b>{name}</b> • {cap}',x,t+190,378,8.5)
c.showPage()

heading(4,'Mapa de instalações: lavanderia','Etapa 3 • As faces L1/L2 e a parede J/L3 são correlacionadas à planta por topologia, com espelhamento considerado.')
items=[
    (BASE/'frames'/'lavanderia'/'LAV-07_05m30s.jpg',34,115,[(1000,445,'V'),(1670,831,'H'),(1497,992,'D')],'LAV-07 • V grelha L-V01 • H registro L-H04 • D ralo L-D01'),
    (BASE/'adicional'/'frames'/'AD-0278.jpg',430,115,[(220,872,'H'),(813,916,'H'),(516,1040,'G')],'AD-0278 • L-H02: conexões • L-G01: gás • aviso do aquecedor'),
    (BASE/'adicional'/'frames'/'AD-0302.jpg',34,329,[(657,583,'H'),(776,713,'H')],'AD-0302 • L-H03: conexões no retorno; função individual a confirmar'),
    (BASE/'frames'/'lavanderia'/'LAV-08_05m42s.jpg',430,329,[(1343,400,'V'),(1571,435,'C')],'LAV-08 • L-V02: abertura alta • L-C01: ressalto e volumes superiores'),
]
for fn,x,t,pins,cap in items:
    xy,dh=photo(fn,x,t,378,188)
    for u,v,s in pins:
        xx,yy=xy(u,v);pin(xx,yy,s,GREEN)
    p(cap,x,t+190,378,8.5)
c.showPage()

inventory=[
 ('K-E01','K1','Tomada próxima à entrada',1,'AD-0166','Circuito, tensão e posição na unidade.'),
 ('K-E02','K1','Placa dupla à direita da pia no vídeo',2,'AD-0166/0170','Circuitos e altura da bancada futura.'),
 ('K-E03','K1','Tomada alta',1,'AD-0178','Função, circuito e altura.'),
 ('K-E04','K1','Tomada acima da pia',1,'AD-0186','Altura e relação com frontão.'),
 ('K-E05','K1','Tomada sob a pia',1,'AD-0202/0206','Acesso pelo gabinete e circuito.'),
 ('K-E06','K1','Placa dupla próxima ao retorno técnico',2,'AD-0246','Circuitos e posição.'),
 ('K-E07','K1','Tomada abaixo de K-E06',1,'AD-0246','Equipamento atendido e circuito.'),
 ('K-G01','K1','Registro de gás entre pia e tanque',1,'AD-0238/0246','Posição real e acesso à conexão.'),
 ('K-H01','K1','Torneira da pia, dois comandos','conj.','AD-0218','Identificar água fria/quente.'),
 ('K-H02','K1','Sifão, fechamento e suportes da pia','conj.','AD-0202/0206','Volume ocupado e acesso.'),
 ('L-H01','L1','Tanque suspenso e torneira','conj.','AD-0262','Eixos, fixação e geometria.'),
 ('L-H02','L1','Duas conexões na região do aquecedor',2,'AD-0278','Identificar cada entrada/saída.'),
 ('L-G01','L1','Válvula de gás junto ao aquecedor',1,'AD-0278','Ligação, manual e acesso.'),
 ('L-H03','L2','Ponto tampado e abertura inferior',2,'AD-0302','Provável máquina; função e diâmetros.'),
 ('L-H04','L1','Registro abaixo do tanque',1,'AD-0262','Trecho da rede que ele isola.'),
 ('L-G02','L1/L2','Tubulação aparente sob o tanque','-','AD-0262/0246','Rede provável de gás; percurso completo.'),
 ('L-D01','piso AS','Ralo próximo ao tanque',1,'AD-0262','Localização, acesso e caimentos.'),
 ('L-V01','J/L3','Grelha abaixo da janela',1,'LAV-07','Dimensões, função e área livre.'),
 ('L-V02','J/L3','Abertura circular acima da janela',1,'LAV-08','Função de exaustão ainda não comprovada.'),
 ('L-C01','L1/L2','Ressalto e volumes superiores','conj.','AD-0322','Profundidades e alturas reais.'),
 ('L-I01','oposta','Interfone',1,'AD-0334','Posição e acesso à operação.'),
 ('E-C02','oposta','Duas teclas junto ao interfone',2,'AD-0334','Retorno de cada comando.'),
 ('T-I01','teto','Saídas no conjunto social/cozinha/AS',4,'AD-0446','Separar ambientes, eixos e circuitos.'),
]
heading(5,'Inventário consolidado de pontos','23 registros • Elementos observados na unidade filmada. Coordenadas X/Y/Z da unidade de Elias continuam sem medição.')
table(['ID','Face','Elemento observado','Qtd.','Evidência','Conferência necessária'],inventory,[58,48,232,35,94,307],34,111,8)
c.showPage()

heading(6,'Limites, correções e continuidade','Etapas 1 a 3 concluídas com a base disponível • 8º andar informado por Elias; planta de referência: Torre 2, final 06.')
box(34,115,374,174)
p('Teste no vídeo: proporção, sem cota em cm',46,125,350,12,INK,True)
p('No frame COZ-02, foi feita uma retificação piloto usando os quatro cantos externos da janela como referência. A largura externa da grelha resultou em aproximadamente <b>46% da largura externa da janela</b>. Ao variar as marcações em ±5 pixels, 1.000 perturbações deram resultados entre 42% e 49%.',46,153,350,9.5)
p('Resultado exploratório: planos próximos, bordas pouco nítidas e lente sem calibração. Não foi convertido em centímetros nem em área de ventilação. A altura da janela continua desconhecida.',46,236,350,9.5)
box(428,115,380,174)
p('Informações que continuam sem cota',440,125,355,12,INK,True)
p('Pé-direito e rebaixos; alturas da janela e do peitoril; volume técnico completo; eixos e alturas das instalações; folgas de manutenção; percurso oculto de tubulações.',440,153,350,10)
p('Não há medida dos revestimentos originais. Não se adotou tamanho padrão de azulejo, tomada, tanque ou porta como régua do vídeo. A estimativa antiga de pé-direito de 2,60 m permanece fora da base dimensional.',440,214,350,9.5)
p('Correções de interpretação para o estudo da lavanderia',34,306,774,13,INK,True)
p('• A planta já distingue a direção de 1,29 m da direção de 1,54 m. Não tratar essas cotas como opções para uma mesma parede.<br/>• O estudo A04.1 R00 não comprova que máquina + tanque + apoio caibam ou não caibam: as conclusões baseadas em larguras típicas devem ser substituídas por geometria e modelos reais.<br/>• Os 15 cm são uma intenção de apoio do briefing, não uma cota encontrada na planta ou no vídeo; posição e forma ainda precisam ser desenhadas.<br/>• A R02 corrige o frame de 11:06 e associa provavelmente A → Dormitório 02 e B → Dormitório 01. A geometria de P01 permanece na orientação original.',34,331,774,10)
p('Próximo uso desta base',34,446,774,12,INK,True)
p('Desenvolver alternativas preliminares para a lavanderia, preservando pedra contínua, máquina única, tanque esculpido, cesto ventilado, parede da janela livre, acesso ao aquecedor e varal oculto. O modelo da geladeira também será necessário para localizar o início da continuidade da bancada.',34,469,774,9.5)
p('Fontes: P01 (planta oficial, folha única); A01.1 R01 e R02; frames identificados; briefing de Elias. Método de retificação: documentação oficial OpenCV, “Basic concepts of the homography explained with code”.',34,513,774,8,MUTED)
c.linkURL('https://docs.opencv.org/4.10.0/d9/dab/tutorial_homography.html',(34,H-541,808,H-513),relative=0)
c.save()

# Dados de apoio: nenhuma coordenada de fotografia é apresentada como posição real.
data={
 'documento':'A01.2 R00','data':'2026-09-08','escopo':['geometria documental','avaliação de estimativas','mapa de instalações'],
 'unidade':{'andar_informado_por_usuario':8,'torre_na_planta':2,'final_na_planta':'06','observacao':'Resposta do usuário informou apenas o andar; torre/final seguem a identificação da fonte P01.'},
 'fontes':{'P01':'../../01_Documentos_base/Planta baixa oficial.pdf','R01':'../../04_Levantamento/levantamento/A01.1_Levantamento_R01.html','R02':'../../04_Levantamento/levantamento/adicional/A01.1_Extracao_adicional_R02.html'},
 'cotas_oficiais_m':{'AS_paralela_cozinha':1.29,'AS_perpendicular':1.54,'cozinha_trecho_longitudinal':3.52,'cozinha_transversal':1.55},
 'calibracao_pdf':{'unidade_coordenada':'ponto de PDF, origem superior esquerda','escalas_pt_por_m':scales,'escala_mediana':S,'perturbacao_por_extremidade_pt':0.4,'nao_e_precisao_fisica':True,
 'referencias':[{'cota_m':1.29,'eixo':'x','inicio':300.68,'fim':357.56},{'cota_m':3.52,'eixo':'x','inicio':359.12,'fim':513.92},{'cota_m':1.55,'eixo':'y','inicio':305.0,'fim':373.52}]},
 'estimativas_graficas':[{'id':a,'trecho':b,'extensao_pt':delta,'valor_calculado_m':delta/S,'valor_publicado':val,'faixa_sensibilidade':ran,'limite':lim} for a,b,delta,val,ran,lim in estimates],
 'teste_video':{'frame':'COZ-02_02m42s.jpg','imagem_px':[1920,1080],'metodo':'Homografia para quadrado de referência; somente proporção horizontal exploratória. Altura física não definida.',
 'janela_vertices_px':[[318.7,251.3],[608,280],[614.7,554.7],[338,573.3]],'grelha_vertices_px':[[332.7,626.7],[468.7,613.3],[470,681.3],[333.3,693.3]],'razao_largura':0.45502766438451625,'sensibilidade_1000_amostras_uniformes_5px_seed9':[0.41522643230004963,0.4934541726365428],'adotado_como_cota':False},
 'instalacoes':[{'id':a,'face_video':b,'descricao':d,'quantidade_visivel':q,'evidencia':f,'pendencia':pend,'confirmacao':'observado na unidade filmada; correspondência na unidade de Elias pendente','x_m':None,'y_m':None,'z_m':None} for a,b,d,q,f,pend in inventory]
}
(OUT/'A01.2_Dados_e_rastreabilidade_R00.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
md='''# A01.2 - Cozinha e lavanderia: base dimensional e instalações

**R00 | 08/09/2026 | Estudo preliminar | Etapas 1 a 3**

[Abrir as seis pranchas em PDF](A01.2_Base_dimensional_Cozinha_Lavanderia_R00.pdf)

## Resultado

Base consolidada na orientação de P01, avaliação de estimativas gráficas e inventário de 23 registros de instalações/elementos. As nove tomadas em sete placas foram mantidas sem duplicar pontos que reaparecem em fotografias. Não foi iniciada a distribuição final dos módulos nem alterada escolha de material.

Elias informou o 8º andar, dentro do intervalo do 4º ao 16º declarado em P01. Torre 2 e final 06 são a identificação da planta recebida; a resposta desta etapa informou apenas o andar. Elias não tem as medidas dos revestimentos originais mostrados no vídeo.

## 1. Geometria documental

| Cota de P01 | Interpretação |
|---|---|
| 1,29 m | Trecho da área de serviço paralelo à frente da cozinha, da face da parede da janela ao limite desenhado entre setores. |
| 1,54 m | Dimensão perpendicular da área de serviço junto ao limite com a cozinha. Não é uma alternativa de comprimento para a mesma parede. |
| 3,52 m | Trecho da cozinha depois da faixa desenhada entre setores, até a face lateral junto à entrada. |
| 1,55 m | Dimensão transversal indicada no setor da cozinha. Não é largura de circulação livre depois dos móveis. |

P01 tem uma faixa estreita entre os trechos cotados. Sua natureza não foi confirmada. A soma das duas cotas longitudinais é 4,81 m, mas exclui a faixa gráfica intermediária e não define a bancada. O alcance da bancada a partir do fim da geladeira depende do layout e do equipamento escolhido.

A prancha 1 usa um recorte da planta original, preservando paredes, aberturas, símbolos e ressaltos. J/L3 = parede da janela; K1 = parede da pia/equipamentos; L1/L2 = tanque e retorno técnico; E = entrada; F = faixa desenhada entre setores. A correspondência dos detalhes do vídeo é topológica, não uma medição.

## 2. Estimativas gráficas

As estimativas vêm do desenho de P01, e não de medidas reais do imóvel. Foram comparadas três cotas: 1,29 m, 3,52 m e 1,55 m. A escala mediana é 44,093 pontos de PDF por metro; a dispersão entre as escalas é aproximadamente 0,52%. Cada extremidade foi variada em 0,4 ponto para a análise de sensibilidade, também usando a menor e a maior escala. Os intervalos publicados foram arredondados para fora.

**Essas faixas medem sensibilidade de leitura do desenho. Não são tolerâncias de obra, intervalos estatísticos ou garantia de exatidão física. A cota escrita prevalece sobre o traço.**

| ID | Trecho | Estimativa | Sensibilidade gráfica | Limite |
|---|---|---|---|---|
'''
for a,b,delta,val,ran,lim in estimates:md+=f'| {a} | {b} | {val} | {ran} | {lim} |\n'
md+='''
### Memória dos segmentos de P01

Coordenadas em pontos de PDF, com origem no canto superior esquerdo. G-01: y=314,60 a 358,16; G-02: y=331,28 a 366,92; G-03: x=385,40 a 438,20; G-04: y=350,00 a 373,28; G-05: x=334,88 a 385,40; G-06: x=300,68 a 513,92; G-07: y=364,76 a 373,52. G-07 mede o recuo da linha estrutural, não todo o fechamento técnico. Conferir o traço com a prancha original se houver dúvida sobre a interpretação.

### Avaliação do vídeo

COZ-02 é útil para relacionar janela, grelha, tanque, retorno técnico, gás e pia. LAV-07 mostra as interferências inferiores. LAV-08 e AD-0322 mostram o alto. AD-0246 e AD-0302 aproximam os pontos próximos à máquina. As imagens permitem mapear os elementos e comparar proporções, mas não há referência vertical medida nem calibração de lente.

Um teste piloto com os quatro cantos externos da janela em COZ-02 produziu uma razão de largura grelha/janela de 0,455. Com perturbações uniformes de até 5 pixels em todos os vértices, 1.000 amostras (semente 9) variaram de 0,415 a 0,493. Esse resultado não é independente da seleção de bordas; há distorção de lente não modelada e possível diferença entre os planos da esquadria e da grelha. Não foi convertido em centímetros, nem adotado como dimensão de compra ou de ventilação. A altura física da janela não foi determinada pela transformação.

Método de referência: [documentação oficial do OpenCV sobre homografia e retificação de planos](https://docs.opencv.org/4.10.0/d9/dab/tutorial_homography.html). A análise numérica foi realizada com os pontos registrados no arquivo de rastreabilidade.

## 3. Mapa de instalações

Os pontos estão identificados nas fotografias e relacionados às faces na planta. Suas coordenadas reais X/Y/Z não foram inferidas. Os lados direito/esquerdo nas descrições abaixo se referem à unidade filmada. O espelhamento não implica igualdade dos eixos entre unidades.

| ID | Face | Elemento | Quantidade visível | Evidência | Pendência |
|---|---|---|---|---|---|
'''
for row in inventory:md+='| '+' | '.join(map(str,row))+' |\n'
md+='''
Os identificadores originais da R02 foram preservados. T-I01 abrange também o setor social; suas quatro saídas não significam quatro pontos exclusivos da cozinha e lavanderia. Na unidade filmada, o aquecedor ainda não estava instalado. Não foram presumidos circuitos, tensão, bitolas, alimentação de água quente ou função definitiva da abertura circular.

## Pendências remanescentes

| Informação | Por que importa | Como fechar |
|---|---|---|
| Pé-direito e alturas dos rebaixos | Limites dos aéreos e espaço do varal | Levantamento ou corte oficial cotado. |
| Peitoril, altura da janela, ventilação | Relação com bancada e área técnica | Medidas e documentação da esquadria/sistema. |
| Volume técnico completo | Espaço efetivo sob tanque, ao lado da máquina e acima | Croqui cotado e projeto de instalações. |
| Eixos e alturas de cada ponto | Compatibilização com gabinete, cesto e equipamentos | Planta de instalações ou levantamento na unidade. |
| Tipo da faixa F e interface cozinha/serviço | Continuidade da pedra e passagem | Manual, detalhe oficial ou observação na unidade. |
| Modelos dos equipamentos | Vãos, folgas e ponto inicial da bancada após geladeira | Modelos e manuais; necessários na próxima etapa de layout. |

## Correções que orientam a continuidade

- O A04.1 R00 tratava a direção de 1,29/1,54 m como pendência. A leitura documental desta etapa resolve a orientação; continua faltando a medida acabada, não qual direção cada cota representa.
- As conclusões de cabimento do A04.1 R00 baseadas em dimensões típicas de máquina e tanque não são adotadas como prova de viabilidade. A mudança de posição do tanque ou um degrau na pedra não ficam autorizados por essas hipóteses.
- A estimativa anterior de pé-direito de 2,60 m não foi incorporada.
- O apoio de aproximadamente 15 cm é requisito do briefing. Não foi encontrado nem medido em P01 ou no vídeo. A direção e a forma desse apoio deverão aparecer no próximo estudo.
- A R01 permanece a referência documental, complementada pela R02. O frame de 11:06 ainda mostra A; a associação provável é A → Dormitório 02 e B → Dormitório 01.
- Permanecem preservadas as decisões do memorial e do briefing, inclusive a ausência de azul nos móveis do quarto.

## Arquivos e verificação

- PDF: seis pranchas de consulta e revisão.
- Este memorial: resultados, método, referências e pendências.
- `A01.2_Dados_e_rastreabilidade_R00.json`: cotas, segmentos, cálculos e inventário com coordenadas reais em branco.

Fontes: `01_Documentos_base/Planta baixa oficial.pdf`; HTMLs A01.1 R01 e R02 e seus frames; memorial de decisões v2; briefing e resposta de Elias sobre o andar. Os documentos originais foram preservados. Esta R00 complementa o levantamento e não libera fabricação ou intervenção nas instalações.
'''
(OUT/'A01.2_Memorial_e_pendencias_R00.md').write_text(md,encoding='utf-8')
print('PDF:',PDF)
print('Escala:',S,'Registros:',len(inventory))
