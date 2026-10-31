"""Travas de exclusoes planejadas: prova integra e excecao so no candidato."""
import ast
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile
from unittest.mock import patch

SOURCE = Path(__file__).resolve().parents[1] / 'verificar_modelo/verificar_modelo.py'
TREE = ast.parse(SOURCE.read_text(encoding='utf-8'))


def load(name, scope):
    node = next(n for n in TREE.body if isinstance(n, ast.FunctionDef) and n.name == name)
    exec(compile(ast.Module(body=[node], type_ignores=[]), str(SOURCE), 'exec'), scope)
    return scope[name]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, value):
    path.write_text(json.dumps(value), encoding='utf-8')


class RemovalPlan(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='gp-plano-')
        self.addCleanup(self.tmp.cleanup)
        self.folder = Path(self.tmp.name)
        self.repo = self.folder / 'repo'
        (self.repo / 'ferramentas/estudos').mkdir(parents=True)
        script = self.repo / 'ferramentas/estudos/auditar_remocoes_freecad.py'
        script.write_text('# fixture', encoding='utf-8')
        self.source, self.target = self.folder / 'origem.FCStd', self.folder / 'estudo.FCStd'
        for file, names in [(self.source, ['Atual', 'Descartavel']), (self.target, ['Atual'])]:
            self.fcstd(file, names)
        proof = dict(Name='Descartavel', decisao='remocao_provada', expressoes_proprias=0,
                     uso_intrinseco=[], aliases_verificados_para_exclusao=True, referencias={})
        inventory = dict(erros_cobertura=[], remocoes_provadas=['Descartavel'])
        files = [('Inventario_antes.json', 'inventario_sha256', inventory),
                 ('Inventario_candidatos.csv', 'inventario_csv_sha256', []),
                 ('Corpus_conferido.json', 'corpus_sha256', []),
                 ('Dependencias_runtime.json', 'runtime_sha256', {})]
        self.plan = dict(schema=2, modelo_origem=str(self.source), modelo_sha256=sha(self.source),
                         repositorio_auditado=str(self.repo), script_sha256=sha(script),
                         remover=['Descartavel'], provas=[proof])
        for name, field, value in files:
            write(self.folder / name, value)
            self.plan[field] = sha(self.folder / name)
        self.path = self.folder / 'Plano_remocoes.json'
        self.validate = load('conferir_plano', dict(Path=Path, json=json, sha=sha, zipfile=zipfile, RAIZ=self.repo))

    def fcstd(self, file, names):
        with zipfile.ZipFile(file, 'w') as z:
            z.writestr('Document.xml', '<Document><Objects>' + ''.join('<Object name="%s"/>' % n for n in names) + '</Objects></Document>')

    def run_plan(self):
        write(self.path, self.plan)
        return self.validate(self.path, self.target, {'regras': []})

    def test_exact_removals(self):
        self.assertEqual(self.run_plan(), frozenset(['Descartavel']))
        self.fcstd(self.target, [])
        with self.assertRaises(ValueError): self.run_plan()

    def test_tampered_inventory_or_source(self):
        (self.folder / 'Inventario_antes.json').write_text('{}', encoding='utf-8')
        with self.assertRaises(ValueError): self.run_plan()

    def test_remaining_reference_and_missing_proof(self):
        self.plan['provas'][0]['referencias'] = {'movimentos': {'contagem': 1}}
        with self.assertRaises(ValueError): self.run_plan()
        self.plan['provas'] = []
        with self.assertRaises(ValueError): self.run_plan()

    def test_source_must_be_separate(self):
        self.plan['modelo_origem'] = str(self.target)
        self.plan['modelo_sha256'] = sha(self.target)
        with self.assertRaises(ValueError): self.run_plan()

    def test_normal_comparison_still_rejects_removal(self):
        scope = dict(erros=[], avisos=[], SCHEMA=2)
        compare = load('comparar', scope)
        base = dict(objetos={'Descartavel': {}}, total_expressoes=0, invalidos=[])
        now = dict(objetos={}, total_expressoes=0, invalidos=[])
        compare(base, now, {})
        self.assertTrue(scope['erros'])
        scope['erros'].clear()
        compare(base, now, {}, frozenset(['Descartavel']))
        self.assertFalse(scope['erros'])

    def test_never_allows_base_write_or_skipping_movements(self):
        def forbidden(): raise AssertionError('nao deve chegar ao oficial')
        scope = dict(sys=sys, valor_arg=lambda _: None, rapido=forbidden)
        main = load('main', scope)
        for flags in [[], ['--candidato', 'x', '--completo', '--atualizar-base'],
                      ['--candidato', 'x', '--completo', '--sem-movimentos']]:
            with self.subTest(flags=flags), patch.object(sys, 'argv', ['check', '--plano-remocoes', 'p'] + flags):
                with self.assertRaises(SystemExit) as ex: main()
                self.assertEqual(ex.exception.code, 1)


if __name__ == '__main__': unittest.main()
