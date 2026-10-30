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
    def setUp(self):
        self.proposals = c.load_proposals(Path(__file__).parent / 'testes/Cotacoes_ficticias.json')

    def result(self):
        return c.compare(self.proposals, date(2026, 10, 29), c.WEIGHTS)

    def test_unidades_e_decimal(self):
        self.assertEqual(c.quantity('1.250,5', 'cm', 'm'), Decimal('12.505'))
        self.assertEqual(c.quantity('1000', 'mm', 'm'), 1)
        with self.assertRaises(ValueError):
            c.quantity('7', 'unidade', 'par')

    def test_ausencia_nao_zero(self):
        self.assertIsNone(c.number(''))
        self.assertEqual(c.number('0'), 0)
        ref = c.references()['L001']
        self.assertEqual(c.coverage(ref, {})[0], 'não mencionada')
        line = dict(situacao=sourced('incluida'))
        self.assertEqual(c.coverage(ref, line)[0], 'coberta com quantidade diferente')

    def test_substituicao_nao_equivale_nem_precifica(self):
        result = self.result()
        row = next(r for r in result['matriz'] if r['linha'] == 'L051')
        self.assertEqual(row['substituicao'], 'sim')
        cost = next(r for r in result['custos'] if r['linha'] == 'L051')
        self.assertEqual(cost['categoria'], 'sem base')
        self.assertIsNone(result['resumo'][0]['pontuacao'])

    def test_divergencia_chapas_e_faixa_projeto(self):
        result = self.result()
        row = next(r for r in result['matriz'] if r['linha'] == 'L001')
        self.assertIn('divergência de chapas', row['alertas'])
        cost = next(r for r in result['custos'] if r['linha'] == 'L001')
        self.assertEqual((cost['minimo'], cost['maximo']), (Decimal('435.58'), Decimal('520')))
        self.assertIsNone(c.project_range(c.references()['L006']))  # 2100 não herda preço1850

    def test_prioridade_outra_proposta_mesmo_escopo(self):
        other = copy.deepcopy(self.proposals[0])
        other['fornecedor'] = 'F02'
        line = other['linhas']['L001']
        line.update(preco_unitario=sourced('600'), espessura_mm=sourced('18'), cor=sourced('Arenza'))
        self.proposals.append(other)
        cost = c.missing_cost('L001', c.references()['L001'], self.proposals[0], self.proposals, Decimal(1))
        self.assertEqual(cost[:3], (Decimal(600), Decimal(600), 'estimado com base em outra proposta'))
        other['campos']['escopo'] = sourced('etapa')
        self.assertEqual(c.missing_cost('L001', c.references()['L001'], self.proposals[0], self.proposals, Decimal(1))[2], 'estimado por referência do projeto')

    def test_cobertura_completa_da_referencia_e_lacunas(self):
        result = self.result()
        self.assertEqual(len(c.references()), 101)
        self.assertEqual(sum(r['grupo'] == 'lacuna_corte' for r in result['matriz']), 33)
        self.assertEqual(sum(r['grupo'] == 'lacuna_ferragem' for r in result['matriz']), 40)
        self.assertIsNone(result['resumo'][0]['equivalente_max'])

    def test_validacao_origem_e_ids(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'Ficticio.json'
            data = copy.deepcopy(self.proposals)
            data[0]['campos']['preco_total']['origem'] = ''
            c.dump(path, dict(rotulo='FICTÍCIO', propostas=data))
            with self.assertRaises(ValueError):
                c.load_proposals(path)

    def test_prazo_nao_confirma_mudanca(self):
        fields = {k: sourced(v) for k, v in dict(producao_dias='35', entrega_dias='7', montagem_dias='7', inicio_semana_chaves='2', calendario='corridos', gatilho_prazo='executivo').items()}
        self.assertEqual(c.schedule(fields)[0], 9)
        self.assertIn('atenção', c.schedule(fields)[1])
        fields['calendario'] = sourced('uteis')
        self.assertIsNone(c.schedule(fields)[0])


if __name__ == '__main__':
    unittest.main()
