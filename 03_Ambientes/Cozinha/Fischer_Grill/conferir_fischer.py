"""Estudo isolado de envelopes, sem alterar ou recomputar a R30.

Caixas propostas não são CAD do fabricante nem lista de corte. As posições
relativas entre frente, corpo e apoio são hipóteses explícitas de estudo.
"""
import sys,json,hashlib,itertools
from pathlib import Path
sys.path.append('C:/Users/Elias/AppData/Local/Programs/FreeCAD-1.1.4/lib')
import FreeCAD as App,Part

here=Path(__file__).resolve().parent
project=here.parents[1]
source=project/'Modelo_FreeCAD/01_Cadeiras/Guedala_Park_R30_Juntas_Rotulos.FCStd'
before=hashlib.sha256(source.read_bytes()).hexdigest()
doc=App.openDocument(str(source))
refs={}
def mirror_shape(o):
    s=o.Shape.copy();s.Placement=o.getGlobalPlacement()
    m=App.Matrix();m.A11=-1;m.A14=7400
    return s.transformGeometry(m)
def bbox(s):
    b=s.BoundBox
    return [round(v,6) for v in (b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax)]
for n in ['Peca133','Peca134','Peca305','Peca306','Peca307','Peca308','Peca152','Peca357']:
    o=doc.getObject(n);s=mirror_shape(o)
    assert s.isValid(),n
    refs[n]={'label':o.Label,'shape':s,'bbox':bbox(s)}

detail=App.newDocument('Estudo_Fischer_Grill_R30')
baseline=detail.addObject('App::DocumentObjectGroup','ReferenciasR30')
proposed=detail.addObject('App::DocumentObjectGroup','Proposta')
reservations=detail.addObject('App::DocumentObjectGroup','Reservas')
rows={}; shapes={}
def appearance(o,color=None,transparency=None):
    # Sem GUI, ViewObject é None; apresentação da prancha é gerada separadamente.
    if o.ViewObject is not None:
        if color is not None:o.ViewObject.ShapeColor=color
        if transparency is not None:o.ViewObject.Transparency=transparency
def feature(n,label,shape,group,condition):
    o=detail.addObject('Part::Feature',n);o.Label=label;o.Shape=shape
    o.addProperty('App::PropertyString','Condicao','Estudo');o.Condicao=condition
    group.addObject(o);shapes[n]=shape
    rows[n]={'label':label,'bbox_mm':bbox(shape),'valid':shape.isValid(),'condition':condition}
    assert shape.isValid(),n
    return o
for n,r in refs.items():
    if n in ['Peca133','Peca307']:continue
    o=feature('R30_'+n,r['label'],r['shape'],baseline,'Cópia estática espelhada de peça da R30, sem mudança na fonte.')
    appearance(o,(0.72,0.69,0.61),72 if n in ['Peca308','Peca357','Peca152'] else 0)
def box(n,label,pos,dim,group=proposed,condition='Envelope proposto; sem dimensão executiva ou carga comprovada.'):
    return feature(n,label,Part.makeBox(*dim,App.Vector(*pos)),group,condition)

# X segue o eixo do vão R30. Y cresce da frente para a parede; Z vem do piso de estudo.
cx=3226.5
# Topo570 escolhido apenas para estudo: ensaio d131 deixa219 e, com10 de
# tolerância geométrica,209. d131 não é projeção inferior confirmada.
oven_top=570
front_bottom=oven_top-447
support_top=oven_top-432
front=box('FrenteFischer','Fischer escolhido · frente 595 × 447 · gabarito',
          (cx-297.5,6378,front_bottom),(595,26,447),condition='595/447 do desenho; 26 P de representação. Topo Z570 e datum frente/corpo são hipóteses; não define furação nem a base real.')
appearance(front,(0.13,0.16,0.16))
body=box('EncaixeFischer','Envelope de encaixe · L560 × P547 × A432',
         (cx-280,6404,support_top),(560,547,432),condition='L560 é recorte, não largura confirmada do chassi. P547 conservador do nicho Rev03 versus544 no manual. A432 do desenho. Topo Z570 conservador; datum de apoio Z138 proposto, a confirmar.')
appearance(body,(0.30,0.38,0.39))
support=box('ApoioProposto','Apoio inferior candidato · topo Z138',
            (2938,6410,support_top-18),(577,535,18),condition='Chapa18 e topo138 são hipóteses. Apoiar nas laterais; dimensionar material, ligações, pés reais do forno e deformação. Não contar as faixas8,5 como estrutura suficiente.')
appearance(support,(0.71,0.50,0.28))
for side,x in [('Esquerda',2938),('Direita',3506.5)]:
    o=box('Acerto'+side,'Faixa de acerto '+side+' · 8,5 mm nominais',
          (x,6404,support_top),(8.5,541,650-support_top),condition='Reserva geométrica para obter abertura560 no vão577. Material, altura, recobrimento, fixação e plano frontal dependem do conjunto real; não é peça de corte.')
    appearance(o,(0.86,0.66,0.40))
# Reserva conservadora atrás do corpo; não substitui recorte45x560 e desenho de percurso.
air=box('FaixaArTraseira','Reserva traseira de ar · 45 × 560',
        (cx-280,6955,support_top-18),(560,45,900-support_top+18),group=reservations,
        condition='Faixa contínua proposta até a parede de estudo. Conexões/cabos fora dela. Não é certificação de vazão ou desempenho térmico.')
appearance(air,(0.20,0.64,0.75),85)
newcross=box('TravessaProposta','Travessa candidata · 27 mm para a frente',
             (2938,6743,660),(577,212,30),condition='Mesmo envelope577x212x30 da R30, deslocado27mm emY. Não dimensiona carga/fixações/temperatura nem verifica grampos e conexão inferior reais do cooktop.')
appearance(newcross,(0.82,0.40,0.20))
cut=box('RecorteCooktop','Recorte KE4GC de referência · 520 × 390',
        (2960,6490,900),(520,390,20),group=reservations,
        condition='Posição no eixo atualX3220, centrado na mesa600x450. Não cortar a pedra; cotas, raios, grampos, apoio e conexão precisam ser conferidos no produto e na obra.')
appearance(cut,(0.80,0.25,0.20),65)
outlet=box('SaidaFrontalProposta','Reserva de passagem até saída frontal · altura45',
           (cx-280,6378,710),(560,622,45),group=reservations,
           condition='Percurso proposto acima da travessa e abaixo do cooktop hipotético. Saída frontal de área bruta252cm², sem seleção de grelha, comprovação térmica ou vazão. Mantê-lo livre de gás/cabos/armazenamento.')
appearance(outlet,(0.20,0.64,0.75),85)
stress=box('CooktopStress131','Teste de estresse · 131 mm inteiros abaixo da bancada',
           (2920,6460,789),(600,450,131),group=reservations,
           condition='Hipótese conservadora para o corpo: altura TOTAL publicada131 aplicada inteira para baixo. Não é cota instalada e não cobre conexões, grampos ou mangueira não representados.')
appearance(stress,(0.88,0.55,0.19),90)

def common(a,b):return round(a.common(b).Volume,6)
solid_names=['FrenteFischer','EncaixeFischer','ApoioProposto','AcertoEsquerda','AcertoDireita','TravessaProposta']
fixed=['Peca305','Peca306','Peca308','Peca152','Peca357','Peca134']
checks=[]
for a,b in itertools.combinations(solid_names,2):
    checks.append({'a':a,'b':b,'overlap_mm3':common(shapes[a],shapes[b])})
for a in solid_names:
    for b in fixed:checks.append({'a':a,'b':b,'overlap_mm3':common(shapes[a],refs[b]['shape'])})
hits=[r for r in checks if r['overlap_mm3']>0.1]
assert not hits,hits
old_air=common(refs['Peca307']['shape'],shapes['FaixaArTraseira'])
new_air=common(shapes['TravessaProposta'],shapes['FaixaArTraseira'])
assert old_air==453600.0 and new_air==0,(old_air,new_air)
assert common(shapes['EncaixeFischer'],shapes['FaixaArTraseira'])==0
outlet_checks={n:common(shapes['SaidaFrontalProposta'],shapes[n]) for n in solid_names+['CooktopStress131']}
assert not any(v>0.1 for v in outlet_checks.values()),outlet_checks
assert common(shapes['FaixaArTraseira'],shapes['CooktopStress131'])==0
assert common(shapes['SaidaFrontalProposta'],shapes['FaixaArTraseira'])>0

# Triagem localizada adicional das peças nativas Peca* em estado salvo.
# Exclui os dois volumes históricos substituídos; lista explícita no relatório.
native_tests=[];native_hits=[];native_count=0
door_sweep=Part.makeBox(595,473,(447**2+26**2)**0.5,App.Vector(cx-297.5,6378-447,front_bottom))
door_candidates=[]
excluded={'Peca133','Peca307'}
for o in doc.Objects:
    if not o.Name.startswith('Peca') or o.Name in excluded or not hasattr(o,'Shape') or o.Shape.isNull():continue
    s=mirror_shape(o);b=s.BoundBox
    if b.XMax<2850 or b.XMin>3650 or b.YMax<5900 or b.YMin>7020 or b.ZMax<0 or b.ZMin>920:continue
    native_count+=1
    vol=common(door_sweep,s)
    if vol>0.1:door_candidates.append({'source':o.Name,'label':o.Label,'overlap_mm3':vol})
    for name in solid_names:
        p=shapes[name];bb=p.BoundBox
        if all(min(getattr(b,k+'Max'),getattr(bb,k+'Max'))-max(getattr(b,k+'Min'),getattr(bb,k+'Min'))>1e-5 for k in ['X','Y','Z']):
            vol=common(p,s)
            row={'proposed':name,'source':o.Name,'label':o.Label,'overlap_mm3':vol}
            native_tests.append(row)
            if vol>0.1:native_hits.append(row)
assert not native_hits,native_hits
assert not door_candidates,door_candidates
detail.recompute()
target=here/'Estudo_Fischer_Grill_R30.FCStd'
detail.saveAs(str(target))
after=hashlib.sha256(source.read_bytes()).hexdigest();assert before==after
scenarios=[]
for d in [40,60,80,100,120,131]:
    gap=920-d-oven_top
    scenarios.append({'d_hipotetico_mm':d,'separacao_minima_envelope_mm':gap,
                      'saldo_sobre_200_mm':gap-200,'saldo_com_tolerancia_10_mm':gap-210})
report={'date':'2026-10-19','chosen':'Fischer Infinity com grill sem turbo, preto127V,28349-64929',
 'method':'FreeCAD1.1.4 sem interface. Oito formas nativas copiadas e espelhadas pelo planoX3700. Proposta separada de envelopes, interseções volumétricas e triagem Peca* local. Sem salvar ou recomputar R30; não audita toda a instalação.',
 'source':str(source),'sha256_before':before,'sha256_after':after,'study':str(target),
 'reference':{n:{k:v for k,v in r.items() if k!='shape'} for n,r in refs.items()},
 'proposal':rows,'pair_checks':checks,'overlaps':hits,'native_bbox_candidates':native_tests,'native_overlaps':native_hits,
 'native_region_shape_count':native_count,
 'native_filter':'Objetos Peca* com geometria na regiãoX2850..3650,Y5900..7020,Z0..920; excluídosPeca133 ePeca307. Não cobre objetos com outros nomes, movimentos, detalhes ausentes, conexões, chassi real ou obra.',
 'air':{'old_cross_overlap_mm3':old_air,'proposed_cross_overlap_mm3':new_air,
        'body_to_reserved_strip_mm':4,'body_to_wall_mm':49,'support_rear_space_mm':55,
        'manual_slot_width_mm':560,'manual_slot_depth_mm':45,'manual_slot_area_cm2':252,
        'front_outlet_z_mm':[710,755],'outlet_overlap_checks_mm3':outlet_checks,
        'outlet_gap_to_stress131_mm':34,'outlet_gap_to_cross_mm':20,
        'limit':'Continuidade geométrica de reservas; não comprova resfriamento nem área livre com grelha.'},
 'door_sweep':{'bbox_mm':bbox(door_sweep),'overlaps_with_Peca':door_candidates,
               'projection_ahead_of_frame_mm':447,'limit':'Caixa envolvente contínua0..90° da frente inteira595x447x26, eixo hipotético inferior. Porta, puxador e dobradiças reais não modelados; não audita pessoa, móveis de outros nomes, circulação ou manutenção.'},
 'dimensions':{'module_external_width_mm':613,'existing_internal_width_mm':577,'nominal_opening_width_mm':560,
               'nominal_side_adjustment_mm':8.5,'front_max_width_mm':595,'front_side_margin_mm':9,
               'front_top_mm':oven_top,'front_bottom_mm':front_bottom,'support_top_candidate_mm':support_top,
               'oven_axis_x':3226.5,'cooktop_axis_x':3220,'axis_offset_mm':6.5,
               'front_reference_forward_shift_mm':6,'envelope_front_recess_from_stone_mm':8,
               'cabinet_depth_mm':590,'published_niche_depth_mm':580,
               'cooktop_cut_side_gaps_mm':[22,35],'cooktop_cut_front_wall_gaps_mm':[120,120]},
 'scenarios':scenarios,
 'critical_limits':['Envelopes do forno e faixas não são geometrias de fabricante. Datum frente/corpo/apoio e altura de recorte440 não fixados para fabricação.',
 'd=131 é apenas teste de estresse; altura total publicada do cooktop não determina sua projeção inferior.',
 'Recorte de pedra ilustrativo, não executado. Sem verificação de vazão/calor, resistência, elétrica, fixações ou operação/porta aberta.',
 'Isolamento da LG, emenda da pedra e cotas de campo continuam pendentes. Reserva de ar não pode ser ocupada por cabo, tomada, mangueira ou travessa.']}
(here/'Conferencia_Fischer.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
App.closeDocument(detail.Name);App.closeDocument(doc.Name)
print(json.dumps({'study':str(target),'solid_pair_checks':len(checks),'overlaps':hits,
                  'native_candidate_pairs':len(native_tests),'native_overlaps':native_hits,'air':report['air'],
                  'source_unchanged':before==after},ensure_ascii=False))
