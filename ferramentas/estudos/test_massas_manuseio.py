import unittest
from massas_manuseio import calculate


def row(spec='Branco TX', contour='Retangular', c=2750, l=1850, t=18):
    return {'IDs CAD': 'Peca1 | Peca2', 'Qtd': '2', 'C nominal mm': str(c),
            'L nominal mm': str(l), 'Esp. envelope mm': str(t), 'Especificação documental': spec,
            'Peça': 'Painel', 'Contorno': contour}


class MassesTest(unittest.TestCase):
    def test_catalog_sheet_and_expansion(self):
        result = calculate('P03', row('Greenplac Arenza liso'))
        self.assertEqual(len(result), 2)
        self.assertAlmostEqual(result[0]['massa_envelope_cenario_kg'], 63.2)
        self.assertEqual(result[0]['envelope_cenario_maior_25kg'], 'sim')

    def test_no_material_guess(self):
        for spec, t in [('Branco TX', 18), ('Arenza liso', 18), ('Greenplac Arenza', 30)]:
            self.assertEqual(calculate('P01', row(spec, t=t))[0]['massa_envelope_cenario_kg'], '')

    def test_threshold_and_cutout_are_not_solid_claim(self):
        result = calculate('P01', row(contour='Recortado/especial', c=2200, l=1000, t=18))[0]
        self.assertEqual(result['maior_2200mm'], 'nao')
        self.assertEqual(result['contorno'], 'Recortado/especial')
        self.assertAlmostEqual(result['densidade_limiar_25kg_kg_m3'] * result['volume_envelope_m3'], 25)
        self.assertEqual(result['envelope_cenario_maior_25kg'], 'indeterminado')

    def test_planning_reference_covers_every_panel(self):
        result = calculate('P01', row('Branco TX', c=2000, l=2000, t=18))[0]
        self.assertEqual(result['massa_envelope_cenario_kg'], '')
        self.assertAlmostEqual(result['massa_referencia_planejamento_kg'], 0.072 * 63.2 / (2.75 * 1.85 * .018))
        self.assertEqual(result['referencia_maior_25kg'], 'sim')

    def test_quantity_mismatch_stops(self):
        data = row()
        data['Qtd'] = '1'
        with self.assertRaises(ValueError):
            calculate('P01', data)


if __name__ == '__main__':
    unittest.main()
