"""Estudo de luz reproduzível; lê exportações R54, nunca abre/salva FreeCAD.

Fontes comerciais são as da lista curta. Hipóteses não são dados de fabricante.
"""
import argparse
import csv
import copy
import gzip
import hashlib
import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / '03_Ambientes/Iluminacao'
DATE = '29/10/2026'
SOURCES = {
    'N1': ('ABNT NBR ISO/CIE 8995-1:2013, §§4.2–4.4, 4.8, 4.10 e tabela 5/22; texto primário em cópia pública; edição aplicável a confirmar', 'https://drb-assessoria.com.br/drbr/nbrisocie8995.pdf'),
    'N2': ('ABNT NBR 5413:1992, §5.3.65; referência histórica secundária, não declaração de vigência', 'http://ftp.demec.ufpr.br/disciplinas/TM802/NBR5413.pdf'),
    'N3': ('ABNT NBR 5410:2004 corrigida 2008, §§5.1.3.2.2 e 9.1; edição aplicável pelo RT', 'https://universidadeniltonlins.com.br/wp-content/uploads/2019/04/NBR-5410.pdf'),
    'S1': ('Stella: anexos IES /30 e fator de utilização; consulta 29/10', 'https://conhecimento.stella.com.br/hc/pt-br/articles/11888873996311-PLAFON-DE-SOBREPOR-EVO-30W-STH21967-XX'),
    'S2': ('Galaxy, loja oficial: 9608, 2000 lm/25 W/110°/IRC80/IP44; consulta técnica 29/10', 'https://galaxyshop.com.br/plafon-firefly-com-led-integrado-quadrado-ip44-25w-3000k-branco.html'),
    'S3': ('Galaxy, loja oficial: 9605, 2000 lm/25 W/110°/IRC80/IP44; consulta técnica 29/10, preço não transportado', 'https://galaxyshop.com.br/plafon-firefly-com-led-integrado-redondo-ip44-25w-3000k-branco.html'),
    'S4': ('WiZ oficial 929002424712: 800 lm/8,8 W/127 V; não identifica automaticamente a oferta 806 lm/bivolt', 'https://www.wizconnected.com/pt-br/p/lampada-moderna-lampada-60w-a60-e27/8718699787370'),
    'S5': ('Elgin 48D18WSRWIFI: referência comercial 1440 lm/18 W; curva e fluxo por branco ausentes', 'https://www.avantistore.com.br/luminaria-de-sobrepor-redonda-inteligente-18w-3000-6500k-wifi-48d18wsrwifi-elgin'),
    'S6': ('Nordecor EVY2054: 270 lm/3 W/30°/IP20; consulta fabricante 29/10', 'https://nordecor.com.br/produto/arandela-led-pix/'),
    'S7': ('Brilia 314450: 320 lm/3,5 W/3000 K/127 V na tabela, IRC>80; cabeçalho 12 V/0,015 A inconsistente, não usado', 'https://brilia.com/produtos/residencial-e-comercial/mini-g9-35w'),
    'S8': ('Cristallux 221506: 1200 lm/m,12 W/m,12 V,IRC>90; campo0,1 A/m inconsistente, cálculo usa1 A/m', 'https://www.cristallux.com.br/produto/fita-led-cristall-pro-dry-cob-5mt-12v-12w-m-3000k-1200lm-m-ip65-480led-m-irc-90'),
    'S9': ('3R, COB4000K:1200 lm/m,12 W/m,IRC>90; dado comercial, confirmar CLX-FT331240/lote', 'https://www.3reletrica.com.br/fita-de-led-cob-480led/m-ip65-4000k-12v-5-metros-dimerizavel-cristallux'),
    'S10': ('Brilia318939:530 lm/m,4,8 W/m,12 V,3000K,IRC80,IP65; valor comercial já registrado', 'https://www.belluce.com.br/bll604418-fita-de-led-4-8wm-3000k-irc-80-530lmm-12v-angulo-120-brilia-318939'),
    'S11': ('WiZ Pro Kit-C929002681171:1600 lm/20 W/2 m,IRC80,IP20; E05, E06 adiada', 'https://assets.wizconnected.com/datasheets/WiZ_Pro_LED_Strip_RGBTW_2M_Kit-C_929002681171_DS1022.pdf'),
    'S12': ('Shelly Plus RGBW PM:12/24 V CC,<1,2 W,4 A/canal,10 A total,PWM833 Hz/22 kHz; consulta29/10', 'https://kb.shelly.cloud/knowledge-base/shelly-plus-rgbw-pm'),
    'P1': ('Seleção e preços27/10 prevalecem; sem recotação, frete ou instalação', 'Lista_curta_luminarias_e_madeira.md'),
    'P2': ('Alturas nominais2,60/2,50 m; rebaixos e vigas sem cotas verticais confirmadas', '../../01_Programa_e_decisoes/Pesquisa_pe_direito.md'),
    'P3': ('Planta oficial, 1 folha, conferida visualmente29/10; não localiza luminárias', '../../09_Referencias/Plantas_e_manuais/Planta_oficial.pdf'),
    'P4': ('PR-PONTO e contornos nominais, não levantamento da unidade', '../../07_Imovel/Medidas_e_impactos.csv'),
    'P5': ('Comandos funcionais não identificam circuitos/disjuntores/condutores', '../Planta_pontos/README.md'),
    'P6': ('Perfis e fontes; comprimentos existentes C2=1,1 m,S3=1 m,Q06=2 m, não cortes executivos', 'Fechamento_custo_beneficio/Revisao_quarto_CB02.md'),
    'V1': ('Outra unidade espelhada: quatro saídas de teto; foto07:26 conferida29/10', '../../07_Imovel/Complemento/Fotos/AD-0446.jpg'),
    'V2': ('Outra unidade: duas teclas junto ao interfone; função não testada', '../../07_Imovel/Complemento/Fotos/AD-0334.jpg'),
    'V3': ('Outra unidade: três teclas junto à circulação, mão encobre parte', '../../07_Imovel/Complemento/Fotos/AD-0430.jpg'),
    'V4': ('Outra unidade: tomada e interruptor junto ao lavatório/porta', '../../07_Imovel/Complemento/Fotos/AD-0486.jpg'),
    'V5': ('Correspondência corrigida: quartoA→escritório; B→quarto principal; provável', '../../07_Imovel/Complemento/Complemento_da_visita_R02.md'),
}

# Alvos adotados, não uma tabela normativa aplicada a toda residência.
# ambiente, tarefa, altura m, lux mantidos, U0, classificação, fonte
TARGETS = [
    ('sala', 'geral', .75, 150, .4, 'conforto residencial adotado', 'N2 §5.3.65'),
    ('sala', 'mesa/leitura', .75, 500, .7, 'meta residencial para leitura/jogos', 'N2 §5.3.65; N1 analogia tarefa'),
    ('cozinha', 'geral', .75, 150, .4, 'conforto residencial adotado', 'N2 §5.3.65'),
    ('cozinha', 'preparo', .85, 500, .7, 'meta residencial exigente', 'N2 faixa local200–500; N1 analogia tarefa'),
    ('cozinha', 'pia', .85, 300, .7, 'meta residencial adotada', 'N2 §5.3.65'),
    ('lavanderia', 'geral', .75, 150, .4, 'hipótese de conforto', 'H1; N2 analogia'),
    ('lavanderia', 'tanque', .85, 300, .7, 'meta residencial adotada', 'H1; N2 analogia tarefa'),
    ('banho', 'geral', .75, 150, .4, 'hipótese de conforto', 'H1; N2 analogia'),
    ('banho', 'rosto vertical', 1.60, 300, .7, 'meta residencial; faixa de teste150–500', 'H1; não é piso normativo para maquiagem'),
    ('quarto', 'geral', .75, 150, .4, 'conforto residencial adotado', 'N2 §5.3.65'),
    ('quarto', 'leitura cama', .45, 300, .7, 'meta residencial adotada', 'N2 §5.3.65'),
    ('escritorio', 'geral', .75, 150, .4, 'conforto residencial adotado', 'H1; N2 analogia'),
    ('escritorio', 'mesa/monitores', .75, 500, .7, 'referência normativa de tarefa laboral', 'N1 tabela5/22 e§4.3.4; UGR≤19,Ra≥80'),
    ('circulacao', 'piso', 0, 100, .4, 'meta residencial adotada', 'N2 §5.3.65; não iluminação de emergência'),
    ('sala', 'TV', .75, 30, 0, 'faixa de conforto10–50, sem fonte visível/reflexo', 'H1; não requisito normativo'),
]
REFLECTANCES = [
    ('teto branco', .70, .85, 'pintura branca; não medido'),
    ('Algodão Egípcio/off-white', .50, .75, 'paredes claras foscas; não medido'),
    ('Arenza/Beige Matt', .35, .60, 'acabamento areia/fendi; não medido'),
    ('Azul Petróleo/Sauge', .10, .30, 'cores escuras/verde; não medido'),
    ('Itaúnas', .45, .70, 'pedra clara; componente especular não modelado'),
    ('Olmo/greige', .15, .35, 'piso; não medido'),
    ('suede cinza/areia', .20, .50, 'tecido; não medido'),
    ('metal preto/tela apagada', .02, .10, 'difusa apenas; reflexo especular não modelado'),
]
# Fluxos da fonte nua; perdas de vidro/perfil são hipóteses separadas.
PRODUCTS = {
    'C13': dict(room='cozinha', lm=2300, w=30, cct='3000', cri='>90', source='S1', mode='IES', drop=.038),
    'L11': dict(room='lavanderia', lm=2000, w=25, cct='3000', cri='80', source='S2', mode='cos110', drop=.05),
    'B11': dict(room='banho', lm=2000, w=25, cct='3000', cri='80', source='S3', mode='cos110', drop=.05),
    'S03': dict(room='sala', lm=1600, w=17.6, cct='3000 branco de teste; RGB fora da fotometria', cri='80', source='S4', mode='diffuse', drop=.10),
    'E04': dict(room='escritorio', lm=1600, w=17.6, cct='3000 branco de teste; RGB fora da fotometria', cri='80', source='S4', mode='diffuse', drop=.10),
    'Q05': dict(room='quarto', lm=1440, w=18, cct='3000 de teste; ajustável3000–6500', cri='dado ausente', source='S5', mode='diffuse', drop=.05),
    'S04': dict(room='sala', lm=960, w=10.5, cct='3000', cri='>80', source='S7', mode='isotropic', drop=None),
    'Q01': dict(room='quarto', lm=270, w=3, cct='3000', cri='dado ausente', source='S6', mode='cos30', drop=None),
    'Q02': dict(room='quarto', lm=270, w=3, cct='3000', cri='dado ausente', source='S6', mode='cos30', drop=None),
    'C14': dict(room='cozinha', lm=1320, w=13.2, cct='3000', cri='>90', source='S8/P6', mode='strip', length=1.1),
    'S05': dict(room='sala', lm=1200, w=12, cct='3000', cri='>90', source='S8/P6', mode='indirect', length=1),
    'Q06': dict(room='quarto', lm=2400, w=24, cct='3000', cri='>90', source='S8/P6', mode='indirect', length=2),
    'B09': dict(room='banho', lm=1320, w=13.2, cct='4000', cri='>90 comercial', source='S9/P5', mode='mirror', length=1.1),
    'B10': dict(room='banho', lm=1060, w=9.6, cct='3000', cri='80 comercial', source='S10/P5', mode='indirect', length=2),
    'E05': dict(room='escritorio', lm=1600, w=20, cct='3000 de teste; ajustável/RGB', cri='80', source='S11', mode='indirect', length=2),
}


def read_ies(text):
    """LM-63 type C, TILT=NONE, quarter symmetry only; reject unsupported input."""
    if 'TILT=NONE' not in text:
        raise ValueError('Somente TILT=NONE')
    a = [float(x) for x in text.split('TILT=NONE', 1)[1].replace(',', ' ').split()]
    lamps, lm, mult, nv, nh, kind, units, width, length, height = a[:10]
    nv, nh = int(nv), int(nh)
    if kind != 1 or units != 2 or lamps != 1 or len(a) != 13+nv+nh+nv*nh:
        raise ValueError('Cabeçalho IES não suportado ou truncado')
    va, ha = a[13:13+nv], a[13+nv:13+nv+nh]
    if ha[0] != 0 or ha[-1] != 90 or va[0] != 0 or va[-1] != 90:
        raise ValueError('Simetria IES não suportada')
    return dict(lumens=lm, watts=a[12], vertical=va, horizontal=ha,
                cd=[[v*mult for v in a[13+nv+nh+i*nv:13+nv+nh+(i+1)*nv]] for i in range(nh)])


def interpolate(xs, ys, x):
    if x <= xs[0]: return ys[0]
    if x >= xs[-1]: return ys[-1]
    for i in range(1, len(xs)):
        if xs[i] >= x:
            f=(x-xs[i-1])/(xs[i]-xs[i-1])
            return ys[i-1]*(1-f)+ys[i]*f
    raise ValueError(x)


def ies_cd(ies, theta, phi):
    if theta > 90: return 0
    phi=abs(phi)%180
    if phi > 90: phi=180-phi
    rows=[interpolate(ies['vertical'], r, theta) for r in ies['cd']]
    return interpolate(ies['horizontal'], rows, phi)


def cosine_cd(lm, cosine, n=1):
    return lm*(n+1)/(2*math.pi)*max(0,cosine)**n


def illuminance(cd, distance, incidence):
    if distance <= 0: raise ValueError('Distância não positiva')
    return cd*max(0,incidence)/distance**2


def segment_box(a,b,box):
    """Open segment versus axis aligned box; excludes endpoint contact."""
    lo,hi=0.,1.
    for i in range(3):
        d=b[i]-a[i]
        if abs(d)<1e-12:
            if not box[i] < a[i] < box[i+3]: return False
        else:
            u,v=sorted(((box[i]-a[i])/d,(box[i+3]-a[i])/d))
            lo,hi=max(lo,u),min(hi,v)
            if hi <= lo: return False
    return hi>1e-6 and lo<1-1e-6


def write_csv(path, rows):
    rows=list(rows)
    if not rows: return
    with path.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter=';')
        w.writeheader(); w.writerows(rows)


def subtract_box(a,b):
    """Partition a solid box around its intersection with an aperture."""
    lo=[max(a[i],b[i]) for i in range(3)]
    hi=[min(a[i+3],b[i+3]) for i in range(3)]
    if any(hi[i]<=lo[i] for i in range(3)): return [a]
    result=[]; core=list(a)
    for i in range(3):
        for side,v in ((0,lo[i]),(1,hi[i])):
            piece=core[:]
            if side==0: piece[i+3]=v; core[i]=v
            else: piece[i]=v; core[i+3]=v
            if all(piece[j+3]>piece[j] for j in range(3)):result.append(piece)
    return result


def load_geometry():
    sys.path.insert(0,str(ROOT/'ferramentas/pranchas'))
    from gerar import Projeto
    p=Projeto()  # Verifica SHA da exportação, sem abrir o modelo.
    release=json.loads((ROOT/'ferramentas/site/current_release.json').read_text(encoding='utf-8'))
    base=json.loads(gzip.decompress((ROOT/'02_Modelo_3D/Base_verificacao.json.gz').read_bytes()))
    if base['sha256']!=release['cadSHA256'] or p.geo['cad_sha256']!=base['sha256']:
        raise ValueError('Fontes geométricas divergentes; não atualizar a base para passar')
    g=dict(floors={},points={},modules={},walls=[],closed_walls=[],objects={},sha=base['sha256'],heights={})
    for r in p.data['floors']:
        x,y,w,d=[p.m(k).mm/1000 for k in r['refs']]
        g['floors'].setdefault(r['room'],[]).append([x,y,x+w,y+d])
        g['heights'][r['room']]=p.pe(r['room']).mm/1000
    for r in p.data['points']:
        v=[p.m(k).mm for k in r['refs']]
        g['points'][r['id']]=[None if q is None else q/1000 for q in v]
    for n,o in p.modules.items():g['modules'][n]=[v/1000 for v in o['box']]
    for n,o in p.objects.items():g['objects'][n]=[v/1000 for v in o['box']]
    mirror=p.m(p.data['mirror']).mm
    for n in ('Peca188','Peca189','Peca157'):
        b=base['objetos'][n]['caixa_global']
        g['objects'][n]=[v/1000 for v in (mirror-b[3],b[1],b[2],mirror-b[0],b[4],b[5])]
    holes=[]
    for r in p.data['openings']:
        v=[p.m(k).mm for k in r['refs']]
        if len(v)==6 and all(q is not None for q in v):
            x,y,w,d,z,h=[q/1000 for q in v]
            holes.append((r['kind'],[x-.001,y-.001,z,x+w+.001,y+d+.001,z+h]))
    for r in p.data['walls']:
        x,y,w,d=[p.m(k).mm/1000 for k in r['refs']]
        original=[x,y,0,x+w,y+d,g['heights'].get(r['room'],2.6)]
        for destination,only_windows in (('walls',False),('closed_walls',True)):
            pieces=[original]
            for kind,hole in holes:
                if only_windows and kind!='janela':continue
                pieces=[q for b in pieces for q in subtract_box(b,hole)]
            g[destination].extend(pieces)
    return g


def cells(rects, z, step=.25, normal=(0,0,1), vertical=False):
    """Exact partition of a rectangular union, including fractional edge cells."""
    xs=sorted({r[i] for r in rects for i in (0,2)})
    ys=sorted({r[i] for r in rects for i in (1,3)})
    for vals in (xs,ys):
        start,end=vals[0],vals[-1]
        vals[:]=sorted(set(vals+[round(start+i*step,9) for i in range(1,math.ceil((end-start)/step))]))
    result=[]
    for a,b in zip(xs,xs[1:]):
        for c,d in zip(ys,ys[1:]):
            x,y=(a+b)/2,(c+d)/2
            if any(r[0]<=x<=r[2] and r[1]<=y<=r[3] for r in rects):
                point=(x,z,y) if vertical else (x,y,z)
                result.append(dict(point=point,area=(b-a)*(d-c),rect=(a,c,b,d),normal=normal))
    return result


def norm(v):
    d=math.sqrt(sum(x*x for x in v))
    return tuple(x/d for x in v)


def line_sources(code,a,b,normal,count=12):
    return [dict(code=code,position=tuple(a[j]+(b[j]-a[j])*(i+.5)/count for j in range(3)),
                 normal=normal,fraction=1/count) for i in range(count)]


def emitters(g):
    result=[]
    for code,p in PRODUCTS.items():
        if p['mode'] not in ('IES','cos110','diffuse'):continue
        x,y,_=g['points'][code]
        result.append(dict(code=code,position=(x,y,g['heights'][p['room']]-p['drop']),normal=(0,0,-1),fraction=1))
    # Cascata triangular dentro da canopla, não três pontos separados/uma barra linear.
    x,y,_=g['points']['S04']
    for dx,dy,z in ((-.075,-.04,1.625),(.075,-.04,1.775),(0,.08,1.925)):
        result.append(dict(code='S04',position=(x+dx,y+dy,z),normal=(0,0,-1),fraction=1/3))
    for code,cy in (('Q01',1.65),('Q02',2.35)):
        pos=g['points'][code]
        result.append(dict(code=code,position=pos,normal=norm((.6-pos[0],cy-pos[1],.45-pos[2])),fraction=1))
    # Reutiliza1,10 m total nominal, distribuído nos apoios existentes. Não é corte executivo.
    for module,length in (('P13',.625),('P10',.475)):
        b=g['modules'][module]; x=(b[0]+b[3])/2; y=b[1]+.03; z=b[2]-.007
        part=line_sources('C14',(x-length/2,y,z),(x+length/2,y,z),(0,0,-1))
        for e in part:e['fraction']*=length/1.1
        result.extend(part)
    for obj in ('Peca188','Peca189'):
        b=g['objects'][obj];x=(b[0]+b[3])/2;y=b[1]-.001;z=(b[2]+b[5])/2
        part=line_sources('B09',(x-.275,y,z),(x+.275,y,z),(0,-1,0))
        for e in part:e['fraction']*=.5
        result.extend(part)
    return result


SCENARIOS = {
    'baixo':dict(mf=.7,glass=.5,amber=.4,profile=.6,uf=.30),
    'central':dict(mf=.8,glass=.65,amber=.55,profile=.75,uf=.45),
    'alto':dict(mf=.9,glass=.85,amber=.75,profile=.9,uf=.60),
}


def transmission(code,s):
    return s['glass'] if code in ('S03','E04') else s['amber'] if code=='S04' else s['profile'] if code in ('C14','B09') else 1


def direct(cell, lights, s, ies, obstacles):
    point=cell['point']; total=0.
    for e in lights:
        if any(segment_box(e['position'],point,b) for b in obstacles):continue
        delta=tuple(point[i]-e['position'][i] for i in range(3)); d=math.sqrt(sum(x*x for x in delta))
        ray=tuple(v/d for v in delta)
        emission=sum(ray[i]*e['normal'][i] for i in range(3))
        incidence=-sum(ray[i]*cell['normal'][i] for i in range(3))
        if incidence<=0:continue
        code=e['code'];p=PRODUCTS[code];lm=p['lm']*e['fraction']
        if p['mode']=='isotropic':cd=lm/(4*math.pi)
        elif emission<=0:continue
        elif p['mode']=='IES':
            theta=math.degrees(math.acos(min(1,emission)))
            phi=math.degrees(math.atan2(delta[1],delta[0]))
            cd=ies_cd(ies,theta,phi)*2300/ies['lumens']*e['fraction']
        else:
            n=math.log(.5)/math.log(math.cos(math.radians(15 if p['mode']=='cos30' else 55))) if p['mode'] in ('cos30','cos110') else 1
            cd=cosine_cd(lm,emission,n)
        total+=illuminance(cd,d,incidence)*transmission(code,s)*s['mf']
    return total


def statistics(grid,values):
    if not grid:return dict(mean=0,min=0,u0=0,area=0)
    area=sum(c['area'] for c in grid)
    mean=sum(c['area']*v for c,v in zip(grid,values))/area
    return dict(mean=mean,min=min(values),u0=min(values)/mean if mean else 0,area=area)


def calculation_cases(g,step=.25):
    cases=[]
    for room,rects in g['floors'].items():
        z=0 if room=='circulacao' else .75
        grid=cells(rects,z,step)
        # Área útil por envelopes; malha não considera interior de móvel como posto de uso.
        occupied=list(g['modules'].values())
        grid=[c for c in grid if not any(b[0]<c['point'][0]<b[3] and b[1]<c['point'][1]<b[4] and b[2]<z<b[5] for b in occupied)]
        cases.append(dict(id=room+'_geral',room=room,grid=grid,meta=100 if room=='circulacao' else 150,u=.4,z=z))
    specs=[('cozinha_preparo','cozinha',[[5.130,6.370,5.749,7.000]],.85,500),
           ('cozinha_pia','cozinha',[[4.480,6.390,5.130,7.000]],.85,300),
           ('lavanderia_tanque','lavanderia',[[2.550,6.370,3.140,7.000]],.85,300),
           ('sala_mesa','sala',[[6.200,3.700,7.000,5.400]],.79,500),
           ('escritorio_mesa','escritorio',[[2.700,.350,4.700,.700]],.75,500),
           ('quarto_leitura','quarto',[[.400,1.500,.800,1.800],[.400,2.200,.800,2.500]],.45,300)]
    for ident,room,rects,z,meta in specs:
        cases.append(dict(id=ident,room=room,grid=cells(rects,z,min(step,.10)),meta=meta,u=.7,z=z))
    cases.append(dict(id='banho_rosto',room='banho',grid=cells([[4.14,1.35,4.54,1.75]],4.70,min(step,.10),normal=(0,1,0),vertical=True),meta=300,u=.7,z='vertical1,35–1,75'))
    for code in ('cozinha_preparo','cozinha_pia'):
        original=next(c for c in cases if c['id']==code)
        actual=copy.deepcopy(original);actual['id']+='_tampo92';actual['z']=.92
        for c in actual['grid']:c['point']=(*c['point'][:2],.92)
        cases.append(actual)
    person=copy.deepcopy(next(c for c in cases if c['id']=='cozinha_preparo_tampo92'))
    person['id']+='_pessoa';cases.append(person)
    tank=copy.deepcopy(next(c for c in cases if c['id']=='lavanderia_tanque'));tank['id']+='_roupa';cases.append(tank)
    for ident in ('lavanderia_tanque','lavanderia_tanque_roupa'):
        tank=copy.deepcopy(next(c for c in cases if c['id']==ident));tank['id']+='_tampo92';tank['z']=.92
        for c in tank['grid']:c['point']=(*c['point'][:2],.92)
        cases.append(tank)
    closed=copy.deepcopy(next(c for c in cases if c['id']=='circulacao_geral'));closed['id']+='_portas_fechadas';cases.append(closed)
    return cases


def case_lights(case,lights):
    room=case['room'];ids={e['code'] for e in lights if PRODUCTS[e['code']]['room']==room}
    if room=='circulacao':ids={'S03','E04','Q05'}
    elif case['id'].startswith('quarto_geral'):ids={'Q05'}
    elif case['id'].startswith('quarto_leitura'):ids={'Q01','Q02','Q05'}
    elif case['id'].startswith('banho_geral'):ids={'B11'}
    elif case['id'].startswith('lavanderia_'):ids={'L11'}
    return [e for e in lights if e['code'] in ids]


def obstacles_for(g,case):
    walls=g['closed_walls'] if case['id'].endswith('portas_fechadas') else g['walls']
    result=walls+list(g['modules'].values())
    if '_roupa' in case['id']:
        b=g['objects']['Peca157'];result=result+[[b[0],b[1],b[2]-1.2,b[3],b[4],b[2]]]
    if case['id'].endswith('_pessoa'):result=result+[[5.15,6.00,0,5.70,6.35,1.75]]
    return result


def verdict(low,high,meta,u):
    if low['mean']>=meta and low['u0']>=u:return 'atende no cenário'
    if high['mean']<meta or high['u0']<u:return 'não atende no cenário'
    return 'marginal no cenário'


def calculate(g,ies,step=.25):
    lights=emitters(g); rows=[]; grids={}
    for case in calculation_cases(g,step):
        ls=case_lights(case,lights);obstacles=obstacles_for(g,case);stats={}
        inside=all(any(all(b[i]<c['point'][i]<b[i+3] for i in range(3)) for b in g['modules'].values()) for c in case['grid'])
        for name,s in SCENARIOS.items():
            values=[direct(c,ls,s,ies,obstacles) for c in case['grid']]
            stats[name]=statistics(case['grid'],values)
            if name=='central':grids[case['id']]=(case['grid'],values)
        a,b,c=(stats[k] for k in SCENARIOS)
        rows.append(dict(ambiente=case['room'],caso=case['id'],plano_m=case['z'],area_util_m2=round(b['area'],4),
                         media_baixo=round(a['mean'],2),media_central=round(b['mean'],2),media_alto=round(c['mean'],2),
                         minimo_central=round(b['min'],2),uniformidade=round(b['u0'],3),
                         meta_lx=case['meta'],u0_meta=case['u'],veredito='não avaliável: plano dentro da base' if inside else verdict(a,c,case['meta'],case['u']),
                         fonte='P3/P4/R54; '+','.join(sorted({PRODUCTS[e['code']]['source'] for e in ls})),
                         premissa='H3/H5/H6; direta sem reflexões; caixas opacas; branco100%; pontos nominais'))
    return rows,grids


def result_text(g,rows,grids):
    lines=['## Resultados por cômodo e tarefa', '',
        '**Veredito apenas do cenário direto. O desempenho real permanece indeterminado.** A faixa baixo–alto varia manutenção e transmissão; não limita todas as curvas/posições possíveis. Uniformidade é amostrada, não garantia entre pontos nem resultado mantido medido. Indiretas sem coordenadas/reflexões não recebem contribuição inventada.', '',
        '| Caso | Plano m | Área útil m² | Emed baixo–alto lx (central) | Emin lx | U0 | Meta lx/U0 | Veredito condicional |',
        '|---|---|---:|---:|---:|---:|---|---|']
    for r in rows:
        numbers='não avaliável' if r['veredito'].startswith('não avaliável') else f"{r['media_baixo']:.0f}–{r['media_alto']:.0f} ({r['media_central']:.0f})"
        minimum='—' if r['veredito'].startswith('não avaliável') else f"{r['minimo_central']:.0f}"
        uniform='—' if r['veredito'].startswith('não avaliável') else f"{r['uniformidade']:.2f}"
        lines.append(f"| {r['caso']} | {r['plano_m']} | {r['area_util_m2']:.2f} | {numbers} | {minimum} | {uniform} | {r['meta_lx']}/{r['u0_meta']} | {r['veredito']} |")
    lines+=['', '### Fluxo zonal, controle independente da direta', '',
            'H4: FU0,30/0,45/0,60; E=ΣΦútil×FU×FM/área bruta, com FM e transmissões de H3/H5. Sem oclusão explícita, sem uso de FU como multiplicador da grade. A área inclui as zonas sob armários: não comparar diretamente com a média da área útil.', '',
            '| Ambiente | Área bruta m² | Fluxo útil central lm | Emed zonal baixo–alto lx (central) | Fonte |', '|---|---:|---:|---:|---|']
    lights=emitters(g)
    for room,rects in g['floors'].items():
        if room=='circulacao':continue
        area=sum(c['area'] for c in cells(rects,.75))
        codes={e['code'] for e in case_lights(dict(room=room,id=room+'_geral'),lights)}
        values=[];central_flux=0
        for name,s in SCENARIOS.items():
            flux=sum(PRODUCTS[k]['lm']*transmission(k,s) for k in codes)
            values.append(flux*s['uf']*s['mf']/area)
            if name=='central':central_flux=flux
        lines.append(f'| {room} | {area:.3f} | {central_flux:.0f} | {values[0]:.0f}–{values[2]:.0f} ({values[1]:.0f}) | H3–H5; '+','.join(sorted(codes))+' |')
    lines+=['', '### Escuros, sombras e leitura correta', '',
        'Cozinha: P09–P13 bloqueiam raios do teto; C14 está sob P10/P13 em dois trechos0,475/0,625 m, a7 mm da face inferior,30 mm da frente, hipóteses de posição. O cozinheiro e eletrodomésticos adicionais não foram representados como sólidos: sombras do uso podem reduzir mais. Pia/preparo a0,85 m atravessam as caixas inferiores de0,90 m na R54: o zero calculado representa ponto dentro do sólido, não falta de luz. Esses casos são não avaliáveis; usar os resultados físicos no tampo nominal0,92 m. Na lavanderia há a mesma incompatibilidade0,85×0,92; README local cita bancada0,75, divergência documental preservada para compatibilização.', '',
        'Lavanderia: o caso roupa usa todo o envelope100×50 cm, com queda1,20 m, como opaco conservador; não é a transparência real das roupas nem a antiga chapa de ocultação removida. Geral/tanque sem roupa e tanque com roupa estão separados. A alteração observável não define posição final nem mecanismo do varal.', '',
        'Banheiro: B09 foi distribuído em duas barras horizontais0,55 m, centros das propostas R54 Peca188/Peca189, orientadas para o rosto; não copiou as barras verticais do render. Plano do rosto a y=4,70 m,x=4,14–4,54,z=1,35–1,75 m é hipótese H7. P19 é caixa opaca, sem reflexão especular calculada. Pontos a0,75 m não substituem luz no rosto.', '',
        'Leitura: duas áreas de40×30 cm a0,45 m, com EVY apontadas ao centro, hipótese H8; facho30° não é IES. A cama atual mede0,64 m de altura: plano0,45 é o comparador pedido, não a altura real do livro. Posição da cabeça/livro e ajuste do foco continuam pendentes; não usar pico central como prova de cobertura.', '',
        'Circulação: sem luminária dedicada acrescentada. Compara luz emprestada de S03/E04/Q05 e paredes com/sem vãos de portas abertas. O fechamento é envelope conservador, não giro contínuo; indiretas ainda sem posição não cobrem o percurso por inferência. Noite com os quartos apagados exige nova conferência de trajeto, não circulação no escuro.', '',
        'Sala: mesa Berlin aberta170×80 cm, tampo0,79 m, centrada nominalmente no S04. Cascata triangular compacta, bordas inferiores históricas155/170/185 cm mais7,5 cm até o centro luminoso (H9). Não foram espalhados globos ao longo da mesa. TV, quarto/cabeceira e E05 sem implantação não recebem lux de reflexão fictício. Escritório usa faixa frontal livre da mesa, excluindo a traseira ocupada pelos monitores.', '',
        'O efeito do IES original EVO em comparação com sua normalização é2329/2300='+f'{2329/2300:.5f}'+' vezes a contribuição C13 (≈1,26% a mais); não35,65/30. Potência de ensaio e potência do catálogo não escalam automaticamente a iluminância. Mantida pendência de revisão do fabricante.', '',
        '### Mapas e dados', '',
        '[Resumo numérico](Resumo_lux.csv) e [grade resumida](Grades_lux.csv). Mapas mostram direta central a0,75 m (circulação:piso), com escala comum0–500 lx; branco = fora da malha/volume ocupado, contorno = geometria nominal. Não incluem luz natural. Dados detalhados podem ser regenerados externamente.']
    return '\n'.join(lines)+'\n\n'


def write_maps(out,grids,g):
    from PIL import Image,ImageDraw,ImageFont
    font_path=Path('C:/Windows/Fonts/segoeui.ttf')
    font=ImageFont.truetype(str(font_path),16) if font_path.exists() else ImageFont.load_default()
    small=ImageFont.truetype(str(font_path),13) if font_path.exists() else font
    for room in ('sala','cozinha','lavanderia','banho','quarto','escritorio','circulacao'):
        grid,values=grids[room+'_geral'];rs=[c['rect'] for c in grid]
        x0,y0=min(r[0] for r in rs),min(r[1] for r in rs);x1,y1=max(r[2] for r in rs),max(r[3] for r in rs)
        scale=min(500/(x1-x0),360/(y1-y0));image=Image.new('RGB',(640,510),'#f5f3ee');d=ImageDraw.Draw(image)
        d.text((24,15),room+' | direta central, fonte nominal',fill='#243e43',font=font)
        d.text((24,40),'Sem reflexões/luz natural; não é desempenho medido',fill='#4c5758',font=small)
        for c,v in zip(grid,values):
            r=c['rect'];f=min(1,v/500);color=(int(30+222*f),int(80+120*f),int(120-65*f))
            box=(24+(r[0]-x0)*scale,80+(r[1]-y0)*scale,24+(r[2]-x0)*scale,80+(r[3]-y0)*scale)
            d.rectangle(box,fill=color,outline='#f5f3ee')
        for e in emitters(g):
            if PRODUCTS[e['code']]['room']!=room or PRODUCTS[e['code']]['mode'] not in ('IES','diffuse','cos110'):continue
            px=24+(e['position'][0]-x0)*scale;py=80+(e['position'][1]-y0)*scale
            d.ellipse((px-5,py-5,px+5,py+5),fill='#ffffff',outline='#183238',width=2)
            d.text((px+7,py-7),e['code'],font=small,fill='#183238')
        for i in range(500):
            f=i/499;d.line((24+i,465,24+i,480),fill=(int(30+222*f),int(80+120*f),int(120-65*f)))
        d.text((24,485),'0 lx                 200                      400             ≥500 lx',fill='#243e43',font=small)
        image.save(out/f'Mapa_lux_{room}.png',optimize=True)


def sensitivity(g,ies):
    result=[];lights=emitters(g);s=SCENARIOS['central']
    cases=[c for c in calculation_cases(g) if c['id'].endswith('_geral') and c['room']!='circulacao']
    for case in cases:
        ls=case_lights(case,lights)
        for dx,dy in ((0,0),(-.25,0),(.25,0),(0,-.25),(0,.25)):
            shifted=copy.deepcopy(ls)
            for e in shifted:
                if PRODUCTS[e['code']]['mode'] in ('IES','diffuse','cos110'):
                    x,y,z=e['position'];e['position']=(x+dx,y+dy,z)
            st=statistics(case['grid'],[direct(c,shifted,s,ies,obstacles_for(g,case)) for c in case['grid']])
            result.append(dict(caso=case['id'],dx_m=dx,dy_m=dy,media_lx=round(st['mean'],2),minimo_lx=round(st['min'],2),u0=round(st['u0'],3),fonte='H10: sensibilidade±0,25 m, não tolerância medida no vídeo'))
    return result


def update_summary(out,rows):
    path=out/'README.md'
    if not path.exists():return
    text=path.read_text(encoding='utf-8')
    text=text.split('## Fotometria —')[0].rstrip()
    text+='\n\n## Fotometria — cenários de 29/10/2026\n\n[Estudo completo](Estudo_fotometrico.md), [resultados](Resumo_lux.csv), [grade resumida](Grades_lux.csv), [sensibilidade de posição](Sensibilidade_luz.csv) e [fontes/curva/SHA](Fotometria_fontes.json). Valores abaixo são **luz direta mantida no cenário**, sem reflexões; desempenho real indeterminado até fotometria dos conjuntos e implantação. Não é veredito normativo do apartamento.\n\n| Ambiente/geral | Emed central lx (faixa) | U0 | Veredito condicional |\n|---|---:|---:|---|\n'
    for room in ('sala','cozinha','lavanderia','banho','quarto','escritorio','circulacao'):
        r=next(r for r in rows if r['caso']==room+'_geral')
        text+=f"| [{room}](Mapa_lux_{room}.png) | {r['media_central']:.0f} ({r['media_baixo']:.0f}–{r['media_alto']:.0f}) | {r['uniformidade']:.2f} | {r['veredito']} |\n"
    text+='\nMetas residenciais gerais150 lx (circulação100); U0≥0,40 adotado. Tarefas no detalhe: escritório500 lx/U0≥0,70 como referência laboral; rosto em plano vertical separado. Plano0,85 m atravessa bases da cozinha/lavanderia: não avaliar luz dentro da madeira; tampo R54 em0,92 m calculado separadamente. Cozinha: verificar também bancada real e sombras. Indiretas sem posição/reflexões não receberam lux inventados.\n\nVídeo espelhado conferido: quatro saídas de teto no conjunto social/cozinha/serviço, teclas e tomada do banheiro; evidência e limites no estudo. Centros continuam nominais;±25 cm é sensibilidade, não precisão do vídeo. Fontes técnicas29/10: IES EVO recuperado (ensaio2021 divergente do catálogo); Firefly9608/9605 com2000 lm e EVY2054 com270 lm/30°. E06 continua adiada.\n\nReproduzir: `python -B ferramentas/estudos/estudo_fotometrico.py`; teste: `python -B ferramentas/estudos/test_estudo_fotometrico.py`. `--detalhe <pasta externa>` exporta a malha integral. Modelo não aberto; seleção/preços/itens do site preservados. Dados de manutenção, transmissão e distribuição analítica são hipóteses explícitas.\n'
    path.write_text(text,encoding='utf-8')


def generate_results(out,detail=None):
    ies=json.loads((out/'Fotometria_fontes.json').read_text(encoding='utf-8'))['EVO_2021']
    g=load_geometry();rows,grids=calculate(g,ies)
    write_csv(out/'Resumo_lux.csv',rows)
    grade=[]
    for ident,(grid,values) in grids.items():
        if next(r for r in rows if r['caso']==ident)['veredito'].startswith('não avaliável'):continue
        # Grade resumida a cada quatro células; malha completa só externa se pedida.
        for i,(c,value) in enumerate(zip(grid,values)):
            if i%4==0:grade.append(dict(caso=ident,x_m=round(c['point'][0],4),y_m=round(c['point'][1],4),z_m=round(c['point'][2],4),area_celula_m2=round(c['area'],5),lux_direto=round(value,2),fonte='R54/P4; H3–H9; central'))
    write_csv(out/'Grades_lux.csv',grade);write_maps(out,grids,g)
    shifts=sensitivity(g,ies);write_csv(out/'Sensibilidade_luz.csv',shifts)
    report=premises().replace('Resultados espaciais, cenas/consumo e alternativas serão gerados nas próximas etapas deste mesmo arquivo.',result_text(g,rows,grids))
    report=report.replace('## Fontes','## Sensibilidade e reprodução\n\nDeslocamentos±0,25 m dos plafons, um eixo por vez, em [Sensibilidade_luz.csv](Sensibilidade_luz.csv); mantidos fluxos/curvas/obstáculos. Não são incertezas estatísticas nem uma otimização da posição. Células de0,25 m em geral e0,10 m nas tarefas, divididas nas bordas; média ponderada pela área. Mínimo amostrado pode cair numa malha mais fina.\n\nSHA R54: `'+g['sha']+'`. IES original: `'+ies['sha256']+'`. Regeneração não requer FreeCAD; lê a exportação com SHA e a curva numérica pequena. Dependência dos mapas: Pillow.\n\n## Fontes')
    (out/'Estudo_fotometrico.md').write_text(report,encoding='utf-8')
    update_summary(out,rows)
    if detail:
        detail.mkdir(parents=True,exist_ok=True)
        write_csv(detail/'Grade_completa.csv',(dict(caso=k,x_m=c['point'][0],y_m=c['point'][1],z_m=c['point'][2],area_m2=c['area'],lx=v) for k,(cs,vs) in grids.items() for c,v in zip(cs,vs)))
    return g,rows,grids


def premises():
    lines=['# Estudo fotométrico do apartamento', '',
        f'Estudo de {DATE}; hipóteses explícitas, sem seleção de produto ou alteração de orçamento/CAD. Gerado por `ferramentas/estudos/estudo_fotometrico.py`.', '',
        '## Enquadramento e níveis-alvo', '',
        'N1 trata de trabalho interior. Seus 500 lx mantidos, U0≥0,70, UGR≤19 e Ra≥80 são referência da tarefa de escritório; não uma exigência geral para todos os cômodos domésticos. N2 é referência histórica secundária residencial. Edição aplicável precisa ser confirmada pelo RT; a edição internacional ISO/CIE2025 não atualiza automaticamente a adoção ABNT. Os demais valores são metas de conforto deste estudo, não texto de norma.', '',
        '| Ambiente | Tarefa | Plano m | Meta lx | U0 | Natureza e fonte |',
        '|---|---|---:|---:|---:|---|']
    for room,task,z,lx,u,nature,source in TARGETS:
        lines.append(f'| {room} | {task} | {z:g} | {lx} | {u:g} | {nature}; {source} |')
    lines += ['', 'Limpeza usa a geral+tarefas a100%, sem criar piso normativo próprio. Noite adota5–20 lx no percurso como hipótese de conforto, sem equivaler a iluminação de emergência. A meta TV refere-se ao ambiente, não iluminância da tela. Para maquiagem,300 lx verticais é meta de comparação residencial; não diagnóstico de cores ou suficiência para qualquer tarefa fina.', '',
        '## Refletâncias e perdas', '',
        'Acabamentos identificados no `data.js` e na decisão de chapas vigente; cor de imagem/RGB não é refletância fotópica medida. Faixas abaixo são hipóteses H2 de sensibilidade, não fichas dos materiais nem conversão automática de sRGB. Espelho e tela não podem ser tratados como difusores.', '',
        '| Superfície vigente | ρ mínimo | ρ máximo | Premissa |', '|---|---:|---:|---|']
    for label,lo,hi,note in REFLECTANCES: lines.append(f'| {label} | {lo:.2f} | {hi:.2f} | H2: {note} |')
    lines += ['', 'H3: fatores de manutenção0,70/0,80/0,90 (baixo/central/alto); N1§4.8 exige justificar manutenção real, não usar estes fatores como garantia. H4: FU zonal0,30/0,45/0,60 para comparação; não são tabela do fabricante, nem derivados das refletâncias. O FU concentra distribuição e reflexões de forma agregada. A análise direta ponto a ponto não usa FU e não soma reflexão inventada.', '',
        'H5: transmissão Jurerê0,50/0,65/0,85; âmbar0,40/0,55/0,75; perfil/difusor0,60/0,75/0,90. Faixas de ensaio escolhidas pelo estudo, não limites garantidos do produto. H6: distribuidores analíticos sem IES usam cosⁿ; n=1 como difuso e n=ln(0,5)/ln(cos(facho/2)) quando há facho. Um ângulo publicado não determina toda a curva; a aproximação precisa ser substituída pela fotometria do conjunto.', '',
        '## Produtos e rastreabilidade', '',
        '| Grupo | Fluxo nu lm | Potência W | Cor K | IRC | Fonte / limite |', '|---|---:|---:|---|---|---|']
    for code,p in PRODUCTS.items():
        lines.append(f"| {code} | {p['lm']:g} | {p['w']:g} | {p['cct']} | {p['cri']} | {p['source']}; {p['mode']} |")
    lines += ['', 'Fluxos de fitas resultam de comprimento nominal×lm/m. C2/S3/Q06 mantêm os comprimentos já usados em P6; não são comprimentos de compra. B09=2×0,55 m e B10≤2 m em P5; E05=kit2 m. Não há dado de fluxo por branco/RGB ou intensidade regulada; os cálculos funcionais consideram branco a100%. Faltam transmissão/curva dos conjuntos; IRC das EVY e do Elgin não está comprovado nas fontes usadas. Não confundir lista comercial e SKU conciliado.', '',
        'IES EVO obtido diretamente do anexo oficial S1 em29/10: teste31/08/2021,2329 lm/35,65 W; catálogo2300 lm/30 W. A curva original é cenário histórico, não fotometria certificada do lote30 W. Serão mostrados separadamente curva original e comparação normalizada2300/2329; normalizar fluxo não resolve diferença construtiva. Curva numérica pequena preservada em `Fotometria_fontes.json`, com SHA do IES original.', '',
        '## Geometria e evidências do vídeo', '',
        'Planta oficial P3 conferida com a skill PDF; projeções PR-FLOORS e PR-PONTO de P4 fixam o sistema global da prancha em mm. Exportação R54 e modelo são vinculados por SHA. O FreeCAD não é aberto. Os `bounds` do site incluem margens de câmera e não são áreas dos cômodos. Usar união dos retângulos PR-FLOORS sem duplicar sobreposições; excluir footprints de caixas que atravessam o plano apenas na malha útil, mantendo a área bruta separada.', '',
        'Elias,29/10/2026, nesta conversa: “tem imagens de um video de um apartamento semelhante ao meu (só q espelhado)”. V1–V5 foram conferidos: quatro saídas no conjunto social/cozinha/serviço; duas teclas junto ao interfone; três junto à circulação; tomada+interruptor junto ao lavatório. A→Dormitório02/escritório e B→Dormitório01/quarto é a correspondência provável corrigida pela R02. Orientação transferida pelas paredes e vãos da planta, não por inverter coordenadas de pixels. O vídeo sustenta quantidade e região, não centímetros, retorno, neutro ou circuito.', '',
        'Para o cálculo: centros nominais dos pontos existentes; altura do teto2,60 m (banho2,50) menos corpo/hipótese do emissor. Não deduzir novamente forro de uma altura já acabada. Jurerê10 cm de corpo; EVO3,8 cm; Elgin/Firefly5 cm como hipótese, sem dimensão exata comprovada. Rebaixos/vigas sem cotas ficam como perguntas, sem inventar seção. Deslocamento de±25 cm será ensaio de sensibilidade, não precisão atribuída ao vídeo.', '',
        'Planos pedidos0,75/0,85/0,45 m são comparadores; bancadas atuais chegam a0,92 m na cozinha e0,765 no banho; cama atual tem0,64 m. Registrar as duas referências, sem alterar móveis. Plano vertical do rosto separado da horizontal. Portas/varal e armários serão apenas envelopes de oclusão, não simulação contínua de interferências.', '',
        '## Método a executar', '',
        'Fluxo zonal: Emed=ΣΦ×transmissão×FU×FM/área bruta. Direta: E=ΣI(θ,φ)×cos(incidência)/r²×FM, com visibilidade por segmento×caixa; todas as coordenadas convertidas para metros. Não multiplicar a direta por FU novamente. Emed ponderada pela área das células; Emin por amostra e U0=Emin/Emed. Refinar malha só para testar erro numérico, sem redimensionar instalação condicionada.', '',
        'UGR real requer luminância direcional, área luminosa aparente, luminância de fundo e índice de posição. Curva só da lâmpada/alegaçãoUGR<19 não comprova o ambiente. Sem esses dados, registrar indeterminado e risco/reflexo geométrico, sem fabricar um UGR numérico. Luz natural, Ambilight, telas acesas e iluminação do depurador não entram como fluxo conhecido.', '',
        'Resultados espaciais, cenas/consumo e alternativas serão gerados nas próximas etapas deste mesmo arquivo.', '', '## Fontes', '']
    for k,(label,url) in SOURCES.items(): lines.append(f'- **{k}:** [{label}]({url}).')
    return '\n'.join(lines)+'\n'


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--importar-ies',type=Path)
    parser.add_argument('--saida',type=Path,default=OUT)
    parser.add_argument('--detalhe',type=Path)
    args=parser.parse_args(); args.saida.mkdir(parents=True,exist_ok=True)
    if args.importar_ies:
        raw=args.importar_ies.read_bytes(); ies=read_ies(raw.decode('utf-8-sig'))
        ies.update(sha256=hashlib.sha256(raw).hexdigest(),url='https://conhecimento.stella.com.br/hc/pt-br/article_attachments/35841818392983',test_date='31/08/2021')
        (args.saida/'Fotometria_fontes.json').write_text(json.dumps({'EVO_2021':ies},ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8')
    write_csv(args.saida/'Premissas_luz.csv',(dict(zip(('ambiente','tarefa','plano_m','meta_lx','uniformidade','natureza','fonte'),r)) for r in TARGETS))
    g,rows,grids=generate_results(args.saida,args.detalhe)
    print(f'Fotometria:{len(rows)} casos; SHA R54 {g["sha"]}; sem alteração de CAD/site/orçamento.')


if __name__=='__main__': main()
