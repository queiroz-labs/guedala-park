"""Consolida fontes nominais sem escolher entre divergências nem recalcular corte/CAD.

CSV sintético no pacote; conferências e detalhe somente no diretório externo pedido.
"""
from pathlib import Path
from collections import Counter, defaultdict
from html import escape
import argparse
import csv
import hashlib
import json
import math
import re

from corte_guilhotina import load_panels

ROOT = Path(__file__).resolve().parents[2]
AREA = '04_Moveis/Proximas_decisoes/Corte_e_formatos/'
FUR = '04_Moveis/Furacao/'
CSV = ROOT/'06_Entregas/Cotacao/Quantidades_referencia.csv'
FIELDS = ['grupo','item','movel','padrao','espessura_mm','formato','quantidade',
          'unidade','quantidade_com_perda','base','fonte','observacao']


def read(path):
    with Path(path).open(encoding='utf-8-sig',newline='') as f:
        return list(csv.DictReader(f,delimiter=';'))


def write(path, rows, fields=None):
    with Path(path).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields or list(rows[0]),delimiter=';')
        w.writeheader();w.writerows(rows)


def expanded_fichas(root=ROOT):
    panels={}
    for path in sorted((root/'06_Entregas/Fichas_fabricacao').glob('P??-pecas.csv')):
        for n,r in enumerate(read(path),2):
            ids=[x.strip() for x in r['IDs CAD'].split('|')]
            if len(ids)!=int(r['Qtd']):
                raise ValueError(f'{path.name}:{n}: Qtd diferente dos IDs')
            for ident in ids:
                key=(path.name[:3],ident)
                if key in panels:raise ValueError(f'ID repetido: {key}')
                panels[key]=dict(c=float(r['C nominal mm']),l=float(r['L nominal mm']),
                    t=float(r['Esp. envelope mm']),fonte=f'{path.relative_to(root).as_posix()}:{n}')
    return panels


def checks_equal(checks, item, actual, expected, source, cause):
    equal=math.isclose(actual,expected,abs_tol=1e-7,rel_tol=1e-9) if isinstance(actual,(int,float)) and isinstance(expected,(int,float)) else actual==expected
    checks.append(dict(item=item,valor_A=actual,valor_B=expected,
        resultado='confere' if equal else 'divergencia',fonte=source,
        causa_provavel='' if equal else cause,acao='Não escolher valor; preservar fontes.' if not equal else ''))


def consolidate():
    used=set(); checks=[]; rows=[]
    def source(name):
        used.add(name);return read(ROOT/name)
    def add(group,item,quantity='',unit='',**kw):
        rows.append(dict.fromkeys(FIELDS,'')|dict(grupo=group,item=item,quantidade=quantity,unidade=unit)|kw)
    ps=expanded_fichas()
    used.update(p['fonte'].split(':')[0] for p in ps.values())
    cut=load_panels()  # Só relê regras/IDs; não executa a heurística de corte.
    used.update([AREA+'analisar.py','04_Moveis/Acabamentos_por_peca.csv',AREA+'Parametros.json',
                 'ferramentas/estudos/corte_guilhotina.py'])
    cp={(p['module'],p['id']):p for p in cut}
    edge=source(FUR+'Fita_por_peca.csv'); ep={(p['movel'],p['peca']):p for p in edge}
    drill=source(FUR+'Paineis.csv'); dp={(p['mod'],p['id']):p for p in drill}
    for label,other in [('corte',cp),('fita',ep),('furacao',dp)]:
        checks_equal(checks,'IDs fichas x '+label,sorted(ps),sorted(other),FUR+'Paineis.csv / fichas / corte','Fontes regeneradas em momentos diferentes.')
        if len(other)!=len(cut if label=='corte' else edge if label=='fita' else drill):
            raise ValueError('IDs repetidos em '+label)
    for key,p in ps.items():
        for field,target in [('c','C_mm'),('l','L_mm'),('t','thickness_mm')]:
            checks_equal(checks,f'{key}: ficha x corte {field}',p[field],cp[key][target],p['fonte'],'Dimensão de fonte distinta; não substituir nominal.')
        for field in ('c','l','t'):
            checks_equal(checks,f'{key}: ficha x furacao {field}',p[field],float(dp[key][field]),p['fonte']+' / '+FUR+'Paineis.csv','Exportação de painel em revisão diferente.')
        e=ep[key]
        checks_equal(checks,f'{key}: espessura fita/ficha',p['t'],float(e['espessura_chapa_mm']),FUR+'Fita_por_peca.csv','Revisão de painel diferente.')
        if e['metros_propostos_retos']!='':
            metres=sum(float(e[k])*p['l' if k.startswith('C') else 'c'] for k in ('C0','C1','L0','L1'))/1000
            checks_equal(checks,f'{key}: metros por arestas',float(e['metros_propostos_retos']),metres,FUR+'Fita_por_peca.csv','Regra/orientação ou dimensão diferente; não descontar fita do blank.')
            checks_equal(checks,f'{key}: perda de fita',float(e['metros_propostos_com_perda']),metres*(1+float(e['perda_percentual'])/100),FUR+'Fita_por_peca.csv','Percentual/ arredondamento diferente.')
    sheets=source(AREA+'Chapas_cotacao.csv')
    selected=[r for r in sheets if r['formato']==('2750x2100' if (r['padrao'],float(r['espessura_mm'])) in [('Branco TX',18),('Azul Petroleo',18)] else '2750x1850')]
    for r in selected:
        n=sum(not p['packing_blockers'] and p['pattern']==r['padrao'] and p['thickness_mm']==float(r['espessura_mm']) for p in cut)
        checks_equal(checks,'Peças corte '+r['padrao']+'/'+r['espessura_mm'],int(r['pecas']),n,AREA+'Chapas_cotacao.csv','Resumo de corte não corresponde aos IDs atuais.')
        add('chapas',r['padrao'],int(r['chapas_encontradas']),'chapa',padrao=r['padrao'],espessura_mm=r['espessura_mm'],formato=r['formato'],base='estimativa nominal; subconjunto integral',fonte=AREA+'Chapas_cotacao.csv',observacao=f"{n} painéis; formato do conjunto misto do README de 28/10; confirmar SKU, blank e processo.")
    included=sum(not p['packing_blockers'] for p in cut)
    checks_equal(checks,'Corte: soma de grupos x IDs',sum(int(r['pecas']) for r in selected),included,AREA+'Chapas_cotacao.csv','Cobertura de grupo incompleta.')
    old=source(AREA+'Lista_base_249.csv')
    old_ids={r['id'] for r in old if r['included_in_virtual_plan']=='True'}
    current_ids={r['id'] for r in cut if not r['packing_blockers']}
    checks_equal(checks,'Corte atual x lista virtual anterior',len(current_ids),len(old_ids),AREA+'Lista_base_249.csv / Chapas_cotacao.csv','P13/Peca350 incluída pela decisão F13=A; heurística/formato também mudaram. Não somar planos.')
    for ident in sorted(current_ids^old_ids):
        checks_equal(checks,'Inclusão corte '+ident,ident in current_ids,ident in old_ids,AREA+'Lista_base_249.csv','Decisão posterior na regra corrente; lista anterior preservada.')
    colours=source(FUR+'Fita_por_cor.csv'); eg=defaultdict(lambda:[0.,0.,0])
    for e in edge:
        if e['metros_propostos_retos']=='':
            add('fita_sem_regra',e['peca'],movel=e['movel'],espessura_mm=e['espessura_chapa_mm'],base='pendente; vazio não é zero',fonte=FUR+'Fita_por_peca.csv',observacao=e['detalhe'])
        else:
            v=eg[(e['cor'],float(e['espessura_fita_mm']))]
            v[0]+=float(e['metros_propostos_retos']);v[1]+=float(e['metros_propostos_com_perda']);v[2]+=1
    for r in colours:
        k=(r['cor'],float(r['espessura_fita_mm']));v=eg[k]
        for field,actual in zip(['metros_propostos_retos','metros_propostos_com_perda','paineis_com_regra'],v):
            checks_equal(checks,'Fita '+str(k)+' '+field,actual,float(r[field]),FUR+'Fita_por_cor.csv / Fita_por_peca.csv','Agrupamento ou arredondamento divergente.')
        add('fita',r['cor'],r['metros_propostos_retos'],'m',padrao=r['cor'],espessura_mm=r['espessura_fita_mm'],quantidade_com_perda=r['metros_propostos_com_perda'],base='regra proposta; perda 10%',fonte=FUR+'Fita_por_cor.csv',observacao='Espessura desta linha é da fita; não da chapa. Cor nominal não confirma SKU.')
    bom=source(FUR+'Ferragens_por_movel.csv'); totals=source(FUR+'Ferragens_totais.csv'); bg=Counter()
    tech_path='06_Entregas/Fichas_fabricacao/Tecnica_R15.json'
    tech=json.loads((ROOT/tech_path).read_text(encoding='utf-8'));used.add(tech_path)
    for r in bom+source(FUR+'Ferragens_documentais.csv'):
        if r.get('base','documental')!='documental':continue
        candidates=[h for h in tech['modules'][r['movel']]['hardwareRows'] if h['item']==r['item'] and h.get('quantity') is not None]
        checks_equal(checks,r['movel']+' ficha técnica x '+r['item'],float(r['quantidade']),candidates[-1]['quantity'] if candidates else 'sem correspondência',tech_path+' / '+FUR+'Ferragens_por_movel.csv','Inventário documental/quantidade ou referência de item diferente; manter ambas as fontes.')
    for r in bom:bg[(r['familia'],r['unidade'],r['base'])]+=float(r['quantidade'])
    for r in totals:
        k=(r['familia'],r['unidade'],r['base'])
        checks_equal(checks,'Ferragens '+str(k),bg[k],float(r['quantidade']),FUR+'Ferragens_totais.csv / Ferragens_por_movel.csv','Soma por móvel/base diferente; não juntar unidades distintas.')
        products=sorted({x['produto'] for x in bom if (x['familia'],x['unidade'],x['base'])==k})
        add('ferragens',r['familia'],r['quantidade'],r['unidade'],base=r['base'],fonte=FUR+'Ferragens_por_movel.csv / Ferragens_totais.csv',observacao=' | '.join(products))
    for k,v in bg.items():
        if not any((r['familia'],r['unidade'],r['base'])==k for r in totals):checks_equal(checks,'Ferragem sem total '+str(k),v,'ausente',FUR+'Ferragens_totais.csv','Linha omitida no agrupamento.')
    joints=source(FUR+'Mapa_conectores.csv'); holes=[]
    for path in sorted((ROOT/FUR).glob('P??-coordenadas.csv')):holes+=source(path.relative_to(ROOT).as_posix())
    for mod in sorted({k[0] for k in ps}):
        for fam,typ in [('Minifix 15','Minifix Ø15 corpo'),('Confirmat 7x50','Confirmat piloto topo'),('Cavilhas Ø8x30','cavilha Ø8 topo')]:
            amount=sum(int(j['cavilhas']) if fam.startswith('Cavilhas') else int(j['quantidade']) if j['conector']==fam else 0 for j in joints if j['movel']==mod)
            qty=sum(float(r['quantidade']) for r in bom if r['movel']==mod and r['familia']==fam and r['base']=='proposta condicional')
            checks_equal(checks,mod+' mapa x ferragens '+fam,amount,qty,FUR+'Mapa_conectores.csv / Ferragens_por_movel.csv','Transcrição/agrupamento diferente.')
            checks_equal(checks,mod+' mapa x centros '+fam,amount,sum(h['movel']==mod and h['tipo']==typ for h in holes),FUR+'Mapa_conectores.csv / '+mod+'-coordenadas.csv','Contatos sem centros; não transformar quantidade nominal em gabarito executável.')
    for r in source(FUR+'Comparacao_Minifix.csv'):
        if r['minifix_documentado']:
            checks_equal(checks,r['movel']+' Minifix mapa x documental',int(r['minifix_mapa']),int(r['minifix_documentado']),FUR+'Comparacao_Minifix.csv','P19: regra genérica usa Confirmat no fundo; detalhe documental prevê 12 Minifix. Decisão pendente.')
    for r in source(FUR+'Comparacao_R44.csv'):
        if r['base_comparavel_R44']:
            checks_equal(checks,r['familia']+' cenário x memória',float(r['quantidade_cenario']),float(r['base_comparavel_R44']),FUR+'Comparacao_R44.csv',r['leitura']+'; não somar nem escolher entre cenários.')
    hours=source(FUR+'Horas_furacao.csv')
    checks_equal(checks,'Centros x horas sem subtotais',len(holes),sum(int(r['furos']) for r in hours if not r['tipo'].startswith('Subtotal')),FUR+'Horas_furacao.csv / coordenadas','Subtotal duplicado ou cobertura distinta.')
    masses=source('04_Moveis/Quantitativos/Massas_por_movel.csv')
    for mod in sorted({k[0] for k in ps}):
        keys=[k for k in ps if k[0]==mod];mass=next(r for r in masses if r['movel']==mod)
        checks_equal(checks,mod+' painéis x massas',len(keys),int(mass['paineis']),'04_Moveis/Quantitativos/Massas_por_movel.csv','Revisão de inventário diferente.')
        vol=sum(ps[k]['c']*ps[k]['l']*ps[k]['t']/1e9 for k in keys)
        checks_equal(checks,mod+' volume x massas',vol,float(mass['volume_envelope_m3']),'04_Moveis/Quantitativos/Massas_por_movel.csv','Envelopes ou unidades diferentes.')
        n=sum(not cp[k]['packing_blockers'] for k in keys)
        add('paineis',mod,len(keys),'painel',movel=mod,base='20 móveis integrais; inclui adiados',fonte=f'06_Entregas/Fichas_fabricacao/{mod}-pecas.csv',observacao=f'{n} no corte; {len(keys)-n} excluídos do corte; {sum(ep[k]["metros_propostos_retos"]=="" for k in keys)} sem regra de fita.')
    missing=source(FUR+'Ferragens_pendentes.csv')
    add('limite','Ferragens sem quantidade ou incluídas em kit',base='não somar como zero',fonte=FUR+'Ferragens_pendentes.csv',observacao=f'{len(missing)} linhas a esclarecer; não duplicar componentes de kit.')
    add('comparacao_nao_somar','Minifix documentais',52,'conjunto',base='referência anterior; não somar aos 316',fonte=FUR+'Ferragens_documentais.csv',observacao='P10=20, P11=12, P15=8, P19=12; mapa P19=8, diferença 4 não decidida.')
    used.add(FUR+'Ferragens_documentais.csv')
    release_path='ferramentas/site/current_release.json';used.add(release_path)
    release=json.loads((ROOT/release_path).read_text(encoding='utf-8'))
    checks_equal(checks,'Revisão CAD x base das fichas',release['cadRevision'],tech['cadRevision'],release_path+' / '+tech_path,'Fichas R15 preservam metadado R53; estudo R54 usa inventário documental sem nova extração.')
    checks_equal(checks,'Chapas correntes x memória anterior',sum(int(r['chapas_encontradas']) for r in selected),16,AREA+'README.md','14 versus 16: inclusão de P13, heurística e formatos distintos; não representa economia contratada.')
    detail=[dict(movel=k[0],peca=k[1],**ps[k],no_corte=not cp[k]['packing_blockers'],motivo_corte=' | '.join(cp[k]['packing_blockers']),fita_m=ep[k]['metros_propostos_retos'],fita_mm=ep[k]['espessura_fita_mm']) for k in sorted(ps)]
    sum_piece=round(sum(v[1] for v in eg.values()),4);sum_colour=round(sum(float(r['metros_propostos_com_perda']) for r in colours),4)
    add('comparacao_nao_somar','Fita com perda por peça',sum_piece,'m',base='comparação; não somar à fita por cor',fonte=FUR+'Fita_por_peca.csv',observacao=f'Soma por cor={sum_colour:.4f} m; diferença de arredondamento, sem escolher valor.')
    checks_equal(checks,'Fita com perda: soma por peça x por cor',sum_piece,sum_colour,FUR+'Fita_por_peca.csv / Fita_por_cor.csv','Arredondamento por peça versus por grupo; não escolher valor.')
    summary=dict(paineis=len(ps),corte=included,excluidos=len(ps)-included,chapas=sum(int(r['chapas_encontradas']) for r in selected),fita_m=round(sum(v[0] for v in eg.values()),4),fita_com_perda_soma_pecas_m=sum_piece,fita_com_perda_soma_cores_m=sum_colour,sem_regra_fita=sum(e['metros_propostos_retos']=='' for e in edge),centros=len(holes),massa_referencia_kg=sum(float(r['massa_referencia_paineis_kg']) for r in masses),divergencias=sum(c['resultado']=='divergencia' for c in checks))
    return rows,checks,detail,missing,summary,used


def annex(path=CSV):
    rows=read(path)
    def table(head,body):
        return '<table><thead><tr>'+''.join('<th>'+escape(x)+'</th>' for x in head)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+escape(str(x))+'</td>' for x in r)+'</tr>' for r in body)+'</tbody></table>'
    sheets=[r for r in rows if r['grupo']=='chapas'];edges=[r for r in rows if r['grupo']=='fita'];hardware=[r for r in rows if r['grupo']=='ferragens']
    bythick=defaultdict(lambda:[0.,0.])
    for r in edges:
        bythick[r['espessura_mm']][0]+=float(r['quantidade']);bythick[r['espessura_mm']][1]+=float(r['quantidade_com_perda'])
    families=['Dobradiça Blum 71B3550','Base Blum 173H7100','Limitador 86','Corrediça FGVTN500','Corrediça MOVENTO400','Minifix 15','Confirmat 7x50','Cavilhas Ø8x30']
    body=[]
    for fam in families:
        rr=[r for r in hardware if r['item']==fam]
        body.append([fam,f'{sum(float(r["quantidade"]) for r in rr):g}',rr[0]['unidade'],' / '.join(dict.fromkeys(r['base'] for r in rr))])
    return '<section><h2>Quantidades de referência da contratante</h2><p><b>ESTIMATIVA NOMINAL, 29/10/2026.</b> Referência integral dos 20 móveis, incluindo P16/P17 adiados; não é quantidade da etapa inicial nem ordem de compra. O fornecedor deve separar os escopos e confirmar blanks, formatos, SKUs, fita, perdas, ferragens e processo. Fichas R15 ainda declaram base R53; não renumeradas como extração R54.</p>'+table(['Padrão','Chapa mm','Formato mm','Chapas'],[[r['padrao'],r['espessura_mm'],r['formato'],r['quantidade']] for r in sheets])+f'<p><b>{sum(int(r["quantidade"]) for r in sheets)} chapas para 216 de 249 painéis; 33 excluídos.</b> As exclusões continuam fora dessa estimativa; não cotar 14 chapas como material completo. Metais, espelhos e complementos não são convertidos em chapa.</p>'+table(['Fita mm','Metros retos','Com 10% propostos'],[[t,f'{v[0]:.4f}',f'{v[1]:.4f}'] for t,v in sorted(bythick.items())])+f'<p>191,1360 m retos / 210,2496 m com perda; regra proposta, sem descontar fita dos envelopes. Os {sum(r["grupo"]=="fita_sem_regra" for r in rows)} IDs sem regra estão no CSV. Soma por peça com perda: 210,2498 m, versus 210,2496 m por cor; diferença de arredondamento, sem escolher valor. Valores ausentes não são zero.</p>'+table(['Ferragem','Quantidade','Unidade','Base'],body)+'<p>Minifix: 316 no cenário do mapa versus 52 documentais; não somar. P19: 8 no mapa versus 12 documentais, diferença não decidida. Demais componentes constam no CSV: 7 pares de engates FGVTN incluídos a confirmar, 2 pares MOVENTO separados, 2 trechos de piano e 4 articuladores; confirmar fixadores e pendências. 2.286 centros e 37 restrições são registros de estudo, não programa de máquina.</p><p><a href="Quantidades_referencia.csv">CSV único: quantidades, peças por móvel, 23 IDs sem regra e fontes</a>. Fontes: corte de 28/10 (Chapas_cotacao.csv), Fita_por_cor/peca.csv, Ferragens_por_movel/totais.csv e fichas Pxx-pecas.csv; caminhos completos em cada linha. As fontes são referências de rastreabilidade, não arquivos anexados integralmente.</p></section>'


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--detalhe',type=Path,required=True);a=ap.parse_args()
    dest=a.detalhe.resolve()
    if dest==ROOT or ROOT in dest.parents:raise ValueError('Detalhe deve ficar fora do repositório')
    rows,checks,detail,missing,summary,used=consolidate()
    dest.mkdir(parents=True,exist_ok=True)
    write(CSV,rows,FIELDS);write(dest/'Conferencias.csv',checks);write(dest/'Divergencias.csv',[c for c in checks if c['resultado']=='divergencia'])
    write(dest/'Paineis.csv',detail);write(dest/'Ferragens_pendentes.csv',missing)
    summary['fontes_sha256']={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sorted(used)}
    (dest/'Resumo_quantidades.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in summary.items() if k!='fontes_sha256'},ensure_ascii=False))


if __name__=='__main__':main()
