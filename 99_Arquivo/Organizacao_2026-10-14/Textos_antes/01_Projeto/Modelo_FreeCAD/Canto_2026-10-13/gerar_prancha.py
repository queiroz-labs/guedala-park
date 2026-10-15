from pathlib import Path
import json
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
OUT=ROOT/'output'/'pdf'/'Canto_quarto_FreeCAD_R03_2026-10-13.pdf'
D=json.loads((HERE/'Resultados_envelopes.json').read_text(encoding='utf-8'))
CAD=json.loads((HERE/'Conferencia_FreeCAD.json').read_text(encoding='utf-8'))
for name,file in [('Reg','arial.ttf'),('Bold','arialbd.ttf')]:
    pdfmetrics.registerFont(TTFont(name,'C:/Windows/Fonts/'+file))
W,H=842,595
PAPER='#FAF8F3';INK='#243D3D';MUTED='#5C706F';BLUE='#226F83';GOLD='#B27B36';RED='#AF493B';LINE='#C2CCC5'
c=canvas.Canvas(str(OUT),pagesize=(W,H));c.setTitle('Guedala Park | Canto do quarto | Conferência FreeCAD R03')
page=0
def rect(x,y,w,h,fill,stroke=None):
    c.setFillColor(HexColor(fill));c.setStrokeColor(HexColor(stroke or fill));c.rect(x,H-y-h,w,h,fill=1,stroke=1)
def txt(s,x,y,size=10,font='Reg',col=INK):
    c.setFillColor(HexColor(col));c.setFont(font,size);c.drawString(x,H-y-size,s)
def para(s,x,y,w,size=10,col=INK):
    p=Paragraph(s,ParagraphStyle('body',fontName='Reg',fontSize=size,leading=size*1.38,textColor=HexColor(col)))
    _,h=p.wrap(w,600)
    assert y+h<550,(page,s,y,h)
    p.drawOn(c,x,H-y-h);return y+h
def start(title,sub):
    global page
    if page:c.showPage()
    page+=1;rect(0,0,W,H,PAPER)
    txt('GUEDALA PARK / QUARTO / FREECAD',30,19,9,'Bold')
    txt('R03 / 13.10.2026',705,19,9,col=MUTED)
    txt(title,30,46,23,'Bold');para(sub,30,83,780,10)
    rect(30,113,782,1,LINE);rect(30,559,782,1,LINE)
    txt('Giro ideal em CAD. Ferragens reais, furação, carga e fabricação ainda não liberadas.',30,570,8,col=MUTED)
    txt(str(page).zfill(2),791,568,11,'Bold')
def photo(name,x,y,w,h):
    c.drawImage(str(HERE/(name+'.png')),x,H-y-h,w,h,preserveAspectRatio=True,anchor='c',mask='auto')
def card(title,body,x,y,w):
    txt(title,x,y,12,'Bold');return para(body,x,y+21,w,10)+17

start('Três conflitos, três providências','A R01 foi reproduzida em sólidos 3D. A revisão compara uma faixa fixa recuada e o limitador da dobradiça principal; são propostas para detalhamento.')
for x,title,name,col in [(30,'R01: porta vizinha cruza o canto','R01_colisao',RED),
                         (295,'Faixa aplicada: bate no início','Faixa_alinhada_bate',RED),
                         (560,'Sem limitador: retorna ao maleiro','Sem_limitador_155',RED)]:
    txt(title,x,134,11,'Bold',col);photo(name,x,156,250,198)
para('<b>Colisão com a vizinha.</b> Principal a 10°, articulação a 0° e vizinha a 11,055°. O FreeCAD encontrou interseção de volume entre as folhas; não é apenas cruzamento de linhas.',30,365,245,10)
para('<b>A faixa também é um obstáculo.</b> Com a faixa aplicada na mesma face, a segunda folha a atinge já a 1° neste modelo. A alternativa recuada fica entre os painéis da caixa.',295,365,245,10)
para('<b>155° não serve como curso livre.</b> Principal a 155° e articulação a 60° fazem a folha B intersectar a frente do maleiro. A variante estudada limita a principal a 92°.',560,365,245,10)
rect(30,476,782,63,'#EFE4D1')
para('<b>Direção proposta:</b> principal 71T7550 com limitador 70T7553.09; articulação 79T8500. Faixa nominal de 150 mm recuada 40 mm, com quatro faixas móveis de 412,5 mm e a primeira dobradiça no lado afastado do canto. Essas novas cotas não são decisões aprovadas nem medidas de corte.',45,488,751,10)

start('A revisão abre no modelo ideal','A folha A aparece em azul, a B em ocre e a primeira porta vizinha em vermelho. O modelo nativo tem controles independentes para os dois ângulos e a vizinha.')
photo('R02_posicao_critica',30,134,375,239)
photo('R02_abertura_maxima',430,134,375,239)
txt('Principal 23,75° / articulação 0° / vizinha 24°',30,378,11,'Bold')
txt('Principal 92° / articulação 60° / vizinha 90°',430,378,11,'Bold')
para('Na pose próxima da condição crítica, o CAD mostrou 54,23 mm entre as peças. A varredura conservadora abaixo usa folhas nominais de 400 mm, maiores que a hipótese de 394 mm do CAD.',30,401,375,10)
para('Abertura máxima ensaiada sem interseção com a vizinha ou as frentes do maleiro. Isso é uma pose conferida; a verificação de todo o domínio vem da análise de envelopes.',430,401,375,10)
txt('Faixa nominal',30,467,10,'Bold');txt('Faixas móveis',196,467,10,'Bold');txt('Separação inferior à vizinha*',340,467,10,'Bold');txt('Contrapartida',586,467,10,'Bold')
for y,filler,moving,gap,trade in [(490,'150 mm','4 × 412,5 mm','48,24 mm','Menos frente fixa'),(513,'200 mm','4 × 400 mm','95,45 mm','Mais frente fixa')]:
    txt(filler,30,y,10);txt(moving,196,y,10);txt(gap,340,y,10);txt(trade,586,y,10)
txt('* 88.929 pares de ângulos; vizinha envolvida por disco contínuo; desconto entre amostras de 2,62 mm.',30,541,8,col=MUTED)

start('As folgas calculadas têm condições','A geometria ideal melhora com a faixa recuada, mas a dobradiça real também desloca as folhas. Nenhuma trajetória multilink completa foi importada nesta revisão.')
y=card('Faixa recuada: 22 mm no modelo ideal',
       'Com 40 mm de recuo e chapa de 18 mm, a análise geométrica dá pelo menos 22 mm de separação da folha B à faixa fixa. O painel recuado fica entre base, tampo e lateral; não cobre essas peças por dentro. Essa margem não absorve automaticamente o movimento real nem os ajustes da ferragem.',30,137,376)
y=card('Maleiro: 43,96 mm no modelo ideal',
       'Varredura da folha B frente ao retângulo que envolve os dois planos das portas de correr, com limite principal de 92°. Desconto entre amostras já aplicado. Trilhos, pegas, desalinhamentos e saliências não podem ultrapassar esse envelope sem nova análise.',30,y,376)
y=card('Por que 20 cm não encerra a conferência',
       'A faixa de 200 mm aumenta a separação à porta vizinha, mas não aumenta a margem ao maleiro nem prova o curso das dobradiças. É uma alternativa de composição, não substituto para o ensaio das ferragens reais.',30,y,376)
txt('Sensibilidade: movimentos não documentados',443,137,12,'Bold')
para('Se o canto se aproximasse 20 mm e a vizinha outros 20 mm, a margem de 48,24 mm cairia a 8,24 mm. Com 30 + 30 mm, ela desapareceria. São hipóteses de teste: <b>esses deslocamentos não foram medidos nem fornecidos como limites pelo fabricante.</b>',443,161,365,10)
txt('Como foi calculado',443,280,12,'Bold')
para('Folhas conservadoras de 400 × 18 mm; principal 0-92° e articulação 0-60°, passo de 0,25°. Disco de raio equivalente à diagonal da porta vizinha contém seu giro inteiro. O valor inferior desconta o máximo deslocamento até a amostra mais próxima. Furações e braços da ferragem não entram nesses sólidos.',443,303,365,10)
rect(443,430,365,86,'#F0E2D8')
para('<b>Conclusão técnica:</b> a R01 não deve continuar como solução sem colisão. A faixa de 15 cm recuada 4 cm é candidata no modelo ideal; a confirmação executiva requer ferragens reais, ajustes extremos, pegas e todas as aberturas simultâneas.',456,443,340,10)

start('Ferragens e montagem: o que fecha e o que falta','Códigos consultados no catálogo oficial Blum e nas instruções atuais. A seleção do calço, recobrimento e furação precisa corresponder à montagem final do canto.')
rows=[
    ('Principal na caixa','71T7550 / CLIP top / 155°','Usar o limitador de 92°. A versão T tem mola; não atribuir amortecimento integrado.'),
    ('Limitador','70T7553.09 / 92°','O 70T7553 de 110° é outra peça e deixa um curso maior, inadequado à triagem.'),
    ('Entre as folhas','79T8500 / 60°','Para frentes de 15-23 mm. O caneco da articulação fica na mesma folha A que recebe o da principal.'),
    ('Calços e furação','Ainda sem código fechado','Confirmar aplicação, recobrimento e B. O catálogo mostra exemplos com calços 0/3 mm; não escolher por analogia.'),
    ('Quantidade / fixação','Dois níveis por conjunto: hipótese','Gabaritos visuais a 51/255 mm do corpo do canto. Quantidade, furação e capacidade do conjunto baixo com duas folhas a confirmar.')]
y=137
for heading,part,body in rows:
    txt(heading,30,y,11,'Bold');txt(part,208,y,11,'Bold',BLUE)
    h=para(body,208,y+19,598,10);y=h+18
rect(30,430,782,89,'#EFE4D1')
para('<b>Não cortar 400 mm automaticamente.</b> O catálogo apresenta DW = IW + W - T - R - G, com o batente/amortecedor também considerado no passo de cálculo. As faixas nominais de 400 mm e as peças de 394 mm com junta de 3 mm nesta revisão são hipóteses geométricas. Só fechar o corte após a montagem do calço, recobrimento, junta e eixo reais.',44,443,754,10)
txt('Preservados: roupeiro 650 mm; aéreo 250 mm; base superior 2132 mm; topo de estudo 2440 mm; programa R02.',30,535,8,col=MUTED)

start('Conferência final e arquivo editável','O apartamento original R01 foi preservado. A revisão R02 do arquivo FreeCAD abre com o canto isolado e os controles de estudo disponíveis na árvore.')
y=card('No FreeCAD',
       'Abra Guedala_Park_R02_Canto.FCStd. Na planilha <b>Canto - ângulos e variantes</b>, altere Alpha, Beta e Vizinha. Faixa = 150/200 mm compara as propostas; Faixa = 0 reproduz a R01. Recuo = 0 mostra a faixa aplicada; Recuo = 40 mm mostra a candidata recuada. As propriedades não impõem limites mecânicos.',30,137,376)
y=card('Antes de liberar o conjunto',
       'Obter a aplicação CAD correta ou montar gabarito com 71T7550, 79T8500, calços e limitador. Conferir as folhas entre si, caixa, faixa recuada, portas vizinhas e os dois planos de correr. Incluir ajustes, carga, pegas, apoios e tolerâncias. Um STEP estático isolado não fornece, por si, toda a cinemática.',30,y,376)
y=card('Critério de encerramento',
       'Todo o curso deve manter separação positiva nas combinações de uso e ajustes definidos; o conjunto deve atender à carga e fixação do fornecedor. Fechar dimensões de corte e quantidade de ferragens somente depois dessa prova. Nenhuma cota nova está registrada como aprovação do usuário.',30,y,376)
txt('Fontes oficiais consultadas',443,137,12,'Bold')
sources=[('Catálogo Blum 2025, páginas 31, 32 e 47','https://d2.blum.com/services/BEC003/concealedhinges_ep_dok_bus_%24sen-us_%24aof_%24v18.pdf'),
         ('Planejamento do canto, página 117','https://publications.blum.com/2024/catalogue/en/117/'),
         ('Principal e limitadores, página 84','https://publications.blum.com/2024/catalogue/en/84/'),
         ('Blum ID20027, ficha atual da articulação','https://www.blum.com/file/iak0027-id20027_at_dok_bau?country=ca&language=en'),
         ('Instrução oficial do limitador 155°','https://www.blum.com/file/clp0004-ma-481-0_ma_dok_bau?country=ca&language=en'),
         ('Blum Product Configurator: dados CAD','https://www.blum.com/us/en/services/e-services/onlineproductconfigurator/')]
y=162
for label,url in sources:
    txt(label,443,y,10,col=BLUE)
    c.linkURL(url,(443,H-y-15,805,H-y+3),relative=0)
    y+=30
para('O catálogo mostra uma dimensão de planejamento de 32 mm na principal a 90°. Essa dimensão não é um limite para a translação durante o curso: não foi usada para certificar folgas. O acesso completo aos dados CAD é associado ao E-SERVICES; nenhum arquivo cinemático completo foi obtido nesta rodada.',443,375,365,10)
para('<b>Arquivos de evidência:</b> Resultados_envelopes.json, Conferencia_FreeCAD.json, scripts reproduzíveis e oito imagens de poses. Gabaritos de canecos no modelo são referências visuais ocultas, não ferragens CAD reais nem autorização de furação.',443,479,365,9)
c.save()
print(str(OUT))
