"""Selecao candidata, centros de furacao e demandas do grupo P03/A.

Nao abre CAD. Nao prescreve pilotos nem calcula capacidade sem chapa/produto.
As cotas representam somente canecos e centros do calco37/32, nao seus corpos.
"""
import hashlib,json,math
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont

ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'04_Moveis/P03'
parent=json.loads((OUT/'Abertura_e_dobradicas_A.json').read_text(encoding='utf-8'))
source=ROOT/'02_Modelo_3D/Guedala_Park_R52_Corrigido.FCStd'
assert hashlib.sha256(source.read_bytes()).hexdigest()==parent['source_sha256']
centers=[52.,153.,254.]
holes=[]
for side,cup_x,plate_x in [('left',5414.5,5408.),('right',6715.5,6722.)]:
    for index,z_leaf in enumerate(centers,1):
        z=2133+z_leaf
        holes.append(dict(side=side,hinge=index,cup_center_world_mm=[cup_x,3308.,z],
                          cup_center_from_leaf_bottom_mm=z_leaf,cup_diameter_mm=35.,
                          minimum_cup_depth_from_guide_mm=13.,nominal_front_skin_if_depth13_mm=5.,
                          cup_top_bottom_minimum_ligament_to_leaf_edge_mm=min(z_leaf,306-z_leaf)-17.5,
                          plate_holes_world_mm=[[plate_x,3347.,z-16],[plate_x,3347.,z+16]],
                          plate_hole_heights_from_inner_base_mm=[z-16-2150,z+16-2150],
                          plate_hole_min_distance_to_base_top_mm=min(z-16-2150,2422-z-16)))
assert len(holes)==6
assert min(h['plate_hole_min_distance_to_base_top_mm'] for h in holes)==19.
assert min(h['cup_top_bottom_minimum_ligament_to_leaf_edge_mm'] for h in holes)==34.5
assert all(2150<p[2]<2422 for h in holes for p in h['plate_holes_world_mm'])
loads=[]
for mass in [3.,4.,5.]:
    weight=mass*9.80665;moment=weight*.336
    loads.append(dict(finished_door_hypothesis_kg=mass,vertical_group_N=weight,
                      moment_nominal_Nm=moment,equivalent_pair_over202mm_N=moment/.202,
                      per_fastener_force=None,capacity_margin=None))
sources=[
 dict(url='https://publications.blum.com/2024/catalogue/en/76/',
      supports=['71B3550 aparafusada, recobrimento total, CLIP top BLUMOTION110.',
                '70T3553 nominal86;609.1500 diametro3.5/comprimento15 na lista de acessorios.',
                'BLUMOTION integrado e desativavel; nao misturar familia CLIP com mola emfrentes largas com base na nota de combinacao.']),
 dict(url='https://publications.blum.com/2024/catalogue/en/77/',
      supports=['TB/K3-7;K5/calco0 recobrimento16;caneco35 e minimo13 de profundidade.',
                'Folga minima tabelaFD18/TB5:0.8;acrescimo0.4 para ajuste lateral+2. Nao representa margem do conjunto P03.']),
 dict(url='https://publications.blum.com/2024/catalogue/en/152/',
      supports=['173H7100 distancia0/altura8.5,aco,fixacao com parafusoaglomerado3.5 ou4,calco37/32,regulagemaltura±2.']),
 dict(url='https://publications.blum.com/2024/catalogue/en/718/',
      supports=['Quantidade depende de peso/altura;dados para frente600 de largura;maior distanciaentre dobradicas favorece estabilidade.']),
 dict(url='https://ea.blum.com/en/number-of-hinges/',
      supports=['Extensao orientativa ate650 comdobradicaadicional;recomendaaltura maiorquelargura.']),
 dict(url='https://ea.blum.com/en/opening-angle-stops-for-110-and-107-hinges/',
      supports=['70T3553 para CLIPtopBLUMOTION110 limita86;instalar emtodasdobradicas.',
                'Dobradicafechada,instalarantesdeencaixarportanocalco,espacoentrecanecoearticulacao.']),
 dict(url='https://publications.blum.com/2024/catalogue/en/710/',
      supports=['Fabricante moveleiro deve escolher fixacoes conforme material.',
                'Recomendacoes de fixacao referem chapaP2 EN312,650kg/m3 EN323,revestida conforme texto.',
                'Aplicacoes especiais/muito largas exigem consideracao especifica;nao transferir capacidade padrao automaticamente.'])]

report=dict(source_sha256=parent['source_sha256'],selected_for_evaluation_only=True,
            leaf_mm=[672,306,18],finished_mass_hypothesis_kg=4,
            bill_of_materials_candidate=[
                dict(part='71B3550',quantity=6,status='candidata;3porfolha'),
                dict(part='173H7100',quantity=6,status='calco0candidato'),
                dict(part='70T3553',quantity=6,status='umportodadobradica;encaixorealpendente'),
                dict(part='609.1500',quantity=24,status='12nocaneco+12nocalco;candidato3.5x15;confirmarcabeca,pilotoechapa')],
            centers=holes,load_cases=loads,sources=sources,
            alternatives=[
                dict(option='2hinges_extremes202',status='sensibilidade,naoliberado',reason='Mesmo bracoextremo;menos pontos e menor massa,mas semaprovacao/aplicacaolarga.'),
                dict(option='3hinges_extremes202',status='prioridade_de_consulta',reason='MantemA;alinhargrupoeconfirmarcapacidade/fechamentoreais.'),
                dict(option='4hinges',status='naoadotarautomaticamente',reason='Semcapacidadedemonstrada;maisfuracaoemfolhabaixanaoeliminarestricaolargura.'),
                dict(option='INSERTA_71B3590',status='naosubstituirsemnovoestudo',reason='Muda fixacao,nao comprova maiscapacidade;exigegabarito/produtoreal.'),
                dict(option='155degrees',status='semnecessidadedemonstrada',reason='Outro mecanismo/gabarito/varredura;maiorangulonaoprova maiorcapacidade.')],
            pending=['Confirmar71B3550/calco0 comfolha672x306,4kgacabados eextremos202.',
                     'BaseMDFBP Greenplac18/ArenzaColoreLizze nasduasfacesP03;confirmar SKU/substrato e massa acabada reais,conformeChapa_P03.json.',
                     'Gabarito real dos dois parafusos do caneco, diametro/profundidade dos pilotos e ferramenta.',
                     'Capacidade do grupo/fixacoes,rigidez,alinhamento e regulagens;naodividir esforcos igualmente.',
                     'Corpos completos,limitador e espaco para montagem/retirada,antesdeafirmarpassagemeafetiva.',
                     'Prototipo da folha real:flecha/desalinhamento,manutencaodejuntas,aberturafechamentoeatrito de ferragens,comcriteriosdo fornecedor.',
                     'Caixa/base/sustentacao de malas20kg e eventual30kg sao verificacoes separadas.'],
            assumptions=['Centros de calco alinhados emZ ao caneco,comdoisfuros±16:conferir produto real.',
                         '19mm e distancia de centro de parafuso a borda interna,nao distancia da borda do furo nemprova contra fendilhamento.',
                         'Profundidademinima13 nao e instrucao parafresarsem tolerancia:5mm epele nominalsem ponta/desvios.',
                         'Comprimento15 do parafuso nao e penetracao util15;descontar ferragem/cabeca/ponta conforme desenho.',
                         'Numero de limitadores documentado;forca/impacto no batente e encaixe fisico nao calculados.',
                         'NaofoiabertoFreeCAD,nemalteradaR52.'],
            conclusion='CANDIDATO_COHERENTE_NAO_HOMOLOGADO: referencias e centros conferidos;nao ha capacidade publicada especifica para672x306 neste dossie.')
(OUT/'Dobradicas_A.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

im=Image.new('RGB',(1800,1250),'white');dr=ImageDraw.Draw(im)
def font(n,b=False):return ImageFont.truetype('C:/Windows/Fonts/'+('arialbd.ttf' if b else 'arial.ttf'),n)
def tx(x,y,t,n=25,b=False,c='#2a414e'):dr.text((x,y),t,font=font(n,b),fill=c)
tx(60,35,'Maleiro A — grupo candidato de dobradiças',38,True)
tx(60,100,'Uma folha ilustrada • outra espelhada • centros nominais, sem programa de usinagem',25)
tx(60,170,'Verso da porta: 672 × 306 × 18 mm',28,True)
sx=1.65;ox=120;oy=255
dr.rectangle([ox,oy,ox+672*sx,oy+306*sx],fill='#ddc9a6',outline='#665b4b',width=3)
for z in centers:
    x=ox+22.5*sx;y=oy+(306-z)*sx;r=17.5*sx
    dr.ellipse([x-r,y-r,x+r,y+r],fill='#f3f5f3',outline='#526b76',width=3)
    dr.line([(x+40,y),(ox+250,y)],fill='#526b76',width=2)
    tx(ox+265,y-16,f'{z:g} mm desde a borda inferior',25)
tx(130,805,'Canecos Ø35 • K5 • eixo a 22,5 mm da borda lateral',24)
tx(130,845,'Profundidade mínima publicada 13; pele nominal 5 se usinado a 13.',24)

tx(1310,170,'Lateral (trecho interno)',26,True)
px=1380;py=295;sy=1.5
dr.rectangle([px-45,py,px+180,py+272*sy],fill='#e8efed',outline='#526b76',width=3)
for z in centers:
    mid=z-17
    for h in [mid-16,mid+16]:
        y=py+(272-h)*sy
        dr.ellipse([px-5,y-5,px+5,y+5],fill='#526b76')
    y=py+(272-mid)*sy
    tx(px+30,y-15,f'{mid:g}',23)
tx(1285,755,'Centros dos calços: 35 / 136 / 237 mm',22)
tx(1285,790,'desde a base interna; furos ±16 mm.',22)
tx(1285,825,'Extremos dos furos: 19 mm às bordas.',22)

tx(60,930,'Para o maleiro completo: 6 dobradiças 71B3550 + 6 calços 173H7100 + 6 limitadores 70T3553.',25,True)
tx(60,978,'24 parafusos são apenas quantitativo candidato; composição/SKU da chapa e pilotos a confirmar.',25)
tx(60,1040,'Capacidade pendente: folha de 672 mm excede a orientação publicada até 650 mm.',27,True,c='#9a4e38')
tx(60,1090,'O grupo deve suportar a porta e manter alinhamento; não basta somar capacidades individuais.',25)
tx(60,1160,'Posições cabem nominalmente. Corpos, regulagens, fixação e protótipo precisam de conferência.',24)
im.save(OUT/'Dobradicas_A.png')
print(json.dumps(dict(hinges=6,plates=6,stops=6,candidate_screws=24,
                      plate_min_center_edge_mm=19,cup_min_top_bottom_edge_mm=34.5,
                      moment4kg_Nm=loads[1]['moment_nominal_Nm'],pair4kg_N=loads[1]['equivalent_pair_over202mm_N'],
                      capacity_approved=False,source_hash_unchanged=True),ensure_ascii=False))
