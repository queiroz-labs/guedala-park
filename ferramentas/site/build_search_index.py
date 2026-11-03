"""Índice offline gerado das escolhas, módulos, documentos e dados de consulta."""
import json,re,unicodedata
from build_architect_data import HERE,literal
from build_downloads_data import selection

# Também ajuda a localizar documentos e cômodos por vocabulário cotidiano.
CONCEPTS=[
    ('orcamento custos precos cotacao','orçamento custo preço cotação valores'),
    ('cronograma','prazos agenda calendário cronograma'),
    ('medidas dimensoes cotas dimensional','medida dimensão cota tamanho largura altura profundidade'),
    ('iluminacao luminarias luz','iluminação luminária luz lâmpada'),
    ('acabamentos pintura revestimentos','acabamento pintura tinta revestimento'),
    ('ferragens','ferragem dobradiça corrediça'),
    ('lavanderia','lavanderia área de serviço'),
    ('escritorio','escritório home office'),
    ('tv televisao televisor','tv televisão televisor'),
    ('geladeira refrigerador','geladeira refrigerador'),
    ('microondas','microondas micro ondas'),
    ('roupeiro','roupeiro guarda roupa'),
]

def words(text):
    folded=''.join(c for c in unicodedata.normalize('NFD',text.lower()) if not unicodedata.combining(c))
    return ' '.join(dict.fromkeys(re.findall(r'[a-z0-9]+',folded)))


def build(data):
    items=literal(HERE/'src/data.js','ITEMS')
    aliases=json.loads((HERE/'search_aliases.json').read_text(encoding='utf-8'))
    assert set(aliases)=={r['id'] for r in items},'Revisar nomes comuns dos itens da busca'
    item_names={r['id']:r['name']+' '+aliases[r['id']] for r in items}
    rooms={r['id']:r['name']+' '+r.get('sub','') for r in literal(HERE/'src/data.js','PROJECT')['rooms']}
    rows=[]
    def add(kind,title,tab,id,room='all',terms='',**extra):
        names=extra.pop('aliases','')
        seed=set(words(title+' '+names).split())
        names+=' '+' '.join(value for triggers,value in CONCEPTS if seed.intersection(triggers.split()))
        if names.strip():extra['aliases']=words(names)
        # Não repetir título e sinônimos no texto secundário do índice offline.
        primary=set(words(title+' '+names).split())
        tokens=' '.join(t for t in words(terms+' '+rooms.get(room,'')).split() if t not in primary)
        rows.append(dict(key=kind+':'+id,kind=kind,title=title,tab=tab,id=id,room=room,tokens=tokens,**extra))
    for r in data['disciplines']+data['itemResponsibilities']:
        add('pending',r['title'],'architect',r['id'],r.get('room','all'),r['text']+' '+' '.join(r['owners']),item=r.get('item'))
    for r in items:
        add('choice',r['name'],'decisions',r['id'],r['room'],r.get('notes','')+' '+r.get('dimensions',''),aliases=aliases[r['id']])
    for r in literal(HERE/'src/data.js','PROJECT')['rooms']:
        add('room',r['name'],'model',r['id'],r['id'],r.get('sub',''))
    for r in literal(HERE/'src/cad-data.js','CAD_DATA')['modules']:
        add('module',r['code']+' · '+r['name'],'model',r['code'],r['room'],r.get('item',''),aliases=item_names.get(r.get('item'),''))
    for r in literal(HERE/'src/workshop-docs.js','WORKSHOP_DOCS'):
        if not r.get('internal') and r.get('path'):
            add('document',r['title'],'documents',r['id'],r['rooms'][0] if len(r['rooms'])==1 else 'all',r.get('summary','')+' '+r.get('searchTerms',''))
    for r in data.get('glossary',[]):add('glossary',r['term'],'architect',r['id'],terms=r['definition'])
    for r in selection()['items']:add('download',r['title'],'documents',r['id'],terms=r['description']+' '+r['status']+' baixar download '+r['path'])
    assert len({r['key'] for r in rows})==len(rows)
    content='// Gerado por build_search_index.py; palavras únicas, sem duplicar textos longos.\nglobalThis.GUEDALA_SEARCH_INDEX='+json.dumps(rows,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')+';\n'
    target=HERE/'src/search-data.js'
    if not target.exists() or target.read_text(encoding='utf-8')!=content:target.write_text(content,encoding='utf-8',newline='\n')
    return rows
