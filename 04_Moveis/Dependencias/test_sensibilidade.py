import copy
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from sensibilidade import (document,dimensional,variable_specs,response_model,
                           actual,predict,gap_map,tolerance,perform)


class Sensibilidade(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc=document();cls.rows=dimensional.entradas(nominal=True)
        cls.specs=variable_specs(cls.doc,cls.rows)
        cls.base,cls.coeff=response_model(cls.rows,cls.doc,cls.specs)

    def test_modelo_cruzado_com_motor(self):
        for values in [{'DEP-COZ-PRUMO':0},{'DEP-COZ-PRUMO':-20,'DIM-07/1':1531},
                       {'CAMPO-COZ-ESQUADRO':.73,'CAMPO-COZ-PISO':9,'PD-COZ':2581},
                       {'PR-WALLS-00-X':-80,'DIM-03/0':2470}]:
            values={k:v for k,v in values.items() if k in self.specs}
            expected=gap_map(actual(values,self.rows,self.doc))
            calculated=predict(values,self.base,self.coeff,self.specs)
            self.assertEqual(expected.keys(),calculated.keys())
            for k,v in expected.items():self.assertAlmostEqual(v,calculated[k],places=6)

    def test_limite_prumo_zero_e_origem_quarto_10(self):
        t,sign,_=tolerance(self.specs['DEP-COZ-PRUMO'],self.coeff['DEP-COZ-PRUMO'],self.base)
        self.assertEqual(t,0);self.assertEqual(sign,'aumentar')
        t,sign,_=tolerance(self.specs['PR-FLOORS-00-X'],self.coeff['PR-FLOORS-00-X'],self.base)
        self.assertEqual(t,10);self.assertEqual(sign,'aumentar')

    def test_parede_sem_regra_nao_ganha_coeficiente(self):
        self.assertEqual(self.coeff['PR-WALLS-00-X'],{})

    def test_cache_recusa_envelope_que_nao_seja_fixo(self):
        changed=copy.deepcopy(self.doc)
        next(r for r in changed['regras'] if r.get('eixo') is not None)['modo']='segue_parede'
        with tempfile.TemporaryDirectory(prefix='gp-mc-test-') as tmp:
            with patch('sensibilidade.document',return_value=changed):
                with self.assertRaisesRegex(ValueError,'Envelope móvel'):perform(Path(tmp)/'saida')


if __name__=='__main__':unittest.main()
