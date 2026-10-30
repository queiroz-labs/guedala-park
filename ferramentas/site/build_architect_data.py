"""Entrada de consulta: fontes documentais existentes; somente biblioteca padrão."""
import csv,json,posixpath,re,shutil
from urllib.parse import urlsplit,unquote,quote
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]


def plain(text):
    return re.sub(r'[*`]', '',re.sub(r'\[([^]]+)\]\([^)]+\)',r'\1',text)).strip()


def literal(path,name):
    s=path.read_text(encoding='utf-8');start=re.search(r'const '+name+r'\s*=',s).end()
    return json.JSONDecoder().raw_decode(s[start:].lstrip())[0]


def responsibilities():
    items=literal(HERE/'src/data.js','ITEMS');cad=literal(HERE/'src/cad-data.js','CAD_DATA')
    with (ROOT/'07_Imovel/Medidas_e_impactos.csv').open(encoding='utf-8-sig',newline='') as f:fields=list(csv.DictReader(f))
    result=[]
    for item in items:
        if item.get('measure')=='Projeto aprovado':continue
        modules={m['code'] for m in cad['modules'] if m['item']==item['id']}
        related=[r for r in fields if modules&set(r['moveis_afetados'].split('|'))]
        roles=sorted({r['quem_valida'] for r in related});owners=set()
        for role in roles:
            if re.search(r'\bRT\b',role):owners.add('RT')
            if re.search(r'oficina|marceneiro',role,re.I):owners.add('Oficina/marceneiro')
            # Registrar/identificar fotos não transfere uma decisão técnica para Elias.
            if 'Elias' in role and not re.search(r'Elias (registra|identifica)',role):owners.add('Elias')
        result.append(dict(id='item-'+item['id'],item=item['id'],title=item['name'],room=item['room'],
            text=item.get('measure') or 'Conferência pendente na ficha',owners=sorted(owners) or ['a definir'],
            measurement=bool(related),source='07_Imovel/Medidas_e_impactos.csv' if related else None,
            codes=[r['codigo_medida'] for r in related],roles=roles))
    return result


def build():
    state=(ROOT/'ESTADO_ATUAL.md').read_text(encoding='utf-8')
    release=json.loads((HERE/'current_release.json').read_text(encoding='utf-8'))
    source=json.loads((HERE/'architect-source.json').read_text(encoding='utf-8'))
    table=state.split('## Onde estamos',1)[1].split('## Decisões',1)[0]
    progress=[]
    for line in table.splitlines():
        cells=[plain(c) for c in line.strip('|').split('|')]
        if len(cells)==3 and re.match(r'\d',cells[1]) and '%' in cells[1]:progress.append(dict(stage=cells[0],percent=cells[1],reading=cells[2].split(';')[0],source='ESTADO_ATUAL.md'))
    assert len(progress)==9,'Tabela de etapas mudou: revisar o extrator'
    for p in progress:
        original=p['reading'];p['reading']=source['progressBrief'].get(p['stage'],original)
        if p['stage']=='Orçamento':p['reading']=original+'; propostas pendentes.'
    def bullet(label):return plain(re.search(r'- \*\*'+label+r':\*\* (.+)',state)[1])
    overview=dict(project=plain(state.split('## O projeto',1)[1].split('\n\n')[1]),objective=bullet('Objetivo'),budget=bullet('Verba'),model=release['cadRevision'],notice='Tudo nominal até o levantamento real',source='ESTADO_ATUAL.md')
    for d in source['disciplines']:
        assert (ROOT/d['path']).exists(),d['path']
        if d['ownerSource']:assert d['ownerQuote'].lower() in (ROOT/d['ownerSource']).read_text(encoding='utf-8').lower(),d['id']
    for d in source['disciplines']:d['owners']=d['owners'] or ['a definir']
    for g in source['glossary']:g['term']=g['term'].replace('{cadRevision}',release['cadRevision'])
    stages=(ROOT/source['glossaryStagesSource']).read_text(encoding='utf-8')
    stages=re.findall(r'^### (T0[1-9]) — ([^|]+)\|',stages,re.M)
    assert len(stages)==9,'Etapas T01–T09 mudaram: conferir o glossário'
    for code,title in stages:
        source['glossary'].append(dict(id=code.lower(),term=code,definition='Etapa do plano: '+title.strip()+'. Código da agenda; não indica execução concluída.',path=source['glossaryStagesSource']))
    for m in literal(HERE/'src/cad-data.js','CAD_DATA')['modules']:
        source['glossary'].append(dict(id=m['code'].lower(),term=m['code'],definition='Código do móvel '+m['name']+'. Consulte a ficha; medidas são de projeto.',path='06_Entregas/Fichas_fabricacao/'+m['code']+'.html'))
    revisions=dict(architect=release['cadRevision'],model=release['cadRevision'],mood=release['appearanceRevision'],decisions=release['cadRevision']+'/'+release['lightingRevision'],documents=release['packageRevision']+'/'+release['fabricationRevision'],chaves=release['fabricationRevision'],obra=re.search(r'\| Cronograma \| ([^;|]+)',state)[1].strip(),floorplan=release['cadRevision'])
    contexts={id:dict(text=text,revision=revisions[id]) for id,text in source['tabDescriptions'].items()}
    data=dict(overview=overview,progress=progress,itemResponsibilities=responsibilities(),tabContexts=contexts,**source)
    import io
    stream=io.StringIO(newline='');writer=csv.writer(stream)
    writer.writerow(['id','pendencia','ambiente','responsavel'])
    for r in data['disciplines']+data['itemResponsibilities']:
        if 'a definir' in r['owners']:writer.writerow([r['id'],r['title'],r.get('room','geral'),'a definir'])
    (HERE/'Responsaveis_pendentes.csv').write_text(stream.getvalue(),encoding='utf-8',newline='')
    content='// Gerado por build_architect_data.py; fontes documentais.\nglobalThis.GUEDALA_ARCHITECT='+json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')+';\n'
    target=HERE/'src/architect-data.js'
    if not target.exists() or target.read_text(encoding='utf-8')!=content:target.write_text(content,encoding='utf-8',newline='\n')
    return data


if __name__=='__main__':build()


def publish_docs(target):
    """Fontes explícitas da entrada; não amplia o pacote selado ou varre pastas."""
    from build_workshop_docs import markdown,page
    data=build();target=Path(target)
    paths={'ESTADO_ATUAL.md','01_Programa_e_decisoes/Roteiro_para_projeto_oficial.md','01_Programa_e_decisoes/Plano_de_reforma_NBR16280.md','07_Imovel/Medidas_e_impactos.csv'}
    for item in data['shortcuts']+data['disciplines']:
        paths.update(item[k] for k in ('path','ownerSource') if item.get(k))
    paths.update(g['path'] for g in data.get('glossary',[]))
    for name in paths:
        source=ROOT/name;dest=target/(name+'.html' if source.suffix=='.md' else name)
        if dest.exists():continue
        dest.parent.mkdir(parents=True,exist_ok=True)
        if source.suffix!='.md':shutil.copyfile(source,dest);continue
        html=page(source.stem,markdown(source.read_text(encoding='utf-8')))
        def link(m):
            attr,delimiter,url=m.group(1,2,3);parsed=urlsplit(unquote(url))
            if parsed.scheme or url.startswith('#'):return m[0]
            resolved=posixpath.normpath(posixpath.join(posixpath.dirname(name),parsed.path))
            final=resolved+'.html' if resolved.endswith('.md') else resolved
            if (target/final).exists() or resolved in paths:
                return attr+'='+delimiter+quote(posixpath.relpath(final,posixpath.dirname(name)),safe='/')+('#'+parsed.fragment if parsed.fragment else '')+delimiter
            return 'data-unpublished-reference='+delimiter+url+delimiter
        html=re.sub(r'\b(href|src)\s*=\s*([\"\'])(.*?)\2',link,html)
        dest.write_text(html,encoding='utf-8')
    (target/'architect-sources.json').write_text(json.dumps(sorted(paths),ensure_ascii=False),encoding='utf-8')
