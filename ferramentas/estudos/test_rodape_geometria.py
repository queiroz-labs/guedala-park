"""Vãos, dois lados de divisória e recortes: nenhuma medida existente muda."""
import unittest
import ast
import copy
import tempfile
import shutil
from pathlib import Path
from types import SimpleNamespace

MACRO = Path(__file__).with_name('modelar_rodape.FCMacro')
tree = ast.parse(MACRO.read_text(encoding='utf8'))
# Carrega só funções puras: o teste não importa FreeCAD, abre CAD ou executa main.
names = {'inside','merge','subtract','rect','wall_faces','strip_box','ensure_destination','apply_finish','copy_candidate'}
nodes = [n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names
         or isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in {'EPS','FLOORS'} for t in n.targets)]
scope = {'Path':Path,'defaultdict':__import__('collections').defaultdict,'shutil':shutil}
exec(compile(ast.Module(body=nodes,type_ignores=[]),str(MACRO),'exec'),scope)
FLOORS,merge,subtract,strip_box,wall_faces,ensure_destination,apply_finish = (scope[n] for n in ('FLOORS','merge','subtract','strip_box','wall_faces','ensure_destination','apply_finish'))
copy_candidate=scope['copy_candidate']


class RodapeGeometryTests(unittest.TestCase):
    def test_overlapping_cuts_and_disjoint_spans(self):
        self.assertEqual(subtract([(0, 1000)], [(100, 300), (200, 400), (800, 1200)]), [(0, 100), (400, 800)])
        self.assertEqual(subtract([(0, 100)], [(200, 300)]), [(0, 100)])
        self.assertEqual(subtract([(0, 100)], [(-20, 120)]), [])

    def test_thickness_grows_only_into_room(self):
        face = dict(axis='x', fixed=1000, sign=-1)
        self.assertEqual(strip_box(face, 100, 500, 15), [985, 100, 0, 1000, 500, 80])
        self.assertEqual(strip_box(face, 100, 500, 20), [980, 100, 0, 1000, 500, 80])

    def test_opening_and_lintel_do_not_gain_baseboard(self):
        objects = {n: {'caixa_global': [9000, 9000, -50, 9001, 9001, 0]} for ns in FLOORS.values() for n in ns}
        objects['Peca'] = {'caixa_global': [0, 0, -50, 1000, 1000, 0]}
        objects.update(A={'caixa_global': [0, -100, 0, 300, 0, 2600]},
                       B={'caixa_global': [700, -100, 0, 1000, 0, 2600]},
                       Verga={'caixa_global': [300, -100, 2050, 700, 0, 2600]})
        faces = wall_faces(objects, ['A', 'B', 'Verga'])
        self.assertEqual([(f['start'], f['end']) for f in faces], [(0, 300), (700, 1000)])
        self.assertTrue(all(f['room']=='quarto' for f in faces))

    def test_candidate_is_never_overwritten_or_created_inside_repository(self):
        with tempfile.TemporaryDirectory(prefix='gp-rodape-') as tmp:
            root=Path(tmp)/'repo';out=Path(tmp)/'externo'
            root.mkdir();out.mkdir();candidate=out/'ocupado.txt';candidate.write_text('outra sessão',encoding='utf8')
            with self.assertRaises(FileExistsError):ensure_destination(root,out,candidate)
            self.assertEqual(candidate.read_text(encoding='utf8'),'outra sessão')
            with self.assertRaises(ValueError):ensure_destination(root,root,root/'candidato.txt')
            ensure_destination(root,out,out/'livre.txt')

    def test_matte_material_is_assigned_back_to_the_view(self):
        class View:
            def __init__(self):self.saved=[SimpleNamespace(Shininess=90,SpecularColor=(1,1,1))]
            @property
            def ShapeAppearance(self):return copy.deepcopy(self.saved)
            @ShapeAppearance.setter
            def ShapeAppearance(self,value):self.saved=copy.deepcopy(value)
        view=View();apply_finish(view)
        self.assertEqual(view.saved[0].Shininess,5)
        self.assertEqual(view.saved[0].SpecularColor,(0,0,0))
        self.assertEqual(view.ShapeColor,(238/255,234/255,225/255))

    def test_exclusive_copy_protects_a_file_created_by_another_session(self):
        with tempfile.TemporaryDirectory(prefix='gp-rodape-copy-') as tmp:
            source=Path(tmp)/'origem.txt';source.write_bytes(b'fonte')
            target=Path(tmp)/'candidato.txt';target.write_bytes(b'outra sessao')
            with self.assertRaises(FileExistsError):copy_candidate(source,target)
            self.assertEqual(target.read_bytes(),b'outra sessao')

    def test_macro_starts_from_original_r54_without_floor_macro_dependency(self):
        source=MACRO.read_text(encoding='utf8')
        self.assertIn('Guedala_Park_R54_Berlin.FCStd',source)
        self.assertNotIn('modelar_pisos',source)
        self.assertNotIn('rodape_geometria import',source)


if __name__=='__main__':
    unittest.main()
