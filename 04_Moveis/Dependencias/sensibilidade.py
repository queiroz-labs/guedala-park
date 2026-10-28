"""Paredes como retas compartilhadas em datum R54; caixas/folgas nominais intactas."""
import argparse,csv,hashlib,json,math,random,tempfile,time
from pathlib import Path
from collections import defaultdict
from orquestrar import ROOT,HERE,document,dimensional,evaluate,gap_map,furacao,outside,json_out


def model(doc=None):
    doc=doc or document();rows=dimensional.entradas(nominal=True);bounds={}
    for r in doc['regras']:
        if r.get('eixo') not in [0,1]:continue
        room=doc['alvos'][r['movel']]['room'];axis=r['eixo']
        origin=dimensional.resolver(rows,r['origem']).mm;span=dimensional.resolver(rows,r['dimensao']).mm
        pair=(origin,origin+span)
        if axis in bounds.setdefault(room,{}) and bounds[room][axis]!=pair:raise ValueError('Limites incompatíveis no mesmo ambiente')
        bounds[room][axis]=pair
    walls={}
    source={}
    for code,r in rows.items():
        if code.startswith('PR-WALLS-'):
            _,_,ident,axis=code.split('-');source.setdefault(ident,{})[axis]=dimensional.resolver(rows,code).mm
            source[ident]['room']=r['ambiente']
    for ident,v in sorted(source.items()):
        room=v['room'];bb=bounds[room];axis=0 if v['W']<=v['D'] else 1
        start=v['X'] if axis==0 else v['Y'];thick=v['W'] if axis==0 else v['D']
        side=0 if sum(bb[axis])/2>start+thick/2 else 1
        position=start+thick if side==0 else start
        lo=v['Y'] if axis==0 else v['X'];hi=lo+(v['D'] if axis==0 else v['W'])
        wid='PAREDE-'+ident
        pivot=[position,(lo+hi)/2] if axis==0 else [(lo+hi)/2,position]
        desc='Descrição pendente: identificar os dois extremos do pano acabado e datum M0 no croqui.'
        if ident=='15':desc='Face acabada da parede atrás da bancada da cozinha e do tanque; marcar extremos do pano junto à cozinha e lavanderia.'
        if ident=='02':desc='Face acabada da parede da cabeceira e aéreo P04 no quarto; marcar os dois extremos do pano no croqui.'
        walls[wid]=dict(id=wid,axis=axis,position=position,side=side,segment=[lo,hi],pivot=pivot,physical=desc,rooms=[room],source='PR-WALLS-'+ident)
    targets={};nominal=evaluate(rows,doc);gaps=gap_map(nominal)
    for name,t in doc['alvos'].items():
        bb=t['box_planta'];selected=[]
        for wid,w in walls.items():
            other=1-w['axis'];overlap=min(bb[other+3],w['segment'][1])-max(bb[other],w['segment'][0])
            if overlap<=0:continue
            near=abs((bb[w['axis']] if w['side']==0 else bb[w['axis']+3])-w['position'])<=30
            if t['room'] in w['rooms'] or near:selected.append(wid)
        targets[name]=dict(room=t['room'],box=bb,walls=selected,ceiling=gaps[f'{name}/Z/topo'])
    return dict(doc=doc,walls=walls,targets=targets,gaps=gaps)


def wall_gap(w,box,displacement=0,angle=0):
    sign=1 if w['side']==0 else -1
    theta=math.radians(angle);normal=[0.,0.];normal[w['axis']]=sign*math.cos(theta);normal[1-w['axis']]=sign*math.sin(theta)
    d=sum(normal[i]*w['pivot'][i] for i in [0,1])+displacement
    box=list(box);other=1-w['axis'];box[other]=max(box[other],w['segment'][0]);box[other+3]=min(box[other+3],w['segment'][1])
    if box[other]>=box[other+3]:return float('inf')
    return min(normal[0]*x+normal[1]*y-d for x in [box[0],box[3]] for y in [box[1],box[4]])


def minimum(m,values=None):
    values=values or {};result={}
    for name,t in m['targets'].items():
        g=[wall_gap(m['walls'][w],t['box'],values.get(w+'-DESLOCAMENTO',0),values.get(w+'-ANGULO',0)) for w in t['walls']]
        g.append(t['ceiling']+values.get('TETO-'+t['room'],0)-values.get('PISO-'+t['room'],0))
        result[name]=min(g)
    return result


def nominal_tables(m,dest,N=10):
    records=[];questions=[];frames=furacao.load('ferramentas/site/fabrication/module-frames.json')['frames']
    for name,t in m['targets'].items():
        zero=[]
        for key,g in m['gaps'].items():
            target,axis,side=key.split('/')
            if target!=name or g>15:continue
            matches=[wid for wid in t['walls'] if m['walls'][wid]['axis']==('XY'.index(axis) if axis in 'XY' else -1) and m['walls'][wid]['side']==(0 if side=='inicio' else 1) and abs(wall_gap(m['walls'][wid],t['box'])-g)<1e-5]
            text=' | '.join(m['walls'][w]['physical'] for w in matches) or 'Limite do retângulo de referência; parede física não identificada (não comprova contato).'
            records.append(dict(modulo=name,lado=axis+'/'+side,folga_mm=g,encosta_em=text,parede=' | '.join(matches),situacao='conflito nominal existente' if g<0 else 'contato nominal' if abs(g)<1e-6 else 'folga curta'))
            if abs(g)<1e-6 and axis in 'XY':zero.append((axis,side,matches))
        if zero:
            width_axis=max(range(2),key=lambda a:abs(frames[name][0][a])) if name in frames else 0
            loss_width=sum(axis=='XY'[width_axis] for axis,_,_ in zero)*N
            loss_depth=sum(axis!='XY'[width_axis] for axis,_,_ in zero)*N
            questions.append(dict(modulo=name,lados_hoje_zero=' | '.join(axis+'/'+side for axis,side,_ in zero),folga_proposta_por_lado_mm=N,perda_largura_util_mm=loss_width,perda_profundidade_mm=loss_depth,lados_sem_parede_identificada=sum(not matches for _,_,matches in zero),condicao='Pergunta; confirmar panos abertos/parede antes de arremate. Não muda caixa; conflitos nominais negativos continuam.'))
    furacao.write_csv(dest/'Folgas_ate_15.csv',records);furacao.write_csv(dest/'Pergunta_folga_zero.csv',questions)
    return records,questions


def perform(output,n=5000,seed=28102026):
    if n<5000:raise ValueError('Mínimo5000 cenários')
    output=outside(output);output.mkdir(parents=True,exist_ok=True)
    if any(output.iterdir()):raise ValueError('Saída deve estar vazia')
    start=time.perf_counter();m=model();rng=random.Random(seed);variables={}
    for w in m['walls']:
        variables[w+'-DESLOCAMENTO']=(-20,20,'mm');variables[w+'-ANGULO']=(-1,1,'grau')
    for room in sorted({t['room'] for t in m['targets'].values()}):
        variables['TETO-'+room]=(-20,20,'mm');variables['PISO-'+room]=(0,10,'mm')
    # A and B are independent samples. Hybrid A_Bi replaces one physical wall
    # parameter; coordinates of all modules remain in the same global datum.
    A=[{c:rng.uniform(lo,hi) for c,(lo,hi,_) in variables.items()} for _ in range(n)]
    B=[{c:rng.uniform(lo,hi) for c,(lo,hi,_) in variables.items()} for _ in range(n)]
    YA=[minimum(m,v) for v in A];YB=[minimum(m,v) for v in B];variance={}
    for target in m['targets']:
        vv=[v[target] for v in YA+YB];avg=sum(vv)/len(vv);variance[target]=sum((v-avg)**2 for v in vv)/len(vv)
    ranks=[];detail=[]
    for code,(lo,hi,unit) in variables.items():
        # Cache unchanged wall contributions by updating only affected targets.
        wall=code.rsplit('-',1)[0] if code.startswith('PAREDE-') else None
        affected=[t for t,v in m['targets'].items() if wall in v['walls']] if wall else [t for t,v in m['targets'].items() if v['room']==code.split('-',1)[1]]
        explained=[]
        for t in affected:
            vt=m['targets'][t];responses=[]
            for i in range(n):
                value=A[i].copy();value[code]=B[i][code]
                gg=[wall_gap(m['walls'][w],vt['box'],value.get(w+'-DESLOCAMENTO',0),value.get(w+'-ANGULO',0)) for w in vt['walls']]
                yy=min(*gg,vt['ceiling']+value.get('TETO-'+vt['room'],0)-value.get('PISO-'+vt['room'],0));responses.append(yy)
            var=variance[t]
            raw=sum(YB[i][t]*(responses[i]-YA[i][t]) for i in range(n))/n/var if var>1e-12 else 0
            index=max(0,min(1,raw));value=index*var;explained.append(value)
            detail.append(dict(medida=code,modulo=t,variancia_folga_minima_mm2=round(var,5),indice_primeira_ordem=round(index,5),estimador_bruto=round(raw,5),variancia_explicada_mm2=round(value,5)))
        w=m['walls'].get(wall,{})
        description=w.get('physical','Altura livre sobre os móveis do ambiente' if code.startswith('TETO') else 'Desnível do piso acabado na área de apoio')
        ranks.append(dict(codigo_medida=code,descricao_fisica=description,instrumento='laser de distâncias + nível/laser angular; a1m do piso; datum M0 comum' if wall else 'laser de distâncias vertical / nível laser + régua',unidade=unit,modulos=' | '.join(affected),variancia_explicada_mm2=round(sum(explained),5),metodo='Sobol primeira ordem, pick-freeze; soma ponderada pela variância por módulo'))
    ranks.sort(key=lambda x:(-x['variancia_explicada_mm2'],x['codigo_medida']))
    furacao.write_csv(output/'Ranking_15.csv',ranks[:15]);furacao.write_csv(output/'Variancia_por_modulo.csv',detail)
    furacao.write_csv(output/'Paredes.csv',[dict(id=k,ambientes=' | '.join(v['rooms']),eixo=v['axis'],posicao_nominal_mm=v['position'],lado=v['side'],pivot_x=v['pivot'][0],pivot_y=v['pivot'][1],descricao=v['physical']) for k,v in m['walls'].items()])
    folgas,questions=nominal_tables(m,output)
    with (output/'Cenarios.csv').open('w',encoding='utf-8',newline='') as f:
        ww=csv.writer(f);ww.writerow(['amostra','conjunto',*variables,*m['targets']])
        for label,xx,yy in [('A',A,YA),('B',B,YB)]:
            for i,(x,y) in enumerate(zip(xx,yy)):ww.writerow([i,label,*x.values(),*y.values()])
    summary=dict(cenarios_base=n,avaliacoes_independentes=2*n,seed=seed,paredes=len(m['walls']),variaveis=len(variables),modelo='Retas compartilhadas, deslocamento normal±20mm, rotação±1° no mesmo datum; teto±20mm (BAN base2500, demais2600), piso0–10mm.',top15=ranks[:15],folgas_ate_15=len(folgas),modulos_com_zero=len(questions),folga_montagem_pergunta_mm=10,caixas_alteradas=0,folgas_base_alteradas=0,tempo_s=round(time.perf_counter()-start,3),sha256_cenarios=hashlib.sha256((output/'Cenarios.csv').read_bytes()).hexdigest(),limites='Panos reais vêm dos26 retângulos PR-WALLS, não dos limites abertos dos pisos. Faces internas orientadas pelo ambiente; panos compartilhados usam a mesma reta. Identificação física e datum M0 ainda pendentes onde indicado. Não há origens independentes. Relações físicas entre panos devem ser confirmadas no croqui. Índice de primeira ordem não inclui toda interação; erro amostral pode produzir estimador negativo, preservado na tabela detalhada; índices exibidos truncados0–1. Menor folga é nominal, não tolerância de obra. Nenhuma caixa ou folga original foi modificada.')
    json_out(output/'Sensibilidade.json',summary)
    return summary


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--saida',type=Path);ap.add_argument('--cenarios',type=int,default=5000);ap.add_argument('--seed',type=int,default=28102026);a=ap.parse_args();out=a.saida or Path(tempfile.mkdtemp(prefix='gp-paredes-'));r=perform(out,a.cenarios,a.seed);print(json.dumps({k:v for k,v in r.items() if k not in ['top15','limites']},ensure_ascii=False));print(out)
