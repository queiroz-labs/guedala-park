import csv
import math
import unittest
from collections import defaultdict
import acustica_envoltoria as a


class EnvoltoriaTests(unittest.TestCase):
    def test_massa_impedancia_igual(self):
        m=1.2*343/(math.pi*500)
        self.assertAlmostEqual(a.massa_normal(m,500),10*math.log10(2))

    def test_massa_dobrar(self):
        self.assertAlmostEqual(a.massa_normal(200,500)-a.massa_normal(100,500),
                               20*math.log10(2),places=3)

    def test_composto_uniforme(self):
        self.assertAlmostEqual(a.composto([(2,30),(8,30)]),30)

    def test_composto_abertura(self):
        expected=-10*math.log10(.99*1e-5+.01)
        self.assertAlmostEqual(a.composto([(.99,50),(.01,0)]),expected)

    def test_flancos(self):
        self.assertEqual(a.perda_flancos(0),0)
        self.assertAlmostEqual(a.perda_flancos(1),10*math.log10(2))
        self.assertGreater(a.perda_flancos(3),a.perda_flancos(1))

    def test_ressonancia(self):
        self.assertAlmostEqual(a.ressonancia(200,10,.1)*2,a.ressonancia(200,10,.025))

    def test_fundo(self):
        self.assertAlmostEqual(a.corrigir_fundo(50,40),10*math.log10(90000))
        with self.assertRaises(ValueError): a.corrigir_fundo(45,40)

    def test_dominios(self):
        for fn,args in [(a.massa_normal,(0,100)),(a.composto,([(0,30)],)),
                        (a.perda_flancos,(-1,)),(a.ressonancia,(100,10,0))]:
            with self.assertRaises(ValueError): fn(*args)

    def test_areas_reconciliam(self):
        totals=defaultdict(float)
        for row in a.fronteiras():
            self.assertLessEqual(row['area_liquida_m2'],row['area_bruta_m2'])
            totals[row['ambiente']]+=row['area_liquida_m2']
        p=a.ROOT/'03_Ambientes/Acabamentos/Quantidades_por_ambiente.csv'
        for row in csv.DictReader(p.read_text(encoding='utf-8-sig').splitlines()):
            self.assertAlmostEqual(totals[row['ambiente']],
                float(row['parede_liquida_antes_revestimentos_moveis_m2']),places=5)

    def test_segmentos_disjuntos(self):
        groups=defaultdict(list)
        p=a.ROOT/'03_Ambientes/Acabamentos/Faces_e_vaos.csv'
        for row in csv.DictReader(p.read_text(encoding='utf-8-sig').splitlines()):
            groups[(row['ambiente'],row['eixo'],row['coordenada_cm'])].append(
                (float(row['inicio_cm']),float(row['fim_cm'])))
        for intervals in groups.values():
            intervals.sort()
            for left,right in zip(intervals,intervals[1:]): self.assertLessEqual(left[1],right[0])

    def test_rotulos_e_exportacao(self):
        rows=a.cenarios()
        self.assertEqual(len(rows),256+96+6+4+9+24+12)
        self.assertTrue(all('H' in r['metrica'] for r in rows))
        with (a.OUT/'Cenarios_envoltoria.csv').open(encoding='utf-8') as f:
            exported=list(csv.DictReader(f,delimiter=';'))
        self.assertEqual(len(exported),len(rows))
        for original,saved in zip(rows,exported):
            self.assertEqual(saved,{k:str(v) for k,v in original.items()})


if __name__ == '__main__': unittest.main()
