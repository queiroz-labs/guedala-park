"""Floor plan reference: official written dimensions + separately identified reconstruction.
Writes only this feature's HTML/SVG/JSON/PNG and src/floorplan-ui.js. Never changes CAD.
"""
from pathlib import Path
from html import escape
import json,re,shutil

STUDY=Path(__file__).resolve().parent
ROOT=STUDY.parent.parent
OUT=ROOT/'05_Entregas/Planta_cotada_R13'
PDF='02_Plantas_e_manuais/Planta_oficial.pdf'
SCREEN=OUT/'Planta_oficial.png'  # Versioned full-page official reference; no external build dependency.
source=(STUDY/'src/app.js').read_text(encoding='utf-8')
# The construction comes from the actual viewer source, not from pixel estimates.
def literal(name):
 match=re.search(r'const '+name+r'=(\[.*?\]);',source)
 if not match:raise ValueError('Missing '+name)
 return json.loads(match[1].replace("'",'"'))
floors=literal('floors');walls=literal('walls')
ROOMS=[('all','Visão geral'),('quarto','Quarto · dormitório 01'),('escritorio','Escritório · dormitório 02'),('sala','Sala'),('cozinha','Cozinha'),('lavanderia','Área de serviço'),('banho','Banheiro'),('circulacao','Circulação')]
COTAS=[
 {'id':'quarto','title':'Quarto / dormitório 01','official':'2,45 × 2,95 m','mm':[2450,2950],'scope':'Retângulo principal do dormitório; não inclui a reentrância reconstruída.','match':'Cotas escritas correspondem ao retângulo principal do modelo.'},
 {'id':'escritorio','title':'Escritório / dormitório 02','official':'2,30 × 2,95 m','mm':[2300,2950],'scope':'Entre faces internas do retângulo principal.','match':'Cotas escritas correspondem ao modelo.'},
 {'id':'sala','title':'Sala','official':'Largura 2,45 m','mm':[2450],'scope':'Largura da sala; a cota 5,15 m é o eixo contínuo sala/cozinha.','match':'Não atribuir 5,15 m somente à sala.'},
 {'id':'sala cozinha','title':'Eixo sala + cozinha','official':'5,15 m','mm':[5150],'scope':'Da parede superior da sala à parede inferior da cozinha, no eixo direito.','match':'Correspondência nominal no modelo: y185 a700 cm.'},
 {'id':'banho','title':'Banheiro','official':'2,09 × 1,24 m','mm':[2090,1240],'scope':'Retângulo interno cotado; volumes e equipamentos não desenhados nesta vista.','match':'Cotas escritas correspondem ao modelo.'},
 {'id':'lavanderia','title':'Área de serviço','official':'1,29 × 1,54 m','mm':[1290,1540],'scope':'Cotas da planta oficial. Altura/profundidade 1,54 m está apenas na tabela: os pontos extremos não coincidem com a reconstrução.','match':'Reconstrução do site:1,29 ×1,61 m. Diferença de7 cm no segundo eixo; não resolvida por deslocar uma linha de cota.'},
 {'id':'cozinha','title':'Faixa da cozinha','official':'3,52 × 1,55 m','mm':[3520,1550],'scope':'Faixa indicada na planta; não representa todo o ambiente integrado nem confirma a parede divisória com a área de serviço.','match':'Faixa nominal correspondente no modelo; limites abertos não são novas paredes.'},
 {'id':'circulacao','title':'Circulação','official':'Trechos de 0,90 m e 1,05 m','mm':[900,1050],'scope':'Dois trechos cotados. Não formam um retângulo genérico de0,90 ×1,05.','match':'Faixa reconstruída do site:1,30 ×0,90 m. O trecho1,05 m não é substituído pelo envelope1,30 m.'},
]
NOTE='Cotas transcritas da planta oficial, página1. Geometria de apoio reconstruída a partir do site. As medidas podem variar com os acabamentos, conforme a nota da planta; não são levantamento do apartamento nem liberação de corte.'
SVG_STYLE='''.fp-zone{fill:#f4f1e9;stroke:#e4e0d5;stroke-width:1;cursor:pointer}.fp-zone:focus{outline:none;stroke:#254f43;stroke-width:3}.fp-wall{fill:#55645d}.fp-room-name{font:600 16px system-ui,sans-serif;fill:#34483e;text-anchor:middle;pointer-events:none}.fp-room-sub{font:11px system-ui,sans-serif;fill:#64786b;text-anchor:middle;pointer-events:none}.fp-dim{stroke:#447562;stroke-width:1.2;fill:none}.fp-dim-label{font:600 12px system-ui,sans-serif;fill:#285c49;text-anchor:middle;paint-order:stroke;stroke:#fff;stroke-width:5px;stroke-linejoin:round}.fp-model .fp-dim{stroke:#9a7350;stroke-dasharray:4 4}.fp-model .fp-dim-label{fill:#8b6848}.fp-muted{opacity:.18}.fp-picked.fp-wall{fill:#1b654a}.fp-picked .fp-zone{fill:#dbe9df;stroke:#39765c;stroke-width:2}.fp-picked .fp-dim{stroke:#12583e;stroke-width:1.8}.fp-floorgroup,.fp-dimgroup,.fp-wall{transition:opacity .15s}.fp-legend-text{font:11px system-ui,sans-serif;fill:#5f6c62}.fp-open-edge{stroke:#c9c5ba;stroke-width:1;stroke-dasharray:4 5;fill:none}'''

def group(tag,rooms,content,cls=''):
 return f'<g class="{tag} {cls}" data-fp-room="{rooms}">{content}</g>'
def dim_h(room,x1,x2,y,label,from_y=None,model=False):
 ext='' if from_y is None else f'<path class="fp-dim" d="M{x1},{from_y}V{y+5} M{x2},{from_y}V{y+5}" opacity=".45"/>'
 content=ext+f'<path class="fp-dim" d="M{x1},{y}H{x2} M{x1-4},{y+4}l8,-8 M{x2-4},{y+4}l8,-8"/><text class="fp-dim-label" x="{(x1+x2)/2}" y="{y-7}">{escape(label)}</text>'
 return group('fp-dimgroup',room,content,'fp-model' if model else '')
def dim_v(room,y1,y2,x,label,from_x=None,model=False):
 ext='' if from_x is None else f'<path class="fp-dim" d="M{from_x},{y1}H{x+5} M{from_x},{y2}H{x+5}" opacity=".45"/>'
 mid=(y1+y2)/2
 content=ext+f'<path class="fp-dim" d="M{x},{y1}V{y2} M{x-4},{y1+4}l8,-8 M{x-4},{y2+4}l8,-8"/><text class="fp-dim-label" x="{x-9}" y="{mid}" transform="rotate(-90 {x-9} {mid})">{escape(label)}</text>'
 return group('fp-dimgroup',room,content,'fp-model' if model else '')

def make_svg():
 body=[]
 titles={'quarto':'QUARTO','escritorio':'ESCRITÓRIO','sala':'SALA','cozinha':'COZINHA','lavanderia':'ÁREA DE SERVIÇO','banho':'BANHEIRO','circulacao':'CIRCULAÇÃO'}
 for room in titles:
  rects=[]
  for f in floors:
   if f[0]!=room:continue
   _,x,y,w,h,_=f
   rects.append(f'<rect class="fp-zone" x="{x}" y="{y}" width="{w}" height="{h}" tabindex="0" role="button" data-fp-select="{room}" aria-label="Selecionar {titles[room].lower()}"><title>{titles[room]} — clique para conferir cotas e origem</title></rect>')
  body.append(group('fp-floorgroup',room,''.join(rects)))
 for w in walls:
  room,x,y,ww,hh,*adj=w;keys=[room]+(adj[0] if adj else [])
  body.append(f'<rect class="fp-wall" data-fp-room="{" ".join(keys)}" x="{x}" y="{y}" width="{ww}" height="{hh}"/>')
 positions={'quarto':(133,238),'escritorio':(376,147),'sala':(617,353),'cozinha':(550,614),'lavanderia':(325,610),'banho':(355,480),'circulacao':(426,351)}
 for room,(x,y) in positions.items():
  font=' style="font-size:10px"' if room in ['lavanderia','circulacao'] else ''
  subs={'quarto':'DORMITÓRIO 01','escritorio':'DORMITÓRIO 02','sala':'AMBIENTE INTEGRADO','cozinha':'FAIXA COTADA','lavanderia':'ver diferença abaixo','banho':'','circulacao':'trechos: ver tabela'}
  body.append(group('fp-floorgroup',room,f'<text class="fp-room-name"{font} x="{x}" y="{y}">{titles[room]}</text><text class="fp-room-sub" x="{x}" y="{y+18}">{subs[room]}</text>'))
 body += [dim_h('quarto',0,245,128,'2,45 m'),dim_v('quarto',100,395,28,'2,95 m'),dim_h('escritorio',255,485,28,'2,30 m'),dim_v('escritorio',0,295,281,'2,95 m'),dim_h('sala',495,740,213,'2,45 m'),dim_v('sala cozinha',185,700,790,'5,15 m · sala + cozinha',740),dim_h('banho',255,464,429,'2,09 m'),dim_v('banho',405,529,448,'1,24 m'),dim_h('lavanderia',255,384,565,'1,29 m'),dim_v('lavanderia',539,700,275,'1,61 m · reconstrução',None,True),dim_h('cozinha',388,740,677,'3,52 m'),dim_v('cozinha',545,700,719,'1,55 m')]
 body.append('<text class="fp-legend-text" x="0" y="758">Cotas em metros · paredes e aberturas reconstituídas · sem mobiliário</text>')
 return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="-35 -35 890 815" role="img" aria-labelledby="fpSvgTitle fpSvgDesc"><title id="fpSvgTitle">Guedala Park — planta de consulta com cotas</title><desc id="fpSvgDesc">Cotas da planta oficial sobre apoio geométrico do site. Área de serviço tem1,54mna fonte oficial e1,61mna reconstrução; circulação tem trechos0,90e1,05mna fonte, sem linhas de cota falsas.</desc><style>'+SVG_STYLE+'</style>'+''.join(body)+'</svg>'

CSS='''
.fp-root{--fp-green:#285c49;--fp-ink:#283a32;--fp-muted:#627366;color:var(--fp-ink);font-family:system-ui,sans-serif;max-width:1280px;margin:0 auto;padding:32px 28px 56px}.fp-root *{box-sizing:border-box}.fp-root .fp-eyebrow{color:var(--fp-muted);font-size:11px;letter-spacing:.16em;font-weight:700}.fp-root h1{font:600 clamp(28px,4vw,43px)/1.1 system-ui;margin:12px 0}.fp-root p{line-height:1.6}.fp-intro{max-width:790px;color:var(--fp-muted)}.fp-topline{display:flex;align-items:center;justify-content:space-between;gap:18px}.fp-actions{display:flex;gap:8px;flex-wrap:wrap}.fp-root a.fp-button,.fp-root button{font:600 13px system-ui;border:1px solid #c9d4ca;border-radius:8px;background:#fff;color:var(--fp-green);padding:10px 14px;text-decoration:none;cursor:pointer}.fp-root button[aria-pressed=true]{background:var(--fp-green);border-color:var(--fp-green);color:#fff}.fp-room-nav{display:flex;gap:8px;flex-wrap:wrap;margin:20px 0}.fp-layout{display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:24px;align-items:start}.fp-plan{border:1px solid #d9dfd6;border-radius:14px;background:#fff;padding:18px;min-width:0}.fp-plan svg{display:block;width:100%;height:auto}.fp-key{display:flex;gap:18px;flex-wrap:wrap;color:var(--fp-muted);font-size:12px}.fp-key span::before{content:'';display:inline-block;width:26px;border-top:2px solid #447562;vertical-align:middle;margin-right:7px}.fp-key .fp-key-model::before{border-color:#9a7350;border-top-style:dashed}.fp-context{border:1px solid #d9dfd6;border-radius:14px;padding:22px;background:#f4f5ef;position:sticky;top:16px}.fp-context h2{font-size:20px;line-height:1.25;margin:6px 0 15px}.fp-context .fp-datum{font-size:25px;line-height:1.25;letter-spacing:-.02em;font-weight:600;margin:12px 0 8px}.fp-context p{font-size:13px;margin:8px 0}.fp-source{border-top:1px solid #d6ded3;padding-top:12px;margin-top:18px;font-size:12px;color:var(--fp-muted)}.fp-context a,.fp-root .fp-detail a{color:var(--fp-green)}.fp-detail{margin-top:24px;border:1px solid #d9dfd6;border-radius:12px;padding:16px 20px;background:#fff}.fp-detail summary{cursor:pointer;font-weight:600}.fp-tablewrap{overflow-x:auto}.fp-root table{border-collapse:collapse;width:100%;font-size:13px;margin-top:16px}.fp-root th,.fp-root td{text-align:left;vertical-align:top;padding:12px 10px;border-bottom:1px solid #e1e5dd;line-height:1.5}.fp-root th{font-size:11px;text-transform:uppercase;letter-spacing:.04em;color:var(--fp-muted)}.fp-root tr.fp-current{background:#edf3eb}.fp-difference{border-left:3px solid #a8865b;padding-left:14px;color:#66543e}.fp-original{width:100%;height:auto;border:1px solid #ddd;margin-top:16px}.fp-root .fp-linkrow{display:flex;gap:18px;flex-wrap:wrap;font-size:13px}.fp-root :focus-visible{outline:3px solid #8baa91;outline-offset:3px}@media(max-width:850px){.fp-layout{grid-template-columns:1fr}.fp-context{position:static}.fp-topline{display:block}.fp-actions{margin-top:16px}.fp-root{padding:24px 16px}.fp-plan{padding:5px}.fp-room-nav{flex-wrap:nowrap;overflow-x:auto;padding-bottom:7px}.fp-room-nav button{white-space:nowrap}.fp-context .fp-datum{font-size:23px}}@media print{body{background:white!important}.fp-root{max-width:none;padding:0}.fp-topline,.fp-layout{display:block}.fp-actions,.fp-room-nav,.fp-original-detail{display:none!important}.fp-plan{border:0;padding:0;max-width:175mm;margin:auto}.fp-context{position:static;border:0;padding:8px 0;background:white;page-break-inside:avoid}.fp-detail{border:0;padding:0}.fp-detail>summary{list-style:none}.fp-root table{font-size:9pt}.fp-root h1{font-size:22pt}.fp-intro{font-size:10pt}.fp-muted{opacity:1!important}.fp-root .fp-note-print{display:block}.fp-root .fp-difference{font-size:9pt}.fp-root .fp-context{display:none}.fp-official-table{break-before:page}}
'''

svg=make_svg()
payload={'svg':svg,'css':CSS,'rooms':ROOMS,'cotas':COTAS,'note':NOTE,'pdfPath':PDF,'artifactRoot':'05_Entregas/Planta_cotada_R13/'}
JS=r'''
/* Planta cotada: dimensões oficiais separadas da reconstrução do visualizador. */
(()=>{
 const D=__PAYLOAD__;
 const safe=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 const standalone=!!document.querySelector('[data-floorplan-standalone]');
 function docPath(path){
  if(standalone){if(path.startsWith(D.artifactRoot))return path.slice(D.artifactRoot.length);return '../../'+path;}
  if(location.protocol==='file:'&&location.pathname.replace(/\\/g,'/').includes('/01_Projeto/Estudo_interativo/'))return '../../'+path;
  if(typeof workDocBase!=='undefined')return workDocBase+path;
  return 'docs/'+path;
 }
 const style=document.createElement('style');style.textContent=D.css;document.head.append(style);
 const root=standalone?document.querySelector('[data-floorplan-standalone]'):document.createElement('section');
 root.id='floorplan';root.className='fp-root'+(standalone?'':' tabpage');
 if(!standalone){
  const nav=document.querySelector('.mast nav');if(!nav)return;
  const button=nav.querySelector('[data-tab="floorplan"]')||document.createElement('button');button.type='button';button.dataset.tab='floorplan';button.textContent='Planta cotada';button.setAttribute('aria-pressed','false');
  button.onclick=()=>{if(typeof tab==='function')tab('floorplan');};if(!button.isConnected)nav.append(button);
  const footer=document.querySelector('footer');if(footer)footer.before(root);else document.body.append(root);
 }
 root.innerHTML=`<div class="fp-topline"><div><span class="fp-eyebrow">ENTRE PAREDES · PLANTA OFICIAL</span><h1>Medidas do apartamento.</h1></div><div class="fp-actions">${standalone?'<button data-fp-print>Imprimir / salvar PDF</button>':`<a class="fp-button" href="${safe(docPath(D.artifactRoot+'index.html'))}" target="_blank" rel="noopener">Abrir guia para imprimir</a>`}<a class="fp-button" href="${safe(docPath(D.pdfPath))}" target="_blank" rel="noopener">Planta oficial ↗</a></div></div><p class="fp-intro">Escolha um ambiente para destacar suas cotas. Valores em metros; a vista sem móveis deixa as paredes e os trechos de medida em primeiro plano.</p><nav class="fp-room-nav" aria-label="Ambiente da planta cotada">${D.rooms.map(([id,title])=>`<button type="button" data-fp-filter="${id}" aria-pressed="${id==='all'}">${safe(title)}</button>`).join('')}</nav><div class="fp-layout"><div class="fp-plan">${D.svg}<div class="fp-key"><span>Cota escrita na planta oficial</span><span class="fp-key-model">Medida da reconstrução</span></div></div><aside class="fp-context" aria-live="polite"></aside></div><details class="fp-detail fp-official-table" open><summary>Todas as cotas oficiais</summary><div class="fp-tablewrap"><table><thead><tr><th>Ambiente / trecho</th><th>Cota oficial</th><th>Como usar</th></tr></thead><tbody>${D.cotas.map(c=>`<tr data-fp-row="${c.id}"><td>${safe(c.title)}</td><td><strong>${safe(c.official)}</strong></td><td>${safe(c.scope)}</td></tr>`).join('')}</tbody></table></div><p class="fp-source">Fonte: Planta_oficial.pdf · página 1 · apartamento tipo do 4º ao 16º pavimento, Torre 2, final 06. ${safe(D.note)}</p></details><details class="fp-detail"><summary>Diferenças da reconstrução</summary><p class="fp-difference"><strong>Área de serviço:</strong> a planta informa 1,54 m; a reconstrução do site tem 1,61 m no segundo eixo. A diferença de 7 cm permanece indicada. A cota oficial de 1,54 m fica na tabela, sem deslocar seus extremos para fingir correspondência.</p><p class="fp-difference"><strong>Circulação:</strong> 0,90 m e 1,05 m são trechos cotados na fonte. A faixa reconstruída de 1,30 × 0,90 m é um envelope de desenho; não substitui a cota de 1,05 m nem define um retângulo oficial.</p><p>Paredes, portas e janelas são apoio gráfico reconstituído; espessuras e posições não cotadas não recebem status de medida oficial. Os limites abertos da cozinha e da área de serviço não representam novas paredes. Confira os pontos de referência na fonte antes do levantamento ou da fabricação.</p></details><details class="fp-detail fp-original-detail"><summary>Conferir a página original</summary><p>Imagem integral da página, sem recortar nem alterar as cotas.</p><img class="fp-original" src="${safe(docPath(D.artifactRoot+'Planta_oficial.png'))}" loading="lazy" alt="Página integral da planta oficial Cury, com os valores originais e a legenda."><p class="fp-linkrow"><a href="${safe(docPath(D.pdfPath))}" target="_blank" rel="noopener">Abrir PDF original</a><a href="${safe(docPath(D.artifactRoot+'Planta_cotada.svg'))}" target="_blank" rel="noopener">Abrir desenho SVG</a></p></details>`;
 function selectRoom(id){
  if(!D.rooms.some(r=>r[0]===id))id='all';
  root.dataset.selectedRoom=id;
  root.querySelectorAll('[data-fp-filter]').forEach(b=>b.setAttribute('aria-pressed',b.dataset.fpFilter===id));
  root.querySelectorAll('[data-fp-room]').forEach(el=>{const yes=id==='all'||el.dataset.fpRoom.split(' ').includes(id);el.classList.toggle('fp-muted',!yes);el.classList.toggle('fp-picked',id!=='all'&&yes);});
  root.querySelectorAll('[data-fp-row]').forEach(el=>el.classList.toggle('fp-current',id!=='all'&&el.dataset.fpRow.split(' ').includes(id)));
  const entries=D.cotas.filter(c=>c.id.split(' ').includes(id));
  root.querySelector('.fp-context').innerHTML=id==='all'?'<span class="fp-eyebrow">CONSULTA RÁPIDA</span><h2>Uma medida por vez.</h2><p>Selecione o cômodo no desenho ou use os botões acima. As paredes e as cotas relacionadas ganham destaque.</p><p class="fp-difference">Há diferenças documentadas na área de serviço e na circulação. As duas origens ficam identificadas.</p><div class="fp-source">Fonte oficial: página 1.<br>Desenho: reconstrução do site, sem móveis.</div>':`<span class="fp-eyebrow">${safe(D.rooms.find(r=>r[0]===id)[1])}</span>${entries.map(c=>`<h2>${safe(c.title)}</h2><p class="fp-datum">${safe(c.official)}</p><p>${safe(c.scope)}</p><p${['lavanderia','circulacao'].includes(id)?' class="fp-difference"':''}>${safe(c.match)}</p>`).join('')}<div class="fp-source">Cota documental · não é medição de campo.<br><a href="${safe(docPath(D.pdfPath))}" target="_blank" rel="noopener">Conferir planta oficial, página 1 ↗</a></div>`;
 }
 root.querySelectorAll('[data-fp-filter]').forEach(b=>b.addEventListener('click',()=>selectRoom(b.dataset.fpFilter)));
 root.querySelectorAll('[data-fp-select]').forEach(el=>{el.addEventListener('click',()=>selectRoom(el.dataset.fpSelect));el.addEventListener('keydown',event=>{if(event.key==='Enter'||event.key===' '){event.preventDefault();selectRoom(el.dataset.fpSelect);}});});
 const print=root.querySelector('[data-fp-print]');if(print)print.onclick=()=>{root.querySelectorAll('details:not(.fp-original-detail)').forEach(el=>el.open=true);selectRoom('all');window.print();};
 selectRoom('all');window.GuedalaFloorplan={selectRoom,data:D};
})();
'''.replace('__PAYLOAD__',json.dumps(payload,ensure_ascii=False,separators=(',',':')))

def build():
 OUT.mkdir(parents=True,exist_ok=True)
 assert SCREEN.is_file() and (ROOT/PDF).is_file()
 if SCREEN.resolve() != (OUT/'Planta_oficial.png').resolve():
  shutil.copyfile(SCREEN,OUT/'Planta_oficial.png')
 (OUT/'Planta_cotada.svg').write_text(svg,encoding='utf-8')
 data={'source':{'path':PDF,'page':1,'method':'Cotas escritas conferidas visualmente na página integral.'},'units':'mm in arrays; displayed in metres','cotas':COTAS,'reconstructionSource':'01_Projeto/Estudo_interativo/src/app.js: floors/walls','note':NOTE}
 (OUT/'Cotas.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
 (STUDY/'src/floorplan-ui.js').write_text(JS,encoding='utf-8')
 # Pre-render the entire guide: the technical-documents publisher intentionally
 # strips scripts. The source HTML is enhanced when scripts are available, while
 # the published read-only copy remains useful, styled and printable.
 static_svg=re.sub(r' tabindex="0" role="button"','',svg)
 rows=''.join('<tr><td>'+escape(c['title'])+'</td><td><strong>'+escape(c['official'])+'</strong></td><td>'+escape(c['scope'])+'</td></tr>' for c in COTAS)
 static='<div class="fp-topline"><div><span class="fp-eyebrow">ENTRE PAREDES · PLANTA OFICIAL</span><h1>Medidas do apartamento.</h1></div><a class="fp-button" href="../../'+PDF+'">Abrir planta oficial ↗</a></div><p class="fp-intro">Guia de consulta e impressão. Para destacar cômodos e suas cotas, use a aba “Planta cotada” do site. No navegador, imprimir ou salvar PDF: Ctrl+P.</p><div class="fp-plan">'+static_svg+'<div class="fp-key"><span>Cota escrita na planta oficial</span><span class="fp-key-model">Medida da reconstrução</span></div></div><section class="fp-detail fp-official-table"><h2>Todas as cotas oficiais</h2><div class="fp-tablewrap"><table><thead><tr><th>Ambiente / trecho</th><th>Cota oficial</th><th>Como usar</th></tr></thead><tbody>'+rows+'</tbody></table></div><p class="fp-source">Fonte: Planta_oficial.pdf · página 1 · apartamento tipo do 4º ao 16º pavimento, Torre 2, final 06. '+escape(NOTE)+'</p></section><section class="fp-detail"><h2>Diferenças da reconstrução</h2><p class="fp-difference"><strong>Área de serviço:</strong> 1,54 m na fonte oficial e 1,61 m na reconstrução. A diferença de 7 cm não foi escondida: a cota oficial fica na tabela, sem deslocar os extremos da linha para fingir correspondência.</p><p class="fp-difference"><strong>Circulação:</strong> 0,90 m e 1,05 m são trechos oficiais. A faixa reconstruída de 1,30 × 0,90 m é um envelope de desenho, não um retângulo oficial nem substituto da cota 1,05 m.</p><p>Paredes, portas e janelas são apoio gráfico reconstituído; espessuras e posições não cotadas não são medidas oficiais. Limites abertos entre ambientes não representam novas paredes.</p></section><details class="fp-detail fp-original-detail"><summary>Conferir a página original</summary><img class="fp-original" src="Planta_oficial.png" alt="Página integral da planta oficial, sem recortes"><p class="fp-linkrow"><a href="../../'+PDF+'">Abrir PDF original</a><a href="Planta_cotada.svg">Abrir desenho SVG</a><a href="Cotas.json">Dados das cotas</a></p></details>'
 html='<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Guedala Park · Planta cotada</title><style>body{margin:0;background:#fafaf6}'+CSS+'</style></head><body><main class="fp-root" data-floorplan-standalone>'+static+'</main><script>'+JS+'</script></body></html>'
 (OUT/'index.html').write_text(html,encoding='utf-8')
 print(json.dumps({'directory':str(OUT),'officialRows':len(COTAS),'files':['index.html','Planta_cotada.svg','Planta_oficial.png','Cotas.json'],'ui':'src/floorplan-ui.js'},ensure_ascii=False))
if __name__=='__main__':build()
