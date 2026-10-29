"""Auditoria aritmetica independente: biblioteca padrao, sem importar geradores.

Le fichas, mapas, dados documentais e arvores de corte persistidas. Nao abre CAD,
nao altera fontes e nao considera demonstrada a suficiencia tecnica das propostas.
"""
from pathlib import Path
from collections import Counter, defaultdict
from decimal import Decimal, ROUND_HALF_UP
import argparse
import csv
import hashlib
import json
import math

ROOT = Path(__file__).resolve().parents[2]
D = Decimal
FUR = '04_Moveis/Furacao/'
CUT = '04_Moveis/Proximas_decisoes/Corte_e_formatos/'
QUOTE = '06_Entregas/Cotacao/Quantidades_referencia.csv'
RHO = D('63.2') / (D('2.75') * D('1.85') * D('0.018'))


def decimal(value):
    if value is None or value == '':
        return None
    return D(str(value).replace(',', '.'))


def rounded(value, places):
    return value.quantize(D(1).scaleb(-places), rounding=ROUND_HALF_UP)


def expand_panels(rows, module):
    result = {}
    for row in rows:
        ids = [s.strip() for s in row['IDs CAD'].split('|')]
        if len(ids) != int(row['Qtd']) or any(not s for s in ids):
            raise ValueError('Quantidade/IDs inconsistentes em ' + module)
        for name in ids:
            if name in result:
                raise ValueError('ID duplicado: ' + name)
            result[name] = dict(id=name, module=module,
                c=decimal(row['C nominal mm']), l=decimal(row['L nominal mm']),
                t=decimal(row['Esp. envelope mm']), finish=row['Especificação documental'],
                contour=row['Contorno'])
    return result


def tape_from_edges(panel, row):
    """C0/C1 tem comprimento L; L0/L1 tem comprimento C; branco fica ausente."""
    if row['metros_propostos_retos'] == '':
        return None
    edges = [decimal(row[k]) for k in ('C0', 'C1', 'L0', 'L1')]
    if any(x not in (D(0), D(1)) for x in edges):
        raise ValueError('Mapa de bordas nao binario')
    return ((edges[0] + edges[1]) * panel['l'] +
            (edges[2] + edges[3]) * panel['c']) / D(1000)


def family(item):
    mapping = {
        'Dobradiças das portas de abrir': 'Dobradiça Blum 71B3550',
        'Calços das dobradiças': 'Base Blum 173H7100',
        'Limitadores de abertura 86°': 'Limitador 86',
        'Corrediças 500 com engates convencionais E/D': 'Corrediça FGVTN500',
        'Corrediças 400': 'Corrediça MOVENTO400',
        'Engates MOVENTO esquerdo e direito': 'Engates',
        'Gabarito MOVENTO de engates/ganchos': 'Ferramenta compartilhada',
        'Apoios das duas prateleiras': 'Suportes de prateleira',
        'Confirmat de união do quadro': 'Confirmat 7x50',
        'Cavilhas da união permanente do quadro': 'Cavilhas Ø8x30',
        'Cavilhas da interface desmontável': 'Cavilhas Ø8x30',
    }
    if item.startswith('Parafusos'):
        return 'Parafusos'
    return mapping.get(item, item)


def hardware_from_sources(technical, joints):
    inventory = defaultdict(Decimal)
    pending = []
    documentary_minifix = defaultdict(Decimal)
    for module, data in technical['modules'].items():
        for row in data['hardwareRows']:
            item, quantity = row['item'], decimal(row.get('quantity'))
            if item in ('Caixas Minifix', 'Pinos Minifix'):
                documentary_minifix[(module, item)] += quantity
                continue
            if quantity is None or row.get('includedIn'):
                pending.append((module, item))
                continue
            if row.get('exclusiveGroup'):
                raise ValueError('Alternativa exige tratamento explicito: ' + item)
            inventory[(module, family(item), row['unit'], 'documental')] += quantity
            if item == 'Corrediças 500 com engates convencionais E/D':
                inventory[(module, 'Engates FGVTN500 incluidos', 'par',
                           'incluido no kit; nao somar compra')] += quantity
    for row in joints:
        module = row['movel']
        unit = 'conjunto' if row['conector'] == 'Minifix 15' else 'unidade'
        inventory[(module, row['conector'], unit, 'proposta condicional')] += decimal(row['quantidade'])
        if decimal(row['cavilhas']):
            inventory[(module, 'Cavilhas Ø8x30', 'unidade', 'proposta condicional')] += decimal(row['cavilhas'])
    return dict(inventory), pending, dict(documentary_minifix)


def close_rect(a, b, tolerance=1e-6):
    return len(a) == len(b) and all(abs(float(x)-float(y)) <= tolerance for x, y in zip(a, b))


def validate_sheet(sheet, panels, width, height, trim=10., kerf=3.2, directional=False):
    """Reconstroi a particao guilhotinada e confronta as pecas com as fichas."""
    free = [[trim, trim, width-2*trim, height-2*trim]]
    placements = {}
    for p in sheet['placements']:
        if p['id'] in placements:
            raise ValueError('Peca repetida na chapa')
        placements[p['id']] = p
        raw = panels[p['id']]
        c, l = float(raw['c']), float(raw['l'])
        if not close_rect(sorted((p['w'], p['h'])), sorted((c, l))):
            raise ValueError('Dimensao de corte diferente da ficha: '+p['id'])
        if directional and (p['rotated'] or not close_rect((p['w'],p['h']), (max(c,l), min(c,l)))):
            raise ValueError('Sentido de veio contraria a hipotese: '+p['id'])
    cut_ids = []
    for cut in sheet['cuts']:
        match = [i for i, rect in enumerate(free) if close_rect(rect, cut['parent'])]
        if len(match) != 1:
            raise ValueError('Corte fora da arvore de retangulos livres')
        x,y,w,h = free.pop(match[0])
        pw, ph = cut['w'], cut['h']
        if pw > w+1e-6 or ph > h+1e-6:
            raise ValueError('Peca excede o retangulo de corte')
        p = placements[cut['piece']]
        if not close_rect((p['x'],p['y'],p['w'],p['h']), (x,y,pw,ph)):
            raise ValueError('Posicao diverge da arvore de corte')
        if cut['vertical_first']:
            children = [[x+pw+kerf,y,w-pw-kerf,h], [x,y+ph+kerf,pw,h-ph-kerf]]
        else:
            children = [[x,y+ph+kerf,w,h-ph-kerf], [x+pw+kerf,y,w-pw-kerf,ph]]
        children = [r for r in children if r[2] > 1e-6 and r[3] > 1e-6]
        recorded = cut['children']
        if len(children) != len(recorded) or not all(close_rect(a,b) for a,b in zip(children,recorded)):
            raise ValueError('Serra/filhos da guilhotina divergentes')
        free.extend(children)
        cut_ids.append(cut['piece'])
    if set(cut_ids) != set(placements) or len(cut_ids) != len(placements):
        raise ValueError('Cobertura dos cortes incompleta/duplicada')
    if len(free) != len(sheet['free']) or not all(any(close_rect(a,b) for b in sheet['free']) for a in free):
        raise ValueError('Sobras divergentes')
    leftovers = [r for r in free if r[2] > 300 and r[3] > 300]
    return list(placements), len(leftovers), sum(r[2]*r[3] for r in leftovers)/1e6


class Audit:
    def __init__(self, root):
        self.root = root
        self.sources = {}
        self.checks = []

    def bytes(self, name):
        p = self.root/name
        raw = p.read_bytes()
        self.sources[name] = hashlib.sha256(raw).hexdigest()
        return raw

    def rows(self, name):
        return list(csv.DictReader(self.bytes(name).decode('utf-8-sig').splitlines(), delimiter=';'))

    def data(self, name):
        return json.loads(self.bytes(name))

    def compare(self, source, item, declared, recalculated, unit='', tolerance=D('0.000001'), cause=''):
        a,b = decimal(declared),decimal(recalculated)
        if a is None or b is None:
            equal = a is b
        else:
            equal = abs(a-b) <= tolerance
        record = dict(arquivo=source, item=item, valor_documentado='' if a is None else str(a),
            valor_recalculado='' if b is None else str(b), delta='' if a is None or b is None else str(b-a),
            unidade=unit, resultado='confere' if equal else 'divergencia',
            causa=cause if not equal else '')
        self.checks.append(record)
        return record


def run(root, output, plans_path, details):
    audit=Audit(root)
    panels={}
    for module in (f'P{i:02d}' for i in range(1,21)):
        expanded=expand_panels(audit.rows(f'06_Entregas/Fichas_fabricacao/{module}-pecas.csv'),module)
        if panels.keys() & expanded.keys(): raise ValueError('IDs repetidos entre moveis')
        panels.update(expanded)
    per_module=Counter(p['module'] for p in panels.values())
    listed_panels=audit.rows(FUR+'Paineis.csv')
    for row in listed_panels:
        for axis in ('c','l','t'):
            audit.compare(FUR+'Paineis.csv',row['id']+'/'+axis,row[axis],panels[row['id']][axis],'mm',cause='Ficha e inventario de furacao divergem')
    assert {r['id'] for r in listed_panels}==set(panels)

    tape=audit.rows(FUR+'Fita_por_peca.csv')
    tape_groups=defaultdict(Decimal);piece_loss=D(0);missing=[];perimeter=D(0)
    for row in tape:
        p=panels[row['peca']];quantity=tape_from_edges(p,row)
        per=2*(p['c']+p['l'])/1000;perimeter+=per
        audit.compare(FUR+'Fita_por_peca.csv',row['peca']+'/perimetro',row['perimetro_envelope_m'],per,'m',tolerance=D('0.00005'),cause='Perimetro versus C/L das fichas')
        audit.compare(FUR+'Fita_por_peca.csv',row['peca']+'/fita',row['metros_propostos_retos'],quantity,'m',tolerance=D('0.00005'),cause='Bordas C0/C1/L0/L1 versus C/L das fichas')
        if quantity is None: missing.append(row['peca']);continue
        loss=rounded(quantity*(1+decimal(row['perda_percentual'])/100),4)
        piece_loss+=loss
        audit.compare(FUR+'Fita_por_peca.csv',row['peca']+'/perda',row['metros_propostos_com_perda'],loss,'m',tolerance=D('0.00005'),cause='Aplicacao de perda e arredondamento por peca')
        tape_groups[(row['cor'],row['espessura_fita_mm'])]+=quantity
    color_loss=D(0)
    for row in audit.rows(FUR+'Fita_por_cor.csv'):
        value=tape_groups[row['cor'],row['espessura_fita_mm']]
        audit.compare(FUR+'Fita_por_cor.csv',row['cor']+'/'+row['espessura_fita_mm'],row['metros_propostos_retos'],value,'m',tolerance=D('0.00005'),cause='Agregacao independente das bordas por cor')
        with_loss=rounded(value*D('1.1'),4);color_loss+=with_loss
        audit.compare(FUR+'Fita_por_cor.csv',row['cor']+'/perda',row['metros_propostos_com_perda'],with_loss,'m',tolerance=D('0.00005'),cause='Perda por grupo arredondada')

    joints=audit.rows(FUR+'Mapa_conectores.csv')
    tech=audit.data('ferramentas/site/fabrication/technical-r14.json')
    hardware,pending,documentary_minifix=hardware_from_sources(tech,joints)
    by_family=defaultdict(Decimal)
    for (_,fam,unit,base),q in hardware.items(): by_family[(fam,unit,base)]+=q
    hardware_rows=audit.rows(FUR+'Ferragens_por_movel.csv')
    for row in hardware_rows:
        key=(row['movel'],row['familia'],row['unidade'],row['base'])
        # Algumas familias tem varias linhas documentais no mesmo movel: comparar agregado.
        group=sum(decimal(r['quantidade']) for r in hardware_rows if (r['movel'],r['familia'],r['unidade'],r['base'])==key)
        if key not in getattr(audit,'seen_hardware',set()):
            audit.compare(FUR+'Ferragens_por_movel.csv','/'.join(key),group,hardware.get(key),row['unidade'],cause='hardwareRows + mapa de juntas, sem somar decisions ou alternativas')
            audit.seen_hardware=getattr(audit,'seen_hardware',set())|{key}
    if set(hardware)!=audit.seen_hardware: raise ValueError('Familia documental ausente no CSV')
    for row in audit.rows(FUR+'Ferragens_totais.csv'):
        audit.compare(FUR+'Ferragens_totais.csv',row['familia']+'/'+row['base'],row['quantidade'],by_family.get((row['familia'],row['unidade'],row['base'])),row['unidade'],cause='Soma independente de hardwareRows e mapa de juntas')
    pending_rows=audit.rows(FUR+'Ferragens_pendentes.csv')
    assert set(pending)=={(r['movel'],r['item']) for r in pending_rows}

    holes=[]
    for module in per_module: holes.extend(audit.rows(FUR+module+'-coordenadas.csv'))
    hole_ids=[r['furo'] for r in holes]
    if len(set(hole_ids))!=len(hole_ids): raise ValueError('IDs de furos duplicados')
    holes_panels={r['peca'] for r in holes};faces={(r['peca'],r['face']) for r in holes}
    summary=audit.data(FUR+'Resumo.json')
    for key,value in [('paineis',len(panels)),('furos',len(holes)),('juntas',len(joints)),('faces',len(faces)),('paineis_com_centros',len(holes_panels)),('paineis_sem_centros',len(panels)-len(holes_panels))]:
        audit.compare(FUR+'Resumo.json',key,summary[key],value,'contagem',cause='Contagem de IDs/linhas nas fontes primarias CSV')

    masses=audit.rows('04_Moveis/Quantitativos/Massas_por_movel.csv')
    volume_total=D(0);mass_total=D(0);conditional_count=0;conditional_total=D(0)
    for row in masses:
        module=row['movel'];pp=[p for p in panels.values() if p['module']==module]
        volume=sum((p['c']*p['l']*p['t']/D(10)**9 for p in pp),D(0))
        conditional=[p for p in pp if 'Greenplac' in p['finish'] and 'Arenza' in p['finish'] and p['t']==18]
        conditional_mass=sum((p['c']*p['l']*p['t']/D(10)**9*RHO for p in conditional),D(0))
        volume_total+=volume;mass_total+=volume*RHO;conditional_count+=len(conditional);conditional_total+=conditional_mass
        for key,value,tol in [('paineis',len(pp),D(0)),('volume_envelope_m3',volume,D('0.000000005')),('paineis_com_cenario_catalogo',len(conditional),D(0)),('subtotal_envelopes_cenario_kg',conditional_mass if conditional else None,D('0.000001')),('massa_referencia_paineis_kg',volume*RHO,D('0.000001'))]:
            audit.compare('04_Moveis/Quantitativos/Massas_por_movel.csv',module+'/'+key,row[key],value,'kg' if 'kg' in key else 'm3' if 'm3' in key else 'painel',tolerance=tol,cause='Envelopes das fichas x densidade equivalente 63,2/(2,75x1,85x0,018)')

    # Arvores persistidas sao entradas a conferir, nao resultados aceitos sem contraprova.
    plan_raw=plans_path.read_bytes();plan_data=json.loads(plan_raw)
    plans_hash=hashlib.sha256(plan_raw).hexdigest()
    plan_groups={};all_included=set();sheets_verified=0
    for result in plan_data['plans']:
        s=result['summary'];width,height=map(float,s['formato'].split('x'));ids=[];left_count=0;left_area=0
        for sheet in result['plan']['sheets']:
            found,count,area=validate_sheet(sheet,panels,width,height,directional=s['padrao'] in ('Arenza','Louro Freijo Poro'))
            ids.extend(found);left_count+=count;left_area+=area;sheets_verified+=1
        if len(ids)!=len(set(ids)): raise ValueError('Peca repetida entre chapas')
        area=sum(float(panels[n]['c']*panels[n]['l']) for n in ids)
        number=len(result['plan']['sheets']);useful=(width-20)*(height-20)
        key=(s['padrao'],str(s['espessura_mm']),s['formato'])
        plan_groups[key]=dict(sheets=number,ids=set(ids),area=area,lower=math.ceil(area/useful),utilization=round(100*area/(number*useful),2))
        all_included.update(ids)
        for field,value,tolerance in [('pecas',len(ids),D(0)),('chapas_encontradas',number,D(0)),('limite_inferior_area',math.ceil(area/useful),D(0)),('aproveitamento_util_pct',round(100*area/(number*useful),2),D('0.005')),('sobras_maiores_300x300',left_count,D(0)),('area_sobras_m2',round(left_area,4),D('0.00005'))]:
            audit.compare('Planos.json', '/'.join(key)+'/'+field,s[field],value,field,tolerance=tolerance,cause='Arvore guilhotinada, contagem e area recalculadas sem gerador')
    excluded=set(panels)-all_included
    assert excluded=={r['id'] for r in plan_data['excluded']}
    sheets_rows=audit.rows(CUT+'Chapas_cotacao.csv')
    for row in sheets_rows:
        key=row['padrao'],row['espessura_mm'],row['formato'];value=plan_groups[key]
        for column,computed in [('pecas',len(value['ids'])),('chapas_encontradas',value['sheets']),('limite_inferior_area',value['lower']),('aproveitamento_util_pct',value['utilization'])]:
            audit.compare(CUT+'Chapas_cotacao.csv','/'.join(key)+'/'+column,row[column],computed,column,tolerance=D('0.005'),cause='Contraprova da arvore persistida contra fichas atuais')

    quote_rows=audit.rows(QUOTE);quote_audit=[]
    missing_set=set(missing)
    for line,row in enumerate(quote_rows,2):
        group=row['grupo'];value=None;loss=None;scope=''
        if group=='chapas':
            value=plan_groups[(row['padrao'],row['espessura_mm'],row['formato'])]['sheets'];scope='Arvore de cortes conferida contra fichas; nao otimiza globalmente'
        elif group=='fita':
            value=tape_groups[row['padrao'],row['espessura_mm']];loss=rounded(value*D('1.1'),4);scope='C/L das fichas e mapa proposto de bordas'
        elif group=='fita_sem_regra':
            assert row['item'] in missing_set;scope='Ausencia de regra mantida; vazio nao e zero'
        elif group=='ferragens':
            value=by_family[(row['item'],row['unidade'],row['base'])];scope='hardwareRows + mapa; componentes incluidos separados'
        elif group=='paineis':value=per_module[row['movel']];scope='IDs expandidos das fichas; inclui adiados'
        elif group=='limite':
            assert str(len(pending))+' linhas' in row['observacao'];scope=f'{len(pending)} linhas documentais sem quantidade; vazio nao e zero'
        elif group=='comparacao_nao_somar':
            if row['item']=='Minifix documentais':value=sum(q for (m,item),q in documentary_minifix.items() if item=='Caixas Minifix')
            elif row['item']=='Fita com perda por peça':value=piece_loss
            else:raise ValueError('Comparacao nova nao mapeada')
            scope='Referencia separada; nao somar aos itens de compra'
        else:raise ValueError('Grupo nao auditado: '+group)
        # Conferir numeros embutidos em observacoes, sem transformar ressalvas em medidas.
        if group=='chapas':
            n=len(plan_groups[(row['padrao'],row['espessura_mm'],row['formato'])]['ids'])
            assert row['observacao'].startswith(f'{n} painéis;')
        elif group=='paineis':
            module_ids={name for name,p in panels.items() if p['module']==row['movel']}
            expected=f"{len(module_ids & all_included)} no corte; {len(module_ids & excluded)} excluídos do corte; {len(module_ids & missing_set)} sem regra de fita."
            assert row['observacao']==expected
        elif group=='fita_sem_regra':
            assert panels[row['item']]['module']==row['movel']
            assert panels[row['item']]['t']==decimal(row['espessura_mm'])
            source=next(r for r in tape if r['peca']==row['item'])
            assert row['observacao']==source['detalhe']
        elif group=='comparacao_nao_somar' and row['item']=='Minifix documentais':
            for (module,item),q in documentary_minifix.items():
                if item=='Caixas Minifix': assert f'{module}={q}' in row['observacao']
            mapped=hardware[('P19','Minifix 15','conjunto','proposta condicional')]
            assert f'mapa P19={mapped}' in row['observacao']
            assert f'diferença {documentary_minifix[("P19","Caixas Minifix")]-mapped}' in row['observacao']
        elif group=='comparacao_nao_somar' and row['item']=='Fita com perda por peça':
            assert f'Soma por cor={color_loss}' in row['observacao']
        sources=row['fonte'].split(' / ')
        for source in sources:
            source_path=Path(source) if '/' in source else Path(sources[0]).parent/source
            assert (root/source_path).is_file(), source
        result=audit.compare(QUOTE,f'linha {line}: '+row['item'],row['quantidade'],value,row['unidade'],tolerance=D('0.00005'),cause='Recálculo independente; ver fonte e escopo')
        loss_result=audit.compare(QUOTE,f'linha {line}: perda '+row['item'],row['quantidade_com_perda'],loss,row['unidade'],tolerance=D('0.00005'),cause='Perda por grupo')
        quote_audit.append(dict(linha_csv=line,grupo=group,item=row['item'],movel=row['movel'],documentado=row['quantidade'],recalculado='' if value is None else str(value),documentado_com_perda=row['quantidade_com_perda'],recalculado_com_perda='' if loss is None else str(loss),resultado='confere' if result['resultado']==loss_result['resultado']=='confere' else 'divergencia',escopo=scope))

    output.mkdir(parents=True,exist_ok=True)
    def write_csv(name,rows):
        with (output/name).open('w',encoding='utf-8-sig',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter=';');writer.writeheader();writer.writerows(rows)
    write_csv('Auditoria_linhas_cotacao.csv',quote_audit)
    divergences=[r for r in audit.checks if r['resultado']=='divergencia']
    differences=[dict(arquivo=FUR+'Fita_por_cor.csv / Fita_por_peca.csv',item='Fita com perda: soma por grupo x soma por peca',
        valor_documentado=str(color_loss),valor_recalculado=str(piece_loss),delta=str(piece_loss-color_loss),unidade='m',
        classe='bases de arredondamento distintas',causa='Perda 10% arredondada a 4 casas em cada peca versus em cada grupo; nao e falta de fita nem credito comercial')]
    for (module,item),quantity in documentary_minifix.items():
        if item!='Caixas Minifix':continue
        mapped=hardware.get((module,'Minifix 15','conjunto','proposta condicional'),D(0))
        if mapped!=quantity:
            differences.append(dict(arquivo=FUR+'Ferragens_documentais.csv / Mapa_conectores.csv',item=module+' Minifix documental x mapa',
                valor_documentado=str(quantity),valor_recalculado=str(mapped),delta=str(mapped-quantity),unidade='conjunto',
                classe='bases de escopo distintas; decisao pendente',causa='O mapa e proposta; detalhe documental anterior nao deve ser somado nem substituido automaticamente'))
    write_csv('Auditoria_diferencas.csv',differences)
    details=details.resolve()
    if details.is_relative_to(root.resolve()):
        raise ValueError('Detalhes volumosos devem ficar fora do repositorio')
    details.mkdir(parents=True,exist_ok=True)
    full_checks=details/'Conferencias.csv'
    with full_checks.open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(audit.checks[0]),delimiter=';')
        writer.writeheader();writer.writerows(audit.checks)
    # Os detalhes de todas as checagens ficam fora do git; o relatorio guarda as divergencias.
    summary=dict(quote_records=len(quote_rows),quote_numeric_records=sum(r['quantidade']!='' for r in quote_rows),quote_divergences=sum(r['resultado']=='divergencia' for r in quote_audit),checks=len(audit.checks),divergences=divergences,panels=len(panels),cut_included=len(all_included),cut_excluded=len(excluded),cut_scenarios=len(plan_groups),sheets_verified_across_scenarios=sheets_verified,tape_m=str(sum(tape_groups.values())),tape_loss_by_piece_m=str(piece_loss),tape_loss_by_color_m=str(color_loss),tape_rounding_delta_m=str(piece_loss-color_loss),tape_without_rule=len(missing),perimeter_m=str(perimeter),joints=len(joints),holes=len(holes),panels_with_holes=len(holes_panels),hardware_pending=len(pending),hardware_families=len(by_family),mass_envelope_m3=str(volume_total),mass_reference_kg=str(mass_total),mass_conditional_panels=conditional_count,mass_conditional_kg=str(conditional_total),density_equivalent_kg_m3=str(RHO),plans_sha256=plans_hash,sources_sha256=audit.sources)
    summary['checks_sha256']=hashlib.sha256(full_checks.read_bytes()).hexdigest()
    summary['differences_between_bases']=differences
    # Uma auditoria nao deve misturar entradas alteradas no meio de outra sessao.
    if any(hashlib.sha256((root/name).read_bytes()).hexdigest()!=digest for name,digest in audit.sources.items()):
        raise ValueError('Fonte alterada durante a auditoria; repetir apos estabilizar')
    (output/'Auditoria_resultado.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if divergences:write_csv('Auditoria_divergencias.csv',divergences)
    print(json.dumps({k:v for k,v in summary.items() if k!='sources_sha256'},ensure_ascii=False,indent=2))
    return summary


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--root',type=Path,default=ROOT)
    parser.add_argument('--saida',type=Path,default=ROOT/'06_Entregas/Cotacao')
    parser.add_argument('--planos',type=Path,default=ROOT.parent/'outputs/Corte_cotacao/Planos.json')
    parser.add_argument('--detalhes',type=Path,default=ROOT.parent/'outputs/Auditoria_quantidades')
    args=parser.parse_args();run(args.root,args.saida,args.planos,args.detalhes)
