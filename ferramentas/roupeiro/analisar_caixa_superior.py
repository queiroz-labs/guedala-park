"""Cortes e topologia P01/P02/P03. Sem rigidez ficticia e sem alterar CAD.

python -B ferramentas/roupeiro/analisar_caixa_superior.py
Requer NumPy e Pillow. A saida nao dimensiona conectores nem libera carga.
"""
from pathlib import Path
import csv
import hashlib
import itertools
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / '04_Moveis/Proximas_decisoes/P01_P03'
GEOMETRY = OUT / 'Geometria_P02_individual.json'
D = json.loads(GEOMETRY.read_text(encoding='utf-8'))
G = 9.80665
P = D['panels']
P01 = {n for n,r in P.items() if r['module']=='P01'}
P02 = {n for n,r in P.items() if r['module']=='P02'}
P03 = {n for n,r in P.items() if r['module']=='P03'}
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(ROOT / D['source']) == D['source_sha256']


def total(rows):
    mass = sum(r['mass_kg'] for r in rows)
    return dict(mass_kg=mass, weight_N=mass*G,
                com_mm=[sum(r['mass_kg']*r['com_mm'][i] for r in rows)/mass for i in range(3)])


def wood(v, module, rho):
    names = P02 if module=='P02' else P03
    return [dict(name=n, mass_kg=v['bodies'].get(n,P[n])['volume_mm3']*rho/1e9,
                 com_mm=v['bodies'].get(n,P[n])['com_mm']) for n in sorted(names)]


def prepare(v, uppers):
    points = []
    for c in v['contacts']:
        if c['axis'] != 2 or abs(c['center_mm'][2]-2132)>1e-6:
            continue
        if c['a'] in P01 and c['b'] in uppers:
            lower, upper = c['a'], c['b']
        elif c['b'] in P01 and c['a'] in uppers:
            lower, upper = c['b'], c['a']
        else:
            continue
        for point in c['vertices_mm']:
            points.append(dict(point_mm=point, lower=lower, upper=upper))
    A = np.array([[1., (r['point_mm'][0]-7000)/1000,
                   (r['point_mm'][1]-3290)/1000] for r in points]).T
    triples, inv = [], []
    for ix in itertools.combinations(range(len(points)),3):
        if abs(np.linalg.det(A[:,ix])) < 1e-11:
            continue
        triples.append(ix)
        inv.append(np.linalg.inv(A[:,ix]))
    return dict(points=points, A=A, triples=np.array(triples), inverse=np.array(inv))


def solve(cut, aggregate):
    b = aggregate['weight_N']*np.array([1., (aggregate['com_mm'][0]-7000)/1000,
                                      (aggregate['com_mm'][1]-3290)/1000])
    reactions = np.einsum('kij,j->ki',cut['inverse'],b)
    ok = np.min(reactions,axis=1)>=-1e-7
    if not np.any(ok):
        ymin = min(r['point_mm'][1] for r in cut['points'])
        deficit = aggregate['weight_N']*(ymin-aggregate['com_mm'][1])/1000
        assert deficit>0, 'Este caso exige outro certificado de inviabilidade.'
        return dict(feasible=False, certificate='CG a frente de todos os contatos inferiores',
                    front_contact_y_mm=ymin, minimum_resisting_wrench_about_front_Nm=deficit)
    rr, tt = reactions[ok], cut['triples'][ok]
    env = {}
    for lower in sorted({r['lower'] for r in cut['points']}):
        mask = np.array([r['lower']==lower for r in cut['points']])
        values = np.sum(rr*mask[tt],axis=1)
        env[lower] = dict(min_N=float(values.min()), max_N=float(values.max()))
    # Apenas um certificado de equilibrio. Nao e partilha prevista ou dimensionamento.
    witness = [dict(**cut['points'][int(ix)], force_z_N=float(value))
               for ix,value in zip(tt[0],rr[0])]
    return dict(feasible=True, witness=witness, compression_envelopes_N=env)


positions = {'area_L': [7105.0829875518675,3524.792531120332,2160.],
             'anterior_y3300': [7115.,3300.,2290.],
             'ponta_retorno': [7275.,2920.,2160.]}
cases = []
thresholds = []
sections = []
jointmap = []
for variant,v in D['variants'].items():
    solo, coupled = prepare(v,P02), prepare(v,P02|P03)
    for rho,kg,placement in itertools.product([650,800,900],[0,10,20],positions):
        w02, w03 = wood(v,'P02',rho), wood(v,'P03',rho)
        l02 = w02+[dict(name='conteudo_P02',mass_kg=kg,com_mm=positions[placement])]
        l03 = w03+[dict(name='conteudo_P03',mass_kg=kg,com_mm=[6065.,3320.,2160.])]
        agg02, both = total(l02), total(l02+l03)
        cases.append(dict(id=f'{variant}_rho{rho}_kg{kg}_{placement}',variant=variant,
                          rho_hypothesis_kg_m3=rho,content_each_upper_kg=kg,
                          P02_placement=placement,P02_loads=l02,P03_loads=l03,
                          P02_total=agg02,coupled_total=both,
                          P02_compression_only=solve(solo,agg02),
                          coupled_necessary_cut=solve(coupled,both)))
    upper = P02|P03
    for i,c in enumerate(v['contacts']):
        a,b = c['a'],c['b']
        if a not in upper and b not in upper:
            continue
        pair = {a,b}
        if (a in P01 or b in P01) and c['axis']==2:
            role='Apoio inferior compressivo; junta de retencao separada'
        elif pair=={'Peca259','LateralApoioPrincipal'}:
            role='C01: ligacao positiva face a face P03-P02; quatro estacoes de estudo'
        elif (a in P02 and b in P03) or (b in P02 and a in P03):
            role='Contato cruzado: nao adicionar outra junta independente alem de C01'
        elif pair=={'FaixaQuinaAR04','FaixaQuinaBR04'}:
            role='Quina fixa: nao portante; requer fixacao a caixa atraves da folga2'
        else:
            role='Junta estrutural de painel a detalhar; contato nao fornece rigidez'
        jointmap.append(dict(variant=variant,ref=f'F{i:02}',a=a,b=b,geometry='face',
                             axis='XYZ'[c['axis']],area_mm2=c['area_mm2'],length_mm='',
                             center_mm=c['center_mm'],role=role))
    for i,c in enumerate(v['edge_only']):
        pair = {c['a'],c['b']}
        role=('Fundos P02: sem junta direta creditada; ligar cada fundo a base/topo inteiros'
              if pair=={'Peca255','Peca256'} else
              'P03: sem apoio de face; proposta amplia painel inteiro18 para tras')
        jointmap.append(dict(variant=variant,ref=f'E{i:02}',a=c['a'],b=c['b'],geometry='aresta',
                             axis='',area_mm2=0.,length_mm=c['length_mm'],center_mm='',role=role))

for rho in [650,800,900]:
    w = total(wood(D['variants']['atual_R52'],'P02',rho))
    thresholds.append(dict(rho_hypothesis_kg_m3=rho,P02_wood=w,
        front_line_y_mm=3290.,tip_content_y_mm=2920.,
        necessary_front_y_threshold_content_kg=w['mass_kg']*(w['com_mm'][1]-3290)/370))
    frontrows = [dict(name=r['name'], mass_kg=r['volume_mm3']*rho/1e9, com_mm=r['com_mm'])
                 for r in D['P02_front_cut_parts']['3290']]
    for kg in [0,10,20]:
        ll = frontrows+[dict(name='conteudo_ponta',mass_kg=kg,com_mm=positions['ponta_retorno'])]
        a = total(ll)
        moment = sum(r['mass_kg']*G*(3290-r['com_mm'][1])/1000 for r in ll)
        sections.append(dict(rho_hypothesis_kg_m3=rho,content_tip_kg=kg,loads=ll,
            cut_y_mm=3290.,weight_forward_N=a['weight_N'],moment_x_at_cut_Nm=moment,
            hypothetical_flange_couple_arm_mm=290.,
            axial_pair_if_only_top_base_couple_N=moment/.290))

# Quatro eixos de ESTUDO no encontro lateral18+18. Nao sao furos/CNC/compra.
stations = [dict(id=f'C01_{i+1}',axis='X',start_mm=[6722.,y,z],end_mm=[6758.,y,z])
            for i,(y,z) in enumerate(itertools.product([3370.,3862.],[2210.,2362.]))]
result = dict(geometry_sha256=sha(GEOMETRY),source_sha256=D['source_sha256'],
              assumptions=dict(densities_kg_m3=[650,800,900],gravity_m_s2=G,
                content_each_upper_kg=[0,10,20],P02_positions_mm=positions,
                P03_content_position_mm=[6065.,3320.,2160.],door_pose='R52 salva',
                absent=['massa ferragens','movimento portas P02','impacto','propriedades juntas',
                        'deformacao placas','ancoragens','demais cargas inferiores P01']),
              cases=cases,front_y_thresholds=thresholds,return_sections=sections,
              C01_study_stations=stations,joint_map=jointmap,
              recommendation='Desenvolver caixa com base/topo L inteiros, C01 positivo e topo P03 inteiro650; nao integrar sem validar.',
              limitations=['Corte acoplado e condicao necessaria, nao prova equilibrio de cada painel.',
                           'Envelopes de receptores distintos nao sao necessariamente simultaneos.',
                           'Nao atribuir capacidade a quatro eixos, densidade ou par axial ilustrativo.',
                           'Nao e verificacao de rigidez, resistencia, carga liberada ou furacao.'])
(OUT/'Resultados_topologia.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
with (OUT/'Mapa_juntas.csv').open('w',newline='',encoding='utf-8-sig') as f:
    writer=csv.DictWriter(f,fieldnames=list(jointmap[0]));writer.writeheader();writer.writerows(jointmap)


def draw():
    im=Image.new('RGB',(2000,1460),'white');d=ImageDraw.Draw(im)
    def font(size,bold=False):
        return ImageFont.truetype('C:/Windows/Fonts/'+('arialbd.ttf' if bold else 'arial.ttf'),size)
    def txt(p,s,size=24,color='#233746',bold=False):d.text(p,s,font=font(size,bold),fill=color)
    txt((65,40),'P01 / P03 / P02 — ligações da caixa superior',40,bold=True)
    txt((65,99),'Estudo nominal • R52 preservada • cotas em mm • sem fabricação ou carga liberada',25)
    txt((65,155),'1. PLANTA — portas omitidas para mostrar o caminho',28,bold=True)
    sx=.55;ox=90;oy=255
    def xy(x,y):return (ox+(x-5390)*sx,oy+(y-2890)*sx)
    def rect(b,fill,outline='#3c5363',width=2):d.rectangle((*xy(b[0],b[1]),*xy(b[2],b[3])),fill=fill,outline=outline,width=width)
    rect([5390,3290,7390,3940],'#e9f0f4')
    rect([5408,3290,6722,3940],'#dde9f8')
    poly=[(6740,3310),(7160,3310),(7160,2890),(7390,2890),(7390,3940),(6740,3940)]
    d.polygon([xy(*p) for p in poly],fill='#e1ecd9',outline='#33563d',width=3)
    rect([6722,3310,6758,3922],'#d27631')
    rect([7372,2890,7390,3922],'#496951')
    rect([6740,3922,7372,3940],'#496951')
    x1,y1=xy(5390,3290);x2,y2=xy(7390,3290)
    d.line((x1,y1,x2,y2),fill='#bd3e2f',width=4)
    txt((110,oy+300),'P03: caixa reta',26,bold=True)
    txt((110,oy+338),'P01 fica abaixo da faixa azul',23)
    tx,ty=xy(6780,3530);txt((tx,ty),'P02',27,bold=True)
    tx,ty=xy(6810,3650);txt((tx,ty),'base e topo em L inteiros',21)
    tx,ty=xy(7040,2920);txt((tx-8,ty+2),'Retorno',23)
    tx,ty=xy(7275,2920);d.ellipse((tx-8,ty-8,tx+8,ty+8),fill='#bd3e2f')
    txt((1210,220),'RETORNO EM BALANÇO',26,bold=True)
    txt((1210,268),'400 até a linha de apoio y=3290.',24)
    txt((1210,310),'20 kg na ponta: y=2920 (hipótese).',24)
    txt((1210,352),'Não se equilibra só por compressão',24,color='#a02f26')
    txt((1210,389),'nos apoios inferiores de P01.',24,color='#a02f26')
    txt((1210,450),'C01 — unir as duas laterais18.',25,bold=True)
    txt((1210,493),'A linha laranja tem face612 × 272.',24)
    txt((1210,536),'Os fundos do L só compartilham',24)
    txt((1210,573),'uma aresta272; não são uma junta.',24)
    txt((1210,634),'Linha vermelha = apoio mais frontal.',22)
    txt((65,875),'2. SEÇÃO TRASEIRA P03 — proposta, sem alterar o envelope',28,bold=True)
    x0,y0=100,970;scale=1.05
    def yz(y,z):return(x0+(y-3290)*scale,y0+(2440-z)*scale)
    for b,col in [([3290,2422,3940,2440],'#86a9d1'),([3922,2150,3940,2422],'#779361'),
                  ([3290,2132,3940,2150],'#86a9d1')]:
        d.rectangle((*yz(b[0],b[3]),*yz(b[2],b[1])),fill=col,outline='#233746',width=2)
    d.rectangle((*yz(3922,2440),*yz(3940,2422)),fill='#d27631',outline='#233746',width=2)
    txt((825,970),'Topo P03:632 → 650, chapa inteira.',25,bold=True)
    txt((825,1015),'Acréscimo18 atrás, sobre o fundo.',24)
    txt((825,1060),'Base650 e fundo P01 +18 já eram estudo.',24)
    txt((825,1105),'Sem ampliar o topo, o encontro com o fundo',24)
    txt((825,1145),'também é apenas uma aresta1314.',24)
    txt((825,1205),'Ainda faltam produto, juntas, rigidez e ensaio.',24,color='#a02f26')
    txt((65,1340),'C01: quatro estações preliminares no mapa. Não são quantidade de ferragens nem furação executiva.',23)
    txt((65,1385),'Fonte: faces BREP da R52; cálculo e parâmetros em Resultados_topologia.json.',22)
    im.save(OUT/'Topologia_caixa.png')


draw()
print(json.dumps(dict(cases=len(cases),P02_compression_infeasible=sum(not r['P02_compression_only']['feasible'] for r in cases),
                     coupled_cut_feasible=sum(r['coupled_necessary_cut']['feasible'] for r in cases),
                     source_unchanged=sha(ROOT/D['source'])==D['source_sha256'])))
