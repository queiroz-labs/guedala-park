"""Apresentação pública; nunca altera os documentos de trabalho."""
import json
import re
from dataclasses import dataclass, field
from html import escape
from html.parser import HTMLParser
from pathlib import Path
import posixpath

HERE = Path(__file__).resolve().parent
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'wbr'}
PATTERNS = json.loads((HERE/'publicacao_documentos.json').read_text(encoding='utf-8'))['padroes']
CODE = re.compile(PATTERNS['codigos'])
PATH = re.compile(PATTERNS['caminhos'], re.I)
COMMAND = re.compile(PATTERNS['comandos'], re.I)
BASE_STYLE = 'body{font:16px/1.6 system-ui,sans-serif;color:#26322d;background:#faf9f5;max-width:1120px;margin:auto;padding:40px}h1{font-size:36px;line-height:1.15}h2{margin-top:40px}h3{margin-bottom:8px}a{color:#336d57}table{width:100%;border-collapse:collapse;font-size:14px}td,th{border-bottom:1px solid #d8dfd8;padding:10px;text-align:left;vertical-align:top}th{background:#e8eee7}section{padding:20px 0;border-bottom:1px solid #d8dfd8}.note{padding:18px;background:#edf1e9;border-radius:10px}.meta{font-size:13px;color:#607066}.tags{display:flex;gap:12px;flex-wrap:wrap}button{padding:10px 18px;border:1px solid #667767;border-radius:8px;background:white;cursor:pointer}ul,ol{padding-left:22px}ul.chk{list-style:none;padding-left:0}ul.chk li{margin:6px 0}ul.chk label{display:flex;gap:10px;align-items:flex-start;min-height:40px;padding:6px 4px;cursor:pointer}ul.chk input{width:22px;height:22px;flex:none;margin-top:2px}ul.chk input:checked+span{color:#7b867f;text-decoration:line-through}.tbl{overflow-x:auto}@media(max-width:640px){body{padding:16px}h1{font-size:28px}table{font-size:13px}td,th{padding:8px 6px}}@media print{body{background:white;padding:0;font-size:10pt}h1{font-size:24pt}.no-print{display:none}section{break-inside:avoid}a{color:inherit;text-decoration:none}table{font-size:9pt}h2,h3{break-after:avoid}}main p,main li,main dd{text-align:justify;text-justify:inter-word;hyphens:auto;-webkit-hyphens:auto;overflow-wrap:break-word}main table p,main table li,main .doc-crumbs{text-align:left;hyphens:manual}'
LIBRARY_STYLE = '.doc-library{max-width:960px}.doc-library h1{font:38px/1.15 Georgia,serif;text-wrap:balance}.doc-library h2{font:25px/1.2 Georgia,serif}.doc-library .eyebrow{font-size:11px;letter-spacing:1.4px;text-transform:uppercase;color:#66726c}.doc-library nav{display:flex;flex-wrap:wrap;gap:8px}.doc-library nav a{padding:9px 13px;border:1px solid #d8dfd8;border-radius:8px}.doc-library .doc-links{list-style:none;padding:0}.doc-library .doc-links li{padding:12px 0;border-bottom:1px solid #d8dfd8}.doc-library a{overflow-wrap:anywhere;text-underline-offset:4px}.doc-library details>summary{cursor:pointer;padding:12px 0;min-height:24px}.doc-library a:focus-visible,.doc-library summary:focus-visible{outline:2px solid #336d57;outline-offset:4px}.doc-library .doc-status{display:inline-block;font-size:12px;background:#edf1e9;padding:4px 10px;border-radius:20px}.doc-library section{scroll-margin-top:20px}.doc-library .doc-crumbs{font-size:14px;color:#66726c;margin-bottom:18px}@media(max-width:600px){body{padding:24px 18px}.doc-library h1{font-size:30px}}'
READ_STYLE = '''
.public-document{font:17px/1.6 system-ui,sans-serif;max-width:860px;margin:auto;overflow-wrap:anywhere}
.public-document h1{font-size:32px;line-height:1.2;text-wrap:balance}
.public-document h2{font-size:24px;line-height:1.3;margin:28px 0 12px}
.public-document .eyebrow,.public-document .meta,.public-document .doc-status{font-size:14px}
.public-document h3{font-size:20px;line-height:1.4}
.public-document p{max-width:65ch;margin:12px 0}
.public-document details{border-bottom:1px solid #d8dfd8;margin:16px 0;padding:0 0 8px}
.public-document summary{cursor:pointer;min-height:44px;box-sizing:border-box;padding:12px 0;line-height:1.5}
.public-document a{overflow-wrap:anywhere;min-height:44px;display:inline-flex;align-items:center}
.public-document button,.public-document select,.public-document input:not([type=checkbox]){min-height:44px;font-size:16px}
.public-document .reading-summary{padding:16px 20px;background:#edf1e9;border-radius:10px;margin:24px 0}
.public-document .reading-summary h2{margin:0;font-size:20px}
.public-document .reading-summary p{margin:8px 0;text-align:left}
.public-document table{font-size:16px;max-width:100%}
.public-document img,.public-document svg{max-width:100%;height:auto}
.public-document a:focus-visible,.public-document summary:focus-visible{outline:2px solid #336d57;outline-offset:4px}
.document-bar{display:flex;align-items:center;gap:16px;background:#faf9f5;border-bottom:1px solid #d8dfd8;padding:8px 16px;font:16px/1.5 system-ui,sans-serif}
.document-bar a{color:#336d57;min-height:44px;display:inline-flex;align-items:center;flex:none}
.document-bar span{font-size:14px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.public-document .doc-crumbs{font-size:14px;margin:16px 0;text-align:left}
@media(max-width:600px){
body:has(.public-document){padding:20px 16px}
body:has(.document-bar){padding-top:88px}
.document-bar{position:fixed;inset:0 0 auto;z-index:20;min-height:60px;box-sizing:border-box}
.public-document h1{font-size:28px}.public-document h2{font-size:23px}
.public-document .tbl{overflow:visible}
.public-document table[data-mobile-cards],.public-document table[data-mobile-cards] tbody{display:block;width:100%}
.public-document table[data-mobile-cards] tr{display:block;border:1px solid #d8dfd8;border-radius:8px;margin:12px 0;padding:8px;max-width:100%}
.public-document table[data-mobile-cards] .table-head{display:none}
.public-document table[data-mobile-cards] td{display:grid;grid-template-columns:minmax(0,1fr);width:auto;max-width:100%;padding:8px;border:0;font-size:16px;white-space:normal}
.public-document table[data-mobile-cards] td::before{content:attr(data-label);font-weight:600;font-size:14px;color:#607066}
}
@media print{.document-bar,.reading-summary,.related-links,.source-codes,.reading-details>summary{display:none}.reading-details::details-content{display:contents}.public-document{max-width:none}}
'''


def config():
    return json.loads((HERE/'publicacao_documentos.json').read_text(encoding='utf-8'))


def policy(path):
    return next((d for d in config()['documentos'] if d['path'] == path),
                dict(path=path, publico='tecnico', titulo_simples='', motivo='Documento vinculado; consulta técnica.'))


def publish_styles(target):
    target = Path(target)
    target.mkdir(parents=True, exist_ok=True)
    (target/'leitura.css').write_text(BASE_STYLE+'\n'+LIBRARY_STYLE+'\n'+READ_STYLE, encoding='utf8', newline='\n')


@dataclass
class Node:
    tag: str = ''
    attrs: dict = field(default_factory=dict)
    children: list = field(default_factory=list)

    def text(self):
        return ''.join(c.text() if isinstance(c, Node) else c for c in self.children)

    def html(self):
        content = ''.join(c.html() if isinstance(c, Node) else c if self.tag in {'script','style'} else escape(c, quote=False) for c in self.children)
        if not self.tag:
            return content
        attrs = ''.join(' '+k+('="'+escape(str(v), quote=True)+'"' if v is not None else '') for k, v in self.attrs.items())
        return '<'+self.tag+attrs+'>'+('' if self.tag in VOID else content+'</'+self.tag+'>')

    def find(self, tag):
        for child in self.children:
            if isinstance(child, Node):
                if child.tag == tag:
                    yield child
                yield from child.find(tag)


class Tree(HTMLParser):
    def __init__(self, html):
        super().__init__(convert_charrefs=True)
        self.root = Node()
        self.stack = [self.root]
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        node = Node(tag, dict(attrs))
        self.stack[-1].children.append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for i in range(len(self.stack)-1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        self.stack[-1].children.append(data)


def clean_markdown(text):
    """Retira cercas antes do conversor simples, inclusive cercas sem fechamento."""
    text = re.sub(r'<(?:pre|code)\b[^>]*>.*?</(?:pre|code)>', '', text, flags=re.S|re.I)
    out = []
    fence = None
    for line in text.splitlines():
        match = re.match(r'^\s*(`{3,}|~{3,})', line)
        if match:
            if fence is None:
                fence = match[1][0]
            elif match[1][0] == fence:
                fence = None
            continue
        if fence or COMMAND.search(line):
            continue
        out.append(line)
    return '\n'.join(out)


def slice_node(node, start, end):
    """Découpe par texte, en conservant liens, emphase et cases à cocher."""
    result = Node(node.tag, dict(node.attrs))
    offset = 0
    for child in node.children:
        length = len(child.text() if isinstance(child, Node) else child)
        if offset < end and offset+length > start:
            lo, hi = max(0, start-offset), min(length, end-offset)
            result.children.append(slice_node(child, lo, hi) if isinstance(child, Node) else child[lo:hi])
        offset += length
    return result


def short_paragraphs(node):
    children = []
    for child in node.children:
        if not isinstance(child, Node):
            children.append(child)
            continue
        if child.tag != 'p':
            short_paragraphs(child)
            children.append(child)
            continue
        text = child.text()
        starts = [0]+[m.end() for m in re.finditer(r'(?<=[.!?])\s+(?=[A-ZÀ-Ý0-9])', text)]+[len(text)]
        start = starts[0]
        for i in range(1, len(starts)):
            if i == len(starts)-1 or starts[i+1]-start > 230:
                children.append(slice_node(child, start, starts[i]))
                start = starts[i]
    node.children = children


def mobile_tables(main):
    for table in main.find('table'):
        table.attrs['data-mobile-cards'] = ''
        rows = list(table.find('tr'))
        if not rows:
            continue
        headers = [c.text().strip() for c in rows[0].children if isinstance(c, Node) and c.tag in {'td', 'th'}]
        has_header = any(isinstance(c, Node) and c.tag=='th' for c in rows[0].children)
        if has_header:
            rows[0].attrs['class'] = 'table-head'
        else:
            headers = ['Informação '+str(i+1) for i in range(len(headers))]
        for row in rows[1:] if has_header else rows:
            cells = [c for c in row.children if isinstance(c, Node) and c.tag in {'td', 'th'}]
            for i, cell in enumerate(cells):
                cell.attrs['data-label'] = headers[i] if i < len(headers) else 'Informação'


def add_summary(main):
    paragraphs = [p.text().strip() for p in main.find('p') if p.text().strip() and 'crumb' not in p.attrs.get('class', '')]
    # Extração literal: não há inferência de valores ou de decisões.
    sentences = [s.strip() for p in paragraphs for s in re.split(r'(?<=[.!?])\s+', p) if s.strip()]
    selected = []
    for sentence in sentences:
        if len(sentence) <= 180 and sentence not in selected:
            if selected and len(' '.join(selected+[sentence])) > 180:
                break
            selected.append(sentence)
            if len(selected) == 3:
                break
    if not selected:
        cells = [c.text().strip() for c in main.find('td') if c.text().strip()]
        selected = cells[:3]
    summary = Node('aside', {'class': 'reading-summary', 'aria-label': 'Em resumo'}, [Node('h2', {}, ['Em resumo']), Node('p', {}, [' '.join(selected)])])
    index = next((i+1 for i, c in enumerate(main.children) if isinstance(c, Node) and c.tag == 'h1'), 0)
    main.children.insert(index, summary)


def fold_sections(main, limits):
    """Agrupa por título; preserva a hierarquia e todos os valores do conteúdo."""
    first = True
    def words(node):
        if node.tag in {'details', 'nav'} or node.attrs.get('class')=='reading-summary':
            return 0
        return sum(words(c) if isinstance(c, Node) else len(c.split()) for c in node.children)
    def fold(container):
        nonlocal first
        for node in container.children:
            if isinstance(node, Node) and node.tag in {'section', 'div', 'article', 'aside'} and node.attrs.get('class')!='reading-summary':
                fold(node)
        groups = []
        group = []
        for node in container.children:
            if isinstance(node, Node) and node.tag in {'h2', 'h3'} and group:
                groups.append(group)
                group = []
            group.append(node)
        if group:
            groups.append(group)
        result = []
        for group in groups:
            nodes = [n for n in group if isinstance(n, Node)]
            count = sum(words(n) if isinstance(n, Node) else len(n.split()) for n in group if not isinstance(n, Node) or n.tag not in {'h1', 'h2', 'h3', 'details', 'nav'})
            large_list = any(len(list(n.find('li'))) > limits['itens_lista'] for n in nodes if n.tag in {'ul', 'ol'})
            if count > limits['palavras_recolher'] or large_list:
                fixed = [n for n in group if isinstance(n, Node) and (n.tag in {'h1', 'h2', 'h3', 'nav'} or n.attrs.get('class')=='reading-summary')]
                body = [n for n in group if n not in fixed]
                attrs = {'class': 'reading-details'}
                if first:
                    attrs['open'] = None
                    first = False
                result.extend(fixed+[Node('details', attrs, [Node('summary', {}, ['Ver detalhes'])]+body)])
            else:
                result.extend(group)
        container.children = result
    fold(main)
    ordered = [node for node in main.find('details') if node.attrs.get('class')=='reading-details']
    for node in ordered:
        node.attrs.pop('open', None)
    if ordered:
        ordered[0].attrs['open'] = None


def related_links(main, settings):
    links = {}
    def extract(node):
        children = []
        for child in node.children:
            if isinstance(child, Node):
                if child.tag == 'a' and child.attrs.get('href'):
                    links.setdefault(child.attrs['href'], child.text().strip() or 'Documento relacionado')
                    children.extend(child.children)
                    continue
                extract(child)
            children.append(child)
        node.children = children
    extract(main)
    readings = [d['path'] for d in settings['documentos'] if d['publico']=='leitura']
    def priority(item):
        url = item[0]
        return 0 if any(url.endswith(p) or url.endswith(p+'.html') for p in readings) else 2 if url.startswith('http') else 1
    rows = sorted(links.items(), key=priority)
    def items(rows):
        return Node('ul', {}, [Node('li', {}, [Node('a', {'href': href}, [label])]) for href, label in rows])
    if rows:
        main.children.append(Node('section', {'class': 'related-links'}, [Node('h2', {}, ['Relacionados']), items(rows[:5])]))
    return items(rows[5:]) if len(rows)>5 else None


def public_html(content, path, title=None):
    """Limpa só a cópia publicada; atributos/URLs conservam destinos e âncoras."""
    tree = Tree(content).root
    main = next(tree.find('main'), None) or next(tree.find('body'), None)
    if main is None:
        parent = next(tree.find('html'), tree)
        meta = [n for n in parent.children if isinstance(n, Node) and n.tag in {'head', 'meta', 'title', 'style', 'link'}]
        main = Node('main', {}, [n for n in parent.children if n not in meta])
        parent.children = meta+[main]
    settings = config()
    entry = policy(path)
    title = entry.get('titulo_simples') or title
    codes = []
    names = settings.get('moveis', {})

    def prose(text):
        text = text.replace('`', '')
        text = PATH.sub('', text)
        def replace(m):
            if m[0] not in codes:
                codes.append(m[0])
            return names.get(m[0], '')
        text = CODE.sub(replace, text)
        text = re.sub(r'[ \t]{2,}', ' ', text)
        return text

    def clean(node):
        children = []
        for child in node.children:
            if not isinstance(child, Node):
                children.append(prose(child))
                continue
            if child.tag in {'script', 'pre'}:
                continue
            if 'crumb' in child.attrs.get('class', ''):
                continue
            if child.tag in {'style', 'svg'}:
                children.append(child)
                continue
            if child.tag == 'code':
                if COMMAND.search(child.text()) or PATH.search(child.text()) or len(child.text()) > 100:
                    continue
                children.append(prose(child.text()))
                continue
            if child.tag in {'p', 'li'} and COMMAND.search(child.text()):
                continue
            if child.tag == 'a' and PATH.search(child.text()):
                href = child.attrs.get('href', '').split('#')[0]
                source = next((d for d in settings['documentos'] if href.endswith(d['path']) or href.endswith(d['path']+'.html')), None)
                child.children = [(source or {}).get('titulo_simples') or 'Documentação relacionada']
            clean(child)
            if child.tag not in {'p', 'li', 'h1', 'h2', 'h3', 'h4', 'a'} or child.text().strip() or list(child.find('img')):
                children.append(child)
        node.children = children

    clean(main)
    for style in tree.find('style'):
        style.children = [style.text().replace(BASE_STYLE, '').replace(LIBRARY_STYLE, '')]
    extra_links = related_links(main, settings) if settings['recursos']['relacionados'] else None
    if title:
        h1 = next(main.find('h1'), None)
        if h1:
            h1.children = [prose(title)]
        page_title = next(tree.find('title'), None)
        if page_title:
            page_title.children = [prose(title)]
    main.attrs['data-public-document'] = path
    main.attrs['class'] = (main.attrs.get('class', '')+' public-document').strip()
    if settings['recursos']['resumo']:
        short_paragraphs(main)
        add_summary(main)
        mobile_tables(main)
        parent = next(tree.find('head'), None) or next(tree.find('html'), tree)
        parent.children.insert(0, Node('link', {'rel': 'stylesheet', 'href': posixpath.relpath('leitura.css', posixpath.dirname(path))}))
    if settings['recursos']['recolher']:
        fold_sections(main, settings['limites'])
    if codes or extra_links:
        source = [Node('summary', {}, ['Fonte e códigos'])]
        if codes:
            source.append(Node('ul', {}, [Node('li', {}, [code]) for code in codes]))
        if extra_links:
            source.append(extra_links)
        main.children.append(Node('details', {'class': 'source-codes'}, source))
    if settings['recursos']['navegacao']:
        # O mesmo caminho é reescrito pelo pacote para o HTML autônomo.
        home = posixpath.relpath('index.html', posixpath.dirname('docs/'+path))
        section = 'Para ler' if entry['publico']=='leitura' else 'Arquivo técnico'
        main.children.insert(0, Node('p', {'class': 'doc-crumbs'}, [Node('a', {'href': home+'?aba=documentos'}, ['Documentos']), ' › '+section]))
        bar = Node('nav', {'class': 'document-bar', 'aria-label': 'Voltar'}, [Node('a', {'href': home}, ['← Voltar ao site']), Node('span', {}, [section])])
        main.children.insert(0, bar)
    return '<!doctype html>'+tree.html()
