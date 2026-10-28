"""Quantitativos de cotação condicionais; orçamento e CAD preservados."""
import argparse
import csv
import json
from collections import Counter,defaultdict
from pathlib import Path
from gerar_furacao import ROOT,OUT,TECH,load,panels,write_csv
from conferir_furacao import read

LIMIT_SOURCE='https://publications.blum.com/2024/catalogue/en/76/ p.76; https://ea.blum.com/en/opening-angle-stops-for-110-and-107-hinges/ regra de montagem (sem pagina)'
PROPOSED_LOSS=.10
# Front normal and side are proposals for edge identification, never new CAD datums.
FRONTS={f'P{i:02}':(1,0) for i in range(1,21)}
FRONTS.update(P02=None,P04=(0,0),P17=(0,0),P20=(0,1))
KEEP_DISASSEMBLY={'P01':'roupeiro alto: propor desmontagem para transporte',
                  'P17':'caixa longa do escritorio: propor desmontagem para transporte',
                  'P19':'manter separado enquanto divergem12 documentais e8 do mapa'}


def proposed_edges(p):
    """Physical rule + explicit C/L edge proposal; unidentified contours stay pending."""
    name=p['name'].lower();pid=p['id'];all_edges=['C0','C1','L0','L1']
    if any(s in name for s in ['porta','frente','folha']) or pid.startswith('Frente'):
        return 'porta/frente',all_edges,1.,'quatro bordas retas do envelope; cavas/recortes fora da soma'
    if pid.startswith('Gaveta'):
        if ('axes' in p and p['axes'][2]==2) or pid in {'GavetaComumR062','GavetaComumR074','GavetaComumR086'}:
            return 'fundo gaveta',[],.45,'nenhuma borda; selagem e encaixe a confirmar'
        return 'caixa gaveta',['L1'],.45,'borda superior C proposta; identificar aresta nas pecas equivalentes'
    if 'fundo' in name:return 'fundo',[],.45,'nenhuma borda; recortes e selagem fora da soma'
    if p['contour']!='Retangular':
        return 'contorno especial',None,None,'descricao/exposicao pendente; nao calcular perimetro recortado pelo envelope'
    if p['mod']=='P13':
        return 'prateleira aparente',['C0','C1','L0'],1.,'frente e duas laterais expostas propostas; traseira junto a parede sem fita'
    if any(s in name for s in ['painel','faixa','rodapé','rodape']) or pid.startswith('BancoR43_Painel'):
        return 'aparente',all_edges,1.,'quatro bordas propostas como expostas; conferir contatos/arremates por ID'
    front=FRONTS[p['mod']]
    if front and 'axes' in p and front[0] in p['axes'][:2]:
        edge=('C' if p['axes'][0]==front[0] else 'L')+str(front[1])
        return 'caixa/prateleira/apoio',[edge],.45,'somente borda frontal visivel; direcao frontal proposta em FRONTS'
    return 'sem classificacao fisica',None,None,'descricao/exposicao pendente; nao inferir comprimento pela maior dimensao'


def edge_rows(ps):
    rows=[];groups=defaultdict(lambda:[0.,0])
    for p in ps.values():
        kind,edges,thickness,detail=proposed_edges(p)
        colour=p['finish'].split(' — ')[0]
        if 'Arenza liso' in colour:colour='Arenza liso (referencia nominal)'
        if colour.startswith('Um único padrão'):colour='Padrao a definir'
        metres=None if edges is None else sum(p['l'] if e.startswith('C') else p['c'] for e in edges)/1000
        row=dict(movel=p['mod'],peca=p['id'],tipo=kind,cor=colour,espessura_chapa_mm=p['t'],espessura_fita_mm=thickness if thickness is not None else '',
                 **{e:('pendente' if edges is None else int(e in edges)) for e in ['C0','C1','L0','L1']},
                 metros_fita_definidos='',metros_propostos_retos='' if metres is None else round(metres,4),perda_percentual=PROPOSED_LOSS*100,
                 metros_propostos_com_perda='' if metres is None else round(metres*(1+PROPOSED_LOSS),4),
                 perimetro_envelope_m=round(2*(p['c']+p['l'])/1000,4),situacao='regra proposta, a confirmar com Elias/oficina',detalhe=detail)
        rows.append(row)
        if metres is not None:
            groups[(colour,thickness)][0]+=metres;groups[(colour,thickness)][1]+=1
    totals=[dict(cor=c,espessura_fita_mm=t,metros_propostos_retos=round(v[0],4),perda_percentual=10,metros_propostos_com_perda=round(v[0]*1.10,4),paineis_com_regra=v[1],situacao='regra proposta, a confirmar com Elias/oficina') for (c,t),v in sorted(groups.items())]
    return rows,totals


def estimate(holes,args):
    operations=Counter((h['movel'],h['tipo']) for h in holes)
    default={typ:((25,45) if 'caneco' in typ or 'corpo' in typ else (12,25) if 'cavilha' in typ else (8,20)) for _,typ in operations}
    if args.tempos:
        for r in read(args.tempos):default[r['tipo']]=(float(r['segundos_min']),float(r['segundos_max']))
    rows=[];totals=defaultdict(lambda:[0.,0.]);types=defaultdict(lambda:[0,0.,0.])
    for (mod,typ),qty in sorted(operations.items()):
        low,high=default[typ];pending=sum(h['movel']==mod and h['tipo']==typ and h['situacao']=='parâmetro a confirmar' for h in holes)
        rows.append(dict(movel=mod,tipo=typ,furos=qty,com_parametros=pending,segundos_por_furo_min=low,segundos_por_furo_max=high,horas_min=round(qty*low/3600,4),horas_max=round(qty*high/3600,4),fonte='hipotese de planejamento da oficina; nao medido'))
        totals[mod][0]+=qty*low/3600;totals[mod][1]+=qty*high/3600
        types[typ][0]+=qty;types[typ][1]+=qty*low/3600;types[typ][2]+=qty*high/3600
    for mod in [f'P{i:02}' for i in range(1,21)]:
        faces=len({(h['peca'],h['face']) for h in holes if h['movel']==mod});low=faces*args.setup_min/60;high=faces*args.setup_max/60
        rows.append(dict(movel=mod,tipo='Preparacao por face',furos=0,com_parametros='',segundos_por_furo_min='',segundos_por_furo_max='',horas_min=round(low,4),horas_max=round(high,4),fonte=f'hipotese: {faces} faces x {args.setup_min}-{args.setup_max}min; sem economia por lote'))
        totals[mod][0]+=low;totals[mod][1]+=high
    for mod,(low,high) in totals.items():rows.append(dict(movel=mod,tipo='Subtotal incluindo preparacao',furos=sum(v for (m,_),v in operations.items() if m==mod),com_parametros='',segundos_por_furo_min='',segundos_por_furo_max='',horas_min=round(low,4),horas_max=round(high,4),fonte='nao somar subtotal novamente as operacoes'))
    return rows,totals,types


def alternatives(joints,holes,bom,args):
    policy=[]
    for j in joints:
        if j['conector']!='Minifix 15':continue
        reason=KEEP_DISASSEMBLY.get(j['movel'])
        policy.append(dict(movel=j['movel'],junta=j['junta'],peca_a=j['a'],peca_b=j['b'],quantidade=int(j['quantidade']),alternativa='Minifix 15' if reason else 'Confirmat 7x50 + cavilha/cola',motivo=reason or 'caixa proposta permanente; confirmar acesso exterior, aparencia, transporte e possibilidade de cola'))
    convert={r['junta'] for r in policy if r['alternativa']!='Minifix 15'}
    virtual=[];mapped=Counter()
    for h in holes:
        j=h['grupo'].rsplit('-',1)[0];h=h.copy()
        if j in convert and h['tipo'].startswith('Minifix'):
            if h['tipo']=='Minifix Ø15 corpo':mapped[h['movel']]+=1;continue
            h['tipo']='Confirmat piloto topo' if h['papel']=='topo' else 'Confirmat passagem face'
        virtual.append(h)
    times,totals,_=estimate(virtual,args)
    base=Counter()
    for r in bom:base[(r['movel'],r['familia'])]+=float(r['quantidade'])
    rows=[]
    _,baseline_totals,_=estimate(holes,args)
    for mod in [f'P{i:02}' for i in range(1,21)]:
        n=sum(r['quantidade'] for r in policy if r['movel']==mod and r['junta'] in convert)
        for label,changes,hours in [('Minifix316',0,baseline_totals),('Desmontagem_proposta',n,totals)]:
            rows.append(dict(cenario=label,movel=mod,minifix=int(base[(mod,'Minifix 15')])-changes,confirmat=int(base[(mod,'Confirmat 7x50')])+changes,cavilhas=int(base[(mod,'Cavilhas Ø8x30')]),conectores_convertidos=changes,convertidos_com_centros=mapped[mod] if changes else 0,horas_min=round(hours[mod][0],4),horas_max=round(hours[mod][1],4),situacao='cenario proposto; nao adotado; horas somente centros mapeados',limites='cavilhas mantidas; cola em ligacoes permanentes sem volume inferido; confirmar cabecas/acesso/recortes; sem auditoria espacial alternativa'))
    return policy,rows,times


def family(item,reference):
    s=(item+' '+(reference or '')).lower()
    if 'gabarito' in s:return 'Ferramenta compartilhada'
    if 'confirmat' in item.lower():return 'Confirmat 7x50'
    if 'parafus' in item.lower():
        return 'Confirmat 7x50' if 'confirmat' in s else 'Parafusos'
    if 'cavilha' in s:return 'Cavilhas Ø8x30'
    if 'minifix' in s:return 'Minifix 15'
    if 'limitador' in s:return 'Limitador 86'
    if 'calços das dobradi' in s:return 'Base Blum 173H7100'
    if 'dobradiças das portas' in s:return 'Dobradiça Blum 71B3550'
    if 'corrediças' in s:return 'Corrediça MOVENTO400' if 'movento' in s else 'Corrediça FGVTN500'
    if 'engates' in s:return 'Engates'
    if '282.04.711' in s:return 'Suportes de prateleira'
    return item


def generate(dest,args,pecas=None,furacao=None):
    entrada_furacao=furacao or OUT
    ps=panels(pecas or ROOT/'06_Entregas/Fichas_fabricacao');tech=load(TECH)['modules']
    edges,edge_groups=edge_rows(ps)
    joints=read(entrada_furacao/'Mapa_conectores.csv');bom=[];missing=[];documentary=[]
    for mod,m in tech.items():
        selected={}
        for d in m['hardwareRows']:
            # hardwareRows is the physical inventory. Decisions describe the same
            # assemblies with different labels and must not be added a second time.
            if d['item'] not in selected or d.get('quantity') is not None:selected[d['item']]=d
        for d in selected.values():
            fam=family(d['item'],d.get('reference',''));qty=d.get('quantity')
            if fam=='Minifix 15' and qty is not None:
                documentary.append(dict(movel=mod,item=d['item'],quantidade=qty,unidade=d.get('unit',''),observacao='quantidade documental anterior; comparar, nao somar ao mapa novo'));continue
            if qty is None:
                missing.append(dict(movel=mod,item=d['item'],referencia=d.get('reference',''),quantidade='',situacao='parâmetro a confirmar',fonte=TECH));continue
            if d.get('includedIn'):
                missing.append(dict(movel=mod,item=d['item'],referencia=d.get('reference',''),quantidade=qty,situacao='incluido no kit; nao somar compra',fonte=TECH));continue
            bom.append(dict(movel=mod,familia=fam,item=d['item'],produto=d.get('reference',''),quantidade=qty,unidade=d.get('unit','unidade'),base='documental',situacao=d.get('status','nominal'),fonte=TECH))
        for kind in ['Minifix 15','Confirmat 7x50','Parafuso face a face']:
            js=[r for r in joints if r['movel']==mod and r['conector']==kind];qty=sum(int(r['quantidade']) for r in js)
            if qty:bom.append(dict(movel=mod,familia=kind,item='Mapa de contatos - '+kind,produto='catalogo de referencia, SKU a confirmar' if kind!='Minifix 15' else '262.26.034 + S100262.28.920; passagem Ø7; SKU a confirmar',quantidade=qty,unidade='conjunto' if kind=='Minifix 15' else 'unidade',base='proposta condicional',situacao='inclui contatos sem centros; nao somar 52 antigos',fonte='04_Moveis/Furacao/Mapa_conectores.csv'))
        qty=sum(int(r['cavilhas']) for r in joints if r['movel']==mod)
        if qty:bom.append(dict(movel=mod,familia='Cavilhas Ø8x30',item='Cavilhas do mapa de contatos',produto='267.82.230; face12/topo20 propostos em18mm; SKU a confirmar',quantidade=qty,unidade='unidade',base='proposta condicional',situacao='quantidade de cavilhas, dois furos por cavilha',fonte='04_Moveis/Furacao/Mapa_conectores.csv'))
    # Kit counterparts, not additional purchases.
    for mod,qty in [('P01',4),('P06',3)]:
        bom.append(dict(movel=mod,familia='Engates FGVTN500 incluidos',item='Par E/D por gaveta',produto='engate convencional correspondente; confirmar embalagem',quantidade=qty,unidade='par',base='incluido no kit; nao somar compra',situacao='cotacao deve confirmar inclusao',fonte=TECH))
    totals=defaultdict(float)
    for r in bom:totals[(r['familia'],r['unidade'],r['base'])]+=float(r['quantidade'])
    totalrows=[dict(familia=k[0],unidade=k[1],base=k[2],quantidade=v) for k,v in sorted(totals.items())]
    sums=Counter()
    for r in bom:sums[r['familia']]+=float(r['quantidade'])
    compare=[]
    for fam,base,reference in [('Dobradiça Blum 71B3550',52,'R44 memoria:42 comuns+4 canto+6 espelho; marca FGVTN anterior'),('Base Blum 173H7100',52,'R44 memoria: bases incluidas nos 52 conjuntos; recotar Blum'),('Corrediça FGVTN500',7,'R44 memoria:7 pares'),('Corrediça MOVENTO400',2,'R44 memoria:2 pares+engates'),('Suportes de prateleira',8,'R44 memoria:8 pinos espelheiro'),('Minifix 15',52,'R44 T07:52 definidos; +60 loteB e subtotal112 condicionais; memoria financeira antiga20'),('Limitador 86',0,'Memoria R44 nao previa limitador86 separado'),('Confirmat 7x50',None,'R44 sem quantidade total separada'),('Cavilhas Ø8x30',None,'R44 sem quantidade total separada'),('Parafusos',None,'R44 sem quantidade total separada'),('Parafuso face a face',None,'R44 sem quantidade total separada')]:
        qty=sums[fam];compare.append(dict(familia=fam,quantidade_cenario=qty,base_comparavel_R44='' if base is None else base,diferenca='' if base is None else qty-base,leitura=reference,condicao='proposta condicional quando vem do mapa; diferenca nao altera verba nem compra'))
    minifix_by_mod=[]
    old={'P10':20,'P11':12,'P15':8,'P19':12}
    for mod in tech:
        qty=sum(int(r['quantidade']) for r in joints if r['movel']==mod and r['conector']=='Minifix 15');minifix_by_mod.append(dict(movel=mod,minifix_mapa=qty,minifix_documentado=old.get(mod,''),diferenca='' if mod not in old else qty-old[mod],observacao='Novo mapa e alternativa de distribuicao: nao somar ao anterior; P19 fundo proposto Confirmat precisa reconciliar detalhe Minifix existente.'))
    holes=[h for p in sorted(entrada_furacao.glob('P??-coordenadas.csv')) for h in read(p)]
    times,time_totals,time_types=estimate(holes,args)
    policy,scenarios,alternate_times=alternatives(joints,holes,bom,args)
    scenario_totals=[]
    for label in ['Minifix316','Desmontagem_proposta']:
        selected=[r for r in scenarios if r['cenario']==label]
        scenario_totals.append(dict(cenario=label,**{k:round(sum(r[k] for r in selected),4) for k in ['minifix','confirmat','cavilhas','conectores_convertidos','convertidos_com_centros','horas_min','horas_max']}))
    for r in bom:
        if r['familia']=='Limitador 86':r.update(fonte=LIMIT_SOURCE,situacao='um por dobradica das portas que recebem limitador; cenario documental52 mantido')
    dest.mkdir(parents=True,exist_ok=True)
    files={'Cenarios_conectores_por_movel.csv':scenarios,'Cenarios_conectores_totais.csv':scenario_totals,'Politica_desmontagem.csv':policy,'Horas_alternativa.csv':alternate_times,'Fita_por_peca.csv':edges,'Fita_por_cor.csv':edge_groups,'Ferragens_por_movel.csv':bom,'Ferragens_totais.csv':totalrows,'Ferragens_pendentes.csv':missing,'Ferragens_documentais.csv':documentary,'Comparacao_R44.csv':compare,'Comparacao_Minifix.csv':minifix_by_mod,'Horas_furacao.csv':times}
    for name,rows in files.items():write_csv(dest/name,rows)
    summary=dict(cenarios_conectores=scenario_totals,fita_metros_propostos_retos=round(sum(float(r['metros_propostos_retos'] or 0) for r in edges),4),fita_metros_propostos_com_perda=round(sum(float(r['metros_propostos_retos'] or 0)*1.10 for r in edges),4),paineis_sem_regra_proposta=sum(r['metros_propostos_retos']=='' for r in edges),fita_metros_definidos=None,paineis_sem_mapa_borda=len(edges),perimetro_envelopes_referencia_m=round(sum(r['perimetro_envelope_m'] for r in edges),4),ferragens_por_familia=dict(sums),horas_cenario_min=round(sum(v[0] for v in time_totals.values()),2),horas_cenario_max=round(sum(v[1] for v in time_totals.values()),2),furos_no_cenario=len(holes),furos_nao_mapeados='bases, corredicas, parte das gavetas, fixacoes especiais e linhas System32 nao entram nas horas',fontes=[TECH,'05_Orcamento_e_cronograma/Orcamento/Orcamento_R43.md','05_Orcamento_e_cronograma/Orcamento/Marcenaria_35mil/Reconciliacao_ferragens_fichas_R14_2026-10-24.md'],files=list(files)+['Quantitativos.json','Quantitativos.md'])
    (dest/'Quantitativos.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines=['# Quantitativos para cotação — cenário nominal','', '## Ferragens','', '| Família | Quantidade cenário | Base R44 comparável | Diferença |','|---|---:|---:|---:|']
    for r in compare:lines.append(f'| {r["familia"]} | {r["quantidade_cenario"]:g} | {r["base_comparavel_R44"]} | {r["diferenca"]} |')
    lines+=['', '316 Minifix do mapa são cenário de contatos, incluindo juntas com centros pendentes. Não somar os 52 documentais nem os 60 do loteB. P19 passa de12 para8 Minifix porque a regra genérica atribui Confirmat ao fundo: isso é divergência a resolver com o detalhe existente, não substituição automática da decisão. P10/11/15 mantêm20/12/8. Confirmat e cavilhas incluem quatro Confirmat e oito cavilhas documentais do quadro P18, que não tem contatos elegíveis no mapa.','', 'Os 52 dobradiças/52 bases/52 limitadores e7 pares FGVTN500/2 MOVENTO400 são quantidades documentais. A conferência das portas ainda condiciona sua adoção. Engates FGVTN são sete pares incluídos a confirmar; MOVENTO dois pares separados. Parafusos das guias/engates e frentes, retenções e outras linhas sem contagem constam em Ferragens_pendentes.csv. Piano: 2 trechos e 4 articuladores documentais; produto e fixadores condicionados. Não equivalem a zero. Parafusos dos canecos/bases208 incluídos na lista documental; pinos Minifix são componentes dos conjuntos, sem nova compra duplicada.','', 'R44 T07 reconhece 52 Minifix definidos e 60 candidatos; a memória financeira antiga tinha 20. O cenário 316 difere em+264 dos 52, +204 do subtotal condicional112 e+296 dos20 históricos, sem converter nenhum subtotal em pedido de compra. Orçamento preservado; não se inferiu custo por unidade a partir da provisão global de ferragens.','', '## Fita de borda','', f'**Regra proposta, a confirmar com Elias/oficina:** {summary["fita_metros_propostos_retos"]:.4f}m de bordas retas calculadas; {summary["fita_metros_propostos_com_perda"]:.4f}m com10% de perda. Portas/frentes:4 bordas, fita1mm; laterais/base/topo/prateleira/apoios:frontal visivel, fita0,45mm; fundos:nenhuma; aparentes:bordas expostas propostas (P13 frente+duas laterais; paineis/faixas4 a conferir). Caixas de gaveta:borda superior, fundo sem fita. C0/C1 medem L, L0/L1 medem C. Contornos especiais sem descricao e arestas sem orientacao ficam pendentes: {summary["paineis_sem_regra_proposta"]} IDs. Cavas/recortes nao calculados, nenhuma compensacao no C×L. Direcoes frontais propostas por modulo no script; P02 emL exige mapa proprio. Cores agrupadas por nome nominal, nao equivalencia de SKU; espessura de fita e perda sao propostas, nao decisao. Nenhum dos249 mapas foi confirmado. Totais por cor e espessura da fita abaixo; espessura da chapa separada por ID em Fita_por_peca.csv.','', '## Horas de furação','', f'**Cenário dos{len(holes)} centros: {summary["horas_cenario_min"]:.2f}–{summary["horas_cenario_max"]:.2f}horas**, incluindo preparação por face. São horas de trabalho/máquina em hipótese de oficina, não prazo de calendário nem levantamento cronometrado. Não incluem centros ainda ausentes, corte, fita, transporte, montagem, ensaio/retrabalho e inspeção. Peças conflitantes e incompletas entram só como cenário de volume, não tarefa executável.','', '| Tipo | Furos | Horas de perfuração mín.–máx. |','|---|---:|---:|']
    for typ,(n,low,high) in sorted(time_types.items()):lines.append(f'| {typ} | {n} | {low:.2f}–{high:.2f} |')
    lines+=['','## Fita por cor e espessura proposta','', '| Cor | Fita mm | Metros retos | Com10% perda |','|---|---:|---:|---:|']
    for r in edge_groups:lines.append(f'| {r["cor"]} | {r["espessura_fita_mm"]} | {r["metros_propostos_retos"]:.4f} | {r["metros_propostos_com_perda"]:.4f} |')
    lines+=['','## Cenários de conectores para escolha','', '| Cenário | Minifix | Confirmat | Cavilhas | Horas mín.–máx. |','|---|---:|---:|---:|---:|']
    for r in scenario_totals:lines.append(f'| {r["cenario"]} | {r["minifix"]:g} | {r["confirmat"]:g} | {r["cavilhas"]:g} | {r["horas_min"]:.2f}–{r["horas_max"]:.2f} |')
    lines+=['','Alternativa: propor manter Minifix em P01 (transporte do roupeiro), P17 (caixa longa) e P19 (divergencia ainda aberta); trocar nos demais contatos por Confirmat+cavilha/cola. E uma proposta de onde desmontar, nao necessidade comprovada. Politica_desmontagem.csv identifica cada junta, motivo e quantidade; Cenarios_conectores_por_movel.csv mostra o impacto. Nao foram trocados o mapa nem os CSVs de coordenadas. Confirmar transporte, cabecas aparentes, acesso exterior e possibilidade de cola antes de escolher. Fixacoes de pecas removiveis nao cobertas pelo mapa continuam pendentes.','', 'As horas alternativas substituem apenas os tres centros Minifix por dois estagios Confirmat nos grupos ja mapeados; operacao escalonada considera passagem+escareado no mesmo ciclo, a confirmar com a broca. Contatos sem centros permanecem na compra condicional, sem inventar horas. Preparacao por face e recalculada; cola/aperto/montagem ficam fora. Cavilhas mantidas; nenhum volume de cola inferido. Demais familias sao as mesmas de Ferragens_por_movel.csv.','', 'Limitador86: manter52. Produto70T3553 em [Blum p.76](https://publications.blum.com/2024/catalogue/en/76/); a [regra oficial de montagem](https://ea.blum.com/en/opening-angle-stops-for-110-and-107-hinges/) determina um em cada dobradica da porta que receber o recurso (artigo sem paginacao). A pagina do catalogo identifica o produto; nao atribuir a ela a regra do artigo.','', '**P19:12 documentais ×8 do mapa. Nenhuma troca decidida.** Quatro conjuntos de diferenca estao ligados a classificacao generica do fundo como Confirmat. Manter as duas quantidades visiveis e reconciliar o detalhe do fundo antes da cotacao definitiva.','', '**Perguntas para Elias:** manter cenario316 ou escolher alternativa com desmontagem em P01/P17/P19? Confirmar regra de fita e espessuras1/0,45mm com10% de perda? No P19, preservar detalhe de12 Minifix ou propor8+Confirmat no fundo?']
    lines+=['', f'Hipóteses: caneco/corpo 25–45s; cavilha 12–25s; demais 8–20s; preparação {args.setup_min:g}–{args.setup_max:g}min por face. Opções `--tempos CSV` (tipo;segundos_min;segundos_max), `--setup-min` e `--setup-max` substituem taxas. Quantidades e subtotais por móvel em Horas_furacao.csv. Não somar linhas Subtotal novamente.','', 'Reproduzir: `python -B ferramentas/estudos/quantificar_furacao.py`; `--saida DIR` para ensaios externos. Quantitativos monetários de R44, medidas do imóvel e modelo não foram alterados.']
    (dest/'Quantitativos.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in summary.items() if k not in ['files','fontes','ferragens_por_familia']},ensure_ascii=False));return summary


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--saida',type=Path,default=OUT);ap.add_argument('--tempos',type=Path);ap.add_argument('--setup-min',type=float,default=2);ap.add_argument('--setup-max',type=float,default=5);a=ap.parse_args();generate(a.saida,a)
