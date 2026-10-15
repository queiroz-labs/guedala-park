from pathlib import Path
import json
from html import escape
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image
from pypdf import PdfReader

HERE=Path(__file__).parent
ROOT=HERE.parents[1]
OUT=ROOT/'05_Entregas/pdf/Renders_dos_ambientes_2026-10-12.pdf'
for n,f in [('Reg','arial.ttf'),('Bold','arialbd.ttf')]:
    pdfmetrics.registerFont(TTFont(n,str(Path('C:/Windows/Fonts')/f)))
pdfmetrics.registerFontFamily('Reg',normal='Reg',bold='Bold',italic='Reg',boldItalic='Bold')
records=[
 ('Sala_jantar','Sala e jantar','Mesa 150/180 × 75; três cadeiras na lateral; banco 180 × 55; sofá Bonnie; painel liso e prateleiras Arenza; fotos preservadas.',
  'Nova vista com a fruteira ventilada e as três cadeiras na lateral. Cortina, luminárias e móveis seguem a direção visual aprovada. O tecido, os perfis e as proporções são aproximações; base da mesa, apoios do banco e iluminação ainda dependem de detalhamento.'),
 ('Cozinha','Cozinha','Azul Petróleo nos superiores, Arenza nos inferiores, Branco Itaúnas; IB6S, PE12G junto à geladeira, três gavetas, pia e cocção.',
  'Cozinha e lavanderia contínuas, sem a divisória criada na primeira tentativa. Marcenaria e produtos têm representação aproximada; a perspectiva não comprova folgas. Os 10 cm acima do micro foram preservados como intenção de projeto, com a divergência do manual ainda pendente. Corte forno/cooktop e transição dos aéreos seguem técnicos.'),
 ('Lavanderia','Lavanderia','LG Inox Look, tanque esculpido, cesto sob o tanque, air fryer na bancada, superiores azuis e chapa lisa para o varal.',
  'Tanque, varal elevado e área do aquecedor são estudos de aparência. A chapa lisa substitui o ripado gerado inicialmente. Posição exata, tamanho e mecanismo do varal, ligações, duto, afastamentos do E21 e guarda do banquinho ainda não estão resolvidos por esta imagem. Não usar o render para instalar.'),
 ('Quarto','Quarto principal / L alinhado','Guarda-roupa com 65 cm totais; conjunto em L com bases alinhadas a 213,2 cm e topo contínuo no teto; espelho lateral e cama clara/oliva.',
  'Nova decisão: subir o fundo do aéreo da cabeceira em 8,2 cm, até a cota inferior do maleiro. No cenário com teto 247, arremate 3 e chapas 1,8, ambos ficam com 30,8 cm de corpo e 27,2 cm de altura interna geométrica. Profundidades 65/25 e junta 3 preservadas. Detalhe na página 8; ferragens continuam pendentes.'),
 ('Escritorio','Escritório / uso diário','Bancada com duas telas e notebook, PC à direita; duas gavetas à esquerda com corrediças nominais de 40 cm; sofá-cama cinza e TV oposta.',
  'Armário alto sobre o sofá, área aberta acima dos consoles e ausência do antigo módulo da caixa do PC. Cadeira, artes finais, plantas e tapete são elementos ilustrativos da cena, não novas escolhas ou compras. O sofá e os aparelhos aproximam o programa; a imagem não comprova modelo comercial exato nem o modo hóspedes.'),
 ('Banheiro','Banheiro','Uma parede verde no box; cuba branca, torneira preta atrás dela, gabinete fechado bege, armário espelhado iluminado e chuveiro redondo.',
  'A referência foi corrigida para chuveiro redondo com duchinha e pedra clara de granulação fina. Louças e metais aproximam os modelos escolhidos, sem reprodução técnica exata. Duas frentes do gabinete, detalhes do box e parede clara do banho permanecem hipóteses. A imagem não fecha o percurso hidráulico nem a ocultação de sua descida.')]
c=canvas.Canvas(str(OUT),pagesize=(842,595)); c.setTitle('Guedala Park - seis ambientes em renders de estudo')
def text(x,y,t,size=11,bold=False):
    c.setFillColor(HexColor('#263E40'));c.setFont('Bold' if bold else 'Reg',size);c.drawString(x,y,t)
def para(x,y,w,t,size=10):
    p=Paragraph(t,ParagraphStyle('p',fontName='Reg',fontSize=size,leading=size*1.4,textColor=HexColor('#263E40')))
    _,h=p.wrap(w,500); assert y-h>36,(t,y,h);p.drawOn(c,x,y-h);return y-h
def header(page,title):
    c.setFillColor(HexColor('#FAF8F3'));c.rect(0,0,842,595,fill=1,stroke=0)
    text(30,565,'GUEDALA PARK / 12 OUT 2026',10,True);text(30,527,title,23,True)
    text(30,20,'Renders de estudo por IA. As cotas e escolhas documentadas prevalecem sobre as imagens.',8)
    text(779,20,f'{page} / 8',8)
header(1,'O apartamento / primeira rodada atualizada')
para(30,492,780,'<b>Seis imagens realistas para revisar o conjunto.</b> Sala/jantar, cozinha, lavanderia, quarto, escritório e banheiro. Base: decisões registradas até esta rodada, incluindo o aceite de 65 cm para o guarda-roupa e corrediças de 40 cm no escritório.',12)
y=414
for title,body in [
 ('O que já permite desenhar','Implantação de estudo, paleta, materiais principais, funções e referências visuais estão definidos. As imagens antigas aprovadas orientam o resultado, com correções conforme decisões posteriores.'),
 ('O que ainda pode mudar a aparência','Banheiro: ocultação hidráulica, frentes e detalhes do box. Escritório: cadeira e artes finais. Lavanderia: tamanho/posição da chapa e conjunto técnico. Tons, texturas e modelos comerciais são aproximados nas imagens.'),
 ('O que permanece técnico','Ferragens do maleiro e demais móveis, estrutura, instalações, ventilação dos equipamentos, iluminação calculada e medidas acabadas. Esses pontos não bloqueiam uma rodada visual, mas impedem tratá-la como projeto executivo.'),
 ('Como ler a entrega','Estas imagens foram geradas e editadas por IA a partir das referências e instruções; não são saídas de um modelo 3D com dimensões travadas. Não medem passagens, folgas ou encaixes. Nenhum detalhe incidental da imagem vira uma decisão sua automaticamente.')]:
    text(30,y,title,13,True); y=para(30,y-13,780,body,11)-23
c.showPage()
for page,(key,title,choices,note) in enumerate(records,2):
    header(page,title)
    p=HERE/('Quarto_R02_L_alinhado.png' if key=='Quarto' else key+'_R01.png');iw,ih=Image.open(p).size
    s=min(780/iw,364/ih);w=iw*s;h=ih*s
    c.drawImage(str(p),30+(780-w)/2,132+(364-h)/2,w,h)
    para(30,119,780,'<b>Base:</b> '+choices,9)
    para(30,85,780,'<b>Leitura e pendências:</b> '+note,9)
    c.showPage()
header(8,'Quarto / mesma altura nos dois braços do L')
para(30,491,780,'<b>Decisão de Elias:</b> igualar pela altura maior do maleiro. O aéreo da cabeceira sobe pela base; o maleiro, o topo e os cabideiros mantêm suas cotas.',12)
def z(height):return 201+(height-195)*4.4
def box(x,low,width,high,color):
    c.setFillColor(HexColor(color));c.setStrokeColor(HexColor('#263E40'));c.setLineWidth(.7)
    c.rect(x,z(low),width,(high-low)*4.4,fill=1,stroke=1)
for x,w in [(65,310),(423,336)]:
    box(x,244,w,247,'#B99A72');box(x,213.2,w,244,'#C6A77C')
    box(x,213.2,w,215,'#E8DCC9');box(x,242.2,w,244,'#E8DCC9')
    c.setStrokeColor(HexColor('#263E40'))
    count=2 if x==65 else 4
    for j in range(1,count):c.line(x+w*j/count,z(215),x+w*j/count,z(242.2))
text(115,390,'Maleiro do guarda-roupa',12,True);text(493,390,'Aéreo da cabeceira',12,True)
c.setStrokeColor(HexColor('#3A666D'));c.setLineWidth(1.4);c.setDash(4,3)
c.line(45,z(213.2),786,z(213.2));c.setDash()
text(69,z(213.2)-20,'213,2 / mesma face inferior nos dois corpos',12,True)
text(69,z(247)+10,'Teto 247 / cenário; arremate superior 3',10)
text(81,z(230),'L 200 / P 65',11,True);text(479,z(230),'L 217 / P 25',11,True)
c.setStrokeColor(HexColor('#3A666D'));c.setDash(3,3);c.line(65,z(205),375,z(205));c.setDash()
text(69,z(205)-17,'Varão do guarda-roupa preservado: 205',10)
para(30,186,780,'<b>Altura do corpo:</b> 244 − 213,2 = <b>30,8 cm</b>, nos dois braços. <b>Altura interna geométrica:</b> 244 − 1,8 − 215 = <b>27,2 cm</b>. No aéreo, a referência anterior de 35,4 cm cai 8,2 cm. Ferragens podem reduzir a abertura efetiva.',11)
para(30,118,780,'<b>Geometria preservada:</b> guarda-roupa 65 cm, aéreo 25 cm, junta de 3 cm e passagem nominal de 49 cm no cenário adotado. Altura final depende do teto acabado e do arremate. As frentes serão dimensionadas conforme os respectivos sistemas para preservar a linha visual comum; não são peças de corte idênticas.',10)
c.showPage();c.save()
reader=PdfReader(OUT);assert len(reader.pages)==8
assert all(page.extract_text().strip() for page in reader.pages)
html=['<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Guedala Park | Renders</title><style>body{margin:0;background:#faf8f3;color:#263e40;font:17px/1.55 system-ui}main{max-width:1150px;margin:auto;padding:36px}h1{font-size:38px}article{margin:48px 0}img{display:block;max-width:100%;max-height:850px;margin:auto;border-radius:6px}p{max-width:1000px}small{display:block;color:#526667}nav{display:flex;flex-wrap:wrap;gap:18px}a{color:inherit}</style><main><h1>O apartamento, em seis imagens</h1><p>12/10/2026 · Primeira rodada de renders de estudo. Guarda-roupa de 65 cm adotado; corrediças de 40 cm no escritório.</p><p>Imagens geradas por IA a partir das referências e decisões. As cotas documentadas prevalecem; detalhes incidentais não representam novas escolhas. As pendências técnicas continuam registradas.</p><nav>']
html += [f'<a href="#{k}">{escape(t)}</a>' for k,t,_,_ in records]
html+=['</nav>']
for k,t,choices,note in records:
    filename='Quarto_R02_L_alinhado.png' if k=='Quarto' else k+'_R01.png'
    html.append(f'<article id="{k}"><h2>{escape(t)}</h2><a href="{filename}"><img src="{filename}" alt="Render de estudo: {escape(t)}"></a><p>{escape(choices)}</p><small>{escape(note)}</small></article>')
html.append('</main></html>');(HERE/'Galeria.html').write_text('\n'.join(html),encoding='utf-8')
(HERE/'Verificacao.json').write_text(json.dumps({'pages':8,'images':6,'all_assets_exist':all((HERE/('Quarto_R02_L_alinhado.png' if r[0]=='Quarto' else r[0]+'_R01.png')).exists() for r in records),'pdf_text_checked':True,'common_lower_cm':213.2,'body_height_cm':30.8,'clear_height_cm':27.2},indent=2),encoding='utf-8')
print(OUT)
