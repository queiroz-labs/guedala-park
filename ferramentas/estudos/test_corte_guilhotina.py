import copy, unittest
from corte_guilhotina import pack, optimize, validate, TRIM, KERF, load_panels


def panel(name,w,h,directional=False):
    return dict(id=name,module='P01',w=w,h=h,directional=directional)


class GuilhotinaTests(unittest.TestCase):
    def test_serra_nao_desaparece(self):
        rows=[panel('a',500,500),panel('b',500,500)]
        good=pack(rows,1000+KERF,500,0,0);validate(good,rows,1000+KERF,500)
        self.assertEqual(len(good['sheets']),1)
        self.assertEqual(len(pack(rows,1000,500,0,0)['sheets']),2)

    def test_veio_bloqueia_rotacao(self):
        rows=[panel('veio',800,300,True)]
        self.assertEqual(pack(rows,400,900,0,0)['oversized'],['veio'])
        rows[0]['directional']=False
        p=pack(rows,400,900,0,0);validate(p,rows,400,900)
        self.assertTrue(p['sheets'][0]['placements'][0]['rotated'])

    def test_corte_alterado_detectado(self):
        rows=[panel('a',200,100),panel('b',200,100)]
        p=optimize(rows,1000,1000);validate(p,rows,1000,1000)
        q=copy.deepcopy(p);q['sheets'][0]['placements'][0]['x']+=1
        with self.assertRaises(AssertionError):validate(q,rows,1000,1000)
        q=copy.deepcopy(p);q['sheets'][0]['cuts'][0]['children'][0]=(0,0,200,200)
        with self.assertRaises(AssertionError):validate(q,rows,1000,1000)

    def test_margem_e_limite_de_formato(self):
        p=[panel('fundo',2096,1964)]
        self.assertEqual(optimize(p,2750-2*TRIM,1850-2*TRIM)['oversized'],['fundo'])
        q=optimize(p,2750-2*TRIM,2100-2*TRIM)
        validate(q,p,2750-2*TRIM,2100-2*TRIM);self.assertEqual(len(q['sheets']),1)

    def test_fontes_e_p13(self):
        rows=load_panels();self.assertEqual(len(rows),249)
        p=next(p for p in rows if p['id']=='Peca350')
        self.assertFalse(p['packing_blockers']);self.assertTrue(p['directional'])
        self.assertTrue(next(p for p in rows if p['id']=='PecaBaixaR036')['packing_blockers'])


if __name__=='__main__':unittest.main()
