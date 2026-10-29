"""Conservação de fluxo, geometria de raios e leitura de fotometria."""
import math
import unittest
import estudo_fotometrico as f


class Physics(unittest.TestCase):
    def test_inverse_square_and_incidence(self):
        self.assertAlmostEqual(f.illuminance(100,2,.5),12.5)
        self.assertEqual(f.illuminance(100,1,-1),0)
        with self.assertRaises(ValueError):f.illuminance(100,0,1)

    def test_flux_conservation(self):
        # Numerical hemisphere integral of several cos^n models, independent of grids.
        for n in (0,1,3,20):
            count=20000; dt=math.pi/2/count
            total=sum(f.cosine_cd(1000,math.cos((i+.5)*dt),n)*2*math.pi*math.sin((i+.5)*dt)*dt for i in range(count))
            self.assertAlmostEqual(total,1000,places=3)

    def test_ray_occlusion_not_box_behind_source(self):
        box=(1,1,1,2,2,2)
        self.assertTrue(f.segment_box((0,1.5,1.5),(3,1.5,1.5),box))
        self.assertFalse(f.segment_box((0,0,0),(.5,.5,.5),box))
        self.assertFalse(f.segment_box((0,0,0),(0,3,3),box))

    def test_ies_parser_symmetry_and_reject_truncation(self):
        txt='TILT=NONE\n1 100 2 2 2 1 2 .3 .3 0\n1 1 5\n0 90\n0 90\n10 0 20 0'
        ies=f.read_ies(txt)
        self.assertEqual(f.ies_cd(ies,0,90),40)
        self.assertEqual(f.ies_cd(ies,0,270),40)
        self.assertAlmostEqual(f.ies_cd(ies,45,45),15)
        self.assertEqual(f.ies_cd(ies,91,0),0)
        with self.assertRaises(ValueError):f.read_ies(txt.rsplit(' ',1)[0])
        with self.assertRaises(ValueError):f.read_ies('TILT=INCLUDE')

    def test_existing_choices_and_targets(self):
        self.assertNotIn('E06',f.PRODUCTS)
        self.assertEqual(f.PRODUCTS['L11']['source'],'S2')
        self.assertEqual(f.PRODUCTS['B11']['source'],'S3')
        self.assertEqual(f.PRODUCTS['C14']['w'],13.2)
        self.assertEqual(next(r[3:5] for r in f.TARGETS if r[:2]==('escritorio','mesa/monitores')),(500,.7))


if __name__=='__main__':unittest.main()
