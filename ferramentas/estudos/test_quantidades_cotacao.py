"""Conferências de unidades, cobertura, duplicação, proteção de respostas e ZIP."""
import collections
import csv
import io
from pathlib import Path
import posixpath
import re
import unittest
from urllib.parse import unquote, urlsplit
import zipfile

import consolidar_quantidades_cotacao as q
import gerar_pedidos_cotacao as pack


def bad_links(archive):
    """Resolve arquivos internos do ZIP; não consulta links externos."""
    names=set(archive.namelist());bad=[]
    for name in sorted(names):
        if not name.endswith('.html'):continue
        text=archive.read(name).decode('utf-8')
        for href in re.findall(r'(?:href|src)=["\']([^"\']+)',text):
            url=urlsplit(href)
            if url.scheme or url.netloc or not url.path:continue
            target=posixpath.normpath(posixpath.join(posixpath.dirname(name),unquote(url.path)))
            if target not in names:bad.append((name,href))
    return bad


class Quantities(unittest.TestCase):
    def test_inventory_and_current_drawer_scope(self):
        rows=q.current_rows()
        self.assertEqual(sum(int(r['quantidade']) for r in rows if r['grupo']=='paineis'),251)
        rails=[r for r in rows if r['item'].startswith('Corrediças laterais')]
        self.assertEqual({r['movel']:r['quantidade'] for r in rails},{'P01':4,'P06':3,'P16':2})
        self.assertTrue(all('500 mm' in r['item'] for r in rails if r['movel']!='P16'))
        self.assertIn('400 mm',next(r['item'] for r in rails if r['movel']=='P16'))
        self.assertTrue(all(r['quantidade']=='' for r in rows if r['grupo']=='pendencia'))
        self.assertTrue(all(r['grupo'] not in ('chapas','fita') for r in rows))
        for r in rows:
            self.assertTrue((q.ROOT/r['fonte']).is_file(),r['fonte'])
        serialized=str(rows)
        self.assertNotIn('MOVENTO',serialized)
        self.assertNotIn('FGVTN',serialized)

    def test_csv_matches_current_sources(self):
        expected=io.StringIO(newline='')
        writer=csv.DictWriter(expected,fieldnames=q.FIELDS,delimiter=';')
        writer.writeheader();writer.writerows(q.current_rows())
        self.assertEqual(q.CSV.read_text(encoding='utf-8-sig'),expected.getvalue().replace('\r\n','\n'))


class Package(unittest.TestCase):
    def test_form_idempotent_services_once(self):
        old=[dict(zip(pack.FORM_FIELDS,['P01','Roupeiro','']+['']*9))]
        once=pack.form_rows(old)
        repeated=[dict(zip(pack.FORM_FIELDS,r)) for r in once+once[-7:]+once[-7:]]
        self.assertEqual(pack.form_rows(repeated),once)
        ids=collections.Counter(r[0] for r in once)
        self.assertTrue(all(v==1 for v in ids.values()))

    def test_protects_response_and_duplicate_module(self):
        row=dict(zip(pack.FORM_FIELDS,['P01','Roupeiro','']+['']*9))
        with self.assertRaises(ValueError):pack.form_rows([row,row])
        row[pack.FORM_FIELDS[3]]='1000'
        with self.assertRaises(ValueError):pack.form_rows([row])

    def test_zip_crc_links_sources_and_scope(self):
        pack.require_unsent()
        with zipfile.ZipFile(pack.OUT/'Marcenaria.zip') as z:
            self.assertIsNone(z.testzip())
            self.assertEqual(bad_links(z),[])
            self.assertEqual(z.read('Quantidades_referencia.csv'),q.CSV.read_bytes())
            text=z.read('Pedido.html').decode('utf-8')
            self.assertIn('A combinar no envio',text)
            self.assertNotIn('30/10/2026, às 18h',text)
            self.assertIn('ESTIMATIVA NOMINAL',text)
            self.assertIn('251 painéis',text)
            self.assertIn('7 pares de 500 mm',text)
            self.assertIn('2 pares de 400 mm',text)
            self.assertNotIn('MOVENTO',text)
            self.assertNotIn('FGVTN',text)
            self.assertIn('12 Minifix documentais versus 8 no mapa',text)
            for forbidden in ['35.000','37.000','46.500','137.748','120.000','2290','2.290','VG27AQ5A']:
                self.assertNotIn(forbidden,text)
            for name in z.namelist():
                if name.startswith('Fichas_R15/'):
                    self.assertEqual(z.read(name),(q.ROOT/'06_Entregas/Fichas_fabricacao'/name.split('/',1)[1]).read_bytes())
            form=list(csv.DictReader(io.StringIO(z.read('Formulario_resposta.csv').decode('utf-8-sig')),delimiter=';'))
            self.assertEqual(len(form),33)
            self.assertEqual(len({r['ID'] for r in form}),33)
        with zipfile.ZipFile(pack.OUT/'Pacote_cotacao.zip') as z:
            self.assertIsNone(z.testzip())
            self.assertEqual(bad_links(z),[])
            self.assertEqual(z.read('Marcenaria.zip'),(pack.OUT/'Marcenaria.zip').read_bytes())
            for name in z.namelist():
                if name.endswith('.html'):
                    page=z.read(name).decode('utf-8')
                    self.assertIn('combinar no envio',page)
                    self.assertNotIn('30/10/2026, às 18h',page)


if __name__=='__main__':unittest.main()
