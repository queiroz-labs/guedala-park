"""Cobertura dos 89 destinos, páginas geradas e navegação offline da biblioteca."""
import contextlib
import csv
import io
import json
import posixpath
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote,urlsplit
import build_workshop_docs as docs
from document_library import HOME,selected_sources
from build_work_data import document_paths as work_document_paths


class Links(HTMLParser):
    def __init__(self):super().__init__();self.links=[]
    def handle_starttag(self,tag,attrs):
        if tag=='a':self.links.extend(v for k,v in attrs if k=='href')


class DocumentLibraryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        docs.build(export_docs=False)

    def test_fifteen_visible_short_titles_and_complete_migration(self):
        visible=[d for d in docs.DOCS if d.get('publicSection')=='leitura']
        self.assertEqual(len(visible),20)
        self.assertTrue(all(d.get('path') for d in visible))
        for d in visible:self.assertNotRegex(d['title'],r'\b(?:R\d+|CB\d+|P\d\d|L\d+|T\d+)\b')
        with (docs.STUDY/'Documentos_antes_depois.csv').open(encoding='utf-8',newline='') as f:rows=list(csv.DictReader(f,delimiter=';'))
        self.assertEqual(len(rows),89);self.assertEqual(len({r['id'] for r in rows}),89)
        comparison = next(r for r in rows if r['id'] == 'comparacao-r54')
        self.assertTrue(comparison['depois'])
        path = next(d['path'] for d in docs.DOCS if d['id'] == 'comparacao-r54')
        self.assertIn(path, selected_sources(docs.RELEASE, docs.STUDY))
        self.assertTrue(all(r['depois'] for r in rows))
        self.assertEqual(sum(r['depois']=='oculto: histórico' for r in rows),9)

    def test_twenty_modules_keep_studies_and_all_panel_entries(self):
        html=docs.GENERATED_PAGES['biblioteca/moveis.html']
        self.assertEqual(html.count('<h3>Estudos deste móvel</h3>'),20)
        for code,f in docs.FABRICATION.items():
            self.assertIn('id="'+code+'"',html)
            self.assertIn(code+'-coordenadas.csv',html)
            for p in f['panels']:self.assertIn(p['id'],html)
        for did in ['p01-p03-ligacoes','p03-estudos','suspensao-p12','suspensao-p17','movento','espelheiro','banco','banco-atual']:
            path=next(d['path'] for d in docs.DOCS if d['id']==did)
            self.assertIn(path,selected_sources(docs.RELEASE,docs.STUDY))

    def test_exported_groups_have_no_dropped_or_missing_links(self):
        with tempfile.TemporaryDirectory(prefix='gp-library-') as tmp:
            target=Path(tmp)/'docs'
            with contextlib.redirect_stdout(io.StringIO()):docs.build(target=target)
            for source in work_document_paths():
                exported=target/(source+'.html')
                self.assertTrue(exported.is_file(),source)
                self.assertIn('<html',exported.read_text(encoding='utf-8'),source)
            for source in docs.GENERATED_PAGES:
                content=(target/source).read_text(encoding='utf-8')
                self.assertNotIn('data-unpublished-reference',content,source)
                links=Links();links.feed(content)
                for href in links.links:
                    parsed=urlsplit(unquote(href))
                    if href in {HOME,HOME.split('?')[0]} or not parsed.path:continue
                    file=target/posixpath.normpath(posixpath.join(posixpath.dirname(source),parsed.path))
                    self.assertTrue(file.is_file(),(source,href))
            sala=(target/'biblioteca/sala.html').read_text(encoding='utf-8')
            self.assertEqual(sala.count('Mesa_e_varal.md.html'),1)
            modelo=(target/'biblioteca/modelo.html').read_text(encoding='utf-8')
            self.assertEqual(modelo.count('.FCStd'),1)
            self.assertNotIn('Historico/',modelo)

    def test_sources_build_is_idempotent_and_keeps_placeholders_out(self):
        before=(docs.STUDY/'src/workshop-docs.js').read_bytes()
        docs.build(export_docs=False)
        self.assertEqual(before,(docs.STUDY/'src/workshop-docs.js').read_bytes())
        visible=[d for d in docs.DOCS if d.get('publicSection')=='leitura']
        self.assertTrue(all(d.get('path') for d in visible))


if __name__=='__main__':unittest.main()
