"""Monte Carlo fictício reproduzível; respostas obtidas do motor vigente.

Caixas fixas produzem a mesma chave de painéis: furação/corte são memoizados,
não reexecutados 5.000 vezes nem confundidos com ausência de pendências.
"""
import argparse
import copy
import csv
import hashlib
import json
import math
from pathlib import Path
import random
import tempfile
import time
import contextlib
import io
from collections import defaultdict
from orquestrar import (ROOT,HERE,AUX,ROOMS,document,evaluate,gap_map,dimensional,
                        furacao,outside,json_out,run)


def set_value(rows,code,value):
    parent,_,component=code.partition('/')
    if component:
        vals=[dimensional.resolver(rows,parent+'/'+str(i)).mm for i in range(1 if parent in ['DIM-03','DIM-04'] else 2)]
        vals[int(component)]=value
        rows[parent]['valor_medido']=' x '.join(f'{v:.9f}' for v in vals)+' mm'
    else:rows[parent]['valor_medido']=f'{value:.9f} mm'


def variable_specs(doc,rows):
    used=sorted({c for r in doc['regras'] for c in r['medidas']})
    # Also sample wall coordinates explicitly; unsupported walls stay flagged.
    extra=[c for c in rows if c.startswith('PR-WALLS-') and c not in used]
    for parent in [f'DIM-{i:02}' for i in range(1,9)]:
        extra += [parent+'/'+str(i) for i in range(1 if parent in ['DIM-03','DIM-04'] else 2) if parent+'/'+str(i) not in used]
    extra += [c for c in rows if c.startswith('PD-') and c not in used]
    specs={}
    for code in used+extra:
        value=dimensional.resolver(rows,code).mm
        if value is None:continue
        if code.startswith('PD-'):low,high=(2480,2520) if code=='PD-BAN' else (2580,2620)
        else:low,high=value-20,value+20
        specs[code]=dict(nominal=value,low=low,high=high,unit='mm',used=code in used,kind='prumo' if code=='DEP-COZ-PRUMO' else 'linear')
    for code,v in AUX.items():specs[code]=dict(nominal=0,low=0,high=1 if v['kind']=='ESQUADRO' else 10,unit='grau' if v['kind']=='ESQUADRO' else 'mm',used=True,kind='angle' if v['kind']=='ESQUADRO' else 'linear')
    return specs


def transformed(value,spec):
    if spec['kind']=='angle':return math.tan(math.radians(value))
    if spec['kind']=='prumo':return max(0,value)
    return value-spec['nominal']


def actual(values,rows,doc):
    changed=copy.deepcopy(rows);aux={}
    for code,value in values.items():
        if code in AUX:aux[code]=value
        else:set_value(changed,code,value)
    return evaluate(changed,doc,aux)


def response_model(rows,doc,specs):
    """Finite-difference response table; independent full-engine validation below.

    Current formulas accept only +/- and constants. Nonlinear inputs are
    converted with max(prumo,0) and tan(angle), exactly as declared by the chain.
    Any future non-additive rule must fail validation instead of silently using
    this acceleration.
    """
    baseline=gap_map(evaluate(rows,doc));coeff={}
    for code,s in specs.items():
        if not s['used']:coeff[code]={};continue
        trial=1 if code in AUX else s['nominal']+1
        result=gap_map(actual({code:trial},rows,doc));den=transformed(trial,s)
        coeff[code]={k:(v-baseline[k])/den for k,v in result.items() if abs(v-baseline[k])>1e-9}
    return baseline,coeff


def predict(values,baseline,coeff,specs):
    result=baseline.copy()
    for code,value in values.items():
        delta=transformed(value,specs[code])
        for key,slope in coeff[code].items():result[key]+=slope*delta
    return result


def tolerance(spec,slopes,base):
    candidates=[]
    for key,slope in slopes.items():
        if abs(slope)<1e-12:continue
        if base[key]<-1e-6:continue # existing failure, not a new threshold
        adverse=-1 if slope>0 else 1
        if spec['kind'] in ['angle','prumo'] and adverse<0:continue
        distance=max(0,base[key])/abs(slope)
        distance=math.degrees(math.atan(distance)) if spec['kind']=='angle' else distance
        candidates.append((distance,adverse,key))
    if not candidates:return None,'',''
    distance,sign,key=min(candidates)
    return round(distance,6),('aumentar' if sign>0 else 'reduzir'),key


def perform(output,n=5000,seed=28102026):
    if n<5000:raise ValueError('Monte Carlo exige pelo menos 5000 cenários')
    output=outside(output);output.mkdir(parents=True,exist_ok=True)
    if any(output.iterdir()):raise ValueError('Escolha pasta de saída vazia')
    start=time.perf_counter();doc=document();rows=dimensional.entradas(nominal=True);specs=variable_specs(doc,rows)
    if any(r.get('eixo') is not None and r['modo']!='fixa_com_folga_variavel' for r in doc['regras']):
        raise ValueError('Envelope móvel exige invalidar cache de peças e rever modelo de sensibilidade')
    baseline,coeff=response_model(rows,doc,specs);rng=random.Random(seed)
    max_error=0
    for _ in range(32):
        values={c:rng.uniform(s['low'],s['high']) for c,s in specs.items()}
        expected=gap_map(actual(values,rows,doc));predicted=predict(values,baseline,coeff,specs)
        max_error=max(max_error,max(abs(expected[k]-v) for k,v in predicted.items()))
    if max_error>1e-5:raise ValueError('Resposta deixou de ser aditiva; erro máximo '+str(max_error))
    # One real end-to-end run proves the memoized quantities/holes/cut baseline.
    fixture=output/'Nominal.csv';fixture.write_text('codigo_medida,valor_medido\n',encoding='utf-8')
    with contextlib.redirect_stdout(io.StringIO()):chain,_=run(fixture,output/'Cadeia_nominal')
    totals=defaultdict(int);independent=defaultdict(int);positive_new=0;max_new=0;sum_new=0
    scenario_file=output/'Cenarios.csv'
    with scenario_file.open('w',encoding='utf-8',newline='') as f:
        writer=csv.writer(f);writer.writerow(['cenario',*specs,'folgas_negativas_novas','pecas_CxL_alteradas','conflitos_furacao_novos','chapas_extras'])
        for i in range(n):
            values={c:rng.uniform(s['low'],s['high']) for c,s in specs.items()}
            result=predict(values,baseline,coeff,specs)
            newly={k for k,v in result.items() if v < -1e-6 and baseline[k]>=-1e-6}
            if newly:positive_new+=1
            max_new=max(max_new,len(newly));sum_new+=len(newly)
            for code,s in specs.items():
                delta=transformed(values[code],s)
                # Paired counterfactual: remove only this measurement's adverse
                # contribution from the joint scenario, not merely correlation.
                attributed=[k for k in newly if result[k]-coeff[code].get(k,0)*delta>=-1e-6]
                totals[code]+=len(attributed)
                independent[code]+=sum(baseline[k]+slope*delta < -1e-6 and baseline[k]>=-1e-6 for k,slope in coeff[code].items())
            writer.writerow([i+1,*[round(v,6) for v in values.values()],len(newly),0,0,0])
    panels=furacao.panels(ROOT/'06_Entregas/Fichas_fabricacao');ids_by_mod=defaultdict(set)
    for p in panels.values():ids_by_mod[p['mod']].add(p['id'])
    aggregates=defaultdict(list)
    for code,s in specs.items():aggregates[code.partition('/')[0]].append(code)
    ranked=[]
    for parent in [*rows,*AUX]:
        components=aggregates.get(parent,[]);related=[r for r in doc['regras'] if any(c in r['medidas'] for c in components)]
        targets={r['movel'] for r in related}
        for c in components:
            targets.update(k.split('/')[0] for k in coeff[c])
        affected=set().union(*(ids_by_mod[t] for t in targets)) if targets else set()
        t_candidates=[(tolerance(specs[c],coeff[c],baseline),c) for c in components if coeff[c]]
        t_candidates=[(t,c) for t,c in t_candidates if t[0] is not None]
        threshold,component=min(t_candidates,key=lambda v:v[0][0]) if t_candidates else ((None,'',''),'')
        impact=sum(totals[c] for c in components);single=sum(independent[c] for c in components)
        existing=sum(v< -1e-6 and any(k in coeff[c] for c in components) for k,v in baseline.items())
        status='medida sem regra quantitativa' if not related and not any(coeff[c] for c in components) else 'alta' if threshold[0] is not None and threshold[0]<=1e-6 else 'atenção nominal existente' if existing else 'média' if impact else 'revisão de referência' if affected else 'sem efeito computável'
        description=rows[parent]['medida_ou_verificacao'] if parent in rows else 'Desvio absoluto do esquadro' if AUX[parent]['kind']=='ESQUADRO' else 'Elevação do piso desde a referência baixa'
        ranked.append(dict(codigo_medida=parent,medida=description,criticidade=status,pecas_afetadas_revisao=len(affected),pecas_CxL_alteradas=0,conflitos_furacao_novos=0,folgas_negativas_atribuidas=impact,folgas_negativas_isoladas=single,chapas_extras=0,limiar_novo_conflito=threshold[0],unidade=specs[component]['unit'] if component else '',sentido=threshold[1],componente=component,folga_limitante=threshold[2],folgas_negativas_ja_nominais=existing,componentes_simulados=' | '.join(components),alvos=' | '.join(sorted(targets)),cobertura='caixas fixas; revisão não é redimensionamento' if components else 'qualitativa/sem equação: tolerância RT/oficina pendente'))
    ranked.sort(key=lambda r:(-r['folgas_negativas_atribuidas'],-r['folgas_negativas_isoladas'],-r['pecas_afetadas_revisao'],r['codigo_medida']))
    furacao.write_csv(output/'Todas_medidas.csv',ranked)
    top=[r for r in ranked if r['componentes_simulados']][:15]
    furacao.write_csv(output/'Ranking_15.csv',top)
    summary=dict(cenarios=n,seed=seed,distribuicao='uniforme independente; paredes/origens/dimensões±20mm; PD2580–2620/BAN2480–2520; esquadro0–1°; piso0–10mm',variaveis_simuladas=len(specs),medidas_total=len(ranked),com_novas_folgas_negativas=positive_new,media_folgas_negativas_novas=round(sum_new/n,4),max_folgas_negativas_novas=max_new,pecas_CxL_alteradas=0,conflitos_furacao_novos=0,chapas_extras=0,validacao_motor_completo_cenarios=32,erro_maximo_resposta_mm=max_error,cache_derivados='mesma chave C×L/t/topologia de249 IDs; cadeia nominal executada, demais reutilizam resultado idêntico; referências/fechamentos sem ID ficam fora da compra',tempo_cadeia_s=chain['tempos']['total_s'],tempo_s=time.perf_counter()-start,sha256_cenarios=hashlib.sha256(scenario_file.read_bytes()).hexdigest(),sha256_todas_medidas=hashlib.sha256((output/'Todas_medidas.csv').read_bytes()).hexdigest(),top15=top,limites='Limiar geométrico nominal, não tolerância de obra. Contagem de peças é revisão pelos vínculos; nenhuma caixa foi esticada. Zero novos furos/chapas vale só para os IDs fixos cobertos, não para fechamentos sem ID,104 peças sem centros,2130 posições incompletas ou preços ausentes. PR-WALLS sem equação permanece cobertura pendente. Frequências fictícias não são probabilidades da obra.')
    summary['sha256_regras']=hashlib.sha256((HERE/'regras.json').read_bytes()).hexdigest()
    summary['sha256_nominais']=hashlib.sha256(json.dumps({c:s['nominal'] for c,s in specs.items()},sort_keys=True).encode()).hexdigest()
    summary['sha256_motor']=hashlib.sha256(Path(dimensional.__file__).read_bytes()).hexdigest()
    summary['sha256_sensibilidade']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    json_out(output/'Sensibilidade.json',summary)
    lines=['# Sensibilidade nominal — Monte Carlo fictício','',f'{n} cenários; seed{seed}; {positive_new} com folga nova negativa. Máximo{max_new}; média{sum_new/n:.3f}.','',summary['limites'],'','| Medida | Peças a revisar | Folgas atribuídas | Limiar nominal |','|---|---:|---:|---|']
    for r in top:lines.append(f'| {r["codigo_medida"]} | {r["pecas_afetadas_revisao"]} | {r["folgas_negativas_atribuidas"]} | {r["limiar_novo_conflito"]} {r["unidade"]}; {r["sentido"]} |')
    lines+=['','Furos, chapas e dimensões alteradas: zero nos IDs fixos, por cache verificado da cadeia. Arquivo Todas_medidas.csv cobre cada código do roteiro/índice, inclusive os qualitativos sem equação. Limiar0 significa qualquer variação adversa além da margem numérica, não precisão de medição zero.','', 'Modelo de resposta obtido por perturbação unitária do motor existente; validado contra32 cenários completos. Esquadro usa tan(ângulo), prumo usa parte positiva. Para cada cenário, a atribuição retira uma variável por vez: uma falha com múltiplas causas suficientes pode não ser atribuída a nenhuma isoladamente; soma das atribuições não é total de defeitos únicos.','', 'As 5.000 linhas brutas ficam fora do projeto; resumo e ranking pequeno podem ser versionados. Reproduzir com mesma seed; tempos e caminho não participam do hash dos cenários.']
    (output/'Sensibilidade.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    return summary


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--saida',type=Path);ap.add_argument('--cenarios',type=int,default=5000);ap.add_argument('--seed',type=int,default=28102026);args=ap.parse_args()
    out=args.saida or Path(tempfile.mkdtemp(prefix='guedala-sensibilidade-'))
    result=perform(out,args.cenarios,args.seed);print(json.dumps({k:v for k,v in result.items() if k not in ['top15','limites']},ensure_ascii=False));print(out)
