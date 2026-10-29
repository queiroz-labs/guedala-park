import unittest
from quadro_cargas_minimos import union_geometry, minimum_points, lighting_va, socket_va


class MinimosTest(unittest.TestCase):
    def test_rectangle(self):
        self.assertEqual(union_geometry([(0,0,200,300)]),(6,10))

    def test_overlap_and_internal_edge(self):
        self.assertEqual(union_geometry([(0,0,200,100),(100,0,300,100)]),(3,8))

    def test_cut_changes_boundary(self):
        self.assertEqual(union_geometry([(0,0,200,200)],[(100,0,200,100)]),(3,8))

    def test_lighting_whole_increments(self):
        self.assertEqual([lighting_va(a) for a in [6,6.01,9.999,10,14]],[100,100,100,160,220])

    def test_points_fraction_not_round(self):
        self.assertEqual(minimum_points('molhado',5,7),2)
        self.assertEqual(minimum_points('molhado',5,7.001),3)
        self.assertEqual(minimum_points('sala_dormitorio',8,10.5),3)
        self.assertEqual(minimum_points('outro',.945,3.9),1)
        self.assertEqual(minimum_points('banheiro',2.66,6.86),1)

    def test_va_not_watts(self):
        self.assertEqual(socket_va(4,True),1900)
        self.assertEqual(socket_va(4,True,True),1400)
        self.assertEqual(socket_va(3,False),300)

    def test_invalid_geometry(self):
        with self.assertRaises(ValueError): minimum_points('outro',0,1)
        with self.assertRaises(ValueError): lighting_va(0)


if __name__ == '__main__': unittest.main()
