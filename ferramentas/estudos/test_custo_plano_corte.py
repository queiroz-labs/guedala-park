import unittest
from custo_plano_corte import price,rolls


class CostTest(unittest.TestCase):
    def test_no_price_transfer_between_thickness_or_color(self):
        self.assertIsNone(price('Branco TX',16,'Lume')[0])
        self.assertIsNone(price('Louro Freijo Poro',18,'Lume')[0])
        self.assertIsNone(price('Off-white fosco',15,'Lume')[0])

    def test_sample_options_do_not_stack(self):
        self.assertEqual(price('Off-white fosco',18,'Lume')[0],589.47)
        self.assertEqual(price('Off-white fosco',18,'Areia')[0],643.98)
        self.assertEqual(price('Arenza',18,'Areia')[0],435.58)

    def test_whole_rolls_by_group(self):
        self.assertEqual(rolls(50),1)
        self.assertEqual(rolls(50.0001),2)
        self.assertEqual(rolls(0),0)


if __name__=='__main__':unittest.main()
