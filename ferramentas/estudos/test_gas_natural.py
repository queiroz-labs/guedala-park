import math
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gas_natural as g


class TestDemanda(unittest.TestCase):
    def test_cooktop_soma_dos_queimadores(self):
        self.assertAlmostEqual(g.cooktop_kw(), 8.8, places=6)

    def test_fator_do_manual_do_e21(self):
        self.assertAlmostEqual(g.kw_para_m3h(33.7), 3.04, places=6)

    def test_total_maximo(self):
        s1 = g.cenarios_demanda()[0]
        self.assertAlmostEqual(s1["total_kW"], 42.5, places=1)
        self.assertAlmostEqual(s1["total_m3_h"], 3.834, places=2)

    def test_e21_satura_na_potencia_nominal(self):
        self.assertAlmostEqual(g.kw_e21(14, 30), g.E21_KW, places=6)
        self.assertLess(g.kw_e21(8, 25), g.E21_KW)

    def test_sem_vazao_sem_gas(self):
        self.assertEqual(g.kw_e21(0, 30), 0.0)


class TestRede(unittest.TestCase):
    def test_queda_cresce_com_comprimento_e_cai_com_diametro(self):
        q = 3.04
        a, _ = g.perda_de_carga(q, 5, 14, 0.0015)
        b, _ = g.perda_de_carga(q, 10, 14, 0.0015)
        c, _ = g.perda_de_carga(q, 10, 18, 0.0015)
        self.assertGreater(b, a)
        self.assertLess(c, b)
        self.assertAlmostEqual(b / a, 2.0, delta=0.05)

    def test_concorda_com_renouard(self):
        dp, _ = g.perda_de_carga(3.04, 10, 14, 0.0015)
        ref = g.renouard_mmca(3.04, 10, 14)
        self.assertAlmostEqual(dp / ref, 1.0, delta=0.25)

    def test_laminar_usa_64_sobre_re(self):
        self.assertAlmostEqual(g._f_colebrook(1000, 1e-4), 0.064, places=6)

    def test_velocidade_conserva_massa(self):
        _, v = g.perda_de_carga(3.04, 5, 14, 0.0015)
        area = math.pi * 0.014 ** 2 / 4
        rho = g.D_REL * g.RHO_AR_KG_M3 * (g.P_ATM_PA + 200 * g.MMCA_PA) / g.P_ATM_PA
        self.assertAlmostEqual(v * area * rho, 3.04 / 3600 * g.D_REL * g.RHO_AR_KG_M3, delta=1e-9)

    def test_menor_diametro_nao_diminui_com_o_comprimento(self):
        rede = g.tabela_rede()
        ids = [g.menor_di(rede, "ramal E21", "cobre", c) for c in (3, 5, 8, 12, 18)]
        self.assertEqual(ids, sorted(ids))
        self.assertTrue(all(i is not None for i in ids))


class TestVentilacao(unittest.TestCase):
    def setUp(self):
        self.v = {l["item"]: l["valor"] for l in g.tabela_ventilacao()}

    def test_abertura_minima_do_manual(self):
        self.assertAlmostEqual(self.v["secao_chamine_cm2"], 28.3, places=1)
        self.assertEqual(self.v["abertura_permanente_minima_cm2"], 100.0)

    def test_isencao_de_ventilacao_nao_se_aplica(self):
        self.assertAlmostEqual(self.v["volume_para_dispensar_ventilacao_m3"], 382.5, places=1)
        self.assertLess(self.v["volume_unidade_bruto_m3"], self.v["volume_para_dispensar_ventilacao_m3"])

    def test_volume_minimo_do_e21(self):
        self.assertLess(self.v["volume_area_servico_nominal_m3"], self.v["volume_minimo_E21_m3"])
        self.assertGreater(self.v["volume_cozinha_mais_AS_m3"], self.v["volume_minimo_E21_m3"])

    def test_mais_excesso_de_ar_pede_mais_area(self):
        a = self.v["area_livre_para_1ms_lambda_1.2_cm2"]
        b = self.v["area_livre_para_1ms_lambda_2.0_cm2"]
        self.assertGreater(b, a)


class TestCombustao(unittest.TestCase):
    def test_estequiometria_do_metano(self):
        _, p = g.combustao_cooktop()
        self.assertAlmostEqual(p["kg_CO2_por_m3_gas"], 1.83, delta=0.02)
        self.assertAlmostEqual(p["kg_H2O_por_m3_gas"], 1.50, delta=0.02)

    def test_sem_trocas_de_ar_o_limite_e_gerado_sobre_volume(self):
        linhas, p = g.combustao_cooktop()
        pequena = next(l for l in linhas if l["trocas_ar_h"] == 0.5 and l["minutos"] == 30 and l["volume"] == "cozinha+AS")
        sem_vent = 1e6 * p["gas_4kW_m3_h"] * 0.5 / pequena["volume_m3"]
        self.assertLess(pequena["CO2_acima_do_externo_ppm"], sem_vent)

    def test_mais_trocas_de_ar_menos_co2(self):
        linhas, _ = g.combustao_cooktop()
        sel = [l for l in linhas if l["volume"] == "unidade inteira" and l["minutos"] == 60]
        vals = [l["CO2_acima_do_externo_ppm"] for l in sorted(sel, key=lambda l: l["trocas_ar_h"])]
        self.assertEqual(vals, sorted(vals, reverse=True))

    def test_psicrometria_ponto_de_orvalho(self):
        w = g.razao_mistura(22.0, 100.0)
        self.assertAlmostEqual(g.ur_com_razao(22.0, w), 100.0, places=6)


class TestSaida(unittest.TestCase):
    def test_gerar_escreve_somente_na_pasta_pedida(self):
        with tempfile.TemporaryDirectory() as d:
            g.gerar(d)
            nomes = sorted(p.name for p in Path(d).iterdir())
        self.assertEqual(nomes, ["Combustao_cooktop.csv", "Demanda.csv", "Dimensionamento_rede.csv", "Ventilacao_e_ar.csv"])


if __name__ == "__main__":
    unittest.main()
