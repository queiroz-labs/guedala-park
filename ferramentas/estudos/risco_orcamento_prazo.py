"""Monte Carlo condicional: hipóteses editáveis, sem revisar orçamento/cronograma."""
import argparse
from collections import Counter
import copy
from datetime import date,timedelta
import json
from pathlib import Path
import re
import sys
sys.dont_write_bytecode=True
import numpy as np
import comparador_cotacoes as io
import cronograma_risco as cron

ROOT=io.ROOT
OUT=ROOT.parent/'outputs/Codex_perguntas_e_risco'
AREA=ROOT/'05_Orcamento_e_cronograma/Risco'
MODEL=ROOT/'ferramentas/estudos/modelos/Risco_hipoteses.json'
BUDGET='05_Orcamento_e_cronograma/Orcamento/Orcamento_R43.md'
NOTICE='as faixas refletem as hipóteses de entrada, não a realidade; itens sem base vêm de regra de simulação.'


def budget():
    rows=[];total=None
    for index,line in enumerate((ROOT/BUDGET).read_text(encoding='utf-8').splitlines(),1):
        parts=[p.strip() for p in line.strip('|').split('|')]
        if not line.startswith('|') or len(parts)<5:continue
        if parts[0]=='**Total**':
            total=float(io.number(parts[1].replace('**','')));break
        if re.fullmatch(r'\d[\d.,]*',parts[1]):
            rows.append(dict(id=parts[0],central=float(io.number(parts[1])),fonte=BUDGET+':'+str(index),tipo='provisão' if parts[0] in {'Marcenaria','Obra e pintura','Instalações','Pedras e box','Iluminação','Coordenação e logística'} else 'estimativa'))
    if total is None or abs(sum(r['central'] for r in rows)-total)>.005:
        raise ValueError('Tabela única do orçamento não reconciliada')
    return rows,total


def default_config():
    costs,total=budget()
    split=[]
    for row in costs:
        if row['id']=='Pedras e box':
            for name,val in [('Pedras',5300),('Box',1400)]:
                split.append(dict(row,id=name,central=val,fonte=row['fonte']+'; Limite_e_metas_130mil.json: revisaoPedrasBox, rateio 5300/1400'))
        else:split.append(row)
    rules={'preço confirmado':0,'cotado sem validade':.10,'estimativa':.15,'provisão':.30}
    for row in split:
        row.update(ativo=True,distribuicao='triangular',regra='hipótese de simulação: ±'+str(int(100*rules[row['tipo']]))+'% do central; limites não são cotações')
    split += [dict(id='Climatização adicional',central=None,tipo='estimativa',ativo=False,distribuicao=None,fonte='01_Programa_e_decisoes/Plano_de_reforma_NBR16280.md: fora do escopo; consulta própria',regra='Sem base de custo; cenário com climatização não calculável até informar faixa'),
        dict(id='Reserva',central=10000,tipo='preço confirmado',ativo=False,distribuicao='ponto',fonte='ferramentas/fatos.json; reserva fixa separada, não preço de serviço',regra='Não é gasto; somada somente ao total planejado com reserva')]
    previous=ROOT.parent/'outputs/Cronograma_risco/Cronograma_risco.json'
    if previous.exists():
        old=json.loads(previous.read_text(encoding='utf-8'))
        if old['source_sha256']!=io.sha(cron.SOURCE):raise ValueError('Cronograma externo desatualizado; conferir a fonte antes de simular')
        nodes=copy.deepcopy(old['nodes']);network_source='../outputs/Cronograma_risco/Cronograma_risco.json'
    else:
        nodes,_,_=cron.current_model(cron.SOURCE.read_text(encoding='utf-8'),cron.QUOTE.read_text(encoding='utf-8'),cron.PROGRAM.read_text(encoding='utf-8'))
        network_source='ferramentas/estudos/cronograma_risco.py: current_model (mesmo motor; arquivo externo ausente)'
    ranges={
        'chaves':(0,0,0),'vistoria_medicao':(.1,.25,.5),'executivo':(.5,1,1.5),'fabricacao':(5,5.5,6),
        'inferiores':(.25,.5,1),'gabarito':(.1,.2,.3),'pedras':(1,8.5/7,10/7),'rt':(.5,1,2),
        'protocolo':(.1,.25,.5),'analise_condominio':(.5,1,2),'eletrica_hidraulica':(1,1.5,2),
        'impermeabilizacao_cura':(.5,1,1.5),'revestimentos':(1,1.5,2),'pintura_base':(.5,.75,1),
        'vinilico':(.5,.75,1),'medicao_box':(.1,.2,.3),'fornecimento_box':(1,2,3),
        'instalacoes_box_e21_luz':(.25,.5,1),'retoques_limpeza_testes':(.25,.5,1),'mudanca':(.1,.2,.4),
        'envio_cotacao':(.1,.2,.3),'retornos_cotacao':(.5,1,1.5),'comparacao_propostas':(.1,.25,.5),
        'contratacao_marcenaria':(.1,.25,.5),'definicoes_marcenaria':(.5,1,2),'pedido_ferragens':(.1,.2,.3),
        'abastecimento_ferragens':(1,2,3),'inicio_fabricacao':(0,0,0)}
    nodes=[n for n in nodes if n['id']!='marcenaria_pedras_loucas_metais_eletros']
    for n in nodes:
        name=n['id'];a,m,b=ranges[name]
        n['triangular']=[a,m,b]
        n['origem_semana']=-4 if name in {'rt','envio_cotacao','definicoes_marcenaria'} else None if n['depends'] else 0
        n['origem_natureza']='hipótese: preparativos iniciados quatro semanas antes das chaves' if n['origem_semana'] else 'origem relativa às chaves, não data de calendário'
        if name in {'chaves','inicio_fabricacao'}:nature='marco lógico fixo'
        elif name in {'fabricacao','fornecimento_box','abastecimento_ferragens'}:nature='limites típicos documentados; moda central é hipótese de simulação'
        elif name=='pedras':nature='7–10 dias da seção 1; moda8,5 dias é hipótese; 1–2 semanas como cenário separado'
        else:nature='hipótese de simulação: duração ausente; janelas de calendário não são durações observadas'
        n['natureza']=nature
        n['depends_original']=n['depends'][:]
        n['ligacao_nova']=''
    by_id={n['id']:n for n in nodes}
    changed={'protocolo':['chaves','rt'],'inferiores':['fabricacao','vinilico'],
        'instalacoes_box_e21_luz':['fornecimento_box','eletrica_hidraulica'],
        'retoques_limpeza_testes':['montagem_resto','instalacao_pedras','loucas_metais_eletros','instalacoes_box_e21_luz'],
        'mudanca':['retoques_limpeza_testes']}
    for name,deps in changed.items():
        by_id[name]['depends']=deps;by_id[name]['ligacao_nova']='hipótese explícita para completar rede até ocupação; confirmar com RT/oficina'
    for name,deps,tri in [('montagem_resto',['inferiores'],[.25,.5,1]),('instalacao_pedras',['pedras'],[.1,.25,.5]),('loucas_metais_eletros',['instalacao_pedras','eletrica_hidraulica'],[.25,.5,1])]:
        nodes.append(dict(id=name,depends=deps,triangular=tri,origem_semana=0,depends_original=[],ligacao_nova='hipótese: desagregação do agregado semana 7–8, sem somá-lo novamente',natureza='hipótese de simulação: serviço sem duração documentada',source_section='Cronograma R00 seção1/2'))
    events=[]
    for name,target,p,tri in [('exigencia_condominio','analise_condominio',.20,[.5,1,2]),
        ('medida_divergente','executivo',.25,[.25,.75,1.5]),('falta_material','abastecimento_ferragens',.20,[.5,1,2]),
        ('atraso_marcenaria','fabricacao',.20,[2,3,4]),('atraso_pedra','pedras',.15,[.25,.5,1])]:
        events.append(dict(id=name,atividade=target,probabilidade=p,atraso_semanas=tri,
            natureza='hipótese de simulação; probabilidade não observada; não representa estatística de fornecedor',
            fonte='R00: riscos qualitativos; fila de oficina 2–4 semanas somente como evento, fora dos 5–6 de produção'))
    return dict(schema=1,semente=20261029,iteracoes=20000,data_chaves=None,
        escopo_base='Referência integral R44 histórica; sem climatização adicional e sem novos bens fora da verba',
        orcamento_soma_vigente=total,reserva=10000,regras_amplitude=rules,itens=split,
        rede=nodes,rede_origem=network_source,rede_base_sha256=io.sha(previous) if previous.exists() else None,
        riscos=events,custo_armazenamento_semana=150,
        regra_armazenamento='hipótese de simulação: R$150 por semana além da semana 12; não cotação e não parcela já provada da logística',
        retrabalho_fracao_marcenaria=[.02,.05,.10],regra_retrabalho='hipótese de simulação: custo adicional somente se evento medida_divergente ocorrer',
        independencia='Preços e durações-base independentes. Mesmo evento de retrabalho gera atraso/custo; mudança além de12 gera armazenamento. Sem correlação de mercado presumida.',
        cenarios=[dict(id='Integral_R44'),dict(id='Etapa_D05C_documentada',centrais={'Marcenaria':37000,'Móveis e tecidos':8549,'Iluminação':4534.55},nota='cenário documental 27/10:127101,22, não oferta obtida; nenhum desconto sorteado como fato'),
            dict(id='Somente_se_propostas_ate35mil',marcenaria_fixa=35000,nota='Condição imposta: proposta integral instalada ≤35mil; usa teto de R$ 35 mil, não estima chance de obter proposta nem trunca a distribuição da base'),
            dict(id='Medida_real_diverge',forcar_medida=True,nota='Evento imposto, não previsão de probabilidade das medidas; usa vínculos externos sem transformar contagem em custo'),
            dict(id='Sem_refazer_impermeabilizacao',zerar_atividade='impermeabilizacao_cura',nota='Somente se RT confirmar desnecessidade; provisão de custo não é reduzida sem rateio documentado'),
            dict(id='Pedras_1a2_semanas',pedras_tri=[1,1.5,2],nota='Alternativa documental da seção3; não somar com faixa7–10 dias'),
            dict(id='Com_climatizacao_a_cotar',sem_base=True,nota='Custo/escopo ausentes: informar faixa própria antes de calcular, sem imputar zero')],
        fontes_sha256={BUDGET:io.sha(ROOT/BUDGET),'05_Orcamento_e_cronograma/Cronograma_obra_e_compras.md':io.sha(cron.SOURCE),
            '05_Orcamento_e_cronograma/Orcamento/Limite_e_metas_130mil.json':io.sha(ROOT/'05_Orcamento_e_cronograma/Orcamento/Limite_e_metas_130mil.json')})


def sample(rng,tri,n):
    a,m,b=map(float,tri)
    if not all(np.isfinite([a,m,b])) or not 0<=a<=m<=b:raise ValueError('Triangular inválida')
    return np.full(n,a) if a==b else rng.triangular(a,m,b,n)


def scheduling(nodes,durations):
    ordered=cron.ancestors(nodes,'mudanca')
    n=len(durations[ordered[0]['id']]);starts={};finishes={}
    for node in ordered:
        parents=[finishes[k] for k in node['depends']]
        origin=node.get('origem_semana')
        if origin is not None and not np.isfinite(origin):raise ValueError('Origem temporal não finita')
        start=np.maximum.reduce(parents) if parents else np.full(n,float(origin or 0))
        if parents and origin is not None:start=np.maximum(start,float(origin))
        starts[node['id']]=start;finishes[node['id']]=start+durations[node['id']]
    end=finishes['mudanca'];latest={};critical={}
    successors={node['id']:[] for node in ordered}
    for node in ordered:
        for parent in node['depends']:successors[parent].append(node['id'])
    for node in reversed(ordered):
        name=node['id']
        finish=np.minimum.reduce([latest[k] for k in successors[name]]) if successors[name] else end
        latest[name]=finish-durations[name]
        critical[name]=np.abs(latest[name]-starts[name])<1e-8
    return end,critical,starts,finishes


def simulate(config,scenario,n=None):
    n=n or config['iteracoes'];rng=np.random.default_rng(config['semente'])
    nodes=copy.deepcopy(config['rede']);durations={node['id']:sample(rng,scenario.get('pedras_tri',node['triangular']) if node['id']=='pedras' else node['triangular'],n) for node in nodes}
    # Preserva a ordem dos sorteios em todos os cenários (comparação com números comuns).
    event_data={};inputs={}
    for event in config['riscos']:
        p=float(event['probabilidade'])
        if not 0<=p<=1:raise ValueError('Probabilidade inválida')
        active=rng.random(n)<p
        if scenario.get('forcar_medida') and event['id']=='medida_divergente':active[:]=True
        impact=active*sample(rng,event['atraso_semanas'],n)
        event_data[event['id']]=active
        durations[event['atividade']]+=impact
        inputs['risco:'+event['id']]=impact
    if scenario.get('zerar_atividade'):durations[scenario['zerar_atividade']]=np.zeros(n)
    end,critical,starts,finishes=scheduling(nodes,durations)
    costs={}
    for item in config['itens']:
        if not item['ativo']:continue
        central=scenario.get('centrais',{}).get(item['id'],item['central'])
        if central is None:raise ValueError('Custo ativo sem base: '+item['id'])
        if not np.isfinite(central) or central<0:raise ValueError('Custo central inválido')
        if item.get('triangular'):
            values=sample(rng,item['triangular'],n)
        elif item['distribuicao']=='ponto':values=np.full(n,float(central))
        else:
            width=float(config['regras_amplitude'][item['tipo']]);values=sample(rng,[central*(1-width),central,central*(1+width)],n)
        if item['id']=='Marcenaria' and 'marcenaria_fixa' in scenario:values=np.full(n,float(scenario['marcenaria_fixa']))
        costs[item['id']]=values
    extra_rework=event_data.get('medida_divergente',np.zeros(n))*sample(rng,config['retrabalho_fracao_marcenaria'],n)*costs['Marcenaria']
    if not np.isfinite(config['custo_armazenamento_semana']) or config['custo_armazenamento_semana']<0:raise ValueError('Armazenamento inválido')
    storage=np.maximum(0,end-12)*float(config['custo_armazenamento_semana'])
    costs['Retrabalho hipotético']=extra_rework;costs['Armazenamento hipotético']=storage
    execution=sum(costs.values());joinery=costs['Marcenaria']+extra_rework
    return dict(execucao=execution,total_planejado=execution+config['reserva'],marcenaria=joinery,
        preco_proposta_marcenaria=costs['Marcenaria'],mudanca=end,custos=costs,duracoes=durations,
        riscos=inputs,criticos=critical,inicios=starts,fins=finishes)


def ranks(values):
    _,inverse,counts=np.unique(values,return_inverse=True,return_counts=True)
    middle=np.cumsum(counts)-(counts-1)/2
    return middle[inverse]


def spearman(a,b):
    if np.ptp(a)==0 or np.ptp(b)==0:return 0.0
    return float(np.corrcoef(ranks(a),ranks(b))[0,1])


def percentiles(values):
    return {f'P{q}':round(float(np.percentile(values,q)),4) for q in [10,50,80,90]}


def stats(data):
    result={k:percentiles(data[k]) for k in ['execucao','total_planejado','marcenaria','mudanca']}
    for name,values,limit in [('execucao_ate120',data['execucao'],120000),('execucao_ate130_usa_reserva',data['execucao'],130000),
        ('total_planejado_ate130',data['total_planejado'],130000),('marcenaria_ate35',data['marcenaria'],35000),
        ('proposta_marcenaria_ate35',data['preco_proposta_marcenaria'],35000),('mudanca_ate9',data['mudanca'],9),('mudanca_ate10',data['mudanca'],10),('mudanca_ate12',data['mudanca'],12)]:
        result[name]=float(np.mean(values<=limit))
    return result


def question_ids():
    path=ROOT/'01_Programa_e_decisoes/Perguntas_em_aberto/Perguntas.csv'
    return {r['chave']:r['id'] for r in io.read_csv(path)} if path.exists() else {}


def sensitivity(data):
    questions=question_ids()
    aliases={'Marcenaria':'cotacao','Pedras':'pedras','Box':'box','Obra e pintura':'impermeab','Instalações':'eletrica',
        'Móveis e tecidos':'cotacao','Pisos e revestimentos':'piso','Iluminação':'ilum_produto','Coordenação e logística':'rt_escopo',
        'fabricacao':'executivo','analise_condominio':'protocolo','vistoria_medicao':'medicao','executivo':'executivo',
        'risco:medida_divergente':'medicao','risco:exigencia_condominio':'protocolo','risco:atraso_marcenaria':'executivo',
        'pedras':'pedras','risco:atraso_pedra':'pedras','revestimentos':'impermeab','Armazenamento hipotético':'elevador','Retrabalho hipotético':'medicao'}
    rows=[]
    for target,features in [('custo',data['custos']),('prazo',{**data['duracoes'],**data['riscos']})]:
        output=data['execucao'] if target=='custo' else data['mudanca']
        part=[dict(alvo=target,entrada=k,spearman=spearman(v,output),pergunta=questions.get(aliases.get(k,'executivo' if target=='prazo' else 'cotacao'),'')) for k,v in features.items()]
        rows += sorted(part,key=lambda r:(-abs(r['spearman']),r['entrada']))[:10]
    return rows


def proposal_inputs(path):
    if not path.exists():return [],'Comparação externa ausente; nenhum preço real usado'
    raw=path.read_text(encoding='utf-8')
    data=json.loads(raw)
    if 'fict' in io.key(raw):return [],'Dados fictícios detectados: não usar como proposta real'
    summaries=data.get('resumo',[])
    if not summaries:return [],'Comparação sem propostas normalizadas; nenhum preço real usado'
    accepted=[r for r in summaries if r.get('escopo')=='integral' and r.get('equivalente_min') is not None and r.get('equivalente_max') is not None and not r.get('sem_base')]
    return accepted, f'{len(accepted)} proposta(s) integral(is) completa(s) utilizável(is); {len(summaries)-len(accepted)} incompletas/escopo distinto; sem seleção de fornecedor'


def run(args):
    output=args.saida.resolve()
    if output==ROOT or ROOT in output.parents:raise ValueError('Iterações devem ficar fora do repositório')
    output.mkdir(parents=True,exist_ok=True);AREA.mkdir(parents=True,exist_ok=True)
    if args.gerar_modelo or not args.entrada.exists():
        if args.entrada!=MODEL:raise ValueError('Entrada própria ausente; não gerar sobre caminho arbitrário')
        io.dump(MODEL,default_config())
    config=json.loads(args.entrada.read_text(encoding='utf-8'))
    for path,expected in config.get('fontes_sha256',{}).items():
        if io.sha(ROOT/path)!=expected:raise ValueError('Fonte alterada: revisar hipóteses e hashes antes de simular: '+path)
    if args.iteracoes:config['iteracoes']=args.iteracoes
    if args.data_chaves:config['data_chaves']=args.data_chaves
    if config['iteracoes']<20000:raise ValueError('Execução requer pelo menos 20000 iterações')
    if config['data_chaves']:date.fromisoformat(config['data_chaves'])
    if config['reserva']!=10000:raise ValueError('Reserva fixa do projeto é10000; não alterar limite vigente')
    if abs(sum(r['central'] for r in config['itens'] if r['ativo'])-budget()[1])>.005:
        raise ValueError('Centrais da base não reconciliam orçamento vigente; modelar alteração em cenário nomeado')
    proposals,proposal_status=proposal_inputs(args.comparacao)
    scenarios=config['cenarios'][:]
    for p in proposals:
        scenarios.append(dict(id='Proposta_'+p['fornecedor'],faixa_marcenaria=[float(p['equivalente_min']), (float(p['equivalente_min'])+float(p['equivalente_max']))/2,float(p['equivalente_max'])],nota='Faixa completa do comparador; moda central hipotética, sem escolher fornecedor'))
    summary=[];long=[];critical=[];sens=[];all_results={}
    for scenario in scenarios:
        if scenario.get('sem_base'):
            summary.append(dict(cenario=scenario['id'],status='sem base — não calculado',nota=scenario['nota']));continue
        active_config=copy.deepcopy(config)
        if scenario.get('faixa_marcenaria'):
            next(r for r in active_config['itens'] if r['id']=='Marcenaria')['triangular']=scenario['faixa_marcenaria']
        data=simulate(active_config,scenario);result=stats(data);all_results[scenario['id']]=result
        summary.append(dict(cenario=scenario['id'],status='simulação condicional',nota=scenario.get('nota',config['escopo_base']),**{name:result[name] for name in result if not isinstance(result[name],dict)},
            custo_P50=result['execucao']['P50'],mudanca_P50=result['mudanca']['P50']))
        for metric in ['execucao','total_planejado','marcenaria','mudanca']:
            row=dict(cenario=scenario['id'],metrica=metric,**result[metric])
            if metric=='mudanca' and config['data_chaves']:
                for q in ['P10','P50','P80','P90']:row['data_'+q]=(date.fromisoformat(config['data_chaves'])+timedelta(days=math_ceil(result[metric][q]*7))).isoformat()
            long.append(row)
        critical += [dict(cenario=scenario['id'],atividade=k,frequencia=float(np.mean(v))) for k,v in data['criticos'].items()]
        sens += [dict(cenario=scenario['id'],**r) for r in sensitivity(data)]
        np.savez_compressed(output/(scenario['id']+'_Iteracoes.npz'),execucao=data['execucao'],total_planejado=data['total_planejado'],marcenaria=data['marcenaria'],mudanca=data['mudanca'])
        if scenario['id']=='Integral_R44':base_data=data
    io.write_csv(AREA/'Resumo_cenarios.csv',summary,sorted(set(k for r in summary for k in r)))
    io.write_csv(AREA/'Percentis.csv',long,['cenario','metrica','P10','P50','P80','P90','data_P10','data_P50','data_P80','data_P90'])
    io.write_csv(AREA/'Sensibilidade.csv',sens,['cenario','alvo','entrada','spearman','pergunta'])
    io.write_csv(AREA/'Criticidade.csv',critical,['cenario','atividade','frequencia'])
    dependency_path=ROOT.parent/'outputs/Codex_cotacao_e_chaves/Linhas_dependentes_medidas.csv'
    deps=io.read_csv(dependency_path) if dependency_path.exists() else []
    for metric in ['execucao','mudanca']:
        counts,edges=np.histogram(base_data[metric],bins=40)
        io.write_csv(output/('Histograma_'+metric+'.csv'),[dict(minimo=float(a),maximo=float(b),contagem=int(n)) for a,b,n in zip(edges[:-1],edges[1:],counts)],['minimo','maximo','contagem'])
    reuse=ROOT.parent/'outputs/Cronograma_risco'
    external_sources=[p for p in [reuse/name for name in ['Cronograma_risco.json','Escopo_cronograma.csv','Marcos_cronograma.csv','Limites_compras.csv']] if p.exists()]
    sources={str(Path('../outputs')/p.parent.name/p.name):io.sha(p) for p in external_sources}
    sources[args.entrada.resolve().relative_to(ROOT).as_posix() if ROOT in args.entrada.resolve().parents else 'entrada_propria']=io.sha(args.entrada)
    if args.comparacao.exists():sources['../outputs/Codex_cotacao_e_chaves/Comparacao.json']=io.sha(args.comparacao)
    if dependency_path.exists():sources['../outputs/Codex_cotacao_e_chaves/Linhas_dependentes_medidas.csv']=io.sha(dependency_path)
    reference_files=[*sorted((ROOT/'05_Orcamento_e_cronograma/Orcamento').rglob('Analise*.md')),
        *sorted((ROOT/'04_Moveis/Plano_de_corte').glob('Custos*.csv')),
        ROOT/'05_Orcamento_e_cronograma/Plano_execucao_ate_31_10.md',ROOT/'06_Entregas/Cotacao/README.md',
        ROOT/'08_Contratos_e_atraso/README.md',ROOT/'08_Contratos_e_atraso/Pesquisa/README.md',
        ROOT/'01_Programa_e_decisoes/Perguntas_em_aberto/Perguntas.csv',ROOT/'01_Programa_e_decisoes/Perguntas_em_aberto/Origens.csv']
    sources.update({p.relative_to(ROOT).as_posix():io.sha(p) for p in reference_files if p.exists()})
    manifest=dict(semente=config['semente'],gerador='numpy.default_rng/PCG64',numpy=np.__version__,iteracoes_por_cenario=config['iteracoes'],
        data_chaves=config['data_chaves'],datas_calendario='indeterminadas' if not config['data_chaves'] else 'condicionadas à data informada',
        propostas=proposal_status,vinculos_medidas=len(deps),linhas_cotacao_dependentes=len({r['linha'] for r in deps}),
        fontes_sha256=sources,resultados=all_results,independencia=config['independencia'],aviso=NOTICE,
        saidas_sha256={p.name:io.sha(p) for p in sorted(output.iterdir()) if p.suffix in {'.npz','.csv'} and ('Iteracoes' in p.name or 'Histograma' in p.name)})
    io.dump(output/'Simulacao_risco.json',manifest)
    readme(config,summary,long,sens,critical,manifest,output)
    print(json.dumps(dict(cenarios=len(all_results),iteracoes=config['iteracoes'],referencia_integral=all_results['Integral_R44'],propostas=proposal_status),ensure_ascii=False))


def math_ceil(v):
    return int(np.ceil(v))


def readme(config,summary,long,sens,critical,manifest,output):
    text=['# Risco de orçamento e prazo','', '**Simulação condicional, sem nova decisão ou revisão de orçamento/cronograma.** '+NOTICE,
        f"Semente {config['semente']}, numpy {np.__version__}, PCG64; {config['iteracoes']} iterações por cenário. Data das chaves: {config['data_chaves'] or 'não documentada; datas de calendário indeterminadas'}. Resultados de prazo em semanas corridas após chaves.",
        manifest['propostas']+'. Nenhuma oferta incompleta ou fictícia foi transformada em preço equivalente completo.', '',
        '## Percentis','', '| Cenário | Métrica | P10 | P50 | P80 | P90 |','|---|---|---:|---:|---:|---:|']
    text += [f"| {r['cenario']} | {r['metrica']} | {r['P10']:.2f} | {r['P50']:.2f} | {r['P80']:.2f} | {r['P90']:.2f} |" for r in long if r['metrica'] in {'execucao','mudanca'}]
    text += ['', '## Probabilidades condicionais','', '| Cenário | Execução ≤120mil | Execução ≤130mil | Marcenaria ≤35mil | Mudança ≤9 / ≤10 / ≤12 |','|---|---:|---:|---:|---|']
    for r in summary:
        if r['status'].startswith('sem base'):continue
        text.append(f"| {r['cenario']} | {r['execucao_ate120']:.1%} | {r['execucao_ate130_usa_reserva']:.1%} | {r['marcenaria_ate35']:.1%} | {r['mudanca_ate9']:.1%} / {r['mudanca_ate10']:.1%} / {r['mudanca_ate12']:.1%} |")
    text += ['', 'Execução é gasto simulado. Reserva fixa de10mil não é custo incorrido: total planejado = execução + reserva; probabilidade desse total ≤ R$ 130 mil é a mesma da execução ≤ R$ 120 mil. Execução ≤ R$ 130 mil admite consumir reserva; isso não autoriza fazê-lo. Meta de R$ 35 mil é comparada ao pacote com retrabalho, além do preço de proposta isolado no CSV. Integral R44 tem centrais137.748,11; D05-C documental tem127.101,22; ambos são bases documentais sem contrato, não somados.',
        'O cenário “Somente_se_propostas_ate35mil” impõe R$ 35 mil como teto de entrada de proposta integral, não calcula chance de conseguir desconto. Retrabalho/armazenamento podem fazê-lo ultrapassar. “Medida_real_diverge” força a ocorrência, sem inferir probabilidade da tabela de medidas. “Com_climatizacao_a_cotar” não foi calculado: custo ausente não é zero. Impermeabilização opcional altera somente prazo; não se retirou custo sem rateio.', '',
        '## Entradas, hipóteses e rede','',
        '[JSON editável](../../ferramentas/estudos/modelos/Risco_hipoteses.json) e [percentis](Percentis.csv), [resumo](Resumo_cenarios.csv), [Spearman](Sensibilidade.csv), [criticidade dinâmica](Criticidade.csv). Os custos de cada categoria conservam origem/central/tipo no JSON. Estimativa usa±15%, provisão±30%, cotado sem validade±10%, preço confirmado é ponto. São regras de simulação onde falta faixa completa; não ofertas. Pontos podem ser editados para faixa documentada em triangular. Reserva é ponto separado e climatização adicional está sem base.',
        'Custos_chapas/Custos_cenarios/Custos_propostas são parciais de subconjuntos, não faixa instalada das categorias: não extrapolar. Limite_e_metas e análises históricas não substituem a tabela R44. Ofertas completas integrais do comparador, se surgirem, criam cenário Fxx por faixa, com moda central hipotética; não escolhe fornecedor. Confirmação por SKU e serviços continua necessária.',
        'Reaproveita os29 nós de Cronograma_risco e o motor topológico existente. O agregado da semana 7–8 sai para evitar duplicação, e são acrescentadas montagem restante, instalação de pedras e louças/eletros. Predecessores novos estão marcados no JSON como hipótese. Marcenaria corre em paralelo à obra; inferiores aguardam fabricação e piso; gabarito e pedras vêm depois. Semanas de serviço ausentes recebem faixas explícitas de hipótese, não alegação de medição.',
        'Fabricação de 5–6 semanas, abastecimento de 1–3 semanas e box de 1–3 semanas são limites típicos documentados, não compromisso. Modas centrais são hipóteses. Pedras de 7–10 dias e 1–2 semanas são cenários separados. RT, envio e definições começam em −4 por hipótese de preparo antecipado; não é data conhecida. Confirmar disponibilidade e calendário útil/corrido; simulação usa dias/7.',
        'Eventos, probabilidades e impactos estão no JSON: exigência do condomínio 20%, medida divergente 25%, falta de material 20%, atraso de marcenaria 20% e pedra 15%. Não são frequências observadas. Fila de oficina 2–4 entra somente no evento, fora do prazo de produção. Retrabalho 2–5–10% da marcenaria só ocorre no mesmo evento que atrasa executivo; armazenamento hipotético de R$ 150/semana incide após semana 12.',
        'Materiais além das ferragens são supostos disponíveis no início de cada etapa; seus limites de pedido anteriores permanecem em Limites_compras.csv e devem ser conferidos. O evento de falta de material está ligado ao abastecimento de ferragens no JSON; atrasos adicionais de outros materiais não estão quantificados. Resultado de 0% significa zero ocorrências na amostra, não impossibilidade; erro amostral máximo aproximado de 0,35 ponto percentual em 20 mil, sem cobrir erro das hipóteses.',
        config['independencia']+' Correlações de Spearman não são efeitos causais nem parcelas somáveis. Frequência crítica é fração de cenários com folga total zero, recalculada por passagens direta/reversa; empates contam todos os nós críticos. O sumário anterior sem parâmetros permanece indeterminado: esta é outra análise com hipóteses autorizadas.',
        f"Medidas: {manifest['vinculos_medidas']} vínculos e {manifest['linhas_cotacao_dependentes']} linhas da cotação expostas; não são quantidades de compras, peças novas ou percentuais de reajuste. O cenário de divergência usa esse sinal de exposição, sem ratear custo por contagem.", '',
        '## Onde melhorar a informação','', '| Entrada | Alvo | Spearman | Pergunta |','|---|---|---:|---|']
    base=[r for r in sens if r['cenario']=='Integral_R44']
    chosen=[];seen=set()
    for r in sorted(base,key=lambda r:-abs(r['spearman'])):
        if r['pergunta'] and r['pergunta'] not in seen:
            chosen.append(r);seen.add(r['pergunta'])
        if len(chosen)==5:break
    text += [f"| {r['entrada']} | {r['alvo']} | {r['spearman']:.3f} | {r['pergunta']} |" for r in chosen]
    text += ['', 'Prioridade indicativa por associação no modelo: obter cotação, prazo aceito, medidas e parecer nos IDs do [pacote](../../01_Programa_e_decisoes/Perguntas_em_aberto/README.md). Não demonstra valor monetário de informação nem ganho garantido de prazo. Os dez primeiros por alvo/cenário estão no CSV.', '',
        '## Rodar','', 'Da raiz, `. ..\\ferramentas_locais\\ativar.ps1`, depois:', '',
        '```powershell','python -B ferramentas/estudos/risco_orcamento_prazo.py','python -B ferramentas/estudos/test_risco_orcamento_prazo.py','```','',
        '`--entrada caminho.json`, `--iteracoes 20000` ou mais, `--data-chaves YYYY-MM-DD` somente quando informada/documentada; `--saida` exige pasta externa. `--gerar-modelo` substitui a configuração: não usar sobre hipóteses próprias sem preservar a entrada externa. Mesma semente/configuração/versão reproduz arrays e estatísticas. Histograma CSV e iterações NPZ ficam externos; nenhum pacote novo instalado.','',
        'SHA256 Simulacao_risco.json: `'+io.sha(output/'Simulacao_risco.json')+'`. Os hashes individuais de iterações/histogramas e fontes estão nesse manifesto externo.']
    (AREA/'README.md').write_text('\n'.join(text)+'\n',encoding='utf-8',newline='\n')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--entrada',type=Path,default=MODEL);parser.add_argument('--saida',type=Path,default=OUT)
    parser.add_argument('--iteracoes',type=int);parser.add_argument('--data-chaves');parser.add_argument('--gerar-modelo',action='store_true')
    parser.add_argument('--comparacao',type=Path,default=ROOT.parent/'outputs/Codex_cotacao_e_chaves/Comparacao.json')
    run(parser.parse_args())
