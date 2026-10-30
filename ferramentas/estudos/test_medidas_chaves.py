"""FICTÍCIO: cenários sintéticos, sem medidas reais nem decisões de tolerância."""
from pathlib import Path
import tempfile
import unittest
import medidas_chaves as m


class Medidas(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows, cls.engine = m.catalog(), m.chain()

    def test_dentro_fora_tolerancia_e_zero(self):
        table = m.hypothesis()
        self.assertEqual(m.classify('DIM-01', [2451, 2950], [2450, 2950], table)[0], 'ok')
        self.assertEqual(m.classify('DIM-01', [2454, 2950], [2450, 2950], table)[0], 'atenção')
        self.assertEqual(m.classify('DIM-01', [2460, 2950], [2450, 2950], table)[0], 'revisar')
        self.assertEqual(m.classify('DIM-01', [2450, 2950], [2450, 2950], [])[0], 'sem tolerância')
        self.assertEqual(m.classify('CAMPO-COZ-PISO', [0], [0], table)[0], 'ok')

    def test_ausencia_nao_zero(self):
        row = self.rows['PD-QUA']
        self.assertIsNone(m.parse_measured(row, dict(valor_medido='', unidade='mm'), self.engine)[0])
        self.assertEqual(m.classify('PD-QUA', None, [2600], m.hypothesis())[0], 'sem medida')
        with self.assertRaises(ValueError):
            m.parse_measured(row, dict(valor_medido='0', unidade='mm'), self.engine)

    def test_unidade_errada_e_virgula_decimal(self):
        row = self.rows['PD-QUA']
        self.assertEqual(m.parse_measured(row, dict(valor_medido='2,599', unidade='m'), self.engine)[0], [2599])
        for text, unit in [('2,6', 'kg'), ('2600 mm', 'm'), ('NaN', 'mm')]:
            with self.assertRaises(ValueError):
                m.parse_measured(row, dict(valor_medido=text, unidade=unit), self.engine)

    def test_codigo_desconhecido_duplicado(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'Ficticio.csv'
            for data in [[dict(codigo_medida='INEXISTENTE', valor_medido='')],
                         [dict(codigo_medida='PD-QUA', valor_medido=''), dict(codigo_medida='PD-QUA', valor_medido='')]]:
                m.cot.write_csv(path, data, ['codigo_medida', 'valor_medido'])
                with self.assertRaises(ValueError):
                    m.read_input(path, self.rows, self.engine)

    def scenario(self):
        return m.read_input(Path(__file__).parent / 'testes/Medidas_ficticias.csv', self.rows, self.engine)

    def test_lavanderia_box_propagacao_sem_redimensionar(self):
        result, geometry, _ = m.impacts(self.rows, self.scenario(), m.hypothesis(), self.engine)
        index = {r['codigo_medida']: r for r in result}
        self.assertEqual(index['DIM-06']['delta'], [0, 70])
        self.assertEqual(index['DIM-06']['classificacao'], 'revisar')
        self.assertEqual(index['BOX-VERDE']['delta'], [440, 220])
        self.assertEqual(index['BOX-VERDE']['classificacao'], 'revisar')
        self.assertIn('P01', index['PD-QUA']['moveis'])
        self.assertIn('P01.html', index['PD-QUA']['fichas'])
        self.assertEqual(index['PD-COZ']['classificacao'], 'sem medida')
        height = next(r for r in geometry if r['movel'] == 'P01' and r['cota'] == 'altura')
        self.assertEqual(height['depois_mm'], height['antes_mm'])
        self.assertEqual(height['folgas_mm']['topo'], 466)

    def test_modelo_na_ordem_dos_15_e_mapa_cotacao(self):
        ranking = m.cot.read_csv(m.ROOT / (m.DEPS + 'Ranking_15.csv'))
        self.assertEqual(list(self.rows)[:15], [r['codigo_medida'] for r in ranking])
        deps = m.quote_dependencies(self.rows, self.engine.document())
        self.assertTrue(any(r['linha'] == 'L079' and r['codigo_medida'] == 'PD-QUA' and 'P01' in r['moveis'] for r in deps))
        self.assertTrue(any(r['linha'] == 'L001' and 'P01' in r['moveis'] for r in deps))

    def test_tabela_propria_sem_fallback_e_unidade(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'Ficticio.csv'
            rows = [dict(codigo_medida='PD-QUA', unidade='mm', ok_ate='1', atencao_ate='3', natureza='FICTÍCIO', fonte='FICTÍCIO', quem_confirma='FICTÍCIO')]
            m.cot.write_csv(path, rows, list(rows[0]))
            table = m.thresholds(path, 'hipotese')
            self.assertEqual(m.classify('PD-COZ', [2600], [2600], table)[0], 'sem tolerância')
            rows[0]['unidade'] = 'grau'
            m.cot.write_csv(path, rows, list(rows[0]))
            with self.assertRaises(ValueError):
                m.impacts(self.rows, {}, m.thresholds(path, 'hipotese'), self.engine)

    def test_coordenada_sem_datum_nao_vira_ok(self):
        code = 'PR-PONTO-C05-X'
        raw = dict(valor_medido=self.rows[code]['valor_nominal_atual'], unidade='mm')
        vals, norm = m.parse_measured(self.rows[code], raw, self.engine)
        reading = {code: dict(valores=vals, normalizado=norm, data_hora='', evidencia='FICTÍCIO', obs='FICTÍCIO')}
        result, _, _ = m.impacts(self.rows, reading, m.hypothesis(), self.engine)
        self.assertNotEqual(next(r for r in result if r['codigo_medida'] == code)['classificacao'], 'ok')


if __name__ == '__main__':
    unittest.main()
