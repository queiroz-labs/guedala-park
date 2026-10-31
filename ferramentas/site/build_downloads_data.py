"""Downloads explícitos; bytes medidos nas fontes ou no artefato publicado."""
from pathlib import Path
from urllib.parse import urlsplit,unquote,quote
from html import escape
import argparse,json,posixpath,re,shutil,tempfile
from current_release import ROOT,STUDY,load_release


def selection():
    data=json.loads((STUDY/'downloads-source.json').read_text(encoding='utf-8'));release=load_release()
    for row in data['items']:
        if row.get('releasePath'):row['path']=release['packageDirectory']+'/'+release['packageFile']
        name=row['path'];path=Path(name)
        if path.is_absolute() or '..' in path.parts:raise ValueError('Download fora da raiz: '+name)
        if not row.get('releasePath') and not (ROOT/name).is_file():raise FileNotFoundError(name)
    assert len({r['id'] for r in data['items']})==len(data['items'])
    return data


def published_path(name):return name+'.html' if name.endswith('.md') else name


def publish(target,write_source=False):
    """Completa somente a seleção explícita; reutiliza documentos já exportados."""
    from build_workshop_docs import markdown,page
    target=Path(target);data=selection();paths=[r['path'] for r in data['items']]+data['support']
    mapping={p:published_path(p) for p in paths if (ROOT/p).is_file()}
    for name,dest_name in mapping.items():
        source=ROOT/name;dest=target/dest_name
        if dest.exists() and source.suffix!='.md':continue
        dest.parent.mkdir(parents=True,exist_ok=True)
        if source.suffix!='.md':shutil.copyfile(source,dest);continue
        from publication import clean_markdown,public_html
        content=page(source.stem,markdown(clean_markdown(source.read_text(encoding='utf-8'))))
        def link(m):
            attr,delimiter,url=m.group(1,2,3);parsed=urlsplit(unquote(url))
            if parsed.scheme or url.startswith('#'):return m[0]
            resolved=posixpath.normpath(posixpath.join(posixpath.dirname(name),parsed.path))
            final=mapping.get(resolved,published_path(resolved))
            if resolved in mapping or (target/final).exists():
                rel=quote(posixpath.relpath(final,posixpath.dirname(dest_name)),safe='/')
                return attr+'='+delimiter+rel+('#'+parsed.fragment if parsed.fragment else '')+delimiter
            return 'data-unpublished-reference='+delimiter+escape(url,quote=True)+delimiter
        content=re.sub(r'\b(href|src)\s*=\s*([\"\'])(.*?)\2',link,content)
        dest.write_text(public_html(content,name),encoding='utf-8',newline='\n')
    return build(target,write_source)


def build(published=None,write_source=True):
    if published is None:
        with tempfile.TemporaryDirectory(prefix='gp_downloads_') as folder:return publish(folder,write_source=True)
    data=selection();release=load_release();state=(ROOT/'ESTADO_ATUAL.md').read_text(encoding='utf-8');rows=[]
    for item in data['items']:
        row=dict(item);source=ROOT/row['path'];dest=Path(published)/published_path(row['path']) if published else source
        if not source.exists():continue  # R29 nasce depois de ensure_package, nunca se inventa um tamanho.
        rev=row.pop('revision')
        if 'release' in rev:revision=rev.get('prefix','')+release[rev['release']]
        elif 'path' in rev:
            revisions=set(re.findall(r'\bR\d+\b',(ROOT/rev['path']).read_text(encoding='utf-8')))
            assert len(revisions)==1,'Revisão ambígua: '+rev['path']
            revision=revisions.pop()
        elif 'state' in rev:
            line=next(line for line in state.splitlines() if line.startswith('| '+rev['state']+' |'))
            revision=re.search(r'\bR\d+\b',line)[0]
        else:revision=rev['label']
        numbered=re.search(r'_R\d+\.',source.name)
        if numbered and numbered[0][1:-1] not in revision:raise ValueError('Arquivo diverge da revisão vigente: '+row['path'])
        if not dest.is_file():raise FileNotFoundError('Download não publicado: '+str(dest))
        row.update(revision=revision,publishedPath=published_path(row['path']),sourceBytes=source.stat().st_size,bytes=dest.stat().st_size,
                   format='HTML' if row['path'].endswith('.md') and published else source.suffix[1:].upper())
        rows.append(row)
    content='// Gerado por build_downloads_data.py; tamanhos do arquivo real.\nglobalThis.GUEDALA_DOWNLOADS='+json.dumps(rows,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')+';\n'
    # Fora do HTML selado: o ZIP inclui esse HTML, mas não inclui o próprio tamanho.
    output=STUDY/'src/downloads-data.js' if write_source else Path(published).parent/'downloads-data.js'
    if not output.exists() or output.read_text(encoding='utf-8')!=content:output.write_text(content,encoding='utf-8',newline='\n')
    if published:
        manifest=dict(items=rows,files=[published_path(p) for p in [r['path'] for r in data['items']]+data['support'] if (ROOT/p).is_file()])
        (Path(published)/'downloads-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return rows


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--published-dir');a=parser.parse_args()
    print(json.dumps(dict(items=len(build(a.published_dir))),ensure_ascii=False))
