"""Navegação por intenção; os documentos de origem e seus URLs são preservados."""
import csv
import io
import json
import posixpath
import re
from collections import defaultdict
from html import escape
from urllib.parse import quote

HOME='../../index.html?aba=documentos'
PUBLIC_IMOVEL={'07_Imovel/Medidas_e_impactos.csv','07_Imovel/Roteiro_dia_das_chaves_R01.md'}
STYLE='''.doc-library{max-width:960px}.doc-library h1{font:38px/1.15 Georgia,serif;text-wrap:balance}.doc-library h2{font:25px/1.2 Georgia,serif}.doc-library .eyebrow{font-size:11px;letter-spacing:1.4px;text-transform:uppercase;color:#66726c}.doc-library nav{display:flex;flex-wrap:wrap;gap:8px}.doc-library nav a{padding:9px 13px;border:1px solid #d8dfd8;border-radius:8px}.doc-library .doc-links{list-style:none;padding:0}.doc-library .doc-links li{padding:12px 0;border-bottom:1px solid #d8dfd8}.doc-library a{overflow-wrap:anywhere;text-underline-offset:4px}.doc-library details>summary{cursor:pointer;padding:12px 0;min-height:24px}.doc-library a:focus-visible,.doc-library summary:focus-visible{outline:2px solid #336d57;outline-offset:4px}.doc-library .doc-status{display:inline-block;font-size:12px;background:#edf1e9;padding:4px 10px;border-radius:20px}.doc-library section{scroll-margin-top:20px}.doc-library .doc-crumbs{font-size:14px;color:#66726c;margin-bottom:18px}@media(max-width:600px){body{padding:24px 18px}.doc-library h1{font-size:30px}}'''


def library_config(release):
    config=release['documentLibrary']
    if not 1<=len(config['cards'])<=15:raise ValueError('Biblioteca deve ter no máximo15 cartões')
    ids=[d['id'] for d in config['cards']]
    if len(ids)!=len(set(ids)):raise ValueError('Cartão duplicado')
    for d in config['cards']:
        if d['status'] not in {'Atual','Em estudo','Pendente'}:raise ValueError('Status de cartão inválido')
        if re.search(r'\b(?:R\d+|CB\d+|L\d+|T\d+|P\d\d)\b',d['title']):raise ValueError('Código interno no título')
    return config


def selected_ids(release):
    config=library_config(release);ids=set()
    for card in config['cards']:
        if card.get('direct'):ids.add(card['direct'])
        for section in card['sections']:ids.update(section['documents'])
    ids.update('ficha-'+code for code in config['moduleStudies'])
    for studies in config['moduleStudies'].values():ids.update(studies)
    return ids


def selected_sources(release,study):
    """A mesma seleção alimenta o pacote offline, sem incluir pastas por recursão."""
    text=(study/'src/workshop-docs.js').read_text(encoding='utf-8')
    docs=json.loads(re.search(r'const WORKSHOP_DOCS = (.*);\n',text)[1])
    selected=selected_ids(release)
    return list(dict.fromkeys(d['path'] for d in docs if d['id'] in selected and d['id']!='pacote-compartilhar' and d.get('path') and not d.get('generated')))


def configure(catalog,release,fabrication,root,page):
    config=library_config(release);original=list(catalog)
    catalog.extend(dict(d,category='Consulta',internal=True,available=(root/d['path']).is_file()) for d in config['extraDocuments'])
    byid={d['id']:d for d in catalog}
    if len(byid)!=len(catalog):raise ValueError('ID de documento duplicado')
    hidden=set(config['hiddenHistory']);used=selected_ids(release)
    if used&hidden:raise ValueError('Histórico incluído na biblioteca pública')
    if used-set(byid):raise ValueError('Documento desconhecido: '+str(sorted(used-set(byid))))
    for d in catalog:d['internal']=True
    labels=config.get('labels',{});pages={};destinations=defaultdict(list)
    def link(did,base,label=None):
        d=byid[did];label=label or labels.get(did,d['title'])
        if not d.get('path') or d.get('available') is False:return '<li>'+escape(label)+' — Pendente</li>'
        target=quote(posixpath.relpath(d['path'],posixpath.dirname(base)),safe='/#')
        return '<li><a href="'+target+'">'+escape(label)+'</a></li>'
    def wrap(title,body):
        return page(title,'<p class="doc-crumbs">Guedala Park › <a href="'+HOME+'">Documentos</a> › <span>'+escape(title)+'</span></p>'+body).replace('<main>','<main class="doc-library">',1).replace('</style>',STYLE+'</style>',1)
    for card in config['cards']:
        public={k:card[k] for k in ['id','title','category','status','summary','rooms']}
        direct=card.get('direct')
        if direct:
            public.update(path=byid[direct]['path'],available=True)
            destinations[direct].append(card['title'])
        else:
            path='biblioteca/'+card['id'].removeprefix('biblioteca-')+'.html'
            public.update(path=path,generated=True,available=True)
            body='<p class="eyebrow">'+escape(card['category'])+'</p><h1>'+escape(card['title'])+'</h1><p>'+escape(card['summary'])+'</p><span class="doc-status">'+escape(card['status'])+'</span>'
            for note in card.get('notes',[]):body+='<p class="note">'+escape(note)+'</p>'
            for section in card['sections']:
                seen=set();body+='<section><h2>'+escape(section['title'])+'</h2><ul class="doc-links">'
                for did in section['documents']:
                    destinations[did].append(card['title']+' → '+section['title'])
                    source=byid[did].get('path')
                    if source and source in seen:continue
                    seen.add(source);body+=link(did,path)
                body+='</ul></section>'
            if card.get('modules'):
                body+='<h2>Escolha um móvel</h2><nav aria-label="Móveis">'+''.join('<a href="#'+code+'">'+escape(f['name'])+'</a>' for code,f in fabrication.items())+'</nav>'
                assets=next(d['files'] for d in release['technicalDocuments'] if d['id']=='furacao-pecas')
                for code,f in fabrication.items():
                    destination=card['title']+' → '+code
                    destinations['ficha-'+code].append(destination)
                    body+='<section id="'+code+'"><h2>'+escape(f['name'])+'</h2><ul class="doc-links">'+link('ficha-'+code,path,'Abrir ficha completa')+'</ul><h3>Estudos deste móvel</h3><ul class="doc-links">'
                    for did in config['moduleStudies'][code]:
                        destinations[did].append(destination+' → Estudos deste móvel');body+=link(did,path)
                    body+='</ul><details><summary>Furação por peça</summary><p>Coordenadas nominais; conferir parâmetros, acesso e cobertura antes de fabricar.</p><ul class="doc-links">'
                    csvpath='04_Moveis/Furacao/'+code+'-coordenadas.csv'
                    body+='<li><a href="'+quote(posixpath.relpath(csvpath,posixpath.dirname(path)),safe='/')+'">Coordenadas deste móvel · CSV</a></li>'
                    drawings=defaultdict(list)
                    for asset in assets:
                        m=re.search('/'+code+r'-(.+)-(A|B|topo-[CL][01])\.svg$',asset)
                        if m:drawings[m[1]].append((m[2],asset))
                    for panel in f['panels']:
                        pid=panel['id'];body+='<li>'+escape(pid)+' · '+escape(panel.get('name',panel.get('label','Peça')))+': '
                        body+=' · '.join('<a href="'+quote(posixpath.relpath(asset,posixpath.dirname(path)),safe='/')+'">'+escape(face)+'</a>' for face,asset in drawings[pid]) or 'Sem centros mapeados; consultar pendências.'
                        body+='</li>'
                    body+='</ul></details></section>'
            pages[path]=wrap(card['title'],body)
            terms=[byid[d]['title']+' '+byid[d]['summary']+' '+d for s in card['sections'] for d in s['documents']]
            if card.get('modules'):terms.extend(f['name']+' '+code for code,f in fabrication.items());terms.extend(byid[d]['title']+' '+d for ds in config['moduleStudies'].values() for d in ds)
            public['searchTerms']=' '.join(terms)
        catalog.append(public)
    rows=[]
    for d in original:
        did=d['id']
        if did in hidden:destination='oculto: histórico'
        elif not d.get('path'):destination='Antes de fabricar → pendência incorporada; sem cartão ou link vazio'
        elif destinations[did]:destination=' / '.join(dict.fromkeys(destinations[did]))
        else:raise ValueError('Documento sem destino: '+did)
        rows.append(dict(id=did,antes=d['title'],depois=destination))
    stream=io.StringIO(newline='');writer=csv.DictWriter(stream,fieldnames=['id','antes','depois'],delimiter=';');writer.writeheader();writer.writerows(rows)
    return pages,stream.getvalue(),destinations
