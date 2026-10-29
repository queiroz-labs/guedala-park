import unittest
from complementar_corte import retalhos, financial, propostas


class ComplementTest(unittest.TestCase):
    def test_retalhos_identidade_e_limiar(self):
        data={'plans':[{'resumo':dict(variante='base',cenario='10/4',padrao='Branco TX',espessura_mm=18),
                       'plano':{'sheets':[{'free':[(10,10,300,400),(20,20,301,400)]}]}}]}
        rows=retalhos(data)
        self.assertEqual([r['reaproveitavel'] for r in rows],[False,True])
        self.assertAlmostEqual(sum(r['area_m2'] for r in rows),.2404)
        self.assertEqual(rows[1]['desenho'],'G001_chapa01.svg')
        self.assertEqual(rows[1]['comprimento_mm'],301)

    def test_preco_ausente_nao_virar_total(self):
        groups=[dict(padrao='Branco TX',espessura_mm=16,chapas_subconjunto=1),
                dict(padrao='Branco TX',espessura_mm=18,chapas_subconjunto=2)]
        result=financial(groups,'Lume')
        self.assertEqual(result['chapas'],3)
        self.assertEqual(result['chapas_com_referencia'],2)
        self.assertAlmostEqual(result['parcial_chapas_min'],730.22)
        self.assertIn('16 mm',result['grupos_sem_preco'])

    def test_opcoes_isoladas_e_bordas_desconhecidas(self):
        base=dict(variante='base',cenario='s',padrao='Off-white fosco',espessura_mm=18,chapas_subconjunto=1,nao_cabem='')
        data={'variants':{'base':{},'kit':{'total':2,'bloqueados':['nova']}},
              'plans':[{'resumo':base},{'resumo':dict(base,variante='kit')}]}
        rows=propostas(data)
        self.assertEqual(len(rows),3)
        self.assertEqual({r['parcial_chapas_min'] for r in rows},{589.47,643.98,607.15})
        for row in rows:
            self.assertEqual(row['custo_total'],'')
            self.assertEqual(row['custo_fita'],'')
            self.assertEqual(row['delta_parcial_min'],0)
            self.assertEqual(row['paineis_bloqueados'],1)


if __name__=='__main__': unittest.main()
