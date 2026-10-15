from pathlib import Path
import sys, re, json
from html import escape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image as PILImage
from pypdf import PdfReader

sys.stdout.reconfigure(encoding='utf-8')
root=Path.cwd()
base=root/'01_Projeto/Pesquisa_comparativa_Cury'
assets=base/'fontes'
out=root/'output/pdf/Pesquisa_Cury_40m2.pdf'
out.parent.mkdir(parents=True,exist_ok=True)
pdfmetrics.registerFont(TTFont('Arial','C:/Windows/Fonts/arial.ttf'))
pdfmetrics.registerFont(TTFont('ArialB','C:/Windows/Fonts/arialbd.ttf'))
pdfmetrics.registerFontFamily('Arial',normal='Arial',bold='ArialB')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='BodyPT',fontName='Arial',fontSize=10.5,leading=14.6,spaceAfter=9,textColor=colors.HexColor('#263846')))
styles.add(ParagraphStyle(name='TitlePT',fontName='ArialB',fontSize=22,leading=26,spaceAfter=16,textColor=colors.HexColor('#153e50')))
styles.add(ParagraphStyle(name='SubPT',fontName='ArialB',fontSize=12,leading=16,spaceAfter=8,spaceBefore=9,textColor=colors.HexColor('#153e50')))
styles.add(ParagraphStyle(name='SmallPT',fontName='Arial',fontSize=8,leading=10.5,spaceAfter=6,textColor=colors.HexColor('#52636f')))
styles.add(ParagraphStyle(name='CellPT',fontName='Arial',fontSize=9,leading=12,textColor=colors.HexColor('#263846')))
story=[]
md=['# Pesquisa comparativa Cury: apartamento de canto de 40,18 m²\n','Pesquisa em 12/09/2026. Referência: Guedala Park III / Premium, Torre 02, final 06, 8º andar, conforme o projeto existente.\n']
def p(text,style='BodyPT'):
    story.append(Paragraph(text,styles[style]))
    plain=re.sub('<[^>]+>','',text)
    md.append(plain+'\n')
def title(text):
    if story: story.append(PageBreak())
    story.append(Paragraph(text,styles['TitlePT']))
    md.append('\n## '+text+'\n')
def table(rows,widths):
    data=[[Paragraph(escape(str(x)),styles['CellPT']) for x in row] for row in rows]
    t=Table(data,colWidths=widths,hAlign='LEFT',repeatRows=1)
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e6eff2')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('LINEBELOW',(0,0),(-1,0),.6,colors.HexColor('#87a4af')),('LINEBELOW',(0,1),(-1,-1),.35,colors.HexColor('#d4e0e4'))]))
    story.extend([t,Spacer(1,12)])
    md.append('| '+' | '.join(rows[0])+' |\n| '+' | '.join(['---']*len(rows[0]))+' |\n'+'\n'.join('| '+' | '.join(row)+' |' for row in rows[1:])+'\n')
def img(name,maxh=330):
    path=assets/name
    with PILImage.open(path) as im: w,h=im.size
    scale=min(499/w,maxh/h)
    story.extend([Image(str(path),width=w*scale,height=h*scale),Spacer(1,8)])
    md.append(f'![Planta de referência](fontes/{name})\n')
def source(text): p(text,'SmallPT')

title('O que a pesquisa esclareceu')
p('<b>A melhor referência encontrada é uma planta adicional da própria Cury para o Guedala Park Premium.</b> Ela reúne a configuração do seu apartamento e identifica outros finais onde procurar fotos e vídeos equivalentes. Há também uma família de plantas de ponta em Vila das Belezas / João Dias muito próxima da sua.')
p('Não localizei outro empreendimento da Cury com <b>exatamente 40,18 m²</b> e equivalência de planta comprovada. Localizei áreas próximas e desenhos úteis, mas nenhuma dessas fontes substitui a documentação da sua unidade.')
table([['Referência','Área publicada','Utilidade para você'],['Guedala Park III / Premium','40,18 m²','Mesma tipologia; fonte prioritária.'],['Dez Canindé','40,20 m² (+0,02)','Área quase igual; não foi possível vincular os 40,20 a uma imagem específica da galeria.'],['Cidade Mooca - Vila Sardenha','40,13 m² (-0,05)','Área próxima; comercialização com terraço e desenhos diferentes.'],['Cury João Dias / Vila das Belezas','40,68 m² (+0,50)','Desenho de ponta muito semelhante; nomes e fases exigem cuidado.']],[145,112,242])
p('Para prever <b>distribuição e proporções</b>, a semelhança geométrica ajuda mais do que uma diferença mínima na área total. Para prever <b>acabamentos, instalações e altura</b>, é necessário o documento do seu empreendimento e do seu final.')
p('Critério usado: planta da unidade fornecida no projeto; imagens oficiais da Cury; livros comerciais; acervos de corretores; memorial técnico de outro empreendimento; pesquisa acadêmica. Os resultados abaixo distinguem comprovação direta, comparação e informação ainda ausente.')
source('Referências [1]-[8], detalhadas no índice de fontes. Data de consulta: 12/09/2026. Este relatório não altera as medidas nem as decisões já registradas no projeto.')

title('1. Outros apartamentos do seu tipo')
img('cury_guedala_sul_2.jpg',310)
source('Imagem original da Cury: Guedala Park Premium, Condomínio 03 [1]. Cotas e mobiliário apresentados em planta comercial.')
table([['Condomínio 03','Finais / colunas','Pavimentos da imagem'],['Torres 01 e 02','02, 06 e 07','3º ao 16º'],['Torres 01 e 02','01','4º ao 16º'],['Torre 03','01 e 02','3º ao 20º'],['Torre 03','06 e 07','2º ao 20º']],[135,125,239])
p('Esse mapa permite direcionar a busca por registros de moradores para <b>finais 01, 02, 06 e 07 do Condomínio 03</b>, observando torre e andar. Algumas unidades são espelhadas; fachadas e orientação solar variam.')
p('Sua planta contratual identifica Torre 02, final 06, do <b>4º ao 16º</b>; a imagem comercial inclui o 3º nessa coluna. O seu 8º andar está nas duas faixas. A informação comercial não amplia a validade do documento da unidade.')

title('2. O que já sabemos do seu interior')
p('As cotas abaixo vêm da <b>planta oficial já presente no seu projeto</b> [U1]. A planta encontrada na internet repete as principais proporções. São medidas de projeto, ainda sem conferência presencial no apartamento acabado.')
table([['Ambiente / trecho','Cota da sua planta','Leitura prática'],['Dormitório 01','2,45 × 2,95 m','Retângulo principal do quarto; o recuo de acesso tem geometria própria.'],['Dormitório 02 / escritório','2,30 × 2,95 m','Base mais confiável para estudar bancada, armário e cama de hóspedes.'],['Banheiro','2,09 × 1,24 m','Janela lateral junto ao box; atenção ao enchimento técnico.'],['Cozinha','3,52 × 1,55 m','Cota longitudinal do setor; não significa 3,52 m livres para armários.'],['Lavanderia','1,29 × 1,54 m','1,29 paralelo à bancada; 1,54 no sentido transversal. Janela lateral própria.'],['Sala','2,45 m de largura','A cota maior de 5,15 m atravessa o conjunto sala/cozinha.'],['Circulação','0,90 m e 1,05 m','Cotas em eixos distintos; não representam um único corredor de largura constante.']],[134,111,254])
p('<b>O que muda no planejamento:</b> a largura da sala não é a largura da janela; a cota da cozinha não é o comprimento útil de bancada; os retângulos dos quartos não incluem automaticamente folgas de portas, armários e rodapés.')
p('Como exercício de proporção, uma cama de 1,58 m em uma largura de 2,45 m deixaria <b>0,87 m no total</b> para os dois lados, antes de qualquer interferência. Isso não aprova uma disposição: apenas mostra por que alguns centímetros fazem diferença.')
p('A planta também distingue paredes estruturais, trechos de gesso e enchimentos técnicos. Não permite concluir que um volume possa ser removido ou que uma instalação possa mudar de posição.')
source('[U1] 02_Plantas_e_manuais/Planta_oficial.pdf. A interpretação dimensional complementa os estudos existentes em 01_Projeto/Medidas; não libera fabricação.')

title('3. A comparação mais parecida')
img('dez_joao_jm_2.jpg',355)
source('Planta de ponta publicada no acervo “Cury Dez João Dias” da JM Marques [4]. Esta imagem não escreve a área total.')
p('O desenho mantém sala ao lado dos quartos, cozinha transversal na entrada, banheiro central e lavanderia na extremidade. Ao girá-lo 180°, a organização fica muito próxima da sua. As colunas destacadas são 01, 02, 06 e 07.')
table([['Cota','Seu Guedala','Planta comparada'],['Quarto 01, retângulo principal','2,45 × 2,95 m','2,40 × 2,95 m'],['Quarto 02','2,30 × 2,95 m','2,30 × 2,90 m'],['Banheiro','2,09 × 1,24 m','2,15 × 1,20 m']],[220,139,140])
p('Um anúncio “Cury João Dias” apresenta desenho semelhante como <b>40,68 m²</b> [3]; outro o chama “Vila das Belezas” [5]. O acervo [4] ainda contém fachada com nome de outra fase. Por isso, não trato todos os nomes como um único empreendimento nem atribuo automaticamente 40,68 m² à imagem cotada acima.')

title('4. Detalhes encontrados nessa família')
img('vila_belezas_ponta.jpg',315)
source('Material de divulgação “Cury Vila das Belezas”, identificado como planta de ponta [5].')
p('A imagem destaca ventilação natural, área de serviço independente, previsão de chuveiro a gás, piso laminado nos quartos, cerâmica até o teto na parede hidráulica e tomada USB no quarto de casal.')
p('<b>O que pode ser aproveitado:</b> a relação entre cozinha, tanque, janela, banho e quartos ajuda a reconhecer vídeos de uma configuração semelhante. A indicação de área de serviço independente descreve uma posição setorizada; não basta para concluir que exista porta separando a cozinha.')
p('<b>O que não pode ser transferido:</b> chuveiro a gás, tomada USB, extensão dos revestimentos e materiais são promessas desse material comercial, não confirmações de entrega no Guedala. Mesmo em desenhos semelhantes, essas especificações podem mudar.')
p('A semelhança observada é de organização e medidas aproximadas. Ela não demonstra igualdade de shafts, tubulações, espessuras de parede, esquadrias ou altura do teto.')
source('A publicação [3] registra 40,68 m² em uma planta visualmente semelhante. A identificação da fase permanece uma limitação; as imagens foram preservadas com seus nomes de origem.')

title('5. Áreas quase iguais, plantas diferentes')
p('<b>Vila Sardenha: 40,13 m².</b> Anúncios associam essa metragem a dois dormitórios e terraço [6, 6b]. A galeria oficial contém vários tipos [7]; a imagem abaixo é um exemplo, sem área total impressa, e não uma identificação definitiva da unidade de 40,13 m².')
img('cury_sardenha_3.jpg',205)
source('Exemplo da galeria oficial de Vila Sardenha [7]. Não usar suas cotas como medidas do Guedala.')
p('<b>Dez Canindé: 40,20 m².</b> O acervo comercial informa essa área entre outras opções [8]. A Cury publica plantas com e sem terraço [9]. Não encontrei vínculo inequívoco entre a área de 40,20 m² e uma imagem específica.')
img('cury_caninde_2.webp',205)
source('Exemplo oficial do Canindé: planta com terraço, finais 05 e 07 das torres 01 e 03 [9]. A imagem não informa 40,20 m².')
p('Essas referências demonstram o limite da busca por área: diferenças de terraço, circulação e formato dos quartos podem alterar bastante o uso de um apartamento de aproximadamente 40 m².')

title('6. Entrega, teto e instalações')
p('<b>Pé-direito: continua sem confirmação documental para sua unidade.</b> Não localizei corte do Guedala ou tabela de alturas por ambiente. As hipóteses anteriores de 2,57 m e de 2,47 m após um rebaixo de 10 cm continuam sendo cenários de estudo; esta pesquisa não as validou.')
p('<b>Ar-condicionado:</b> o book do Guedala informa ausência de previsão de carga elétrica para instalação nos apartamentos [2]. Isso é uma limitação concreta para planejamento, mas o texto não demonstra, sozinho, qual intervenção futura seria autorizada. É necessário verificar memorial, projeto elétrico e regras aplicáveis à sua unidade.')
p('<b>Acabamentos:</b> o arquivo local “Memorial_do_apartamento_v2.pdf” registra decisões do seu projeto de interiores. Ele não é o memorial descritivo de entrega emitido pela Cury.')
p('Um memorial real: My Miguel Yunes','SubPT')
p('Encontrei um memorial Cury de 25/02/2022 [10]. Ele diferencia pisos por ambiente e prevê forro de gesso no banheiro. Mais decisivo: especifica água quente a gás apenas para determinados finais; os demais recebem previsão de chuveiro elétrico. Também registra limitações próprias para ar-condicionado e coifa.')
p('Esse documento é útil para demonstrar quais informações devem ser procuradas. Ele <b>não define a entrega do Guedala</b>: até dentro de um empreendimento a infraestrutura pode variar conforme o final.')
p('O que ainda falta comprovar','SubPT')
p('Altura livre em cada ambiente; rebaixos e sancas; dimensões e peitoris das janelas; posição exata de tomadas e tubulações; circuitos disponíveis; condições de água quente; material e extensão dos revestimentos; dimensões acabadas dos enchimentos técnicos.')
source('[2] Book Guedala Park III, abril/2023. [10] Memorial My Miguel Yunes, R01, pp. 10-11 e 15-17. O documento de outro empreendimento é somente comparativo. Não foi encontrado um novo documento que resolva o pé-direito do Guedala.')

title('7. Como obter as respostas que faltam')
p('A próxima fonte decisiva é a documentação da <b>Torre 02, final 06, 8º andar</b>. Fotos de finais equivalentes ajudam a antecipar aparência e volumes; dimensões e condições de instalação precisam corresponder à sua unidade.')
table([['Documento a solicitar','Dúvida que resolve'],['Memorial descritivo contratual e eventuais revisões','Pisos, paredes, louças, metais, forros e equipamentos previstos na entrega.'],['Planta de arquitetura cotada, cortes e detalhe de forros','Pé-direito, vigas, sancas, rebaixos, enchimentos e dimensões finais.'],['Quadro / detalhes de esquadrias','Largura e altura das janelas, peitoris e tipo de abertura.'],['Plantas elétrica, hidráulica, gás e esgoto da unidade','Pontos, circuitos, cargas, água quente e trajetos previstos.'],['Manual do proprietário e as built, quando disponíveis','Sistemas efetivamente executados e orientações de uso e intervenção.']],[216,283])
p('Texto preparado para a Cury','SubPT')
p('Sou proprietário de uma unidade do Guedala Park III / Premium, Torre 02, final 06, 8º andar, com 40,18 m² e planta de canto. Solicito o memorial descritivo de entrega correspondente à minha unidade, a planta cotada de arquitetura, cortes ou informação formal de pé-direito por ambiente, planta de forros e detalhes de esquadrias. Solicito também as plantas de instalações disponíveis para o meu final. Preciso confirmar rebaixos, janelas e peitoris, pontos de água e esgoto, água quente, circuitos e previsão de carga para ar-condicionado, além dos revestimentos que serão entregues. Se os documentos finais ainda não estiverem disponíveis, peço a revisão vigente e a indicação do que ainda poderá mudar.')
source('Mensagem preparada, não enviada. Documentos de execução ou as built podem depender da fase da obra. O pedido não pressupõe que todos já estejam disponíveis.')
p('Para novas imagens, priorize buscas com “Guedala Park III final 06”, “Guedala Premium torre 2 canto” e os finais equivalentes do Condomínio 03 listados neste relatório. O site oficial também apresenta um vídeo como tour [11], mas sua correspondência com o final 06 não foi verificada.')

title('Fontes e rastreabilidade')
sources=[
('1','Cury - Guedala Park Premium; imagem oficial da tipologia do Condomínio 03','https://cury.net/storage/images/products/plants/642c90a978dd7.jpeg'),
('2','Book Guedala Park III, abril/2023; tipologias na p. 22 e observações finais','https://www.guerato.com.br/_files/ugd/1d445c_9f2918bdea3e4ea1a33d4b71ed346bc9.pdf'),
('3','Imóvel App - Cury João Dias; planta divulgada como 40,68 m²','https://www.imovelapp.com.br/imovel/cury-joao-dias/'),
('4','JM Marques - acervo “Cury Dez João Dias”; identificação de fase inconsistente','https://www.jmmarques.com.br/pagina/empreendimento/cury-dez-joao-dias=1373'),
('5','Terrara Interlagos - Cury Vila das Belezas; imagens “ponta” e “meio”','https://terrarainterlagos.com.br/cury-vila-das-belezas/'),
('6','JM Marques - Vila Sardenha; faixa publicada de 34,51 a 40,13 m²','https://www.jmmarques.com.br/pagina/empreendimento/cury-cidade-mooca-vila-sardenha=1823'),
('6b','Na Varanda com Prisma - Cidade Mooca, parte 1; associação 40,13 m² e terraço','https://navarandacomprisma.com.br/cidade-mooca-parte-1-cury/'),
('7','Cury - Cidade Mooca Vila Sardenha; galeria oficial de plantas','https://cury.net/imovel/SP/zona-leste/cidade-mooca-vila-sardenha'),
('8','JM Marques - Dez Cury Canindé; áreas publicadas, incluindo 40,20 m²','https://www.jmmarques.com.br/pagina/empreendimento/dez-cury-caninde=1497'),
('9','Cury - Dez Canindé; galeria oficial de plantas','https://cury.net/imovel/SP/zona-norte/dez-caninde'),
('10','Cury - My Miguel Yunes, memorial de vendas R01, 25/02/2022','https://static.orulo.com.br/files/properties/original/538704.pdf'),
('11','Vídeo apresentado como tour na página oficial do Guedala; não analisado','https://www.youtube.com/watch?v=Bl2ayPHnf28'),
('12','Toyoda, Thayna R. L. - Procedimentos adotados pelas incorporadoras para definição das plantas de moradias de dois dormitórios em São Paulo e a explosão dos HIS. USP, 2024; repositório 2025, p. 168','https://www.teses.usp.br/teses/disponiveis/16/16132/tde-02072025-113738/publico/METhaynaRigoldiLeandroToyoda_Rev.pdf'),
]
for n,label,url in sources:
    p(f'[{n}] <a href="{escape(url,quote=True)}" color="#17617c">{escape(label)}</a>','SmallPT')
    md[-1]=f'- [{n}] [{label}]({url})\n'
p('A página oficial do Guedala usada na pesquisa está em cury.net/imovel/SP/zona-sul/guedala-park-premium. [U1] é a planta local fornecida no projeto. As principais imagens e PDFs foram preservados na pasta fontes. Referências de terceiros foram usadas para localizar áreas e desenhos, sem validar anúncios de preço, prazo ou financiamento.','SmallPT')
p('A dissertação [12] foi consultada como contexto sobre famílias de plantas de Cury, incluindo Urban Tatuapé e Sardenha; não comprova equivalência com o Guedala. Também foram rastreados catálogos e anúncios com 40,18 / 40,13 / 40,20 / 40,68 m². Ausência de confirmação nesta pesquisa não demonstra inexistência de outro produto com 40,18 m².','SmallPT')

def footer(c,doc):
    c.setStrokeColor(colors.HexColor('#c7d8de'));c.line(48,43,547,43)
    c.setFont('Arial',8);c.setFillColor(colors.HexColor('#52636f'))
    c.drawString(48,29,'GUEDALA PARK | Pesquisa comparativa | 12/09/2026')
    c.drawRightString(547,29,str(doc.page))

SimpleDocTemplate(str(out),pagesize=(595.28,841.89),rightMargin=48,leftMargin=48,topMargin=44,bottomMargin=57,title='Guedala Park - Pesquisa de plantas Cury de aproximadamente 40 m²',author='Pesquisa para Projeto Guedala Park').build(story,onFirstPage=footer,onLaterPages=footer)
(base/'Pesquisa_Cury_40m2.md').write_text('\n'.join(md),encoding='utf-8')
manifest={}
for path in (root/'tmp/pesquisa_cury/downloads.json',root/'tmp/pesquisa_cury/downloads2.json'):
    if path.exists(): manifest.update(json.loads(path.read_text(encoding='utf-8-sig')))
manifest.update({'vila_belezas_ponta.jpg':'https://terrarainterlagos.com.br/wp-content/uploads/2019/06/Planta-da-Ponta.jpg','vila_belezas_meio.jpg':'https://terrarainterlagos.com.br/wp-content/uploads/2019/06/Planta-do-Meio.jpg'})
(base/'fontes/Indice_de_imagens.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
r=PdfReader(str(out));print('PDF',out,'Páginas:',len(r.pages))
for i,page in enumerate(r.pages,1):print(i,len(page.extract_text() or ''),(page.extract_text() or '')[:65].replace('\n',' '))
