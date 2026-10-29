"""Sensibilidades acústicas condicionais; não prediz desempenho da unidade."""
import csv
import hashlib
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / '03_Ambientes/Acustica'
AREA = 30.8101  # Acabamentos/README.md, área nominal, não levantamento presencial


def base_homogenea(massa_superficial):
    """Bettarello et al., NZA 2012, p.21, eq.1; só base homogênea."""
    if not 100 <= massa_superficial <= 600:
        raise ValueError('Massa fora do domínio 100–600 kg/m²')
    return 164 - 35 * math.log10(massa_superficial)


def campo_livre(lp_referencia, distancia, distancia_referencia=1, perda=0):
    """OSHA OTM III.5; perda adicional é hipótese, não Rw de parede."""
    if distancia <= 0 or distancia_referencia <= 0 or perda < 0:
        raise ValueError('Distâncias positivas e perda não negativa necessárias')
    return lp_referencia - 20 * math.log10(distancia / distancia_referencia) - perda


def somar_niveis(niveis):
    if not niveis:
        raise ValueError('Não há fontes')
    return 10 * math.log10(sum(10 ** (nivel / 10) for nivel in niveis))


def gerar():
    rows = []
    for massa in (240, 360, 480):
        for delta in (0, 4, 10, 18):
            rows.append(dict(tipo='impacto_condicional', origem='H01/H02', receptor='laboratorio_hipotetico',
                             massa_kg_m2=massa, delta_total_db=delta, lp_ref_dba='', distancia_m='',
                             perda_adicional_db='', resultado_db=round(base_homogenea(massa)-delta, 3),
                             metrica='Lnw_eq_menos_delta_H; nao Lntw',
                             limite='sem laje ou sistema ensaiado; sem classificacao normativa'))
    # Os valores LG são Lp de catálogo; H03 os coloca em r0=1 m APENAS para sensibilidade.
    for modelo, velocidades in {'LG9':(38,28,22), 'LG12':(42,28,22), 'LG18':(45,38,32),
                                'depurador_H':(50,60,70)}.items():
        for modo, lp in zip(('H','L','SL') if modelo != 'depurador_H' else ('H50','H60','H70'), velocidades):
            for receptor in ('quarto_H', 'sala_H'):
                for distancia in (1,2,4):
                    for perda in (0,10,20):
                        rows.append(dict(tipo='aereo_condicional', origem=f'{modelo}/{modo}/H03/H04',
                                         receptor=receptor, massa_kg_m2='', delta_total_db='', lp_ref_dba=lp,
                                         distancia_m=distancia, perda_adicional_db=perda,
                                         resultado_db=round(campo_livre(lp,distancia,perda=perda),3),
                                         metrica='Lp_H_dBA', limite=('varredura arbitraria, nao tipica; ' if modelo=='depurador_H' else '') + 'sem posicao real; sem reverberacao ou fundo'))
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / 'Cenarios.csv'
    with path.open('w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file,fieldnames=rows[0].keys(),delimiter=';')
        writer.writeheader(); writer.writerows(rows)
    print(f'{len(rows)} cenários; SHA256 {hashlib.sha256(path.read_bytes()).hexdigest()}')
    print(f'Teto contábil acústica: {1500/AREA:.2f} R$/m², sem perdas ou instalação')


if __name__ == '__main__':
    gerar()
