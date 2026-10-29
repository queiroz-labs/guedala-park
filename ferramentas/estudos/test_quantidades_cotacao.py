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
    @classmethod
    def setUpClass(cls):
        cls.rows,cls.checks,cls.detail,cls.missing,cls.summary,_=q.consolidate()

    def test_coverage_and_units(self):
        s=self.summary
        self.assertEqual((s['paineis'],s['corte'],s['excluidos'],s['chapas']),(249,216,33,14))
        self.assertEqual(s['centros'],2286)
        self.assertEqual(sum(int(r['quantidade']) for r in self.rows if r['grupo']=='paineis'),249)
        self.assertEqual(len([r for r in self.rows if r['grupo']=='fita_sem_regra']),23)
        self.assertTrue(all(r['quantidade']=='' for r in self.rows if r['grupo']=='fita_sem_regra'))
        self.assertEqual(len({(r['movel'],r['peca']) for r in self.detail}),249)

    def test_loss_is_not_hidden_and_p19_not_decided(self):
        self.assertAlmostEqual(self.summary['fita_m'],191.136)
        self.assertAlmostEqual(self.summary['fita_com_perda_soma_cores_m'],210.2496)
        self.assertAlmostEqual(self.summary['fita_com_perda_soma_pecas_m'],210.2498)
        p19=next(r for r in self.checks if r['item']=='P19 Minifix mapa x documental')
        self.assertEqual((p19['valor_A'],p19['valor_B']),(8,12))
        self.assertEqual(p19['resultado'],'divergencia')
        hardware=[r for r in self.rows if r['grupo']=='ferragens' and r['item']=='Minifix 15']
        self.assertEqual(sum(float(r['quantidade']) for r in hardware),316)

    def test_mismatch_is_reported_not_suppressed(self):
        checks=[]
        q.checks_equal(checks,'alteração',12,8,'teste','causa')
        q.checks_equal(checks,'arredondamento',210.2498,210.2496,'teste','causa')
        self.assertTrue(all(r['resultado']=='divergencia' for r in checks))
        self.assertTrue(all('Não escolher' in r['acao'] for r in checks))

    def test_persisted_csv_is_reproducible(self):
        expected=io.StringIO(newline='')
        writer=csv.DictWriter(expected,fieldnames=q.FIELDS,delimiter=';')
        writer.writeheader();writer.writerows(self.rows)
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
            self.assertIn('30/10/2026, às 18h',text)
            self.assertIn('ESTIMATIVA NOMINAL',text)
            self.assertIn('33 excluídos',text)
            self.assertIn('316 no cenário do mapa versus 52 documentais; não somar',text)
            self.assertIn('12 documentais',text)
            for forbidden in ['35.000','37.000','46.500','137.748','120.000','2290','2.290','VG27AQ5A']:
                self.assertNotIn(forbidden,text)
            form=list(csv.DictReader(io.StringIO(z.read('Formulario_resposta.csv').decode('utf-8-sig')),delimiter=';'))
            self.assertEqual(len(form),33)
            self.assertEqual(len({r['ID'] for r in form}),33)
        with zipfile.ZipFile(pack.OUT/'Pacote_cotacao.zip') as z:
            self.assertIsNone(z.testzip())
            self.assertEqual(bad_links(z),[])
            self.assertEqual(z.read('Marcenaria.zip'),(pack.OUT/'Marcenaria.zip').read_bytes())


if __name__=='__main__':unittest.main()
