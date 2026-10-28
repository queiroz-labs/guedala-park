import json
import unittest
from reconciliar_documentos_dimensionais import AREA, ROOT, GAPS, PANELS, compare, load_js, world_bbox


class ReconciliationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old = {p['name']:p for p in json.loads((AREA/'Inventario/Solidos_finitos_ativos_R44.json').read_text(encoding='utf-8'))}
        cls.cad = load_js(ROOT/'ferramentas/site/src/cad-data.js', 'CAD_DATA')
        cls.parts = {p['source']:p for p in cls.cad['parts']}

    def test_coordinate_transform(self):
        self.assertEqual(world_bbox(dict(x=1,y=0,z=337.2,w=1.8,h=213.2,d=56.8)), [7372,3372,0,7390,3940,2132])

    def test_known_change_is_detected(self):
        rows = compare(self.old, list(self.parts.values()))
        self.assertIn(['P09','Peca320','Y','dimensão',118.0,312.0,194.0], rows)
        self.assertIn(['P16','GavetaComumR084','Z','dimensão',80.0,74.0,-6.0], rows)

    def test_all_cited_ids_exist(self):
        keys = [k for values in PANELS.values() for k in values]
        keys += [k for _,_,hi,_,lo,_ in GAPS for k in (hi,lo)]
        for key in keys:
            self.assertIn(key,self.old)
            self.assertIn(key,self.parts)

    def test_bank_position_is_unchanged_not_only_dimensions(self):
        for key in PANELS['P20']:
            for old,new in zip(self.old[key]['bbox'],world_bbox(self.parts[key])):
                self.assertAlmostEqual(old,new,places=5)


if __name__ == '__main__':
    unittest.main()
