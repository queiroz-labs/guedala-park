"""Conservação de fluxo, geometria de raios e leitura de fotometria."""
import math
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import estudo_fotometrico as f


class Physics(unittest.TestCase):
    def test_radiosity_empty_cube_analytic(self):
        result=f.validate_radiosity()
        self.assertLess(result['erro_relativo'],.03)
        self.assertLess(result['difusor_retangular_erro_relativo'],.03)
        self.assertLess(abs(result['erro_lm']),1e-6)
        self.assertLess(result['residual_lm'],1e-6)

    def test_radiosity_open_boundary_energy(self):
        import numpy as np
        engine=f.Radiosity([(2,0,1,(0,0,2,2),(.2,.5,.8),'piso')],step=1,rays=128)
        for band in range(3):
            _,balance=engine.solve(np.full(4,200.),1000.,band)
            self.assertAlmostEqual(balance['absorvido_lm']+balance['perdido_lm']+balance['residual_lm'],1000.)
            self.assertAlmostEqual(balance['absorvido_lm'],800*(1-(.2,.5,.8)[band]))

    def test_clean_mesh_excludes_solids_and_roundoff_slivers(self):
        grid=f.clean_grid([[0,0,2,1]],.75,.3,[[.5,0,0,1.5,1,1]])
        self.assertAlmostEqual(sum(c['area'] for c in grid),1.)
        self.assertTrue(all(not .5<c['point'][0]<1.5 for c in grid))
        grid=f.cells([[0,0,1,1],[1-1e-16,0,2,1]],.75,.25)
        self.assertTrue(all(c['area']>1e-10 for c in grid))

    def test_case_planes_are_physical(self):
        cases=f.calculation_cases(f.load_geometry())
        self.assertFalse(any(c['id'] in ('cozinha_preparo','cozinha_pia','lavanderia_tanque') for c in cases))
        for c in cases:
            if 'tampo92' in c['id']:self.assertEqual(c['z'],.92)
            if c['id']=='quarto_leitura':self.assertGreater(c['z'],.64)

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

    def test_scene_interlocks_and_energy_accounting(self):
        with self.assertRaises(ValueError):f.active_power('B11',.5)
        self.assertAlmostEqual(f.active_power('C14',1,.8),16.5)
        self.assertEqual(f.active_power('B11',0),0)
        scenes,energy=f.scene_energy()
        self.assertEqual(len(scenes),30)
        self.assertNotIn('E06',{r['grupo'] for r in energy})
        # Recompute one month independently:13.2W times (1.5+.25*.25+.25*.1+.1)*30h,
        # plus1.2W x720h, all divided by efficiency. Controller counted once.
        expected=(13.2*(1.5+.25*.25+.25*.1+.1)*30+1.2*720)/.8/1000
        self.assertAlmostEqual(next(r for r in energy if r['grupo']=='C14')['kWh_mes_alto'],expected,places=4)
        self.assertTrue(all(r['kWh_mes_alto']>=r['kWh_mes_baixo'] for r in energy))

    def test_minimal_uniform_addition(self):
        extra=f.uniform_addition(400,100,500,.7)
        self.assertAlmostEqual(extra,600)
        self.assertAlmostEqual((100+extra)/(400+extra),.7)
        self.assertEqual(f.uniform_addition(500,400,500,.7),0)

    def test_required_flux_mean_and_uniformity_upper_bound(self):
        grid=[dict(area=.5),dict(area=.5)]
        self.assertEqual(f.required_scale(grid,[100,100],[100,100],300,.7),(2.,float('inf')))
        self.assertIsNone(f.required_scale(grid,[100,100],[0,200],300,.7))
        interval=f.required_scale(grid,[100,400],[200,0],300,.7)
        self.assertAlmostEqual(interval[0],75/130)
        self.assertAlmostEqual(interval[1],225/70)
        st=f.statistics(grid,[100+interval[0]*200,400])
        self.assertGreaterEqual(st['mean'],300)
        self.assertAlmostEqual(st['u0'],.7)

    def test_person_is_in_front_of_each_task(self):
        g=f.load_geometry()
        a=next(b for b,label,_ in f.room_solids(g,dict(id='cozinha_preparo_tampo92_pessoa')) if label=='cabeca_H13')
        b=next(b for b,label,_ in f.room_solids(g,dict(id='cozinha_pia_tampo92_pessoa')) if label=='cabeca_H13')
        self.assertAlmostEqual(a[0]-b[0],.65)
        self.assertAlmostEqual(a[3]-b[3],.65)
        self.assertEqual(a[4:],b[4:])

    def test_specular_geometry_and_equal_angles(self):
        import numpy as np
        hit=f.specular_hit((1,2,1),(-1,2,1),(0,0,0),(0,1,0))
        np.testing.assert_allclose(hit[0],(0,0,1))
        self.assertAlmostEqual(hit[1],math.degrees(math.atan(.5)))
        self.assertIsNone(f.specular_hit((1,-2,1),(-1,2,1),(0,0,0),(0,1,0)))

    def test_solid_angle_and_guth(self):
        import numpy as np
        corners=[(-1,-1,2),(1,-1,2),(1,1,2),(-1,1,2)]
        self.assertAlmostEqual(f.rectangle_solid_angle(np.zeros(3),corners),4*math.atan(1/(2*math.sqrt(6))))
        self.assertEqual(f.guth_position((0,1,0),(0,1,0)),1.)
        self.assertGreater(f.guth_position((0,1,1),(0,1,0)),1.)
        with self.assertRaises(ValueError):f.guth_position((0,-1,1),(0,1,0))

    def test_official_ies_integrated_flux_not_watt_scaled(self):
        ies=json.loads((f.OUT/'Fotometria_fontes.json').read_text(encoding='utf-8'))['EVO_2021']
        self.assertAlmostEqual(f.ies_cd(ies,0,0),1022.363)
        integral=0
        for deg in range(90):
            theta=deg+.5
            avg=(f.ies_cd(ies,theta,0)+2*f.ies_cd(ies,theta,45)+f.ies_cd(ies,theta,90))/4
            integral+=2*math.pi*avg*math.sin(math.radians(theta))*math.pi/180
        self.assertLess(abs(integral-2329)/2329,.02)
        self.assertEqual(ies['watts'],35.65)

    def test_reproduction_outside_repository(self):
        # A full isolated run must reproduce committed CSVs, maps and report.
        with tempfile.TemporaryDirectory(prefix='gp_lux_test_') as t:
            proc=subprocess.run([sys.executable,'-B',str(Path(f.__file__)), '--saida',t],capture_output=True,text=True)
            self.assertEqual(proc.returncode,0,proc.stdout+proc.stderr)
            expected=['Resumo_lux.csv','Grades_lux.csv','Sensibilidade_luz.csv','Cenas_luz.csv','Consumo_luz.csv',
                      'Correntes_luz.csv','Alternativas_luz.csv','Estudo_fotometrico.md','Coerencia_imagens_luz.csv','Rastreio_fotometrico.json',
                      'Energia_luz.csv','Superficies_luz.csv','Validacao_luz.json','Fluxo_necessario_luz.csv','Camadas_tarefa_luz.csv',
                      'UGR_luz.csv','Reflexos_telas_luz.csv']
            expected+=['Mapa_lux_'+k+'.png' for k in ('sala','cozinha','lavanderia','banho','quarto','escritorio','circulacao')]
            for name in expected:
                actual,reference=(Path(t)/name).read_bytes(),(f.OUT/name).read_bytes()
                if not name.endswith('.png'):
                    actual,reference=actual.replace(b'\r\n',b'\n'),reference.replace(b'\r\n',b'\n')
                self.assertEqual(actual,reference,name)


if __name__=='__main__':unittest.main()
