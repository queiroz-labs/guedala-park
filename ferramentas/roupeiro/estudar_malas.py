"""Estudo ortogonal de malas P03, usando dados salvos; nao abre FreeCAD.

python -B ferramentas/roupeiro/estudar_malas.py
Requer Pillow. Dimensoes de produto sao referencias, nao medidas das malas de Elias.
"""
from pathlib import Path
import hashlib
import itertools
import json
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'04_Moveis/P03'
GEO=ROOT/'04_Moveis/Proximas_decisoes/P01_P03/Geometria_P02_individual.json'
MONT=ROOT/'02_Modelo_3D/Componentes/Portas_de_correr/Montagem_R14.json'
D=json.loads(GEO.read_text(encoding='utf-8')); M=json.loads(MONT.read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(ROOT/D['source'])==D['source_sha256']
p=D['panels']
x0=p['Peca260']['bbox_mm'][3];x1=p['Peca259']['bbox_mm'][0]
y0=p['Peca262']['bbox_mm'][1];y1=p['Peca261']['bbox_mm'][1]
z0=p['Peca262']['bbox_mm'][5];z1=p['Peca263']['bbox_mm'][2]
W,DEPTH,H=x1-x0,y1-y0,z1-z0
assert (W,DEPTH,H)==(1314.,632.,272.)
door=p['Peca265']['bbox_mm']; leaf_width=door[3]-door[0]
slider_width=W-leaf_width-(door[0]-x0)
assert slider_width==642.
reserve_slider=M['nominal_package_mm']['reserve_frontal']
assert reserve_slider==82
margin=20.; gap=20.; passage_margin=10.

sources=[
 dict(name='Samsonite Varro pequena',url='https://samsonite.com.br/products/mala-pequena-varro-preta',
      published_dimensions_cm=[55,35,25],empty_mass_kg=2.6,
      note='Pagina informa essas dimensoes, mas nao explicita neste trecho se incluem todas as saliencias; expansor fechado e dimensoes reais devem ser conferidos.'),
 dict(name='Samsonite C-Lite pequena',url='https://samsonite.com.br/products/mala-pequena-c-lite-preta',
      published_dimensions_cm=[55,25,38],empty_mass_kg=1.9,
      note='Rotulos de largura/profundidade aparecem25/38 na pagina; estudo usa apenas o envelope reorientavel55x38x25, sem corrigir a ficha do fabricante.')]
references=[dict(id='bordo_55_35_25',long_mm=550.,short_mm=350.,thickness_mm=250.),
            dict(id='bordo_55_38_25',long_mm=550.,short_mm=380.,thickness_mm=250.)]


def layout(ref,count,kind):
    # Reserva32 da alternativa e uma exigencia de desenvolvimento, nao ferragem selecionada.
    frontal=reserve_slider if kind=='correr_atual' else 32.
    bagw=ref['long_mm'] if count==2 else ref['short_mm']
    bagd=ref['short_mm'] if count==2 else ref['long_mm']
    span=count*bagw+(count-1)*gap
    start=margin if count==2 else (W-span)/2
    xs=[margin,W-margin-bagw] if count==2 else [start+i*(bagw+gap) for i in range(count)]
    boxes=[dict(id=i+1,origin_mm=[xs[i],frontal+margin,0.],
                size_mm=[bagw,bagd,ref['thickness_mm']]) for i in range(count)]
    fits=span+2*margin<=W and frontal+2*margin+bagd<=DEPTH and ref['thickness_mm']<=H
    # Certificado de armazenamento: caixas em eixos ortogonais e folgas explicitas.
    if fits:
        for b in boxes:
            o,s=b['origin_mm'],b['size_mm']
            assert margin<=o[0] and o[0]+s[0]<=W-margin
            assert frontal+margin<=o[1] and o[1]+s[1]<=DEPTH-margin
            assert o[2]>=0 and o[2]+s[2]<=H
        for a,b in itertools.combinations(boxes,2):
            assert any(a['origin_mm'][k]+a['size_mm'][k]<=b['origin_mm'][k] or
                       b['origin_mm'][k]+b['size_mm'][k]<=a['origin_mm'][k] for k in range(3))
    storage=bool(fits)
    # Invasoes4/20 sao as hipoteses dos gabaritos, NAO secoes reais homologadas.
    entry_h=H-4-20 if kind=='correr_atual' else None
    entry_w=slider_width if kind=='correr_atual' else None
    required_entry=[bagw+2*10,ref['thickness_mm']+passage_margin]
    side_intervals=[]
    if kind=='correr_atual' and count==2:
        for b,interval in zip(boxes,[[0.,slider_width],[W-slider_width,W]]):
            lo,hi=interval;x=b['origin_mm'][0]
            side_intervals.append(dict(bag=b['id'],clear_interval_x_mm=interval,
                fits_width_with_10mm_each_side=x>=lo+10 and x+bagw<=hi-10))
        assert all(a['fits_width_with_10mm_each_side'] for a in side_intervals)
    return dict(reference=ref['id'],count=count,opening=kind,boxes=boxes,
        frontal_reservation_mm=frontal,storage_with_stated_clearances=storage,
        side_rear_plan_clearances_mm=dict(left=start,right=start,between=xs[1]-xs[0]-bagw,
            rear=DEPTH-(frontal+margin+bagd)),
        upper_storage_clearance_mm=H-ref['thickness_mm'],
        required_entry_width_height_mm=required_entry,
        slider_clear_width_mm=entry_w,slider_profile_hypothesis_clear_height_mm=entry_h,
        slider_straight_entry_fits_hypothesis=None if entry_h is None else
            required_entry[0]<=entry_w and required_entry[1]<=entry_h,
        side_insertion_intervals=side_intervals,
        status='Conferir produto e trajetoria; armazenamento nao prova entrada real ou resistencia')


cases=[layout(ref,n,k) for ref,n,k in itertools.product(references,[2,3],['correr_atual','abrir_estudo'])]
for ref in references:
    # Prova limitada a caixas ortogonais sem empilhar. Como2*lado menor>profundidade,
    # qualquer par se sobrepoe emY: as projecoesX devem ser disjuntas; quatro excedemW.
    assert 2*ref['short_mm']>DEPTH and 4*ref['short_mm']>W
out=dict(source_sha256=D['source_sha256'],geometry_sha256=sha(GEO),assembly_sha256=sha(MONT),
    cabinet_internal_mm=[W,DEPTH,H],sources=sources,references=references,
    demand=dict(minimum_bags=2,category='bordo10kg',user_actual_dimensions_unknown=True,
                added_to_user_program=True,capacity_mass_not_certified=True),
    cases=cases,handling_requirements=dict(plan_margin_mm=margin,plan_gap_mm=gap,
        vertical_total_entry_margin_mm=passage_margin,
        proposed_hinge_frontal_budget_mm=32,proposed_budget_not_hardware_specification=True),
    results=dict(two_bags_storage=True,third_bag_geometric_opportunity=True,
        four_bags_orthogonal_not_fit=True,slider_width_is_not_main_problem_for_two_bags=True,
        slider_248mm_passage_is_only_hypothesis=True,reference_250mm_bag_not_pass_straight_through_248mm_hypothesis=True),
    load_cases_kg=dict(two_empty_Varro=5.2,two_empty_CLite=3.8,
        two_at_10kg_each=20,three_at_10kg_each=30),
    recommendation='Desenvolver duas portas laterais sem montante central no P03; manter caixa/alturas. Troca ainda nao adotada no CAD.',
    limitations=['Sem medicao das malas de Elias, garantia de marca/categoria ou folga real de expansor.',
        'Volume de guarda nao prova passagem; sem inclinacao/diagonal ou deformacao da mala.',
        'Altura das folhas237 nao e altura livre de entrada.',
        'Envoltoria dos perfis4/20 e reserva82 sao hipoteses anteriores, nao desenhos reais dos produtos.',
        'Alternativa de abrir depende de dobradicas, giro junto ao P02, acesso e passagem260mm sem obstaculos.',
        'Tres malas carregadas somam30kg: nao cobertas pelos estudos anteriores de conteudoP03 ate20kg.',
        'Nenhuma alteracao do FreeCAD, corte, compra ou capacidade liberada.'])
OUT.mkdir(exist_ok=True)
(OUT/'Estudo_malas.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# Prancha deterministica: formas e dimensoes sao as mesmas dos certificados.
im=Image.new('RGB',(1800,1320),'white');dr=ImageDraw.Draw(im)
def font(s,b=False):return ImageFont.truetype('C:/Windows/Fonts/'+('arialbd.ttf' if b else 'arial.ttf'),s)
def txt(x,y,t,s=24,c='#263c49',b=False):dr.text((x,y),t,font=font(s,b),fill=c)
txt(55,35,'Maleiro P03 — estudo para duas malas de bordo',38,b=True)
txt(55,94,'Referência de projeto: 55 × 35 × 25 cm por mala • caixas fechadas, sem expansor',25)
def plan(case,ox,oy,title,subtitle):
    s=.58
    txt(ox,oy-85,title,29,b=True);txt(ox,oy-42,subtitle,22)
    x,y=ox,oy
    dr.rectangle([x,y,x+W*s,y+DEPTH*s],fill='#f4f1e9',outline='#556b76',width=3)
    dr.rectangle([x,y,x+W*s,y+case['frontal_reservation_mm']*s],fill='#e5e7e9')
    for box in case['boxes']:
        a,b,_=box['origin_mm'];w,d,h=box['size_mm']
        dr.rounded_rectangle([x+a*s,y+b*s,x+(a+w)*s,y+(b+d)*s],radius=10,
            fill=['#aac7d5','#b7cda5','#dcc495'][box['id']-1],outline='#354e5d',width=3)
        txt(x+(a+15)*s,y+(b+30)*s,'Mala '+str(box['id']),24,b=True)
        txt(x+(a+15)*s,y+(b+90)*s,('55 × 35' if case['count']==2 else '35 × 55')+' cm',21)
    txt(x+210,y+DEPTH*s+15,'Largura interna: 131,4 cm',23)
    txt(x+5,y+DEPTH*s+52,'Profundidade da caixa: 63,2 cm',22)
two=next(c for c in cases if c['reference']=='bordo_55_35_25' and c['count']==2 and c['opening']=='correr_atual')
three=next(c for c in cases if c['reference']=='bordo_55_35_25' and c['count']==3 and c['opening']=='abrir_estudo')
plan(two,55,255,'1. Duas malas — espaço atual','Comprimento de55 cm ao longo da largura; sobra atrás.')
plan(three,955,255,'2. Terceira mala — oportunidade','Arranjo girado; depende da alternativa de abrir.')
txt(55,735,'O ponto crítico é a passagem pela frente',31,b=True)
txt(55,791,'Altura interna: 27,2 cm',27,b=True)
txt(55,835,'Mala deitada: 25 cm → sobra vertical nominal de 2,2 cm.',25)
txt(55,887,'Correr: reservas CAD de20 + 4 mm deixam passagem hipotética de24,8 cm.',25,c='#a63c30')
txt(55,929,'Isso não valida a entrada da mala de25 cm; é preciso conferir o perfil real.',24,c='#a63c30')
txt(55,993,'Alternativa a desenvolver: duas portas de abrir, sem montante central.',26,b=True)
txt(55,1038,'Meta de entrada por mala: ao menos57 cm de largura ×26 cm de altura livre.',24)
txt(55,1080,'Sem baixar o maleiro, retirar espaço das roupas ou mudar o alinhamento do L.',24)
txt(55,1154,'A terceira mala é capacidade geométrica possível, sem carga ou acesso liberados.',23)
txt(55,1193,'Faixas cinzas são reservas de estudo. Perfis, dobradiças e folgas não estão homologados.',22)
txt(55,1238,'Estudo em planta, não render de fabricação. Fonte: R52 e dimensões publicadas pela Samsonite.',21)
im.save(OUT/'Malas_no_maleiro.png')
assert sha(ROOT/D['source'])==D['source_sha256']
print(json.dumps(dict(cases=len(cases),storage_cases_pass=sum(c['storage_with_stated_clearances'] for c in cases),
    source_unchanged=True,internal_mm=[W,DEPTH,H],slider_clear_width_mm=slider_width,
    slider_hypothetical_clear_height_mm=H-24),ensure_ascii=False))
