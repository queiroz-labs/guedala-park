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
CODE = re.compile(r'\b(?:R\d{2,3}|P\d{2}|F\d{2,4}|SHA(?:256)?|[a-fA-F0-9]{40,64})\b')
PATH = re.compile(r'(?:[A-Za-z]:[\\/][^\s<>";,)]+|(?:\.{1,2}/)*(?:0[1-9]_[\w-]+|ferramentas|src)/[^\s<>";,)]+|[\w.-]+\.(?:py|cjs|mjs|ps1|FCStd|json)(?:\b))', re.I)
COMMAND = re.compile(r'(?:\b(?:python(?:3)?|node|npm|git|powershell|pwsh|FreeCADCmd)(?:\.exe)?\s+(?:-\S+|[\w./\\]+\.(?:py|cjs|mjs|ps1)|status\b|clone\b|add\b|commit\b|push\b|ci\b|run\b|install\b)|\s--[a-z][a-z-]*(?:\b)|[\w./\\-]+\.ps1\b)', re.I)
READ_STYLE = '''
.public-document{font:17px/1.6 system-ui,sans-serif;max-width:860px;margin:auto;overflow-wrap:anywhere}
.public-document h1{font-size:32px;line-height:1.2;text-wrap:balance}
.public-document h2{font-size:24px;line-height:1.3;margin:28px 0 12px}
.public-document h3{font-size:20px;line-height:1.4}
.public-document p{max-width:65ch;margin:12px 0}
.public-document details{border-bottom:1px solid #d8dfd8;margin:16px 0;padding:0 0 8px}
.public-document summary{cursor:pointer;min-height:44px;box-sizing:border-box;padding:12px 0;line-height:1.5}
.public-document a{overflow-wrap:anywhere;min-height:44px;display:inline-flex;align-items:center}
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


@dataclass
class Node:
    tag: str = ''
    attrs: dict = field(default_factory=dict)
    children: list = field(default_factory=list)

    def text(self):
        return ''.join(c.text() if isinstance(c, Node) else c for c in self.children)

    def html(self):
        content = ''.join(c.html() if isinstance(c, Node) else escape(c, quote=False) for c in self.children)
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
        rows[0].attrs['class'] = 'table-head'
        for row in rows[1:]:
            cells = [c for c in row.children if isinstance(c, Node) and c.tag in {'td', 'th'}]
            for i, cell in enumerate(cells):
                cell.attrs['data-label'] = headers[i] if i < len(headers) else 'Informação'


def add_summary(main):
    paragraphs = [p.text().strip() for p in main.find('p') if p.text().strip() and 'crumb' not in p.attrs.get('class', '')]
    # Extração literal: não há inferência de valores ou de decisões.
    sentences = [s.strip() for p in paragraphs for s in re.split(r'(?<=[.!?])\s+', p) if s.strip()]
    selected = []
    for sentence in sentences:
        if len(sentence) <= 280 and sentence not in selected:
            if selected and len(' '.join(selected+[sentence])) > 360:
                break
            selected.append(sentence)
            if len(selected) == 3:
                break
    if not selected:
        cells = [c.text().strip() for c in main.find('td') if c.text().strip()]
        selected = cells[:3]
    summary = Node('aside', {'class': 'reading-summary', 'aria-label': 'Em resumo'}, [Node('h2', {}, ['Em resumo'])]+[Node('p', {}, [s]) for s in selected])
    index = next((i+1 for i, c in enumerate(main.children) if isinstance(c, Node) and c.tag == 'h1'), 0)
    main.children.insert(index, summary)


def fold_sections(main, limits):
    """Agrupa por título; preserva a hierarquia e todos os valores do conteúdo."""
    first = True
    def fold(container):
        nonlocal first
        for node in container.children:
            if isinstance(node, Node) and node.tag in {'section', 'div', 'article'}:
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
            words = sum(len(n.text().split()) for n in nodes if n.tag not in {'h1', 'h2', 'h3', 'aside', 'details', 'section', 'div', 'nav'})
            large_list = any(len(list(n.find('li'))) > limits['itens_lista'] for n in nodes if n.tag in {'ul', 'ol'})
            if words > limits['palavras_recolher'] or large_list:
                fixed = [n for n in group if isinstance(n, Node) and n.tag in {'h1', 'h2', 'h3', 'aside', 'nav'}]
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
        text = PATH.sub('', text)
        def replace(m):
            if m[0] not in codes:
                codes.append(m[0])
            return names.get(m[0], '')
        text = CODE.sub(replace, text)
        text = re.sub(r'[`*]+', '', text)
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
            if child.tag == 'style':
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
        style = next(tree.find('style'), None)
        if style:
            style.children.append(READ_STYLE)
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
