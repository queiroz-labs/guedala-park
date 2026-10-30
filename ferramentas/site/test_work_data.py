"""Contrato entre a tabela vigente e o acompanhamento local de obra."""
import json
import unittest
from pathlib import Path
from build_work_data import ROOT, SOURCE, data, display, parse, document_paths


class WorkDataTest(unittest.TestCase):
    def setUp(self):
        self.text = (ROOT / SOURCE).read_text(encoding='utf-8')
        self.rows = parse(self.text)

    def test_table_is_the_only_schedule(self):
        source = self.text.split('## 2.')[1].split('## 3.')[0]
        cells = [[c.strip() for c in line.strip().strip('|').split('|')]
                 for line in source.splitlines() if line.startswith('|')][2:]
        self.assertEqual(len(self.rows), 10)
        for row, original in zip(self.rows, cells):
            self.assertEqual([row['semana'], row['servico'], row['depende_de'], row['observacao']],
                             [display(c) for c in original])
        self.assertEqual(self.rows[-1]['depende_de'], '')  # Não inventar o fechamento da obra.
        self.assertEqual(self.rows[-2]['depende_de'], 'Fabricação')

    def test_changed_condition_does_not_inherit_done(self):
        changed = parse(self.text.replace('| Pintura de base |', '| Pintura de base e vistoria |'))
        self.assertNotEqual(changed[6]['id'], self.rows[6]['id'])
        self.assertEqual([r['id'] for i, r in enumerate(changed) if i != 6],
                         [r['id'] for i, r in enumerate(self.rows) if i != 6])

    def test_links_are_explicit_and_exist(self):
        for path in document_paths():
            self.assertTrue((ROOT / path).is_file(), path)
            self.assertNotIn('..', Path(path).parts)
        for row in self.rows:
            self.assertTrue(row['documentos'])
            for doc in row['documentos']:
                self.assertIn(doc['caminho'], document_paths())

    def test_generated_is_current(self):
        js = (ROOT / 'ferramentas/site/src/work-data.js').read_text(encoding='utf-8')
        generated = json.loads(js.split('globalThis.GUEDALA_WORK_PLAN=')[1].strip().rstrip(';'))
        self.assertEqual(generated, data())

    def test_week_ranges_and_invalid_source(self):
        self.assertEqual((self.rows[4]['inicio'], self.rows[4]['fim']), (2, 4))
        for old, new in [('| 2–4 |', '| 4–2 |'), ('| 0 |', '| a definir |'),
                         ('## 2. ', '## X. '), ('| Semana |', '| Data |')]:
            with self.assertRaises(ValueError):
                parse(self.text.replace(old, new))


if __name__ == '__main__':
    unittest.main()
