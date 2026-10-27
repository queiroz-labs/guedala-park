"""Fichas R15: fonte CAD preservada, evidência documental e campo separados."""
from pathlib import Path
from html import escape as esc
import json,re,csv,io
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
import technical_details as tech
import drilling_drawings
from plain_language import plain_html
from part_groups import group_panels

STUDY=Path(__file__).resolve().parent
ROOT=STUDY.parent.parent
DEST=ROOT/'06_Entregas/Fichas_fabricacao'
DATA=STUDY/'fabrication'
MATERIALS={'wood':'Greenplac Arenza (referência CAD)','petrol':'Guararapes Azul Petróleo','offwhite':'Off-white fosco (referência CAD)','bathbeige':'Bege fosco (referência CAD)','lightwood':'Madeira clara (referência CAD)','head':'Estofado bege','black':'Preto','stone':'Pedra'}
ROOMS={'quarto':'Quarto','cozinha':'Cozinha','escritorio':'Escritório','sala':'Sala + jantar','banho':'Banheiro','lavanderia':'Lavanderia'}

def mm(n): return f'{n:,.2f}'.rstrip('0').rstrip('.').replace(',','~').replace('.',',').replace('~','.')
def text(v): return esc(str(v if v is not None else 'A definir'))
def ul(items): return '<ul>'+''.join('<li>'+text(x)+'</li>' for x in items)+'</ul>'
def shortname(s): return re.sub(r'(?<=[a-záéíóúãõç])\d{3}$','',s,flags=re.I)
def table(headers,rows): return '<div class="table-scroll"><table><thead><tr>'+''.join('<th>'+text(h)+'</th>' for h in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+c+'</td>' for c in row)+'</tr>' for row in rows)+'</tbody></table></div>'

CSS='''*{box-sizing:border-box}body{font:15px/1.55 system-ui,sans-serif;color:#263c35;background:#f7f6f1;margin:0}main{max-width:1160px;margin:auto;padding:32px 28px}h1{font:38px/1.15 Georgia;margin:12px 0}h2{font:25px Georgia;margin:30px 0 14px}h3{font-size:16px}p{max-width:920px}.eyebrow,small{font-size:12px;color:#617269}.top,.nav,.metrics,.cards{display:flex;gap:14px;flex-wrap:wrap}.top{justify-content:space-between}a{color:#265647;text-underline-offset:3px}button,.action{padding:10px 15px;border:1px solid #c7cec4;border-radius:8px;background:white;font:inherit;color:inherit}.metrics>div{padding:16px 20px;background:white;border-radius:10px;min-width:150px}.metrics b{display:block;font:28px Georgia}.metrics span{font-size:12px}.note{padding:14px 18px;border-left:3px solid #b38d49;background:#f1ebdd}.panel{background:#fffefa;padding:20px 24px;margin:18px 0;border:1px solid #dce1d7;border-radius:12px}.table-scroll{overflow:auto}table{border-collapse:collapse;width:100%;font-size:12px}th,td{border-bottom:1px solid #dce1d7;text-align:left;padding:9px 8px;vertical-align:top}th{background:#e9eee5}td small{display:block;font-size:10px}.tag{display:inline-block;border-radius:20px;padding:3px 9px;background:#e5ece1;font-size:11px}.cards{display:grid;grid-template-columns:repeat(3,1fr)}.card{display:block;text-decoration:none;background:white;border:1px solid #dce1d7;border-radius:10px;padding:18px}.card h3{font:22px Georgia;margin:8px 0}.drawing{width:100%;height:auto;max-height:480px}details summary{cursor:pointer;padding:10px 0;font-weight:600}input{border:0;border-bottom:1px solid #84988c;width:130px;padding:8px;background:white}li{margin:7px 0}footer{border-top:1px solid #c7cec4;margin-top:32px;padding-top:15px;font-size:11px;color:#617269}@media(max-width:650px){main{padding:20px 16px}h1{font-size:30px}.cards{grid-template-columns:1fr}.panel{padding:15px}.metrics{gap:8px}.metrics>div{min-width:0;flex:1;padding:10px}.metrics b{font-size:22px}table{min-width:590px}.drawing{min-height:200px}}@media print{body{background:white;font-size:10pt}main{padding:0;max-width:none}.no-print{display:none!important}.panel{border:0;border-radius:0;padding:0;margin:15px 0}.metrics>div{padding:5px 15px 5px 0}.table-scroll{overflow:visible}table{font-size:8pt;min-width:0!important}thead{display:table-header-group}tr{break-inside:avoid}.drawing{max-height:290px}h2,h3{break-after:avoid}h1{font-size:25pt}.note{padding:7px}.cards{grid-template-columns:repeat(2,1fr)}a{color:inherit;text-decoration:none}input{background:white}details>*{display:block}footer{font-size:8pt}}'''

CSS+='\n.sources-note a,.gates a{display:inline-block;min-height:32px;padding:6px 0;margin:4px 0}a:focus-visible,button:focus-visible,input:focus-visible{outline:3px solid #805c32;outline-offset:3px}\n'

def page(title,body): return '<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="'+text(title)+' — medidas, materiais e montagem do projeto Guedala Park."><link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 64 64%27%3E%3Crect width=%2764%27 height=%2764%27 rx=%2714%27 fill=%27%23263f3b%27/%3E%3Ctext x=%2732%27 y=%2742%27 text-anchor=%27middle%27 font-size=%2729%27 fill=%27white%27%3EGP%3C/text%3E%3C/svg%3E"><title>'+text(title)+'</title><style>'+CSS+tech.CSS+'</style></head><body><main>'+plain_html(body)+'</main></body></html>'

def diagram(module,parts,frame):
    # Project each panel's local bounding box. These are explicit envelope diagrams,
    # never hidden-line engineering drawings or hole/cut templates.
    boxes=[];allpoints=[]
    for p in parts:
        pts=[]
        for v in p['v']:
            w=[7400-(p['x']+v[0])*10,(p['z']+v[2])*10,(p['y']+v[1])*10,1]
            pts.append([sum(a*b for a,b in zip(row,w)) for row in frame])
        allpoints+=pts
        if p.get('piece'): boxes.append(([min(v[k] for v in pts) for k in range(3)],[max(v[k] for v in pts) for k in range(3)]))
    lo=[min(v[k] for v in allpoints) for k in range(3)];hi=[max(v[k] for v in allpoints) for k in range(3)]
    svg=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 390" role="img" aria-label="Esquemas de envelopes em três projeções, cotas nominais em milímetros"><rect width="1080" height="390" fill="#fffefa"/>']
    for i,(a,b,title) in enumerate([(0,2,'Elevação · X–Z'),(1,2,'Perfil · Y–Z'),(0,1,'Planta · X–Y')]):
        W=hi[a]-lo[a];H=hi[b]-lo[b];scale=min(255/max(W,1),245/max(H,1));x=i*360+55+(255-W*scale)/2;y=52+(245-H*scale)/2
        svg.append(f'<g font-family="Arial" fill="#334e42"><text x="{i*360+180}" y="25" text-anchor="middle" font-size="15">{title}</text>')
        for low,high in boxes:
            xx=x+(low[a]-lo[a])*scale;yy=y+(hi[b]-high[b])*scale
            ww=max((high[a]-low[a])*scale,.5);hh=max((high[b]-low[b])*scale,.5)
            svg.append(f'<rect x="{xx:.2f}" y="{yy:.2f}" width="{ww:.2f}" height="{hh:.2f}" fill="#dce5d4" fill-opacity=".24" stroke="#738771" stroke-width=".65"/>')
        svg.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{W*scale:.2f}" height="{H*scale:.2f}" fill="none" stroke="#263c35" stroke-dasharray="4 4"/>')
        yy=y+H*scale+18
        svg.append(f'<path d="M{x},{yy-5}v10 M{x},{yy}h{W*scale} m0,-5v10" stroke="#263c35" fill="none"/><text x="{x+W*scale/2}" y="{yy+19}" text-anchor="middle" font-size="13">{mm(W)} mm</text>')
        xx=x-18
        svg.append(f'<path d="M{xx-5},{y}h10 M{xx},{y}v{H*scale} m-5,0h10" stroke="#263c35" fill="none"/><text transform="translate({xx-8},{y+H*scale/2}) rotate(-90)" text-anchor="middle" font-size="12">{mm(H)} mm</text></g>')
    svg.append('<text x="540" y="378" text-anchor="middle" font-family="Arial" font-size="12" fill="#617269">Envelopes dos painéis · contornos especiais, furos e recortes não representados · sem escala de impressão</text></svg>')
    return ''.join(svg)

def build():
    DEST.mkdir(parents=True,exist_ok=True)
    revision=tech.load_revision()
    raw=(STUDY/'src/cad-data.js').read_text(encoding='utf-8');cad=json.loads(raw.split('const CAD_DATA=',1)[1].rstrip(';\n'))
    frames=json.loads((DATA/'module-frames.json').read_text(encoding='utf-8'));assert frames['sha256']==cad['source_sha256']
    hw=json.loads((DATA/'hardware-audit.json').read_text(encoding='utf-8'))
    finish=json.loads((DATA/'finish-audit.json').read_text(encoding='utf-8'))
    overrides={o['source']:o for o in finish.get('overrides',[])}
    matrix={}
    for line in (ROOT/'04_Moveis/Inventario_dimensional/Inventario/Matriz_20_modulos.md').read_text(encoding='utf-8').splitlines():
        if re.match(r'\| P\d\d \|',line):
            row=[p.strip() for p in line.strip('|').split('|')];matrix[row[0]]=row[2]
    allparts={p['source']:p for p in cad['parts']};modules={};assets=[]
    for m in cad['modules']:
        code=m['code'];h=hw['modules'][code];f=finish['modules'][code]
        parts=[allparts[s] for s in m['parts']];panels=[]
        for p in parts:
            if not p.get('piece'): continue
            ov=overrides.get(p['source']);mat=MATERIALS.get(p['piece']['material'],p['piece']['material'] or 'Não individualizado')
            panels.append({'id':p['source'],'name':shortname(p['label']),'dimensions':p['piece']['dimensions'],'thickness':p['piece']['thickness'],'rectangular':p['piece']['rectangular'],'cadMaterial':mat,'specifiedMaterial':ov['material'] if ov else None,'materialEvidence':ov['evidence'] if ov else p.get('materialSource'),'finishComplete':ov.get('finishCompleteForIdentifiedFaces',False) if ov else False,'remainingFinish':ov.get('remainingFinishQuestion') if ov else 'Aplicação por face ainda não individualizada','quantity':1})
        fields=f.get('fieldChecks',[])
        technical=list(dict.fromkeys(h.get('technicalChecks',[])+f.get('technicalChecks',[])))
        assembly=list(dict.fromkeys(f.get('assembly',[])+h.get('assembly',[])))
        g=dict(code=code,name=m['name'],room=m['room'],dimensions=m['dimensionsLocal'],internalMeasures=matrix[code],panels=panels,hardwareRows=h['hardwareRows'],finishSummary=f['finishSummary'],finishSpecs=f.get('finishSpecs',[]),fieldChecks=fields,technicalChecks=technical,assembly=assembly,sources=list(dict.fromkeys(h.get('sources',[])+f.get('sources',[]))),sheetPath=f'06_Entregas/Fichas_fabricacao/{code}.html',drawingPath=f'06_Entregas/Fichas_fabricacao/{code}.svg')
        tech.apply_revision(g,revision)
        g['panelGroups']=group_panels(g,allparts)
        technical=g['technicalChecks'];fields=g['fieldChecks'];assembly=g['assembly']
        modules[code]=g
        assets.append(tech.write_drilling_csv(g,DEST))
        if g.get('drawings'):
            filename=code+'-furacao.svg'
            (DEST/filename).write_text(drilling_drawings.render(g['drawings'],code),encoding='utf-8')
            assets.append(filename)
            g['drillingDrawingPath']='06_Entregas/Fichas_fabricacao/'+filename
        (DEST/f'{code}.svg').write_text(diagram(m,parts,frames['frames'][code]),encoding='utf-8');assets.append(f'{code}.svg')
        headers=['IDs CAD','Peça','Qtd','C nominal mm','L nominal mm','Esp. envelope mm','Referência CAD','Especificação documental','Contorno','Bordas/veios/usinagem','Acabamento parcial']
        rows=[[' | '.join(p['ids']),p['name'],p['quantity'],*p['dimensions'],p['cadMaterial'],p['specifiedMaterial'] or 'Ver regra de acabamento da ficha','Retangular' if p['rectangular'] else 'Recortado/especial','Detalhamento técnico por ID; não descontado do envelope',p['remainingFinish'] or ''] for p in g['panelGroups']]
        buf=io.StringIO();w=csv.writer(buf,delimiter=';');w.writerow(headers);w.writerows(rows);(DEST/f'{code}-pecas.csv').write_text('\ufeff'+buf.getvalue(),encoding='utf-8',newline='');assets.append(f'{code}-pecas.csv')
        hardware_rows=[[text(r.get('quantity'))+' '+text(r.get('unit','')),text(r['item'])+('<small>'+text(r['explanation'])+'</small>' if r.get('explanation') else '')+'<small>'+text(r.get('reference'))+'</small>',text(r['status']),text(r.get('assembly',''))] for r in g['hardwareRows']]
        parts_rows=[]
        for p in g['panelGroups']:
            members=''.join('<li>'+text(item['name'])+' · <code>'+text(item['id'])+'</code></li>' for item in p['members'])
            identity=text(p['name'])+('<details class="part-members"><summary>Ver '+str(p['quantity'])+' peças e IDs</summary><ul>'+members+'</ul></details>' if len(p['ids'])>1 else '<small>'+text(p['id'])+'</small>')
            parts_rows.append([identity,'<strong>'+str(p['quantity'])+'</strong>',text(mm(p['dimensions'][0]))+' × '+text(mm(p['dimensions'][1])),text(mm(p['thickness'])),text(p['specifiedMaterial'] or p['cadMaterial'])+'<small>'+('Acabamento escolhido' if p['specifiedMaterial'] else 'Cor do desenho · confira o acabamento acima')+'</small>'+('<small>Parcial: '+text(p['remainingFinish'])+'</small>' if p['remainingFinish'] else ''),'Retangular' if p['rectangular'] else 'Recortado/especial'])
        finish_rows=[[text(r['area']),text(r['material']),text(r['status'])] for r in g['finishSpecs']]
        body=f'<div class="top no-print"><a href="index.html">← Todas as fichas</a><a href="Levantamento.html#{code}">Medições deste móvel ↗</a></div><p class="eyebrow">{code} · {ROOMS[m["room"]]} · FICHA R15 / MODELO R53 · mm</p><h1>{text(g["name"])}</h1><p class="no-print nav"><button onclick="window.print()">Imprimir / salvar PDF</button><a class="action" href="{code}-pecas.csv" download>Baixar lista de peças · CSV</a></p><div class="metrics">'+''.join(f'<div><b>{mm(v)}</b><span>{label} · mm</span></div>' for v,label in zip(g['dimensions'],['Largura','Profundidade','Altura']))+'</div><p class="eyebrow">Envelope nominal do conjunto, incluindo componentes e reservas. Peças abaixo têm medidas próprias.</p>'
        body+='<p class="revision-summary">'+text(g['technicalSummary'])+'</p><nav class="sheet-nav no-print"><a href="#definido">Definições</a><a href="#furacao">Furação</a><a href="#pecas">Peças</a><a href="#proximos">O que falta</a></nav>'
        body+='<section id="definido" class="panel"><h2>Definido para este móvel</h2>'+tech.choices_html(g)+'</section>'
        body+=f'<img width="1080" height="390" class="drawing" src="{code}.svg" alt="{code}: esquema dimensional de envelopes em três projeções"><div class="panel"><h2>Medidas internas e encontros</h2><p>{text(g["internalMeasures"])}</p></div>'
        body+='<div class="panel"><h2>Acabamentos</h2><p>'+text(g['finishSummary'])+'</p>'+table(['Aplicação','Material / acabamento','Situação'],finish_rows)+'<p class="eyebrow">A especificação documental vigente prevalece sobre cores antigas do modelo. Código comercial não informado permanece a definir.</p></div>'
        body+='<div class="panel" id="pecas"><h2>Peças e espessuras</h2>'+'<p>'+str(len(g['panels']))+' peças em '+str(len(g['panelGroups']))+' grupos. Peças equivalentes aparecem juntas; abra os códigos para consultar cada uma.</p>'+table(['Peça / grupo','Qtd.','C × L · mm','Esp. · mm','Material','Forma'],parts_rows)+'<p class="eyebrow">C e L são as duas maiores dimensões do envelope local, sem indicar sentido do veio. Espessura é a menor dimensão geométrica. Recortes e furação não podem ser recuperados destas três medidas. Fita de borda e folgas não foram descontadas; lista nominal, não plano de corte.</p></div>'
        body+='<div class="panel"><h2>Ferragens e ligações</h2>'+table(['Qtd.','Ferragem / referência','Situação','Montagem / conferência'],hardware_rows)+'<p class="eyebrow">Quantidade de referência não equivale a compra liberada. Itens candidatos conservam seu status até fechar compatibilidade.</p></div>'
        body+='<section class="panel" id="furacao"><h2>Furação e fixação</h2>'+tech.drilling_html(g)+'</section>'
        body+='<div class="panel"><h2>Roteiro de montagem e compatibilização</h2>'+ul(assembly)+'</div><section class="panel" id="proximos"><h2>Fechamentos técnicos deste móvel</h2>'+tech.gates_html(g)+'</section>'
        body+=f'<div class="note"><b>Medição no apartamento, em folha separada</b><p>{len(fields)} conferências para este móvel. <a href="Levantamento.html#{code}">Abrir levantamento de campo →</a></p></div>'
        body+='<details><summary>Rastreabilidade documental</summary>'+ul(g['sources'])+'</details><footer>Ficha R15 · 27/10/2026 · CAD R53 SHA256 '+cad['source_sha256']+'<br>Geometria R53; mapas de furação herdados da R14 conservam suas fontes e condições. Pronta para consulta e compatibilização. Liberação de fabricação exige resolver os fechamentos técnicos e as cotas de campo aplicáveis.</footer>'
        (DEST/f'{code}.html').write_text(page(code+' · '+g['name'],body),encoding='utf-8')
    index='<p class="eyebrow">GUEDALA PARK · FICHAS DE MARCENARIA R15</p><h1>Uma ficha para cada móvel.</h1><p>Medidas, peças, acabamento e ferragens no mesmo documento. Anote as medidas reais na folha do apartamento.</p><p class="nav"><a class="action" href="Levantamento.html">Abrir levantamento no apartamento</a></p><div class="cards">'
    for code,g in modules.items():
        index+=f'<a class="card" href="{code}.html"><span class="eyebrow">{code} · {ROOMS[g["room"]]}</span><h3>{text(g["name"])}</h3><p>{" × ".join(mm(v) for v in g["dimensions"])} mm</p><small>{len(g["panels"])} peças · ferragens · acabamento · montagem</small></a>'
    index+='</div><p class="note">Revisão R15: consulte as definições e a furação de cada móvel. Projeto, prova de oficina e medição no apartamento têm listas separadas. Seleção de ferragem não equivale a liberação de usinagem.</p><p><a href="Pendencias.html">Ver próximos passos dos 20 móveis →</a></p>'
    (DEST/'index.html').write_text(page('Fichas de marcenaria R15',index),encoding='utf-8')
    field='<div class="no-print"><a href="index.html">← Fichas dos móveis</a></div><p class="eyebrow">GUEDALA PARK · LEVANTAMENTO DE CAMPO</p><h1>O que medir no apartamento.</h1><p>Preencher em milímetros, com data, responsável e referência de piso acabado. Anexar fotos com régua e marcar cada ponto na planta. Estes campos são uma folha de coleta: preencher no navegador não salva os valores; imprima ou salve em PDF.</p><p>Data: __________________ Responsável: __________________</p><button class="no-print" onclick="window.print()">Imprimir / salvar PDF</button><p class="note">Material, ferragens, cargas, folgas de mecanismos e usinagem são decisões técnicas das fichas. Aqui entram apenas condições físicas existentes no apartamento.</p>'
    for code,g in modules.items():
        field+=f'<section id="{code}" class="panel"><h2>{code} · {text(g["name"])}</h2>'+table(['Conferência','Como registrar','Afeta','Valor / observação'],[[text(c.get('measure')),text(c.get('method'))+'<small>Referência: '+text(c.get('datum'))+'</small>',text(c.get('affects')),'<input aria-label="'+text(code+' '+c.get('measure',''))+'" placeholder="____________">'] for c in g['fieldChecks']])+'<details><summary>Como conferir o levantamento</summary>'+ul(list(dict.fromkeys(c.get('acceptance','Confrontar com projeto executivo.') for c in g['fieldChecks'])))+'</details></section>'
    (DEST/'Levantamento.html').write_text(page('Levantamento no apartamento',field),encoding='utf-8')
    pending='<div class="no-print"><a href="index.html">← Fichas dos móveis</a></div><p class="eyebrow">REVISÃO R15 · ETAPAS DE FECHAMENTO</p><h1>O que falta, no lugar certo.</h1><p>As escolhas de ferragens e os parâmetros disponíveis estão nas fichas. Aqui, cada móvel distingue compatibilização de projeto, conferência em oficina e levantamento físico no apartamento.</p><p class="note">A seleção das dobradiças Blum substitui alternativas de orçamento ainda abertas. Recotar essa família antes da compra; esta revisão não confirma o total do orçamento anterior.</p>'
    for code,g in modules.items():
        pending+='<section class="panel" id="'+code+'"><h2><a href="'+code+'.html">'+code+' · '+text(g['name'])+'</a></h2><p>'+text(g['technicalSummary'])+'</p>'+tech.gates_html(g)+'</section>'
    (DEST/'Pendencias.html').write_text(page('Próximos passos · R15',pending),encoding='utf-8')
    public_revision=json.loads(json.dumps(revision))
    for code,g in modules.items():
        public_revision['modules'][code]['summary']=g['technicalSummary']
        public_revision['modules'][code]['name']=g['name']
    (DEST/'Tecnica_R15.json').write_text(json.dumps(public_revision,ensure_ascii=False,indent=2),encoding='utf-8')
    assets.append('Tecnica_R15.json')
    package={'revision':'R15','cadRevision':'R53','source_sha256':cad['source_sha256'],'modules':modules}
    (STUDY/'src/fabrication-data.js').write_text('const FABRICATION_DATA = '+json.dumps(package,ensure_ascii=False,indent=2)+';\n',encoding='utf-8')
    (DEST/'manifest.json').write_text(json.dumps({'revision':'R15','modules':20,'panels':sum(len(g['panels']) for g in modules.values()),'files':['index.html','Levantamento.html','Pendencias.html']+[c+'.html' for c in modules]+assets},indent=2),encoding='utf-8')
    print('Fichas R15: 20 módulos; '+str(sum(len(g['panels']) for g in modules.values()))+' painéis; levantamento separado.')
    return modules,assets

if __name__=='__main__':build()
