"""Reconcilia referencias locais; nao pesquisa precos nem adota propostas."""
import json
from decimal import Decimal as D
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / '03_Ambientes/Iluminacao/Fechamento_custo_beneficio/Composicao_CB02.json'
OUT = ROOT / '05_Orcamento_e_cronograma/Orcamento/Reconciliacao_T07.json'

def main():
    source = json.loads(SOURCE.read_text(encoding='utf-8'), parse_float=D)
    totals = {f'L{i:02}': D(0) for i in range(1, 8)}
    rows = []
    mapping = {'C1':'L03', 'L1':'L04', 'Q01/Q02':'L07',
               'S1/E04':'L02', 'Q-geral':'L02', 'S2':'L01',
               'E-TV/E-prateleiras':'L06', 'C2/S3/Q06':'L06',
               'C2/S3/Q06/E-prateleiras':'L06'}
    for item in source['items']:
        amount = D(str(item['subtotal_brl']))
        assert D(str(item['quantity'])) * D(str(item['unit_price_brl'])) == amount
        if item['product'] == 'WiZmote':
            allocation = {'L02':D('186.48'), 'L06':D('186.48')}
        elif item['group'] == 'B09/B10/B11':
            allocation = {'L04':D('141.90'), 'L05':D('288.72'), 'L06':D('182.02')}
        else:
            allocation = {mapping[item['group']]:amount}
        assert sum(allocation.values()) == amount
        for code, value in allocation.items():
            totals[code] += value
        rows.append({'product':item['product'], 'source_group':item['group'],
                     'amount_brl':str(amount), 'allocation_brl':{k:str(v) for k,v in allocation.items()},
                     'condition':item['status']})
    total = sum(totals.values())
    assert total == D(str(source['known_components_scenario_brl'])) == D('4415.94')
    assert sum([D('141.90'),D('288.72'),D('182.02')]) == D('612.64')
    result = {'status':'CENARIO_CONDICIONADO_NAO_ADOTADO', 'source_date':source['date'],
              'source':str(SOURCE.relative_to(ROOT)).replace('\\','/'),
              'groups_brl':{k:str(v) for k,v in totals.items()}, 'items':rows,
              'lighting_scenario_brl':str(total), 'lighting_budget_brl':'3540.00',
              'difference_brl':str(total-D('3540')), 'execution_budget_brl':'137748.11',
              'execution_if_scenario_adopted_brl':str(D('137748.11')-D('3540')+total),
              'old_bathroom_delta_brl':'10.62', 'old_delta_added_again':False,
              'carpentry_provision_brl':{'materials':'20800','hardware':'9200','services':'16500','total':'46500'},
              'exclusions':source['exclusions'], 'new_prices_researched':False,
              'cad_changed':False, 'global_budget_changed':False}
    OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='items'},ensure_ascii=True))

if __name__ == '__main__':
    main()
