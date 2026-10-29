"""Exporta retalhos e custos das propostas, sem recalcular ou alterar o corte."""
import hashlib
import json
from pathlib import Path
from custo_plano_corte import OUT, ROOT, OPTIONS, price, write

EXTERNAL = ROOT.parent / 'outputs/Plano_de_corte'
PLAN_SHA = 'eb7d827d1c32926ca0497851470b506fd7f97071f16b91088f5145298f9fb419'


def retalhos(data):
    rows = []
    for group, entry in enumerate(data['plans'], 1):
        r = entry['resumo']
        for number, sheet in enumerate(entry['plano']['sheets'], 1):
            for idx, (x, y, w, h) in enumerate(sheet['free'], 1):
                rows.append(dict(variante=r['variante'], cenario=r['cenario'], padrao=r['padrao'],
                    espessura_mm=r['espessura_mm'], desenho=f'G{group:03d}_chapa{number:02d}.svg',
                    chapa=number, retalho=idx, x_mm=x, y_mm=y, comprimento_mm=w, largura_mm=h,
                    area_m2=round(w*h/1e6, 10), reaproveitavel=w>300 and h>300,
                    limite='retangulo nominal; sem credito financeiro ou garantia de reuso'))
    return rows


def financial(groups, option):
    low = high = known = total = 0
    unknown = []
    for r in groups:
        n = int(r['chapas_subconjunto']); total += n
        lo, hi, _, _ = price(r['padrao'], float(r['espessura_mm']), option)
        if lo is None:
            unknown.append(f"{r['padrao']} {r['espessura_mm']:g} mm: {n} chapa(s)")
        else:
            known += n; low += n*lo; high += n*hi
    return dict(chapas=total, chapas_com_referencia=known, parcial_chapas_min=round(low,2),
                parcial_chapas_max=round(high,2), grupos_sem_preco=' | '.join(unknown))


def propostas(data):
    rows = []
    for variant, meta in data['variants'].items():
        if variant == 'base' or variant.startswith('sensibilidade_'): continue
        scenarios = sorted({p['resumo']['cenario'] for p in data['plans']})
        for scenario in scenarios:
            groups = [p['resumo'] for p in data['plans'] if p['resumo']['variante']==variant and p['resumo']['cenario']==scenario]
            baseline = [p['resumo'] for p in data['plans'] if p['resumo']['variante']=='base' and p['resumo']['cenario']==scenario]
            for option in OPTIONS:
                costs = financial(groups, option); base = financial(baseline, option)
                rows.append(dict(variante=variant, cenario=scenario, opcao_offwhite=option,
                    paineis_total=meta['total'], paineis_bloqueados=len(meta['bloqueados']),
                    ids_bloqueados=' | '.join(meta['bloqueados']),
                    ids_fora_formato=' | '.join(r['nao_cabem'] for r in groups if r['nao_cabem']),
                    **costs, delta_parcial_min=round(costs['parcial_chapas_min']-base['parcial_chapas_min'],2),
                    delta_parcial_max=round(costs['parcial_chapas_max']-base['parcial_chapas_max'],2),
                    custo_fita='', custo_total='',
                    demais_custos_desconhecidos='bloqueados; fundo; bordas alteradas; ferragens; consumiveis; frete; servicos',
                    interpretacao='delta apenas das chapas precificaveis; desconhecido nao e zero; propostas nao cumulativas'))
    return rows


def main():
    source = EXTERNAL/'Planos.json'
    if hashlib.sha256(source.read_bytes()).hexdigest() != PLAN_SHA:
        raise ValueError('Plano mudou: reconciliar antes de exportar')
    data = json.loads(source.read_text(encoding='utf-8'))
    outputs = {EXTERNAL/'Retalhos.csv':retalhos(data), OUT/'Custos_propostas.csv':propostas(data)}
    for path, rows in outputs.items():
        write(path, rows)
        print(path.name, len(rows), hashlib.sha256(path.read_bytes()).hexdigest())


if __name__ == '__main__': main()
