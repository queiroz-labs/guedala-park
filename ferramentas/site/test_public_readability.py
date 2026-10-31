"""Audita HTML publicado; --site aponta para o artefato, --baseline só mede.

Sem argumento, gera biblioteca, entrada e downloads em diretório temporário.
Não precisa de navegador, pacote novo ou biblioteca externa.
"""
import argparse
import contextlib
import io
import json
import re
import statistics
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).resolve().parent
SETTINGS = json.loads((HERE/'publicacao_documentos.json').read_text(encoding='utf8'))


class Audit(HTMLParser):
    def __init__(self, content):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.errors = set()
        self.links = self.body_links = self.words = self.section_words = 0
        self.max_section = self.max_paragraph = 0
        self.paragraph = None
        self.text = []
        self.visible_words = 0
        self.managed = False
        self.source = None
        self.feed(content)
        self.max_section = max(self.max_section, self.section_words)
        body = ' '.join(self.text)
        for key in ('comandos', 'caminhos'):
            if re.search(SETTINGS['padroes'][key], body, re.I):
                self.errors.add(key)
        limits = SETTINGS['limites']
        if self.max_paragraph > limits['caracteres_paragrafo']:
            self.errors.add('paragrafo')
        if self.max_section > limits['palavras_secao']:
            self.errors.add('secao')
        if self.body_links > limits['links_corpo']:
            self.errors.add('links')

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'data-public-document' in attrs:
            self.managed = True
            self.source = attrs['data-public-document']
        if tag in {'h1', 'h2', 'h3', 'h4', 'section', 'aside'}:
            self.max_section = max(self.max_section, self.section_words)
            self.section_words = 0
        if tag == 'a' and 'href' in attrs:
            self.links += 1
            if not any('source-codes' in a.get('class', '') for _, a in self.stack):
                self.body_links += 1
        if tag in {'pre', 'code'}:
            self.errors.add('codigo')
        if tag == 'p':
            self.paragraph = []
        if tag == 'table' and 'data-mobile-cards' not in attrs:
            self.errors.add('tabela')
        if tag not in {'meta', 'img', 'br', 'hr', 'input', 'link', 'wbr', 'source', 'col'}:
            self.stack.append((tag, attrs))

    def handle_endtag(self, tag):
        if tag=='aside':
            self.max_section = max(self.max_section, self.section_words)
            self.section_words = 0
        if tag == 'p' and self.paragraph is not None:
            self.max_paragraph = max(self.max_paragraph, len(' '.join(''.join(self.paragraph).split())))
            self.paragraph = None
        for i in range(len(self.stack)-1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        if any(t in {'script', 'style', 'title', 'svg'} for t, _ in self.stack):
            return
        if self.paragraph is not None:
            self.paragraph.append(data)
        if any('source-codes' in a.get('class', '') for _, a in self.stack):
            return
        self.text.append(data)
        count = len(data.split())
        self.words += count
        if not any(t == 'details' for t, _ in self.stack):
            self.section_words += count
        if not any(t == 'details' and 'open' not in a for t, a in self.stack):
            self.visible_words += count
        if re.search(SETTINGS['padroes']['codigos'], data):
            self.errors.add('codigos')


def scan(folder, baseline=False):
    rows = []
    candidates = [file for file in Path(folder).rglob('*') if file.is_file() and file.suffix in {'.html', '.md'}]
    for file in sorted(candidates):
        if file.suffix=='.md' and not file.read_bytes()[:80].lstrip().lower().startswith(b'<!doctype html'):
            continue
        audit = Audit(file.read_text(encoding='utf8'))
        if not baseline:
            if file.suffix!='.html':
                audit.errors.add('extensao')
            if not audit.managed:
                audit.errors.add('publicacao')
            if audit.source not in {d['path'] for d in SETTINGS['documentos']}:
                audit.errors.add('classificacao')
            elif next(d for d in SETTINGS['documentos'] if d['path']==audit.source)['publico']=='oculto':
                audit.errors.add('oculto')
        rows.append(dict(path=file.relative_to(folder).as_posix(), bytes=file.stat().st_size,
                         links=audit.links, links_corpo=audit.body_links,
                         palavras_abertas=audit.visible_words, paragrafo=audit.max_paragraph,
                         secao=audit.max_section, erros=sorted(audit.errors), gerado=audit.managed))
    if not rows:
        raise AssertionError('Nenhuma página encontrada')
    metrics = dict(paginas=len(rows), codigo_comando_caminho=sum(bool(set(r['erros']) & {'codigo', 'comandos', 'caminhos'}) for r in rows),
                   maiores_16kb=sum(r['bytes']>16384 for r in rows),
                   links_media=round(statistics.mean(r['links'] for r in rows), 2), links_max=max(r['links'] for r in rows),
                   links_corpo_media=round(statistics.mean(r['links_corpo'] for r in rows), 2), links_corpo_max=max(r['links_corpo'] for r in rows),
                   palavras_abertas_media=round(statistics.mean(r['palavras_abertas'] for r in rows), 1),
                   palavras_abertas_max=max(r['palavras_abertas'] for r in rows))
    failures = []
    exceptions = SETTINGS.get('excecoes', [])
    for row in rows:
        errors = set(row['erros'])
        for exception in exceptions:
            if exception['path'] == row['path']:
                assert exception['motivo'].strip(), 'Exceção sem motivo'
                errors -= set(exception['regras'])
        if errors and not baseline:
            failures.append((row['path'], sorted(errors), row['paragrafo'], row['secao'], row['links_corpo']))
    return dict(metricas=metrics, paginas=rows, falhas=failures)


class GuardTests(unittest.TestCase):
    def test_publisher_keeps_gallery_images_on_repeated_publication(self):
        from publication import public_html
        source = '<html><main><h1>Banheiro</h1><p><img src="../Banheiro_noite.png" alt="Banheiro atual"></p><p>Referência: <img src="outra.png" alt="Outra vista"> com luz acesa.</p></main></html>'
        for _ in range(2):
            source = public_html(source, '09_Referencias/Iluminacao_CB02/Galeria.md')
            self.assertEqual(source.count('<img '), 2)
            self.assertIn('src="../Banheiro_noite.png"', source)
            self.assertIn('alt="Banheiro atual"', source)
            self.assertIn('com luz acesa.', source)

    def test_adversarial_generated_html_is_rejected(self):
        bad = '<main><pre>python ferramentas/test.py --ci</pre><p>'+('palavra '*110)+'</p><section>'+('texto '*160)+'</section>'+('<a href="x">x</a>'*10)+'<table><tr><td>x</td></tr></table></main>'
        self.assertTrue({'codigo', 'comandos', 'caminhos', 'paragrafo', 'secao', 'links', 'tabela'} <= Audit(bad).errors)

    def test_collapsed_sections_and_source_codes_have_explicit_scope(self):
        text = '<main><p>Confira as medidas no local.</p><details><summary>Ver detalhes</summary>'+('texto '*200)+'</details><details class="source-codes"><summary>Fonte e códigos</summary><p>P11 R54</p></details></main>'
        self.assertFalse(Audit(text).errors)
        self.assertIn('codigos', Audit('<p>P11 R54</p>').errors)
        self.assertIn('comandos', Audit('<details><p>python -B teste.py</p></details>').errors)

    def test_publisher_preserves_values_and_does_not_mutate_source(self):
        from build_workshop_docs import markdown, page
        from publication import clean_markdown, public_html
        source = '# Cozinha\n\nMedida nominal de **127 V**, a conferir. Composição: 2 * 18 mm.\n\n```powershell\npython teste.py --ci\n```\n\n[07_Imovel/README.md](../../07_Imovel/README.md)\n\nP11 e R54; montagem pendente.\n'
        result = public_html(page('Cozinha', markdown(clean_markdown(source))), '03_Ambientes/Cozinha/README.md')
        audit = Audit(result)
        self.assertNotIn('comandos', audit.errors)
        self.assertNotIn('caminhos', audit.errors)
        self.assertNotIn('codigos', audit.errors)
        self.assertIn('127 V', result)
        self.assertIn('2 * 18 mm', result)
        self.assertIn('montagem pendente', result)
        self.assertIn('teste.py', source)
        self.assertIn('Fonte e códigos', result)

    def test_first_open_section_is_visible_and_table_keeps_its_values(self):
        from build_workshop_docs import markdown, page
        from publication import public_html, Tree
        source = '# Levantamento\n\n'+('Conferir as faces acabadas. '*90)+'\n\n| Item | Medida |\n|---|---|\n'+''.join('| Parede '+str(i)+' | 2300 mm |\n' for i in range(20))
        result = public_html(page('Levantamento', markdown(source)), '07_Imovel/Roteiro_dia_das_chaves_R01.md')
        tree = Tree(result).root
        details = [node for node in tree.find('details') if node.attrs.get('class')=='reading-details']
        self.assertIn('open', details[0].attrs)
        self.assertTrue(all('open' not in node.attrs for node in details[1:]))
        self.assertEqual(result.count('2300 mm'), 20)
        self.assertIn('data-label="Medida"', result)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--site', type=Path)
    parser.add_argument('--baseline', action='store_true')
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(GuardTests)
    if not unittest.TextTestRunner().run(suite).wasSuccessful():
        return 1
    def check(folder):
        result = scan(folder, args.baseline)
        if args.report:
            args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf8')
        print(json.dumps(result['metricas'], ensure_ascii=False))
        for failure in result['falhas'][:30]:
            print('ERRO:', failure)
        return bool(result['falhas'])
    if args.site:
        return check(args.site/'docs' if (args.site/'docs').is_dir() else args.site)
    from build_workshop_docs import build
    from build_architect_data import publish_docs
    from build_downloads_data import publish
    with tempfile.TemporaryDirectory(prefix='gp-reading-') as tmp:
        folder = Path(tmp)/'docs'
        with contextlib.redirect_stdout(io.StringIO()):
            build(target=folder)
            publish_docs(folder)
            publish(folder)
        return check(folder)


if __name__ == '__main__':
    raise SystemExit(main())
