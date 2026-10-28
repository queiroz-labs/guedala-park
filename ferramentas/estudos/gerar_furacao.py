"""Furação nominal relativa às peças; não abre CAD. Somente biblioteca padrão.

python -B ferramentas/estudos/gerar_furacao.py [--pecas DIR] [--saida DIR]
Os CSVs de entrada definem dimensões; Geometria.json só fornece topologia nominal.
Mudança de dimensão sem nova topologia bloqueia a junta em vez de esticar posições.
"""
import argparse
import csv
import hashlib
import io
import itertools
import json
import math
from collections import defaultdict
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / '04_Moveis/Furacao'
TECH = 'ferramentas/site/fabrication/technical-r14.json'
GEO = '06_Entregas/Caderno_pranchas/Geometria.json'
HINGES = 'ferramentas/site/fabrication/r14/hinge-drilling-maps.json'
MINIFIX = 'https://files.hafele.co.uk/catalogfiles/www/14CFC294.pdf p.294; Minifix_C.md FF2.10/14/17'
BLUM = 'https://publications.blum.com/2024/catalogue/en/'
FIELDS = ['movel','peca','furo','face','x','y','diametro','profundidade','tipo','situacao','parametros','origem','fonte','par','papel','gx','gy','gz','nx','ny','nz','curso_material','grupo','expressao']


def load(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8-sig'))


def write_csv(path, rows, fields=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields or list(rows[0]), delimiter=';', extrasaction='ignore')
        w.writeheader()
        w.writerows(rows)


def count(length):
    return 2 if length <= 400 else 3 if length <= 700 else math.ceil(length / 350) + 1


def panels(folder):
    objects = {o['id']: o for o in load(GEO)['objects']}
    result = {}
    for path in sorted(folder.glob('P??-pecas.csv')):
        for row in csv.DictReader(io.StringIO(path.read_text(encoding='utf-8-sig')), delimiter=';'):
            ids = [s.strip() for s in row['IDs CAD'].split('|')]
            names = row['Peça'].split(' / ')
            for i, pid in enumerate(ids):
                c,l,t = [float(row[k]) for k in ['C nominal mm','L nominal mm','Esp. envelope mm']]
                p = dict(id=pid, mod=path.stem[:3], name=names[min(i,len(names)-1)], c=c,l=l,t=t,
                         finish=row['Especificação documental'], contour=row['Contorno'], border=row['Bordas/veios/usinagem'])
                if pid in objects:
                    box = objects[pid]['box']
                    dims = [box[a+3]-box[a] for a in range(3)]
                    # Deterministic bijection to CSV C,L,t, including square pieces.
                    axes = min(itertools.permutations(range(3)), key=lambda ax: sum(abs(dims[a]-v) for a,v in zip(ax,[c,l,t])))
                    if all(abs(dims[a]-v)<.1 for a,v in zip(axes,[c,l,t])):
                        p.update(box=box, axes=axes)
                result[pid] = p
    return result


def origin(p,face):
    if 'box' not in p:
        return 'canto inferior junto a dobradica; x largura, y altura; face interna A'
    a,b,n = p['axes']
    return f'canto minimo C/L; C=+{"XYZ"[a]}, L=+{"XYZ"[b]}; A={"XYZ"[n]}min, B={"XYZ"[n]}max; topo-C/L0=min,1=max; topo x=eixo restante, y=espessura desde A; sem espelhar B'


def local(p,point,normal):
    a,b,n = p['axes']; box=p['box']; axis=max(range(3),key=lambda i:abs(normal[i]))
    if axis==n:
        return ('A' if normal[n]>0 else 'B'), point[a]-box[a], point[b]-box[b], p['c'], p['l']
    other = b if axis==a else a
    return f'topo-{"C" if axis==a else "L"}{0 if normal[axis]>0 else 1}', point[other]-box[other], point[n]-box[n], p['l'] if axis==a else p['c'], p['t']


def generate(folder, dest):
    ps=panels(folder); tech=load(TECH)['modules']; holes=[]; pending=[]; joints=[]
    def pend(p,topic,reason):
        pending.append(dict(movel=p['mod'],peca=p['id'],tema=topic,situacao='parâmetro a confirmar',detalhe=reason))
    def hole(p,typ,point=None,normal=None,diam=None,depth=None,source='',pair='',role='',group='',xy=None,expr='',params=''):
        h=dict.fromkeys(FIELDS,''); h.update(movel=p['mod'],peca=p['id'],furo=f"F{len(holes)+1:05}",tipo=typ,diametro=diam,profundidade=depth,fonte=source,par=pair,papel=role,grupo=group,expressao=expr,parametros=params)
        if point is not None:
            face,x,y,_,_=local(p,point,normal); h.update(face=face,x=round(x,3),y=round(y,3))
            h.update(zip(['gx','gy','gz'],[round(v,3) for v in point]));h.update(zip(['nx','ny','nz'],normal))
            axis=max(range(3),key=lambda i:abs(normal[i]));h['curso_material']=round(p['box'][axis+3]-p['box'][axis],3)
        else:
            h.update(face='A',x=round(xy[0],3),y=round(xy[1],3),curso_material=p['t'])
        h['origem']=origin(p,h['face']); h['situacao']='parâmetro a confirmar' if params or depth is None or diam is None else 'nominal/proposta'
        holes.append(h);return h
    for p in ps.values():
        pend(p,'bordas/fita','Indicar C0,C1,L0,L1 visiveis, cor e espessura da fita; envelope nao desconta fita.')
        if 'box' not in p: pend(p,'topologia','Sem correspondencia ortogonal entre CSV atual e Geometria.json; junta nao inferida.')
    # Enumerate contacts only between current rectangular stationary panels.
    for mod in tech:
        eligible=[p for p in ps.values() if p['mod']==mod and 'box' in p and p['contour']=='Retangular' and not any(s in p['id'] for s in ['Frente','Gaveta','Painel1','Painel2'])]
        for a,b in itertools.combinations(eligible,2):
            aa,bb=a['box'],b['box']
            for axis in range(3):
                sign=1 if abs(aa[axis+3]-bb[axis])<.01 else -1 if abs(bb[axis+3]-aa[axis])<.01 else 0
                if not sign: continue
                other=[i for i in range(3) if i!=axis]
                lo={i:max(aa[i],bb[i]) for i in other};hi={i:min(aa[i+3],bb[i+3]) for i in other}
                if any(hi[i]-lo[i]<=.01 for i in other):continue
                lengths=[hi[i]-lo[i] for i in other];length=max(lengths)
                jid=f'{mod}-J{sum(j["movel"]==mod for j in joints)+1:03}'
                faceface=axis==a['axes'][2] and axis==b['axes'][2]
                edgeedge=axis!=a['axes'][2] and axis!=b['axes'][2]
                kind='Parafuso face a face' if faceface else 'Confirmat 7x50' if 'fundo' in (a['name']+b['name']).lower() else 'Minifix 15'
                n=4 if faceface else count(length)
                j=dict(movel=mod,junta=jid,a=a['id'],b=b['id'],eixo='XYZ'[axis],contato_mm=round(length,3),conector=kind,quantidade=n,cavilhas=0 if faceface else n,situacao='nominal/proposta')
                joints.append(j)
                if faceface or edgeedge or min(a['t'],b['t'])!=18 or length<152:
                    j['situacao']='parâmetro a confirmar';pend(a,jid,'Tipo/espessura/comprimento de contato exige detalhe especifico; sem centros inventados.');continue
                board,side=(a,b) if a['axes'][2]!=axis else (b,a)
                plane=aa[axis+3] if sign>0 else aa[axis]
                inward=1 if abs(board['box'][axis]-plane)<.01 else -1
                line=next(i for i in other if i!=board['axes'][2]);th=board['axes'][2]
                # A 32 mm phase change on the opposite side of a divider applies to both mating members.
                phase=32 if abs(side['box'][axis]-plane)<.01 else 0
                positions=[lo[line]+60+phase+k*(length-152)/(n-1) for k in range(n)]
                for k,s in enumerate(positions):
                    pair=f'{jid}-{k+1}'
                    pt=[0.,0.,0.];pt[axis]=plane;pt[line]=s;pt[th]=(board['box'][th]+board['box'][th+3])/2
                    sn=[0,0,0];sn[axis]=-inward
                    en=[0,0,0];en[axis]=inward
                    if kind=='Minifix 15':
                        # Access from the thickness face facing the nominal module centre.
                        center=(load_module_boxes[mod][th]+load_module_boxes[mod][th+3])/2
                        access=0 if abs(board['box'][th]-center)<abs(board['box'][th+3]-center) else 3
                        cp=pt.copy();cp[axis]+=inward*34;cp[th]=board['box'][th+access]
                        cn=[0,0,0];cn[th]=1 if access==0 else -1
                        hole(board,'Minifix Ø15 corpo',cp,cn,15,13.5,MINIFIX,group=pair,expr='B34; recuo60; fase32; passo=(contato-152)/(n-1)',params='SKU novo e acesso de ferramenta a confirmar')
                        hole(board,'Minifix Ø8 topo',pt,en,8,None,MINIFIX,pair,'topo',pair,params='S100 vigente usa Ø7; Ø8 exige selecionar pino e profundidade compativeis')
                        hole(side,'Minifix piloto pino',pt,sn,5,8.5,MINIFIX,pair,'face',pair,params='SKU proposto 262.28.920; conferir compatibilidade com passagem Ø8')
                    else:
                        hole(board,'Confirmat piloto topo',pt,en,None,None,'Familia 7x50; ficha '+mod,pair,'topo',pair,params='catalogo do SKU: Ø/profundidade/escalonamento')
                        hole(side,'Confirmat passagem face',pt,sn,None,None,'Familia 7x50; ficha '+mod,pair,'face',pair,params='catalogo do SKU: Ø/profundidade/escareado')
                    dp=pt.copy();dp[line]+=32
                    hole(board,'cavilha Ø8 topo',dp,en,8,None,'Ø8x30: ficha '+mod,pair+'D','topo',pair+'D',params='partilha de embutimento, cola e folga de fundo')
                    hole(side,'cavilha Ø8 face',dp,sn,8,None,'Ø8x30: ficha '+mod,pair+'D','face',pair+'D',params='partilha de embutimento, cola e folga de fundo')
    # Caneco coordinates retain bottom and top margins under C/L changes.
    for d in load(HINGES):
        p=ps.get(d['partId'])
        if not p:continue
        width,height=(p['c'],p['l']) if abs(p['c']-d['width'])<abs(p['l']-d['width']) else (p['l'],p['c'])
        for k,h in enumerate(d['holes']):
            x=h['x'] if h['x']<d['width']/2 else width-(d['width']-h['x'])
            y=d['holes'][0]['y'] if k==0 else height-(d['height']-h['y']) if k==len(d['holes'])-1 else d['holes'][0]['y']+(height-(d['height']-d['holes'][-1]['y'])-d['holes'][0]['y'])*k/(len(d['holes'])-1)
            # Hinge map axes differ from sorted C/L; explicitly preserve hinge datum.
            if 'box' in p:
                del_box=p.pop('box'); del_axes=p.pop('axes')
                hole(p,'caneco Ø35',diam=35,depth=h['depth'],source=BLUM+'77/ p.77; mapa nominal R45',xy=(x,y),expr='margens inferior/superior preservadas; intermediarios equidistantes')
                p['box']=del_box;p['axes']=del_axes
            else:hole(p,'caneco Ø35',diam=35,depth=h['depth'],source=BLUM+'77/ p.77',xy=(x,y))
            holes[-1]['origem']=f'canto inferior de menor u do mapa R45; x=largura {width}, y=altura {height}; A interna; verificar mao'
            # Pattern screw-on CLIP top: 45 mm pitch, pilot line 9.5 toward hinge edge from cup centre.
            for dy in [-22.5,22.5]:
                px=x+(-9.5 if x<width/2 else 9.5)
                hh=hole(p,'piloto flange Blum',diam=2.7,depth=8,source=BLUM+'77/ p.77; '+BLUM+'160/ p.160',xy=(px,y+dy),expr='caneco x +/-9.5; y +/-22.5')
                hh['origem']=holes[-3]['origem'] if dy>0 else holes[-2]['origem']
        pend(p,'base dobradica 37/32','ID/face do apoio e transformacao da folha para apoio pendentes; x=37 desde frente do apoio; y=centro montado +/-16; Ø2.7x8, Blum p.152/160.')
    # Retain every descriptive operation not completely converted as a traceable pending item.
    for mod,m in tech.items():
        for d in m['drilling']:
            if 'nominalCenters' in d or 'Pilotos de fixação dos canecos'==d['item']:continue
            for pid in d.get('partIds',[]) or ['SEM_ID']:
                p=ps.get(pid,dict(mod=mod,id=pid))
                pend(p,d['id']+' '+d['item'],d.get('pattern','')+' | fonte: '+json.dumps(d.get('sources',[]),ensure_ascii=False))
    for pid in ['Peca400','Peca401']:
        p=ps[pid];a,b,n=p['axes']
        for depth in [20,86]:
            for height in [244,488]:
                pt=p['box'][:3].copy();pt[a]+=height;pt[b]+=depth
                center=(load_module_boxes['P19'][n]+load_module_boxes['P19'][n+3])/2
                end=0 if abs(p['box'][n]-center)<abs(p['box'][n+3]-center) else 3
                pt[n]=p['box'][n+end];normal=[0,0,0];normal[n]=1 if end==0 else -1
                hole(p,'apoio prateleira Ø5',pt,normal,5,8.5,'Ficha P19-F05/F06; Hafele 282.04.711; profundidade proposta',params='Profundidade proposta; nao e linha System32 (244/488 nao passo32)')
        pend(p,'linha System32','Passo 32 mm; definir inicio/fim e recuos. Nao transformar prateleiras fixas em removiveis; oito apoios vigentes mantidos separadamente.')
    for mod in tech:
        write_csv(dest/f'{mod}-coordenadas.csv',[h for h in holes if h['movel']==mod],FIELDS)
    write_csv(dest/'Mapa_conectores.csv',joints)
    write_csv(dest/'Pendencias.csv',pending)
    write_csv(dest/'Paineis.csv',[{k:p.get(k,'') for k in ['mod','id','name','c','l','t','finish','contour']} for p in ps.values()])
    # Each SVG has one face, circles labelled by stable hole ID and dimensions in mm.
    drawings=[]
    for (pid,face),hs in itertools.groupby(sorted(holes,key=lambda h:(h['peca'],h['face'])),key=lambda h:(h['peca'],h['face'])):
        hs=list(hs);p=ps[pid]
        if hs[0]['tipo'] in ['caneco Ø35','piloto flange Blum'] or hs[0]['origem'].startswith('canto inferior de menor u'):
            d=next(d for d in load(HINGES) if d['partId']==pid);w,h=d['width'],d['height']
        elif face in ['A','B']:w,h=p['c'],p['l']
        else:w,h=(p['l'] if face.startswith('topo-C') else p['c']),p['t']
        title=f'{p["mod"]} {pid} {face} — nominal/proposta'
        scale=min(900/w,500/h);height_page=680+len(hs)*15
        svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 {height_page}"><title>{escape(title)}</title><rect width="1000" height="{height_page}" fill="white"/><text x="35" y="30" font-size="18">{escape(title)}</text><text x="35" y="55" font-size="12">Origem (0,0) canto inferior; +x direita; +y acima; mm; tracejado=Ø pendente</text><g transform="translate(50,{85+h*scale}) scale({scale},-{scale})"><rect width="{w}" height="{h}" fill="white" stroke="black" stroke-width="{1/scale}"/>'
        for hh in hs:
            radius=float(hh['diametro'] or 4)/2
            svg+=f'<circle cx="{hh["x"]}" cy="{hh["y"]}" r="{radius}" fill="none" stroke="#a33" stroke-width="{1/scale}"'+(' stroke-dasharray="2 2"' if not hh['diametro'] else '')+'/>'
        svg+='</g><text x="35" y="615" font-size="13">'+escape(f'{w} × {h}; face B sem espelhamento; Ø e profundidade em mm')+'</text>'
        for i,hh in enumerate(hs):
            label=f'{hh["furo"]}  ({hh["x"]}; {hh["y"]})  {hh["tipo"]}  Ø{hh["diametro"] or "?"}  prof.{hh["profundidade"] or "?"}'
            svg+=f'<text x="35" y="{645+i*15}" font-size="11">{escape(label)}</text>'
        svg+='</svg>'
        name=f'Desenhos/{p["mod"]}-{pid}-{face}.svg';(dest/name).parent.mkdir(parents=True,exist_ok=True);(dest/name).write_text(svg,encoding='utf-8');drawings.append(name)
    summary=dict(paineis=len(ps),furos=len(holes),juntas=len(joints),pendencias=len(pending),faces=len(drawings),furos_com_parametros=sum(h['situacao']=='parâmetro a confirmar' for h in holes),fontes={s:hashlib.sha256((ROOT/s).read_bytes()).hexdigest() for s in [TECH,GEO,HINGES]},files=[f'P{i:02}-coordenadas.csv' for i in range(1,21)]+['Mapa_conectores.csv','Pendencias.csv','Paineis.csv','Resumo.json']+drawings)
    summary['paineis_com_centros']=len({h['peca'] for h in holes})
    summary['paineis_sem_centros']=len(ps)-summary['paineis_com_centros']
    summary['csvs_pecas_sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(folder.glob('P??-pecas.csv'))}
    index='<html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Furação nominal por peça</title><main><h1>Furação nominal por peça</h1><p>Propostas relativas às bordas. Valores vazios são parâmetros a confirmar. Os círculos com Ø pendente são apenas símbolos. Fontes, origem e condições no CSV. Não usar como arquivo de máquina.</p><p>249 IDs incluem peças especiais, gavetas e tampas sem mapa completo; ausência de furos não significa ausência de ligação.</p><p><a href="Pendencias.csv">Parâmetros a confirmar</a> · <a href="Mapa_conectores.csv">Conectores por encontro</a></p>'
    for mod in tech:
        index+=f'<h2>{mod}</h2><p><a href="{mod}-coordenadas.csv">Coordenadas CSV</a></p><ul>'
        for p in ps.values():
            if p['mod']!=mod:continue
            links=[f'<a href="{escape(name)}">{escape(name.rsplit("-",1)[-1][:-4])}</a>' for name in drawings if name.startswith(f'Desenhos/{mod}-{p["id"]}-')]
            index+=f'<li>{escape(p["id"])} — {escape(p["name"])}: '+(' · '.join(links) or 'parâmetro a confirmar; sem centros emitidos')+'</li>'
        index+='</ul>'
    index+='</main></html>'; (dest/'index.html').write_text(index,encoding='utf-8');summary['files'].append('index.html')
    (dest/'Resumo.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return summary


load_module_boxes={m['id']:m['box'] for m in load(GEO)['modules']} if isinstance(load(GEO)['modules'],list) else {k:v['box'] for k,v in load(GEO)['modules'].items()}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--pecas',type=Path,default=ROOT/'06_Entregas/Fichas_fabricacao');ap.add_argument('--saida',type=Path,default=OUT);args=ap.parse_args();args.saida.mkdir(parents=True,exist_ok=True)
    r=generate(args.pecas,args.saida);print(json.dumps({k:v for k,v in r.items() if k not in ['files','fontes','csvs_pecas_sha256']},ensure_ascii=False))
