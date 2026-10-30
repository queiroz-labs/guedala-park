"""Cenários FICTÍCIOS para motor; reconciliação com a base documental preservada."""
import copy
import unittest
import numpy as np
import risco_orcamento_prazo as r


class Risco(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config=r.default_config()

    def deterministic(self):
        c=copy.deepcopy(self.config)
        for item in c['itens']:item['distribuicao']='ponto'
        for event in c['riscos']:event['probabilidade']=0
        c['custo_armazenamento_semana']=0
        return c

    def test_soma_deterministica_bate_r44_e_d05c(self):
        c=self.deterministic();data=r.simulate(c,{},128)
        np.testing.assert_allclose(data['execucao'],137748.11)
        np.testing.assert_allclose(data['total_planejado'],147748.11)
        scenario=next(s for s in c['cenarios'] if s['id']=='Etapa_D05C_documentada')
        np.testing.assert_allclose(r.simulate(c,scenario,128)['execucao'],127101.22)

    def test_semente_reproduz(self):
        a=r.simulate(self.config,{},200);b=r.simulate(self.config,{},200)
        for key in ['execucao','marcenaria','mudanca','total_planejado']:
            np.testing.assert_array_equal(a[key],b[key])

    def test_ponto_nao_varia(self):
        np.testing.assert_array_equal(r.sample(np.random.default_rng(1),[42,42,42],200),np.full(200,42))

    def test_dependencias_e_critico_dinamico(self):
        nodes=[dict(id='a',depends=[],origem_semana=0),dict(id='b',depends=[],origem_semana=0),dict(id='mudanca',depends=['a','b'])]
        d={'a':np.array([4.,2.]),'b':np.array([3.,3.]),'mudanca':np.ones(2)}
        end,critical,start,finish=r.scheduling(nodes,d)
        np.testing.assert_array_equal(end,[5,4]);np.testing.assert_array_equal(start['mudanca'],[4,3])
        self.assertEqual(np.mean(critical['a']),.5);self.assertEqual(np.mean(critical['b']),.5)

    def test_preparacao_pode_anteceder_chaves(self):
        nodes=[dict(id='a',depends=[],origem_semana=-4),dict(id='mudanca',depends=['a'],origem_semana=None)]
        end,_,start,_=r.scheduling(nodes,{'a':np.ones(2),'mudanca':np.ones(2)})
        np.testing.assert_array_equal(start['mudanca'],[-3,-3])

    def test_probabilidades_triviais_e_coerentes(self):
        c=self.deterministic();s=r.stats(r.simulate(c,{},100))
        self.assertEqual(s['execucao_ate120'],0);self.assertEqual(s['execucao_ate130_usa_reserva'],0)
        self.assertEqual(s['marcenaria_ate35'],0)
        s=r.stats(r.simulate(c,dict(marcenaria_fixa=35000),100))
        self.assertEqual(s['marcenaria_ate35'],1)
        self.assertEqual(s['execucao_ate120'],s['total_planejado_ate130'])
        self.assertLessEqual(s['mudanca_ate9'],s['mudanca_ate10']);self.assertLessEqual(s['mudanca_ate10'],s['mudanca_ate12'])

    def test_correlacao_constante_e_limites_invalidos(self):
        self.assertEqual(r.spearman(np.ones(10),np.arange(10)),0)
        with self.assertRaises(ValueError):r.sample(np.random.default_rng(1),[2,1,3],10)
        c=copy.deepcopy(self.config);c['riscos'][0]['probabilidade']=2
        with self.assertRaises(ValueError):r.simulate(c,{},10)

    def test_evento_medida_gera_custo_e_prazo(self):
        c=self.deterministic();data=r.simulate(c,dict(forcar_medida=True),100)
        self.assertTrue(np.all(data['custos']['Retrabalho hipotético']>0))
        self.assertTrue(np.all(data['riscos']['risco:medida_divergente']>0))


if __name__=='__main__':unittest.main()
