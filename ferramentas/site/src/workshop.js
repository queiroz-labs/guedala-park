/* Fichas de consulta: medidas derivadas do CAD, sem aprovação implícita de corte. */
const work={module:null,query:'',previousSelect:selectItem,previousRoom:setRoom};
const mm=v=>Number(v).toLocaleString('pt-BR',{maximumFractionDigits:2});
const workPart=s=>CAD_DATA.parts.find(p=>p.source===s);
const workModule=c=>CAD_DATA.modules.find(m=>m.code===c);
const workGuide=m=>(typeof MODULE_GUIDANCE!=='undefined'&&MODULE_GUIDANCE[m.code])||{hardware:['Veja as peças e a montagem na ficha do móvel.'],pending:['Confira as medidas, os cortes, os furos e a fixação.'],finish:'Conferir referência de material de cada peça.',documentIds:[]};
const workDocs=()=>typeof WORKSHOP_DOCS!=='undefined'?WORKSHOP_DOCS:[];
updateMetrics=function(){const m=workModule(work.module);$('metrics').innerHTML=m?(m.dimensionsLocal||m.dimensions).map((v,i)=>`<div class="metric"><b>${mm(v)} mm</b><span>${['Largura','Profundidade','Altura'][i]}</span><small>Medida do desenho</small></div>`).join(''):'<p class="work-note">Escolha um móvel para ver as medidas em milímetros.</p>';$('roomNote').textContent='Confira estas medidas no apartamento. Os espaços internos e as uniões estão na ficha.';};
drawAnnotations=function(ctx,pr,cam,w,h,st){if(!st.measures||!work.module)return;const ps=nodes.filter(n=>n.module===work.module);if(!ps.length)return;let x=Math.min(...ps.map(n=>n.x)),z=Math.min(...ps.map(n=>n.z)),y=Math.min(...ps.map(n=>n.y)),xx=Math.max(...ps.map(n=>n.x+n.w)),zz=Math.max(...ps.map(n=>n.z+n.d)),yy=Math.max(...ps.map(n=>n.y+n.h));if(st.moduleFilter){yy-=y;y=0;}dimension(ctx,pr,[x,y,z-8],[xx,y,z-8],mm((xx-x)*10)+' mm · X');dimension(ctx,pr,[xx+8,y,z],[xx+8,y,zz],mm((zz-z)*10)+' mm · Y');if(st.view!=='top')dimension(ctx,pr,[x-8,y,z],[x-8,yy,z],mm((yy-y)*10)+' mm');};
const workDocBase=window.GUEDALA_WEB?'docs/':location.protocol==='file:'&&!location.pathname.replace(/\\/g,'/').includes('/.site/')?'https://queiroz-labs.github.io/guedala-park/docs/':/\/moodboard\/(?:index\.html)?$/.test(location.pathname)?'../docs/':'docs/';
function workDocUrl(d){
 if(d.available===false)return null;
 if(window.GUEDALA_PACKAGE){if(d.id==='biblioteca-pacote')return GUEDALA_PACKAGE.root+'COMECE_AQUI.html';const files=GUEDALA_PACKAGE.files,target=files.includes(d.path+'.html')?d.path+'.html':files.includes(d.path)?d.path:null;return target?GUEDALA_PACKAGE.root+target:null;}
 if(d.localOnly&&location.protocol==='file:')return '../../'+d.path;
 return workDocBase+d.path+(d.path.endsWith('.md')?'.html':'');
}
function workParts(m){return m.parts.map(workPart).filter(p=>p&&p.piece);}
function workMaterialName(id){return MAT[id]?.name||id||'Não especificado';}
function workMaterialStatus(id){return MAT[id]?.status||'Referência do modelo';}
function workModuleButtons(mods){return mods.map(m=>`<button data-module="${m.code}"><code>${m.code}</code><span>${esc(m.name)}</span><span style="margin-left:auto">↗</span></button>`).join('');}
function bindModuleButtons(parent){parent.querySelectorAll('[data-module]').forEach(b=>b.onclick=()=>showModule(b.dataset.module));}
function roomWorkshop(){
 const mods=CAD_DATA.modules.filter(m=>state.room==='all'||m.room===state.room);
 $('selectedInfo').innerHTML=`<h2>${state.room==='all'?'Escolha um móvel<br>para ver os detalhes.':'Marcenaria<br>deste ambiente.'}</h2><p>Toque no móvel no desenho ou escolha uma ficha. Medidas, peças e ferragens ficam no mesmo lugar.</p><span class="work-count">${mods.length} móveis do projeto</span><div class="work-list">${workModuleButtons(mods)}</div><details class="work-accordion"><summary>Como ler as medidas</summary><p>As fichas usam milímetros. As medidas gerais mostram o espaço ocupado pelo móvel. Antes de cortar, confira os recortes, o sentido da madeira, as bordas e as folgas.</p></details>`;
 bindModuleButtons($('selectedInfo'));
 if(state.room==='all'){
  $('selectedInfo').querySelector('.work-list').innerHTML=PROJECT.rooms.filter(r=>r.id!=='all').map(r=>`<button data-work-room="${r.id}"><span>${esc(r.name)}</span><small style="margin-left:auto;color:var(--muted)">${CAD_DATA.modules.filter(m=>m.room===r.id).length} →</small></button>`).join('');
  $('selectedInfo').querySelectorAll('[data-work-room]').forEach(b=>b.onclick=()=>setRoom(b.dataset.workRoom));
 }
}
function refreshModuleSelect(){const mods=CAD_DATA.modules.filter(m=>state.room==='all'||m.room===state.room);$('workModule').innerHTML='<option value="">Escolha um móvel para consultar</option>'+mods.map(m=>`<option value="${m.code}">${m.code} · ${esc(m.name)}</option>`).join('');if(work.module&&mods.some(m=>m.code===work.module))$('workModule').value=work.module;}
setRoom=function(id){state.moduleFilter=null;state.focusPart=null;work.module=null;work.previousRoom(id);refreshModuleSelect();roomWorkshop();$('workContext').textContent=id==='lavanderia'?'Cafeteira: espaço a definir · medidas pendentes; sem volume no desenho.':'Vista de consulta · toque em um móvel para abrir sua ficha.';};
selectItem=function(id,open=true){
 const mods=CAD_DATA.modules.filter(m=>m.item===id||(id==='laundrybasket'&&m.code==='P14'));
 if(mods.length===1){showModule(mods[0].code);return;}
 if(mods.length>1){state.selected=id;state.moduleFilter=null;state.focusPart=null;work.module=null;$('selectedInfo').innerHTML=`<button class="work-back" id="workBack">← Móveis do ambiente</button><h2>${esc(ITEMS.find(i=>i.id===id)?.name||'Escolha o módulo')}</h2><p>Abra a ficha do módulo que você quer consultar.</p><div class="work-list">${workModuleButtons(mods)}</div>`;bindModuleButtons($('selectedInfo'));$('workBack').onclick=roomWorkshop;requestRender();return;}
 work.previousSelect(id,false);$('inspector').classList.remove('open');$('inspector').removeAttribute('role');$('inspector').removeAttribute('aria-modal');
};
function partsTable(m,print=false){return `<table class="work-table"><thead><tr><th>Peça</th><th>C × L · mm</th><th>Esp.¹</th></tr></thead><tbody>${workParts(m).map(p=>`<tr data-piece-row="${p.source}"><td>${print?esc(p.label):`<button data-piece="${p.source}">${esc(p.label)}</button>`}<small>${esc(p.source)} · ${esc(workMaterialName(p.piece.material))}</small></td><td>${mm(p.piece.dimensions[0])} × ${mm(p.piece.dimensions[1])}${p.piece.rectangular?'':'<small>Contorno / recorte</small>'}</td><td>${mm(p.piece.thickness)}</td></tr>`).join('')}</tbody></table>`;}
function showModule(code){
 const m=workModule(code);if(!m)return;
 if(state.room!==m.room)setRoom(m.room);
 work.module=code;state.selected=m.item;state.moduleFilter=null;state.focusPart=null;$('workModule').value=code;
 const g=workGuide(m),ps=workParts(m),materials=[...new Set(ps.map(p=>p.piece.material))];
 const docs=workDocs().filter(d=>d.path&&g.documentIds.includes(d.id));
 $('selectedInfo').innerHTML=`<button class="work-back" id="workBack">← Móveis do ambiente</button><div class="work-subtitle">${code} · ${esc(PROJECT.rooms.find(r=>r.id===m.room).name)}</div><h2>${esc(m.name)}</h2><span class="work-status">Conferir antes de fabricar</span><div class="work-measures">${(m.dimensionsLocal||m.dimensions).map((v,i)=>`<div><b>${mm(v)}</b><span>${['Largura','Profundidade','Altura'][i]} · mm</span></div>`).join('')}</div><p class="work-note">Medidas gerais do móvel no desenho. Consulte abaixo as medidas das peças e dos espaços internos.</p>${materials.map(id=>`<div class="work-material"><i style="background:${MAT[id]?.color||'#c4b9a8'}"></i><span>${esc(workMaterialName(id))}<small>${esc(workMaterialStatus(id))}</small></span></div>`).join('')}<details class="work-accordion"><summary>Peças e espessuras <span class="work-subtitle">· ${ps.length}</span></summary><p>Toque no nome de uma peça para vê-la no 3D.</p><div class="work-table-wrap">${partsTable(m)}</div><p class="work-note">¹ A espessura vem do desenho. Confira a chapa real antes de cortar. As medidas ainda não descontam bordas, recortes ou folgas.</p><div class="work-actions"><button id="exportPieces">Baixar lista de peças · CSV</button></div></details><details class="work-accordion"><summary>Peças e uniões de montagem</summary><ul>${g.hardware.map(t=>`<li>${esc(t)}</li>`).join('')}</ul><p class="work-note">Confirme as peças, as quantidades e os furos antes de comprar ou fabricar.</p></details><details class="work-accordion"><summary>Acabamento e montagem</summary><p>${esc(g.finish)}</p><ul>${g.pending.map(t=>`<li>${esc(t)}</li>`).join('')}</ul></details><details class="work-accordion"><summary>Estudos deste móvel</summary>${docs.length?docs.map(d=>workDocUrl(d)?`<p><a href="${workDocUrl(d)}" target="_blank" rel="noopener">${esc(d.title)} ↗</a></p>`:`<p>${esc(d.title)} · fonte não incluída neste pacote</p>`).join(''):'<p>Consulte a matriz de módulos na documentação.</p>'}<p><a href="${workDocUrl({path:CAD_DATA.current_source_path,localOnly:true})}" download>Baixar FreeCAD ${esc(CAD_DATA.current_revision)} · modelo corrente</a></p></details><div class="work-actions"><button id="isolateModule" class="work-primary" aria-pressed="false">Isolar no 3D</button><button id="printModule">Imprimir ficha</button></div>`;
 $('workBack').onclick=()=>{state.moduleFilter=null;state.focusPart=null;work.module=null;state.selected=null;$('workModule').value='';roomWorkshop();requestRender();};
 $('selectedInfo').querySelector('a[download]').href=workDocUrl({path:CAD_DATA.current_source_path,localOnly:true});
 $('isolateModule').onclick=()=>{state.moduleFilter=state.moduleFilter?null:code;$('isolateModule').textContent=state.moduleFilter?'Ver no ambiente':'Isolar no 3D';$('isolateModule').setAttribute('aria-pressed',String(!!state.moduleFilter));requestRender();};
 $('printModule').onclick=()=>printModule(m);$('exportPieces').onclick=()=>exportPieces(m);
 const panelPieceButtons=$('selectedInfo').querySelectorAll('[data-piece],[data-piece-group]');
 panelPieceButtons.forEach(b=>b.onclick=()=>{const ids=(b.dataset.pieceGroup||b.dataset.piece).split('|');state.focusPart=ids.length===1?ids[0]:ids;state.moduleFilter=code;$('isolateModule').textContent='Ver no ambiente';$('isolateModule').setAttribute('aria-pressed','true');document.querySelectorAll('[data-piece-row]').forEach(r=>r.classList.toggle('is-focused',(r.dataset.pieceIds||r.dataset.pieceRow).split('|').some(id=>ids.includes(id))));$('workContext').textContent=(ids.length===1?workPart(ids[0]).label:ids.length+' peças equivalentes')+' · destaque em ocre';requestRender();});
 $('workContext').textContent=`${code} · ${m.name} · ${ps.length} peças com medidas no projeto`;
 updateMetrics();
 requestRender();
}
function exportPieces(m){const rows=[['Módulo','ID CAD','Peça','Comprimento envelope mm','Largura envelope mm','Espessura envelope mm','Material','Forma','Status'],...workParts(m).map(p=>[m.code,p.source,p.label,...p.piece.dimensions,workMaterialName(p.piece.material),p.piece.rectangular?'Retangular':'Contorno/recorte','Consulta R45; conferir antes de cortar'])];const csv='\ufeff'+rows.map(r=>r.map(v=>'"'+String(v).replace(/"/g,'""')+'"').join(';')).join('\r\n');download(new Blob([csv],{type:'text/csv;charset=utf-8'}),`Guedala_${m.code}_pecas_R45.csv`);}
function printModule(m){const g=workGuide(m);$('workPrint').innerHTML=`<h1>${m.code} · ${esc(m.name)}</h1><p>Guedala Park · Ficha do móvel · Unidades: mm</p><p class="stamp">Conferir antes de fabricar. Medidas do desenho. Confira as peças, as bordas, os furos e a montagem antes de cortar.</p><h2>Envelope nominal · largura × profundidade × altura</h2><p>${(m.dimensionsLocal||m.dimensions).map(mm).join(' × ')} mm</p><h2>Peças · comprimento × largura × menor espessura do envelope local</h2>${partsTable(m,true)}<h2>Peças e uniões de montagem</h2><ul>${g.hardware.map(s=>`<li>${esc(s)}</li>`).join('')}</ul><h2>Acabamento e montagem</h2><p>${esc(g.finish)}</p><ul>${g.pending.map(s=>`<li>${esc(s)}</li>`).join('')}</ul><p>Fonte: modelo FreeCAD ${esc(CAD_DATA.current_revision)} · SHA256 ${CAD_DATA.source_sha256}</p>`;window.print();}
function drawDocuments(){
 const query=$('docSearch').value.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase(),room=$('docRoom').value,category=$('docCategory').value,packaged=!!window.GUEDALA_PACKAGE;
 const browsing=!query&&room==='all'&&category==='all',roomCards=workDocs().filter(d=>!d.internal&&d.category==='Por ambiente');
 $('docRooms').innerHTML=browsing&&roomCards.length?'<span>Documentos por cômodo:</span>'+roomCards.map(d=>workDocUrl(d)?`<a href="${workDocUrl(d)}">${esc(d.title)}</a>`:'').join(''):'';
 const docs=workDocs().filter(d=>!d.internal&&!(browsing&&d.category==='Por ambiente')&&(room==='all'||d.rooms.includes(room)||d.rooms.includes('all'))&&(category==='all'||category===d.category)&&`${d.title} ${d.summary} ${d.category} ${d.searchTerms||''}`.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().includes(query));
 $('docCount').textContent=`${docs.length} ${docs.length===1?'acesso':'acessos'} para consultar o projeto`;
 $('docCards').innerHTML=docs.length?docs.map(d=>`<article id="doc-${d.id}" class="work-doc"><p class="eyebrow">${esc(d.category)}</p><h2>${esc(d.title)}</h2><span class="work-status">${esc(d.status)}</span><p class="work-doc-summary">${esc(d.summary)}</p>${d.path&&workDocUrl(d)?`<a href="${workDocUrl(d)}" ${d.id==='biblioteca-pacote'&&!packaged?'download':d.generated?'':'target="_blank" rel="noopener"'} aria-label="${esc(d.id==='biblioteca-pacote'?(packaged?'Abrir índice do pacote':'Baixar pacote ZIP'):'Ver documentos: '+d.title)}">${d.id==='biblioteca-pacote'?(packaged?'Abrir índice do pacote':'Baixar pacote · ZIP'):(d.generated?'Ver documentos →':'Ver documentos ↗')}</a>`:'<p>Não incluído nesta cópia do pacote.</p>'}</article>`).join(''):'<div class="work-empty">Nenhum resultado. Tente outro termo ou ambiente.</div>';
}
const WORK_TABS={apartamento:'model',ambientes:'model',comodos:'mood','cômodos':'mood',materiais:'mood',escolhas:'decisions',documentos:'documents',planta:'floorplan',chaves:'chaves',obra:'obra'};
function initializeWorkshop(){
 document.querySelector('.welcome-copy h1').textContent='Conheça o projeto do apartamento.';
 document.querySelector('.welcome-copy p').textContent='Escolha um ambiente. Toque em um móvel para ver medidas, materiais e montagem.';
 document.querySelector('.welcome .eyebrow').textContent='GUEDALA PARK / PROJETO DO APARTAMENTO';
 document.querySelector('.sidebar h2').textContent='Ambientes';
 document.querySelector('[data-view="iso"]').textContent='3D';
 document.querySelector('.inspector-header .section-label').textContent='FICHA DO MÓVEL';
 document.querySelector('.stage-tag').textContent='Desenho do projeto · cores aproximadas';
 $('measureToggle').parentElement.lastChild.textContent=' Medidas do móvel · mm';
 document.querySelector('.assumptions').hidden=true;
 $('workModule').onchange=e=>{if(e.target.value)showModule(e.target.value);else{state.moduleFilter=null;state.focusPart=null;work.module=null;state.selected=null;roomWorkshop();requestRender();}};
 $('workSeeDetails').onclick=()=>$('inspector').scrollIntoView({behavior:'smooth',block:'start'});
 document.querySelector('[data-tab="model"]').textContent='Apartamento';document.querySelector('[data-tab="decisions"]').textContent='Escolhas';document.querySelector('[data-tab="mood"]').textContent='Cômodos';
 document.querySelector('footer').insertAdjacentHTML('beforebegin',`<section id="documents" class="tabpage work-library"><span class="eyebrow">BIBLIOTECA DO PROJETO</span><h1>O que você quer consultar?</h1><p>Comece pelo assunto. As fichas, os estudos e os documentos de origem ficam reunidos em cada acesso.</p><div class="work-filters"><input id="docSearch" class="work-search" type="search" aria-label="Buscar no projeto" placeholder="Buscar: espelheiro, ferragem, piso…"><select id="docRoom" aria-label="Filtrar ambiente">${PROJECT.rooms.map(r=>`<option value="${r.id}">${r.id==='all'?'Todos os ambientes':esc(r.name)}</option>`).join('')}</select><select id="docCategory" aria-label="Filtrar assunto"><option value="all">Todos os assuntos</option>${[...new Set(workDocs().filter(d=>!d.internal).map(d=>d.category))].map(c=>`<option>${esc(c)}</option>`).join('')}</select></div><p id="docCount" class="work-doc-count" aria-live="polite"></p><p id="docRooms" class="doc-rooms"></p><div id="docCards" class="work-docs"></div></section><section id="workPrint" class="work-print"></section>`);
 ['docSearch','docRoom','docCategory'].forEach(id=>$(id).addEventListener(id==='docSearch'?'input':'change',drawDocuments));
 document.querySelectorAll('[data-tab]').forEach(b=>b.onclick=()=>{tab(b.dataset.tab);if(b.dataset.tab==='documents')drawDocuments();});
 document.querySelector('#decisions .doc-title p').textContent='Veja as escolhas e o que falta conferir. Abra a ficha do móvel para ver os detalhes.';
 document.querySelector('footer').innerHTML='GUEDALA PARK · Projeto do apartamento <span>Medidas em milímetros · confira antes de fabricar</span>';
 window.GuedalaStudy.setRoom=setRoom;window.GuedalaStudy.selectItem=selectItem;window.GuedalaWorkshop={showModule,work,drawDocuments,exportPieces,workParts};
 const show=syncExperience;syncExperience=function(){show();};
 setRoom('all');
 // Endereços antigos continuam válidos: ?aba=materiais e ?aba=planta levam ao lugar novo.
 const target=WORK_TABS[(new URLSearchParams(location.search).get('aba')||'').toLowerCase()];
 if(target)setTimeout(()=>{tab(target);if(target==='documents')drawDocuments();});
}
initializeWorkshop();
