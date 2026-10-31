"""Travas do modo externo: proibir gravacao de base e exigir cores GUI."""
import ast
from pathlib import Path
import tempfile
import unittest
import zipfile

SOURCE=Path(__file__).resolve().parents[1]/'verificar_modelo/verificar_modelo.py'
tree=ast.parse(SOURCE.read_text(encoding='utf8'))
node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='validar_candidato')


class ReadOnlyCandidate(unittest.TestCase):
    def test_rejects_base_write_internal_path_and_missing_gui(self):
        with tempfile.TemporaryDirectory(prefix='gp-candidato-') as tmp:
            root=Path(tmp)/'repo';root.mkdir()
            scope=dict(Path=Path,zipfile=zipfile,RAIZ=root)
            exec(compile(ast.Module(body=[node],type_ignores=[]),str(SOURCE),'exec'),scope)
            validate=scope['validar_candidato']
            candidate=Path(tmp)/'candidato.FCStd'
            with zipfile.ZipFile(candidate,'w') as archive:
                archive.writestr('Document.xml','documento')
            with self.assertRaises(ValueError):validate(candidate,True,True)
            with self.assertRaises(ValueError):validate(candidate,False,False)
            with self.assertRaises(ValueError):validate(root/'modelo.FCStd',True,False)
            with self.assertRaises(ValueError):validate(candidate,True,False)
            with zipfile.ZipFile(candidate,'a') as archive:
                archive.writestr('GuiDocument.xml','cores')
            self.assertEqual(validate(candidate,True,False),candidate.resolve())


if __name__=='__main__':unittest.main()
