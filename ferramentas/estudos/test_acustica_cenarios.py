import unittest
import csv
from pathlib import Path
from acustica_cenarios import base_homogenea, campo_livre, somar_niveis


class AcusticaTest(unittest.TestCase):
    def test_csv_depurador_identifica_hipotese_arbitraria(self):
        path=Path(__file__).resolve().parents[2]/'03_Ambientes/Acustica/Cenarios.csv'
        with path.open(encoding='utf-8') as f:
            rows=[r for r in csv.DictReader(f,delimiter=';') if r['origem'].startswith('depurador_H/')]
        self.assertEqual(len(rows),54)
        self.assertTrue(all('varredura arbitraria, nao tipica' in r['limite'] for r in rows))

    def test_massas_analiticas(self):
        self.assertAlmostEqual(base_homogenea(100),94)
        self.assertAlmostEqual(base_homogenea(200),83.4639501518)

    def test_dobrar_distancia(self):
        self.assertAlmostEqual(campo_livre(60,2),53.9794000867)
        self.assertAlmostEqual(campo_livre(60,4),47.9588001734)

    def test_referencia_e_perda(self):
        self.assertEqual(campo_livre(60,2,2,10),50)

    def test_soma_energetica(self):
        self.assertAlmostEqual(somar_niveis([40,40]),43.0102999566)
        self.assertAlmostEqual(somar_niveis([40]),40)

    def test_dominio(self):
        for massa in (0,99,601):
            with self.assertRaises(ValueError): base_homogenea(massa)
        with self.assertRaises(ValueError): campo_livre(50,0)
        with self.assertRaises(ValueError): somar_niveis([])


if __name__ == '__main__': unittest.main()
