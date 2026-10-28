"""Audita dados de furação. Código 1: conflito ou informação insuficiente.

Saída completa em CSV; não confundir ausência de interferência detectada com
completude. Critérios de oficina (margens/ferramenta) são hipóteses configuráveis.
"""
import argparse
import csv
import itertools
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from gerar_furacao import ROOT, OUT, GEO, HINGES, load, panels, write_csv

DENSITY_SOURCE='https://www.sonaearauco.com/media/vt5gihec/tds0356sair01_mdf-standard-carb2_epa_en.pdf p.1 (>12-19mm:700kg/m3)'
HINGE_SOURCE='https://publications.blum.com/2024/catalogue/en/718/ p.718; manual local Blum_110_planejamento.pdf p.2'


def read(path):
    return list(csv.DictReader(path.open(encoding='utf-8-sig'),delimiter=';'))


def number(value):
    return None if value in ['',None] else float(value)


def point(h):
    return [number(h[k]) for k in ['gx','gy','gz']]


def normal(h):
    return [number(h[k]) for k in ['nx','ny','nz']]


def segment_distance(a,b,c,d):
    """Exact minimum for axis-aligned segments, including degenerate points."""
    def dist_to_seg(p,u,v):
        dv=[v[i]-u[i] for i in range(3)];den=sum(x*x for x in dv)
        t=max(0,min(1,sum((p[i]-u[i])*dv[i] for i in range(3))/den)) if den else 0
        return math.dist(p,[u[i]+t*dv[i] for i in range(3)])
    ax=next((i for i in range(3) if abs(b[i]-a[i])>1e-9),None)
    bx=next((i for i in range(3) if abs(d[i]-c[i])>1e-9),None)
    candidates=[dist_to_seg(p,u,v) for p,u,v in [(a,c,d),(b,c,d),(c,a,b),(d,a,b)]]
    if ax is not None and bx is not None and ax!=bx:
        pa=a.copy();pc=c.copy();pa[ax]=max(min(c[ax],max(a[ax],b[ax])),min(a[ax],b[ax]));pc[bx]=max(min(a[bx],max(c[bx],d[bx])),min(c[bx],d[bx]));candidates.append(math.dist(pa,pc))
    return min(candidates)


def end(h):
    p=point(h);n=normal(h);return [p[i]+n[i]*float(h['profundidade']) for i in range(3)]


def ray_box(p,n,box,length,radius):
    """Conservative swept screwdriver cylinder vs expanded orthogonal box."""
    axis=max(range(3),key=lambda i:abs(n[i]))
    if any(p[i]+radius<=box[i]+.01 or p[i]-radius>=box[i+3]-.01 for i in range(3) if i!=axis):return False
    q=p[axis]-n[axis]*length
    return min(p[axis],q)<box[axis+3]-.01 and max(p[axis],q)>box[axis]+.01


def required_hinges(width,height,mass):
    # Upper envelopes read from Blum's chart; lower mass is not a rejection.
    if width>650 or height>2500 or mass>22:return None
    n=next((n for n,h,m in [(2,750,6),(3,1500,12),(4,2100,17),(5,2500,22)] if height<=h and mass<=m),None)
    return n+(1 if width>600 else 0) if n else None


def audit(holes,ps,gap=3,tool_length=100,tool_radius=10):
    issues=[];distances=[];access=[]
    def issue(h,code,detail,other='',metric=None,severity=2):
        issues.append(dict(prioridade=severity,movel=h['movel'],peca=h['peca'],face=h['face'],x=h['x'],y=h['y'],furo=h['furo'],outro=other,tipo=code,medida_mm='' if metric is None else round(metric,3),detalhe=detail))
    bypart=defaultdict(list);pairs=defaultdict(list)
    hinge_dims={d['partId']:(d['width'],d['height']) for d in load(HINGES)}
    for h in holes:
        p=ps[h['peca']];bypart[h['peca']].append(h)
        if h['par']:pairs[h['par']].append(h)
        diam,depth=number(h['diametro']),number(h['profundidade'])
        if diam is None or depth is None or h['situacao']=='parâmetro a confirmar':
            issue(h,'PARAMETRO','Ø/profundidade/SKU/acesso incompleto: '+h['parametros'],severity=3)
        if depth is not None and depth>=float(h['curso_material'])-3:
            issue(h,'PROFUNDIDADE','Reserva inferior ou igual a 3mm no eixo de perfuracao; topo usa comprimento atravessado, face usa espessura.',metric=float(h['curso_material'])-depth,severity=0)
        if h['face'] in ['A','B']:
            w,he=hinge_dims.get(h['peca'],(p['c'],p['l']))
        else:w,he=(p['l'] if h['face'].startswith('topo-C') else p['c']),p['t']
        x,y=float(h['x']),float(h['y']);edge=min(x,w-x,y,he-y)
        if diam is not None:
            clearance=edge-diam/2
            if clearance<gap-.001:issue(h,'BORDA','Margem de madeira abaixo do criterio proposto; fita/rebaixo ainda nao descontados.',metric=clearance,severity=0 if clearance<0 else 1)
        elif edge<0:issue(h,'CENTRO_FORA','Centro fora do envelope.',metric=edge,severity=0)
    for pid,hs in bypart.items():
        for a,b in itertools.combinations(hs,2):
            if a['grupo'] and a['grupo']==b['grupo']:continue # intended cam-to-bolt intersection
            da,db=number(a['diametro']),number(b['diametro'])
            if da is None or db is None:continue
            if a['face']==b['face']:
                center=math.dist([float(a['x']),float(a['y'])],[float(b['x']),float(b['y'])]);clearance=center-(da+db)/2
                distances.append(dict(peca=pid,a=a['furo'],b=b['furo'],centros_mm=round(center,3),bordas_mm=round(clearance,3)))
                if clearance<gap-.001:issue(a,'SOBREPOSICAO_FACE' if clearance<0 else 'DISTANCIA',f'{a["tipo"]} x {b["tipo"]}; criterio borda-borda {gap}mm (centro >= soma dos raios + margem).',b['furo'],clearance,0 if clearance<0 else 1)
            elif a['gx'] not in ['',None] and b['gx'] not in ['',None] and a['profundidade'] not in ['',None] and b['profundidade'] not in ['',None]:
                clearance=segment_distance(point(a),end(a),point(b),end(b))-(da+db)/2
                if clearance<0:issue(a,'CRUZAMENTO_INTERNO','Cilindros em faces/arestas diferentes cruzam dentro do envelope nominal.',b['furo'],clearance,0)
        for a in hs:
            if a['tipo']!='Minifix Ø15 corpo' or a['gx'] in ['',None]:continue
            for q in ps.values():
                if q['id']==pid or q['mod']!=a['movel'] or 'box' not in q:continue
                if ray_box(point(a),normal(a),q['box'],tool_length,tool_radius):
                    issue(a,'ACESSO','Apertar antes de instalar '+q['id']+'; envelope de ferramenta proposto, sem simulacao de mao/mandril.',q['id'],severity=1)
                    access.append(dict(movel=a['movel'],grupo=a['grupo'],apertar_peca=pid,antes_de_instalar=q['id'],furo=a['furo']))
    for pair,hs in pairs.items():
        a=hs[0]
        if len(hs)!=2 or set(h['papel'] for h in hs)!={'face','topo'}:
            issue(a,'PAR_AUSENTE','Par deve ter exatamente uma entrada de topo e uma de face.',pair,severity=0);continue
        if any(h['gx'] in ['',None] for h in hs):issue(a,'PAR_SEM_REFERENCIAL','Par sem coordenada comum.',pair,severity=2);continue
        delta=math.dist(point(hs[0]),point(hs[1]));n0,n1=normal(hs[0]),normal(hs[1])
        if delta>.5 or any(abs(n0[i]+n1[i])>.001 for i in range(3)):
            issue(a,'PAR_DESALINHADO','Desvio >0,5mm ou normais nao opostas.',hs[1]['furo'],delta,0)
    issues.sort(key=lambda r:(r['prioridade'],r['medida_mm'] if isinstance(r['medida_mm'],(int,float)) else 0,r['peca'],r['furo']))
    return issues,distances,access


def execute(folder,dest,args):
    ps=panels(ROOT/'06_Entregas/Fichas_fabricacao');holes=[h for p in sorted(folder.glob('P??-coordenadas.csv')) for h in read(p)]
    issues,distances,access=audit(holes,ps,args.margem,args.ferramenta_comprimento,args.ferramenta_raio)
    doors=[]
    for d in load(HINGES):
        p=ps[d['partId']];w,h=d['width'],d['height'];mass=w*h*p['t']*700/1e9
        req=required_hinges(w,h,mass);existing=len(d['holes'])
        doors.append(dict(movel=d['module'],peca=d['partId'],largura_mm=w,altura_mm=h,espessura_mm=p['t'],densidade_kg_m3=700,massa_mdf_kg=round(mass,3),dobradicas_atuais=existing,dobradicas_envelope_proposto=req or '',situacao='fora da faixa nominal' if req is None or existing<req or w>=h else 'comparacao nominal; massa acabada a confirmar',observacao='MDF sem puxador/espelho/revestimento; abaixo de4kg: ensaio primeira folha; largura>=altura fora da orientacao Blum.',fonte=HINGE_SOURCE+'; '+DENSITY_SOURCE))
    assembly=[]
    for mod in [f'P{i:02}' for i in range(1,21)]:
        module=[p for p in ps.values() if p['mod']==mod];deps=defaultdict(set)
        for a in access:
            if a['movel']==mod:deps[a['antes_de_instalar']].add(a['apertar_peca'])
        remaining={p['id'] for p in module};ordered=[]
        while remaining:
            ready=sorted(p for p in remaining if not(deps[p]&remaining))
            if not ready:break
            ordered+=ready;remaining-=set(ready)
        assembly.append(dict(movel=mod,etapa=1,acao='Identificar A/B, frente e cantos; usinar e testar ferragens nas pecas soltas; conferir pares.',pecas=' | '.join(p['id'] for p in module),condicao='proposta; parametros pendentes impedem sequencia executiva'))
        assembly.append(dict(movel=mod,etapa=2,acao='Apresentar laterais/base e horizontais; apertar Minifix antes de instalar cada bloqueador listado.',pecas=' | '.join(ordered),condicao='Ordem parcial por acesso nominal; nao representa encaixe/estabilidade de montagem'))
        for a in access:
            if a['movel']==mod:assembly.append(dict(movel=mod,etapa=3,acao=f'Apertar {a["grupo"]} ({a["furo"]}) antes de instalar {a["antes_de_instalar"]}.',pecas=a['apertar_peca'],condicao='Dependencia de ferramenta; se ja fechado, acesso bloqueado'))
        assembly.append(dict(movel=mod,etapa=4,acao='Conferir esquadro, fechar fundo apos ultimos apertos acessiveis; instalar mecanismos e frentes por ultimo.',pecas='',condicao='Ciclo a resolver: '+' | '.join(sorted(remaining)) if remaining else 'Confirmar retirada de ferramenta e montagem em seco; instalacao no imovel fora do escopo'))
    dest.mkdir(parents=True,exist_ok=True)
    write_csv(dest/'Conflitos.csv',issues,['prioridade','movel','peca','face','x','y','furo','outro','tipo','medida_mm','detalhe'])
    write_csv(dest/'Distancias.csv',distances,['peca','a','b','centros_mm','bordas_mm'])
    write_csv(dest/'Portas.csv',doors)
    write_csv(dest/'Montagem.csv',assembly)
    counts=Counter(i['tipo'] for i in issues);geometric=sum(v for k,v in counts.items() if k!='PARAMETRO')
    summary=dict(resultado='REPROVADO' if issues else 'sem conflito detectado; cobertura deve ser conferida',furos=len(holes),conflitos=geometric,parametros=counts['PARAMETRO'],por_tipo=dict(counts),portas_fora_da_faixa=sum(d['situacao']=='fora da faixa nominal' for d in doors),criterios=dict(margem_mm=args.margem,tolerancia_par_mm=.5,ferramenta_comprimento_mm=args.ferramenta_comprimento,ferramenta_raio_mm=args.ferramenta_raio),piores=issues[:10])
    (dest/'Conferencia.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    rows=['# Conferência da furação nominal','',f'**{summary["resultado"]}**: {geometric} ocorrências geométricas/acesso e {counts["PARAMETRO"]} posições incompletas. '+f'{summary["portas_fora_da_faixa"]} portas fora do envelope nominal de quantidade/proporção.','', '## Dez ocorrências de maior prioridade','', '| Peça | Face | x; y mm | Tipo | Outro | Medida mm |','|---|---|---|---|---|---|']
    for i in issues[:10]:rows.append(f'| {i["peca"]} | {i["face"]} | {i["x"]}; {i["y"]} | {i["tipo"]} | {i["outro"]} | {i["medida_mm"]} |')
    rows+=['','Ocorrências são pares/regiões, não peças únicas. Interseção intencional do corpo/pino Minifix no mesmo grupo é excluída. Profundidade desconhecida não passa: fica incompleta. Distâncias entre faces diferentes só são calculadas com diâmetro, profundidade e referência espacial conhecidos. Topos usam o curso da madeira no eixo do furo, não os 18 mm transversais.','', '## Cobertura e limites','', 'Os canecos têm referência 2D histórica de porta; não há transformação suficiente para confrontá-los com peças vizinhas. Bases 37/32, linhas System32 e corrediças não individualizadas continuam sem verificação espacial: pendências de cobertura, não zero conflitos. Também não são simulados recortes, ponta cônica da broca, fita, parafusos já montados, mão ou mandril. AABB é triagem conservadora nos painéis especiais.','', 'Ferramenta: cilindro proposto de raio 10 e curso 100 mm. Acesso bloqueado produz precedência em Montagem.csv; se houver ciclo, sequência executiva fica pendente. O CSV contém proposta para todos os 20 móveis, sem supor montagem/parede estáveis.','', 'Portas.csv: área × espessura × 700 kg/m³, referência Sonae Arauco MDF ST CARB2/EPA >12–19 mm, p.1; não é densidade medida da Greenplac. Tabela Blum p.718/manual local p.2: envelopes 2/750/6, 3/1500/12, 4/2100/17, 5/2500/22 (dobradiças/mm/kg). Largura600–650 acrescenta uma; >650, >2500 ou >22 fica fora. Usar o maior requisito entre altura e peso é triagem conservadora, não interpolação da curva nem conclusão sobre retenção. MDF sem puxador, espelho ou revestimento: massa acabada permanece a confirmar. Portas abaixo de4 kg exigem prova funcional.','', 'Fontes: [Blum planejamento p.718](https://publications.blum.com/2024/catalogue/en/718/), [orientação Blum por largura](https://ea.blum.com/en/number-of-hinges/), [densidade nominal p.1](https://www.sonaearauco.com/media/vt5gihec/tds0356sair01_mdf-standard-carb2_epa_en.pdf).','', 'Reproduzir: `python -B ferramentas/estudos/conferir_furacao.py`. Código1 é esperado enquanto houver conflitos ou parâmetros. Opções `--entrada`, `--saida`, `--margem`, `--ferramenta-comprimento`, `--ferramenta-raio` permitem ensaios externos; valores propostos não são mínimos do fabricante.']
    (dest/'Conferencia.md').write_text('\n'.join(rows)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in summary.items() if k not in ['piores','criterios']},ensure_ascii=False))
    return bool(issues)


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--entrada',type=Path,default=OUT);ap.add_argument('--saida',type=Path,default=OUT);ap.add_argument('--margem',type=float,default=3);ap.add_argument('--ferramenta-comprimento',type=float,default=100);ap.add_argument('--ferramenta-raio',type=float,default=10);a=ap.parse_args();raise SystemExit(execute(a.entrada,a.saida,a))
