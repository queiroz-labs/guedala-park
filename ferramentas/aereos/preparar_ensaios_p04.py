"""Pacote de preparacao para marcenaria/laboratorio. Nao executa ensaios."""
from pathlib import Path
import csv,functools,hashlib,json,math
import numpy as np
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.graphics.shapes import Drawing,Rect,Line,Circle,String
from fontes import sha,HASH_RULE

ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'04_Moveis/Aereos_suspensao'
def read(p):return json.loads(p.read_text(encoding='utf8'))
def csvwrite(path,rows):
    with path.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter=';');w.writeheader();w.writerows(rows)

def main():
    g=read(OUT/'Lote_B_geometria.json');b=read(OUT/'Lote_B_detalhamento.json');v=read(OUT/'P04_validacao.json')
    release=read(ROOT/'ferramentas/site/current_release.json');assert sha(ROOT/release['cadPath'])==v['cad_sha256']
    m=next(m for m in g['modules'] if m['code']=='P04');full=next(x for x in m['variants'] if x['preferred_for_study'])
    sources=['Peca267','Peca269','Peca270','Peca268','ApoioOpostoR002'];labels=['Lateral esquerda','Base','Tampo','Fundo inteiro','Divisor junto a lateral']
    cuts=[]
    for i,(name,label) in enumerate(zip(sources,labels)):
        box=np.array(full['boxes_uvz_mm'][name]);box[3]=min(box[3],200)
        dims=box[3:]-box[:3];thickness=int(np.argmin(dims));sizes=[float(dims[k]) for k in range(3) if k!=thickness]
        cuts.append(dict(id=f'T0-{i+1}',source_CAD=name,piece=label,qty=1,finished_A_mm=max(sizes),finished_B_mm=min(sizes),
            nominal_thickness_mm=float(dims[thickness]),box_uvz_mm=box.tolist(),
            scope='Retalho geometricoT0,nao peca para fabricar o armario ou ensaio de resistencia'))
    joints=[r for r in b['joints'] if r['code']=='P04' and r['a'] in ['Peca267','ApoioOpostoR002']]
    assert len(joints)==8
    critical=[r for r in joints if r['a']=='Peca267'];assert len(critical)==4
    plate=[h for h in v['static_hardware'] if h['box_uvz_mm'][3]<200];assert len(plate)==2
    bom=[dict(item='Minifix 15 - 262.26.034',qty_T0=8,purpose='Canecos das 8 juntas locais; não são compra adicional do P04.'),
        dict(item='Pino B34 - 262.28.920',qty_T0=8,purpose='Conferir produto, rosca e gabarito na chapa real.'),
        dict(item='Calço 173H7100',qty_T0=2,purpose='Calços fixos esquerdos nas posições R52; sem portas no T0.'),
        dict(item='Allen SW4 - Wera 950 PKS 05133154001',qty_T0=1,purpose='Braços 80 x 22 mm; usar braço curto reto.'),
        dict(item='Bigfer 04.02.058 candidata',qty_T0=1,purpose='Conferência geométrica esquerda, sem carga; método/fixadores pendentes.')]
    registry=[]
    def blank(id,stage,case='',side='',V='',T=''):
        registry.append(dict(id=id,stage=stage,replica='',case_id=case,side=side,service_V_target_N=V,service_T_target_N=T,
            specimen_lot='',measured_thickness_mm='',actual_hardware='',actual_tool='',process_pilot_torque='',
            applied_V_N='',applied_T_N='',relative_displacement_mm='',device_displacement_mm='',min_clearance_mm='',
            damage_or_contact='',recovery_mm='',time_temperature_humidity='',evidence_file='',laboratory_id='',
            result='',status='NAO_EXECUTADO'))
    for r in critical:blank(r['id'],'T0_acesso')
    for code in ['axial_base_divisor','axial_topo_divisor','cortante_horizontal_lateral','grupo_traseiro']:
        blank('T1_'+code,'T1_juntas')
    for i,r in enumerate(v['qualification_cases']):blank(f'T2_{i+1}','T2_suporte',r['case_id'],r['side'],r['V_N'],r['T_N'])
    blank('T3_caixa_completa','T3_conjunto')
    result=dict(scope='Preparacao para marcenaria/laboratorio,sem ensaio fisico ou compra.',
        authorization='Elias,25/10/2026:"Preparar para marcenaria/laboratório".',
        cad_sha256=v['cad_sha256'],cad_opened=False,cad_changed=False,physical_tests_executed=0,
        T0_external_mm=[218,230,308],T0_crop_internal_u_mm=[0,200],T0_internal_height_mm=272,T0_gap_side_divider_mm=7,
        T0_cut_list=cuts,T0_joints=joints,T0_critical_access_ids=[r['id'] for r in critical],T0_fixed_calcos=plate,T0_bom=bom,
        T0_assembly=['Montar base/divisor/tampo com os4pinos verticais;fechar topo emz.',
            'Aproximar lateral pela direcaou,encaixando simultaneamente4pinos horizontais.',
            'Apertar4canecos junto a lateral comSW4 curta,com divisor ja montado.',
            'Posicionar fundo/calcos/suporte candidato e repetir acesso/reencaixe/retirada,sem carga.',
            'Fixacao temporaria do dispositivo fora da regiao validada,sem inventar cavilhas ou furos estruturais.'],
        laboratory_to_define=['SKU/lote/espessura real e acabamento de cada chapa;gabarito,pilotos,passagens,escareamento e torque.',
            'Dispositivo e cadeia de forca/deslocamento calibrados;faixas,resolucao/incerteza e correcao da deformacao do aparelho.',
            'Numero de corpos/repeticoes,incrementos,tempos/ciclos,criterios e fatores do protocolo de resistencia aplicavel.',
            'Metodo Bigfer no fundo18/divisor18,retencao e fixadores;centro/area reais dos apoios inferiores antes de aceitarh160.'],
        limits=['T0e recorte de200mm de largura interna;nao representa flexao da caixa1800 nem capacidade das juntas/suspensao.',
            'Dimensoes finais nominais,nao corte bruto ouCNC;ajustar pela espessura/fita real antes de usinar.',
            'Dados de seis vetores sao servico estatico do estudo,nao cargas normativas de prova;nao transformarN emkg e aplicar separadamente.',
            'Nenhum limite de resistencia/torque/fator foi inventado;lab deve registrar protocolo antes da aplicacao de carga.',
            'Planilha de registro e modelo vazio:replicas e medidas em branco;NAO_EXECUTADO nao significa reprovado.'],
        qualification_cases=v['qualification_cases'],registration_template=registry,hash_rule=HASH_RULE,
        sources_sha256={str(p.relative_to(ROOT)).replace('\\','/'):sha(p) for p in [OUT/'Lote_B_geometria.json',OUT/'Lote_B_detalhamento.json',OUT/'P04_validacao.json',OUT/'P04_fontes_validacao.json']},
        generator_sha256=sha(Path(__file__)),hash_helper_sha256=sha(Path(__file__).with_name('fontes.py')))
    (OUT/'P04_preparacao_ensaios.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    csvwrite(OUT/'P04_retalhos_T0.csv',cuts);csvwrite(OUT/'P04_registro_laboratorio.csv',registry)
    make_pdf(result)
    print(json.dumps(dict(pdf='P04_ensaios_laboratorio.pdf',cut_parts=5,Minifix_T0=8,critical_accesses=4,registration_rows=len(registry),physical_tests_executed=0)))

def make_pdf(d):
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='BodyLab',fontName='Helvetica',fontSize=9.5,leading=13,spaceAfter=7,textColor=colors.HexColor('#293a31')))
    styles.add(ParagraphStyle(name='SmallLab',fontName='Helvetica',fontSize=8,leading=10,spaceAfter=5))
    styles['Title'].fontName='Helvetica-Bold';styles['Title'].fontSize=23;styles['Title'].leading=27
    styles['Heading2'].textColor=colors.HexColor('#345e4d');styles['Heading2'].fontSize=13;styles['Heading2'].spaceBefore=10
    def p(s,small=False):return Paragraph(s,styles['SmallLab' if small else 'BodyLab'])
    def h(s):return Paragraph(s,styles['Heading2'])
    def title(s):return Paragraph(s,styles['Title'])
    def table(rows,widths):
        cells=[[p(str(c),True) for c in row] for row in rows];t=Table(cells,colWidths=widths,repeatRows=1,hAlign='LEFT')
        t.spaceAfter=8
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e1e9e3')),('VALIGN',(0,0),(-1,-1),'TOP'),
            ('LINEBELOW',(0,0),(-1,0),.8,colors.HexColor('#688474')),('LINEBELOW',(0,1),(-1,-1),.25,colors.HexColor('#ccd3cc')),
            ('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),4)]));return t
    story=[title('P04 | Preparação dos ensaios'),p('Pacote para marcenaria/laboratório - 25/10/2026. Estudo separado da R52. Nenhum ensaio físico executado.'),
        h('Sequência e decisões de passagem'),table([['Etapa','O que conferir','Saída necessária'],
        ['T0 - sem carga','Montagem do canto e quatro acessos com chave curta.','Registro de giro, retirada, folga e contato, sem dano.'],
        ['T1 - juntas','Retenção axial, cortante e grupos traseiros nas chapas reais.','Curvas força-deslocamento e danos/recuperação.'],
        ['T2 - suporte','Suporte no fundo/divisor de 18 mm e fundo/lateral de 18 mm.','V/T simultâneos, retenção e método de montagem.'],
        ['T3 - caixa inteira','Conjunto de 1800 mm com portas, ferragens e conteúdo pesados.','Deformações/contatos e protocolo definido pelo laboratório.']],[82,210,219]),
        p('Executar primeiro o T0. A autorização é para preparar os ensaios; este pacote não define compra, fabricação do móvel ou carga de prova de resistência.'),
        h('Antes de cortar ou aplicar carga'),p('O laboratório deve confirmar substratos/SKUs, espessuras e acabamentos; escolher gabaritos, pilotos, passagens, escareamento e torque pelas ferragens reais. Definir dispositivo, instrumentos, replicação, ciclos/tempos e critérios do protocolo. Não completar essas lacunas por suposição.'),
        h('Conjunto mínimo para o T0'),table([['Material/ferragem','Qtd.','Uso'],*[[r['item'],r['qty_T0'],r['purpose']] for r in d['T0_bom']]],[240,32,239]),
        p('Separar cinco retalhos da página 2. O fundo permanece Branco TX nas duas faces, com fita inferior Arenza. Nas demais peças, manter o material correspondente ao projeto. Substituição de substrato limita o resultado ao acesso geométrico.',True),PageBreak(),
        title('T0 | Retalhos e referências'),p('Unidades: mm. Origem u0 na face interna da lateral; v0 na traseira, crescendo para frente; z0 na base externa. Vistas esquemáticas cotadas, sem escala de impressão.'),
        drawing(d),table([['ID / peça de origem','Dimensões finais A x B x esp.','Qtd.'],
        *[[r['id']+' / '+r['piece']+' ('+r['source_CAD']+')',f"{r['finished_A_mm']:g} x {r['finished_B_mm']:g} x {r['nominal_thickness_mm']:g}",r['qty']] for r in d['T0_cut_list']]],[300,170,41]),
        p('Dimensões acabadas nominais: descontar a fita e ajustar pelo material real antes do corte bruto. O recorte tem largura interna 200 e externa 218, profundidade 230 e altura 308; vão vertical 272. Não usar estes retalhos para demonstrar resistência ou rigidez do armário inteiro.',True),PageBreak(),
        title('T0 | Montagem e registro'),p('Montagem: primeiro base/divisor/tampo pelos pinos verticais; depois lateral pelos quatro pinos horizontais. Assim não se exige fechar eixos u e z por uma única translação. Não instalar portas no T0.'),
        h('Oito conectores locais - coordenadas de conferência'),
        table([['Peças','Caneco:face u/v/z','Interface do pino u/v/z'],
        *[[r['a']+' + '+r['b'],' / '.join(f'{x:g}' for x in r['cam_access_uvz_mm']),' / '.join(f'{x:g}' for x in r['interface_uvz_mm'])] for r in d['T0_joints']]],[220,145,146]),
        p('Caneco Ø15, A9, B34 e profundidade 13,5+0,5 são referências candidatas, não programa CNC. A interface acima não é necessariamente a face inicial do piloto. Medir espessuras e usar desenho/gabarito do fabricante.'),
        h('Quatro acessos críticos'),p('São os canecos em u34, v90/158, z18/290. Usar a haste curta reta SW4 da chave 80 x 22. Aplicar cursos de até 60 graus na janela livre, retirar e reencaixar 60 graus; repetir até o travamento conforme fabricante. Não usar a ponta esférica inclinada nem inventar torque.'),
        p('Após montar, posicionar os dois calços fixos esquerdos e conferir o suporte candidato. Calços: caixas nominais u25..33,5, v172,5..214,01, z51,417..108,583 e 199,417..256,583. Suporte esquerdo: envolvente u25..74,5, v18..55,8, z242..258. São obstáculos/modelos do estudo, não gabaritos de instalação.'),
        p('Em cada um dos quatro pontos, registrar: ferramenta/SKU, ângulo disponível, engate, retirada, folga mínima, contato com chapa/calço/suporte e marca no BP. Fotografar. Acesso sem contato forçado/dano e sem furar a face inferior é o objetivo T0; não valida capacidade.'),
        table([['Acesso','Giro / retirada','Folga / contato / evidência'],*[[r['id'],'________________','______________________'] for r in d['T0_joints'] if r['id'] in d['T0_critical_access_ids']]],[235,120,156]),PageBreak(),
        title('T1-T3 | Qualificação e medições'),h('T1 - orientações das juntas'),
        p('Base/divisor e topo/divisor: retenção axial em z, caneco na divisória. Base/lateral e topo/lateral: cortante vertical e retenção, caneco no horizontal. Traseira: grupo completo, cabeça junto à parede e deformação do fundo. Caracterizar acomodação, curva relativa e recuperação descontando o dispositivo.'),
        p('K = 1000 N/mm por junta/posição é requisito hipotético da memória local, não propriedade do Minifix. Os 25,6 N/ponto e 1,523 mm antigos não abrangem automaticamente a nova entrada de carga no divisor esquerdo. Não duplicar rigidez de uma mesma ligação.'),
        h('T2 - seis vetores de serviço para qualificação'),
        table([['Caso / lado','V (N)','T (N)','R (N)','Controle'],
        *[[str(r['case_id'])+' / '+('esq.' if r['side']==0 else 'dir.'),f"{r['V_N']:.2f}",f"{r['T_N']:.2f}",f"{r['R_N']:.2f}",','.join(r['controls'])] for r in d['qualification_cases']]],[103,68,68,68,204]),
        p('Usar oCSV completo para portas, distribuição do conteúdo, partilha e momentos r x F. Preservar V/T simultâneos de cada linha; não combinar máximos nem tratar estes vetores como cargas normativas de prova. Fatores, ciclos, repetições e cargas finais devem ser definidos pelo laboratório.'),
        h('T3 - caixa completa e apoio real'),p('Caixa 1800 x 230 x 308, fundo 1764 x 308 x 18; peso estimado máximo 46,21 kg já inclui conteúdo 10 kg, antes das ferragens. Pesar conjunto/portas e registrar CG. Dois suportes são hipótese. Assentos u65,5/1723,5, z250 e compressão hipotética z90 dão braço 160; medir contatos/centro reais e recalcular se mudarem.'),
        p('Registrar deslocamentos da frente/base/fundo/divisor/referência superior, abertura de juntas, retenção e recuperação. O dispositivo rígido do laboratório não demonstra a ancoragem na parede real do imóvel.'),
        h('Ficha e entregas do laboratório'),p('O CSV P04_registro_laboratorio contém 15 linhas-modelo sem medições, todas NAO_EXECUTADO; replicação em branco não significa um único corpo. Preencher material/lote, ferragens, processo, instrumentos/calibração, forças aplicadas, deformações, danos, tempo/ambiente, evidências e conclusão por etapa.'),
        p('Entregar: protocolo adotado, desenhos da montagem/dispositivo, curvas brutas, fotos, critérios de interpretação e limitações. Encaminhar dúvidas de produto antes da carga. Este pacote não foi enviado a terceiros.'),
        p('Fontes: geometria e cálculos locais R52; <link href="https://www.hafele.com.de/en/product/connector-housing-haefele-minifix-15-zinc-alloy-without-rim/26226034/" color="#345e4d">Häfele Minifix</link>; <link href="https://www.hafele.com/us/en/product/countersunk-connector-haefele-confirmat-countersunk-head-for-drill-hole-5-mm-sw4/26443600/" color="#345e4d">Häfele Confirmat</link>; <link href="https://www.weratools.com/en-ca/tools/950-pks-l-key-metric-chrome-plated" color="#345e4d">Wera 950 PKS</link>; <link href="https://www.bigfer.com.br/suporte-aereo-l-armarios/" color="#345e4d">Bigfer 04.02.058</link>. Hashes no JSON de preparação. Nenhuma capacidade foi copiada por nome de produto.',True)]
    def page(c,doc):
        c.saveState();c.setStrokeColor(colors.HexColor('#ccd3cc'));c.line(42,34,553,34);c.setFont('Helvetica',8)
        c.drawString(42,22,'P04 - preparação para laboratório | sem ensaios executados | R52 preservada');c.drawRightString(553,22,str(doc.page));c.restoreState()
    pdf=SimpleDocTemplate(str(OUT/'P04_ensaios_laboratorio.pdf'),pagesize=A4,rightMargin=42,leftMargin=42,topMargin=36,bottomMargin=46,
        title='P04 - preparacao de ensaios para marcenaria/laboratorio',author='Projeto Guedala Park')
    pdf.build(story,onFirstPage=page,onLaterPages=page,canvasmaker=functools.partial(canvas.Canvas,invariant=1))

def drawing(d):
    art=Drawing(511,368);green=colors.HexColor('#467c66');wood=colors.HexColor('#b7a68a');pale=colors.HexColor('#e8ece4')
    def rect(x,y,w,h,color):art.add(Rect(x,y,w,h,fillColor=color,strokeColor=colors.HexColor('#81725d'),strokeWidth=.7))
    art.add(String(12,352,'Elevação frontal (projeção)',fontName='Helvetica-Bold',fontSize=10))
    rect(30,30,200,308,pale);rect(12,30,18,308,wood);rect(30,30,200,18,wood);rect(30,320,200,18,wood);rect(37,48,18,272,wood)
    for z in [18,290]:art.add(Circle(64,30+z,3,fillColor=green,strokeColor=green))
    art.add(String(60,302,'vão 272',fontSize=9));art.add(String(60,285,'divisor 18; folga 7',fontSize=8));art.add(String(65,18,'largura interna 200',fontSize=9))
    art.add(String(282,352,'Planta / vista de cima',fontName='Helvetica-Bold',fontSize=10))
    rect(282,90,18,230,wood);rect(300,302,200,18,wood);rect(300,90,200,212,pale);rect(307,90,18,212,wood)
    for v in [90,158]:
        art.add(Circle(334,320-v,7.5,fillColor=green,strokeColor=green))
        art.add(String(350,320-v-3,f'u34 / v{v}',fontSize=8))
    art.add(String(330,72,'v230: frente aberta',fontSize=9));art.add(String(350,330,'v0: traseira',fontSize=8))
    art.add(String(12,0,'Corpo T0 recortado:sem capacidade estrutural representativa da caixa inteira.',fontSize=8))
    return art

if __name__=='__main__':main()
