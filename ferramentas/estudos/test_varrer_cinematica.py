import unittest
import numpy as np
from varrer_cinematica import transformed_box, distances
from resumir_articulacoes import native_pairs


class BoundingBoxes(unittest.TestCase):
    def test_rotation_encloses_corners(self):
        m=np.eye(4);m[:2,:2]=[[0,-1],[1,0]];m[:3,3]=[10,20,30]
        np.testing.assert_allclose(transformed_box([0,0,0,2,3,4],m),[7,20,30,10,22,34])

    def test_distance_is_lower_bound_and_not_penetration(self):
        a=np.array([[0,0,0,1,1,1]])
        b=np.array([[4,5,1,5,6,2],[.5,.5,.5,2,2,2]])
        np.testing.assert_allclose(distances(a,b),[[5,0]])

    def test_independent_simultaneous_states(self):
        a=np.array([[0,0,0,1,1,1],[4,0,0,5,1,1]])
        b=np.array([[8,0,0,9,1,1],[4.5,0,0,5.5,1,1]])
        d=distances(a,b)
        self.assertEqual(d.shape,(2,2))
        self.assertGreater(d[0,1],0)
        self.assertGreater(d[1,0],0)
        self.assertEqual(d[1,1],0)

    def test_reject_wrong_native_source(self):
        with self.assertRaises(ValueError):native_pairs({'sha256':'B'},'A')

    def test_native_pair_order_does_not_create_new_collision(self):
        native={'sha256':'A','movimentos':{'m':{'novas_intersecoes':[['b','a',3]]}}}
        self.assertEqual(native_pairs(native,'A'),{('a','b')})


if __name__=='__main__':unittest.main()
