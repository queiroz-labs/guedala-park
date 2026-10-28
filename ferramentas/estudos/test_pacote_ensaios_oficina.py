"""Integridade da entrega de oficina; não executa ensaio físico."""
from pathlib import Path
from urllib.parse import unquote, urlsplit
import csv
import hashlib
import io
import json
import posixpath
import re
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT/'06_Entregas/Ensaios_oficina'


class PacoteOficina(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with zipfile.ZipFile(OUT/'Pacote_ensaios_oficina.zip') as z:
            assert z.testzip() is None
            cls.files = {n.removeprefix('Ensaios_oficina/'): z.read(n) for n in z.namelist()}
        cls.manifest = json.loads(cls.files['Manifesto.json'])

    def test_integridade_e_fontes(self):
        self.assertEqual(json.loads(self.files['Manifesto.json']), json.loads((OUT/'Manifesto.json').read_text(encoding='utf-8-sig')))
        self.assertEqual(set(self.files), {'Manifesto.json'} | {x['caminho'] for x in self.manifest['arquivos']})
        for item in self.manifest['arquivos']:
            b = self.files[item['caminho']]
            self.assertEqual(len(b), item['bytes'])
            self.assertEqual(hashlib.sha256(b).hexdigest(), item['sha256'])
        for name in self.manifest['fontes']:
            atual=(ROOT/name).read_bytes(); salvo=self.files['Fontes/'+name]
            if Path(name).suffix in {'.md','.csv','.txt','.json','.svg'}:
                atual=atual.replace(b'\r\n',b'\n');salvo=salvo.replace(b'\r\n',b'\n')
            self.assertEqual(atual,salvo,name)

    def test_registro_sem_resultados(self):
        rows=list(csv.DictReader(io.StringIO(self.files['Registro.csv'].decode('utf-8-sig')),delimiter=';'))
        self.assertEqual(len(rows),342)
        for row in rows:
            self.assertEqual(row['estado'],'pendente de execução')
            for key in list(row)[6:-1]: self.assertEqual(row[key],'',(row['medicao_id'],key))

    def test_navegacao_offline(self):
        for name,raw in self.files.items():
            self.assertNotIn('..',Path(name).parts)
            self.assertNotEqual(Path(name).suffix.lower(),'.fcstd')
            if not name.endswith('.html'):continue
            for url in re.findall(r'(?:href|src)="([^"]+)"',raw.decode('utf8')):
                part=urlsplit(unquote(url))
                if not part.scheme and part.path:
                    dest=posixpath.normpath(posixpath.join(posixpath.dirname(name),part.path))
                    self.assertIn(dest,self.files,(name,url))

    def test_pdf_e_apresentacao(self):
        self.assertEqual(self.files['Caderno_ensaios_oficina.pdf'],(OUT/'Caderno_ensaios_oficina.pdf').read_bytes())
        page=(OUT/'index.html').read_text(encoding='utf8')
        self.assertIn('Pendente de execução',page)
        self.assertIn('Pacote_ensaios_oficina.zip',page)
        self.assertNotRegex(page,r'ChatGPT|inteligência artificial|atualizad[oa]|alteramos|R28')


if __name__=='__main__': unittest.main()
