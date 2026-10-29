"""Tests of chronology and missing-data guards; synthetic times are not project data."""
import tempfile
import unittest
from pathlib import Path

import cronograma_risco as schedule


class ScheduleTests(unittest.TestCase):
    def test_cycle_and_missing_predecessor_fail(self):
        with self.assertRaisesRegex(ValueError, 'Ciclo'):
            schedule.topological([{'id': 'a', 'depends': ['b']}, {'id': 'b', 'depends': ['a']}])
        with self.assertRaisesRegex(ValueError, 'ausente'):
            schedule.topological([{'id': 'a', 'depends': ['missing']}])

    def test_missing_mode_is_not_silently_midpoint(self):
        nodes = [dict(id='a', depends=[], minimum=1, maximum=3, mode=None)]
        with self.assertRaisesRegex(ValueError, 'moda triangular'):
            schedule.simulate(nodes, 'a')

    def test_missing_duration_is_not_zero(self):
        with self.assertRaisesRegex(ValueError, 'duração a confirmar'):
            schedule.simulate([dict(id='a', depends=[])], 'a')

    def test_fixed_and_parallel_chain(self):
        nodes = [dict(id='start', depends=[], fixed=0),
                 dict(id='slow', depends=['start'], fixed=5),
                 dict(id='fast', depends=['start'], fixed=2),
                 dict(id='finish', depends=['slow', 'fast'], fixed=1)]
        r = schedule.simulate(nodes, 'finish')
        self.assertEqual(r['scenarios'], 5000)
        self.assertEqual((r['P50'], r['P80'], r['probability_by_week_8']), (6, 6, 1))
        self.assertEqual(r['critical_paths'][0]['path'], ['start', 'slow', 'finish'])

    def test_triangular_respects_source_triplet_and_is_repeatable(self):
        n = [dict(id='a', depends=[], minimum=1, mode=2, maximum=4)]
        a, b = schedule.simulate(n, 'a'), schedule.simulate(n, 'a')
        self.assertEqual(a, b)
        self.assertTrue(1 < a['P50'] < a['P80'] < 4)
        self.assertEqual(a['probability_by_week_8'], 1)

    def test_backward_dates_can_precede_keys(self):
        self.assertEqual(schedule.purchase_limit(2, 4), -2)
        self.assertEqual(schedule.purchase_limit(1, 2), -1)
        self.assertIsNone(schedule.purchase_limit(None, 3))
        self.assertAlmostEqual(schedule.purchase_limit(7, 10/7), 39/7)

    def test_real_source_is_blocked_not_probabilistic(self):
        nodes, purchases = schedule.source_model(schedule.SOURCE.read_text(encoding='utf-8'))
        self.assertEqual(len(schedule.topological(nodes)), 21)
        self.assertGreater(len(schedule.duration_errors(nodes)), 15)
        with self.assertRaises(ValueError):
            schedule.simulate(nodes, 'mudanca')
        self.assertTrue(all(p['mode_weeks'] is None for p in purchases))
        # The slot 1–2 is calendar timing, never a duration triangle 1/1.5/2.
        electrical = next(n for n in nodes if n['id'] == 'eletrica_hidraulica')
        self.assertIsNone(electrical['minimum'])

    def test_output_is_reproducible_without_mutating_source(self):
        before = schedule.SOURCE.read_bytes()
        with tempfile.TemporaryDirectory(prefix='gp_schedule_test_') as tmp:
            a = schedule.build(Path(tmp))
            b = schedule.build(Path(tmp))
            self.assertEqual(a, b)
        self.assertEqual(before, schedule.SOURCE.read_bytes())

    def test_current_network_adds_quote_and_supply_gates_without_dates(self):
        nodes, _, decisions = schedule.current_model(
            schedule.SOURCE.read_text(encoding='utf-8'),
            schedule.QUOTE.read_text(encoding='utf-8'),
            schedule.PROGRAM.read_text(encoding='utf-8'))
        self.assertEqual(len(schedule.topological(nodes)), 29)
        needed = {n['id'] for n in schedule.ancestors(nodes, 'inicio_fabricacao')}
        self.assertTrue({'envio_cotacao', 'retornos_cotacao', 'contratacao_marcenaria',
                         'abastecimento_ferragens', 'vistoria_medicao'} <= needed)
        self.assertEqual(len(decisions), 5)
        with self.assertRaisesRegex(ValueError, 'data de início'):
            schedule.simulate(nodes, 'mudanca')

    def test_unknown_milestone_probability_is_none_not_zero(self):
        rows = schedule.milestone_results([dict(id='x', depends=[])],
                [dict(id='m', terminal='x', deadline_week=8, target='8')])
        self.assertIsNone(rows[0]['probabilidade'])
        self.assertEqual(rows[0]['cenarios'], 0)

    def test_unrelated_unknown_branch_does_not_block_complete_milestone(self):
        nodes = [dict(id='a', depends=[], fixed=2), dict(id='unknown', depends=[])]
        rows = schedule.milestone_results(nodes, [dict(id='m', terminal='a', deadline_week=1, target='1')])
        self.assertEqual(rows[0]['probabilidade'], 0)
        self.assertEqual(rows[0]['cenarios'], 5000)

    def test_absolute_deadline_is_not_relative_week_zero(self):
        rows = schedule.milestone_results([dict(id='a', depends=[], fixed=0)],
                [dict(id='m', terminal='a', deadline_week=None, target='30/10 18h')])
        self.assertIsNone(rows[0]['probabilidade'])
        self.assertIn('ponte de calendário', rows[0]['lacunas'])

    def test_complete_durations_do_not_hide_missing_dependencies(self):
        with self.assertRaisesRegex(ValueError, 'predecessores ainda incompletos'):
            schedule.simulate([dict(id='m', depends=[], fixed=1, dependencies_complete=False)], 'm')

    def test_partial_sensitivity_does_not_claim_whole_project_gain(self):
        r = schedule.known_chain_sensitivity()
        self.assertIsNone(r['global_best_item'])
        self.assertEqual([x['ganho_na_cadeia_conhecida_semanas'] for x in r['sensitivity']], [1, 1])
        self.assertTrue(all(x['ganho_na_mudanca'] is None for x in r['sensitivity']))
        self.assertIsNone(r['largest_avoided_risk']['avoided_weeks_guaranteed'])


if __name__ == '__main__':
    unittest.main()
