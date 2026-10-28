"""Conferência contra âncoras documentais e prevenção de compras duplicadas."""
import contextlib
import io
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from quantificar_furacao import generate
from conferir_furacao import read


class Quantitativos(unittest.TestCase):
    def test_inventario_documental_e_componentes(self):
        with tempfile.TemporaryDirectory(prefix='gp-quantidades-') as tmp:
            dest=Path(tmp)
            with contextlib.redirect_stdout(io.StringIO()):
                summary=generate(dest,SimpleNamespace(tempos=None,setup_min=2,setup_max=5))
            q=summary['ferragens_por_familia']
            self.assertEqual(q['Dobradiça Blum 71B3550'],52)
            self.assertEqual(q['Base Blum 173H7100'],52)
            self.assertEqual(q['Corrediça FGVTN500'],7)
            self.assertEqual(q['Corrediça MOVENTO400'],2)
            self.assertEqual(q['Suportes de prateleira'],8)
            self.assertEqual(q['Porcas transversais'],4)
            self.assertEqual(summary['paineis_sem_mapa_borda'],249)
            self.assertIsNone(summary['fita_metros_definidos'])
            bom=read(dest/'Ferragens_por_movel.csv')
            self.assertEqual(sum(float(r['quantidade']) for r in bom if r['familia']=='Confirmat 7x50' and r['movel']=='P18'),4)
            self.assertEqual(sum(float(r['quantidade']) for r in bom if r['familia']=='Cavilhas Ø8x30' and r['movel']=='P18'),8)
            self.assertEqual(sum(float(r['quantidade']) for r in bom if r['familia']=='Engates FGVTN500 incluidos'),7)
            self.assertTrue(all('incluido' in r['base'] for r in bom if r['familia']=='Engates FGVTN500 incluidos'))
            # Regeneration must be byte-identical and preserve blank unknowns.
            before={p.name:p.read_bytes() for p in dest.iterdir()}
            with contextlib.redirect_stdout(io.StringIO()):generate(dest,SimpleNamespace(tempos=None,setup_min=2,setup_max=5))
            self.assertEqual(before,{p.name:p.read_bytes() for p in dest.iterdir()})


if __name__=='__main__':unittest.main()
