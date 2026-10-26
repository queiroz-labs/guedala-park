"""Vao reto, avanco das folhas e demandas de dobradicas da alternativa A.

Sem abrir/alterar CAD. Usa o mecanismo de quatro barras ja conferido.
O corredor e conservador para translacao reta; nao otimiza trajetoria diagonal.
Nao inclui corpos de ferragens, maos, tolerancias ou comprovacao resistente.
"""
import json, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import detalhar_portas_maleiro as base

G=9.80665
mm=np.eye(4);mm[2,3]=2132
rows=[dict(side='left',module_matrix=mm.tolist(),hinge_support_inner_x_mm=5408,
           hinge_origin_y_mm=3346.5,closed_leaf_base=[5392,3290,1],front_local_box=[0,0,0,672,18,306]),
      dict(side='right',module_matrix=mm.tolist(),hinge_support_inner_x_mm=6722,
           hinge_origin_y_mm=3346.5,closed_leaf_base=[6738,3290,1],front_local_box=[-672,0,0,0,18,306])]

def corridor(angle, both):
    left=base.polygons(rows[0],[angle])[0]
    right=base.polygons(rows[1],[angle if both else 0])[0]
    lo=max(5408.,float(left[:,0].max()))
    hi=min(6722.,float(right[:,0].min()))
    return dict(angle_deg=float(angle),both_open=both,left_x_mm=lo,right_x_mm=hi,
                width_mm=max(0.,hi-lo),height_between_wood_mm=272.,
                advance_from_closed_front_mm=3290-float(left[:,1].min()))

curves=[corridor(a,both) for both in [False,True] for a in base.angles]
selected=[c for c in curves if c['angle_deg'] in [60,70,75,80,82,84,86]]
minimum_angles={}
for both in [False,True]:
    for width in [550,570,1120]:
        ok=[c['angle_deg'] for c in curves if c['both_open']==both and c['width_mm']>=width]
        minimum_angles[f'{"both" if both else "one"}_{width}mm']=min(ok) if ok else None

one=corridor(86,False);two=corridor(86,True)
assert one['width_mm']>=570 and two['width_mm']>=1120
body={n:list(r['bbox_mm']) for n,r in base.D['panels'].items() if not r['door']}
for n in ['Peca259','Peca260','Peca262','Peca263']:body[n][1]+=20
# Verifica tambem o espelho da entrada individual, ambas as profundidades e
# um envelope com folga lateral20/altura10. Contato com base e permitido.
paths=[]
for mode in ['left_only','right_only','both']:
    aa=[86,86] if mode=='both' else ([86,0] if mode=='left_only' else [0,86])
    fronts=[base.polygons(r,[a]) for r,a in zip(rows,aa)]
    if mode=='both':xs=[5505.,6075.]
    else:
        x=one['left_x_mm']+(one['width_mm']-550)/2
        xs=[x if mode=='left_only' else 12130-(x+550)]
    for depth in [350,380]:
        for i,x in enumerate(xs):
            for padding in [False,True]:
                lo=x-10 if padding else x
                width=570 if padding else 550
                height=260 if padding else 250
                hits=[];min_front_sep=float('inf')
                for y in np.arange(2550,3410.001,5.):
                    poly=base.rect([lo,y,2150,lo+width,y+depth,2150+height])[None,:]
                    for j,front in enumerate(fronts):
                        gap=float(base.separations(poly,front)[0,0])
                        min_front_sep=min(min_front_sep,gap)
                        if gap < -1e-6:hits.append(dict(y_mm=float(y),obstacle=f'front_{j}'))
                    for name,bb in body.items():
                        if min(2150+height,bb[5])<=max(2150,bb[2])+1e-6:continue
                        if base.separations(poly,base.rect(bb)[None,:])[0,0]<-1e-6:
                            hits.append(dict(y_mm=float(y),obstacle=name))
                paths.append(dict(mode=mode,bag=i+1,x_mm=x,depth_mm=depth,
                                  padded_envelope=padding,minimum_sampled_front_axis_gap_mm=min_front_sep,hits=hits))
assert len(paths)==16 and all(not p['hits'] for p in paths)

groups=[]
for centers in [[79,227],[52,254],[52,153,254]]:
    span=max(centers)-min(centers)
    cups=len(centers)
    wood=672*306*18-cups*math.pi*17.5**2*13
    loads=[dict(finished_door_hypothesis_kg=m,vertical_group_N=m*G,
                gravitational_group_moment_Nm=m*G*.336,
                extreme_pair_equivalent_N=m*G*.336/(span/1000)) for m in [3,4,5]]
    groups.append(dict(cup_centers_from_bottom_mm=centers,hinges=cups,span_mm=span,
                       wood_mass_kg_at_density={str(rho):wood*rho/1e9 for rho in [650,800,900]},
                       demand_cases=loads,approved=False))

reduction=1-148/202
result=dict(source_sha256=base.D['source_sha256'],source_unchanged=base.sha(base.ROOT/base.D['source'])==base.D['source_sha256'],
            preference='A672x306, escolhida por Elias para continuar estudo; sem liberacao de fabricacao',
            corridor_definition='Intervalo X entre projecoes completas das folhas, limitado a abertura entre madeiras. Serve para translacao reta; ferragens excluidas.',
            one_open86=one,both_open86=two,sampled_curves=curves,selected_angles=selected,
            minimum_sampled_angle_for_width=minimum_angles,bag_paths=paths,
            hinge_groups=groups,extreme_pair_reduction_148_to202_fraction=reduction,
            equal_height_thickness_density_solid_door_moment_ratio_vs650=(672/650)**2,
            sources=['https://ea.blum.com/en/number-of-hinges/'],
            limitations=['Largura672 alem da extensao650 publicada; proporcao baixa tambem exige confirmacao.',
                         'Corpos de dobradicas/limitadores e regulagens nao incluidos no corredor.',
                         'Amostragem0.5grau/5mm nao prova folga continua nem tolerancia.',
                         'Tres dobradicas nao significam divisao igual de carga, nem aprovacao automatica.',
                         'Momento por braco nominal336; nao e capacidade ou esforco por parafuso.',
                         'Peso das malas pertence a caixa/base; nao se soma a massa da porta para selecionar dobradica.',
                         'Espaco da mao, alcance a2.15m e operacao real precisam de prototipo.',
                         'Posicoes52/153/254 sao candidatas; verificar corpos, calcos, parafusos e chapa.'],
            gate='NAO_ATENDIDO: passagem nominal passa; capacidade de ferragem/fixacoes nao comprovada')
(base.OUT/'Abertura_e_dobradicas_A.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

im=Image.new('RGB',(1800,1250),'#ffffff');dr=ImageDraw.Draw(im)
def font(n,b=False):return ImageFont.truetype('C:/Windows/Fonts/'+('arialbd.ttf' if b else 'arial.ttf'),n)
def tx(x,y,t,n=25,b=False,c='#263e4b'):dr.text((x,y),t,font=font(n,b),fill=c)
tx(60,35,'Alternativa A — abertura e dobradiças',38,True)
tx(60,95,'Duas folhas 67,2 × 30,6 × 1,8 cm • desenho de estudo, sem alteração do CAD',25)

scale=.40;ox=280;oy=755
def xy(x,y):return (ox+(x-5390)*scale,oy-(y-2550)*scale)
def box(bb,fill,outline='#62727a'):
    a=xy(bb[0],bb[1]);b=xy(bb[2],bb[3]);dr.rectangle([min(a[0],b[0]),min(a[1],b[1]),max(a[0],b[0]),max(a[1],b[1])],fill=fill,outline=outline,width=2)
tx(60,155,'Vista de cima — ambas abertas a 86°',27,True)
box([5390,3310,6740,3940],'#eef0ee')
box([5408,3310,6722,3922],'#ffffff')
for x in [5505,6075]:box([x,3410,x+550,3760],'#b4d5d3')
for r in rows:
    pp=base.polygons(r,[86])[0]
    dr.polygon([xy(x,y) for x,y in pp],fill='#c6a67b',outline='#6f583f',width=3)
tx(920,285,'Malas vistas de cima:',25,True)
tx(920,330,'55 × 35 cm cada',25)
tx(920,385,'As folhas avançam 65,7 cm',25)
y=3320;left=xy(two['left_x_mm'],y);right=xy(two['right_x_mm'],y)
dr.line([left,right],fill='#1e7776',width=3)
for x in [left[0],right[0]]:dr.line([(x,left[1]-8),(x,left[1]+8)],fill='#1e7776',width=3)
tx(920,440,'120,3 cm entre folhas',25,True,c='#1e7776')
tx(70,760,'Uma folha a 86°: corredor nominal 60,2 cm; mala de 55 cm deixa 5,2 cm totais.',26,True)
tx(70,805,'Altura entre madeiras: 27,2 cm; mala de 25 cm deixa 2,2 cm. Avanço da porta: 65,7 cm.',25)
tx(70,850,'Corredores excluem corpos das ferragens, mãos e tolerâncias. Abrir ambas facilita o acesso.',24)
tx(70,925,'Mesma frente, melhor espaçamento a investigar',28,True)
tx(70,975,'Extremos a 148 mm: par equivalente 89,1 N. Extremos a 202 mm: 65,2 N (−26,7%).',25)
tx(70,1020,'Hipótese de porta acabada de 4 kg: peso 39,2 N e momento do grupo 13,18 Nm em ambos.',25)
tx(70,1065,'Investigar três dobradiças em 52 / 153 / 254 mm; quantidade e fixações ainda sem aprovação.',25)
tx(70,1140,'672 mm ultrapassam os 650 mm da orientação publicada. Confirmar aplicação e protótipo.',25,True,c='#9a4e38')
tx(70,1190,'Demandas calculadas não comprovam capacidade da ferragem, da chapa ou dos parafusos.',24)
im.save(base.OUT/'Abertura_e_dobradicas_A.png')
print(json.dumps(dict(one_open_mm=one['width_mm'],both_open_mm=two['width_mm'],advance_mm=two['advance_from_closed_front_mm'],
                      minimum_sampled_angles=minimum_angles,bag_paths=len(paths),bag_hits=sum(len(p['hits']) for p in paths),
                      equivalent_pair_reduction_fraction=reduction,source_unchanged=result['source_unchanged']),ensure_ascii=False))
