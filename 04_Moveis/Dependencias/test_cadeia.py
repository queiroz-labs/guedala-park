"""Integração real dos geradores em saída descartável, sem FCStd."""
import contextlib
import csv
import io
from pathlib import Path
import tempfile
import unittest
from orquestrar import ROOT,run,document,evaluate,gap_map,dimensional,outside


class Cadeia(unittest.TestCase):
    def test_saida_de_cenario_nao_pode_ser_repositorio(self):
        with self.assertRaises(ValueError):outside(ROOT/'04_Moveis/Dependencias/Resultado')

    def test_caixas_fixas_e_furos_preservados_com_fixture(self):
        with tempfile.TemporaryDirectory(prefix='gp-cadeia-test-') as tmp:
            with contextlib.redirect_stdout(io.StringIO()):
                result,output=run(ROOT/'ferramentas/medidas/cenarios/ensaio_chaves.csv',Path(tmp)/'saida')
            self.assertEqual(result['pecas_total'],249)
            self.assertEqual(result['pecas_alteradas'],0)
            self.assertEqual(result['furos_novos'],0)
            self.assertEqual(result['furos_perdidos'],0)
            self.assertEqual(result['conflitos_novos'],0)
            self.assertEqual(result['novas_folgas_negativas'],10)
            self.assertIsNone(result['orcamento']['delta_reais_total'])
            self.assertTrue((output/'Furacao/Quantitativos.json').is_file())
            self.assertTrue((output/'Chapas_virtuais.json').is_file())
            self.assertEqual(sum(len(list(csv.DictReader(io.StringIO(p.read_text(encoding='utf-8-sig')),delimiter=';'))) for p in (output/'Furacao').glob('P??-coordenadas.csv')),2286)

    def test_esquadro_e_piso_consumem_folga_sem_mudar_caixa(self):
        doc=document();rows=dimensional.entradas(nominal=True)
        base=evaluate(rows,doc);other=evaluate(rows,doc,{'CAMPO-COZ-ESQUADRO':1,'CAMPO-COZ-PISO':10})
        b,a=gap_map(base),gap_map(other)
        self.assertLess(a['P10/Y/fim'],b['P10/Y/fim'])
        self.assertAlmostEqual(a['P10/Z/topo'],b['P10/Z/topo']-10)
        self.assertEqual(base['envelopes'],other['envelopes'])

    def test_auxiliar_invalido_rejeitado(self):
        from orquestrar import parse_aux
        with self.assertRaises(ValueError):parse_aux('CAMPO-COZ-ESQUADRO','1 mm')
        with self.assertRaises(ValueError):parse_aux('CAMPO-COZ-PISO','-1 mm')


if __name__=='__main__':unittest.main()
