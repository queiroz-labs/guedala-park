from pathlib import Path
import json,csv,html,hashlib,math,re
from collections import Counter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A3,A4,landscape
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,KeepTogether
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle

p=Path(__file__).resolve().parent;b=p.parent;repo=b.parents[1]
out=repo/'output/pdf';out.mkdir(parents=True,exist_ok=True)
d=json.loads((p/'Base_pranchas_R28.json').read_text(encoding='utf-8'))
font=Path('C:/Windows/Fonts')
pdfmetrics.registerFont(TTFont('Main',str(font/'arial.ttf')))
pdfmetrics.registerFont(TTFont('MainBold',str(font/'arialbd.ttf')))
pdfmetrics.registerFontFamily('Main',normal='Main',bold='MainBold',italic='Main',boldItalic='MainBold')
ink=colors.HexColor('#223D39');teal=colors.HexColor('#287C79');orange=colors.HexColor('#B66A22');gray=colors.HexColor('#6B7475');light=colors.HexColor('#E8EFEB')
names=['Roupeiro','Canto em L','Maleiro','Cabeceira - aéreo','Gabinete da pia','Gavetas G1/G2/G3','Estrutura de cocção','Gaveta baixa','Aéreo D','Aéreo C','Aéreo B','Aéreo A','Apoio do micro','Tanque e cesto','Aéreo lavanderia','Gavetas escritório','Aéreo escritório','Gabinete banheiro','Armário espelhado','Banco baú']
notes=[
 'Programa preservado: 650 externos / zona de roupa550. Folhas995x1999; curso965 proposto. Guias/apoios/retencão são reservas. Quatro gavetas NL500, curso400 de estudo.',
 'Duas portas271x306x18; faixas142/124; juntas2; faixa vizinha25. K4, caneco35x13 propostos. 86° não comprova batente. Este L exige leitura conjunta das três projeções.',
 'Duas folhas670x237; curso640. Aplicação baixa/larga e retenção do RO-62 não comprovadas. Corpo1350x650x308 preservado.',
 'Quatro folhas atuais alternadas incluindo vizinha R18. Vizinha K6/recobrimento17; demais K5/16. Apoios duplos36 e novas juntas são propostas, não ligações calculadas.',
 'Par de portas comuns: K5/recobrimento16/calço0. Centro e hidráulica dependem da cuba/sifão reais. Não interpretar caixas da bancada como recorte executivo.',
 'Frentes16/16/40cm preservadas. Interno G2 541x459; bandejas455 e folgas2+2. Reserva G2 até guia G1 116,4, apenas5,4 além do programa111. Carga total40kg candidata.',
 'Corpo CAD não resolve recorte/instalação do forno/cooktop. Venax3/5 versus10cm e cota inferior KE4GC pendentes; ventilação/apoios/isolamento LG a detalhar.',
 'Programa: frente106, base180/recuo80, cabos fixos/cabeças retiradas. Interno1187x406x88. Curso530 é retirada ideal, não batente; seis rodas são gabaritos.',
 'D: canal196x178 ainda bloqueado por base/tampo inteiros. Não furar por este esquema. Conexão do depurador, retorno e fixação continuam pendentes.',
 'Par de portas comuns e programa interno preservados. Conteúdo real, alcance, carga e fixação não comprovados. K5/recobrimento16/calço0.',
 'Micro:100mm acima é escolha expressa que diverge dos300 do manual. Não alterar B para aparentar atendimento; implantação executiva ainda não fechada.',
 'Geladeira: reservas100 laterais/traseira/topo do estudo. Não são tolerâncias extras. Abertura/retirada reais, pés, tomadas e acabamentos pendentes.',
 'Prateleira aberta697x470x18. Corpo micro352 de profundidade, reserva traseira separada. Fixação/apoio/pés/cabos/carga ainda não definidos.',
 'Cesto450x250x450, giro55 e saco removível. Pivôs/apoios são gabaritos. Na manutenção, Loop temporariamente650 antes da retirada da armação; produto/recorte do tanque pendentes.',
 'Par de portas comuns. E21 tem folgas laterais70/50 versus200 recomendados. Datums, duto e conexões desconhecidos; não alterar instalações com base no esquema.',
 'Duas gavetas NL400/curso400. Caixa e frente preservadas; perfis estáticos. Uso com sofá-cama preparado não está homologado; fixação/carga pendentes.',
 'R28: base1900/topo2450; teto de estudo2470, folga20 nominal. Caixa550 e vãos preservados. Quatro portas alternadas496x548; apoios36 propostos.',
 'Duas folhas297x543, centro livre. Fechar entrada ideal antes de abrir gabinete. Porta de entrada700/eixo/maçaneta não medidos; hidráulica/fixação pendentes.',
 'Duas folhas297x748, madeira18 + espelho4. Três dobradiças por folha candidatas. Duas prateleiras560x104x18; vidro/adesivo/pinos/LED reais pendentes.',
 'Programa externo1800x550 e topo470. Corpo450x400 não é envelope acabado. Quatro setores: sequência sofá→cozinha. Última almofada removível/recuo folha24 são propostas novas.'
]
source_by_module=['Correr_R14_2026-10-14/README.md','Canto_2026-10-13/Canto_simples_R04/README.md','Correr_R14_2026-10-14/README.md','Portas_opostas_R18_2026-10-14/README.md','Dobradicas_R10_2026-10-14/README.md','Padronizacao_R08_2026-10-14/README.md','Equipamentos_R17_2026-10-14/README.md','Gaveta_rodas_R13_2026-10-14/README.md','Equipamentos_R17_2026-10-14/README.md','Dobradicas_R10_2026-10-14/README.md','Equipamentos_R17_2026-10-14/README.md','Equipamentos_R17_2026-10-14/README.md','Equipamentos_R17_2026-10-14/README.md','Cesto_R15_2026-10-14/README.md','Equipamentos_R17_2026-10-14/README.md','Padronizacao_R08_2026-10-14/README.md','Folga_teto_R28_2026-10-14/README.md','Banheiro_R12_2026-10-14/README.md','Banheiro_R12_2026-10-14/README.md','Banco_R16_2026-10-14/README.md']

# Hardware quantities count assemblies, not STEP bodies.
hardware=[
 ['F01','Blum71B3550','54 conjuntos','26 portas:24 comuns +2 canto','Referência oficial; quantidade/montagem candidata','R10:24; R18:16; R12:10; R04:4. Não somar R11 antigo ou71B3650 aposentada.'],
 ['F02','Blum173H7100','54 calços','Um por dobradiça F01','Referência oficial; aplicação proposta','Calço0, recobrimentos/K conforme cada montagem; parafusos/apoio a conferir.'],
 ['F03','Blum70T3553','Quantidade executiva não definida','Portas com estudo86°','Referência oficial; encaixe/batente pendentes','Fabricante orienta todas as dobradiças da folha;54 seria cenário para equipar todas as F01, não lista de compra.'],
 ['F04','MOVENTO NL500 /40kg candidato','7 pares','4 roupeiro + G1/G2/G3','Fontes oficiais; 6 aplicações parametrizadas +G2 configurada','Curso roupeiro400/cozinha500. Sólidos estáticos, não telescópio; carga inclui caixa/frente/conteúdo.'],
 ['F05','MOVENTO NL400 /40kg candidato','2 pares','Escritório','Fontes oficiais; aplicações propostas','Curso400. Capacidade/fixação individuais a confirmar.'],
 ['F06','BlumT51.7600','9 pares /18 travas','Nove gavetas F04/F05','Referência oficial; aplicação proposta','Par esquerdo/direito por gaveta. Não tratar um par como18 pares.'],
 ['F07','RometalRO-62 - carros','8 reservas','2 carros por folha;4 folhas','Manual oficial; semSTEP oficial','Dimensões dos carros são hipotéticas;60kg/porta não é capacidade por carro.'],
 ['F08','Guia Flex / freios / retenções','8 /8 /8 reservas','Roupeiro e maleiro','Manual e reservas; kit exato pendente','Aplicação maleiro baixo/largo não comprovada. Não fabricar peças pelos gabaritos.'],
 ['F09','RM-025 superior / RM-023 inferior','4 /4 trechos modelados','Duas vias em cada um dos2 módulos','Larguras oficiais; seções restantes hipotéticas','Contagem de trechos CAD, não barras comerciais ou comprimentos de compra.'],
 ['F10','Rodízio fixo de silicone','6 gabaritos','Gaveta baixa','Sem produto/composição/carga confirmados','Roda30/altura39 é estudo; não substituir por PVC nem dividir carga por6 como garantia.'],
 ['F11','Guias laterais da baixa','2 faixas propostas','Gaveta baixa','Peças de marcenaria; não ferragem selecionada','3mm +2mm de corrida/lado; não são apoios verticais.'],
 ['F12','Pivô/retentor do cesto','2 pinos ideais; retenção a definir','Cesto55°','Gabaritos sem SKU/carga','PinosØ10x20 não são prescrição de fabricação; apoios/hidráulica reais pendentes.'],
 ['F13','Giro/retenção das tampas do banco','4 eixos ideais; quantidade comercial indefinida','Quatro setores','Sem ferragem executiva selecionada','Não interpretar4eixos como4dobradiças suficientes. Preservar tampas/rotina e carga do assento.'],
 ['F14','Pinos das prateleiras do banheiro','A definir','2 prateleiras removíveis','Produto/fixação/carga pendentes','Não atribuir quantidade/capacidade a apoios não selecionados.'],
 ['F15','Fixações de parede, apoios, puxadores e vidro','A definir','Todos os módulos aplicáveis','Dependência física/comercial','Substrato, carga, material, adesivo, ferragem e acabamento reais necessários.']]

sequences=[
 ('S01 - Preparação e montagem geral',[
  'Usar o arquivo R28 e o módulo indicado na prancha; confirmar que a cozinha fica à esquerda ao entrar. Os nomes de controle vigentes referem-se à implantação espelhada.',
  'Antes de executar: conferir paredes, teto acabado, piso, pontos hidráulicos/elétricos/gás, produtos e substrato de fixação. O caderno não contém pilotos, ancoragens ou cortes executivos.',
  'Conferir o corpo e a ordem dos apoios/divisores; depois apresentar frentes e ferragens comuns na configuração comercial correspondente. Apoios duplos36 e montagens de18 continuam propostas a dimensionar.',
  'Instalar somente após fechar fixação/carga e instruções do produto escolhido; regular folgas e batentes. A etapa final em obra deve verificar os acessos reais e as interferências, sem tratar os testes CAD como substituto.'
 ],'R28; R10/R18/R12; relatório de pendências. Sequência de planejamento, não instrução executiva de instalação.'),
 ('S02 - Portas comuns e canto',[
  'Usar os controles originais do guia vigente. Nas folhas comuns, Abertura0 é fechado e86 é limite do estudo; não editar Placement dos vínculos.',
  'Escritório e cabeceira alternam esquerda/direita na vista frontal vigente. Na vizinha do canto usar ControleVizinhaR18.Abertura; ControleCanto.B4 pertence ao histórico.',
  'No canto, ControleSimplesR04.B2 controla A e B3 controla B. As duas folhas são independentes com faixas fixas; o cenário R04 estudou ambas abertas. Não voltar à articulação79T8500.',
  'Em montagem real, confirmar caneco/calço/parafusos e limitador conforme ferragem. O curso86 da planilha não comprova o contato do70T3553, e o mapa de centros dos calços não é mapa de furação.'
 ],'Guia vigente R28; R04; R18. Não pressupõe intertravamento físico.'),
 ('S03 - Roupeiro, maleiro e gavetas comuns',[
  'Abrir a folha de correr correspondente antes de acessar as quatro gavetas do roupeiro. Os controles de correr têm valor positivo em ambos os lados, com drivers em sentidos opostos.',
  'Roupeiro: Deslocamento0–965 de estudo; maleiro0–640. Essas distâncias não comprovam freio, batente, antidesencaixe ou curso comercial.',
  'Gavetas do roupeiro e escritório: Extensao0–400; cozinha G1/G2/G3:0–500. Manipular o objeto original através do atalho, sem deslocar a geometria do módulo.',
  'Para retirada física/manutenção, seguir a instrução da configuração comercial efetivamente instalada. Não inferir destravamento ou telescópio pelo sólido estático; não forçar uma gaveta contra uma porta parcialmente aberta.',
  'Fechar as gavetas antes de devolver a porta de correr. Conferir massa total com o quadro de carga; saldo calculado não é carga útil liberada.'
 ],'R08/R14; guia vigente; Cargas_gavetas_R28. Puxadores, mãos e configuração de cama preparada não homologados.'),
 ('S04 - G2 e bandejas removíveis',[
  'Abrir G2 na posição de estudo500 antes de iniciar as rotas documentadas de retirada. As duas bandejas têm455mm de profundidade, com2mm à frente e atrás no interno459.',
  'Manter os oito utensílios e a frigideira candidata nos respectivos gabaritos; suas caixas não informam peso, alças ou pega real.',
  'As rotas documentadas são translações com orientação fixa. Não inclinar, trocar posição ou empilhar objetos e assumir que a mesma conferência cobre a nova operação.',
  'Recolocar bandejas e conteúdo no arranjo previsto, verificar livre assentamento e fechar G2. Confirmar materiais, massas, tolerâncias e fixação antes da execução.'
 ],'R06/R07/R08; Complementos_R24; orçamento de carga R28.'),
 ('S05 - Gaveta baixa sobre rodas',[
  'Preservar cabos fixos com as cabeças retiradas; não trocar por cabos retráteis nem corrediças MOVENTO.',
  'Extensao530 é a retirada completa ilustrativa. A posição400 herdada não é comprimento nominal de guia;442 é profundidade da caixa, não NL comercial.',
  'No percurso ideal documentado, retirar até530 e elevar40 para manutenção. Pega, esforço, piso, batente e rodízios reais continuam pendentes; essa trajetória não é instrução física já validada.',
  'Repor sobre as guias/piso sem sobrecarregar o fundo. Confirmar o material silicone e a distribuição de carga, sem garantir seis apoios simultâneos.'
 ],'R13; Cotas/rodízios em Pendencias_autonomas. Frente106/base180/recuo80 preservados.'),
 ('S06 - Cesto: uso diário',[
  'ControleCestoR15: abrir55; retirar o saco445; endireitar o saco55, nessa ordem do estudo.',
  'Não confundir retirada diária do saco com remoção completa da armação. O saco removível e o giro55 fazem parte do programa preservado.',
  'Repor em ordem inversa: desfazer endireitamento, devolver saco e fechar o cesto. Confirmar retenção, ferragem, carga e manuseio reais antes de uso físico.'
 ],'R15; guia vigente. Valores CAD não constituem trava ou intertravamento.'),
 ('S07 - Cesto: manutenção da armação',[
  'Desocupar o trajeto e deslocar a Loop20L por ControleLoopManutencaoR26.Afastamento650, do lugar habitual em direção ao centro da cozinha. O controle0 é a posição cotidiana.',
  'Com a lixeira na posição proposta, seguir a abertura55 e os comandos de manutenção do painel/armação documentados na R15/R26. A retirada integral é estudo condicionado, não uma operação física já homologada.',
  'A posição habitual da lixeira colide com a armação nas retiradas300/400. Não ocultar a lixeira e não iniciar essa retirada mantendo-a em0.',
  'Repor armação e painel, fechar o cesto e somente então devolver a Loop para0. Piso, pessoa, pega, peso e apoios reais ainda precisam ser conferidos.'
 ],'R26; R15. Há100mm nominais no encontro avaliado; não garantia de manuseio.'),
 ('S08 - Banco: uso dos setores diários',[
  'Banco desocupado. A ordem do programa parte do sofá: potes/travessas/batedeira; liquidificador/bebidas; balde; folha/aspirador/jogos.',
  'Primeiro setor: o estudo gira assento integral70. Não tratar a almofada como solta durante o giro; acoplamento, massa, pega e retenção continuam pendentes.',
  'Bebidas: elevar almofada60, deslocar711, baixar elevação para50; depois abrir tampa90. Balde: elevar60, deslocar733, baixar para50; depois abrir90.',
  'As almofadas estacionam sobre o último setor fechado. Enquanto estiverem ali, não abrir o setor da folha. Devolver cada almofada após fechar sua tampa, em ordem inversa.',
  'Para retirar os painéis de armazenamento dos potes, esvaziá-los primeiro. O balde segue a rota ideal de levantar32 e recuar19 antes de subir; alça e mão reais não foram validadas.'
 ],'R16. Apoios7mm/24mm de montagem são propostas geométricas, não capacidade de assento.'),
 ('S09 - Banco: acesso à folha da mesa',[
  'Devolver primeiro as almofadas de bebidas e balde aos seus setores e manter os três primeiros setores fechados. Não abrir contra almofadas estacionadas.',
  'Nova proposta do último setor: elevar a almofada60, deslocar873 rumo ao sofá e baixar a elevação para50, sobre os três outros setores fechados. Eles ficam temporariamente inacessíveis.',
  'Abrir a tampa fina90. Recuar a folha inteira800x350x70 em24 antes de subir pela rota documentada; a vista de estudo usou elevação970. Não reduzir a folha.',
  'Transporte, pessoa, pega e instalação na mesa não foram validados. Repor em ordem inversa e devolver a almofada antes de usar os outros setores. Não atribuir esta nova rotina ao aceite antigo de09/10.'
 ],'R16 e complemento banco×sofá R28. Rotas limitadas ao cenário documentado, sem intertravamento.'),
 ('S10 - Banheiro e equipamentos',[
  'Fechar a entrada ideal antes de abrir o gabinete inferior do banheiro. A folha700, eixo e maçaneta são referências não medidas; não há bloqueio físico que imponha essa ordem.',
  'Fechar o gabinete inferior antes de reabrir a entrada. Não usar110° nas portas de estudo: há interferências com parede/espelho nas condições registradas.',
  'Prateleiras removíveis, vidro, adesivo, pinos, LED e hidráulica precisam de especificação real. Não apoiar peso ou deduzir capacidade das caixas CAD.',
  'Antes da instalação dos equipamentos, fechar as divergências do relatório: E21, micro100vs300, retorno Suggar, forno/cooktop e isolamento LG. Não operar a airfryer no nicho de guarda por ausência de colisão; o programa prevê uso temporário no preparo.'
 ],'R12/R17; relatório de correções. Não há nova decisão de modelo ou ponto de instalação.')]

audit=[
 ['D01','Controle da porta vizinha','README R04 ainda indicava ControleCanto.B4, que pertence à etapa anterior.','Guia vigente identifica ControleVizinhaR18.Abertura. Nota de precedência adicionada ao histórico.'],
 ['D02','Quantidade de dobradiças','Somar R10+R11+R12+R18 duplicaria sete montagens e manteria a71B3650 aposentada.','Inventário deduplicado por folha atual:24+16+10+4=54;54calços.'],
 ['D03','Carga útil','A fórmula R08 subtraía o conteúdo mas era chamada payload.','Quadro R28 distingue orçamento para conteúdo de margem restante; histórico anotado.'],
 ['D04','Folga teto/escritório','Tabela histórica R26 registrava zero e base1920/topo2470.','Atual R28: base1900/topo2450 e folga20 sob teto hipotético2470. Nota de supersessão sem apagar evidência antiga.'],
 ['D05','Manutenção Loop','Textos antigos diziam apenas desobstruir a lixeira, sem endereço.','R26 define estacionamento650; guia e sequências atuais incorporam ida/volta e limites físicos.'],
 ['D06','Cotas de corpo e acabado','Banco450x400 e baixa145 podem ser confundidos com envelope acabado.','Pranchas separam corpo CAD, banco externo550/topo470 e baixa frente106/base180/recuo80.'],
 ['D07','Quantidade de controles','R21/R23 tinham45 acessos; textos históricos ainda usam essa contagem.','R26/R28 têm46, incluindo Loop; os57 campos pertencem aos controles originais.'],
 ['D08','Dados oficiais e gabaritos','Sólidos de ferragem, esquemas, cursos e reservas podem parecer lista de compra.','Classificação explícita de referência oficial/aplicação proposta/reserva; sem quantidade executiva inventada.'],
 ['D09','Revisão Astra e prazo','Documentos antigos registram reserva18h30; prazo19h já encerrou.','Resultado final é pendente/não verificado; automação excluída. Este novo trabalho é pedido humano posterior, sem reiniciar agendamento.']]

def savecsv(file,headers,rows):
 with (p/file).open('w',newline='',encoding='utf-8-sig') as f:
  w=csv.writer(f,delimiter=';');w.writerow(headers);w.writerows(rows)
savecsv('Ferragens_consolidadas_R28.csv',['ID','Referencia','Quantidade_do_estudo','Aplicacao','Classificacao','Limite'],hardware)
coords=[];pieces=[]
for i,m in enumerate(d['modules']):
 C=m['body_dimensions_mm']['Comprimento']
 for j,h in enumerate(m['hinge_references']):
  x,y,z=h['plate_center_local_mm'];coords.append([f'P{i+1:02d}',m['object'],f'H{j+1:02d}',h['plate'],h['door'],C-x,y,z,'Centro da envoltoria do calco; NAO coordenada de furacao',h['source']])
 for q in m['pieces']:pieces.append([f'P{i+1:02d}',m['object'],q['object'],q['label'],q['kind'],*q['local_bbox']])
savecsv('Referencias_calcos_54_R28.csv',['Prancha','Modulo','Marcador','Objeto','Porta','X_frontal_espelhado','Y_local','Z_local','Tipo_de_referencia','Fonte'],coords)
savecsv('Componentes_774_R28.csv',['Prancha','Modulo','Objeto','Rotulo','Representacao','Xmin_local','Ymin_local','Zmin_local','Xmax_local','Ymax_local','Zmax_local'],pieces)
savecsv('Conferencia_documental_R28.csv',['ID','Tema','Divergencia_ou_risco','Tratamento'],audit)
(p/'Sequencias_R28.json').write_text(json.dumps(sequences,ensure_ascii=False,indent=2),encoding='utf-8')

def wrapdraw(c,text,x,y,width,size=9,leading=13):
 c.setFont('Main',size);c.setFillColor(ink)
 line=''
 for word in text.split():
  t=(line+' '+word).strip()
  if pdfmetrics.stringWidth(t,'Main',size)>width and line:
   c.drawString(x,y,line);y-=leading;line=word
  else:line=t
 if line:c.drawString(x,y,line);y-=leading
 return y
def dim(c,p1,p2,label,vertical=False):
 c.setStrokeColor(teal);c.setLineWidth(.6);c.line(*p1,*p2)
 for x,y in [p1,p2]:
  if vertical:c.line(x-4,y,x+4,y)
  else:c.line(x,y-4,x,y+4)
 c.setFillColor(teal);c.setFont('MainBold',9)
 if vertical:
  c.saveState();c.translate(p1[0]-7,(p1[1]+p2[1])/2);c.rotate(90);c.drawCentredString(0,0,label);c.restoreState()
 else:c.drawCentredString((p1[0]+p2[0])/2,p1[1]-13,label)
def projection(c,m,axis,x,y,w,h,title):
 C,P,A=[m['body_dimensions_mm'][k] for k in ['Comprimento','Profundidade','Altura']]
 # Corner's source frame extends backwards from Y=-1050 to0. Normalize only the drawing.
 yshift=P if m['object']=='Modulo001' else 0
 def project(v):return (C-v[0],v[2]) if axis=='front' else (C-v[0],v[1]+yshift) if axis=='top' else (v[1]+yshift,v[2])
 bodyW,bodyH=(C,A) if axis=='front' else (C,P) if axis=='top' else (P,A)
 corners=[(0,0),(bodyW,bodyH)]
 for q in m['pieces']:
  bb=q['local_bbox'];corners.extend(project(v) for v in [(bb[0],bb[1],bb[2]),(bb[3],bb[4],bb[5])])
 xmin=min(v[0] for v in corners);xmax=max(v[0] for v in corners);ymin=min(v[1] for v in corners);ymax=max(v[1] for v in corners)
 scale=min((w-90)/(xmax-xmin),(h-70)/(ymax-ymin));ox=x+45+(w-90-(xmax-xmin)*scale)/2-xmin*scale;oy=y+35+(h-70-(ymax-ymin)*scale)/2-ymin*scale
 xy=lambda v:(ox+v[0]*scale,oy+v[1]*scale)
 c.setFillColor(ink);c.setFont('MainBold',11);c.drawString(x,y+h-10,title)
 for q in m['pieces']:
  c.setStrokeColor(teal if q['kind']=='metal' else orange if q['kind']=='reserve' else gray);c.setLineWidth(.4 if q['kind']=='panel' else .5)
  if q['lines']:
   for line in q['lines']:
    points=[xy(project(pt)) for pt in line];path=c.beginPath();path.moveTo(*points[0])
    for pt in points[1:]:path.lineTo(*pt)
    c.drawPath(path)
  else:
   bb=q['local_bbox'];v1=xy(project(bb[:3]));v2=xy(project(bb[3:]));c.rect(min(v1[0],v2[0]),min(v1[1],v2[1]),abs(v2[0]-v1[0]),abs(v2[1]-v1[1]),fill=0,stroke=1)
 c.setDash(4,3);c.setStrokeColor(colors.HexColor('#243E39'));c.setLineWidth(.8);a=xy((0,0));c.rect(a[0],a[1],bodyW*scale,bodyH*scale);c.setDash()
 dim(c,(ox,oy-15),(ox+bodyW*scale,oy-15),f'{bodyW:g} corpo')
 dim(c,(ox-18,oy),(ox-18,oy+bodyH*scale),f'{bodyH:g} corpo',True)
 if axis=='front':
  for j,r in enumerate(m['hinge_references']):
   px,py=xy(project(r['plate_center_local_mm']));c.setFillColor(teal);c.circle(px,py,2,fill=1,stroke=0);c.setFont('MainBold',7);c.drawString(px+4,py+3,f'H{j+1:02d}')
 c.setFillColor(gray);c.setFont('Main',7);c.drawRightString(x+w,y+2,'Escala ajustada à folha; não medir pelo papel')

pdf1=out/'Guedala_R28_Pranchas_cotadas.pdf'
c=canvas.Canvas(str(pdf1),pagesize=landscape(A3));W,H=landscape(A3)
c.setTitle('Guedala Park R28 - Pranchas cotadas de compatibilizacao')
c.setFillColor(ink);c.setFont('MainBold',32);c.drawString(45,H-70,'Guedala Park | 20 módulos')
y=wrapdraw(c,'Pranchas cotadas de compatibilização - base R28',45,H-110,1050,20,27)
y=wrapdraw(c,'Entregue após pedido de Elias para executar o detalhamento documental. Não houve alteração do arquivo FreeCAD. As projeções usam a geometria atual dos módulos, com cotas de corpo e referências de posição; não são desenhos de corte ou furação.',45,y-20,1060,12,18)
y=wrapdraw(c,'Leitura: contorno tracejado = corpo nominal; linhas cinza = geometria CAD simplificada; azul = envoltórias de ferragens; laranja = reservas identificadas. H01... são centros das envoltórias dos calços, não centros de parafusos. Todas as cotas estão em mm. Frontais espelhadas; vistas complementares em coordenadas locais. Sem escala fixa.',45,y-14,1060,11,17)
y=wrapdraw(c,'Programa preservado: implantação com cozinha à esquerda, portas vizinhas alternadas, canto simples, modelos de equipamentos e organização aprovada. Cotas derivadas das propostas R04–R28 não se tornam aprovadas por aparecerem cotadas. Referências completas e limites estão no caderno técnico.',45,y-12,1060,11,17)
for i,n in enumerate(names):
 col=i//10;row=i%10;c.setFont('Main',12);c.drawString(55+col*530,y-40-row*24,f'P{i+1:02d}  {n}')
wrapdraw(c,'Fora do recorte das pranchas: arquitetura e equipamentos soltos constam nas oito vistas do relatório geral. O banco tem encosto externo fora do módulo; ver dimensão acabada1800x550/topo470. Ferragens de compra e ancoragens dependem de confirmação.',45,115,1070,11,16)
c.setFont('Main',8);c.drawString(45,42,'R28 |14/10/2026 | Compatibilização, sem liberação de fabricação | Folha0');c.showPage()
for i,m in enumerate(d['modules']):
 C,P,A=[m['body_dimensions_mm'][k] for k in ['Comprimento','Profundidade','Altura']];bb=m['closed_adopted_bbox_mirrored_mm']
 c.setFillColor(ink);c.setFont('MainBold',22);c.drawString(42,H-48,f'P{i+1:02d} | {names[i]}')
 c.setFont('Main',11);c.drawString(42,H-73,f'{m["object"]} | Corpo CAD {C:g} x {P:g} x {A:g} mm | Z global do conjunto: {bb[2]:g} a {bb[5]:g} mm')
 wrapdraw(c,'REFERÊNCIA DE MODELO / PROPOSTA DE COMPATIBILIZAÇÃO. Não medir pela escala nem usar centros de calço como furação.',42,H-96,1100,9,13)
 projection(c,m,'front',48,335,620,365,'FRONTAL - orientação local espelhada')
 projection(c,m,'top',48,92,620,210,'PLANTA LOCAL - profundidade do corpo')
 projection(c,m,'side',715,335,415,365,'LATERAL LOCAL - projeção sem corte')
 y=wrapdraw(c,notes[i],715,300,415,10,15)
 fronts=[]
 for dr in d['doors']:
  if dr['module']==m['object']:
   q=next(v for v in m['pieces'] if v['object']==dr['front']);z=q['local_bbox'];fronts.append(f'{z[3]-z[0]:g}x{z[5]-z[2]:g}')
 if fronts:y=wrapdraw(c,'Frentes LxA no estado fechado (mm): '+', '.join(fronts)+'.',715,y-4,415,8,11)
 if m['object']=='Modulo001':y=wrapdraw(c,'Origem do canto: Ylocal -1050 a0; planta/lateral normalizadas apenas no desenho.',715,y-3,415,8,11)
 y=wrapdraw(c,'Calços: marcadores da frontal; XYZ completos no CSV Referencias_calcos_54_R28. Origem local do módulo; Xfrontal = largura - Xlocal.',715,y-7,415,8,11)
 for j,h in enumerate(m['hinge_references'][:8]):
  x,y0,z=h['plate_center_local_mm'];c.setFont('Main',8);c.drawString(715,y,f'H{j+1:02d}: X{C-x:.1f} / Y{y0:.1f} / Z{z:.1f} mm - centro de envoltória');y-=12
 if not m['hinge_references']:y=wrapdraw(c,'Sem conjunto de dobradiça comum neste módulo. Ferragens e mecanismos aplicáveis: consultar lista consolidada.',715,y-4,415,9,13)
 c.setStrokeColor(light);c.line(42,70,W-42,70)
 wrapdraw(c,'Fonte: '+source_by_module[i],42,56,1080,8,11)
 c.setFont('Main',8);c.drawString(42,29,'R28 | mm | Proposta sem corte/furação/compra | Tracejado: corpo nominal | Demais peças podem exceder o corpo');c.drawRightString(W-42,29,f'P{i+1:02d} /20');c.showPage()
c.save()

styles=getSampleStyleSheet();styles.add(ParagraphStyle(name='BodyX',fontName='Main',fontSize=9.5,leading=14,spaceAfter=8,textColor=ink));styles.add(ParagraphStyle(name='TitleX',fontName='MainBold',fontSize=24,leading=29,spaceAfter=20,textColor=ink));styles.add(ParagraphStyle(name='HeadX',fontName='MainBold',fontSize=15,leading=20,spaceAfter=12,textColor=ink));styles.add(ParagraphStyle(name='CellX',fontName='Main',fontSize=8,leading=11,textColor=ink))
P=lambda t:Paragraph(t.replace('→',' para ').replace('−','-').replace('–','-'),styles['BodyX'])
def tbl(headers,rows,widths):
 data=[[Paragraph(html.escape(str(v)),styles['CellX']) for v in r] for r in [headers]+rows]
 t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT');t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),light),('VALIGN',(0,0),(-1,-1),'TOP'),('GRID',(0,0),(-1,-1),.3,colors.HexColor('#BBC8BF')),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]));return t
story=[Paragraph('Guedala Park<br/>Caderno técnico documental R28',styles['TitleX']),P('Ferragens, referências de posição, sequências e conferência documental. 14/10/2026.'),P('<b>Status:</b> detalhamento da solução de estudo preservada; não libera corte, furação, compra ou fabricação. As instruções de montagem são um roteiro condicionado à seleção e ao dimensionamento reais.'),P('<b>Base:</b> R28, cozinha à esquerda ao entrar, alternância das portas, canto simples, nove gavetas comuns, bandejas455 e programa do banco preservados. Não foram adicionados mecanismos complexos.'),P('<b>Separação necessária:</b> referência oficial identifica produto/documento; aplicação proposta identifica como ele foi usado no CAD; gabarito representa espaço sem comprovar a peça real. Nenhum desses estados substitui levantamento físico, carga ou fixação.'),P('Conteúdo: lista consolidada de15linhas;54centros de referência de calços; dez sequências de planejamento/uso/manutenção; nove pontos de reconciliação documental; matriz de20módulos e fontes.'),P('Arquivos CSV permitem localizar os objetos sem contar referências duplicadas. As pranchas têm774sólidos de módulos; os925sólidos do inventário geral também incluem arquitetura/objetos independentes. As duas contagens têm escopos diferentes.'),PageBreak()]
for start,end in [(0,8),(8,15)]:
 story.extend([Paragraph('1. Ferragens consolidadas'+(' - continuação' if start else ''),styles['HeadX']),P('Quantidades da montagem candidata, sem liberação de compra. Conjuntos contados uma única vez; não por número de corpos STEP.'),tbl(['ID / referência','Quantidade / aplicação','Estado e limite'],[[h[0]+' / '+h[1],h[2]+'; '+h[3],h[4]+'. '+h[5]] for h in hardware[start:end]],[142,150,219]),PageBreak()])
for start in [0,18,36]:
 story.extend([Paragraph('2. Referências de posição dos calços'+(' - continuação' if start else ''),styles['HeadX']),P('XYZ em mm. Xfrontal espelhado; Y e Z locais. No canto, Ylocal vai de-1050 a0. Centros de envoltórias dos calços: <b>não são coordenadas de furação ou eixos de caneco.</b>'),tbl(['Prancha / marcador','Objeto','X / Y / Z'],[[r[0]+' '+r[2],r[3],f'{r[5]:.1f} / {r[6]:.1f} / {r[7]:.1f}'] for r in coords[start:start+18]],[100,225,186]),PageBreak()])
story.extend([Paragraph('3. Sequências simples',styles['HeadX']),P('Rotina preservada e operações propostas no CAD. Não há intertravamento físico/software. Instalações e fixações não devem ser executadas por gabaritos de volume.')])
for title,steps,source in sequences:
 story.append(Paragraph(title,styles['HeadX']))
 for j,step in enumerate(steps):story.append(P(f'<b>{j+1}.</b> '+html.escape(step)))
 story.extend([P('<b>Base e limite:</b> '+html.escape(source)),PageBreak()])
story.extend([Paragraph('4. Conferência documental',styles['HeadX']),P('As correções abaixo reconciliam a documentação com a revisão atual. Não representam novas alterações geométricas ou nova aprovação de movimentos.'),tbl(['ID / tema','Divergência ou risco','Tratamento vigente'],[[a[0]+' '+a[1],a[2],a[3]] for a in audit],[105,195,211]),PageBreak(),Paragraph('5. Matriz dos 20 módulos',styles['HeadX']),tbl(['Prancha / módulo','Corpo C x P x A (mm)','Limite de compatibilização'],[[f'P{i+1:02d} {names[i]}',' x '.join(f'{m["body_dimensions_mm"][k]:g}' for k in ['Comprimento','Profundidade','Altura']),notes[i]] for i,m in enumerate(d['modules'])],[120,105,286]),PageBreak(),Paragraph('6. Fontes e rastreabilidade',styles['HeadX']),P('Caminhos abaixo são relativos a01_Projeto/Modelo_FreeCAD. Cada montagem contém referências aos documentos oficiais e aos arquivos STEP usados. As revisões anteriores foram preservadas como histórico, não substituem a R28.')])
for f in sorted(set(source_by_module+['Consistencia_controles_R28_2026-10-14/Guia_controles_vigentes_R28.md','Manutencao_R26_2026-10-14/README.md','Cargas_gavetas_R28_2026-10-14/Cargas_gavetas_R28.html','Revisao_solicitada_R28_2026-10-14/Relatorio_revisao_R28.html'])):story.append(P(html.escape(f)))
story.extend([P('<b>Arquivo canônico:</b> Folga_teto_R28_2026-10-14/Guedala_Park_R28_Folga_Teto_Proposta.FCStd'),P('<b>SHA-256:</b> '+d['sha256']),P('Execução desta entrega: leitura e projeção documental; sem salvar/reabrir oCAD, movimentar controles, reparentar objetos ou repetir varreduras. Ferragens de fabricação e instalação não foram escolhidas por inferência.'),P('Revisão final Astra solicitada anteriormente permaneceu não verificada; o agendamento foi encerrado às19h. Este caderno foi produzido por novo pedido de Elias e não reinicia esse agendamento nem comprova a execução da revisão reservada.')])
def footer(c,doc):
 c.setFont('Main',8);c.setFillColor(gray);c.drawString(42,26,'Guedala Park | R28 | Compatibilização documental | Sem liberação executiva');c.drawRightString(A4[0]-42,26,str(doc.page))
pdf2=out/'Guedala_R28_Ferragens_sequencias_conferencia.pdf'
SimpleDocTemplate(str(pdf2),pagesize=A4,rightMargin=42,leftMargin=42,topMargin=42,bottomMargin=43).build(story,onFirstPage=footer,onLaterPages=footer)

links=[('../../../output/pdf/'+pdf1.name,'Pranchas cotadas dos 20 módulos - PDF A3'),('../../../output/pdf/'+pdf2.name,'Ferragens, sequências e conferência - PDF A4'),('Ferragens_consolidadas_R28.csv','Lista de ferragens - CSV'),('Referencias_calcos_54_R28.csv','54 referências de posição dos calços - CSV'),('Componentes_774_R28.csv','774 componentes dos módulos - CSV'),('Conferencia_documental_R28.csv','Conferência documental - CSV'),('Sequencias_R28.json','Sequências estruturadas - JSON'),('../Revisao_solicitada_R28_2026-10-14/Relatorio_revisao_R28.html','Relatório geral com oito vistas'),('../Cargas_gavetas_R28_2026-10-14/Cargas_gavetas_R28.html','Orçamento de massa das gavetas')]
index='<!doctype html><html lang="pt-BR"><meta charset="utf-8"><title>Guedala Park - detalhamento R28</title><style>body{font:17px/1.6 system-ui;background:#f4f3ef;color:#233d39;max-width:1000px;padding:40px;margin:auto}a{color:#126d66}li{margin:12px 0}h1{line-height:1.2}section{background:white;padding:24px;margin:24px 0;border:1px solid #ccd8d0}</style><h1>Detalhamento documental R28</h1><p>Quatro entregas executadas: pranchas cotadas, lista de ferragens, sequências e conferência documental. Arquivo FreeCAD preservado.</p><section><b>Como ler:</b> cotas de corpo CAD e posições de estudo; referências oficiais não homologam aplicações. H01... indicam centros de envoltórias dos calços, não furos. Não é lista de corte, compra ou fabricação.</section><ul>'+''.join(f'<li><a href="{url}">{label}</a></li>' for url,label in links)+'</ul><section><h2>Conferência final</h2><p>20 módulos; 54 conjuntos de dobradiça/calço; nove pares de corrediças candidatas; 18 travas; 15 linhas consolidadas de ferragens. Sequências incluem as condições de uso do banco, cesto, Loop, banheiro e gavetas. Históricos foram mantidos e divergências de instruções receberam notas de precedência.</p><p>Controles: usar originais do guia vigente. Materiais, carga, fixação, batentes, equipamentos e levantamento físico permanecem pendentes. Não há nova geometria ou automação.</p></section></html>'
(p/'Indice_entregas_R28.html').write_text(index,encoding='utf-8')
manifest={'canonical_sha256':d['sha256'],'modules':20,'module_pieces':len(pieces),'hinge_assemblies':54,'plates':len(coords),'hardware_rows':len(hardware),'sequences':len(sequences),'document_audit_rows':len(audit),'pdfs':[str(pdf1),str(pdf2)],'cad_changed':False}
(p/'Manifesto_entrega.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(manifest,ensure_ascii=False))
