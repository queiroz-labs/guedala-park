"""Regressões de unidade, partilha de tubos, incerteza e cobertura do comparador."""
import math
import unittest
from agua_quente_banheiro import geometry, routes, volume, length, unique_length, turns, report, visual, OPTIONS


class WaterRoutes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.g = geometry()
        cls.r = routes(cls.g)

    def test_litres_and_seconds(self):
        self.assertAlmostEqual(volume(1, 16.2), 0.206119894, places=8)
        self.assertAlmostEqual(volume(1, 18), 0.254469005, places=8)
        self.assertAlmostEqual(volume(4.34, 16.2)*60/3.9, 13.7624668, places=6)

    def test_known_routes_and_shared_tee(self):
        # 1.35 subida + 0.99 horizontal + 2.00 descida.
        self.assertAlmostEqual(length(self.r['A1']['pia']), 4.34)
        # Ramal da ducha acrescenta 1.95, não todo o caminho S→ducha.
        self.assertAlmostEqual(unique_length(self.r['A1'].values()), 6.29)
        self.assertAlmostEqual(length(self.r['A3']['pia']), 1.64)
        self.assertAlmostEqual(length(self.r['B4']['ducha']), .67875)
        self.assertEqual(turns(self.r['A1']['pia']), 2)

    def test_union_partly_overlapping_and_reverse_segments(self):
        paths=[[(0,0,0),(2000,0,0)],[(3000,0,0),(1000,0,0)],[(2000,0,0),(2000,0,1000)]]
        self.assertEqual(unique_length(paths), 4)
        with self.assertRaises(ValueError):
            unique_length([[(0,0,0),(100,100,0)]])

    def test_uncertain_origin_sensitivity(self):
        higher=routes(self.g, source_z=1500)
        self.assertAlmostEqual(length(higher['A1']['pia'])-length(self.r['A1']['pia']), -.3)
        self.assertAlmostEqual(length(higher['A4']['pia'])-length(self.r['A4']['pia']), .3)

    def test_cabinet_and_real_tank_clearance_rejection(self):
        b=self.g['interior']
        self.assertEqual([b[i+3]-b[i] for i in range(3)], [564,382,509])
        self.assertGreater(355+2*250, b[3]-b[0])
        self.assertEqual(self.g['boxes']['BC43_Sifao'][2]-b[2],298)
        self.assertGreater(355,298)

    def test_all_options_and_no_false_zero_wait(self):
        self.assertEqual(set(self.r),set(o['id'] for o in OPTIONS))
        self.assertEqual(len(self.r),13)
        self.assertNotIn('pia',self.r['B4'])
        self.assertEqual(self.r['C3'],{})
        page=visual(self.g,self.r); md=report(self.g,self.r)
        self.assertEqual(page.count('<svg '),26)
        self.assertEqual(page.count('<article '),13)
        self.assertIn('não o tempo total desde o E21',md)
        self.assertIn('120 V',md)
        self.assertIn('NÃO demonstra espaço',md)
        self.assertLess(len(md.encode()),60*1024)
        self.assertLess(len(page.encode()),1024*1024)


if __name__=='__main__':
    unittest.main()
