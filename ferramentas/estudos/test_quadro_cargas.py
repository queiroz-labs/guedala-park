import unittest
from quadro_cargas import current, voltage_drop, build_loads, aggregate, read_csv, AREA, LIGHT


class QuadroCargasTest(unittest.TestCase):
    def test_missing_is_not_zero(self):
        self.assertIsNone(current(None))
        self.assertEqual(current(0), 0)

    def test_fp_and_voltage(self):
        self.assertAlmostEqual(current(1270, pf=.8), 12.5)
        for v, pf in [(0, 1), (127, 0), (127, 1.1)]:
            with self.assertRaises(ValueError): current(100, v, pf)

    def test_voltage_drop_needs_actual_route(self):
        self.assertIsNone(voltage_drop(10, None, 8, .1, .9))
        self.assertAlmostEqual(voltage_drop(10, 20, 8, 0, 1), 3.2)

    def test_unique_and_current_equipment(self):
        rows = build_loads(read_csv(AREA / 'Cargas_entradas.csv'), read_csv(LIGHT))
        self.assertEqual(sum(r['id'] == 'EQ23' for r in rows), 1)
        self.assertEqual(sum(r['id'].startswith('LUZ-') for r in rows), 15)
        self.assertEqual(next(r['potencia_W'] for r in rows if r['id'] == 'EQ07'), '1650')
        self.assertEqual(next(r['potencia_W'] for r in rows if r['id'] == 'EQ24'), '')
        self.assertFalse(any('F80N' in r['item'] for r in rows))

    def test_duplicate_rejected(self):
        rows = read_csv(AREA / 'Cargas_entradas.csv')
        with self.assertRaises(ValueError): build_loads(rows + [rows[0]], [])

    def test_no_dimensioning_from_partial_power(self):
        rows = build_loads(read_csv(AREA / 'Cargas_entradas.csv'), read_csv(LIGHT))
        circuits = aggregate(rows)
        self.assertTrue(all(c['Ib_dimensionante_A'] == '' and c['secao_final_mm2'] == '' and c['queda_V'] == '' for c in circuits))
        self.assertGreater(sum(c['cargas_sem_potencia'] for c in circuits), 0)

    def test_lighting_not_doubled(self):
        rows = build_loads([], read_csv(LIGHT))
        self.assertAlmostEqual(sum(float(r['potencia_W']) for r in rows), 264.2)


if __name__ == '__main__':
    unittest.main()
