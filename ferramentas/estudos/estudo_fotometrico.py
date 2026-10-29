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
        for i,p in enumerate(self.patches):
            origins=np.tile(p['point']+p['normal']*1e-6,(self.rays,1))
            origins[:,p['axes'][0]]+=(rng.random(self.rays)-.5)*p['du']
            origins[:,p['axes'][1]]+=(rng.random(self.rays)-.5)*p['dv']
            hits=self.trace(origins,hemisphere(rng,self.rays,p['normal']))
            counts=np.bincount(hits[hits>=0],minlength=len(self.patches));indices=np.flatnonzero(counts)
            src.extend([i]*len(indices));dst.extend(indices);weights.extend(counts[indices]/self.rays)
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
            for c in grid:
                pos=np.array(c['point'])+np.array(c['normal'])*1e-5
                hits.append(self.trace(pos,hemisphere(rng,rays,c['normal'])))
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
    return dict(analitico_lx=expected,calculado_lx=sampled,erro_relativo=abs(sampled-expected)/expected,**balance)


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


def alternatives(g,ies,rows):
    lights=emitters(g);s=SCENARIOS['central'];cases={c['id']:c for c in calculation_cases(g)};result=[]
    chosen=('sala_mesa','escritorio_mesa','cozinha_preparo_tampo92','cozinha_pia_tampo92','lavanderia_tanque_tampo92','quarto_geral','circulacao_geral')
    for ident in chosen:
        row=next(r for r in rows if r['caso']==ident)
        if row['veredito']=='atende no cenário':continue
        add=uniform_addition(row['media_central'],row['minimo_central'],row['meta_lx'],row['u0_meta'])
        result.append(dict(caso=ident,opcao='acréscimo espacialmente homogêneo mínimo, ideal matemático',
                           media_antes=row['media_central'],u0_antes=row['uniformidade'],media_depois=round(row['media_central']+add,2),
                           u0_depois=round((row['minimo_central']+add)/(row['media_central']+add),3),delta_lux=round(add,2),
                           delta_material_RS='sem produto cotado que comprove esta distribuição',instalacao='não é especificação; obter fotometria/posição para materializar',fonte='H12:solução algébrica; meta e malha central'))
    tests=[('sala_mesa','um Jurerê+2WiZ adicional, posição nominal de comparação',258.59),
           ('cozinha_preparo_tampo92','recuar eixo do perfil para centro transversal da bancada',None),
           ('lavanderia_tanque_tampo92','deslocar plafon35 cm rumo ao tanque e20 cm longitudinalmente',None)]
    for ident,label,cost in tests:
        case=cases[ident];ls=copy.deepcopy(case_lights(case,lights));before=next(r for r in rows if r['caso']==ident)
        if ident=='sala_mesa':
            e=next(e for e in ls if e['code']=='S03');e=copy.deepcopy(e);e['position']=(6.17,4.75,2.50);ls.append(e)
        elif ident.startswith('cozinha'):
            for e in ls:
                if e['code']=='C14':e['position']=(e['position'][0],6.685,e['position'][2])
        else:
            for e in ls:
                if e['code']=='L11':e['position']=(2.85,6.15,e['position'][2])
        st=statistics(case['grid'],[direct(c,ls,s,ies,obstacles_for(g,case)) for c in case['grid']])
        result.append(dict(caso=ident,opcao=label,media_antes=before['media_central'],u0_antes=before['uniformidade'],media_depois=round(st['mean'],2),u0_depois=round(st['u0'],3),
                           delta_lux=round(st['mean']-before['media_central'],2),delta_material_RS=cost if cost else 'sem novo produto; remanejamento sem cotação',
                           instalacao='opção, não adotada; conferir portas/canopla/varal/forro e infraestrutura; mão de obra desconhecida',fonte='P1:60,65+2×98,97=258,59 quando aplicável;H12; malha central'))
    return result


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
 ('R02','alta','UGR leitura/TV/escritório','UGR real indeterminado: luminância direcional/área aparente/Lb/índiceGuth ausentes; EVOUGR<19 de catálogo não é cálculo da sala','obter IES/LDT e tabelaUGR do conjunto; simular observadores e medir instalação; não inventar índice'),
 ('R03','alta','compatibilidade elétrica','Opus36 W/3 A e Shelly4 A/canal não validam PWM/regulação/térmica nem contatoTramontina; G9/D1 ainda sem ensaio do trio10,5 W','respostasIL04–IL07/IL09;12VCC no controlador, nunca127V em I1; ensaio do trio antes de compra'),
 ('R04','alta','fitas/dissipação','C14/S05/Q06 nominais13,2/12/24 W, mais<1,2 W/controlador;5m de fita=60 W excedem fonte36 W; perfilMOV4329 com fita12 W/m sem capacidade térmica confirmada','manter grupos e confirmar dissipação, área útil, terminais, proteção e temperatura; não alojar fonte no fluxo do depurador/micro'),
 ('R05','alta','banheiro/IP','IP44 do plafon não valida todas as posições; IP65 da fita/IP67 da fonte não protegem cortes/emendas','N3§9.1:volumes pelo RT;IPX7/0,IPX4/1,IPX3/2,IPX1/3 na edição consultada;DR≤30mA§5.1.3.2.2; equipotencialização e classes; confirmar revisão aplicável'),
 ('R06','média','sombra e giro','caixas de aéreos e roupa produzem sombras; cozinha EVO41cm em teto260cm ainda cruza altura do giro nominal; folga histórica13cm não é conferência executiva','preservar abertura integral e acesso; posições/fontes só após coordenação, sem limitar porta/varal para caber luz'),
 ('R07','alta','luz no rosto','300 lx verticais é meta residencial, faixa255–493 lx do cenário; barras inferior/superior e torneira exigem acesso, sem refletância especular modelada','confirmar geometriaB09, IRC do lote, conforto e incidência no rosto; não tomar render com barras verticais como detalhe executivo'),
 ('R08','média','reflexos em telas','difusor/âmbar/linhaLED podem aparecer diretamente ou no reflexo; posição/tilt das telas/olhos e luminância ausentes; janela atrás dos monitores cria contraste','manter luz fora da reflexão especular para observadores; cortina/blackout; teste com tela apagada e acesa; não prometer ausência de reflexo'),
 ('R09','alta','circuitos e consumo','símbolo de iluminação visível no quadro da outra unidade; amperagem/curva/condutor/retornos e correspondência à unidade sem comprovação','RT identifica circuito real e FP/inrush; correnteP/127 é equivalente ativa, não correnteRMS de LED'),
 ('R10','média','fonte documental','EVO2329lm35,65W em2021 versus2300lm30W atual; WiZ800lm127V versus oferta806lmbivolt; Brilia cabeçalho12V versus tabela314450127V','pedir ficha/etiqueta do lote, fotometria e transmissão do conjunto; não transferir dados entre variantes'),
]


def final_text(out,g,ies,rows):
    scenes,energy=scene_energy();cr=circuits();alts=alternatives(g,ies,rows)
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
    lines+=['', 'UGR em leitura/TV/escritório fica **indeterminado**, com campos necessários listados em R02; um número assumindo área/índice de posição/fundo seria precisão fabricada. Reflexos especulares e contraste de telas são riscos separados de UGR. Não foi feito ensaio de segurança elétrica, dissipação, dimerização ou desempenho no imóvel.', '',
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
    scenes,energy=scene_energy()
    low=sum(r['kWh_mes_baixo'] for r in energy);high=sum(r['kWh_mes_alto'] for r in energy)
    text+='\n[Cenas e horas](Cenas_luz.csv), [consumo por grupo](Consumo_luz.csv), [correntes](Correntes_luz.csv), [opções numéricas](Alternativas_luz.csv) e [coerência dia/noite](Coerencia_imagens_luz.csv). Subtotal modelado no perfil de uso: **'+f'{low:.2f}–{high:.2f} kWh/mês'+'**, incluindo provisão Shelly24h, sem standby desconhecido das demais fontes/smart. Não é previsão de fatura; grupos não identificam circuitos. UGR e reflexos reais permanecem indeterminados por falta de luminância/curva/observadores.\n\n**Perguntas para Elias:** manter500 lx de leitura/jogos na mesa aberta ou comparar300 lx? Se o déficit persistir, aceita comparar reforço de tarefa? No espelho, prefere avaliar barras horizontais técnicas ou verticais do render? Nenhuma nova seleção inferida. Fabricantes: IES/LDT/SKU, transmissão e IL pendentes. RT/instalador: circuito/quadro real, retorno/neutro, posições/rebaixos e volumes; não pedir agora medidas inexistentes ao morador.\n'
    path.write_text(text,encoding='utf-8')
    with path.open('a',encoding='utf-8') as f:
        f.write('\nMotor de radiosidade por patches implementado e validado em caixa vazia (<3% frente à solução analítica) e balanço de energia com abertura. Integração aos cômodos em andamento; tabela acima ainda direta. Dependências: NumPy e Pillow nas ferramentas locais.\n')


def generate_results(out,detail=None):
    if not (out/'Fotometria_fontes.json').exists():
        (out/'Fotometria_fontes.json').write_bytes((OUT/'Fotometria_fontes.json').read_bytes())
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
    report=report.replace('## Fontes',final_text(out,g,ies,rows)+'## Fontes')
    inputs=['03_Ambientes/Iluminacao/Fotometria_fontes.json','03_Ambientes/Iluminacao/Lista_curta_luminarias_e_madeira.md',
            '07_Imovel/Medidas_e_impactos.csv','06_Entregas/Caderno_pranchas/Geometria.json','06_Entregas/Planta_cotada/Cotas.json',
            'ferramentas/estudos/estudo_fotometrico.py','09_Referencias/Moodboard.json']
    trace=dict(data=DATE,cad_sha256=g['sha'],ies_sha256=ies['sha256'],fontes_sha256_texto_LF={p:hashlib.sha256((ROOT/p).read_bytes().replace(b'\r\n',b'\n')).hexdigest() for p in inputs})
    (out/'Rastreio_fotometrico.json').write_text(json.dumps(trace,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    report=report.replace('## Fontes','[Rastreio das entradas por SHA](Rastreio_fotometrico.json): inclui curva, código, lista comercial, geometria, coordenadas e manifesto das imagens; textos normalizados paraLF, CAD/IES originais por bytes.\n\n## Fontes')
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
