from pathlib import Path
import json,ast,csv,hashlib
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A3,landscape
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
p=Path(__file__).resolve().parent; repo=p.parent.parent
d=json.loads((p/'Base_pranchas_R30.json').read_text(encoding='utf-8'))
old=p.parent/'Modelo_FreeCAD/02_Revisoes_e_estudos/Detalhamento_documental_R28_2026-10-14/gerar_entregas.py'
tree=ast.parse(old.read_text(encoding='utf-8'))
for node in tree.body:
    if isinstance(node,ast.Assign) and isinstance(node.targets[0],ast.Name) and node.targets[0].id in ('names','notes','hardware'):
        globals()[node.targets[0].id]=ast.literal_eval(node.value)
for node in tree.body:
    if isinstance(node,ast.FunctionDef) and node.name in ('wrapdraw','dim','projection'):
        exec(compile(ast.Module(body=[node],type_ignores=[]),str(old),'exec'))
for name,file in [('Main','arial.ttf'),('MainBold','arialbd.ttf')]:pdfmetrics.registerFont(TTFont(name,'C:/Windows/Fonts/'+file))
ink=colors.HexColor('#223D39');teal=colors.HexColor('#287C79');orange=colors.HexColor('#B66A22');gray=colors.HexColor('#6B7475');light=colors.HexColor('#E8EFEB')
notes[0]='R30: quatro gavetas NL500/curso500; recuo10; frentes superiores130. Folga ideal até a cama62 com abertura total; não é passagem. Roupeiro650 externos / zona de roupa550. Portas995x1999, curso965 de estudo. Confirmar puxador, retenção e ferragem comercial.'
notes[3]='R30: juntas4/4/4; larguras439,75 /439,75 /440,25 /440,25. Bordas junto às dobradiças preservadas. Apoios duplos36 e ligações ainda dependem de dimensionamento.'
notes[6]='R30: corpo613; vão577; envelope do forno517 e folgas30/30. Envelope não é corpo de embutimento. Traseira15 e travessa tocando o topo do forno: instalação pendente. Ver corte Q03; não liberar recortes.'
notes[9]='R29/R30: três dobradiças em cada porta (seis neste módulo). Quantidade de estudo sujeita ao peso/acabamento e aplicação comercial. Portas270x1016; K5/recobrimento16/calço0 de estudo.'
notes[13]='R30: rodapé80, base80–98; fundo em U com abertura450x602. Confirmar rigidez e hidráulica. Giro55 e saco removível; pivôs são reservas. Apoios C01–C03 estão na alternativa A01, não incorporados.'
notes[19]='Banco acabado1800x550, topo470; corpo nominal1800x450x400 não inclui todo o encosto/estofado. Quatro tampas; ferragens e carga pendentes. Apoios B01–B04 são alternativa A01, não incorporados. Rotina da folha/almofada ainda proposta.'
hardware[0][2]='56 conjuntos';hardware[0][5]='R30: inclui duas dobradiças adicionais do aéreo C. Confirmar aplicação e carga.'
hardware[1][2]='56 calços';hardware[2][5]='Quantidade comercial depende da configuração e limitadores escolhidos; não adotar os 54 históricos.'
hardware[3][5]='Curso roupeiro500 / cozinha500. Carga inclui caixa, frente e conteúdo; não é capacidade aprovada.'
rooms=['Quarto']*4+['Cozinha']*9+['Lavanderia']*2+['Escritório']*2+['Banheiro']*2+['Sala']
out=repo/'05_Entregas/pdf/Guedala_R30_Pacote_para_orcamento.pdf';out.parent.mkdir(parents=True,exist_ok=True)
c=canvas.Canvas(str(out),pagesize=landscape(A3));W,H=landscape(A3)
c.setTitle('Guedala Park | R30 | Pacote para orçamento preliminar')
pages=[]
def header(code,title,sub='14/10/2026 | Base R30 | Valores a preencher pelo fornecedor'):
    pages.append(code);c.setFillColor(ink);c.setFont('MainBold',25);c.drawString(42,H-53,code+' | '+title)
    c.setFont('Main',11);c.drawString(42,H-78,sub)
def end():
    c.setStrokeColor(light);c.line(42,52,W-42,52);c.setFillColor(gray);c.setFont('Main',9)
    c.drawString(42,32,'R30 | Orçamento preliminar condicionado | Cotas em mm | Sem liberação de fabricação')
    c.drawRightString(W-42,32,str(len(pages)));c.showPage()
def para(t,y,size=12):return wrapdraw(c,t,48,y,W-96,size,size*1.5)-12
def table(headers,rows,widths,y,step=29):
    x=48;c.setFillColor(light);c.rect(x,y-step,sum(widths),step,fill=1,stroke=0)
    for text,w in zip(headers,widths):c.setFillColor(ink);c.setFont('MainBold',10);c.drawString(x+7,y-step+10,text);x+=w
    y-=step
    for row in rows:
        x=48
        for text,w in zip(row,widths):
            wrapdraw(c,str(text),x+7,y-13,w-14,9,11);c.setStrokeColor(light);c.rect(x,y-step,w,step);x+=w
        y-=step
    return y
header('Q00','Guedala Park — orçamento da marcenaria')
y=para('Base para propostas comparáveis dos 20 módulos, complementos e instalação. A geometria foi consultada no FreeCAD R30; nenhuma peça do apartamento foi alterada. Preços e condições comerciais permanecem em branco.',H-125,16)
y=para('Escopo-base: P01–P20 e complementos C01–C06 descritos na Q02. Alternativa A01: sete apoios do estudo construtivo, cotados separadamente. Propostas devem declarar material, acabamento, ferragens, premissas e exclusões; não converter dimensões de corpo em lista de corte.',y)
y=para('Leitura das pranchas: frontal espelhada, planta e lateral em coordenadas locais; linhas cinza mostram projeções transparentes das peças, inclusive arestas internas. Tracejado indica corpo nominal; laranja, reservas. Ferragens não são desenhadas neste pacote. As vistas laterais dos módulos não são cortes executivos.',y)
y=para('Fontes e precedência: R30 vigente + correções R29; fechamento de cocção, roteiro de visita e caderno construtivo de 14/10/2026. PDFs R28 permanecem históricos. O estudo dos apoios continua separado, sem nova revisão do apartamento.',y)
table(['Folhas','Conteúdo'],[['Q01–Q02','Escopo por ambiente, complementos e exclusões'],['Q03','Corte esquemático de cocção e condições de orçamento'],['Q04','Alternativa A01 — sete apoios propostos'],['P01–P20','Frontal, planta e lateral dos 20 módulos R30'],['F01–F02','Ferragens de referência — quantidades de estudo'],['Q05','Ficha de resposta e critérios de comparação']],[130,960],y-10,34)
end()
header('Q01','Escopo-base por ambiente')
rows=[]
for i,m in enumerate(d['modules']):
    dimtext=' × '.join(f'{m["body_dimensions_mm"][k]:g}' for k in ('Comprimento','Profundidade','Altura'))
    rows.append([f'P{i+1:02}',rooms[i],names[i],dimtext,'1 conjunto','________'])
table(['Item','Ambiente','Módulo','Corpo L × P × A (mm)','Quantidade','Preço (R$)'],rows,[65,110,295,270,135,215],H-112,28)
para('Valores por conjunto instalado; declarar os itens que não estiverem incluídos. Cotas são do corpo CAD, não dimensões de chapas. Complementos fora destes módulos devem entrar na Q02. Não usar a soma dos envelopes como quantitativo de material.',135,11);end()
header('Q02','Complementos, interfaces e exclusões')
rows=[['C01','Quarto','Painéis de cabeceira, arremates, proteção posterior e fechamentos fora dos quatro corpos. Quantificar na conferência; preço separado.'],['C02','Escritório','Bancada e seus apoios/fixações; arremates fora dos dois módulos. Declarar material, espessura e dimensão orçada.'],['C03','Sala','Mesa/folha800x350x70, encosto, almofadas e acabamento do banco; discriminar o que é marcenaria, estofaria ou fornecimento externo.'],['C04','Todos','Arremates, rodapés, puxadores, bordas, fixações e ferragens auxiliares não listados: declarar quantidades/premissas, sem duplicar P01–P20.'],['C05','Logística','Levantamento, detalhamento executivo, transporte, montagem, proteção e limpeza: informar incluso ou preço separado.'],['C06','Interfaces','Pedras/recortes, cubas/tanque, espelhos, iluminação e instalações: informar fornecedor e responsabilidade; cotar separadamente quando ofertados.']]
table(['Item','Ambiente','Complemento a discriminar'],rows,[65,130,895],H-115,62)
y=para('Fora do preço-base de marcenaria, salvo inclusão expressa e separada: compra de eletrodomésticos, cadeiras, cama/sofá; obras civis; instalação elétrica, gás e hidráulica; pedras e estofaria terceirizadas. O desenho de um objeto não implica fornecimento pelo marceneiro.',300)
y=para('Fechar antes da fabricação: medidas na unidade real, substratos e fixações, chapas/espessuras/acabamentos, pesos e ferragens comerciais, acesso de manutenção e instalação dos equipamentos. O roteiro da visita tem 21 itens ainda sem medidas coletadas.',y)
para('Solicitar proposta com premissas explícitas: preço estimativo agora e revisão discriminada após levantamento. Não considerar o orçamento uma aprovação do projeto executivo.',y);end()
header('Q03','Cocção — corte esquemático para compatibilização')
# Section in Y/Z, normalized to front. Geometry only, no unsupported hardware details.
ox,oy,s=95,190,.49
def rect(y,z,dep,h,color):
    c.setStrokeColor(color);c.setLineWidth(1.2);c.rect(ox+(y-6370)*s,oy+z*s,dep*s,h*s)
rect(6370,50,615,610,gray);rect(6410,900,590,20,teal);rect(6460,920,450,15,orange)
c.setStrokeColor(ink);c.line(ox+630*s,oy,ox+630*s,oy+980*s)
for z,label in [(920,'Bancada: topo920'),(660,'Forno: topo660'),(50,'Envelope: base50')]:
    yy=oy+z*s;c.setFont('Main',10);c.setFillColor(ink);c.drawString(ox+350,yy,label);c.line(ox+310,yy,ox+345,yy)
c.setFont('Main',10);c.drawString(95,165,'Envelope forno: profundidade615 / altura610. Parede de estudo Y7000.')
y=H-130
for text in ['CORTE LATERAL ESQUEMÁTICO — sem escala fixa; não define recortes ou apoios.','Folga traseira do envelope: 15. Fonte arquivada pede50; solução ainda pendente. A travessa toca o topo do forno em660.','d = distância do topo da bancada ao ponto mais baixo instalado do cooktop. Separação nominal até o forno = 260 − d. Para cenário de200: d precisa ser no máximo60. Cota real não confirmada.','Frontal R30: corpo613; vão577; envelope517; folgas30/30. Corpo de embutimento485 é outra referência documental. Não tratar os517 como largura do corpo.','Afastamentos documentais30/50 versus100 permanecem divergentes. Exigir fechamento da instalação e ventilação antes de definir a solução executiva.','Interface lavanderia: lateral avançou13 sob a pedra; LG a67 da lateral e eixos forno/cooktop defasados6,5. Rever emenda, isolamento e acessos.']:
    y=wrapdraw(c,text,660,y,470,12,18)-19
para('Fonte: Cozinha/Fechamento_R30_2026-10-14. O corte detalhado HTML acompanha o pacote; dimensões de equipamentos e manuais são referências arquivadas, sem nova homologação.',115,10);end()
header('Q04','Alternativa A01 — apoios do banco e do cesto')
y=para('Cotar separadamente sete apoios propostos. Não incluídos na geometria R30 nem aprovados para fabricação. Volumes abaixo são envelopes de estudo, sujeitos a material, isolamento, nivelamento, ligações e dimensionamento.',H-115)
support=[['B01','Banco / divisória panelas','18 × 390 × 80'],['B02','Banco / divisória bebidas','18 × 390 × 82'],['B03','Banco / divisória folha','18 × 390 × 82'],['B04','Banco / posterior','1764 × 18 × 18'],['C01','Cesto / lateral','18 × 580 × 98'],['C02','Cesto / lateral','18 × 580 × 98'],['C03','Cesto / posterior','554 × 18 × 80']]
table(['ID','Aplicação','Envelope (mm)','Quantidade','Preço (R$)'],[r+['1','________'] for r in support],[65,365,250,140,270],y,32)
img=p.parent/'Detalhamento_construtivo_R30_2026-10-14/Apoios_propostos.png'
c.drawImage(str(img),60,80,width=540,height=310,preserveAspectRatio=True,anchor='c',mask='auto')
wrapdraw(c,'Laranja: novos apoios. Banco e cesto estão separados para leitura; não é a implantação do apartamento. A conferência geométrica não comprova capacidade. O fornecedor deve apresentar solução de material/ligação e informar o impacto no preço, no acabamento e na manutenção. Não somar a alternativa ao total-base sem aceite.',660,330,450,13,20);end()
for i,m in enumerate(d['modules']):
    C,P,A=[m['body_dimensions_mm'][k] for k in ('Comprimento','Profundidade','Altura')]
    header(f'P{i+1:02}',names[i],f'{rooms[i]} | {m["object"]} | Corpo CAD {C:g} × {P:g} × {A:g} mm | 1 conjunto')
    projection(c,m,'front',48,335,620,365,'FRONTAL — orientação local espelhada')
    projection(c,m,'top',48,85,620,220,'PLANTA LOCAL')
    projection(c,m,'side',715,335,415,365,'LATERAL LOCAL — projeção sem corte')
    y=wrapdraw(c,notes[i],715,305,415,12,18)-12
    fronts=[]
    for dr in d['doors']:
        if dr['module']==m['object']:
            q=next(v for v in m['pieces'] if v['object']==dr['front']);z=q['local_bbox'];fronts.append(f'{z[3]-z[0]:g} × {z[5]-z[2]:g}')
    if fronts:y=wrapdraw(c,'Frentes fechadas L × A (mm): '+', '.join(fronts)+'.',715,y,415,10,15)-10
    wrapdraw(c,'Orçar corpo, frentes, divisões e ferragens aplicáveis; declarar acabamento, puxadores e instalação. As linhas internas não indicam usinagem. Conferir dimensões de campo e detalhar ligações antes da fabricação.',715,y,415,10,15)
    end()
for page,group in enumerate((hardware[:8],hardware[8:]),1):
    header(f'F{page:02}','Ferragens e mecanismos — referência para cotação')
    rows=[[r[0],r[1],r[2],r[3],r[5]] for r in group]
    table(['ID','Referência / família','Quantidade de estudo','Aplicação','Condição / premissa'],rows,[45,190,200,210,445],H-115,67)
    para('Não é lista de compra. Declarar códigos comerciais completos, acessórios inclusos, capacidades e alternativas equivalentes para análise. Quantidades indefinidas devem vir com premissa; não preencher com zero nem esconder no total.',120,11);end()
header('Q05','Resposta do fornecedor e comparação')
y=para('Fornecedor: __________________________________  Contato: __________________________  Data: ______________',H-120)
y=table(['Parcela','Valor (R$)','Premissa / inclusão'],[['P01–P20: soma módulos','____________','Valores individuais na Q01'],['C01–C04: complementos','____________','Detalhar quantidades e materiais'],['C05: logística e montagem','____________','Declarar se já inclusa nos módulos'],['C06: interfaces terceirizadas','____________','Responsabilidade e valor separados'],['TOTAL-BASE sem duplicidades','____________','Somar apenas parcelas não inclusas em outras'],['A01: alternativa sete apoios','____________','Separada do total-base']],[410,180,500],y,36)
for t in ['Material/chapa, espessuras, acabamento interno/externo e bordas: ________________________________________________________','Ferragens, puxadores, códigos comerciais e substituições: ______________________________________________________________','Prazo após medição/aprovação: __________________  Montagem: __________________  Validade da proposta: __________________','Pagamento e tributos: _________________________________  Garantia e assistência: _____________________________________','Exclusões, pendências e gatilhos de revisão do valor: __________________________________________________________________']:
    y=para(t,y-15,11)
para('Comparar pelo mesmo escopo: verificar itens faltantes, material, ferragens, montagem, responsabilidades e alternativa A01 antes de comparar o total. Nenhum preço foi estimado ou fornecedor contatado neste pacote.',y-5,11);end()
c.save()
with (p/'Mapa_de_cotacao_R30.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f,delimiter=';');w.writerow(['Item','Ambiente','Descricao','Quantidade','Unidade','Preco_R$','Premissas'])
    for i,n in enumerate(names):w.writerow([f'P{i+1:02}',rooms[i],n,1,'conjunto','',''])
    for code,desc in [('C01','Complementos quarto'),('C02','Bancada escritorio'),('C03','Mesa encosto estofados'),('C04','Arremates e auxiliares'),('C05','Logistica montagem'),('C06','Interfaces terceirizadas'),('A01','Alternativa sete apoios')]:w.writerow([code,'',desc,'','a discriminar','',''])
(p/'Manifesto.json').write_text(json.dumps({'source_sha256':d['sha256'],'pdf':str(out),'pages':pages,'modules':20,'alternative_supports':7,'cad_unchanged':hashlib.sha256(Path(d['file']).read_bytes()).hexdigest()==d['sha256'],'hardware_assemblies_reference':56},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'pdf':str(out),'pages':len(pages)},ensure_ascii=False))
