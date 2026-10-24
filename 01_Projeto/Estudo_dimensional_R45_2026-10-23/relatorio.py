import pathlib,json,hashlib,shutil,html
from PIL import Image, ImageDraw, ImageFont
ROOT=pathlib.Path('C:/Users/Elias/Documents/PROJETOS/Guedala park')
P=ROOT/'guedala-park/01_Projeto'
OUT=P/'Estudo_dimensional_R45_2026-10-23'
d=json.loads((OUT/'Calculos_e_ensaios.json').read_text(encoding='utf8'))
FONT='C:/Windows/Fonts/segoeui.ttf'
def canvas(title):
 im=Image.new('RGB',(1500,850),'#faf9f6');dr=ImageDraw.Draw(im)
 dr.text((55,30),title,font=ImageFont.truetype(FONT,32),fill='#24322f')
 return im,dr
def text(dr,xy,t,size=22,color='#24322f'):
 dr.multiline_text(xy,t,font=ImageFont.truetype(FONT,size),fill=color,spacing=7)
im,dr=canvas('Banco | corte nominal no setor da tampa de 825 mm')
def pt(x,z):return (100+(x-70)*1.65,760-(z-70)*1.65)
def rect(x,z,w,h,color):
 a=pt(x,z+h);b=pt(x+w,z);dr.rectangle([a,b],fill=color,outline='#333',width=2)
rect(100,70,18,330,'#a18b6b');rect(530,70,18,330,'#a18b6b')
rect(102,400,448,20,'#79583c');rect(140,292,372,18,'#a18b6b');rect(160,110,350,164,'#b7c8bd')
text(dr,pt(185,210),'Reserva do aspirador / jogos\ntopo Z = 274 mm',21)
text(dr,pt(195,438),'Tampa 825 × 448 × 20 mm',23)
text(dr,pt(245,306),'Prateleira 18 mm',18)
def arrow(x,z1,z2,label,color,dx=10):
 a,b=pt(x,z1),pt(x,z2);dr.line([a,b],fill=color,width=3)
 for yy,sign in [(a[1],1),(b[1],-1)]:dr.line([(a[0]-7,yy+sign*10),(a[0],yy),(a[0]+7,yy+sign*10)],fill=color,width=3)
 text(dr,(a[0]+dx,(a[1]+b[1])/2-23),label,22,color)
arrow(440,400,310,'90 mm\nlivres','#157464')
arrow(290,400,270,'130 mm\nmanual','#b54a2b',-125)
a,b=pt(140,270),pt(512,252);dr.rectangle([a,b],outline='#b54a2b',width=3)
text(dr,(975,480),'Baixar 40 mm:\ninvade 22 mm do\ngabarito abaixo.',23,'#b54a2b')
dr.line([(960,525),pt(480,260)],fill='#b54a2b',width=2)
text(dr,(55,790),'Comparação de cotas. A seta de 130 mm não representa o corpo da ferragem. Nenhuma peça foi alterada.',19,'#555')
im.save(OUT/'Banco_corte.png')
im,dr=canvas('Tampas | massa calculada somente da chapa, sem almofadas')
def chartpt(x,y):return (140+(x-650)/250*1130,700-(y-4.5)/4*520)
for y in [5,6,7,8]:
 a=chartpt(650,y);b=chartpt(900,y);dr.line([a,b],fill='#d5d8d5',width=2);text(dr,(75,a[1]-15),str(y)+' kg',19)
for x in [650,750,800,900]:text(dr,(chartpt(x,4.5)[0]-25,720),str(x),20)
a,b=chartpt(650,7),chartpt(900,7);dr.line([a,b],fill='#b54a2b',width=3)
text(dr,(150,a[1]-30),'7 kg: limite da tabela / 2 articuladores',18,'#b54a2b')
for lid,col in zip(d['bank'],['#157464','#ab5936']):
 pts=[chartpt(v['density_kg_m3'],v['panel_kg']) for v in lid['mass_scenarios']];dr.line(pts,fill=col,width=4)
 for v,point in zip(lid['mass_scenarios'],pts):
  x,y=point;dr.ellipse((x-6,y-6,x+6,y+6),fill=col);text(dr,(x+12 if v['density_kg_m3']==650 else x-35,y-35),f"{v['panel_kg']:.2f} kg",19,col)
text(dr,(140,110),'971 × 448 × 20 mm',23,'#157464');text(dr,(520,110),'825 × 448 × 20 mm',23,'#ab5936')
text(dr,(420,755),'Densidade hipotética da chapa (kg/m³)',22)
text(dr,(55,805),'Cenários, não pesagens. Somar acabamento e acessórios móveis. Não é cálculo de resistência do assento.',19,'#555')
im.save(OUT/'Banco_massas.png')
md='''# Estudo dimensional R45 — gavetas e tampas do banco

23/10/2026. Estudo separado da R44, que permanece vigente e preservada. Nenhuma medida real do apartamento foi presumida. O modelo de estudo contém 129 objetos; a geometria copiada serve à análise, não à fabricação.

## Resultado principal

- **Gavetas:** sete têm profundidade nominal suficiente para a família FGVTN escolhida; as duas do escritório continuam 8 mm aquém na R44. A variante R04 oferece 432 mm livres, 12 mm além do mínimo de 420. Encaixe real de perfis/engates ainda não fechado.
- **Tampas:** 182 posições nominais (0–90°, passo 1°, duas tampas) sem interseção volumétrica acima de 0,1 mm³ contra o contexto copiado do banco e a outra tampa fechada, com almofadas removidas. Isso verifica o eixo ideal existente, não a cinemática de dobradiças reais.
- **Banco / ferragem:** a tampa menor tem somente 90 mm até a prateleira; o manual Slow Multi pede 130 mm de altura mínima de montagem. Faltam 40 mm nessa região. A tampa maior pode ultrapassar os 7 kg admitidos pela tabela, dependendo da chapa e do acabamento.

## Respostas FGVTN conferidas no Outlook

Busca em 23/10 por FGVTN desde 21/10, sem página adicional. Localizadas duas respostas do SAC em 22/10: às 09:31:34 de São Paulo, envio dos STEP aberta/fechada da 54FGOC12400TSX0; às 09:42:25, informação de que não têm ferragem para o cesto consultado. Metadados dos anexos conferidos. São os mesmos arquivos registrados na R44; nenhum desenho novo dos engates foi localizado nessa busca. Não houve envio de mensagem.

Os anexos não confirmam explicitamente datum de instalação, engates, parafusos, destravamento ou recortes traseiros. O STEP de 400 não foi escalado para representar o de 500 mm. [Registro anterior e fontes](../Modelo_FreeCAD/01_Atual/FGVTN_R44_2026-10-22/Fontes/LEIA-ME.md).

## 1. Gavetas: cotas que já podem ser fechadas como estudo

Recalculadas larguras entre faces internas das laterais e profundidades entre frente da carcaça e face interna do fundo no arquivo R44 aberto. Resultados coincidem com o levantamento anterior.

| Local | Quantidade | Profundidade livre | Mínimo da família | Margem |
|---|---:|---:|---:|---:|
| Roupeiro | 4 | 550 mm | 520 mm | +30 mm |
| Cozinha | 3 | 572 mm | 520 mm | +52 mm |
| Escritório R44 | 2 | 412 mm | 420 mm | −8 mm |
| Escritório variante R04 | 2, alternativa às anteriores | 432 mm | 420 mm | +12 mm |

Pelo desenho Set24, largura interna da caixa = A−41, tolerância +1/−0,5 mm, com lateral até 16 mm. Para laterais de 15 mm, a caixa externa nominal resulta A−11. Isso fornece 5,5 mm de folga por lado quando centrada; na faixa de tolerância de largura, 5 a 5,75 mm por lado. Não é folga do engate nem tolerância liberada para cada peça isoladamente.

| Local | Vão A | Largura interna nominal | Faixa documental | Largura externa com laterais 15 |
|---|---:|---:|---:|---:|
| Roupeiro | 355 | 314 | 313,5–315 | 344 |
| Cozinha | 583 | 542 | 541,5–543 | 572 |
| Escritório | 364 | 323 | 322,5–324 | 353 |

Dimensões em mm. As sete gavetas de 500 mm foram conferidas quanto a essas cotas; não receberam perfis/engates novos nem ensaio mecânico equivalente ao de 400 mm.

### Escritório: capacidade e tolerâncias

A variante R04 mantém base útil 323 × 364 mm, altura de conteúdo 60,4 mm na inferior e 54 mm na superior: 7,101 L e 6,349 L. São prismas de referência, não volumes certificados de carga. Repetido o ensaio conservador dos volumes de conteúdo ao longo de 0–378 mm e regulagem 0–3 mm, contra carcaça e envelopes da outra gaveta: nenhuma interseção acima de 0,01 mm³. O relatório R04 anterior contém o ensaio das madeiras e fixações; nesta etapa não se declara que o perfil real passou nesse ensaio.

As folgas verticais mínimas do conteúdo são apenas 1,6 e 1 mm. Num exemplo de acúmulo desfavorável de dois erros de 0,5 mm, restariam 0,6 e 0 mm. Com três erros de 0,5 mm, restariam 0,1 e −0,5 mm. Esses valores ilustram o orçamento de tolerâncias; não são tolerâncias industriais assumidas. A montagem precisa ter margem definida pelo fabricante/marceneiro antes de fechar altura das caixas e furação.

### Corrediça recebida: o que foi efetivamente testado

Reproduzida a hipótese rejeitada na R44: plano Y=0 do STEP junto à lateral X=4318, extremidade Z=148,5 da base em Y=676 e face X=30,6 do perfil móvel sob o fundo. O curso do estágio móvel é 374,3 mm e o intermediário 256,35 mm, extraídos dos arquivos recebidos. Usada somente a lateral fornecida.

Foram feitos **24 casos**: duas gavetas × fechado/aberto × rebaixamentos de 0, 1, 2, 5, 10 e 12 mm do perfil, mantendo as caixas. Todos mantêm ao menos uma interferência. Abaixar o perfil também perde a hipótese de apoio no fundo; esse ensaio é diagnóstico de sensibilidade, não uma proposta de montagem. Não é possível concluir incompatibilidade geral da ferragem a partir dessa orientação ainda não confirmada.

**Conclusão:** não recortar a madeira para acomodar essa posição por tentativa. Próximo dado necessário é o datum correto do conjunto e o desenho dos engates/recortes. A caixa R04 continua alternativa dimensional, sem incorporação como solução mecânica concluída.

## 2. Banco: abertura e implantação

Mantidas duas tampas de 971 × 448 × 20 e 825 × 448 × 20 mm, junta longitudinal de 2 mm sobre a divisória de 18 mm. Apoio geométrico nominal na divisória: 8 mm para cada tampa; isso não é cálculo de pressão ou resistência. Folga nominal ao encosto: 2 mm. Ambas alcançam Z=868 mm abertas a 90°, a partir do eixo ideal em Z=420 mm.

O ensaio amostral de 1° não encontrou colisões no contexto do banco. Não cobre pessoas, mãos, ferragens ausentes nem certifica todos os ângulos intermediários. A junta de 2 mm e o recuo de 2 mm devem receber tolerâncias de execução, acabamento e deformação.

### Slow Multi: quantidade condicional e massa

O manual arquivado indica um articulador até largura de 700 mm/peso 3,5 kg e dois até 1.400 mm/7 kg, com 210 < H < 500 mm. As duas tampas têm largura acima de 700 e profundidade H=448; a hipótese é **dois por tampa, quatro no total**, condicionada à massa acabada e à montagem. Não há aprovação de quatro peças para compra.

| Densidade hipotética | Tampa 971 mm | Margem até 7 kg | Tampa 825 mm | Margem até 7 kg |
|---|---:|---:|---:|---:|
| 650 kg/m³ | 5,655 kg | 1,345 kg | 4,805 kg | 2,195 kg |
| 750 kg/m³ | 6,525 kg | 0,475 kg | 5,544 kg | 1,456 kg |
| 800 kg/m³ | 6,960 kg | 0,040 kg | 5,914 kg | 1,086 kg |
| 900 kg/m³ | 7,830 kg | excede 0,830 kg | 6,653 kg | 0,347 kg |

Massa = volume CAD × densidade. A chapa maior sozinha chega a 7 kg em aproximadamente 804,6 kg/m³; a menor, em 947,0 kg/m³. Somar acabamento e acessórios que se movam com a tampa. As almofadas devem ser retiradas. Não afinar a chapa apenas para entrar na tabela: o dimensionamento do assento é independente e não foi realizado aqui.

### Altura de montagem versus armazenamento

Na tampa de 825 mm, a face inferior da tampa está em Z=400 e a prateleira em Z=310: apenas 90 mm. A altura mínima indicada no manual é 130 mm. Uma simples descida da prateleira em 40 mm colocaria sua face inferior em Z=252, cruzando 22 mm dos gabaritos do aspirador/jogos, que chegam a Z=274. **Essa alternativa foi rejeitada; nada foi movido.**

O fechamento deverá comparar um articulador com instalação que caiba no espaço disponível ou um detalhe local da prateleira que preserve armazenamento e resistência. Um recorte não está dimensionado nem aprovado nesta etapa, pois falta o envelope completo da ferragem. Sob a tampa maior também há objetos próximos às laterais: no setor dos potes, a reserva começa 10 mm após a face interna da lateral, enquanto a linha de referência da fixação superior fica 12 mm para dentro. Há conflito potencial de ocupação, a confirmar com o corpo real do mecanismo, não demonstrado como colisão de ferragem inexistente.

### Referências de montagem marcadas no estudo

Aplicadas somente como marcações de estudo as cotas do desenho: eixo lateral a 40 mm do topo e 60 mm da face interna do fundo; furos laterais a 26/54 mm do topo (28 mm entre centros); indicação superior 188/204 mm desde a borda traseira assumida da tampa, em plano a 12 mm da face interna lateral. Recobrimento r e dobradiça real ainda precisam compatibilização. Marcadores não perfuram as peças.

Por causa da divisória compartilhada, a distância da borda da tampa à linha de montagem não é igual nas duas pontas: 29/20 mm na tampa de 971 e 20/29 mm na de 825. Não copiar automaticamente E+12 = 30 mm a partir de todas as bordas da tampa; o desenho deve ser referenciado às faces reais da carcaça e à dobradiça escolhida.

## Entregas e limites

- [Modelo separado no FreeCAD](Gavetas_Banco_R45_ESTUDO.FCStd).
- [Cálculos, coordenadas e ensaios](Calculos_e_ensaios.json).
- [Corte do banco](Banco_corte.png) e [cenários de massa](Banco_massas.png).
- [Verificação de salvamento e preservação](Verificacao.json).

O arquivo abre no setor Banco. Para inspecionar as gavetas, oculte o grupo 01 — BANCO e exiba 02 — GAVETAS; ajuste a vista ao conteúdo. No modelo, grupos de hipóteses rejeitadas da corrediça, referências Slow Multi e tampas a 90° começam ocultos. Exibir separadamente. O grupo de caixas representa a variante R04, não as gavetas instaladas da R44. O estudo mantém coordenadas globais do apartamento.

Não houve fabricação, compra, redução do armazenamento, alteração do arquivo R44 ou contato com fornecedores. Faltam dados de produto e fabricação, além da conferência de campo futura; esses grupos de dependências não foram confundidos.

## Fontes locais

- R44 consolidada, R04 das gavetas e STEP oficiais recebidos em 22/10 (hashes registrados nos cálculos e na pasta de fontes R44).
- [FGVTN Oculta ET — instrução Set24](../Avanco_pendencias_2026-10-21/Ferragens/FGVTN_Oculta_ET_montagem_Set24.pdf), página única, inspecionada visualmente.
- [FGVTN Slow Multi — montagem](../Modelo_FreeCAD/01_Atual/Ferragens_R38_2026-10-20/Fontes/FGVTN_Slow_Multi_Montagem.pdf), página única, inspecionada visualmente. Documento de referência arquivado; não implica confirmação comercial atual.
'''
(OUT/'README.md').write_text(md,encoding='utf8')
try:
 import markdown
 body=markdown.markdown(md,extensions=['tables'])
except ImportError:
 import re
 def inline(t):
  t=html.escape(t)
  t=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',t)
  t=re.sub(r'\[([^]]+)\]\(([^)]+)\)',r'<a href="\2">\1</a>',t)
  return t
 parts=[];lines=md.splitlines();i=0
 while i<len(lines):
  line=lines[i].strip()
  if not line:i+=1;continue
  if line.startswith('|'):
   rows=[]
   while i<len(lines) and lines[i].strip().startswith('|'):
    row=lines[i].strip();i+=1
    if set(row.replace('|','').replace(':','').replace(' ',''))=={'-'}:continue
    cells=[x.strip() for x in row.strip('|').split('|')];tag='th' if not rows else 'td'
    rows.append('<tr>'+''.join('<'+tag+'>'+inline(x)+'</'+tag+'>' for x in cells)+'</tr>')
   parts.append('<table>'+''.join(rows)+'</table>');continue
  if line.startswith('#'):
   n=len(line)-len(line.lstrip('#'));parts.append(f'<h{n}>'+inline(line[n:].strip())+f'</h{n}>')
  elif line.startswith('- '):
   items=[]
   while i<len(lines) and lines[i].startswith('- '):items.append('<li>'+inline(lines[i][2:])+'</li>');i+=1
   parts.append('<ul>'+''.join(items)+'</ul>');continue
  else:parts.append('<p>'+inline(line)+'</p>')
  i+=1
 body=''.join(parts)
body=body.replace('<h2>1. Gavetas', '<h2>1. Gavetas')
body=body.replace('<h2>2. Banco:', '<img src="Banco_corte.png" alt="Corte do banco"/><h2>2. Banco:')
body=body.replace('<h3>Altura de montagem', '<img src="Banco_massas.png" alt="Cenários de massa"/><h3>Altura de montagem')
page='''<!doctype html><html lang="pt-br"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>R45 · Estudo dimensional</title><style>body{font:16px/1.6 system-ui,sans-serif;color:#24322f;background:#f5f4ef;margin:0}main{max-width:1000px;margin:auto;padding:50px 40px;background:white}h1{font-size:34px;line-height:1.2}h2{margin-top:44px;border-top:2px solid #c9d6cf;padding-top:22px}h3{margin-top:28px}table{border-collapse:collapse;width:100%;font-size:14px;margin:20px 0}th,td{padding:9px 12px;border-bottom:1px solid #d9dfdb;text-align:left}th{background:#e9efeb}a{color:#17685c}img{max-width:100%;margin-top:30px}strong{color:#1b5147}pre{font:15px/1.6 system-ui}@media print{main{padding:0}h2,h3{break-after:avoid}tr,img{break-inside:avoid}}</style><main>'''+body+'</main></html>'
(OUT/'Relatorio.html').write_text(page,encoding='utf8')
for name in ['estudar.py','inspecionar.py','relatorio.py']:
 shutil.copyfile(ROOT/'outputs/estudo-dimensional-2026-10-23'/name,OUT/name)
print(OUT)
