"""Apresentação pública; nunca altera os documentos de trabalho."""
import json
import re
from dataclasses import dataclass, field
from html import escape
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).resolve().parent
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'wbr'}
CODE = re.compile(r'\b(?:R\d{2,3}|P\d{2}|F\d{2,4}|SHA(?:256)?|[a-fA-F0-9]{40,64})\b')
PATH = re.compile(r'(?:[A-Za-z]:[\\/][^\s<>";,)]+|(?:\.{1,2}/)*(?:0[1-9]_[\w-]+|ferramentas|src)/[^\s<>";,)]+|[\w.-]+\.(?:py|cjs|mjs|ps1|FCStd|json)(?:\b))', re.I)
COMMAND = re.compile(r'(?:\b(?:python(?:3)?|node|npm|git|powershell|pwsh|FreeCADCmd)(?:\.exe)?\s+(?:-\S+|[\w./\\]+\.(?:py|cjs|mjs|ps1)|status\b|clone\b|add\b|commit\b|push\b|ci\b|run\b|install\b)|\s--[a-z][a-z-]*(?:\b)|[\w./\\-]+\.ps1\b)', re.I)


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


def public_html(content, path, title=None):
    """Limpa só a cópia publicada; atributos/URLs conservam destinos e âncoras."""
    tree = Tree(content).root
    main = next(tree.find('main'), None) or next(tree.find('body'), tree)
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
    if title:
        h1 = next(main.find('h1'), None)
        if h1:
            h1.children = [prose(title)]
        page_title = next(tree.find('title'), None)
        if page_title:
            page_title.children = [prose(title)]
    main.attrs['data-public-document'] = path
    if codes:
        main.children.append(Node('details', {'class': 'source-codes'}, [Node('summary', {}, ['Fonte e códigos']), Node('p', {}, ['Códigos de referência do documento: '+', '.join(codes)+'.'])]))
    return '<!doctype html>'+tree.html()
