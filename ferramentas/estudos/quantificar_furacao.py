"""Quantitativos de cotação condicionais; orçamento e CAD preservados."""
import argparse
import csv
import json
from collections import Counter,defaultdict
from pathlib import Path
from gerar_furacao import ROOT,OUT,TECH,load,panels,write_csv
from conferir_furacao import read


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
    ps=panels(pecas or ROOT/'06_Entregas/Fichas_fabricacao');tech=load(TECH)['modules'];edges=[];edge_totals=defaultdict(float)
    for p in ps.values():
        # All source edge maps are null; never infer visibility from contact alone.
        row=dict(movel=p['mod'],peca=p['id'],cor=p['finish'].split(' — ')[0],espessura_chapa_mm=p['t'],espessura_fita_mm='',C0='',C1='',L0='',L1='',metros_fita_definidos='',perimetro_envelope_m=round(2*(p['c']+p['l'])/1000,4),situacao='parâmetro a confirmar',detalhe='Definir bordas visiveis por ID; quatro bordas do envelope sao apenas referencia; recortes mudam contorno.')
        edges.append(row);edge_totals[(row['cor'],p['t'])]+=row['perimetro_envelope_m']
    edge_groups=[dict(cor=c,espessura_chapa_mm=t,espessura_fita_mm='',metros_fita_definidos='',referencia_perimetros_m=round(v,4),situacao='parâmetro a confirmar; sem percentual de perda aplicado') for (c,t),v in sorted(edge_totals.items())]
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
            if qty:bom.append(dict(movel=mod,familia=kind,item='Mapa de contatos - '+kind,produto='SKU a confirmar' if kind!='Minifix 15' else 'conjunto corpo+pino; passagem Ø8 pendente',quantidade=qty,unidade='conjunto' if kind=='Minifix 15' else 'unidade',base='proposta condicional',situacao='inclui contatos sem centros; nao somar 52 antigos',fonte='04_Moveis/Furacao/Mapa_conectores.csv'))
        qty=sum(int(r['cavilhas']) for r in joints if r['movel']==mod)
        if qty:bom.append(dict(movel=mod,familia='Cavilhas Ø8x30',item='Cavilhas do mapa de contatos',produto='Ø8x30; embutimento a confirmar',quantidade=qty,unidade='unidade',base='proposta condicional',situacao='quantidade de cavilhas, dois furos por cavilha',fonte='04_Moveis/Furacao/Mapa_conectores.csv'))
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
    holes=[h for p in sorted(entrada_furacao.glob('P??-coordenadas.csv')) for h in read(p)];operations=Counter((h['movel'],h['tipo']) for h in holes)
    # Transparent shop-planning assumptions, not manufacturer cycle times.
    default={typ:((25,45) if 'caneco' in typ or 'corpo' in typ else (12,25) if 'cavilha' in typ else (8,20)) for _,typ in operations}
    if args.tempos:
        for r in read(args.tempos):default[r['tipo']]=(float(r['segundos_min']),float(r['segundos_max']))
    times=[];time_totals=defaultdict(lambda:[0.,0.]);time_types=defaultdict(lambda:[0,0.,0.])
    for (mod,typ),qty in sorted(operations.items()):
        low,high=default[typ];pending=sum(h['movel']==mod and h['tipo']==typ and h['situacao']=='parâmetro a confirmar' for h in holes)
        times.append(dict(movel=mod,tipo=typ,furos=qty,com_parametros=pending,segundos_por_furo_min=low,segundos_por_furo_max=high,horas_min=round(qty*low/3600,4),horas_max=round(qty*high/3600,4),fonte='hipotese de planejamento da oficina; nao medido'))
        time_totals[mod][0]+=qty*low/3600;time_totals[mod][1]+=qty*high/3600
        time_types[typ][0]+=qty;time_types[typ][1]+=qty*low/3600;time_types[typ][2]+=qty*high/3600
    for mod in tech:
        faces=len({(h['peca'],h['face']) for h in holes if h['movel']==mod});low=faces*args.setup_min/60;high=faces*args.setup_max/60
        times.append(dict(movel=mod,tipo='Preparacao por face',furos=0,com_parametros='',segundos_por_furo_min='',segundos_por_furo_max='',horas_min=round(low,4),horas_max=round(high,4),fonte=f'hipotese: {faces} faces x {args.setup_min}-{args.setup_max}min; sem economia por lote'))
        time_totals[mod][0]+=low;time_totals[mod][1]+=high
    for mod,(low,high) in time_totals.items():times.append(dict(movel=mod,tipo='Subtotal incluindo preparacao',furos=sum(v for (m,_),v in operations.items() if m==mod),com_parametros='',segundos_por_furo_min='',segundos_por_furo_max='',horas_min=round(low,4),horas_max=round(high,4),fonte='nao somar subtotal novamente as operacoes'))
    dest.mkdir(parents=True,exist_ok=True)
    files={'Fita_por_peca.csv':edges,'Fita_por_cor.csv':edge_groups,'Ferragens_por_movel.csv':bom,'Ferragens_totais.csv':totalrows,'Ferragens_pendentes.csv':missing,'Ferragens_documentais.csv':documentary,'Comparacao_R44.csv':compare,'Comparacao_Minifix.csv':minifix_by_mod,'Horas_furacao.csv':times}
    for name,rows in files.items():write_csv(dest/name,rows)
    summary=dict(fita_metros_definidos=None,paineis_sem_mapa_borda=len(edges),perimetro_envelopes_referencia_m=round(sum(r['perimetro_envelope_m'] for r in edges),4),ferragens_por_familia=dict(sums),horas_cenario_min=round(sum(v[0] for v in time_totals.values()),2),horas_cenario_max=round(sum(v[1] for v in time_totals.values()),2),furos_no_cenario=len(holes),furos_nao_mapeados='bases, corredicas, parte das gavetas, fixacoes especiais e linhas System32 nao entram nas horas',fontes=[TECH,'05_Orcamento_e_cronograma/Orcamento/Orcamento_R43.md','05_Orcamento_e_cronograma/Orcamento/Marcenaria_35mil/Reconciliacao_ferragens_fichas_R14_2026-10-24.md'],files=list(files)+['Quantitativos.json','Quantitativos.md'])
    (dest/'Quantitativos.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines=['# Quantitativos para cotação — cenário nominal','', '## Ferragens','', '| Família | Quantidade cenário | Base R44 comparável | Diferença |','|---|---:|---:|---:|']
    for r in compare:lines.append(f'| {r["familia"]} | {r["quantidade_cenario"]:g} | {r["base_comparavel_R44"]} | {r["diferenca"]} |')
    lines+=['', '316 Minifix do mapa são cenário de contatos, incluindo juntas com centros pendentes. Não somar os 52 documentais nem os 60 do loteB. P19 passa de12 para8 Minifix porque a regra genérica atribui Confirmat ao fundo: isso é divergência a resolver com o detalhe existente, não substituição automática da decisão. P10/11/15 mantêm20/12/8. Confirmat e cavilhas incluem quatro Confirmat e oito cavilhas documentais do quadro P18, que não tem contatos elegíveis no mapa.','', 'Os 52 dobradiças/52 bases/52 limitadores e7 pares FGVTN500/2 MOVENTO400 são quantidades documentais. A conferência das portas ainda condiciona sua adoção. Engates FGVTN são sete pares incluídos a confirmar; MOVENTO dois pares separados. Parafusos das guias/engates e frentes, retenções e outras linhas sem contagem constam em Ferragens_pendentes.csv. Piano: 2 trechos e 4 articuladores documentais; produto e fixadores condicionados. Não equivalem a zero. Parafusos dos canecos/bases208 incluídos na lista documental; pinos Minifix são componentes dos conjuntos, sem nova compra duplicada.','', 'R44 T07 reconhece 52 Minifix definidos e 60 candidatos; a memória financeira antiga tinha 20. O cenário 316 difere em+264 dos 52, +204 do subtotal condicional112 e+296 dos20 históricos, sem converter nenhum subtotal em pedido de compra. Orçamento preservado; não se inferiu custo por unidade a partir da provisão global de ferragens.','', '## Fita de borda','', f'**249 IDs sem mapa C0/C1/L0/L1 nem espessura de fita. Metragem definida: desconhecida.** Soma dos perímetros de envelopes: {summary["perimetro_envelopes_referencia_m"]:.4f}m, somente referência geométrica; inclui bordas ocultas e não representa contorno real de peças especiais. Não é teto garantido para recortes. Por cor e espessura **da chapa** em Fita_por_cor.csv; coluna da espessura **da fita** vazia. Sem percentual de perdas ou compra de rolos inventados. P18 também requer selagem de bordas/cavas/furos, produto pendente.','', '## Horas de furação','', f'**Cenário dos{len(holes)} centros: {summary["horas_cenario_min"]:.2f}–{summary["horas_cenario_max"]:.2f}horas**, incluindo preparação por face. São horas de trabalho/máquina em hipótese de oficina, não prazo de calendário nem levantamento cronometrado. Não incluem centros ainda ausentes, corte, fita, transporte, montagem, ensaio/retrabalho e inspeção. Peças conflitantes e incompletas entram só como cenário de volume, não tarefa executável.','', '| Tipo | Furos | Horas de perfuração mín.–máx. |','|---|---:|---:|']
    for typ,(n,low,high) in sorted(time_types.items()):lines.append(f'| {typ} | {n} | {low:.2f}–{high:.2f} |')
    lines+=['', f'Hipóteses: caneco/corpo 25–45s; cavilha 12–25s; demais 8–20s; preparação {args.setup_min:g}–{args.setup_max:g}min por face. Opções `--tempos CSV` (tipo;segundos_min;segundos_max), `--setup-min` e `--setup-max` substituem taxas. Quantidades e subtotais por móvel em Horas_furacao.csv. Não somar linhas Subtotal novamente.','', 'Reproduzir: `python -B ferramentas/estudos/quantificar_furacao.py`; `--saida DIR` para ensaios externos. Quantitativos monetários de R44, medidas do imóvel e modelo não foram alterados.']
    (dest/'Quantitativos.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in summary.items() if k not in ['files','fontes','ferragens_por_familia']},ensure_ascii=False));return summary


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--saida',type=Path,default=OUT);ap.add_argument('--tempos',type=Path);ap.add_argument('--setup-min',type=float,default=2);ap.add_argument('--setup-max',type=float,default=5);a=ap.parse_args();generate(a.saida,a)
