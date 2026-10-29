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
import re
from pathlib import Path
import sys
import numpy as np

sys.dont_write_bytecode = True

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
    'S13': ('Radiance/EPFL: implementação primária get_posindex/get_ugr; equações Guth/UGR, consulta29/10', 'https://github.com/LBNL-ETA/Radiance/blob/master/src/util/evalglare.c'),
    'S14': ('Radiance evalglare: fundo CIE Lb=(Ev−Edir)/π; documentação primária', 'https://www.radiance-online.org/learning/documentation/manual-pages/pdfs/evalglare.pdf'),
    'P1': ('Seleção e preços27/10 prevalecem; sem recotação, frete ou instalação', 'Lista_curta_luminarias_e_madeira.md'),
    'P2': ('Alturas nominais2,60/2,50 m; rebaixos e vigas sem cotas verticais confirmadas', '../../01_Programa_e_decisoes/Pesquisa_pe_direito.md'),
    'P3': ('Planta oficial, 1 folha, conferida visualmente29/10; não localiza luminárias', '../../09_Referencias/Plantas_e_manuais/Planta_oficial.pdf'),
    'P4': ('PR-PONTO e contornos nominais, não levantamento da unidade', '../../07_Imovel/Medidas_e_impactos.csv'),
    'P5': ('Comandos funcionais não identificam circuitos/disjuntores/condutores', '../Planta_pontos/README.md'),
    'P6': ('Perfis e fontes; comprimentos existentes C2=1,1 m,S3=1 m,Q06=2 m, não cortes executivos', 'Fechamento_custo_beneficio/Revisao_quarto_CB02.md'),
    'P7': ('Berlin110/170×80 cm, tampo nominal79 cm na R54; fonte vigente29/10', '../Sala_e_jantar/README.md'),
    'P8': ('Cama viúva atual128×188×64 cm; queen só futura', '../Quarto_e_portas/README.md'),
    'P9': ('Cozinha: materiais, aéreos, passagem e bancada nominais', '../Cozinha/README.md'),
    'P10': ('Lavanderia: varal100×50 cm; texto de bancada75 cm diverge da caixa CAD92 cm, não corrigido neste estudo', '../Lavanderia/README.md'),
    'V1': ('Outra unidade espelhada: quatro saídas de teto; foto07:26 conferida29/10', '../../07_Imovel/Complemento/Fotos/AD-0446.jpg'),
    'V2': ('Outra unidade: duas teclas junto ao interfone; função não testada', '../../07_Imovel/Complemento/Fotos/AD-0334.jpg'),
    'V3': ('Outra unidade: três teclas junto à circulação, mão encobre parte', '../../07_Imovel/Complemento/Fotos/AD-0430.jpg'),
    'V4': ('Outra unidade: tomada e interruptor junto ao lavatório/porta', '../../07_Imovel/Complemento/Fotos/AD-0486.jpg'),
    'V5': ('Correspondência corrigida: quartoA→escritório; B→quarto principal; provável', '../../07_Imovel/Complemento/Complemento_da_visita_R02.md'),
    'V6': ('Outra unidade: saída de teto visível no quartoA,09:30; região central, sem escala', '../../07_Imovel/Fotos/dormitorio_A/DRA-01_09m30s.jpg'),
    'V7': ('Outra unidade: saída de teto visível no quartoB,11:30; região central, sem escala', '../../07_Imovel/Fotos/dormitorio_B/DRB-02_11m30s.jpg'),
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
    return dict(lumens=lm, watts=a[12], luminous_width_m=width,luminous_length_m=length,luminous_height_m=height,vertical=va, horizontal=ha,
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
            if b-a<1e-8 or d-c<1e-8:continue
            x,y=(a+b)/2,(c+d)/2
            if any(r[0]<=x<=r[2] and r[1]<=y<=r[3] for r in rects):
                point=(x,z,y) if vertical else (x,y,z)
                result.append(dict(point=point,area=(b-a)*(d-c),rect=(a,c,b,d),normal=normal))
    return result


def norm(v):
    d=math.sqrt(sum(x*x for x in v))
    return tuple(x/d for x in v)


def rect_difference(a,b):
    """Non-overlapping remainder of rectangle a after subtracting b."""
    x,y,X,Y=max(a[0],b[0]),max(a[1],b[1]),min(a[2],b[2]),min(a[3],b[3])
    if X<=x or Y<=y:return [a]
    return [r for r in ((a[0],a[1],x,a[3]),(X,a[1],a[2],a[3]),
                         (x,a[1],X,y),(x,Y,X,a[3])) if r[2]-r[0]>1e-7 and r[3]-r[1]>1e-7]


def hemisphere(rng,n,normal,exponent=1):
    """Cosine-power PDF; exponent=1 samples diffuse projected solid angle."""
    normal=np.asarray(normal,float);u=np.asarray(norm(np.cross(normal,(1,0,0) if abs(normal[0])<.9 else (0,1,0))))
    v=np.cross(normal,u);mu=rng.random(n)**(1/(exponent+1));phi=rng.random(n)*2*math.pi
    return mu[:,None]*normal+np.sqrt(1-mu*mu)[:,None]*(np.cos(phi)[:,None]*u+np.sin(phi)[:,None]*v)


class Radiosity:
    """Diffuse patch transport in lumens. Open boundaries lose energy; no daylight.

    Geometry consists of axis-aligned rectangles with inward/exposed normals.
    Ray tracing is vectorized over rays; patch lookup is deterministic. Transfer
    fractions come from uniform-area, cosine-weighted Monte Carlo (fixed seed).
    Solving outgoing powers rather than irradiance preserves energy even though
    finite-sample factors only satisfy reciprocity statistically.
    """
    def __init__(self,faces,step=.45,rays=512,seed=291026):
        self.faces=[];self.patches=[];self.seed=seed;self.rays=rays
        for axis,plane,sign,rect,rho,label in faces:
            a,b,A,B=rect;nu=max(1,math.ceil((A-a)/step));nv=max(1,math.ceil((B-b)/step))
            axes=[k for k in range(3) if k!=axis];normal=np.zeros(3);normal[axis]=sign
            start=len(self.patches);du=(A-a)/nu;dv=(B-b)/nv
            self.faces.append((axis,plane,sign,rect,axes,nu,nv,start))
            for i in range(nu):
                for j in range(nv):
                    p=np.zeros(3);p[axis]=plane;p[axes]=[a+(i+.5)*du,b+(j+.5)*dv]
                    self.patches.append(dict(point=p,normal=normal,area=du*dv,rho=rho,label=label,axes=axes,du=du,dv=dv))
        self.area=np.array([p['area'] for p in self.patches]);self.rho=np.array([p['rho'] for p in self.patches])
        self.source_cache={};self.sensor_cache={};self.edges=None

    def trace(self,origins,directions):
        origins=np.broadcast_to(origins,directions.shape);count=len(directions)
        distance=np.full(count,np.inf);hit=np.full(count,-1,dtype=np.int32)
        for axis,plane,sign,r,axes,nu,nv,start in self.faces:
            den=directions[:,axis];valid=den*sign < -1e-10
            t=np.divide(plane-origins[:,axis],den,out=np.full(count,np.inf),where=valid)
            valid &= (t>1e-7)&(t<distance)
            ix=np.flatnonzero(valid)
            if not len(ix):continue
            u=origins[ix,axes[0]]+t[ix]*directions[ix,axes[0]]
            v=origins[ix,axes[1]]+t[ix]*directions[ix,axes[1]]
            inside=(u>=r[0])&(u<r[2])&(v>=r[1])&(v<r[3]);ix=ix[inside];u=u[inside];v=v[inside]
            hit[ix]=start+np.minimum(nu-1,((u-r[0])/(r[2]-r[0])*nu).astype(int))*nv+np.minimum(nv-1,((v-r[1])/(r[3]-r[1])*nv).astype(int))
            distance[ix]=t[ix]
        return hit

    def transport(self):
        if self.edges is not None:return
        rng=np.random.default_rng(self.seed);src=[];dst=[];weights=[];escape=[]
        for start in range(0,len(self.patches),32):
            starts=[];directions=[]
            for p in self.patches[start:start+32]:
                origins=np.tile(p['point']+p['normal']*1e-6,(self.rays,1))
                origins[:,p['axes'][0]]+=(rng.random(self.rays)-.5)*p['du']
                origins[:,p['axes'][1]]+=(rng.random(self.rays)-.5)*p['dv']
                starts.append(origins);directions.append(hemisphere(rng,self.rays,p['normal']))
            all_hits=self.trace(np.concatenate(starts),np.concatenate(directions)).reshape(-1,self.rays)
            for offset,hits in enumerate(all_hits):
                counts=np.bincount(hits[hits>=0],minlength=len(self.patches));indices=np.flatnonzero(counts)
                src.extend([start+offset]*len(indices));dst.extend(indices);weights.extend(counts[indices]/self.rays)
                escape.append(float(np.mean(hits<0)))
        self.edges=(np.array(src,int),np.array(dst,int),np.array(weights));self.escape=np.array(escape)

    def solve(self,incident,emitted,rho_index=1):
        self.transport();src,dst,w=self.edges;rho=self.rho[:,rho_index]
        reflected=rho*incident;total=reflected.copy();absorbed=float(((1-rho)*incident).sum())
        lost=float(emitted-incident.sum())
        for iteration in range(500):
            lost+=float(reflected@self.escape)
            incoming=np.bincount(dst,weights=reflected[src]*w,minlength=len(self.patches))
            absorbed+=float(((1-rho)*incoming).sum());reflected=rho*incoming;total+=reflected
            if reflected.sum()<max(1,emitted)*1e-10:break
        # Residual is explicitly retained, not silently counted as absorption.
        residual=float(reflected.sum())
        return total/self.area,dict(emitido_lm=float(emitted),absorvido_lm=absorbed,perdido_lm=lost,
                                   residual_lm=residual,erro_lm=float(emitted-absorbed-lost-residual),iteracoes=iteration+1)

    def sensors(self,grid,rays=1024):
        key=tuple((tuple(c['point']),tuple(c['normal'])) for c in grid)
        if key not in self.sensor_cache:
            rng=np.random.default_rng(self.seed+17);hits=[]
            for start in range(0,len(grid),32):
                starts=[];directions=[]
                for c in grid[start:start+32]:
                    pos=np.array(c['point'])+np.array(c['normal'])*1e-5
                    starts.append(np.tile(pos,(rays,1)));directions.append(hemisphere(rng,rays,c['normal']))
                hits.extend(self.trace(np.concatenate(starts),np.concatenate(directions)).reshape(-1,rays))
            self.sensor_cache[key]=np.array(hits)
        return self.sensor_cache[key]

    def reflected_lux(self,grid,radiosity):
        hits=self.sensors(grid);extended=np.r_[radiosity,0.]
        # L=B/pi, cosine-weighted integral E=pi*mean(L).
        return extended[hits].mean(axis=1)

    def deposit(self,lights,scenario,ies,rays=8192):
        incident=np.zeros(len(self.patches));emitted=0.
        for e in lights:
            key=(e['code'],tuple(e['position']),tuple(e['normal']))
            if key not in self.source_cache:
                rng=np.random.default_rng(self.seed+31);mode=PRODUCTS[e['code']]['mode']
                if mode=='isotropic':
                    dirs=hemisphere(rng,rays,(0,0,1),0);dirs[:,2]*=rng.choice([-1,1],rays)
                elif mode=='IES':
                    angles=[(t+.5,h+2.5) for t in range(90) for h in range(0,360,5)]
                    weights=np.array([ies_cd(ies,t,h)*math.sin(math.radians(t)) for t,h in angles]);weights/=weights.sum()
                    chosen=np.asarray(angles)[rng.choice(len(angles),rays,p=weights)]
                    theta=np.radians(chosen[:,0]+rng.random(rays)-.5);phi=np.radians(chosen[:,1]+5*rng.random(rays)-2.5)
                    dirs=np.column_stack((np.sin(theta)*np.cos(phi),np.sin(theta)*np.sin(phi),-np.cos(theta)))
                else:
                    power=math.log(.5)/math.log(math.cos(math.radians(15 if mode=='cos30' else 55))) if mode in ('cos30','cos110') else 1
                    dirs=hemisphere(rng,rays,e['normal'],power)
                hits=self.trace(np.array(e['position']),dirs)
                self.source_cache[key]=np.bincount(hits[hits>=0],minlength=len(self.patches))/rays
            flux=PRODUCTS[e['code']]['lm']*e['fraction']*transmission(e['code'],scenario)*scenario['mf']
            incident+=self.source_cache[key]*flux;emitted+=flux
        return incident,emitted


def validate_radiosity():
    """Closed empty cube, known Lambertian ceiling emitter: global exact solution.

    For uniform reflectance rho and emitted Phi, mean reflected irradiance over
    ALL enclosing surfaces equals rho*Phi/(A*(1-rho)), irrespective of source
    distribution. Independent sensor estimate also checks the ray integrator.
    """
    faces=[]
    for axis in range(3):
        for plane,sign in ((0,1),(2,-1)):faces.append((axis,plane,sign,(0,0,2,2),(.5,.5,.5),'caixa'))
    engine=Radiosity(faces,step=1,rays=2048);rng=np.random.default_rng(7)
    hits=engine.trace(np.array([1,1,1.999]),hemisphere(rng,65536,(0,0,-1)))
    q=np.bincount(hits[hits>=0],minlength=len(engine.patches))*1000/len(hits)
    B,balance=engine.solve(q,1000);expected=1000*.5/(24*(1-.5))
    grid=[dict(point=p['point'],normal=p['normal'],area=p['area']) for p in engine.patches]
    sampled=statistics(grid,engine.reflected_lux(grid,B))['mean']
    # Independent point solution for a uniform square luminous ceiling in black
    # cavity. Rectangle projected solid angle, not a global energy identity.
    factor=2/math.pi*(2/math.sqrt(5)*math.atan(1/math.sqrt(5)))
    uniform=np.array([250. if p['normal'][2]==-1 else 0. for p in engine.patches])
    point=[dict(point=(1,1,0),normal=(0,0,1),area=1)]
    engine.sensors(point,rays=65536)
    point_value=float(engine.reflected_lux(point,uniform)[0]);analytic=250*factor
    return dict(analitico_lx=expected,calculado_lx=sampled,erro_relativo=abs(sampled-expected)/expected,
                difusor_retangular_analitico_lx=analytic,difusor_retangular_calculado_lx=point_value,
                difusor_retangular_erro_relativo=abs(point_value-analytic)/analytic,**balance)


def room_solids(g,case=None):
    """H13: physical envelopes only; no future queen or deferred shelf E06."""
    solids=[]
    for i,b in enumerate(g['closed_walls'] if case and case['id'].endswith('portas_fechadas') else g['walls']):
        solids.append((b,'parede'+str(i),(.5,.625,.75)))
    for name,b in g['modules'].items():
        if name=='P17':continue  # D06: deferred; not an existing reflector/occluder.
        rho=(.1,.2,.3) if name in ('P09','P10','P11','P12') else (.35,.475,.60)
        solids.append((b,name,rho))
    ids=list(range(77,84))+list(range(113,129))+[84,85,86,88,110,131,134,138,139,140,150,152,155,156,184,185,186,187]
    for i in ids:
        key=f'Peca{i:03d}';b=g['objects'][key]
        rho=(.2,.35,.5) if i in list(range(77,84))+list(range(122,129)) else (.02,.06,.10)
        if i in (84,85,86,110):rho=(.35,.475,.60)
        if i==184:rho=(.45,.575,.70)
        if i==185:rho=(.5,.625,.75)
        solids.append((b,key,rho))
    # Actual bed dimensions from P8; placement centered on historical bed axis is H13.
    solids.append(([.05,1.36,0,1.93,2.64,.64],'viuva_H13',(.2,.35,.5)))
    # Berlin extended task top and kitchen stone; no fake volume down to floor.
    solids.append(([6.2,3.7,.76,7.,5.4,.79],'Berlin_H9',(.35,.475,.60)))
    for name in ('P05','P06'):
        b=g['modules'][name];solids.append(([b[0],b[1],.9,b[3],b[4],.92],'pedra_'+name,(.45,.575,.70)))
    if case and '_roupa' in case['id']:
        b=g['objects']['Peca157'];solids.append(([b[0],b[1],b[2]-1.2,b[3],b[4],b[2]],'roupa_H13',(.2,.35,.5)))
    if case and case['id'].endswith('_pessoa'):
        dx=-.65 if case['id'].startswith('cozinha_pia') else 0
        solids.extend([([5.15+dx,6.00,0,5.70+dx,6.35,1.5],'ombros_H13',(.2,.35,.5)),
                       ([5.29+dx,6.07,1.5,5.56+dx,6.34,1.75],'cabeca_H13',(.2,.35,.5))])
    return solids


def scene_faces(g,case=None):
    solids=room_solids(g,case);air=[]
    for room,rects in g['floors'].items():
        for c in cells(rects,0,20):
            a,b,A,B=c['rect'];h=g['heights'][room];air.append([a,b,0,A,B,h])
            solids.extend([([a,b,-.05,A,B,0],'piso_'+room,(.15,.25,.35)),
                           ([a,b,h,A,B,h+.05],'teto_'+room,(.7,.775,.85))])
    faces=[]
    for b,label,rho in solids:
        for axis in range(3):
            uv=[i for i in range(3) if i!=axis]
            for side,sign in ((0,-1),(3,1)):
                plane=b[axis+side];near=plane+sign*1e-5;rect=(b[uv[0]],b[uv[1]],b[uv[0]+3],b[uv[1]+3]);pieces=[]
                for a in air:
                    if not a[axis]<near<a[axis+3]:continue
                    r=(max(rect[0],a[uv[0]]),max(rect[1],a[uv[1]]),min(rect[2],a[uv[0]+3]),min(rect[3],a[uv[1]+3]))
                    if r[2]<=r[0] or r[3]<=r[1]:continue
                    new=[r]
                    for old in pieces:new=[v for q in new for v in rect_difference(q,old)]
                    pieces.extend(new)
                for other,_,_ in solids:
                    if other is b or not other[axis]<near<other[axis+3]:continue
                    clip=(other[uv[0]],other[uv[1]],other[uv[0]+3],other[uv[1]+3])
                    pieces=[v for q in pieces for v in rect_difference(q,clip)]
                for r in pieces:
                    reflect=rho
                    if label.startswith('P') and axis==2 and sign==1 and plane>=2.4:reflect=(.7,.775,.85)
                    # Mirror front is not turned into a diffuse white reflector.
                    if label=='P19' and axis==1 and sign==-1:reflect=(0,0,0)
                    # Sauge wall in shower zone; split off exact rectangle as H13.
                    if label.startswith('parede') and axis==1 and abs(plane-5.29)<.03:
                        clip=(2.55,0,3.35,2.5);ix=(max(r[0],clip[0]),max(r[1],clip[1]),min(r[2],clip[2]),min(r[3],clip[3]))
                        if ix[2]>ix[0] and ix[3]>ix[1]:
                            faces.append((axis,plane,sign,ix,(.1,.2,.3),'Sauge_H13'))
                            faces.extend((axis,plane,sign,q,reflect,label) for q in rect_difference(r,clip));continue
                    faces.append((axis,plane,sign,r,reflect,label))
    return faces


def clean_grid(rects,z,step,boxes):
    parts=[c['rect'] for c in cells(rects,z,20)]
    for b in boxes:
        if b[2]<=z+1e-7 and b[5]>=z-1e-7:
            parts=[q for r in parts for q in rect_difference(r,(b[0],b[1],b[3],b[4]))]
    return [c for r in parts for c in cells([r],z,step)]


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
    'baixo':dict(mf=.7,glass=.5,amber=.4,profile=.6),
    'central':dict(mf=.8,glass=.65,amber=.55,profile=.75),
    'alto':dict(mf=.9,glass=.85,amber=.75,profile=.9),
}

# Cenas alternativas, não agenda do morador: horas/cena não se sobrepõem no cômodo.
# dias do mês:30 por conforto,22 dias de trabalho no escritório.
SCENES = [
 ('sala','geral',.5,30,{'S03':1}),('sala','leitura/jogos',1,30,{'S03':1,'S04':1}),
 ('sala','relaxar/TV',2.5,30,{'S05':.15}),('sala','noite',.25,30,{'S05':.05}),('sala','limpeza',.1,30,{'S03':1,'S04':1,'S05':1}),
 ('cozinha','geral',.25,30,{'C13':1}),('cozinha','tarefa',1.5,30,{'C13':1,'C14':1}),
 ('cozinha','relaxar/apoio',.25,30,{'C14':.25}),('cozinha','noite',.25,30,{'C14':.1}),('cozinha','limpeza',.1,30,{'C13':1,'C14':1}),
 ('lavanderia','geral',.1,30,{'L11':1}),('lavanderia','tarefa',.25,30,{'L11':1}),
 ('lavanderia','relaxar',0,30,{}),('lavanderia','noite',.05,30,{'L11':1}),('lavanderia','limpeza',.1,30,{'L11':1}),
 ('banho','geral',.15,30,{'B11':1}),('banho','rosto/tarefa',.5,30,{'B11':1,'B09':1}),
 ('banho','relaxar',.15,30,{'B10':1}),('banho','noite',.1,30,{'B10':1}),('banho','limpeza',.1,30,{'B11':1,'B09':1,'B10':1}),
 ('quarto','geral',.25,30,{'Q05':1}),('quarto','leitura lado1',.75,30,{'Q01':1}),
 ('quarto','relaxar',.5,30,{'Q06':.25}),('quarto','noite',.25,30,{'Q06':.05}),('quarto','limpeza',.1,30,{'Q05':1,'Q01':1,'Q02':1,'Q06':1}),
 ('escritorio','geral',.5,30,{'E04':1}),('escritorio','trabalho',8,22,{'E04':1}),
 ('escritorio','relaxar/TV',1.5,30,{'E05':.15}),('escritorio','noite',.15,30,{'E05':.05}),('escritorio','limpeza',.1,30,{'E04':1,'E05':1}),
]
DC_GROUPS={'C14','S05','Q06','B09','B10'}
SHELLY_GROUPS={'C14','S05','Q06'}
COMMON_GROUPS={'C13','L11','B11','B09','B10','Q01','Q02'}


def active_power(code,level,efficiency=.85):
    if not 0<=level<=1:raise ValueError('Intensidade inválida')
    if code in COMMON_GROUPS and level not in (0,1):raise ValueError('Comando comum sem dimerização')
    return PRODUCTS[code]['w']*level/(efficiency if code in DC_GROUPS else 1)


def idle_power(code,efficiency=.85):
    # Provisão superior do consumo publicado<1,2 W, sempre alimentado no cenário.
    return 1.2/efficiency if code in SHELLY_GROUPS else 0


def scene_energy():
    scenes=[];energy=[]
    for room,name,h,days,levels in SCENES:
        codes=[k for k,p in PRODUCTS.items() if p['room']==room]
        powers=[sum(active_power(k,levels.get(k,0),eta)+idle_power(k,eta) for k in codes) for eta in (.9,.8)]
        scenes.append(dict(ambiente=room,cena=name,horas_por_dia=h,dias_mes=days,grupos=';'.join(k+'='+str(v) for k,v in levels.items()) or 'todos apagados',
                           W_baixo=round(powers[0],3),W_alto=round(powers[1],3),kWh_cena_baixo=round(powers[0]*h*days/1000,4),kWh_cena_alto=round(powers[1]*h*days/1000,4),
                           fonte='P1/P5/P6,S12; H11:horas/linearidade/eficiência80–90%; standby smart/fonte desconhecido excluído'))
    for code,p in PRODUCTS.items():
        use=[(h,days,levels.get(code,0)) for room,_,h,days,levels in SCENES if room==p['room']]
        if sum(h*days for h,days,_ in use)>720:raise ValueError('Horas sobrepostas no mês')
        vals=[(sum(active_power(code,b,eta)*h*d for h,d,b in use)+idle_power(code,eta)*720)/1000 for eta in (.9,.8)]
        energy.append(dict(ambiente=p['room'],grupo=code,kWh_mes_baixo=round(vals[0],4),kWh_mes_alto=round(vals[1],4),
                           horas_equivalentes100=round(sum(h*d*b for h,d,b in use),3),standby_conhecido_W='1,2/eficiência' if code in SHELLY_GROUPS else 'não incluído; dado ausente ou comando corta rede',
                           fonte=p['source']+';H11; subtotal, não fatura prevista'))
    return scenes,energy


def circuits():
    result=[]
    for code,p in PRODUCTS.items():
        w=active_power(code,1,.8)+idle_power(code,.8)
        result.append(dict(grupo_funcional=code,ambiente=p['room'],W_entrada_cenario=round(w,3),I_ativa_equivalente_A=round(w/127,4),
                           I_hipotese_FP05_A=round(w/127/.5,4),circuito_real='não identificado',protecao_cabo_capacidade='dado ausente; sem comparação possível',
                           fonte='P5;ENT-02 do vídeo: símbolo iluminação visível, corrente/retornos/unidade não confirmados;H11'))
    return result


def uniform_addition(mean,minimum,target,u):
    """Smallest spatially constant addition satisfying both mean and U0."""
    return max(0,target-mean,(u*mean-minimum)/(1-u))



VISUALS = [
 ('sala','coerência parcial','1 plafon e3 globos nas duas imagens; noite quente e indireta acima do painel; sombras/reflexos ilustrativos; cápsulas aparentam filamento, não MiniG9 real','09_Referencias/Sala_noite_web.webp','S03/S04/S05;P1'),
 ('cozinha','divergência de trecho','1 plafon cozinha+1 lavanderia coerentes; render mostra linha contínua incluindo zona de cocção; C14 técnico são dois trechos sob apoios, não fita comum junto ao cooktop','09_Referencias/Cozinha_noite_web.webp','C13/C14/L11;P5/P6'),
 ('lavanderia','coerência qualitativa','1 plafon como única fonte, sem fita sob aéreo; corpo/posição e intensidade não medem fluxo real; varal está vazio','09_Referencias/Lavanderia_noite_web.webp','L11;S2;V1'),
 ('banho','divergência de geometria/cor','1 plafon real+reflexo no espelho, não2 plafons; duas linhas verticais luminosas no render versus propostas R54 horizontais;4000K não verificável em imagem com balanço de branco; indireta inferior não prova B10 separado','09_Referencias/Banheiro_noite_web.webp','B09/B10/B11;P5;Peca188/189'),
 ('quarto','coerência parcial','1 plafon,2 arandelas e linha de cabeceira; luminária smart/modelo/3000K não verificáveis só por imagem; representa queen futura, não viúva atual','09_Referencias/Quarto_noite_web.webp','Q01/Q02/Q05/Q06;P1'),
 ('escritorio','divergência de escopo','noite mostra linha quente sob prateleira e halo TV; E06/prateleira adiada, só E05/TV nesta etapa; produtos são aproximações; luz da tarefa não comprovada pelo brilho do render','09_Referencias/Escritorio_noite_web.webp','E04/E05;E06 adiada por D06-B27/10'),
]
RISKS = [
 ('R01','alta','mesa escritório/jantar','malhas centrais abaixo da meta de tarefa; indireta/TV não é reforço direto quantificado','fotometria do conjunto e distribuição de tarefa; opções em Alternativas_luz.csv'),
 ('R02','alta','UGR leitura/TV/escritório','UGR dos conjuntos atuais indeterminado; EVO histórico tem cenário H16, sem comprovar o lote30W; demais produtos sem IES/área luminosa','obter IES/LDT e tabelaUGR do conjunto; simular observadores e medir instalação; não inventar índice'),
 ('R03','alta','compatibilidade elétrica','Opus36 W/3 A e Shelly4 A/canal não validam PWM/regulação/térmica nem contatoTramontina; G9/D1 ainda sem ensaio do trio10,5 W','respostasIL04–IL07/IL09;12VCC no controlador, nunca127V em I1; ensaio do trio antes de compra'),
 ('R04','alta','fitas/dissipação','C14/S05/Q06 nominais13,2/12/24 W, mais<1,2 W/controlador;5m de fita=60 W excedem fonte36 W; perfilMOV4329 com fita12 W/m sem capacidade térmica confirmada','manter grupos e confirmar dissipação, área útil, terminais, proteção e temperatura; não alojar fonte no fluxo do depurador/micro'),
 ('R05','alta','banheiro/IP','IP44 do plafon não valida todas as posições; IP65 da fita/IP67 da fonte não protegem cortes/emendas','N3§9.1:volumes pelo RT;IPX7/0,IPX4/1,IPX3/2,IPX1/3 na edição consultada;DR≤30mA§5.1.3.2.2; equipotencialização e classes; confirmar revisão aplicável'),
 ('R06','média','sombra e giro','caixas de aéreos e roupa produzem sombras; cozinha EVO41cm em teto260cm ainda cruza altura do giro nominal; folga histórica13cm não é conferência executiva','preservar abertura integral e acesso; posições/fontes só após coordenação, sem limitar porta/varal para caber luz'),
 ('R07','alta','luz no rosto','300 lx verticais é meta residencial; comparações H15 não comprovam luz instalada; barras inferior/superior e torneira exigem acesso, sem refletância especular modelada','confirmar geometriaB09, IRC do lote, conforto e incidência no rosto; não tomar render com barras verticais como detalhe executivo'),
 ('R08','média','reflexos em telas','difusor/âmbar/linhaLED podem aparecer diretamente ou no reflexo; posição/tilt das telas/olhos e luminância ausentes; janela atrás dos monitores cria contraste','manter luz fora da reflexão especular para observadores; cortina/blackout; teste com tela apagada e acesa; não prometer ausência de reflexo'),
 ('R09','alta','circuitos e consumo','símbolo de iluminação visível no quadro da outra unidade; amperagem/curva/condutor/retornos e correspondência à unidade sem comprovação','RT identifica circuito real e FP/inrush; correnteP/127 é equivalente ativa, não correnteRMS de LED'),
 ('R10','média','fonte documental','EVO2329lm35,65W em2021 versus2300lm30W atual; WiZ800lm127V versus oferta806lmbivolt; Brilia cabeçalho12V versus tabela314450127V','pedir ficha/etiqueta do lote, fotometria e transmissão do conjunto; não transferir dados entre variantes'),
]


def final_text(out,g,ies,rows):
    scenes,energy=scene_energy();cr=circuits();alts=[]
    write_csv(out/'Cenas_luz.csv',scenes);write_csv(out/'Consumo_luz.csv',energy);write_csv(out/'Correntes_luz.csv',cr);write_csv(out/'Alternativas_luz.csv',alts)
    write_csv(out/'Coerencia_imagens_luz.csv',(dict(ambiente=r,status=s,evidencia=e,imagem_noite=p,imagem_dia=p.replace('_noite','_dia'),fonte=f,data_inspecao=DATE) for r,s,e,p,f in VISUALS))
    lines=['## Posições aproximadas pelas fotos do vídeo espelhado', '',
        '| Elemento observado | Localização relativa transferível | Uso no estudo / limite |', '|---|---|---|',
        '| Quatro saídas sociais, V1 | duas na faixa da sala/jantar e duas na faixa cozinha/serviço, interpretação pela continuidade das paredes/vãos | quantidade compatível comS03/S04/C13/L11; não são quatro circuitos nem coordenadas obtidas dos pixels |',
        '| Teto do quartoA, V6/V5 | saída na região central do quarto identificado provavelmente comoDormitório02/escritório | apoia uma geralE04; centroPR-PONTO é nominal, não medido no vídeo |',
        '| Teto do quartoB, V7/V5 | saída na região central doDormitório01/quarto principal provável | apoia uma geralQ05; ponto nominal mantido |',
        '| Interfone, V2 | duas teclas na parede oposta aos equipamentos, perto do interfone | funções cozinha/serviço são hipótese; retorno/neutro não identificados |',
        '| Acesso íntimo, V3 | três teclas junto à circulação e portas | não deduzir três retornos utilizáveis ou três circuitos |',
        '| Banheiro, V4 | placa com tomada+interruptor ao lado do lavatório/porta | posição relativa existe na outra unidade; não classificar volume/IP/circuito pela foto |',
        '| Tomadas da cozinha, V5/K-E01–07 | parede de equipamentos: uma região de entrada, dupla junto à pia, alta e sob a pia, região de cocção | inventário prévio R02: 9 posições em 7 placas, sem duplicar reaparições; não é capacidade/circuito nem posição da unidade de Elias |',
        '| Quadro, ENT-02 | junto à porta de entrada da outra unidade | símbolo de lâmpada visível; amperagem/curva e associação à unidade sem leitura confiável |', '',
        'O espelhamento foi tratado pela relação pia/tanque/janelas/acesso íntimo da plantaP3 e pela correçãoV5, sem presumir que a própria imagem foi espelhada digitalmente. Não foi criado ponto em centímetros a partir da perspectiva. O ensaio±25 cm mostra a consequência de posições aproximadas, sem atribuir essa precisão ao vídeo. Estas evidências acrescentam informação útil de infraestrutura, mas não substituem o quadro/pontos da unidade real.', '',
        '## Cenas, consumo e corrente a127 V', '',
        'H11: perfil de uso ilustrativo, não informado pelo morador. Horas por cena abaixo são mutuamente exclusivas dentro do cômodo; trabalho8 h×22 dias, demais30 dias/mês. Dimerização proporcional à potência é hipótese ideal, sem curva de consumo. Fontes avulsas usam eficiência suposta80–90%, não fichaOpus; incluiu provisão1,2 W de cada Shelly permanentemente alimentado. Standby das WiZ/Elgin/kit/fonte/D1, perdas de cabos e tolerâncias desconhecidos **não estão fechados**. O total é subtotal modelado, não previsão de fatura. Não atribuir standby zero ao produto.', '',
        '| Ambiente | Cena | h/dia ×dias | Grupos e fração de teste | W entrada cenário |', '|---|---|---|---|---:|']
    for r in scenes:lines.append(f"| {r['ambiente']} | {r['cena']} | {r['horas_por_dia']:g}×{r['dias_mes']} | {r['grupos']} | {r['W_baixo']:.1f}–{r['W_alto']:.1f} |")
    lines+=['', 'Circulação: não cria grupo, cena ou consumo duplicado. Geral/limpeza depende de vizinhos e portas; noite não tem cobertura demonstrada. Lavanderia/banho gerais permanecem liga/desliga; não aplicar10% em interruptor comum. B09/B10 são dois comandos comuns separados, não Shelly novos. EVY independentes; Q05/WiZ devem permanecer alimentadas para smart, e o comando físico do Elgin é pendência. S04 usa D1 apenas como candidato. Percentuais0,05/0,10/0,15/0,25/1 são ensaio deste estudo, não mínimo estável nem cenas aceitas por Elias.', '',
        '3000K é base funcional onde escolhida; espelho4000K. WiZ/Elgin em branco ajustável: fluxo nos extremos/RGB desconhecido, portanto não transportar o cenário branco100% para cores. IRC no inventário; IRC80/90 não substitui amostra nem temperatura. Nenhum UGR/cintilação/nível mínimo de dimmer foi deduzido do render.', '',
        '| Ambiente | Subtotal mensal kWh no perfil |', '|---|---:|']
    total=[0.,0.]
    for room in sorted({p['room'] for p in PRODUCTS.values()}):
        v=[sum(r[k] for r in energy if r['ambiente']==room) for k in ('kWh_mes_baixo','kWh_mes_alto')]
        total=[total[i]+v[i] for i in range(2)]
        lines.append(f'| {room} | {v[0]:.2f}–{v[1]:.2f} |')
    lines+=['| **Total parcial** | **'+f'{total[0]:.2f}–{total[1]:.2f}'+'** |', '',
        'Não somar novamente kWh das cenas ao subtotal por grupo: a base de Shelly24h já está incluída uma vez no Consumo_luz.csv. Somar cenas isoladas não cobre as horas restantes de standby. Tarifa não fornecida: sem valor emR$/mês. Consumo real depende de horas, brilho, FP, perdas e standby medidos.', '',
        '[Correntes por grupo](Correntes_luz.csv): Iativa=Pentrada/127. FP desconhecido: IRMS=P/(127×FP), sem limite superior demonstrado; FP0,5 no CSV é só sensibilidade, não dado de fabricante. Soma simultânea dos cenários a100%: '+f'{sum(r["W_entrada_cenario"] for r in cr):.1f} W, {sum(r["I_ativa_equivalente_A"] for r in cr):.2f} A equivalentes ativos'+'. Não atribuir a um circuito único. Projeto de pontos identifica funções, não disjuntor/cabo. Vídeo ENT-02 mostra símbolo de lâmpada no quadro, mas não sustenta curva/corrente ou que seja o quadro desta unidade. **Comparação com capacidade do circuito: indeterminada.**', '',
        '## Ajustes mínimos condicionais e opções', '',
        'O cenário falhar não prova falha do produto instalado. Não há menor alteração executiva demonstrável sem curvas/implantação do conjunto. Para quantificar o tamanho do problema sem escolher produto: acréscimo uniforme ideal ΔE=max(0,meta−Emed,(Umeta×Emed−Emin)/(1−Umeta)). É o menor ΔE espacialmente constante que resolve simultaneamente média eU0 no modelo. Não especifica fonte real; aumentar todos os lúmens preservaU0 e pode continuar falhando.', '',
        '| Caso | Opção de estudo | Emed antes→depois lx | U0 antes→depois | Diferença material |', '|---|---|---:|---:|---|']
    for r in alts:lines.append(f"| {r['caso']} | {r['opcao']} | {r['media_antes']:.0f}→{r['media_depois']:.0f} | {r['u0_antes']:.2f}→{r['u0_depois']:.2f} | {r['delta_material_RS']} |")
    lines+=['', 'H12: opção adicionalJurerê usa apenas preçosP1 de27/10:60,65+2×98,97=R$258,59, sem novo WiZmote se o grupo existente puder controlar o conjunto. Controle novo custaria maisR$117,73 da mesma lista, se necessário; compatibilidade térmica/SKU ainda pendente. Posição de comparação(6,17;4,75;2,50)m não coincide com a canoplaS04, mas sua instalação e abertura dos armários não foram validadas. Não é compra nem solução escolhida. Remanejamentos de perfil/plafon não têm mão de obra, cabos, gesso e acabamento cotados: diferença instalada desconhecida, nunca zero. As três opções geométricas são comparações fixas, não otimização iterativa de instalação condicionada.', '',
        '## Riscos e lacunas', '', '| ID/gravidade | Frente | Evidência | O que resolve |', '|---|---|---|---|']
    for code,severity,where,evidence,fix in RISKS:lines.append(f'| {code}/{severity} | {where} | {evidence} | {fix} |')
    lines+=['', 'UGR em leitura/TV/escritório fica **indeterminado**, com campos necessários em R02. EVO tem cálculo do cenário histórico H16 acima, sem comprovar o lote atual. Reflexos especulares e contraste de telas são riscos separados de UGR. Não foi feito ensaio de segurança elétrica, dissipação, dimerização ou desempenho no imóvel.', '',
        '## Confronto com as imagens dia/noite', '',
        'Doze WebP atuais inspecionados visualmente em29/10, sem regeneração. [Tabela reproduzida](Coerencia_imagens_luz.csv). Não converter pixels em lux ou temperatura Kelvin: exposição, emissão gerada e balanço de branco são desconhecidos.', '',
        '| Ambiente | Situação | Evidência observada |', '|---|---|---|']
    for room,status,evidence,path,source in VISUALS:lines.append(f'| {room} | {status} | {evidence}; {source} |')
    lines+=['', '## Perguntas objetivas', '',
        '1. **Elias:** manter500 lx como meta de leitura/jogos na mesa aberta, ou comparar também uma meta residencial menos exigente de300 lx? Não alterada automaticamente. Para o escritório, a referência de500 lx na tarefa laboral permanece.',
        '2. **Elias:** caso a confirmação fotométrica mantenha o déficit, aceita comparar reforço local de tarefa ou prefere preservar somente luminárias gerais? Não é autorização de compra/novo ponto.',
        '3. **Elias:** para o espelho, prefere avaliar barras horizontais da proposta técnica ou a composição vertical da imagem? Ambas precisam de validação; nenhuma foi escolhida neste estudo.',
        '4. **Fornecedores, dentro das IL existentes:** qual IES/LDT/transmissão do conjunto exato por SKU, branco e difusor? O IES2021 representa o EVO30W atual? Confirmar corrente Cristallux e tensão/cabeçalho G9, PWM/curva térmica da fonte e uso WiZ em plafon fechado.',
        '5. **RT/instalador após documentação/levantamento:** quais circuito/disjuntor/FP/inrush/condutores e retornos efetivos, coordenadas/altura do emissor, rebaixos/vigas, volumes/IP/DR e sombras de uso? Não pedir agora ao morador medidas que ele não possui.', '',
        'Sem produto escolhido, envio a fornecedor, mudança de cota/preço/orçamento, modificação de item do site, publicação ou CAD salvo.']
    return '\n'.join(lines)+'\n\n'


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
    if len(grid)!=len(values):raise ValueError('Malha e valores com tamanhos diferentes')
    if not grid:return dict(mean=0,min=0,u0=0,area=0,e5=None,filtered_min=None,filtered_mean=None,filtered_u0=None,filtered_area=0)
    if any(c['area']<=0 or not math.isfinite(c['area']) or not math.isfinite(v) for c,v in zip(grid,values)):
        raise ValueError('Area/iluminancia invalida')
    area=sum(c['area'] for c in grid)
    mean=sum(c['area']*v for c,v in zip(grid,values))/area
    cumulative=0
    for value,weight in sorted((float(v),c['area']) for c,v in zip(grid,values)):
        cumulative+=weight
        if cumulative>=.05*area:
            e5=value;break
    kept=[(c['area'],float(v)) for c,v in zip(grid,values) if c['area']>=.02-1e-12]
    filtered_area=sum(a for a,v in kept)
    filtered_mean=sum(a*v for a,v in kept)/filtered_area if kept else None
    filtered_min=min(v for a,v in kept) if kept else None
    return dict(mean=mean,min=min(values),u0=min(values)/mean if mean else 0,area=area,e5=e5,
                filtered_min=filtered_min,filtered_mean=filtered_mean,
                filtered_u0=(filtered_min/filtered_mean if filtered_mean else 0) if kept else None,
                filtered_area=filtered_area)


def diagnostic_fields(st,prefix=''):
    """Diagnosticos separados: nao substituem Emin/Emed da malha original."""
    return {prefix+k:round(st[v],6) if st[v] is not None else '' for k,v in (
        ('E5_area_lx','e5'),('Emin_celulas_ge002_lx','filtered_min'),
        ('Emed_celulas_ge002_lx','filtered_mean'),('U0_celulas_ge002','filtered_u0'),
        ('area_celulas_ge002_m2','filtered_area'))}


def calculation_cases(g,step=.25):
    cases=[]
    for room,rects in g['floors'].items():
        z=0 if room=='circulacao' else .75
        grid=cells(rects,z,step)
        # Área útil por envelopes; malha não considera interior de móvel como posto de uso.
        occupied=[[b[0],b[1],min(b[2],z),b[3],b[4],max(b[5],z+.01)] for b,_,_ in room_solids(g) if b[2]<=max(z,1.)]
        grid=clean_grid(rects,z,step,occupied)
        cases.append(dict(id=room+'_geral',room=room,grid=grid,meta=100 if room=='circulacao' else 150,u=.4,z=z))
    specs=[('cozinha_preparo_tampo92','cozinha',[[5.130,6.390,5.749,7.000]],.92,500),
           ('cozinha_pia_tampo92','cozinha',[[4.480,6.390,5.130,7.000]],.92,300),
           ('lavanderia_tanque_tampo92','lavanderia',[[2.550,6.370,3.140,7.000]],.92,300),
           ('sala_mesa','sala',[[6.200,3.700,7.000,5.400]],.79,500),
           ('escritorio_mesa','escritorio',[[2.700,.350,4.700,.700]],.75,500),
           ('quarto_leitura','quarto',[[.400,1.500,.800,1.800],[.400,2.200,.800,2.500]],.85,300)]
    for ident,room,rects,z,meta in specs:
        boxes=[b for b,_,_ in room_solids(g) if b[5]>z+1e-7]
        cases.append(dict(id=ident,room=room,grid=clean_grid(rects,z,min(step,.10),boxes),meta=meta,u=.7,z=z))
    cases.append(dict(id='banho_rosto',room='banho',grid=cells([[4.14,1.35,4.54,1.75]],4.70,min(step,.10),normal=(0,1,0),vertical=True),meta=300,u=.7,z='vertical1,35–1,75'))
    for code in ('cozinha_preparo_tampo92','cozinha_pia_tampo92'):
        person=copy.deepcopy(next(c for c in cases if c['id']==code));person['id']+='_pessoa';cases.append(person)
    tank=copy.deepcopy(next(c for c in cases if c['id']=='lavanderia_tanque_tampo92'))
    tank['id']='lavanderia_tanque_roupa_tampo92';cases.append(tank)
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
    return [b for b,_,_ in room_solids(g,case)]


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
        rows[-1].update(diagnostic_fields(b))
        if '_roupa' in case['id']:
            rows[-1]['veredito']='caso-limite: envelope opaco de roupa; nao e veredito do ambiente'
    return rows,grids


RAD_CACHE={}


def required_scale(grid,base,unit,target,u):
    """Exact feasible interval for a>=0 with mean>=target and every E>=u*mean.

    Scaling a source with poor uniformity can impose an UPPER bound. Do not
    claim an arbitrary larger flux solves a distribution that has no solution.
    """
    mean=statistics(grid,base)['mean'];gain=statistics(grid,unit)['mean']
    lower=0.;upper=math.inf
    constraints=[(gain,target-mean)]+[(k-u*gain,u*mean-b) for b,k in zip(base,unit)]
    for coefficient,needed in constraints:
        if abs(coefficient)<1e-12:
            if needed>1e-9:return None
        elif coefficient>0:lower=max(lower,needed/coefficient)
        else:upper=min(upper,needed/coefficient)
    return (lower,upper) if lower<=upper+1e-9 else None


def option_light(code,pos,normal=(0,0,-1),fraction=1):
    return dict(code=code,position=tuple(pos),normal=normal,fraction=fraction)


def option_patterns(case,g):
    """H14 finite comparison catalogue, not an installation/layout optimization."""
    room=case['room'];grid=case['grid'];points=np.array([c['point'] for c in grid]);center=np.average(points,axis=0,weights=[c['area'] for c in grid])
    yield dict(name='vigente sem acréscimo',family='vigente',shift=0,lights=[],flux=0,watts=0,cost=0,
               effort='sem intervenção adicional; compra vigente continua condicionada',risk='mesmos limites H2/H3/H5/H6/H13; delta material zero só significa nenhum item acrescentado')
    general={'sala':('S03',258.59),'escritorio':('E04',258.59),'quarto':('Q05',134.83),
             'cozinha':('C13',239.4),'lavanderia':('L11',203.9),'banho':('B11',129.),'circulacao':('Q05',134.83)}
    code,price=general[room];height=g['heights'][room]-PRODUCTS[code]['drop']
    axis=0 if room in ('escritorio','cozinha','lavanderia','circulacao') else 1
    # Same bounded three tested translations for every scheme; no continuous claim.
    offsets=(-.15,0,.15)
    for count in (1,2,4,6):
        for shift in offsets:
            positions=[]
            for i in range(count):
                p=center.copy();p[2]=height;p[axis]+=(i-(count-1)/2)*.45;p[1-axis]+=shift
                if not any(r[0]+.18<p[0]<r[2]-.18 and r[1]+.18<p[1]<r[3]-.18 for r in g['floors'][room]):break
                if any(all(b[j]<p[j]<b[j+3] for j in range(3)) for b,_,_ in room_solids(g)):break
                positions.append(p)
            if len(positions)!=count:continue
            yield dict(name=f'geral {count} × {code}',family='geral',shift=shift,lights=[option_light(code,p) for p in positions],
                       flux=count*PRODUCTS[code]['lm'],watts=count*PRODUCTS[code]['w'],cost=round(count*price,2),
                       effort='alto: novos pontos/forro/comandos; posições não compatibilizadas',risk='portas, calor, ofuscamento; SKU/curva ausentes salvo EVO histórico')
    if case['id'].endswith('_geral') or room=='circulacao':return
    if room=='banho':return  # Mirror alternatives have exact equal length in layer comparison.
    # Local profiles: two axes over useful task, no deferred shelf assumed as support.
    rects=[c['rect'] for c in grid];extent=[max(r[i+2] for r in rects)-min(r[i] for r in rects) for i in (0,1)]
    axis=0 if room in ('cozinha','lavanderia','escritorio') else int(extent[1]>extent[0])
    length=min(2.,extent[axis]);center[axis]=(min(r[axis] for r in rects)+max(r[axis+2] for r in rects))/2
    z={'cozinha':1.525,'lavanderia':1.50,'escritorio':1.40,'sala':2.0,'quarto':1.40}[room]
    for count in (1,2,3,4):
        for shift in offsets:
            ls=[]
            for i in range(count):
                a=center.copy();b=center.copy();a[2]=b[2]=z;a[axis]-=length/2;b[axis]+=length/2
                a[1-axis]+=shift+(i-(count-1)/2)*.18;b[1-axis]=a[1-axis]
                part=line_sources('C14',a,b,(0,0,-1),count=8)
                for e in part:e['fraction']*=length/1.1
                ls+=part
            total=count*length
            # Full purchase packs, never prorate a roll or presume leftovers.
            drivers=math.ceil(total/2.7);profiles=math.ceil(total/2)
            cost=math.ceil(total/5)*164.8+drivers*98.91+profiles*33.54
            yield dict(name=f'local {count} perfil COB {length:.2f}m',family='local',shift=shift,lights=ls,flux=1200*total,
                       watts=12*total/.85,cost=round(cost,2),effort='alto: suporte/perfil/fonte e comando comum independente; não pressupõe prateleira E06',
                       risk='suporte/dissipação/calor/contato visual a confirmar; custo sem conexões/comando; fonte80–90% hipótese')


def response_vectors(engine,case,lights,g,ies):
    s=SCENARIOS['central'];q,flux=engine.deposit(lights,s,ies)
    d=np.array([direct(c,lights,s,ies,obstacles_for(g,case)) for c in case['grid']])
    return [d+engine.reflected_lux(case['grid'],engine.solve(q,flux,band)[0]) for band in range(3)]


def comparable_options(g,ies,out):
    results=[];requirements=[]
    for ident,(engine,case,ls,bases,ds) in RAD_CACHE.items():
        if ident.endswith('_pessoa') or '_roupa' in ident or ident.endswith('fechadas') or ident=='banho_rosto':continue
        print('Opções: '+ident,flush=True)
        targets=(300,500) if ident in ('sala_mesa','escritorio_mesa') else (case['meta'],)
        for pattern in option_patterns(case,g):
            # Reject emitters in an opaque box; do not optimize around real conflicts.
            if any(any(all(b[j]<e['position'][j]<b[j+3] for j in range(3)) for b,_,_ in room_solids(g)) for e in pattern['lights']):continue
            increments=response_vectors(engine,case,pattern['lights'],g,ies)
            pos=' | '.join(','.join(f'{v:.3f}' for v in e['position']) for e in (pattern['lights'][0],pattern['lights'][-1])) if pattern['lights'] else 'pontos vigentes'
            for target in targets:
                scales=[required_scale(case['grid'],base,delta,target,case['u']) for base,delta in zip(bases,increments)]
                fluxes=['inviável por distribuição' if v is None else round(v[0]*pattern['flux'],1) for v in scales]
                stats=[statistics(case['grid'],base+delta) for base,delta in zip(bases,increments)]
                meets=[st['mean']>=target and st['u0']>=case['u'] for st in stats]
                requirements.append(dict(caso=ident,meta_lx=target,opcao=pattern['name'],deslocamento_m=pattern['shift'],
                                         lm_adicionais_rho_baixo=fluxes[0],lm_adicionais_rho_central=fluxes[1],lm_adicionais_rho_alto=fluxes[2],
                                         pos_extremos_m=pos,fonte='H14; mínimo para este padrão fixo; fluxos nus S1–S9; H2/H3/H5/H6/H13'))
                row=dict(ambiente=case['room'],caso=ident,meta_lx=target,opcao=pattern['name'],camada=pattern['family'],
                         deslocamento_m=pattern['shift'],fluxo_adicional_lm=round(pattern['flux'],2),pos_extremos_m=pos,
                         W_nominal=round(pattern['watts'],2),I_ativa_127V_A=round(pattern['watts']/127,4),
                         material_parcial_RS=pattern['cost'],instalacao=pattern['effort'],risco=pattern['risk'])
                for name,st,ok in zip(('baixo','central','alto'),stats,meets):
                    row.update({f'Emed_{name}':round(st['mean'],2),f'Emin_{name}':round(st['min'],2),f'U0_{name}':round(st['u0'],4),f'meta_{name}':bool(ok)})
                row.update(fonte='P1 preços27/10; H14 posições/quantidades; H2/H3/H5/H6/H13; fonte/W por branco/curva do conjunto ausentes; sem compra',
                           delta_lx_central=round(stats[1]['mean']-statistics(case['grid'],bases[1])['mean'],2))
                results.append(row)
    write_csv(out/'Alternativas_luz.csv',results);write_csv(out/'Fluxo_necessario_luz.csv',requirements)
    return results


def options_text(options):
    lines=['## Ajustes mínimos condicionais e opções', '',
        'H14: [fluxo necessário por padrão/posição](Fluxo_necessario_luz.csv) resolve exatamente as inequações Emed≥meta e cada Ei≥Umeta×Emed para base+a×resposta. É mínimo entre escalas de um padrão fixo, não mínimo global instalado. Se a resposta piora U0, há também limite superior; distribuição inviável não vira promessa de mais lúmens. Lúmens são adicionais nus, antes de H3/H5. Posições amostradas em −0,15/0/+0,15 m no eixo transversal; não representam intervalo contínuo validado nem tolerância de obra.', '',
        '[Opções comparáveis](Alternativas_luz.csv) usa somente produtos P1/S1–S9: gerais adicionais do mesmo tipo e perfis COB locais independentes. Local não reativa E06 nem supõe prateleira. Compra de rolos/fontes/perfis inteiros, sem ratear sobra: fonte por no máximo2,7 m/32,4 W nominais; capacidade térmica ainda pendente. Não são uma solução executiva nem novos itens da lista de compra. FP/inrush desconhecidos; corrente é P/127, não RMS. W das fitas usa eficiência85% hipotética; faixa80–90% dá W×85/90 a W×85/80.', '',
        'Sóρ varia nas colunas baixo/central/alto; fluxo branco/transmissão/curva ausentes permanecem limitações fora dessa faixa. Sem fotometria do conjunto, cumprir o cenário não comprova produto instalado. Os preços são materiais parciais P1, não custo entregue: instalação/comandos/frete/acessórios sem cotação. WiZ usa preço da oferta sem SKU conciliado; não atribuir preço ao SKU técnico. Troca por lâmpada de maior fluxo no mesmo soquete e refletor de parede: dado ausente no catálogo permitido, sem opção comercial fabricada.', '',
        '| Cômodo/tarefa/meta | Até três menores materiais parciais que cumprem cenárioρcentral | Posições testadas que cumprem |', '|---|---|---|']
    keys=sorted({(r['caso'],r['meta_lx']) for r in options})
    for ident,target in keys:
        valid=[r for r in options if r['caso']==ident and r['meta_lx']==target and r['meta_central']]
        best={}
        for r in sorted(valid,key=lambda r:(r['material_parcial_RS'],-r['U0_central'])):best.setdefault(r['opcao'],r)
        chosen=list(best.values())[:3]
        desc='; '.join(f"{r['opcao']}: R${r['material_parcial_RS']:.2f}, {r['Emed_central']:.0f} lx/U0 {r['U0_central']:.2f}" for r in chosen) or 'nenhuma das opções testadas fecha média e U0; não há três para ranquear'
        position='; '.join(r['opcao']+': '+','.join(str(v['deslocamento_m']) for v in valid if v['opcao']==r['opcao'])+' m' for r in chosen) or 'nenhuma'
        lines.append(f'| {ident} / {target} lx | {desc} | {position} |')
    lines+=['', 'As alternativas que falham também permanecem no CSV. Nenhuma é selecionada; limites por interferência/pontos reais ficam com RT. Metas300/500 lx para sala/escritório coexistem: escolher uma não está implícito no cálculo.', '']
    return '\n'.join(lines)+'\n'


def task_layers(g,ies,out):
    rows=[]
    for ident in ('cozinha_preparo_tampo92','cozinha_pia_tampo92','lavanderia_tanque_tampo92','escritorio_mesa','sala_mesa'):
        engine,case,ls,bases,ds=RAD_CACHE[ident]
        patterns=list(option_patterns(case,g));chosen=[]
        for family in ('local','geral'):
            eligible=[p for p in patterns if p['family']==family and p['shift']==0 and p['name'].startswith(family+' 2')]
            if eligible:chosen.append(eligible[0])
        variants=[ident]
        if ident.startswith('cozinha'):variants.append(ident+'_pessoa')
        if ident.startswith('lavanderia'):variants.append('lavanderia_tanque_roupa_tampo92')
        for variant in variants:
            e,c,_,b,d=RAD_CACHE[variant]
            for pattern in [None]+chosen:
                values=b if pattern is None else [v+a for v,a in zip(b,response_vectors(e,c,pattern['lights'],g,ies))]
                stats=[statistics(c['grid'],v) for v in values]
                row=dict(caso=variant,opcao='vigente' if pattern is None else pattern['name'],fluxo_adicional_lm=0 if pattern is None else round(pattern['flux'],2))
                for name,st in zip(('baixo','central','alto'),stats):row.update({f'Emed_{name}':round(st['mean'],2),f'Emin_{name}':round(st['min'],2),f'U0_{name}':round(st['u0'],3)})
                row['fonte']='H14; mesmos produtos/posições com e sem cabeça+ombros ou envelope opaco de roupa; H2/H3/H5/H6/H13'
                rows.append(row)
    engine,case,ls,bases,ds=RAD_CACHE['banho_rosto']
    for label in ('horizontal R54','vertical imagem','horizontal + geral adicional'):
        lights=copy.deepcopy(ls)
        if label=='vertical imagem':
            lights=[e for e in lights if e['code']!='B09']
            for x in (4.065,4.615):
                line=line_sources('B09',(x,5.139,1.25),(x,5.139,1.80),(0,-1,0))
                for e in line:e['fraction']*=.5
                lights+=line
        if label.endswith('adicional'):lights.append(option_light('B11',(2.95,4.65,2.45)))
        values=response_vectors(engine,case,lights,g,ies)
        row=dict(caso='banho_rosto',opcao=label,fluxo_adicional_lm=2000 if label.endswith('adicional') else 0)
        for name,values in zip(('baixo','central','alto'),values):
            st=statistics(case['grid'],values);row.update({f'Emed_{name}':round(st['mean'],2),f'Emin_{name}':round(st['min'],2),f'U0_{name}':round(st['u0'],3)})
        row['fonte']='H15; B09 mesmo total1,10m/1320lm/13,2W; H7 plano do rosto; vertical posição hipotética da imagem; B11 adicional é opção129,00/P1, não composição vigente'
        rows.append(row)
    # Same selected arandelas, aim at the physical book plane; no new purchase.
    engine,case,ls,bases,ds=RAD_CACHE['quarto_leitura'];aimed=copy.deepcopy(ls)
    for e in aimed:
        if e['code'] in ('Q01','Q02'):
            target=(.6,1.65 if e['code']=='Q01' else 2.35,.85)
            e['normal']=norm(np.array(target)-np.array(e['position']))
    vals=response_vectors(engine,case,aimed,g,ies)
    row=dict(caso='quarto_leitura',opcao='EVY apontadas ao livro0,85m',fluxo_adicional_lm=0)
    for name,vs in zip(('baixo','central','alto'),vals):
        st=statistics(case['grid'],vs);row.update({f'Emed_{name}':round(st['mean'],2),f'Emin_{name}':round(st['min'],2),f'U0_{name}':round(st['u0'],3)})
    row['fonte']='H15; mesmo par270lm/3W cada; orientação nominal ao livro, limites mecânicos e conforto pendentes; sem material adicional, instalação desconhecida';rows.append(row)
    write_csv(out/'Camadas_tarefa_luz.csv',rows)
    lines=['## Camada de tarefa e espelho', '',
           'H15: comparação finita de reforço local e geral; [todos os valores e três faixasρ](Camadas_tarefa_luz.csv). Pessoa tem ombros até1,50 m e cabeça até1,75 m; na pia desloca-se0,65 m em X para ficar diante da pia, sem reutilizar a posição do preparo. Não representa anatomia medida. Roupa permanece envelope totalmente opaco; seu resultado não prevê o tecido real.', '',
           '| Caso | Camada/opção | Emed central lx (baixo–alto) | Emin central / U0 |','|---|---|---:|---|']
    for r in rows:lines.append(f"| {r['caso']} | {r['opcao']} | {r['Emed_central']:.0f} ({r['Emed_baixo']:.0f}–{r['Emed_alto']:.0f}) | {r['Emin_central']:.0f} / {r['U0_central']:.2f} |")
    lines+=['', 'Espelho: horizontais R54 e verticais H15 usam o mesmo1,10 m de COB4000K,13,2 W e1320 lm nus, com mesma hipótese de difusor. Vertical: x4,065/4,615 m,y5,139 m,z1,25–1,80 m; não é cota inferida dos pixels. Material nominal reutilizável, custo de remanejamento/terminações sem cotação (não zero). Variante com segundo plafon acrescenta25 W/2000 lm/R$129,00 parciais; composição vigente tem somente um. A escolha estética não está feita.', '',
            'EVY reorientadas ao livro é outra hipótese de orientação, não troca de luminária nem promessa sobre seu curso mecânico. Reforços locais podem introduzir fonte no campo visual/reflexos; cálculos de lux não autorizam montagem sobre aquecedor, passagem, móveis, varal ou área molhada.', '']
    return '\n'.join(lines)+'\n'


def guth_position(direction,gaze):
    direction=np.asarray(norm(direction));gaze=np.asarray(norm(gaze))
    cosine=float(direction@gaze)
    if cosine<=0:raise ValueError('Fonte fora do hemisfério frontal')
    sigma=math.degrees(math.acos(min(1,cosine)))
    perpendicular=direction-cosine*gaze;length=np.linalg.norm(perpendicular)
    tau=math.degrees(math.acos(float(np.clip(perpendicular[2]/length,-1,1)))) if length>1e-12 else 0.
    if direction[2]<0:raise ValueError('Este observador só usa fonte acima da linha de visão')
    exponent=(35.2-.31889*tau-1.22*math.exp(-2*tau/9))*sigma/1000+(21+.26667*tau-.002963*tau*tau)*sigma*sigma/100000
    return min(16,math.exp(exponent))


def rectangle_solid_angle(eye,corners):
    rays=[np.asarray(norm(np.array(v)-eye)) for v in corners]
    def triangle(a,b,c):
        return 2*math.atan2(abs(float(a@np.cross(b,c))),1+float(a@b+b@c+c@a))
    return triangle(*rays[:3])+triangle(rays[0],rays[2],rays[3])


def specular_hit(source,eye,plane,normal):
    """Mirror a point source across the screen, intersect eye-to-virtual-source."""
    source,eye,plane,normal=map(lambda v:np.asarray(v,float),(source,eye,plane,normal))
    if float((source-plane)@normal)<=0 or float((eye-plane)@normal)<=0:return None
    virtual=source-2*float((source-plane)@normal)*normal;delta=virtual-eye;den=float(delta@normal)
    if abs(den)<1e-12:return None
    t=float((plane-eye)@normal)/den
    if not 0<t<1:return None
    point=eye+t*delta;angle=math.degrees(math.acos(float(np.clip(np.dot(norm(source-point),normal),-1,1))))
    return point,angle


def glare_and_screens(g,ies,out):
    engine,case,_,_,_=RAD_CACHE['cozinha_geral'];e=next(e for e in emitters(g) if e['code']=='C13')
    eye=np.array([5.215,5.0,1.60]);gaze=np.array([0.,1.,0.]);source=np.array(e['position']);delta=source-eye;distance=np.linalg.norm(delta)
    w=ies['luminous_width_m'];length=ies['luminous_length_m'];area=w*length
    if area<=0:raise ValueError('IES não contém abertura luminosa positiva; UGR indeterminado')
    cosine=delta[2]/distance;projected=area*cosine
    theta=math.degrees(math.acos(cosine));phi=math.degrees(math.atan2(-delta[1],-delta[0]))
    intensity=ies_cd(ies,theta,phi)*SCENARIOS['central']['mf'];luminance=intensity/projected
    corners=[source+np.array([dx*w/2,dy*length/2,0]) for dx,dy in ((-1,-1),(1,-1),(1,1),(-1,1))]
    omega=rectangle_solid_angle(eye,corners);position=guth_position(delta,gaze)
    original=dict(e,fraction=ies['lumens']/PRODUCTS['C13']['lm']);q,flux=engine.deposit([original],SCENARIOS['central'],ies)
    observer=[dict(point=eye,normal=gaze,area=1)];ugr_rows=[]
    for band,name in enumerate(('baixo','central','alto')):
        B,_=engine.solve(q,flux,band);background=float(engine.reflected_lux(observer,B)[0])/math.pi
        value=8*math.log10(.25/background*luminance*luminance*omega/position**2)
        ugr_rows.append(dict(cena='somente C13; IES2021 original2329lm',observador_m='5.215,5.000,1.600',olhar='0,1,0',rho=name,
                             area_luminosa_m2=round(area,6),area_projetada_m2=round(projected,6),I_cd=round(intensity,3),L_cd_m2=round(luminance,2),
                             omega_sr=round(omega,7),Guth=round(position,5),Lb_cd_m2=round(background,3),UGR=round(value,2),
                             fonte='S1 cabeçalho LM63; S13/S14; H16 observador e abertura uniforme; H13 fundo difuso; sem outras fontes'))
    write_csv(out/'UGR_luz.csv',ugr_rows)
    screens=[('TV_sala','sala','Peca088',0,1,(6.75,2.65,1.10)),
             ('TV_escritorio','escritorio','Peca131',0,-1,(3.10,2.05,1.10)),
             ('monitor_esquerdo','escritorio','Peca115',1,1,(3.70,1.,1.20)),
             ('monitor_direito','escritorio','Peca117',1,1,(3.70,1.,1.20))]
    reflections=[]
    for label,room,obj,axis,sign,observer in screens:
        box=g['objects'][obj];plane=np.array([(box[i]+box[i+3])/2 for i in range(3)]);plane[axis]=box[axis+3] if sign==1 else box[axis]
        normal=np.zeros(3);normal[axis]=sign;other=[i for i in range(3) if i!=axis]
        for index,e in enumerate(x for x in emitters(g) if PRODUCTS[x['code']]['room']==room):
            hit=specular_hit(e['position'],observer,plane,normal);inside=False;blocked=False;angle='';point=''
            if hit:
                p,angle=hit;inside=all(box[i]<=p[i]<=box[i+3] for i in other)
                blocked=any(segment_box(e['position'],p,b) or segment_box(p,observer,b) for b,name,_ in room_solids(g) if name!=obj)
                point=','.join(f'{v:.4f}' for v in p);angle=round(angle,3)
            reflections.append(dict(tela=label,emissor=e['code']+'_'+str(index+1),olho_m=','.join(map(str,observer)),
                                    fonte_m=','.join(f'{v:.4f}' for v in e['position']),intersecao_m=point,angulo_inc_ref_graus=angle,
                                    centro_na_tela=inside,caminho_obstruido=blocked,
                                    resultado='centro aparece no cenário geométrico' if inside and not blocked else 'centro não aparece no cenário geométrico',
                                    fonte='H17 espelho plano, orientação/olho nominais; envelopes R54 Peca088/131/115/117; dimensões visíveis do SKU/tilt ausentes'))
    write_csv(out/'Reflexos_telas_luz.csv',reflections)
    lines=['## UGR e reflexos geométricos', '',
        'H16: UGR=8 log10[(0,25/Lb)Σ(L²ω/p²)], com índice Guth S13 e fundo Lb=Evertical_refletida/π S14. Observador em(5,215;5,000;1,600)m, olhar horizontal+Y, apenas EVO aceso. IES2021 original2329 lm, abertura luminosa0,354×0,354 m do cabeçalho LM63, manutenção0,80. L=I/Aprojetada, área uniforme em cada direção como hipótese de cálculo; ω calculado pelas duas faces triangulares do retângulo aparente. Não se copiou UGR<19 do catálogo. Não é a cena cozinha completa, pois C14 não tem IES/área luminosa conciliados.', '',
        '| ρ | Lb cd/m² | L EVO cd/m² | ω sr | Guth | UGR no cenário EVO |','|---|---:|---:|---:|---:|---:|']
    for r in ugr_rows:lines.append(f"| {r['rho']} | {r['Lb_cd_m2']:.2f} | {r['L_cd_m2']:.0f} | {r['omega_sr']:.5f} | {r['Guth']:.3f} | {r['UGR']:.1f} |")
    lines+=['', '[Entradas e resultado UGR](UGR_luz.csv). Abertura2021 e luminância média não demonstram distribuição de luminância do difusor/lote30W atual; UGR desse lote continua pendente. Demais luminárias: **indeterminado** até IES/LDT do conjunto, dimensões luminosas/área aparente, luminância direcional por branco e condições de montagem. Fundo/observador acima são H13/H16, não medidos.', '',
            'H17: para telas apagadas, reflete-se a fonte no plano da tela e intersecta-se a reta olho→fonte virtual. Incidência=reflexão; só conta se o ponto fica dentro do envelope da tela e os dois segmentos estão visíveis. [Todas as coordenadas/ângulos](Reflexos_telas_luz.csv). Olhos sentados são hipóteses explícitas; orientação sem inclinação é do envelope R54. Monitor27/24 atual pode divergir dos envelopes R54: não é medição da área ativa dos novos SKUs. Não se calculou intensidade do reflexo, porque faltam BRDF/haze/revestimento. Centro fora não exclui reflexo parcial de um difusor finito.', '',
            '| Tela / olho nominal m | Centros de fontes que aparecem | Incidência=reflexão |','|---|---|---|']
    for label,room,obj,axis,sign,observer in screens:
        rr=[r for r in reflections if r['tela']==label and r['centro_na_tela'] and not r['caminho_obstruido']]
        lines.append('| '+label+' / '+','.join(map(str,observer))+' | '+(', '.join(r['emissor'] for r in rr) or 'nenhum dos centros testados')+' | '+(', '.join(str(r['angulo_inc_ref_graus'])+'°' for r in rr) or 'ver interseções fora da tela no CSV')+' |')
    lines+=['', 'S05/E05/Q06 e Ambilight: implantação/área luminosa ausentes, reflexo indeterminado. Janela, tela acesa e luz natural não estão nesta cena; ausência de um centro testado não promete tela sem reflexos no uso.', '']
    return '\n'.join(lines)+'\n'


def decision_summary(out):
    """Readable choices from the generated tables; never a chosen product."""
    def read(name):
        with (out/name).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=';'))
    options=read('Alternativas_luz.csv');layers=read('Camadas_tarefa_luz.csv')
    def best(ident,target,family=None):
        rows=[r for r in options if r['caso']==ident and float(r['meta_lx'])==target and r['meta_central']=='True' and (family is None or r['camada']==family)]
        return min(rows,key=lambda r:(float(r['material_parcial_RS']),float(r['W_nominal']))) if rows else None
    def describe(r):
        if r is None:return 'nenhuma opção testada cumpre média e U0 no cenário central'
        return f"{r['opcao']}: {float(r['Emed_central']):.0f} lx/U0 {float(r['U0_central']):.2f}, material parcial R${float(r['material_parcial_RS']):.2f}"
    texts=['## Perguntas objetivas e consequências numéricas', '',
           '**Cenários, não escolhas.** As faixas completas estão nos CSV; números abaixo usamρcentral/H13 e preços parciais P1, sem instalação/frete/comando novo. A menor opção do catálogo testado não é o mínimo de mercado nem solução de obra.', '',
           '1. **Mesa da sala:300 ou500 lx?** Para300: '+describe(best('sala_mesa',300))+'. Para500: '+describe(best('sala_mesa',500))+'. A exigência de U0 mantém o mesmo menor pacote testado nas duas metas; não há economia demonstrada só por baixar a média.',
           '2. **Escritório:300 residencial ou500 lx laboral; aceita reforço local?** '+describe(best('escritorio_mesa',300))+', em nenhuma das duas metas. Confirmar área efetiva de trabalho e sombras dos equipamentos antes de compra; não descartar pontos escuros apenas para subir U0.',
           '3. **Sala:reforço local ou somente geral?** Local500: '+describe(best('sala_mesa',500,'local'))+'. Somente geral300: '+describe(best('sala_mesa',300,'geral'))+'. Somente geral500: '+describe(best('sala_mesa',500,'geral'))+'.',
           '4. **Espelho:horizontal ou vertical?** '+ '; '.join(f"{r['opcao']}: {float(r['Emed_central']):.0f} lx/U0 {float(r['U0_central']):.2f}" for r in layers if r['caso']=='banho_rosto')+'. Mesmo1,10 m de fita nas duas orientações; relocalização/terminações ainda sem cotação.', '',
           '**Dados faltantes e destinatários:** WiZ/Taschibra:SKU, branco e conjunto fechado/difusor; Stella:IES do lote30W/abertura; Galaxy/Elgin/Nordecor:curva, abertura e fluxo por branco; Cristallux:corrente/fluxo/curva; Brilia:tensãoG9; Opus/Shelly:PWM, perdas e corrente; fornecedores nos [rascunhos IL02–IL09](Fechamento_custo_beneficio/Revisao_quarto_CB02.md#consultas-aos-fornecedores--rascunhos-não-enviados), sem envio. RT/instalador:posição, área de tarefa, circuito, retornos, teto e interferências após levantamento. Não transformar resposta estética em autorização de compra.', '',
           '[Prompts de correção por cômodo](../../09_Referencias/README.md#prompts-de-correção-da-luz--rascunhos29102026): apenas rascunhos; nenhuma imagem gerada/substituída.']
    return '\n\n'.join(texts)+'\n'


def calculate_reflections(g,ies,rows,grids):
    engines={};balances=[];total_grids={};lights=emitters(g)
    for case in calculation_cases(g):
        kind=case['id'] if case['id'].endswith('_pessoa') else 'roupa' if '_roupa' in case['id'] else 'fechadas' if case['id'].endswith('portas_fechadas') else 'abertas'
        if kind not in engines:
            print('Radiosidade: geometria '+kind,flush=True)
            engines[kind]=Radiosity(scene_faces(g,case));engines[kind].transport()
        engine=engines[kind];ls=case_lights(case,lights);q,emitted=engine.deposit(ls,SCENARIOS['central'],ies)
        row=next(r for r in rows if r['caso']==case['id']);ds=np.array(grids[case['id']][1]);stats=[];vectors=[]
        for band,name in enumerate(('baixo','central','alto')):
            B,balance=engine.solve(q,emitted,band);ref=engine.reflected_lux(case['grid'],B);total=ds+ref
            st=statistics(case['grid'],total);stats.append(st);vectors.append(total)
            row.update({f'ref_media_{name}':round(st['mean'],2),f'ref_minimo_{name}':round(st['min'],2),
                        f'ref_u0_{name}':round(st['u0'],6),f'ganho_{name}_lx':round(st['mean']-row['media_central'],2)})
            row.update(diagnostic_fields(st,'ref_'+name+'_'))
            row['veredito_ref_'+name]=verdict(st,st,case['meta'],case['u'])
            balances.append(dict(caso=case['id'],rho=name,patches=len(engine.patches),**{k:round(v,9) for k,v in balance.items()}))
        row['veredito_ref']=verdict(stats[0],stats[2],case['meta'],case['u'])+' com interreflexão H13; três faixas rho'
        if '_roupa' in case['id']:
            row['veredito_ref']='caso-limite: bloqueio por envelope opaco de roupa, nao conclusao sobre uso real'
            for name in ('baixo','central','alto'):row['veredito_ref_'+name]='caso-limite, sem veredito'
        total_grids[case['id']]=(case['grid'],vectors[1])
        RAD_CACHE[case['id']]=(engine,case,ls,vectors,ds)
    return total_grids,balances,engines


def result_text(g,rows,grids):
    lines=['## Método e resultados por cômodo', '',
        '**H13: interreflexão difusa nominal, não medida.** FU fixo H4 foi retirado. As três faixas abaixo variam somente ρ (H2); manutenção/transmissão ficam centrais H3/H5, para isolar a contribuição refletida. Direta baixo/alto no CSV ainda varia manutenção/transmissão. Nenhuma faixa é intervalo estatístico nem cobre todas as curvas ausentes.', '',
        'Radiosidade: patches retangulares ≤0,45 m; Fij estimado por 512 raios por patch, origem uniforme na área e direção cossenoidal, semente291026. Potências refletidas p=ρ(q+Fᵀp), em lm; B=p/A e L=B/π. Sensor usa1024 direções cossenoidais e Eref=π×média(L); fontes8192 raios/emissor. A direta continua analítica com visibilidade. Perdas pelas aberturas e resíduo iterativo são explícitos em [Energia_luz.csv](Energia_luz.csv). A conservação não prova precisão espacial; reciprocidade é estatística e o erro Monte Carlo depende da malha. NumPy e Pillow nas ferramentas locais.', '',
        'H13/material: paredes Algodão Egípcio0,50/0,625/0,75; teto e topo branco0,70/0,775/0,85; piso Olmo/greige0,15/0,25/0,35; Arenza/Beige/Louro representados por0,35/0,475/0,60; P09–P12 azul e parede Sauge do box0,10/0,20/0,30; tecido0,20/0,35/0,50; eletros/telas0,02/0,06/0,10; pedra0,45/0,575/0,70. São as faixas H2 atribuídas aos acabamentos vigentes, não refletâncias reais medidas. P19 espelho frontal temρdifusa=0: componente especular excluída, energia não devolvida ao campo difuso. Vidro/janela e porta exterior: aberturaρ=0 e fuga integral como limite conservador; sem luz natural. Portas interiores abertas deixam luz atravessar; caso fechado usa parede clara como envelope conservador.', '',
        'H13/geometria: faces expostas dos envelopes R54, paredes com vãos, pisos e tetos por união exata; recorte por sólidos e limite interior. Mesma sombra em direta/refletida. P17/E06 adiado excluído. Cama viúva128×188×64 colocada nominalmente no eixo da reserva, cabeceira x0,05 e centro y2,00 m; não é medida de instalação. Mesa Berlin aberta H9. Caixa de roupa conservadora separada. Sem vidro especular, formas curvas, pessoas móveis ou luz de grupos ainda sem implantação.', '',
        'Malhas: geral0,75 m exclui projeções de móveis/equipamentos baixos e paredes; piso da circulação idem. Tarefas usam somente superfície útil, sem purificador/escorredor/PC. Planos0,85 m dentro das bases foram retirados: cozinha/tanque somente tampo0,92 m. Livro passa a0,85 m, acima da cama real0,64 m; foco das EVY permanece nominal H8 e deve ser ajustado no uso. Não comparar esse resultado com a antiga leitura0,45 m como se apenas ρ tivesse mudado. Lux zero remanescente pode ser sombra física, nunca é removido por ser baixo.', '']
    for room in ('sala','cozinha','lavanderia','banho','quarto','escritorio','circulacao'):
        lines += ['### '+room, '', '| Plano/caso | Área m² | Direta Emed / Emin / U0 | Com reflexão Emed baixo / central / alto | Emin central / U0 | Ganho central lx | Veredito por cenário |','|---|---:|---|---|---|---:|---|']
        for r in rows:
            if r['ambiente']!=room:continue
            lines.append(f"| {r['caso']} ({r['plano_m']} m) | {r['area_util_m2']:.2f} | {r['media_central']:.1f} / {r['minimo_central']:.1f} / {r['uniformidade']:.2f} | {r['ref_media_baixo']:.1f} / {r['ref_media_central']:.1f} / {r['ref_media_alto']:.1f} | {r['ref_minimo_central']:.1f} / {r['ref_u0_central']:.2f} | {r['ganho_central_lx']:.1f} | direta: {r['veredito']}; reflexão: {r['veredito_ref']} |")
        lines.append('')
    lines+=['[Resumo completo](Resumo_lux.csv): mínimos/U0 nas três faixas. [Malha resumida](Grades_lux.csv), [superfícies por material](Superficies_luz.csv), [validação](Validacao_luz.json). Mapas: total direto+refletido central, mesma legenda0–500 lx para todos; branco é fora da malha. Não há luz natural.', '']
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
        d.text((24,15),room+' | direta + reflexao, rho central',fill='#243e43',font=font)
        d.text((24,40),'H13: reflexao difusa nominal; sem luz natural',fill='#4c5758',font=small)
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


def reading_plane_comparison(out,rows):
    current=next(r for r in rows if r['caso']=='quarto_leitura')
    # Registro primario do CSV em git 66083a0; nao e novo calculo da geometria R54 limpa.
    comparison=[dict(plano_m=.45,origem='Resumo_lux.csv no commit 66083a0',
        direta_media_lx=499.83,direta_min_lx=378.71,direta_U0=.758,
        total_rho_baixo_lx='',total_rho_central_lx='',total_rho_alto_lx='',
        veredito_original='atende no cenario historico',
        uso_atual='comparador historico invalido como plano de leitura: abaixo da cama de 0,64 m'),
        dict(plano_m=.85,origem='recalculo vigente com geometria limpa H13',
        direta_media_lx=current['media_central'],direta_min_lx=current['minimo_central'],direta_U0=current['uniformidade'],
        total_rho_baixo_lx=current['ref_media_baixo'],total_rho_central_lx=current['ref_media_central'],total_rho_alto_lx=current['ref_media_alto'],
        veredito_original=current['veredito_ref'],
        uso_atual='plano nominal do livro acima da cama; EVY com orientacao nominal H8')]
    write_csv(out/'Comparacao_planos_leitura.csv',comparison)
    return comparison


def externalize_report_tables(report,out):
    """Preserva todas as celulas das tabelas Markdown em um CSV unico indexado."""
    lines=report.splitlines();result=[];records=[];section='';i=0;table=0
    while i<len(lines):
        line=lines[i]
        if line.startswith('#'):section=line.lstrip('# ').strip()
        if line.startswith('|') and i+1<len(lines) and re.fullmatch(r'[| :\-]+',lines[i+1]):
            table+=1
            split=lambda text:[c.strip().replace('\\|','|') for c in re.split(r'(?<!\\)\|',text.strip()[1:-1])]
            headers=split(line);i+=2;number=0
            while i<len(lines) and lines[i].startswith('|'):
                values=split(lines[i]);number+=1
                if len(values)!=len(headers):raise ValueError('Tabela com colunas inconsistentes: '+section)
                records.append(dict(tabela=table,secao=section,linha=number,
                    colunas=json.dumps(headers,ensure_ascii=False),valores=json.dumps(values,ensure_ascii=False)))
                i+=1
            result.append(f'[Tabela {table}: {section} — {number} linhas](Tabelas_estudo_luz.csv).')
        else:
            result.append(line);i+=1
    write_csv(out/'Tabelas_estudo_luz.csv',records)
    return '\n'.join(result)+'\n'


def update_summary(out,rows):
    path=out/'README.md'
    if not path.exists():return
    text=path.read_text(encoding='utf-8')
    text=text.split('## Fotometria —')[0].rstrip()
    with (out/'Alternativas_luz.csv').open(encoding='utf-8-sig',newline='') as f:options=list(csv.DictReader(f,delimiter=';'))
    tasks={'sala':('sala_mesa',500),'cozinha':('cozinha_pia_tampo92',300),'lavanderia':('lavanderia_tanque_tampo92',300),
           'banho':('banho_geral',150),'quarto':('quarto_leitura',300),'escritorio':('escritorio_mesa',500),'circulacao':('circulacao_geral',100)}
    text+='\n\n## Fotometria — cenários de 29/10/2026\n\n[Estudo](Estudo_fotometrico.md), [resultados](Resumo_lux.csv), [tabelas detalhadas](Tabelas_estudo_luz.csv), [grade](Grades_lux.csv) e [fontes](Fotometria_fontes.json). Direta e interreflexão difusa H13, com fontes centrais e faixas de refletância. Desempenho real indeterminado até fotometria e implantação. **As colunas diagnósticas não demonstram atendimento normativo.**\n\n| Ambiente/geral | Direta lx | Total ρbaixo–alto (central) lx | E5% central lx | U0 original / filtrado | Metas originais: baixo / central / alto | Menor opção testada para a tarefa, cenário central |\n|---|---:|---:|---:|---:|---|---|\n'
    for room in ('sala','cozinha','lavanderia','banho','quarto','escritorio','circulacao'):
        r=next(r for r in rows if r['caso']==room+'_geral')
        ident,target=tasks[room];valid=[v for v in options if v['caso']==ident and float(v['meta_lx'])==target and v['meta_central']=='True']
        best=min(valid,key=lambda v:(float(v['material_parcial_RS']),float(v['W_nominal']))) if valid else None
        short=(best['opcao']+f", {float(best['Emed_central']):.0f} lx, R${float(best['material_parcial_RS']):.2f} parcial") if best else 'sem opção testada que cumpra média e U0'
        short=ident.replace('_tampo92','')+': '+short
        u=f"{r['ref_u0_central']:.2f}" if r['ref_u0_central']>=.01 else '<0,01'
        filtered=r['ref_central_U0_celulas_ge002'];fu=f'{filtered:.3f}' if filtered!='' else 'não calculável'
        labels=['cumpre' if r['veredito_ref_'+b]=='atende no cenário' else 'não cumpre' for b in ('baixo','central','alto')]
        text+=f"| [{room}](Mapa_lux_{room}.png) | {r['media_central']:.0f} | {r['ref_media_baixo']:.0f}–{r['ref_media_alto']:.0f} ({r['ref_media_central']:.0f}) | {r['ref_central_E5_area_lx']:.2f} | {u} / {fu} | {' / '.join(labels)} | {short} |\n"
    current=next(r for r in rows if r['caso']=='quarto_leitura')
    text+='\n**E5%** é o percentil de 5% ponderado pela área: primeira iluminância cuja área acumulada alcança 5%, sem interpolação. **U0 original** permanece Emin/Emed de toda a malha. **U0 filtrado** usa somente células com área ≥0,02 m² e recalcula tanto o mínimo quanto a média nessa área; área retida está no CSV. Não substitui U0 normativo, não elimina sombras físicas e não muda os vereditos originais ou a escolha da menor opção. Malhas de tarefa de 10 cm têm células ≤0,01 m²: o filtro fica vazio, marcado como não calculável, sem engrossar a malha para favorecer o resultado.\n'
    text+='\n**Leitura no quarto — comparação dos planos:** [dados e origem](Comparacao_planos_leitura.csv).\n\n| Plano | Direta média / mínimo / U0 | Total H13, ρ baixo–alto | Interpretação |\n|---|---|---|---|\n| 0,45 m histórico, commit 66083a0 | 499,83 / 378,71 lx / 0,758 | não calculado naquela revisão | antigo “atende”; abaixo do topo da cama atual de 0,64 m, não representa leitura atual |\n'
    text+=f"| 0,85 m atual | {current['media_central']:.2f} / {current['minimo_central']:.2f} lx / {current['uniformidade']:.3f} | {current['ref_media_baixo']:.2f}–{current['ref_media_alto']:.2f} lx | {current['veredito_ref']} |\n"
    text+='\nA mudança de conclusão envolve plano e limpeza da geometria/obstáculos, não apenas refletância; não é comparação controlada de uma única variável. A orientação nominal das EVY também afeta a leitura. **Tanque com roupa** é caso-limite de envelope totalmente opaco: o zero calculado não é veredito da lavanderia com qualquer roupa real. O cenário sem roupa continua separado.\n'
    text+='\nMetas residenciais gerais150 lx (circulação100); U0≥0,40 adotado. Tarefas no detalhe: escritório500 lx/U0≥0,70 como referência laboral; rosto em plano vertical separado. Malha limpa: cozinha/tanque somente no tampo0,92 m; livro0,85 m acima da viúva atual. Mínimos escuros fora de sólidos não são descartados. Cozinha: verificar também bancada real e sombras. Indiretas sem posição/reflexões não receberam lux inventados.\n\nVídeo espelhado conferido: quatro saídas de teto no conjunto social/cozinha/serviço, teclas e tomada do banheiro; evidência e limites no estudo. Centros continuam nominais;±25 cm é sensibilidade, não precisão do vídeo. Fontes técnicas29/10: IES EVO recuperado (ensaio2021 divergente do catálogo); Firefly9608/9605 com2000 lm e EVY2054 com270 lm/30°. E06 continua adiada.\n\nReproduzir: `python -B ferramentas/estudos/estudo_fotometrico.py`; teste: `python -B ferramentas/estudos/test_estudo_fotometrico.py`. `--detalhe <pasta externa>` exporta a malha integral. Modelo não aberto; seleção/preços/itens do site preservados. Dados de manutenção, transmissão e distribuição analítica são hipóteses explícitas.\n'
    scenes,energy=scene_energy()
    low=sum(r['kWh_mes_baixo'] for r in energy);high=sum(r['kWh_mes_alto'] for r in energy)
    text+='\n[Cenas e horas](Cenas_luz.csv), [consumo por grupo](Consumo_luz.csv), [correntes](Correntes_luz.csv), [opções numéricas](Alternativas_luz.csv) e [coerência dia/noite](Coerencia_imagens_luz.csv). Subtotal modelado no perfil de uso: **'+f'{low:.2f}–{high:.2f} kWh/mês'+'**, incluindo provisão Shelly24h, sem standby desconhecido das demais fontes/smart. Não é previsão de fatura; grupos não identificam circuitos. [UGR EVO](UGR_luz.csv) calculado para cena/observador H16; demais conjuntos indeterminados. [Reflexos em telas](Reflexos_telas_luz.csv) têm olho/orientação nominal H17.\n'
    path.write_text(text,encoding='utf-8')
    with path.open('a',encoding='utf-8') as f:
        f.write('\nMotor de radiosidade H13 integrado; resultados totais e balanços no estudo e CSV. Caixa vazia validada (<3% frente à solução analítica) e conservação com abertura. Dependências: NumPy e Pillow nas ferramentas locais.\n')


def generate_results(out,detail=None):
    if not (out/'Fotometria_fontes.json').exists():
        (out/'Fotometria_fontes.json').write_bytes((OUT/'Fotometria_fontes.json').read_bytes())
    ies=json.loads((out/'Fotometria_fontes.json').read_text(encoding='utf-8'))['EVO_2021']
    g=load_geometry();rows,grids=calculate(g,ies)
    reflected,balances,engines=calculate_reflections(g,ies,rows,grids)
    write_csv(out/'Energia_luz.csv',balances)
    (out/'Validacao_luz.json').write_text(json.dumps(validate_radiosity(),indent=2)+'\n',encoding='utf-8')
    materials={}
    for p in engines['abertas'].patches:
        key=(p['label'],tuple(p['rho']));materials[key]=materials.get(key,0)+p['area']
    write_csv(out/'Superficies_luz.csv',(dict(superficie=k[0],area_m2=round(a,6),rho_baixo=k[1][0],rho_central=k[1][1],rho_alto=k[1][2],fonte='H2/H13; R54; Decisao_acabamentos_R13; data.js') for k,a in materials.items()))
    write_csv(out/'Resumo_lux.csv',rows)
    grade=[]
    for ident,(grid,values) in grids.items():
        if next(r for r in rows if r['caso']==ident)['veredito'].startswith('não avaliável'):continue
        # Grade resumida a cada quatro células; malha completa só externa se pedida.
        for i,(c,value) in enumerate(zip(grid,values)):
            if i%4==0:grade.append(dict(caso=ident,x_m=round(c['point'][0],4),y_m=round(c['point'][1],4),z_m=round(c['point'][2],4),area_celula_m2=round(c['area'],5),lux_direto=round(value,2),lux_total_central=round(reflected[ident][1][i],2),fonte='R54/P4; H3–H9; central'))
    write_csv(out/'Grades_lux.csv',grade);write_maps(out,reflected,g)
    shifts=sensitivity(g,ies);write_csv(out/'Sensibilidade_luz.csv',shifts)
    report=premises().replace('Resultados espaciais, cenas/consumo e alternativas serão gerados nas próximas etapas deste mesmo arquivo.',result_text(g,rows,grids))
    report=report.replace('## Fontes','## Sensibilidade e reprodução\n\nDeslocamentos±0,25 m dos plafons, um eixo por vez, em [Sensibilidade_luz.csv](Sensibilidade_luz.csv); mantidos fluxos/curvas/obstáculos. Não são incertezas estatísticas nem uma otimização da posição. Células de0,25 m em geral e0,10 m nas tarefas, divididas nas bordas; média ponderada pela área. Mínimo amostrado pode cair numa malha mais fina.\n\nSHA R54: `'+g['sha']+'`. IES original: `'+ies['sha256']+'`. Regeneração não requer FreeCAD; lê a exportação com SHA e a curva numérica pequena. Dependência dos mapas: Pillow.\n\n## Fontes')
    report=report.replace('## Fontes',final_text(out,g,ies,rows)+'## Fontes')
    options=comparable_options(g,ies,out)
    first=report.index('## Ajustes mínimos condicionais e opções')
    last=report.index('## Riscos e lacunas',first)
    report=report[:first]+options_text(options)+task_layers(g,ies,out)+glare_and_screens(g,ies,out)+report[last:]
    first=report.index('## Perguntas objetivas')
    last=report.index('## Fontes',first)
    report=report[:first]+decision_summary(out)+'\n'+report[last:]
    inputs=['03_Ambientes/Iluminacao/Fotometria_fontes.json','03_Ambientes/Iluminacao/Lista_curta_luminarias_e_madeira.md',
            '07_Imovel/Medidas_e_impactos.csv','06_Entregas/Caderno_pranchas/Geometria.json','06_Entregas/Planta_cotada/Cotas.json',
            'ferramentas/estudos/estudo_fotometrico.py','09_Referencias/Moodboard.json',
            'ferramentas/site/src/data.js','ferramentas/site/fabrication/Decisao_acabamentos_R13.md',
            'ferramentas/pranchas/gerar.py','ferramentas/pranchas/medidas.py','ferramentas/site/current_release.json',
            '03_Ambientes/Iluminacao/Fechamento_custo_beneficio/Revisao_quarto_CB02.md','09_Referencias/README.md']
    trace=dict(data=DATE,cad_sha256=g['sha'],ies_sha256=ies['sha256'],fontes_sha256_texto_LF={p:hashlib.sha256((ROOT/p).read_bytes().replace(b'\r\n',b'\n')).hexdigest() for p in inputs})
    (out/'Rastreio_fotometrico.json').write_text(json.dumps(trace,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    report=report.replace('## Fontes','[Rastreio das entradas por SHA](Rastreio_fotometrico.json): inclui curva, código, lista comercial, geometria, coordenadas e manifesto das imagens; textos normalizados paraLF, CAD/IES originais por bytes.\n\n## Fontes')
    reading_plane_comparison(out,rows)
    report=report.replace('## Método','## Diagnósticos de malha e comparação histórica\n\nE5% ponderado por área e U0 de células ≥0,02 m² são diagnósticos separados no Resumo_lux.csv; não substituem Emin/Emed integral nem os vereditos. Filtro vazio tem campos em branco, não zero. A comparação0,45/0,85 m está em [Comparacao_planos_leitura.csv](Comparacao_planos_leitura.csv): o primeiro é resultado histórico do commit66083a0, abaixo da cama atual, não recalculado como plano físico válido. Tanque com roupa é caso-limite de envelope opaco, sem veredito para uso real.\n\n## Método')
    report=externalize_report_tables(report,out)
    (out/'Estudo_fotometrico.md').write_text(report,encoding='utf-8')
    update_summary(out,rows)
    if (out/'README.md').exists():
        with (out/'README.md').open('a',encoding='utf-8') as f:f.write('\n'+decision_summary(out))
    if (out/'README.md').exists():
        with (out/'README.md').open('a',encoding='utf-8') as f:
            f.write('\nComparação H14/H15: [lúmens necessários](Fluxo_necessario_luz.csv) e [camadas local/geral/espelho](Camadas_tarefa_luz.csv). Sala e escritório têm metas300/500 lx em paralelo. Opções usam preços existentes, só materiais parciais; nenhuma compra inferida. Verticais e horizontais do espelho preservam1,10 m; segundo plafon é apenas opção.\n')
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
    lines += ['', 'H3: fatores de manutenção0,70/0,80/0,90 (baixo/central/alto); N1§4.8 exige justificar manutenção real, não usar estes fatores como garantia. H4 substituída por radiosidade H13; não se usa FU assumido nem se multiplica a direta por um fator de utilização.', '',
        'H5: transmissão Jurerê0,50/0,65/0,85; âmbar0,40/0,55/0,75; perfil/difusor0,60/0,75/0,90. Faixas de ensaio escolhidas pelo estudo, não limites garantidos do produto. H6: distribuidores analíticos sem IES usam cosⁿ; n=1 como difuso e n=ln(0,5)/ln(cos(facho/2)) quando há facho. Um ângulo publicado não determina toda a curva; a aproximação precisa ser substituída pela fotometria do conjunto.', '',
        '## Produtos e rastreabilidade', '',
        '| Grupo | Fluxo nu lm | Potência W | Cor K | IRC | Fonte / limite |', '|---|---:|---:|---|---|---|']
    for code,p in PRODUCTS.items():
        lines.append(f"| {code} | {p['lm']:g} | {p['w']:g} | {p['cct']} | {p['cri']} | {p['source']}; {p['mode']} |")
    lines += ['', 'Fluxos de fitas resultam de comprimento nominal×lm/m. C2/S3/Q06 mantêm os comprimentos já usados em P6; não são comprimentos de compra. B09=2×0,55 m e B10≤2 m em P5; E05=kit2 m. Não há dado de fluxo por branco/RGB ou intensidade regulada; os cálculos funcionais consideram branco a100%. Faltam transmissão/curva dos conjuntos; IRC das EVY e do Elgin não está comprovado nas fontes usadas. Não confundir lista comercial e SKU conciliado.', '',
        'IES EVO obtido diretamente do anexo oficial S1 em29/10: teste31/08/2021,2329 lm/35,65 W; catálogo2300 lm/30 W. A curva original é cenário histórico, não fotometria certificada do lote30 W. UGR H16 usa a curva original; lux H13 usa comparação normalizada2300/2329; normalizar fluxo não resolve diferença construtiva. Curva numérica pequena preservada em `Fotometria_fontes.json`, com SHA do IES original.', '',
        '## Geometria e evidências do vídeo', '',
        'Planta oficial P3 conferida com a skill PDF; projeções PR-FLOORS e PR-PONTO de P4 fixam o sistema global da prancha em mm. Exportação R54 e modelo são vinculados por SHA. O FreeCAD não é aberto. Os `bounds` do site incluem margens de câmera e não são áreas dos cômodos. Usar união dos retângulos PR-FLOORS sem duplicar sobreposições; excluir footprints de caixas que atravessam o plano apenas na malha útil, mantendo a área bruta separada.', '',
        'Elias,29/10/2026, nesta conversa: “tem imagens de um video de um apartamento semelhante ao meu (só q espelhado)”. V1–V5 foram conferidos: quatro saídas no conjunto social/cozinha/serviço; duas teclas junto ao interfone; três junto à circulação; tomada+interruptor junto ao lavatório. A→Dormitório02/escritório e B→Dormitório01/quarto é a correspondência provável corrigida pela R02. Orientação transferida pelas paredes e vãos da planta, não por inverter coordenadas de pixels. O vídeo sustenta quantidade e região, não centímetros, retorno, neutro ou circuito.', '',
        'Para o cálculo: centros nominais dos pontos existentes; altura do teto2,60 m (banho2,50) menos corpo/hipótese do emissor. Não deduzir novamente forro de uma altura já acabada. Jurerê10 cm de corpo; EVO3,8 cm; Elgin/Firefly5 cm como hipótese, sem dimensão exata comprovada. Rebaixos/vigas sem cotas ficam como perguntas, sem inventar seção. Deslocamento de±25 cm é ensaio de sensibilidade, não precisão atribuída ao vídeo.', '',
        'Planos pedidos0,75/0,85/0,45 m são comparadores; bancadas atuais chegam a0,92 m na cozinha e0,765 no banho; cama atual tem0,64 m. Registrar as duas referências, sem alterar móveis. Plano vertical do rosto separado da horizontal. Portas/varal e armários são envelopes de oclusão, não simulação contínua de interferências.', '',
        '## Método', '',
        'Interreflexão calculada por radiosidade H13 abaixo. Direta: E=ΣI(θ,φ)×cos(incidência)/r²×FM, com visibilidade por segmento×caixa; todas as coordenadas convertidas para metros. Não multiplicar a direta por FU novamente. Emed ponderada pela área das células; Emin por amostra e U0=Emin/Emed. Refinar malha só para testar erro numérico, sem redimensionar instalação condicionada.', '',
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
