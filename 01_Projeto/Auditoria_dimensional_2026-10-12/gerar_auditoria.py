from pathlib import Path
import json
from xml.sax.saxutils import escape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.shapes import Drawing, Rect, Line, String
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).parent
OUT=ROOT/'05_Entregas/pdf/Auditoria_dimensional_marcenaria_2026-10-12.pdf'
for n,f in [('Reg','arial.ttf'),('Bold','arialbd.ttf')]: pdfmetrics.registerFont(TTFont(n,str(Path('C:/Windows/Fonts')/f)))
INK='#263E40'; MUTED='#617171'; WOOD='#C6A77C'; BLUE='#3A666D'
styles={k:ParagraphStyle(k,fontName='Bold' if k in ['title','h','th'] else 'Reg',fontSize=s,leading=l,textColor=HexColor(INK),spaceAfter=8) for k,s,l in [('title',23,28),('h',12,16),('p',10,14),('cell',9,12),('th',9,12),('small',8,11)]}
story=[]; inventory=[]
def p(t,style='p'): return Paragraph(t,styles[style])
def section(title,sub):
 if story:story.append(PageBreak())
 story.extend([p(title,'title'),p(sub),Spacer(1,8)])
def prose(t):story.append(p(t))
def rows(items):
 inventory.extend(items)
 data=[[p(x,'th') for x in ['Peça / situação','Dimensão de estudo (cm)','Leitura','Conferência e encaminhamento']]]
 for item in items:data.append([p(escape(str(x)),'cell') for x in item])
 t=Table(data,colWidths=[143,167,123,337],hAlign='LEFT',repeatRows=1)
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor('#E3EAE5')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('LINEBELOW',(0,0),(-1,0),.8,HexColor(INK)),('LINEBELOW',(0,1),(-1,-1),.4,HexColor('#CCD2CA'))]))
 story.extend([t,Spacer(1,10)])
sources=[
 ('S1','Madesa Nice G246013BNC','Móvel de 60 L × 52 P × 68 A; três gavetas. Referência brasileira de escala externa, não da caixa interna.','https://www.madesa.com/products/balcao-60-cm-3-gavetas-suspenso-cinza-nice-madesa'),
 ('S2','IKEA METOD/MAXIMERA 392.797.32','Módulo 80 L; estrutura 60 P × 80 A; frentes 20/20/40. Referência europeia de proporção, sem oferta no Brasil presumida.','https://www.ikea.com/pt/pt/p/metod-maximera-armario-baixo-c-3gavetas-branco-veddinge-branco-s39279732/'),
 ('S3','Blum Brasil - MOVENTO','Programa publicado: classe 40 kg, comprimentos 250–600 mm; outras classes no programa. Comprimento, curso, caixa e carga são variáveis distintas.','https://www.blum.com/br/pt/products/runnersystems/movento/programme/'),
 ('S4','Blum - construção da gaveta MOVENTO','Nesta família, comprimento da lateral = nominal menos 10 mm; largura útil = vão interno do gabinete menos 42 mm. Não aplicar às telescópicas laterais.','https://ea.blum.com/en/building-a-movento-drawer/'),
 ('S5','Blum - catálogo, p. 718 e p. 422','Dobradiças: quantidade depende de altura e peso, gráfico referido a frente de 600 mm. MOVENTO: espaço em profundidade nominal + 3 mm na configuração indicada.','https://publications.blum.com/2024/catalogue/pt/718/'),
 ('S6','Madesa Lux G253509NLX','Aéreo de uma porta: 35 L × 31 P × 66 A. Comparação de escala; não é equivalente exato à porta C do projeto.','https://www.madesa.com/products/armario-aereo-madesa-lux-35-cm-1-porta-rustic'),
 ('S7','IKEA METOD 102.055.34','Estrutura de parede 40 L × 37 P × 60 A, próxima ao módulo de estudo do escritório 40 × 35 × 55.','https://www.ikea.com/pt/pt/p/metod-armario-parede-branco-10205534/'),
 ('S8','Hettich - guia de seleção T&I','TopLine L: portas 550–1500 mm de largura, até 2600 mm de altura e 50 kg no guia consultado. Exemplo de escala viável, não sistema selecionado.','https://catalog.hettich.com/General/TuI_Produkt_Auswahlhilfe/en_DE/catalogs/TuI_Produkt_Auswahlhilfe_en_DE/pdf/complete.pdf'),
 ('S9','IKEA PAX / MEHAMN/AULI 295.613.64','Roupeiro com portas de correr 200 L × 66 P × 236 A. Mostra que profundidade total e profundidade de caixa não se confundem.','https://www.ikea.com/pt/pt/p/pax-mehamn-auli-combinacao-de-roupeiro-cinz-esc-dupla-face-cinz-esc-vidro-espelhado-s29561364/'),
 ('S10','IKEA ENHET 506.230.44','Armário com portas espelhadas 60 L × 17 P × 75 A. O nosso estudo de 12–15 P é mais raso; altura ainda não definida.','https://www.ikea.com/es/en/p/enhet-mirror-cabinet-with-doors-white-50623044/')]

section('As medidas têm escala realista?', 'Guedala Park | Auditoria dimensional de marcenaria | 12/10/2026')
prose('<b>Em grande parte, sim. As gavetas principais da cozinha não estão fora da escala de mercado.</b> Há móveis e ferragens reais com dimensões semelhantes. Ainda não é possível afirmar que toda a marcenaria está bem dimensionada: algumas caixas não têm corte completo, e os elementos especiais dependem de estrutura, carga e ferragens.')
rows([
 ('Manter como base','Cozinha: módulo 61,9; caixas alvo 50 P; frentes 16/16/40','Escala coerente','S1/S2/S3 sustentam largura, profundidade nominal e frente alta. Conferir úteis e peso sem mudar automaticamente as proporções.'),
 ('Ajuste identificado','Escritório: módulo 45 P versus curso ensaiado 45','Rever detalhamento','A corrediça de 450 mm não cabe na construção estudada depois de frente e fundo. Desenvolver referência de 400 mm e recalcular a caixa.'),
 ('Maiores atenções','Base comprida; guarda-roupa 60 P; prateleiras longas','Condições abertas','A gaveta de piso exige estrutura independente; cabides dependem de profundidade líquida; prateleiras e tampo precisam de apoios/carga definidos.'),
 ('Sem desenho completo','Banheiro, portas principais do roupeiro e detalhes de caixas','Não certificável','Dimensões gerais podem ser sensatas e ainda faltar dado para verificar a peça. Ausência de cota não conta como aprovação.')])
prose('<b>Leitura das medidas:</b> L = largura; P = profundidade; A = altura. Frente é a peça visível; caixa é o recipiente; útil é o espaço que sobra dentro. Comprimento nominal da corrediça não é necessariamente a profundidade da caixa ou seu curso. Todas as cotas são de estudo, anteriores ao levantamento acabado.')
prose('A ferragem do maleiro permanece pendente por decisão de Elias. Esta auditoria não a reabre e não altera layout, programa ou escolhas funcionais. Referências comerciais demonstram existência e escala; não são seleção de compra nem comprovação de estoque.')

section('01 / Gavetas: largura, profundidade e altura','A dimensão externa do módulo não deve ser usada como medida interna da gaveta.')
rows([
 ('G1 / talheres','Módulo 61,9 L; frente 16 A; caixa alvo 50 P','Manter escala','Útil horizontal de teste 52,7 × 47. Não é gaveta excessivamente larga ou funda diante de S1/S3. Altura livre ainda depende do corte da ferragem.'),
 ('G2 / utensílios','Mesmo módulo e frente 16 A','Conferir altura útil','A organização vigente exige H livre ≥ 11,1, já considerando o critério do estudo de conteúdo. Isso permite perdas totais de até 4,9 dentro da faixa de 16; não são 16 cm úteis.'),
 ('G3 / mantimentos','Frente 40 A; útil de teste 52,7 L × 47 P','Frente alta realista','Há frente de 40 em produto real S2. Altura da lateral da caixa pode ser menor. Somar peso da caixa, bebidas, secos e organizadores; carga nominal não se refere só ao conteúdo.'),
 ('Quarto / quatro gavetas','Vão 35,5 L; frente ~15 A; curso de ensaio 30','Estreitas, viáveis','Com desconto lateral hipotético 2,6 e laterais da caixa de 1,5: útil 29,9 L. Conferir capacidade de íntimas/meias. Corrediça nominal 300 existe em família comercial; profundidade final da caixa ainda não fechada.'),
 ('Escritório / duas gavetas','Módulo 40 L × 45 P × 24 A; frentes ~12','Corrigir curso','Frente compacta, própria para pequenos itens. Desenvolver nominal 400 mm, não 450. Altura útil e carga permanecem por detalhar. Veja página 5.'),
 ('Cozinha / gaveta de piso','Útil de estudo 118,7 L × 40,6 P × 8,8 A','Peça especial','Não tratar como gaveta convencional de corrediça. Rodas/guias, fundo, esquadro, piso e sustentação dos armários exigem solução própria. Veja página 7.')])
prose('<b>Desconto de ferragem muda o útil:</b> o estudo atual usa 58,3 − 2,6 − 3 = 52,7 cm de largura. Na referência MOVENTO, S4 indica 58,3 − 4,2 = 54,1 cm úteis, mas nominal 500 gera lateral de caixa 490 mm. Os organizadores de 47 cm de profundidade precisam ser reconferidos se houver troca de sistema. Não misturar as duas construções.')

section('02 / Cozinha: portas de abrir e aéreos','Faixas nominais reconstruídas das bases e topo a 255 cm; não são lista de corte de portas.')
rows([
 ('A / sobre geladeira','Caixa 80,1 L × 35 P; faixa A 58,4; 2 frentes ~40,05 L','Escala coerente','Dois vãos internos de 37,35. Frentes abaixo de 60 L, compatíveis em escala com S5/S6. A faixa vertical vai de 196,6 a 255 antes de juntas.'),
 ('B / sobre micro','Caixa 69,7 L × 35 P; faixa A 61; 2 frentes ~34,85 L','Escala coerente','Prateleira atravessa 66,1 L úteis. Carga de louças e flecha precisam de verificação; a aprovação de tamanho não encerra ventilação do micro.'),
 ('C / pia','Caixa proposta 54,7 L × 35 P; faixa A 101,8; 2 frentes ~27,35 L','Altas e estreitas','Dimensão fabricável em princípio. Conferir empenamento e quantidade/posição de dobradiças pelo peso e altura (S5). Não aprovar por comparação apenas com portas de 60 cm de altura.'),
 ('D / depurador','Caixa 65 L × 35 P; faixa de guarda A 59,2; 2 frentes ~32,5 L','Escala coerente','Faixa vai de 195,8 a 255. Vãos irregulares devido ao retorno de ar; portas e divisória não podem obstruir canal ou manutenção.'),
 ('Pia / inferior','Caixa 65 L; frente a P 61; faixa de fechamento ~72 A; 2 folhas ~32,5 L','Escala coerente','Interior nominal 61,4 L × 57,4 P antes de hidráulica. Prateleiras a 22/50 no estudo. Sifão/cuba reduzem volume; útil não é o retângulo inteiro.')])
prose('<b>Um ponto de implantação continua aberto:</b> C de 54,7 pertence à proposta que desloca D 2,5 cm para a lavanderia. A soma A+B+C+D passa a 269,5, contra 267 cm anteriores. Esse avanço já estava registrado; falta comprovar a transição. Não misturar C de 54,7 com uma implantação que só reserve 52,2.')
prose('<b>Profundidade e dobradiças:</b> 35 cm externos deixam 31,4 na hipótese de fundo/frente de 1,8. É uma escala próxima aos aéreos de 31–37 cm dos exemplos S6/S7. Quantidade de dobradiças depende do peso acabado, altura e montagem; não há regra única de duas dobradiças para todas as portas.')

section('03 / Quarto: portas, cabides e profundidade','A questão principal é o espaço líquido após trilhos e fundo, preservando os 60 cm externos de referência.')
rows([
 ('Guarda-roupa / caixa','200 L × 60 P; altura até teto com arremate','Escala plausível','Roupeiro real S9 tem 200 L × 66 P × 236 A. Isso comprova escala geral, mas mostra que copiar uma ferragem pode exigir mais profundidade que a disponível.'),
 ('Portas principais','Duas folhas perto de 100 L; fechamento abaixo do maleiro, cerca de 2 m A','Falta desenho final','Faixa comparável ao TopLine L de S8. Exemplo não selecionado e pode avançar além da caixa. Falta largura/altura acabada, sobreposição, empenamento, carga e percurso para liberar as gavetas.'),
 ('Cabides e roupas','Varões a 103 e 205; maleiro com superfície a 215','Profundidade crítica','Exemplo de sensibilidade: se o sistema consumir 7 P e fundo 1,8, sobram 51,2 P. A reserva de 7 é estudo do maleiro, não medida da ferragem principal; testar cabides vestidos e portas fechadas.'),
 ('Prateleiras / varões','Vãos por pessoa 97,3 L; sapateiras 35,5 L × 35–40 P','Dimensionar apoios','Não deixar automaticamente chapa de 18 mm ou varão de quase 1 m sem conferir peso e flecha. Gavetas externas precisam ficar completamente livres na abertura da porta.'),
 ('Aéreo sobre cama','222 L × 25 P; base 205; 4 folhas de teste 55,2 L','Divisão plausível','No cenário C=244, faixa externa A=39 e útil A=35,4. Cada porta é larga e baixa, mas abaixo da largura de referência de 60 cm de S5. Limitar a abertura conforme estudo em L.'),
 ('Maleiro','Folhas de estudo ~99,45 L × 24 A; 18 mm','Pendente por decisão','RO-32 continua referência condicional. Suspensa a resolução nesta rodada; não transferir para ele a validação das portas principais altas.')])
prose('A proteção posterior de 1 cm já prevista pode levar a projeção total de 60 para 61 cm e reduzir a passagem. Não absorver essa camada diminuindo o interior. Alturas de teto 247/257 cm são cenários documentados; o valor entregue precisa ser medido antes de cortar.')

section('04 / Escritório: onde o detalhe precisa mudar','Profundidade de 45 cm do módulo não comporta uma corrediça de 45 cm mais a construção do móvel.')
rows([
 ('Módulo de gavetas','40 L × 45 P × 24 A; 2 frentes ~12','Nominal 400 como estudo','Com frente e fundo de 1,8, a profundidade geométrica disponível é 41,4. Nominal 450 excede o espaço; nominal 400 deixa reserva para o sistema. Confirmar desenho exato antes de cortar.'),
 ('Aéreo sobre sofá','200 L × 35 P × 55 A; hipótese de 5 módulos de 40','Escala coerente','Comparação S7: módulo real 40 L × 37 P × 60 A. Preservar divisões e apoios; não interpretar os 200 cm como uma única porta ou prateleira sem suporte.'),
 ('Bancada','200 L × 70 P; topo 75 A; espessura aparente 3','Estrutura em aberto','70 P é a profundidade aceita. Um tampo de 2 m com telas e presilhas exige estrutura calculada; 3 cm aparentes não determinam rigidez. Preservar faixa da cadeira e presilha do volante.'),
 ('Prateleira de consoles','110 L × 35 P; topo 195; espessura de estudo 3','Conferir suportes','Existe como peça sob medida, mas parede, balanço, carga e ventilação não estão resolvidos por essas dimensões. Nenhum armário dedicado à caixa do PC deve reaparecer.')])
prose('<b>Conferência com uma referência real:</b> na montagem MOVENTO da p. 422 (S5), 400 + 3 = 403 mm de espaço, menor que 414 mm disponíveis no cenário. A caixa dessa família teria 390 mm de lateral, não 400. Essa é uma demonstração de viabilidade, não escolha de marca ou alteração aprovada da caixa.')
prose('<b>Consequência para o desenho:</b> substituir o ensaio genérico de curso 45 por um ensaio de 40 cm na próxima revisão. A conta y70 + 40 = 110 coincide com o início nominal da cama aberta; folgas, puxador e roupa de cama impedem afirmar acesso garantido. No uso diário, a profundidade da gaveta não é excessiva.')

section('05 / Banheiro e lavanderia','Onde o projeto ainda tem apenas envelopes, a auditoria registra a lacuna em vez de certificar portas inexistentes.')
rows([
 ('Banheiro / gabinete','60 L × 42 P × 54,5 A, suspenso a 20','Envelope plausível','Derivado de pedra a 76,5 e espessura 2. Tipologia e divisão de portas/gavetas ainda não fechadas; não há caixa interna de gaveta para aprovar. Resolver sifão e acesso antes de definir frentes.'),
 ('Banheiro / espelheira','60 L × 12–15 P; A e número de folhas indefinidos','Rasa; falta cota','S10 possui 60 L × 17 P × 75 A. Nossa profundidade é menor, não maior; descontar fundo, espelho/porta, dobradiças e eventual faixa técnica. Não usar 12–15 como profundidade útil.'),
 ('Banheiro / altura de uso','Borda cuba 90; tampo 76,5; cuba 13,5 acima','Coerência aritmética','76,5 + 13,5 = 90. Altura de bancada baixa isolada é consequência da cuba de apoio. Confirmar peça real e conforto; não copiar a bancada de cozinha a 92.'),
 ('Lavanderia / gabinete','59 L; face frontal P 63; pedra 75 P e topo 92','Peça profunda especial','Cesto 45 L × 25 P × 45 A. Profundidade grande serve ao tanque/hidráulica; não significa gaveta de 75 cm. Acessibilidade e manutenção precisam do corte real.'),
 ('Lavanderia / frente cesto','Inferior móvel A 52,1; superior removível A 22,2; largura dentro do módulo 59','Mecanismo por resolver','Folha não é grande demais em escala, mas bascula com cesto e carga. Não substituir por dobradiça comum de porta. Pivô, retenção a 55°, ligação e folgas ainda sem conjunto comercial escolhido.')])
prose('O painel superior do cesto é fixo durante uso e removível para manutenção na proposta. Junta de 4 mm entre painéis e 3 mm sob pedra é estudo. Não confundir a validação geométrica do giro com dimensionamento da ferragem ou aprovação da divisão pelo usuário.')

section('06 / Peças especiais e vãos estruturais','Tamanho fabricável não é o mesmo que capacidade de carga demonstrada.')
rows([
 ('Gaveta de piso','Trecho bruto 126,9; útil 118,7 × 40,6 × 8,8','Prioridade alta','Larga e muito baixa. Seis rodas são apenas proposta; precisam trabalhar sem torção/travamento. Apoios da pedra e dos gabinetes não podem depender da gaveta nem atravessar seu percurso.'),
 ('Banco / tampas','Banco 180 L × 55 P; assento 45 P e topo 47. Tampas estudadas 21,6 e 36,8 L × 44,8 P × 2','Carga de pessoa','Essas tampas não são portas gigantes. O problema é resistência como assento, retenção aberta e apoios. Almofada de 5 cm completa a altura no estudo; não somar a espessura antiga de 7 cm.'),
 ('Prateleiras de cozinha','B: vão 66,1 L; C: 51,1 L no cenário ampliado','Carga localizada','Pilha de 18 pratos concentra peso. Verificar chapa, vão, apoios e deformação ao longo do tempo. Reforço que desça no vão reduz a altura útil e precisa voltar à conta do conteúdo.'),
 ('Sala / painel e prateleiras','Painel 112 L × 165 A; prateleiras 107 L × 25/35 P','Fixação e balanço','Dimensões são plausíveis sob medida; não equivalem a vão de 107 sem apoio. TV e prateleiras precisam de caminho de cargas até a parede, não apenas ao painel decorativo.'),
 ('Mesa extensível','150/180 L × 75 P; folha adicional 30 × 75','Ferragem e pedestal','Dimensões de mobiliário plausíveis; fechamento técnico depende de trilho, travamento e estabilidade da base. Não tratar como porta ou gaveta nem validar só pela espessura do tampo.')])
prose('<b>Critério para G3:</b> pesar ou estimar explicitamente caixa + frente + alimentos + bebidas + organizadores. Como exemplo matemático, conjunto de 30 kg em referência de 40 kg deixa 10 kg até a classe nominal; esse exemplo não mede o nosso estoque. Se a conta ultrapassar a capacidade, mudar o sistema e rever montagem antes de reduzir o programa.')

section('07 / O que esta revisão encaminha','Não há motivo demonstrado para reduzir todas as gavetas ou copiar módulos industriais exatos.')
prose('<b>Manter as proporções:</b> cozinha 61,9 e 16/16/40; duas folhas nos aéreos A/B/C/D; divisões do escritório e do aéreo da cama. Elas têm escala compatível com produtos ou ferragens reais, sob as condições das páginas anteriores.')
prose('<b>Corrigir no próximo detalhamento:</b> escritório com referência nominal 400 mm, abandonando a simulação de 450 dentro de corpo externo 450. Recalcular altura e útil das duas gavetas com a ferragem escolhida.')
prose('<b>Fechar primeiro, antes de fabricar:</b> estrutura e guiamento da gaveta de piso; corte de G2 garantindo H ≥ 11,1; peso/corrediça/fundo do gavetão G3; profundidade líquida e abertura das portas do guarda-roupa; apoios das prateleiras, tampo e assentos.')
prose('<b>Completar as cotas ausentes:</b> caixas internas das gavetas do quarto/escritório, portas principais do roupeiro, altura/folhas da espelheira e interior do gabinete do banheiro. O levantamento acabado também precisa confirmar alturas de teto, esquadro e espessuras de acabamento.')
prose('<b>Manter pendentes:</b> maleiro, conforme pedido; folgas dos equipamentos e avanço de 2,5 cm do aéreo D na transição da lavanderia. A existência de móveis semelhantes no mercado não encerra essas interferências.')
story.append(Spacer(1,10))
prose('Para cada peça executiva, a marcenaria deve entregar uma ficha com: frente acabada; caixa externa; útil interno; espessuras; referência e comprimento de ferragem; curso; peso total e classe de carga; folgas; apoios; abertura e retirada. Assim, uma gaveta “de 50” não muda de significado entre desenho, orçamento e produção.')
prose('<b>Resultado da auditoria:</b> escala geral consistente, um ajuste concreto de profundidade no escritório e pontos especiais identificados. Ainda não há base para declarar todo o apartamento dimensionado para fabricação.')

section('08 / Referências de mercado e ferragens','Fontes primárias consultadas em 12/10/2026. Produtos comparativos; sem pesquisa de preço ou estoque.')
for sid,name,desc,url in sources:
 story.append(p(f'<b>{sid} / <link href="{escape(url)}" color="{BLUE}">{escape(name)}</link></b> — {escape(desc)}','small'))
story.append(p('<b>Complemento S5:</b> <link href="https://publications.blum.com/2024/catalogue/pt/422/" color="#3A666D">MOVENTO, planificação e profundidade mínima</link>. As referências europeias são exemplos construtivos, sem disponibilidade brasileira presumida.','small'))
story.append(p('<b>Base local:</b> Interior das gavetas 25/09 + G1/G2 30/09 + G2 03/10; Torre × gavetas 28/09; Aparelhos R03 27/09; Aéreos R00; Guarda-roupa interior R02 e encontro L 12/10; Escritório R09/R10; Banheiro consolidado 18/09; Cesto retirada 30/09; Detalhe banco 08/10 e aceite 09/10; Painel da sala R01. Notas antigas foram tratadas como históricas quando superadas.','small'))
def frame(c,doc):
 c.setFillColor(HexColor('#FAF8F3'));c.rect(0,0,842,595,fill=1,stroke=0)
 c.setFont('Bold',9);c.setFillColor(HexColor(INK));c.drawString(36,570,'GUEDALA PARK / VERIFICAÇÃO DIMENSIONAL')
 c.setFont('Reg',8);c.drawRightString(806,570,'12/10/2026')
 c.setStrokeColor(HexColor('#BCC8BE'));c.line(36,32,806,32)
 c.setFont('Reg',8);c.drawString(36,18,'COTAS EM CM / ESTUDO DOCUMENTAL / SEM LIBERAÇÃO DE FABRICAÇÃO');c.drawRightString(806,18,str(doc.page))
doc=SimpleDocTemplate(str(OUT),pagesize=(842,595),leftMargin=36,rightMargin=36,topMargin=45,bottomMargin=44,title='Guedala Park - Auditoria dimensional de marcenaria',author='Projeto Guedala Park')
doc.build(story,onFirstPage=frame,onLaterPages=frame)
checks={'cozinha_largura_util_hipotese':61.9-3.6-2.6-3,'cozinha_profundidade_util_hipotese':50-3,'cozinha_altura_frentes':16+16+40,'cozinha_aereos_total_proposto':80.1+69.7+54.7+65,'cozinha_avanco_D':80.1+69.7+54.7+65-267,'escritorio_disponivel_mm':450-18-18,'escritorio_nominal450_cabe':450<=450-18-18,'escritorio_nominal400_mais3_cabe':403<=450-18-18,'g2_perdas_maximas_para_H11_1':16-11.1,'quarto_gaveta_util_hipotese':35.5-2.6-3}
assert abs(checks['cozinha_largura_util_hipotese']-52.7)<1e-8
assert not checks['escritorio_nominal450_cabe'] and checks['escritorio_nominal400_mais3_cabe']
data={'date':'2026-10-12','scope':'auditoria de escala, medidas e referências; não dimensionamento executivo','maleiro':'pendente a pedido de Elias','rows':inventory,'sources':[dict(id=a,name=b,evidence=c,url=d) for a,b,c,d in sources],'checks':checks,'output':str(OUT)}
(HERE/'Auditoria_dados.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
print(str(OUT))
