"""Testes de precedência e mínimo exato; não são validação física."""
import itertools
import unittest

from sequenciar_furacao import build_graph, order_or_cycle, minimum_relaxation


class SequenciaTests(unittest.TestCase):
    def assert_order(self, nodes, edges, order, removed=()):
        self.assertEqual(set(order), set(nodes))
        self.assertEqual(len(order), len(nodes))
        rank = {n: i for i, n in enumerate(order)}
        for a, b, label in edges:
            if label not in removed or not label:
                self.assertLess(rank[a], rank[b])

    def test_both_panels_before_tightening_before_blocker(self):
        holes = [dict(tipo='Minifix corpo', grupo='G1', peca='A'),
                 dict(tipo='Minifix pino', grupo='G1', peca='B')]
        nodes, edges = build_graph({'A', 'B', 'C'}, holes,
                                  [dict(grupo='G1', antes_de_instalar='C')])
        order, cycle = order_or_cycle(nodes, edges)
        self.assertIsNone(cycle)
        self.assert_order(nodes, edges, order)
        self.assertEqual(order[-1], 'instalar:C')
        self.assertEqual(minimum_relaxation(nodes, edges)[0], [])

    def test_reject_incomplete_pair(self):
        with self.assertRaises(ValueError):
            build_graph({'A'}, [dict(tipo='Minifix', grupo='G1', peca='A')], [])

    def test_two_independent_cycles_need_two_changes(self):
        nodes = {'a', 'b', 'c', 'd'}
        edges = [('a', 'b', ''), ('b', 'a', 'x'),
                 ('c', 'd', ''), ('d', 'c', 'y')]
        changed, order, _ = minimum_relaxation(nodes, edges)
        self.assertEqual(changed, ['x', 'y'])
        self.assert_order(nodes, edges, order, changed)

    def test_one_shared_label_breaks_two_cycles(self):
        edges = [('a', 'b', ''), ('b', 'a', 'x'),
                 ('c', 'd', ''), ('d', 'c', 'x')]
        changed, order, _ = minimum_relaxation(set('abcd'), edges)
        self.assertEqual(changed, ['x'])
        self.assert_order(set('abcd'), edges, order, changed)

    def test_unremovable_cycle(self):
        self.assertIsNone(minimum_relaxation({'a', 'b'},
            [('a', 'b', ''), ('b', 'a', '')])[0])

    def test_exact_search_matches_exhaustive_small_graphs(self):
        # Independent exhaustive oracle: enumerate every allowed replacement set.
        nodes = set('abc')
        possible = [('a', 'b', ''), ('b', 'c', ''), ('c', 'a', 'x'),
                    ('b', 'a', 'y'), ('c', 'b', 'z'), ('a', 'c', 'x')]
        for mask in range(1 << len(possible)):
            edges = [e for i, e in enumerate(possible) if mask & (1 << i)]
            optimum = None
            for size in range(4):
                if any(order_or_cycle(nodes, edges, set(choice))[1] is None
                       for choice in itertools.combinations('xyz', size)):
                    optimum = size
                    break
            changed, order, _ = minimum_relaxation(nodes, edges)
            self.assertEqual(None if changed is None else len(changed), optimum)
            if order is not None:
                self.assert_order(nodes, edges, order, changed)
            self.assertEqual(minimum_relaxation(nodes, edges)[0], changed)


if __name__ == '__main__':
    unittest.main()
