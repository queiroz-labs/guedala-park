"""Verifica links locais, imagens HTML e integridade dos binarios reorganizados.

Execute com Python 3, a partir de qualquer pasta. Nao acessa a internet.
"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[2]
SKIP = {'.git', '.agents', '.codex', '.claude', 'tmp'}


class References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in {'href', 'src'} and value:
                self.urls.append(value)
            if key == 'id':
                self.ids.add(value)


def check():
    errors = []
    links = documents = binaries = 0
    anchors = {}

    def ids_for(file):
        if file in anchors:
            return anchors[file]
        text = file.read_text(encoding='utf-8-sig')
        if file.suffix == '.html':
            parser = References()
            parser.feed(text)
            ids = parser.ids
        else:
            ids = set()
            for heading in re.findall(r'^#{1,6}\s+(.+?)\s*#*$', text, re.M):
                slug = re.sub(r'[^\w\- ]', '', heading.lower()).replace(' ', '-')
                unique, number = slug, 0
                while unique in ids:
                    number += 1
                    unique = f'{slug}-{number}'
                ids.add(unique)
        anchors[file] = ids
        return ids
    for file in ROOT.rglob('*'):
        if not file.is_file() or any(p in SKIP for p in file.relative_to(ROOT).parts):
            continue
        if file.suffix not in {'.md', '.html'}:
            continue
        documents += 1
        text = file.read_text(encoding='utf-8-sig')
        if file.suffix == '.html':
            parser = References()
            parser.feed(text)
            urls = parser.urls
        else:
            urls = re.findall(r'!?\[[^\]\n]*\]\(([^\n]*?)\)', text)
        for url in urls:
            url = url.strip('<>')
            if not url or re.match(r'^(?:[a-zA-Z][a-zA-Z0-9+.-]*:|//)', url):
                continue
            parts = urlsplit(url)
            target = (file.parent / unquote(parts.path)).resolve() if parts.path else file
            links += 1
            if not target.exists():
                errors.append(f'{file.relative_to(ROOT).as_posix()}: {url}')
            elif parts.fragment and target.is_file() and target.suffix in {'.md', '.html'}:
                if unquote(parts.fragment) not in ids_for(target):
                    errors.append(f'Ancora ausente em {file.relative_to(ROOT).as_posix()}: {url}')
    manifest = json.loads((ROOT/'99_Arquivo/Organizacao/Mapa_de_arquivos.json').read_text(encoding='utf-8'))
    text_types = {'.md', '.html', '.json', '.jsonl', '.txt', '.py', '.gitignore'}
    for entry in manifest:
        file = ROOT / entry['depois']
        if not file.is_file():
            errors.append(f'Arquivo ausente: {entry["depois"]}')
        elif file.suffix.lower() not in text_types and file.name != '.gitignore':
            binaries += 1
            if hashlib.sha256(file.read_bytes()).hexdigest() != entry['sha256_antes']:
                errors.append(f'Conteudo binario alterado: {entry["depois"]}')
    print(json.dumps({'documentos': documents, 'links_locais': links, 'binarios_preservados': binaries,
                      'erros': errors}, ensure_ascii=False, indent=2))
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(check())
