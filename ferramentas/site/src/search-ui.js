/* Resultados locais: navegação até o registro, sem requisição de rede. */
;(function(){
 const api=GuedalaSearch,index=GUEDALA_SEARCH_INDEX,e=esc;
 const header=document.querySelector('.mast');
 header.insertAdjacentHTML('beforeend','<div class="global-search"><label class="sr-only" for="globalSearch">Buscar em todo o projeto</label><div class="global-search-input"><input id="globalSearch" type="search" placeholder="Buscar no projeto · /" autocomplete="off" aria-controls="globalSearchResults" aria-expanded="false"><button id="globalSearchClear" aria-label="Limpar busca" hidden>×</button></div><div id="globalSearchResults" class="global-search-results" aria-label="Resultados da busca" hidden></div></div>');
 const input=document.getElementById('globalSearch'),results=document.getElementById('globalSearchResults'),clear=document.getElementById('globalSearchClear');
 const types={pending:'Pendência',choice:'Escolha',room:'Cômodo',module:'Móvel / ficha',document:'Documento',glossary:'Glossário',download:'Download'};
 const tabs={architect:'Comece aqui',model:'Apartamento',decisions:'Escolhas',documents:'Documentos'};
 function focus(id){const el=document.getElementById(id);if(!el)return;for(let parent=el.parentElement;parent;parent=parent.parentElement)if(parent.tagName==='DETAILS')parent.open=true;el.tabIndex=-1;el.scrollIntoView({block:'center'});el.focus({preventScroll:true});}
 function choose(r){
  results.hidden=true;input.setAttribute('aria-expanded','false');
  api.navigate(r,{tab,
   pending:r=>{GuedalaResponsibilities.filter('todos');if(r.item)document.getElementById('ownerRoomDetails').open=true;focus(r.item?'owner-'+encodeURIComponent(r.item):'arch-'+r.id);},
   choice:r=>{document.getElementById('filterRoom').value='all';document.getElementById('filterStatus').value='all';renderDecisions();focus('choice-'+encodeURIComponent(r.id));},
   room:r=>{setRoom(r.id);setView('iso');focus('scene');},
   module:r=>{GuedalaWorkshop.showModule(r.id);focus('selectedInfo');},
   document:r=>{document.getElementById('docSearch').value=r.title;document.getElementById('docRoom').value='all';document.getElementById('docCategory').value='all';GuedalaWorkshop.drawDocuments();focus('doc-'+r.id);},
   glossary:r=>globalThis.GuedalaGlossary?.open(r.id),
   download:r=>globalThis.GuedalaDownloads?.show(r.id,'documents')
  });
 }
 function render(){
  clear.hidden=!input.value;const rows=api.find(input.value,index),has=!!api.normalize(input.value);results.hidden=!has;input.setAttribute('aria-expanded',String(has));
  results.innerHTML=!has?'':rows.length?`<p role="status">${rows.length} resultados${rows.length===40?' · refine para ver outros':''}</p><ul>${rows.map(r=>`<li><button data-search-key="${e(r.key)}"><strong>${e(r.title)}</strong><small>${types[r.kind]} · ${tabs[r.tab]}${r.room!=='all'?' · '+e(PROJECT.rooms.find(v=>v.id===r.room)?.name||r.room):''}</small></button></li>`).join('')}</ul>`:'<p role="status"><strong>Nenhum resultado.</strong> Tente um cômodo, P01 ou fixação. Use menos palavras.</p>';
  results.querySelectorAll('[data-search-key]').forEach(b=>b.onclick=()=>choose(index.find(r=>r.key===b.dataset.searchKey)));
 }
 input.addEventListener('input',render);input.addEventListener('focus',render);
 clear.onclick=()=>{input.value='';render();input.focus();};
 document.addEventListener('click',event=>{if(!event.target.closest('.global-search')){results.hidden=true;input.setAttribute('aria-expanded','false');}});
 document.addEventListener('keydown',event=>{
  const editing=event.target.matches('input,textarea,select')||event.target.isContentEditable;
  if(event.key==='/'&&!editing&&!event.ctrlKey&&!event.metaKey&&!event.altKey){event.preventDefault();input.focus();input.select();}
  if(event.key==='Escape'){input.value='';render();}
  if(event.target===input&&event.key==='ArrowDown'){event.preventDefault();results.querySelector('button')?.focus();}
  if(event.target===input&&event.key==='Enter'){event.preventDefault();results.querySelector('button')?.click();}
  if(event.target.closest('#globalSearchResults')&&['ArrowDown','ArrowUp'].includes(event.key)){
   event.preventDefault();const buttons=[...results.querySelectorAll('button')],n=buttons.indexOf(event.target)+(event.key==='ArrowDown'?1:-1);(buttons[n]||input).focus();
  }
 });
 globalThis.GuedalaGlobalSearch={choose,render};
})();
