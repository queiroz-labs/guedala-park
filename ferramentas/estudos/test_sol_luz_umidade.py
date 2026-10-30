"""Testes físicos pequenos, sem rede, climas externos ou alteração de CAD."""
import copy
import json
import math
from pathlib import Path
import unittest
import numpy as np
from conforto_fisica import (solar,day_number,incidence,saturation,dewpoint,
    mixing_ratio,rh_from_w,surface_rh,critical_frsi,moisture_step,Wall,
    cavity_surface,cross_flow,rc_step,required,clear_sky)
from conforto_geometria import (sky_component,internal_reflection,patch,
    obstruction,trace_boxes,tower_horizon)
from conforto_clima import erbs,load_era
from sol_luz_umidade import exposure
from conforto_calor import thermostat_response

CONFIG=Path(__file__).with_name('modelos')/'Conforto_hipoteses.json'


class Physics(unittest.TestCase):
    def setUp(self):self.c=json.loads(CONFIG.read_text(encoding='utf-8'))

    def test_solar_noon_seasons(self):
        for month,target in [(12,89.8),(3,66.4),(6,43.0),(9,66.4)]:
            hours=np.linspace(11,13,4001);alt,az=solar(day_number(month,23 if month==9 else 21),hours)
            i=int(alt.argmax());self.assertAlmostEqual(float(alt[i]),target,delta=1.2)
            # All four dates put declination north of this latitude at transit.
            self.assertLess(min(float(az[i]),360-float(az[i])),4)

    def test_sunset_geometric(self):
        for month,target in [(12,244),(6,296)]:
            lo,hi=16.,20.
            for _ in range(45):
                mid=(lo+hi)/2;alt,az=solar(day_number(month),mid)
                if alt>0:lo=mid
                else:hi=mid
            alt,az=solar(day_number(month),(lo+hi)/2)
            self.assertAlmostEqual(float(az),target,delta=1)
            self.assertAlmostEqual(float(alt),0,places=8)

    def test_north_south_window(self):
        alt,az=solar(day_number(6),12.1)
        self.assertGreater(float(incidence(alt,az,0)),.5)
        self.assertEqual(float(incidence(alt,az,180)),0)

    def test_low_sun_depth(self):
        w=self.c['janelas'][0].copy();w['plano_m']=0
        floor={'test':[[0,0,30,30]]}
        high=patch(w,40,245,[],floor,self.c);low=patch(w,10,245,[],floor,self.c)
        self.assertGreater(low['profundidade_sem_recorte_m'],high['profundidade_sem_recorte_m'])
        self.assertGreater(low['piso_m2'],high['piso_m2'])

    def test_aperture_flux_projection(self):
        w=self.c['janelas'][0].copy();w['plano_m']=0;self.c['parede']['espessura_vano_m']=0
        result=patch(w,30,245,[],{'test':[[0,0,30,30]]},self.c)
        expected=w['largura_m']*w['altura_m']/math.tan(math.radians(30))
        self.assertAlmostEqual(result['piso_m2'],expected,places=8)

    def test_sky_zero_without_window(self):
        e=sky_component([[1,2,.75]],[],[],self.c)
        self.assertEqual(float(e[0]),0)
        self.assertEqual(internal_reflection(0,.6,50),0)

    def test_sky_area_monotonic(self):
        w=self.c['janelas'][0].copy();w['plano_m']=0;w['inicio_m']=.5;w['largura_m']=1
        small=sky_component([[1,2,.75]],[w],[],self.c)[0]
        w['inicio_m']=0;w['largura_m']=2
        large=sky_component([[1,2,.75]],[w],[],self.c)[0]
        self.assertGreater(large,small)

    def test_reflection_lighter(self):
        self.assertGreater(internal_reflection(100,.8,40),internal_reflection(100,.4,40))

    def test_opaque_box_blocks(self):
        distance,hit,face=trace_boxes(np.array([[0.,0.,1.]]),np.array([[0.,1.,0.]]),[([-.5,.5,0,.5,1.,2.],'wall')])
        self.assertEqual(int(hit[0]),0);self.assertAlmostEqual(float(distance[0]),.5);self.assertEqual(int(face[0]),1)

    def test_tetens_known(self):
        self.assertAlmostEqual(float(saturation(20)),2338,delta=2)
        self.assertAlmostEqual(float(dewpoint(20,50)),9.27,delta=.05)
        self.assertAlmostEqual(float(dewpoint(30,70)),23.93,delta=.1)

    def test_psychrometric_roundtrip(self):
        for t in (5,20,30):
            for rh in (30,65,95):self.assertAlmostEqual(float(rh_from_w(t,mixing_ratio(t,rh))),rh,places=10)

    def test_condensation_and_frsi(self):
        td=float(dewpoint(20,65))
        self.assertGreater(float(surface_rh(20,65,td-.5)),100)
        self.assertLess(float(surface_rh(20,65,td+.5)),100)
        f=critical_frsi(20,65,5)
        self.assertAlmostEqual(float(surface_rh(20,65,5+15*f)),80,places=9)
        self.assertTrue(math.isnan(critical_frsi(20,65,25)))

    def test_wall_stationary(self):
        wall=Wall([[.2,1,2000000]])
        result=wall.series(np.zeros(3000),20)
        expected=20-(20-0)*.13/(.2+.13+.04)
        self.assertAlmostEqual(float(result[-1]),expected,places=8)
        self.assertAlmostEqual(wall.u,1/.37,places=10)

    def test_wall_solar_warms(self):
        wall=Wall(self.c['parede']['camadas'])
        base=wall.series(np.full(300,10.),20)
        sunny=wall.series(np.full(300,20.),20)
        self.assertGreater(float(sunny[-1]),float(base[-1]))

    def test_moisture_closed_conserves(self):
        w=float(mixing_ratio(20,65));end,exported=moisture_step(w,0,0,.01,25)
        self.assertEqual(end,w);self.assertEqual(exported,0)
        self.assertAlmostEqual(float(rh_from_w(20,end)),65,places=10)

    def test_moisture_mass_source_and_flow(self):
        w=.01;source=.00003;dt=300;vol=25;rho=1.1
        end,exported=moisture_step(w,source,.04,.008,vol,dt,rho)
        self.assertAlmostEqual(rho*vol*w+source*dt-exported,rho*vol*end,places=12)

    def test_missing_is_not_zero(self):
        for val in ('',None):
            with self.assertRaises(ValueError):required({'test':val},'test')
        with self.assertRaises(KeyError):required({},'test')
        with self.assertRaises(FileNotFoundError):load_era(Path('clima_inexistente.json'),self.c)
        self.assertEqual(required({'test':0},'test'),0)  # zero explícito continua válido.

    def test_uncertainty_orientation(self):
        w=self.c['janelas'][2]
        values=[exposure(w,6,self.c,angle)['h_sol_geometrico'] for angle in (240,245,250)]
        self.assertGreater(max(values)-min(values),.1)
        low=Wall([[.02,1,1400000],[.14,.45,1200000],[.015,.7,1000000]])
        high=Wall([[.02,1,1400000],[.14,1.2,1200000],[.015,.7,1000000]])
        self.assertGreater(high.u,low.u)

    def test_obstruction_scenarios(self):
        w=self.c['janelas'][2]
        self.assertEqual(float(obstruction(w,249,self.c,'hospital20')),20)
        self.assertEqual(float(obstruction(w,269,self.c,'hospital20')),0)
        free=exposure(w,12,self.c,245,'livre')['h_sol_geometrico']
        blocked=exposure(w,12,self.c,245,'hospital20')['h_sol_geometrico']
        self.assertGreater(free,blocked)
        self.assertTrue(np.isfinite(tower_horizon(w,np.arange(360),self.c)).all())

    def test_cabinet_ventilation(self):
        closed=cavity_surface(20,5,.3,.015,.02,0)
        vent=cavity_surface(20,5,.3,.015,.02,.8)
        self.assertGreater(float(vent),float(closed))

    def test_cross_ventilation(self):
        q,sign=cross_flow(2.,135,[.5,1.5]);q2,_=cross_flow(4.,135,[.5,1.5]);closed,_=cross_flow(2.,135,[.5,1.5],path_area=.015)
        self.assertAlmostEqual(float(q2),2*float(q));self.assertGreater(float(sign),0);self.assertLess(float(closed),float(q))
        _,reverse=cross_flow(2.,315,[.5,1.5]);self.assertLess(float(reverse),0)

    def test_rc_equilibrium(self):
        state=rc_step(np.array([20.,20.]),20,20,0,0,10,2,(30000,2000000),50,2.7,5.7,10)
        self.assertTrue(np.allclose(state,[20,20]))

    def test_thermostat_unilateral(self):
        matrix=np.array([[10.,-8.],[-8.,10.]])
        air=np.array([18.,19.99]);mass=air.copy();den=np.array([100.,100.]);ham=np.array([10.,10.])
        ta,tm,q=thermostat_response(matrix,den,ham,air,mass,20,np.array([True,True]))
        self.assertTrue((q>=0).all());self.assertEqual(q[1],0)
        self.assertTrue(((ta+tm)/2>=20-1e-9).all())
        ta,tm,q=thermostat_response(matrix,den,ham,air,mass,20,np.array([True,False]),cap=1)
        self.assertLess((ta[0]+tm[0])/2,20);self.assertLessEqual(float(q.max()),1)

    def test_radiation_balance(self):
        ghi=np.array([0.,300.,800.]);alt=np.array([-5.,30.,60.]);dni,dhi=erbs(ghi,alt,[10,10,10])
        self.assertTrue(np.allclose(dni*np.sin(np.radians(alt))+dhi,ghi))
        self.assertEqual(float(clear_sky(-10)[0]),0)


if __name__=='__main__':unittest.main()
