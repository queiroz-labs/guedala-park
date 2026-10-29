import unittest
from unittest.mock import Mock
from pathlib import Path
from climatizacao import energy, union_area, BTU_PER_WH, OPTIONS, climate, equipment_audit, partial_gain


class ClimatizacaoTest(unittest.TestCase):
    def test_asus_conditional_and_unknown_not_zero(self):
        def row(i,room,p):
            return dict(id=i,ambiente=room,potencia_W=p,item=i,qualidade='referencia',fonte='teste')
        result=equipment_audit([row('EQ28A','escritorio','20.8'),row('EQ27','escritorio',''),row('EQ01','cozinha','2061')])
        self.assertEqual(result[0]['parcela_sensivel_H06_W'],20.8)
        self.assertEqual(result[1]['parcela_sensivel_H06_W'],'')
        self.assertEqual(result[2]['entrada_referencia_W'],'2061')
        self.assertEqual(result[2]['parcela_sensivel_H06_W'],'')

    def test_conditional_equipment_not_scaled_with_lights(self):
        s,l=partial_gain(2,37.6,.5,20.8)
        self.assertAlmostEqual(s+l,273.6)
        s0,l0=partial_gain(2,37.6,.5,0)
        self.assertAlmostEqual(s-s0,20.8)
        self.assertEqual(l,l0)

    def test_consumo(self):
        self.assertEqual(energy(780,8),187.2)
        self.assertEqual(energy(0,8),0)

    def test_negativo(self):
        with self.assertRaises(ValueError):energy(-1,8)

    def test_sobreposicao(self):
        self.assertEqual(union_area([(0,0,2,2),(1,0,2,2)]),6)

    def test_separadas(self):
        self.assertEqual(union_area([(0,0,2,2),(3,0,1,1)]),5)

    def test_unidade(self):
        self.assertAlmostEqual(1000*BTU_PER_WH,3412.141633)

    def test_opcoes_nao_convertem_tensao(self):
        self.assertTrue(all(r[4]==220 for r in OPTIONS[:3]))

    def test_clima_estacao_errada(self):
        p=Mock();p.read_bytes.return_value=b'LOCATION,X,SP,BRA,TMY,000000\n'
        with self.assertRaisesRegex(ValueError,'Congonhas'):climate(p,Path('unused'))

    def test_clima_incompleto(self):
        p=Mock();p.read_bytes.return_value=b'LOCATION,X,SP,BRA,TMY,837800\n'+b'HEADER\n'*7
        with self.assertRaisesRegex(ValueError,'8760'):climate(p,Path('unused'))


if __name__=='__main__':unittest.main()
