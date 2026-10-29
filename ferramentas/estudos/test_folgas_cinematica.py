import unittest
import numpy as np
from medir_folgas_cinematica import bounded_minimum,bounded_search,oriented_lower_bound


class Bounds(unittest.TestCase):
    def test_budget_returns_interval_not_false_minimum(self):
        result=bounded_search([0,1,9],lambda k:[4,2,10][k],max_calls=1)
        self.assertFalse(result['complete'])
        self.assertEqual((result['lower'],result['upper']),(1,4))
        self.assertLessEqual(result['lower'],2);self.assertGreaterEqual(result['upper'],2)

    def test_zero_proves_minimum_even_with_budget(self):
        self.assertTrue(bounded_search([0,0],lambda k:0,max_calls=1)['complete'])

    def test_pruning_preserves_minimum(self):
        distances=[4,2,9,10]
        result,index,calls=bounded_minimum([0,1,9,10],lambda k:distances[k])
        self.assertEqual((result,index,calls),(2,1,2))

    def test_zero_is_global_distance_minimum(self):
        result,index,calls=bounded_minimum([0,0,1],lambda k:0)
        self.assertEqual((result,calls),(0,1))

    def test_invalid_lower_bound_is_rejected(self):
        with self.assertRaises(ValueError):bounded_minimum([3],lambda k:2)

    def test_random_bounds_match_exhaustive_oracle(self):
        rng=np.random.default_rng(42)
        for _ in range(100):
            true=rng.uniform(0,100,200)
            bounds=true*rng.uniform(0,1,200)
            result,_,_=bounded_minimum(bounds,lambda k:true[k])
            self.assertAlmostEqual(result,float(true.min()))

    def test_oriented_bound_common_rotation_against_exact_boxes(self):
        rng=np.random.default_rng(71)
        for _ in range(100):
            q,_=np.linalg.qr(rng.normal(size=(3,3)))
            if np.linalg.det(q)<0:q[:,0]*=-1
            transform=np.eye(4);transform[:3,:3]=q
            delta=rng.uniform(-10,10,3)
            a=np.array([-1,-2,-3,1,2,3]);b=a+np.tile(delta,2)
            exact=np.linalg.norm(np.maximum(np.abs(delta)-[2,4,6],0))
            result=oriented_lower_bound(a,[transform],b,[transform])[0,0]
            self.assertLessEqual(result,exact+1e-9)

    def test_oriented_synchronized_matches_diagonal(self):
        rotations=[]
        for angle in (0,.3,.9):
            m=np.eye(4);c,s=np.cos(angle),np.sin(angle);m[:2,:2]=[[c,-s],[s,c]];rotations.append(m)
        a=[0,0,0,1,2,1];b=[4,0,0,5,1,1]
        all_states=oriented_lower_bound(a,rotations,b,rotations)
        np.testing.assert_allclose(oriented_lower_bound(a,rotations,b,rotations,True),np.diag(all_states))


if __name__=='__main__':unittest.main()
