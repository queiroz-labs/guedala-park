"""Sensibilidade financeira das chapas; preços históricos, lacunas nunca zeradas."""
import csv
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'04_Moveis/Plano_de_corte'
OLD='05_Orcamento_e_cronograma/Orcamento/Marcenaria_35mil/Revisao_materiais_2026-10-23.md'
BOOK='01_Programa_e_decisoes/Caderno_de_especificacoes.md; consulta 27/10/2026'
# Limites superiores declarados como provisão, salvo Azul (duas referências).
PRICES={('Arenza',18):(435.58,520,'referencia/provisao',OLD),
        ('Azul Petroleo',18):(526,618.67,'referencias historicas',OLD),
        ('Branco TX',18):(365.11,400,'referencia/provisao',OLD),
        ('Branco TX',15):(282.67,330,'referencia/provisao',OLD),
        ('Beige Matt',18):(500,650,'provisao sem SKU',OLD)}
OPTIONS={'Lume':589.47,'Areia':643.98,'Nuvem':607.15}


def read(path,delimiter=';'):
    with path.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=delimiter))


def write(path,rows):
    with path.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter=';');w.writeheader();w.writerows(rows)


def price(pattern,thickness,option):
    if pattern=='Off-white fosco' and thickness==18:
        return OPTIONS[option],OPTIONS[option],'opcao de amostra, nao escolhida',BOOK
    return PRICES.get((pattern,thickness),(None,None,'preco compativel ausente','cotacao necessaria'))


def rolls(meters,length=50):
    return math.ceil(meters/length-1e-10)


def main():
    source=read(OUT/'Resumo_chapas.csv')
    base=[r for r in source if r['variante']=='base' and r['formato_mm']=='2750x1850']
    if not base:raise ValueError('Base 2750x1850 ausente')
    lines=[];summary=[]
    tapes=read(ROOT/'04_Moveis/Furacao/Fita_por_cor.csv')
    tape_rows=[]
    for r in tapes:
        m=float(r['metros_propostos_com_perda']);n=rolls(m)
        tape_rows.append(dict(cor=r['cor'],espessura_fita_mm=r['espessura_fita_mm'],
            metros_com_perda=m,rolos50_HF=n,custo_HF_baixo=round(n*28,2),custo_HF_alto=round(n*58,2),
            premissa='HF: uma largura por grupo, rolo50m R$28-58 generico; nao cotacao dos SKUs/cores/espessuras',
            fonte=OLD,pendencia='largura/SKU/preco e 23 paineis sem regra; colagem excluida'))
    flo=sum(r['custo_HF_baixo'] for r in tape_rows);fhi=sum(r['custo_HF_alto'] for r in tape_rows)
    for scenario in sorted({r['cenario'] for r in base}):
        for option in OPTIONS:
            lo=hi=0;unknown=[];count=0
            for r in (r for r in base if r['cenario']==scenario):
                n=int(r['chapas_subconjunto']);t=float(r['espessura_mm']);pattern=r['padrao']
                low,high,kind,ref=price(pattern,t,option)
                count+=n
                if low is None:unknown.append(f'{pattern} {t:g} mm: {n} chapa(s)')
                else:lo+=n*low;hi+=n*high
                lines.append(dict(cenario=scenario,opcao_offwhite=option,padrao=pattern,espessura_mm=t,
                    chapas_subconjunto=n,preco_unit_baixo='' if low is None else low,
                    preco_unit_alto='' if high is None else high,
                    subtotal_baixo='' if low is None else round(n*low,2),
                    subtotal_alto='' if high is None else round(n*high,2),natureza=kind,fonte=ref,
                    limite='215 paineis cortaveis; P01 inteiro e 33 bloqueados fora; preco nao entregue/atualizado'))
            summary.append(dict(cenario=scenario,opcao_offwhite=option,chapas_subconjunto=count,
                subtotal_chapas_referencias_provisoes_baixo=round(lo,2),subtotal_chapas_referencias_provisoes_alto=round(hi,2),
                grupos_sem_preco=' | '.join(unknown),fita_HF_baixo=flo,fita_HF_alto=fhi,
                parcial_com_HF_baixo=round(lo+flo,2),parcial_com_HF_alto=round(hi+fhi,2),
                saldo_meta_material16mil_apos_parcial_baixo=round(16000-lo-flo,2),
                saldo_meta_material16mil_apos_parcial_alto=round(16000-hi-fhi,2),
                teto_material_com_ferragens_servicos_historicos=35000-9200-16500,
                custo_total_material='',custo_total_instalado='',
                conclusao='Depende de lacunas e cotacao integral; parciais nao demonstram meta35mil'))
    write(OUT/'Custos_chapas.csv',lines);write(OUT/'Fita_custo_hipotese.csv',tape_rows)
    write(OUT/'Custos_cenarios.csv',summary)
    print(f'{len(base)} grupos/cenarios; {len(summary)} comparacoes financeiras; fita HF {flo:.2f}–{fhi:.2f}')


if __name__=='__main__':main()
