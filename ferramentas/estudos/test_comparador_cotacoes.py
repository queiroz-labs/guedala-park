"""FICTÍCIO: testes de comportamento; nenhum preço representa proposta recebida."""
import copy
from datetime import date
from decimal import Decimal
from pathlib import Path
import tempfile
import unittest
import comparador_cotacoes as c


def sourced(value, unit=''):
    return dict(valor=value, unidade=unit, origem='FICTÍCIO: teste')


class Comparador(unittest.TestCase):
    def test_unidades_e_ausencia(self):
        self.assertEqual(c.quantity('1.250,5','cm','m'),Decimal('12.505'))
        with self.assertRaises(ValueError):c.quantity('7','unidade','par')
        self.assertIsNone(c.number(''))
        self.assertEqual(c.number('0'),0)
        ref=next(r for r in c.references().values() if r['grupo']=='paineis')
        self.assertEqual(c.coverage(ref,{})[0],'não mencionada')
        self.assertEqual(c.coverage(ref,dict(situacao=sourced('incluida')))[0],'coberta com quantidade diferente')

    def test_ids_stable_and_legacy_rejected(self):
        from unittest.mock import patch
        original=c.references()
        rows=c.read_csv(c.ROOT/c.REF)
        with patch.object(c,'read_csv',return_value=list(reversed(rows))):
            self.assertEqual(c.references(),original)
        with self.assertRaises(ValueError):
            c.load_proposals(Path(__file__).parent/'testes/Cotacoes_ficticias.json')
        with self.assertRaises(ValueError):
            c.compare([],date(2026,11,4),c.WEIGHTS,[dict(linha='L001')])

    def test_current_scope_and_unresolved_quantities(self):
        refs=c.references()
        self.assertEqual(sum(int(r['quantidade']) for r in refs.values() if r['grupo']=='paineis'),251)
        proposal=dict(fornecedor='F01',campos=dict(preco_total=sourced('100'),escopo=sourced('integral')),linhas={})
        result=c.compare([proposal],date(2026,11,4),c.WEIGHTS)
        self.assertEqual(len(result['matriz']),len(refs))
        self.assertIsNone(result['resumo'][0]['equivalente_max'])
        self.assertIsNone(result['resumo'][0]['pontuacao'])
        self.assertEqual(c.gaps(),{})

    def test_other_proposal_requires_same_scope(self):
        code,ref=next((k,r) for k,r in c.references().items() if r['item'].startswith('Corrediças laterais'))
        first=dict(fornecedor='F01',campos=dict(escopo=sourced('integral')),linhas={})
        second=dict(fornecedor='F02',campos=dict(escopo=sourced('integral')),linhas={code:dict(situacao=sourced('incluida'),marca_modelo=sourced(ref['item']),quantidade=sourced('4','par'),preco_unitario=sourced('100'))})
        self.assertEqual(c.missing_cost(code,ref,first,[first,second],Decimal(1))[:2],(Decimal(100),Decimal(100)))
        second['campos']['escopo']=sourced('etapa')
        self.assertEqual(c.missing_cost(code,ref,first,[first,second],Decimal(1))[2],'sem base')

    def test_template_protects_answers(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp)
            c.templates(folder)
            rows=c.read_csv(folder/'Modelo_entrada.csv')
            rows[0]['valor']='FICTICIO'
            c.write_csv(folder/'Modelo_entrada.csv',rows,c.CSV_FIELDS)
            with self.assertRaises(ValueError):c.templates(folder)
            self.assertEqual(c.read_csv(folder/'Modelo_entrada.csv')[0]['valor'],'FICTICIO')

    def test_prazo_nao_confirma_mudanca(self):
        fields={k:sourced(v) for k,v in dict(producao_dias='35',entrega_dias='7',montagem_dias='7',inicio_semana_chaves='2',calendario='corridos',gatilho_prazo='executivo').items()}
        self.assertEqual(c.schedule(fields)[0],9)
        self.assertIn('atenção',c.schedule(fields)[1])
        fields['calendario']=sourced('uteis')
        self.assertIsNone(c.schedule(fields)[0])


if __name__=='__main__':unittest.main()
