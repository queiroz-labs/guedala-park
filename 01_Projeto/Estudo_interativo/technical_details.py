"""R14: escolhas técnicas rastreáveis, furação e etapas de conferência."""
from pathlib import Path
from html import escape
import csv, io, json

DATA = Path(__file__).resolve().parent / 'fabrication/technical-r14.json'

def text(value):
    if value is None or value == '':
        return 'Não definido'
    if isinstance(value, (list, dict)):
        value = json.dumps(value, ensure_ascii=False)
    return escape(str(value))

def source_links(sources):
    out=[]
    for source in sources or []:
        if isinstance(source, str):
            source={'url':source} if source.startswith('https://') else {'title':source}
        label=source.get('title') or source.get('label') or source.get('url') or source.get('path') or 'Fonte'
        url=source.get('url','')
        suffix=' · '+str(source['page']) if source.get('page') else ''
        if url.startswith(('https://','http://')):
            out.append('<a target="_blank" rel="noopener" href="'+escape(url,quote=True)+'">'+text(label)+text(suffix or ' ')+'</a>')
        else:
            out.append(text(label+suffix))
    return '<br>'.join(out)

def load_revision():
    data=json.loads(DATA.read_text(encoding='utf-8'))
    assert set(data['modules']) == {f'P{i:02}' for i in range(1,21)}
    return data

def apply_revision(g, revision):
    module=revision['modules'][g['code']]
    for field in ['hardwareRows','technicalChecks','fieldChecks','assembly']:
        if field in module:
            g[field]=module[field]
    for field in ['decisions','drilling','workshopChecks','projectChecks','resolvedChecks','drawings','unmappedInterfaces']:
        g[field]=module.get(field,[])
    g['revision']='R14'
    g['drillingPath']=f"05_Entregas/Fichas_fabricacao_R13/{g['code']}-furacao.csv"
    g['technicalSummary']=module['summary']
    g['sources']=list(dict.fromkeys(g['sources']+module.get('sourcePaths',[])))
    return g

def choices_html(g):
    out='<div class="decision-grid">'
    for row in g['decisions']:
        qty='' if row.get('quantity') is None else f" · {row['quantity']} {row.get('unit','')}"
        out+='<article class="decision"><small>'+text(row.get('status','Selecionado em projeto'))+'</small><h3>'+text(row['item'])+'</h3><p><strong>'+text(row['reference'])+text(qty or ' ')+'</strong></p><p>'+text(row['reason'])+'</p><div class="sources-note">'+source_links(row.get('sources'))+'</div></article>'
    return out+'</div>'

DRILL_FIELDS=[('partIds','Peças CAD'),('face','Face a trabalhar'),('datum','Origem / referência'),('pattern','Posição dos furos · mm'),('diameter','Diâmetro · mm'),('depth','Profundidade · mm'),('fastener','Fixador'),('releaseCondition','Conferência antes de furar')]

def drilling_html(g):
    out='<p>Valores em milímetros. Cada operação informa sua situação: parâmetro de catálogo, mapa nominal ou detalhe ainda bloqueado. Coordenadas nominais exigem conferência da ferragem e prova em retalho antes de usinar a peça.</p><p class="no-print"><a class="action" href="'+g['code']+'-furacao.csv" download>Baixar tabela de furação CSV</a></p>'
    if g.get('drawings'):
        out+='<details class="no-print"><summary>Ver mapas por peça · '+str(len(g['drawings']))+' vistas</summary><a href="'+g['code']+'-furacao.svg" target="_blank" rel="noopener">Abrir desenho completo ↗</a><img style="width:100%;height:auto" src="'+g['code']+'-furacao.svg" alt="'+g['code']+': mapas nominais de furação com origem e face identificadas"></details>'
    for row in g['drilling']:
        out+='<article class="drilling-card"><div class="drilling-head"><h3>'+text(row['item'])+'</h3><span class="tag">'+text(row['status'])+'</span></div><dl>'
        for field,label in DRILL_FIELDS:
            value=row.get(field)
            if isinstance(value,list):value=', '.join(value)
            out+='<div><dt>'+label+'</dt><dd>'+text(value)+'</dd></div>'
        out+='</dl><div class="sources-note">'+source_links(row.get('sources'))+'</div></article>'
    return out

def check_html(items):
    if not items:return '<p>Nenhuma pendência adicional nesta etapa.</p>'
    return '<ul>'+''.join('<li>'+text(v)+'</li>' for v in items)+'</ul>'

def gates_html(g):
    interfaces=g.get('unmappedInterfaces',[])
    return '<div class="gates"><section><h3>Projeto · compatibilizar</h3>'+check_html(g['projectChecks'])+'</section><section><h3>Oficina · conferir e provar</h3>'+check_html(g['workshopChecks'])+'</section><section><h3>Apartamento · medir</h3><p>'+str(len(g['fieldChecks']))+' conferências físicas, em folha separada.</p><a href="Levantamento.html#'+g['code']+'">Abrir medições deste móvel →</a></section></div>'+('<details><summary>Ligações ainda sem mapa · '+str(len(interfaces))+' contatos</summary><p>Encontros identificados na amostra de painéis retangulares. Cada par ainda exige distribuição de conectores; o número de contatos não é quantidade de parafusos. Ausência na amostra não elimina uma ligação necessária.</p>'+check_html(interfaces)+'</details>' if interfaces else '')

def write_drilling_csv(g, dest):
    buf=io.StringIO(newline='')
    writer=csv.writer(buf,delimiter=';')
    writer.writerow(['Módulo','Operação','Situação']+[label for _,label in DRILL_FIELDS]+['Fontes'])
    for row in g['drilling']:
        values=[g['code'],row['item'],row['status']]
        for key,_ in DRILL_FIELDS:
            val=row.get(key)
            values.append(', '.join(val) if isinstance(val,list) else (val if val is not None else 'Não definido'))
        values.append(json.dumps(row.get('sources',[]),ensure_ascii=False))
        writer.writerow(values)
    filename=g['code']+'-furacao.csv'
    (dest/filename).write_text('\ufeff'+buf.getvalue(),encoding='utf-8',newline='')
    return filename

CSS='''.decision-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}.decision,.drilling-card{border:1px solid #dce1d7;border-radius:9px;padding:16px;margin:12px 0;overflow-wrap:anywhere}.decision h3,.drilling-card h3{margin:5px 0 10px}.decision>small{color:#47654f}.sources-note{font-size:11px;color:#617269;overflow-wrap:anywhere}.drilling-head{display:flex;justify-content:space-between;align-items:start;gap:12px}.drilling-card dl{margin:10px 0}.drilling-card dl>div{display:grid;grid-template-columns:190px 1fr;gap:12px;padding:7px 0;border-bottom:1px solid #e6e9e1;font-size:12px}.drilling-card dt{font-weight:600}.drilling-card dd{margin:0}.gates{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}.gates section{border-top:3px solid #bccbb5;padding-top:5px;font-size:13px}.gates ul{padding-left:18px}.sheet-nav{display:flex;gap:8px;flex-wrap:wrap;margin:20px 0}.sheet-nav a{padding:8px 12px;border:1px solid #c7cec4;border-radius:7px;text-decoration:none;font-size:13px}.revision-summary{background:#edf2e9;padding:15px 20px;border-radius:9px;font-size:14px}@media(max-width:650px){.decision-grid,.gates{grid-template-columns:1fr}.drilling-card dl>div{grid-template-columns:1fr;gap:2px}.drilling-head{display:block}.drilling-card{padding:12px}}@media print{details::details-content{content-visibility:visible!important;display:block!important}.decision-grid,.gates{display:block}.decision,.drilling-card{break-inside:avoid;padding:10px;margin:8px 0}.sources-note{font-size:8pt}.sheet-nav{display:none}.drilling-card dl>div{font-size:8pt;padding:4px 0}}'''
