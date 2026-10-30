"""Contraprovas de união, descontos e rendimento acabado, sem leitura do CAD nativo."""
import unittest
import quantitativos_acabamentos as q


class GeometryTests(unittest.TestCase):
    def test_overlap_not_counted_twice(self):
        self.assertEqual(q.union_area([(0,0,2,2),(1,0,3,2)]),6)

    def test_nested_and_disjoint(self):
        self.assertEqual(q.union_area([(0,0,3,3),(1,1,2,2),(5,0,6,1)]),10)

    def test_empty_and_reversed(self):
        self.assertEqual(q.union_area([]),0)
        self.assertEqual(q.union_area([(2,0,1,3)]),0)

    def test_opening_clipped_to_face(self):
        self.assertEqual(q.union_area([q.clip((0,0,2,2.6),(1,0,3,2.05))]),2.05)

    def test_disjoint_clip_has_zero_area(self):
        self.assertEqual(q.union_area([q.clip((0,0,1,1),(2,2,3,3))]),0)

    def test_finished_yield_not_multiplied_by_coats(self):
        self.assertEqual(q.liters_finished(150,150/18),18)
        self.assertAlmostEqual(q.liters_finished(150,150/18,.20),21.6)

    def test_invalid_yield(self):
        with self.assertRaises(ValueError): q.liters_finished(20,0)

    def test_actual_sources_balance_without_duplicate_floor(self):
        totals,faces,cabinets=q.calculate()
        self.assertAlmostEqual(sum(r['piso_sem_sobreposicao_H01_m2'] for r in totals),35.4583)
        self.assertTrue(cabinets)
        self.assertTrue(all(c['desconto_adotado_m2']==0 for c in cabinets))
        self.assertTrue(all(0<=f['ocultacao_envelopes_H03_m2']<=f['parede_liquida_m2']+1e-6 for f in faces))
        self.assertTrue(all(f['vaos_m2']<=f['parede_bruta_m2'] for f in faces))
        self.assertAlmostEqual(sum(r['piso_bruto_uniao_m2'] for r in totals)-35.4583,.4915)

    def test_floor_box_partition_conserved(self):
        totals,_,_=q.calculate()
        wet,_,_=q.finishing(totals)
        self.assertAlmostEqual(wet[0]['area_liquida_m2']+wet[1]['area_liquida_m2'],2.6616)

    def test_two_green_walls_keep_budget_hypothesis_separate(self):
        wet,_,_=q.finishing(q.calculate()[0])
        self.assertAlmostEqual(wet[5]['area_liquida_m2'],1.24*2.47+.8*2.47)
        self.assertIn('sem descontar',wet[5]['cenario'])
        self.assertIn('hipótese',wet[5]['cenario'])
        self.assertAlmostEqual(wet[8]['area_liquida_m2'],.8*2.47)
        self.assertAlmostEqual(wet[3]['area_liquida_m2']+wet[6]['area_liquida_m2'],5.95)


if __name__=='__main__': unittest.main()
