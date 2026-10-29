"""Conservação de fluxo, geometria de raios e leitura de fotometria."""
import math
import unittest
import estudo_fotometrico as f


class Physics(unittest.TestCase):
    def test_union_cells_preserve_area_and_overlap(self):
        cs=f.cells([[0,0,1,1],[.5,0,1.5,1]],.75,.3)
        self.assertAlmostEqual(sum(c['area'] for c in cs),1.5)
        self.assertTrue(all(c['point'][2]==.75 for c in cs))
        vertical=f.cells([[0,1,1,2]],4,.3,normal=(0,1,0),vertical=True)
        self.assertAlmostEqual(sum(c['area'] for c in vertical),1)
        self.assertTrue(all(c['point'][1]==4 for c in vertical))

    def test_door_aperture_preserves_volume(self):
        solid=[0,0,0,3,.2,2.6];door=[1,0,0,2,.2,2.1]
        pieces=f.subtract_box(solid,door)
        volume=lambda b:math.prod(b[i+3]-b[i] for i in range(3))
        self.assertAlmostEqual(sum(map(volume,pieces)),volume(solid)-volume(door))
        self.assertFalse(any(f.segment_box((1.5,-1,1),(1.5,1,1),b) for b in pieces))
        self.assertTrue(any(f.segment_box((.5,-1,1),(.5,1,1),b) for b in pieces))

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

    def test_no_light_through_wall_and_no_duplicate_flux(self):
        cell=dict(point=(0,0,0),normal=(0,0,1),area=1)
        light=dict(code='Q05',position=(0,0,2),normal=(0,0,-1),fraction=1)
        s=f.SCENARIOS['central']
        e=f.direct(cell,[light],s,{},[])
        self.assertAlmostEqual(e,1440/math.pi/4*.8)
        self.assertEqual(f.direct(cell,[light],s,{},[[-1,-1,.8,1,1,1.2]]),0)
        half=dict(light,fraction=.5)
        self.assertAlmostEqual(f.direct(cell,[half,half],s,{},[]),e)

    def test_area_weighted_statistics_and_uniformity(self):
        st=f.statistics([dict(area=.25),dict(area=.75)],[100,200])
        self.assertEqual(st['mean'],175)
        self.assertAlmostEqual(st['u0'],100/175)
        self.assertEqual(f.statistics([],[])['u0'],0)


if __name__=='__main__':unittest.main()
