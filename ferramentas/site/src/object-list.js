/* Inventário da cena atual. CSV gerado em memória a partir dos mesmos nós. */
let objectRows=[];
function filteredObjectRows(){const term=($('objectSearch')?.value||'').toLocaleLowerCase('pt-BR'),room=$('objectRoom')?.value||state.room,category=$('objectCategory')?.value||'all';return objectRows.filter(r=>(room==='all'||r.roomId===room)&&(category==='all'||r.category===category)&&[r.name,r.id,r.key,r.module,r.reference].join(' ').toLocaleLowerCase('pt-BR').includes(term));}
function revealObjectRow(r){
 if($('objectRoom').value!=='all'&&$('objectRoom').value!==r.roomId)$('objectRoom').value=r.roomId;
 if($('objectCategory').value!=='all'&&$('objectCategory').value!==r.category)$('objectCategory').value='all';
 objectRows=objectRecords();if(!filteredObjectRows().some(q=>q.key===r.key))$('objectSearch').value='';
 $('objectMeasureList').open=true;drawObjectList();
}
function drawObjectList(){
 if(!$('objectMeasureRows'))return;objectRows=objectRecords();const list=filteredObjectRows();
 $('objectMeasureRows').innerHTML=list.map(r=>`<tr data-object-row="${esc(r.key)}" ${r.key===objectSelected?'aria-selected="true"':''}><td><button type="button" data-object-select="${esc(r.key)}">${esc(r.name)}</button><small>${esc(r.module||r.id||r.key)}</small></td><td>${esc(r.room)}</td><td>${esc(r.category)}</td>${['w','d','h'].map(k=>`<td>${r.box?cmTxt(r.box[k]):'—'}</td>`).join('')}<td>${esc(r.reliability)}</td></tr>`).join('');
 $('objectMeasureCount').textContent=list.length+' objetos · medidas em cm';
 $('objectMeasureRows').querySelectorAll('[data-object-select]').forEach(b=>b.onclick=()=>{const r=objectRows.find(r=>r.key===b.dataset.objectSelect);if(r.roomId!==state.room)setRoom(r.roomId);inspectObject(r.node);$('scene').scrollIntoView({block:'center',behavior:'instant'});});
 const selected=$('objectMeasureRows').querySelector('[aria-selected="true"]');if(selected)$('objectMeasureTable').scrollTop=Math.max(0,selected.offsetTop-80);
}
function objectCSV(rows=filteredObjectRows()){
 const quote=v=>'"'+String(v??'').replaceAll('"','""')+'"';
 return '\ufeff'+[['cômodo','categoria','nome','L','P','A','x','y','z','confiabilidade','confiabilidade da posição','referência','id'],...rows.map(r=>[r.room,r.category,r.name,...['w','d','h','x','y','z'].map(k=>r.box?cmTxt(r.box[k]):''),r.reliability,r.box?OBJECT_GRAPHIC:'pendente',r.reference,r.key])].map(row=>row.map(quote).join(';')).join('\r\n');
}
function syncObjectList(id){$('objectRoom').value=id;drawObjectList();}
function initializeObjectList(){
 const panel=document.createElement('details');panel.id='objectMeasureList';panel.className='object-measure-list';panel.innerHTML='<summary>Objetos do cômodo</summary><p>Selecione uma linha para destacar o objeto no desenho. Largura no eixo x; profundidade no eixo z; altura no eixo y.</p><div class="object-filters"><label>Buscar objeto<input type="search" id="objectSearch" placeholder="Nome ou referência"></label><label>Cômodo<select id="objectRoom"></select></label><label>Categoria<select id="objectCategory"><option value="all">Todas</option></select></label><button type="button" id="objectCSV">Baixar CSV</button></div><p id="objectMeasureCount" role="status"></p><div id="objectMeasureTable" class="object-table-scroll" tabindex="0" role="region" aria-label="Medidas de todos os objetos"><table><thead><tr><th>Objeto</th><th>Cômodo</th><th>Categoria</th><th>L · cm</th><th>P · cm</th><th>A · cm</th><th>Confiabilidade</th></tr></thead><tbody id="objectMeasureRows"></tbody></table></div>';
 document.querySelector('#model .workspace').appendChild(panel);
 $('objectRoom').innerHTML=PROJECT.rooms.map(r=>`<option value="${esc(r.id)}">${esc(r.name)}</option>`).join('');
 objectRows=objectRecords();$('objectCategory').insertAdjacentHTML('beforeend',[...new Set(objectRows.map(r=>r.category))].sort().map(c=>`<option>${esc(c)}</option>`).join(''));
 $('objectSearch').oninput=drawObjectList;$('objectRoom').onchange=drawObjectList;$('objectCategory').onchange=drawObjectList;
 $('objectCSV').onclick=()=>download(new Blob([objectCSV()],{type:'text/csv;charset=utf-8'}),'Objetos_do_comodo.csv');
 $('stage').insertAdjacentHTML('afterend','<a class="object-list-link" href="#objectMeasureList">Objetos do cômodo ↓</a>');
 drawObjectList();
 const beforeScene=buildScene;buildScene=function(){const out=beforeScene();drawObjectList();return out;};
 Object.assign(window.GuedalaStudy,{objectCSV});
}
initializeObjectList();
