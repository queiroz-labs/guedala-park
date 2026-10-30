"""Gás natural: demanda, perda de carga, ventilação e subprodutos da combustão.

Aparelhos: Rinnai E21 REU-E211 FEH GN e cooktop Electrolux KE4GC. Dados dos
manuais em 09_Referencias/Plantas_e_manuais/Manuais. Resultados são triagem
nominal: nenhum comprimento, diâmetro ou posição de tubulação do final 06 foi
levantado. Uso:  python -B ferramentas/estudos/gas_natural.py
"""
import argparse
import csv
import math
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
SAIDA_PADRAO = RAIZ / "03_Ambientes" / "Gas_natural"

# Manual Rinnai E21 (tabela de características, REU-E211 FEH GN)
E21_KW = 33.7
E21_M3H = 3.04
E21_RENDIMENTO = 0.86
E21_PRESSAO_MMCA = 200.0
E21_TOLERANCIA = 0.25
E21_CHAMINE_MM = 60.0
E21_VENT_MIN_CM2 = 100.0
E21_VOLUME_MIN_M3 = 6.0
ISENCAO_M3_POR_KW = 9.0
# Manual Electrolux KE4GC: 1 especial 2800 W + 3 semirrápidos de 2000 W, GN 1,96 kPa
COOKTOP_QUEIMADORES_W = [2800.0, 2000.0, 2000.0, 2000.0]
COOKTOP_PRESSAO_MMCA = 1960.0 / 9.80665
KW_POR_M3H = E21_KW / E21_M3H

# Propriedades do gás: densidade relativa coincide nas fontes consultadas; o resto é hipótese
D_REL = 0.60
RHO_AR_KG_M3 = 1.204
MU_PA_S = 1.1e-5
P_ATM_PA = 101325.0
MMCA_PA = 9.80665
RUGOSIDADE_MM = {"cobre": 0.0015, "multicamada": 0.007, "aco": 0.045}
FATOR_CONEXOES = 1.3

# Critérios de perda de carga (fontes secundárias, ver README)
LIMITE_DP_MMCA = 20.0
LIMITE_V_2012_MS = 20.0
LIMITE_V_2021_MS = 6.0

# Geometria nominal (Dados_das_medidas_R00.json e planta oficial); altura nominal 2,60 m
ALTURA_M = 2.60
AREA_COZINHA_M2 = 3.52 * 1.55
AREA_AS_M2 = 1.29 * 1.54
AREA_SALA_M2 = 9.6715
AREA_UNIDADE_M2 = 40.18

AR_ESTEQUIOMETRICO = 9.52  # m3 de ar por m3 de CH4 (2 O2 x 4,76)
MOL_POR_M3_20C = P_ATM_PA / (8.314462 * 293.15)
M_CO2_KG_MOL = 0.04401
M_H2O_KG_MOL = 0.018015


def cooktop_kw():
    return sum(COOKTOP_QUEIMADORES_W) / 1000.0


def kw_para_m3h(kw):
    return kw / KW_POR_M3H


def kw_e21(vazao_lmin, delta_t_k):
    """Entrada de gás do E21 para uma vazão e elevação de temperatura (satura em 33,7 kW)."""
    saida_kw = vazao_lmin / 60.0 * 0.998 * 4.186 * delta_t_k
    return min(saida_kw / E21_RENDIMENTO, E21_KW)


def cenarios_demanda():
    cook = cooktop_kw()
    casos = [
        ("S1", "Tudo no máximo: E21 a 100% + 4 queimadores", E21_KW, cook),
        ("S2", "Inverno: chuveiro 14 L/min, 15→45 °C (E21 satura) + 2 semirrápidos", kw_e21(14, 30), 4.0),
        ("S3", "Chuveiro 8 L/min, 15→40 °C + 1 semirrápido", kw_e21(8, 25), 2.0),
        ("S4", "Só E21 no máximo", E21_KW, 0.0),
        ("S5", "Só cooktop, 4 queimadores", 0.0, cook),
    ]
    linhas = []
    for cod, desc, ke, kc in casos:
        total = ke + kc
        linhas.append({
            "cenario": cod, "descricao": desc, "E21_kW": round(ke, 2), "cooktop_kW": round(kc, 2),
            "total_kW": round(total, 2), "total_m3_h": round(kw_para_m3h(total), 3),
            "total_kcal_h": round(total * 859.845),
        })
    return linhas


def _f_colebrook(re, rug_rel):
    if re < 2300:
        return 64.0 / re
    f = 0.25 / math.log10(rug_rel / 3.7 + 5.74 / re ** 0.9) ** 2
    for _ in range(60):
        novo = 1.0 / (-2.0 * math.log10(rug_rel / 3.7 + 2.51 / (re * math.sqrt(f)))) ** 2
        if abs(novo - f) < 1e-12:
            break
        f = novo
    return f


def perda_de_carga(q_m3h, comprimento_m, di_mm, rugosidade_mm, p_rel_mmca=E21_PRESSAO_MMCA):
    """Darcy–Weisbach + Colebrook. Devolve (queda em mmca, velocidade em m/s)."""
    d = di_mm / 1000.0
    p_abs = P_ATM_PA + p_rel_mmca * MMCA_PA
    rho_n = D_REL * RHO_AR_KG_M3
    rho = rho_n * p_abs / P_ATM_PA
    massa = q_m3h / 3600.0 * rho_n
    area = math.pi * d * d / 4.0
    v = massa / rho / area
    re = rho * v * d / MU_PA_S
    f = _f_colebrook(re, rugosidade_mm / di_mm)
    dp = f * comprimento_m / d * rho * v * v / 2.0
    return dp / MMCA_PA, v


def renouard_mmca(q_m3h, comprimento_m, di_mm):
    """Renouard linear (baixa pressão), usado só como conferência independente."""
    return 232000.0 * D_REL * comprimento_m * q_m3h ** 1.82 / di_mm ** 4.82


def tabela_rede():
    fluxos = [
        ("tronco S1", kw_para_m3h(E21_KW + cooktop_kw())),
        ("ramal E21", kw_para_m3h(E21_KW)),
        ("ramal cooktop", kw_para_m3h(cooktop_kw())),
    ]
    dis = [10, 12, 14, 16, 18, 20, 22, 25]
    comprimentos = [3, 5, 8, 12, 18]
    linhas = []
    for trecho, q in fluxos:
        for material, rug in RUGOSIDADE_MM.items():
            for comp in comprimentos:
                leq = comp * FATOR_CONEXOES
                for di in dis:
                    dp, v = perda_de_carga(q, leq, di, rug)
                    linhas.append({
                        "trecho": trecho, "vazao_m3_h": round(q, 3), "material": material,
                        "L_real_m": comp, "L_equiv_m": round(leq, 1), "DI_mm": di,
                        "queda_mmca": round(dp, 2), "velocidade_m_s": round(v, 2),
                        "ok_20mmca": dp <= LIMITE_DP_MMCA,
                        "ok_50mmca_fabricante": dp <= E21_PRESSAO_MMCA * E21_TOLERANCIA,
                        "ok_v20": v <= LIMITE_V_2012_MS, "ok_v6": v <= LIMITE_V_2021_MS,
                    })
    return linhas


def menor_di(linhas, trecho, material, comp, criterio="ok_20mmca", com_v6=False):
    cand = [l for l in linhas if l["trecho"] == trecho and l["material"] == material
            and l["L_real_m"] == comp and l[criterio] and (l["ok_v6"] or not com_v6)]
    return min((l["DI_mm"] for l in cand), default=None)


def tabela_ventilacao():
    secao_chamine = math.pi * (E21_CHAMINE_MM / 10.0) ** 2 / 4.0
    area_min = max(E21_VENT_MIN_CM2, secao_chamine)
    soma_kw = E21_KW + cooktop_kw()
    vol_coz = AREA_COZINHA_M2 * ALTURA_M
    vol_as = AREA_AS_M2 * ALTURA_M
    linhas = [
        ("secao_chamine_cm2", round(secao_chamine, 1), "π·(6 cm)²/4; manual E21 item 3x"),
        ("abertura_permanente_minima_cm2", round(area_min, 1), "maior entre 100 cm² e a seção da chaminé; manual E21 item 3x"),
        ("soma_potencias_kW", round(soma_kw, 1), "E21 + 4 queimadores"),
        ("volume_para_dispensar_ventilacao_m3", round(ISENCAO_M3_POR_KW * soma_kw, 1), "9 m³/kW da soma; manual E21 item 3x"),
        ("volume_cozinha_nominal_m3", round(vol_coz, 1), "3,52 × 1,55 × 2,60 (cotas oficiais, nominal)"),
        ("volume_area_servico_nominal_m3", round(vol_as, 1), "1,29 × 1,54 × 2,60 (cotas oficiais, nominal)"),
        ("volume_cozinha_mais_AS_m3", round(vol_coz + vol_as, 1), "sem parede entre as duas: não confirmado"),
        ("volume_unidade_bruto_m3", round(AREA_UNIDADE_M2 * ALTURA_M, 1), "40,18 m² × 2,60, inclui paredes"),
        ("volume_minimo_E21_m3", E21_VOLUME_MIN_M3, "manual E21, figura 2"),
    ]
    for lam in (1.2, 1.5, 2.0):
        ar_e21 = kw_para_m3h(E21_KW) * AR_ESTEQUIOMETRICO * lam
        ar_cook = kw_para_m3h(cooktop_kw()) * AR_ESTEQUIOMETRICO * lam
        tot = ar_e21 + ar_cook
        area_1ms = tot / 3600.0 / 1.0 * 1e4
        linhas.append((f"ar_de_combustao_lambda_{lam}_m3_h", round(tot, 1),
                       f"E21 {ar_e21:.1f} + cooktop {ar_cook:.1f}; excesso de ar λ={lam} é hipótese"))
        linhas.append((f"area_livre_para_1ms_lambda_{lam}_cm2", round(area_1ms), "verificação informativa, não é exigência do manual"))
    return [{"item": a, "valor": b, "base": c} for a, b, c in linhas]


def magnus_ps_hpa(t_c):
    return 6.112 * math.exp(17.62 * t_c / (243.12 + t_c))


def razao_mistura(t_c, ur_pct, p_hpa=930.0):
    pv = ur_pct / 100.0 * magnus_ps_hpa(t_c)
    return 622.0 * pv / (p_hpa - pv)


def ur_com_razao(t_c, w_g_kg, p_hpa=930.0):
    pv = w_g_kg * p_hpa / (622.0 + w_g_kg)
    return 100.0 * pv / magnus_ps_hpa(t_c)


def combustao_cooktop():
    kg_co2_m3 = MOL_POR_M3_20C * M_CO2_KG_MOL
    kg_h2o_m3 = 2 * MOL_POR_M3_20C * M_H2O_KG_MOL
    gas_m3h = kw_para_m3h(4.0)
    linhas = []
    volumes = [("cozinha+AS", (AREA_COZINHA_M2 + AREA_AS_M2) * ALTURA_M),
               ("cozinha+AS+sala", (AREA_COZINHA_M2 + AREA_AS_M2 + AREA_SALA_M2) * ALTURA_M),
               ("unidade inteira", AREA_UNIDADE_M2 * ALTURA_M)]
    for nome, vol in volumes:
        for ach in (0.5, 2.0, 5.0):
            for minutos in (30, 60):
                t = minutos / 60.0
                co2_ppm = 1e6 * gas_m3h / (ach * vol) * (1 - math.exp(-ach * t))
                agua_kg = gas_m3h * t * kg_h2o_m3
                massa_ar = vol * 1.15
                w_add = agua_kg / massa_ar * 1000.0
                w0 = razao_mistura(22.0, 60.0)
                ur_fim = ur_com_razao(22.0, w0 + w_add)
                linhas.append({
                    "volume": nome, "volume_m3": round(vol, 1), "trocas_ar_h": ach, "minutos": minutos,
                    "CO2_acima_do_externo_ppm": round(co2_ppm), "agua_gerada_kg": round(agua_kg, 2),
                    "umidade_sem_ventilacao_g_kg": round(w_add, 1),
                    "UR_final_a_22C_sem_remocao_pct": round(min(ur_fim, 100.0)),
                    "passa_da_saturacao": ur_fim > 100.0,
                })
    return linhas, {"kg_CO2_por_m3_gas": kg_co2_m3, "kg_H2O_por_m3_gas": kg_h2o_m3, "gas_4kW_m3_h": gas_m3h}


def vazao_exaustao():
    vol_coz = AREA_COZINHA_M2 * ALTURA_M
    vol_ab = (AREA_COZINHA_M2 + AREA_AS_M2) * ALTURA_M
    return [{"base": nome, "volume_m3": round(v, 1), "trocas_10_m3_h": round(10 * v), "trocas_12_m3_h": round(12 * v)}
            for nome, v in (("cozinha", vol_coz), ("cozinha + AS", vol_ab))]


def escrever_csv(caminho, linhas):
    caminho.parent.mkdir(parents=True, exist_ok=True)
    with open(caminho, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0].keys()), delimiter=";")
        w.writeheader()
        w.writerows(linhas)


def gerar(saida):
    saida = Path(saida)
    demanda = cenarios_demanda()
    rede = tabela_rede()
    ventil = tabela_ventilacao()
    comb, props = combustao_cooktop()
    escrever_csv(saida / "Demanda.csv", demanda)
    escrever_csv(saida / "Dimensionamento_rede.csv", rede)
    escrever_csv(saida / "Ventilacao_e_ar.csv", ventil)
    escrever_csv(saida / "Combustao_cooktop.csv", comb)
    return demanda, rede, ventil, comb, props


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--saida", default=str(SAIDA_PADRAO))
    args = ap.parse_args()
    demanda, rede, ventil, comb, props = gerar(args.saida)
    print(f"fator kW por m3/h: {KW_POR_M3H:.4f}; cooktop {cooktop_kw():.1f} kW")
    for l in demanda:
        print(l["cenario"], l["total_kW"], "kW", l["total_m3_h"], "m3/h")
    for comp in (3, 5, 8, 12, 18):
        print(f"L={comp} m menor DI (ate 20 mmca): tronco",
              menor_di(rede, "tronco S1", "cobre", comp), "E21", menor_di(rede, "ramal E21", "cobre", comp),
              "cooktop", menor_di(rede, "ramal cooktop", "cobre", comp))
    print(props)


if __name__ == "__main__":
    main()
