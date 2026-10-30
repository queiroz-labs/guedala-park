"""Índice offline gerado das escolhas, módulos, documentos e dados de consulta."""
import json,re,unicodedata
from build_architect_data import HERE,literal


def words(text):
    folded=''.join(c for c in unicodedata.normalize('NFD',text.lower()) if not unicodedata.combining(c))
    return ' '.join(dict.fromkeys(re.findall(r'[a-z0-9]+',folded)))


def build(data):
    rows=[]
    def add(kind,title,tab,id,room='all',terms='',**extra):
        rows.append(dict(key=kind+':'+id,kind=kind,title=title,tab=tab,id=id,room=room,tokens=words(title+' '+terms),**extra))
    for r in data['disciplines']+data['itemResponsibilities']:
        add('pending',r['title'],'architect',r['id'],r.get('room','all'),r['text']+' '+' '.join(r['owners']),item=r.get('item'))
    for r in literal(HERE/'src/data.js','ITEMS'):
        add('choice',r['name'],'decisions',r['id'],r['room'],r.get('notes','')+' '+r.get('dimensions',''))
    for r in literal(HERE/'src/data.js','PROJECT')['rooms']:
        add('room',r['name'],'model',r['id'],r['id'],r.get('sub',''))
    for r in literal(HERE/'src/cad-data.js','CAD_DATA')['modules']:
        add('module',r['code']+' · '+r['name'],'model',r['code'],r['room'],r.get('item',''))
    for r in literal(HERE/'src/workshop-docs.js','WORKSHOP_DOCS'):
        if not r.get('internal') and r.get('path'):
            add('document',r['title'],'documents',r['id'],r['rooms'][0] if len(r['rooms'])==1 else 'all',r.get('summary','')+' '+r.get('searchTerms',''))
    for r in data.get('glossary',[]):add('glossary',r['term'],'architect',r['id'],terms=r['definition'])
    assert len({r['key'] for r in rows})==len(rows)
    content='// Gerado por build_search_index.py; palavras únicas, sem duplicar textos longos.\nglobalThis.GUEDALA_SEARCH_INDEX='+json.dumps(rows,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')+';\n'
    target=HERE/'src/search-data.js'
    if not target.exists() or target.read_text(encoding='utf-8')!=content:target.write_text(content,encoding='utf-8',newline='\n')
    return rows
