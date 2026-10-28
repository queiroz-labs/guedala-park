"""Conferência contra âncoras documentais e prevenção de compras duplicadas."""
import contextlib
import io
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from quantificar_furacao import generate,edge_rows
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
            self.assertEqual(q['Limitador 86'],52)
            self.assertEqual(q['Corrediça FGVTN500'],7)
            self.assertEqual(q['Corrediça MOVENTO400'],2)
            self.assertEqual(q['Suportes de prateleira'],8)
            self.assertEqual(q['Porcas transversais'],4)
            self.assertEqual(summary['paineis_sem_mapa_borda'],249)
            self.assertIsNone(summary['fita_metros_definidos'])
            self.assertGreater(summary['fita_metros_propostos_retos'],0)
            base,alternative=summary['cenarios_conectores']
            self.assertEqual(base['minifix'],316)
            self.assertEqual(base['minifix']+base['confirmat'],alternative['minifix']+alternative['confirmat'])
            self.assertEqual(base['cavilhas'],alternative['cavilhas'])
            self.assertLess(alternative['horas_min'],base['horas_min'])
            bom=read(dest/'Ferragens_por_movel.csv')
            self.assertEqual(sum(float(r['quantidade']) for r in bom if r['familia']=='Confirmat 7x50' and r['movel']=='P18'),4)
            self.assertEqual(sum(float(r['quantidade']) for r in bom if r['familia']=='Cavilhas Ø8x30' and r['movel']=='P18'),8)
            self.assertEqual(sum(float(r['quantidade']) for r in bom if r['familia']=='Engates FGVTN500 incluidos'),7)
            self.assertTrue(all('incluido' in r['base'] for r in bom if r['familia']=='Engates FGVTN500 incluidos'))
            # Regeneration must be byte-identical and preserve blank unknowns.
            before={p.name:p.read_bytes() for p in dest.iterdir()}
            with contextlib.redirect_stdout(io.StringIO()):generate(dest,SimpleNamespace(tempos=None,setup_min=2,setup_max=5))
            self.assertEqual(before,{p.name:p.read_bytes() for p in dest.iterdir()})

    def test_fita_nao_confunde_altura_da_lateral_com_profundidade(self):
        ps={}
        for pid,name,c,l,axes in [('porta','Porta',700,500,(2,0,1)),('lateral','Lateral',1800,600,(2,1,0)),('fundo','Fundo',1800,800,(2,0,1))]:
            ps[pid]=dict(id=pid,name=name,c=c,l=l,t=18,axes=axes,mod='P01',finish='Branco TX',contour='Retangular')
        rows,_=edge_rows(ps);d={r['peca']:r for r in rows}
        self.assertEqual(d['porta']['metros_propostos_retos'],2.4)
        self.assertEqual(d['lateral']['metros_propostos_retos'],1.8)
        self.assertEqual(d['fundo']['metros_propostos_retos'],0)
        self.assertEqual(d['lateral']['metros_propostos_com_perda'],1.98)

    def test_recorte_sem_descricao_nao_recebe_perimetro_do_envelope(self):
        row,_=edge_rows({'L':dict(id='L',name='Tampo em L',c=1000,l=600,t=18,mod='P02',finish='Branco TX',contour='Recortado/especial')})
        self.assertEqual(row[0]['metros_propostos_retos'],'')


if __name__=='__main__':unittest.main()
