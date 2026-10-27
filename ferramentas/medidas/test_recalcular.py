"""Reprodução independente da R53, entradas adversas e integração das pranchas."""
import copy
import csv
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True
from recalcular import ROOT, avaliar, base, calcular, entradas, saida_segura
from medidas import resolver


class Dependencias(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = base()
        cls.nominal = entradas(nominal=True)

    def test_reproducao_todas_as_cotas_e_formulas(self):
        geo = json.loads((ROOT/self.doc['exportacao']).read_text(encoding='utf-8'))
        objects = {o['id']:o for o in geo['objects']}
        mirror = resolver(self.nominal, 'PR-EIXO-X').mm
        report = calcular(self.nominal, self.doc)
        self.assertEqual(len(report['resultados']), 469)
        for rule, result in zip(self.doc['regras'], report['resultados']):
            with self.subTest(alvo=rule['movel'], cota=rule['cota']):
                # Não basta retornar a dimensão fixa: também testar a fórmula independente.
                value = avaliar(rule['formula'], self.nominal, rule['folgas'], rule['medidas'])
                self.assertAlmostEqual(value, rule['atual_mm'], places=6)
                self.assertEqual(result['delta_mm'], 0)
                name = rule['movel']
                b = (geo['modules'][name] if name in geo['modules'] else objects[name])['box']
                b = [mirror-b[3], b[1], b[2], mirror-b[0], b[4], b[5]]
                self.assertEqual(b, self.doc['alvos'][name]['box_planta'])
                if 'eixo' in rule:
                    a = rule['eixo']
                    self.assertAlmostEqual(result['depois_mm'], b[a+3]-b[a])
                elif rule.get('representacao') == 'fechamento':
                    self.assertAlmostEqual(value, resolver(self.nominal, rule['medidas'][0]).mm-b[5])
                elif 'referencia' in rule['folgas']:
                    axis = 0 if rule['cota'].endswith('_x') else 1 if rule['cota'].endswith('_y') else 2
                    self.assertAlmostEqual(rule['folgas']['referencia'], b[axis])

    def test_fixo_muda_folga_e_detecta_nao_cabe(self):
        rows = copy.deepcopy(self.nominal)
        rows['PD-QUA']['valor_medido'] = '2400 mm'
        results = calcular(rows, self.doc)['resultados']
        height = next(r for r in results if (r['movel'],r['cota']) == ('P03','altura'))
        self.assertEqual(height['delta_mm'], 0)
        self.assertEqual(height['status'], 'NÃO CABE')
        self.assertEqual(height['folgas_mm']['topo'], -40)
        closure = next(r for r in results if (r['movel'],r['cota']) == ('P03','fechamento_teto'))
        self.assertEqual(closure['delta_mm'], -200)

    def test_segue_parede_muda_envelope_sem_esticar_paineis(self):
        doc = copy.deepcopy(self.doc)
        rule = next(r for r in doc['regras'] if (r['movel'],r['cota']) == ('P03','altura'))
        rule['modo'] = 'segue_parede'  # Exclusivo do teste, não decisão do projeto.
        rule['limites']['min'] = 200
        rows = copy.deepcopy(self.nominal)
        rows['PD-QUA']['valor_medido'] = '2470 mm'
        report = calcular(rows, doc)
        height = next(r for r in report['resultados'] if (r['movel'],r['cota']) == ('P03','altura'))
        self.assertEqual(height['depois_mm'], 178)
        self.assertEqual(height['status'], 'fora do limite')
        self.assertEqual(report['envelopes']['P03'][5], 2310)

    def test_prumo_afeta_encaixe(self):
        rows = copy.deepcopy(self.nominal)
        rows['DEP-COZ-PRUMO']['valor_medido'] = '12 mm'
        r = next(r for r in calcular(rows,self.doc)['resultados'] if (r['movel'],r['cota']) == ('P05','extensao_y'))
        self.assertEqual(r['status'], 'NÃO CABE')
        self.assertEqual(r['folgas_mm']['fim'], -12)

    def test_rejeita_codigo_duplicado_unidade_e_expressao(self):
        with tempfile.TemporaryDirectory(prefix='gp-medidas-test-') as tmp:
            path = Path(tmp)/'cenario.csv'
            for text in ['codigo_medida,valor_medido\nDESCONHECIDO,10 mm\n',
                         'codigo_medida,valor_medido\nPD-QUA,2470 mm\nPD-QUA,2470 mm\n',
                         'codigo_medida,valor_medido\nPD-QUA,2470\n',
                         'codigo_medida,valor_medido\nPD-QUA,\n']:
                path.write_text(text,encoding='utf-8')
                with self.assertRaises(ValueError): entradas(cenario=path)
        for formula in ['__import__("os")', 'm("PD-QUA").real', '1 / 0', 'm("PD-ESC")']:
            with self.assertRaises(ValueError): avaliar(formula,self.nominal,{},['PD-QUA'])
        with self.assertRaises(ValueError): saida_segura(ROOT/'06_Entregas')

    def test_cenario_pranchas_isolado_e_precedencia(self):
        from gerar import Projeto
        with tempfile.TemporaryDirectory(prefix='gp-medidas-test-') as tmp:
            path = Path(tmp)/'cenario.csv'
            path.write_text('codigo_medida,valor_medido\nPD-QUA,2.47 m\nDIM-01,2468 x 2950 mm\nPR-PONTO-C05-X,4780 mm\n',encoding='utf-8')
            p = Projeto(path)
            self.assertEqual(p.pe('quarto').mm,2470)
            self.assertEqual(p.modules['P03']['box'],self.doc['alvos']['P03']['box_planta'])
            self.assertEqual(p.m('DIM-01/0').mm,2468)
            r = next(r for r in p.recalculo['resultados'] if (r['movel'],r['cota']) == ('P05','ponto_C05_x'))
            self.assertEqual(r['delta_mm'],80)
            self.assertEqual(p.m('PR-PONTO-C05-X').mm,4780)
        self.assertEqual(entradas(nominal=True), self.nominal)

    def test_nao_transformar_vazio_em_zero(self):
        rows = copy.deepcopy(self.nominal)
        rows['PD-QUA']['valor_nominal_atual'] = ''
        with self.assertRaises(ValueError): calcular(rows,self.doc)
        rows['PD-QUA']['valor_medido'] = '-1 mm'
        with self.assertRaises(ValueError): calcular(rows,self.doc)


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Dependencias)
    result = unittest.TextTestRunner().run(suite)
    print('Reprodução R53: 469 regras, diferença 0 mm; entradas e integração OK' if result.wasSuccessful() else 'ERRO: dependências dimensionais')
    raise SystemExit(0 if result.wasSuccessful() else 1)
