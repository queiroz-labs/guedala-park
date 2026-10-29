import unittest
from acustica_cenarios import base_homogenea, campo_livre, somar_niveis


class AcusticaTest(unittest.TestCase):
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
