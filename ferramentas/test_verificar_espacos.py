"""Regressão curta: detecção, texto literal e exceções locais."""
import unittest
import contextlib
import io
import json
import tempfile
from pathlib import Path
from unittest.mock import patch
from verificar_espacos import main, ocorrencias


class EspacosTest(unittest.TestCase):
    def test_detecta_erros_no_contexto(self):
        texto = 'comC01 e noP03\nP04:4acessosSW4; 765equilíbrios e revisãoR52'
        achados = ocorrencias(texto)
        self.assertEqual(len(achados), 5)
        self.assertEqual(achados[0], (1, 3, 'mC01'))
        self.assertEqual(achados[-1][0], 2)

    def test_preserva_nomes_codigos_links_e_citacoes(self):
        texto = ('BrancoTX SceneSwitch KE4GC MOVENTO FGVTN SW4 R52 P04 '
                 '173H7100 71B3550 4 acessos com C01\n'
                 '`comC01` [referência](pasta/noP03.md) “4acessos” "noP03"\n'
                 '```python\ncomC01\n```')
        self.assertEqual(ocorrencias(texto), [])

    def test_excecao_nao_esconde_outro_erro(self):
        exc = [{'arquivo': 'a.md', 'trecho': 'objetoP03', 'motivo': 'Identificador literal'}]
        self.assertEqual(len(ocorrencias('objetoP03 noP03', 'a.md', exc)), 1)
        self.assertEqual(len(ocorrencias('objetoP03', 'b.md', exc)), 1)

    def test_aviso_e_bloqueio_sao_distintos(self):
        with tempfile.TemporaryDirectory() as pasta:
            raiz = Path(pasta)
            (raiz / 'a.md').write_text('noP03', encoding='utf-8')
            config = raiz / 'excecoes.json'
            config.write_text(json.dumps({'corrigidos': ['a.md'], 'excecoes': []}), encoding='utf-8')
            args = ['--excecoes', str(config), 'a.md']
            with patch('verificar_espacos.RAIZ', raiz), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(main(args), 0)
                self.assertEqual(main(args + ['--bloquear-corrigidos']), 1)
                self.assertEqual(main(args + ['--bloquear']), 1)


if __name__ == '__main__':
    unittest.main()
