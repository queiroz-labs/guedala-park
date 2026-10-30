/* Explicações e glossário vêm dos dados, com revisão lida do release. */
;(function(){
 const d=GUEDALA_ARCHITECT,e=esc,header=document.querySelector('.mast');
 document.getElementById('helpButton').textContent='Como explorar';
 header.insertAdjacentHTML('beforeend',`<button id="glossaryButton" class="quiet" aria-label="Glossário de códigos" title="Glossário de códigos">?</button><p class="global-project-notice">${e(d.globalNotice)}</p>`);
 for(const [id,context]of Object.entries(d.tabContexts)){
  const page=document.getElementById(id);if(page)page.insertAdjacentHTML('afterbegin',`<aside class="tab-context"><p><strong>O que é isto</strong> · ${e(context.text)} <span>Referência ${e(context.revision)} · nominal / a confirmar</span></p></aside>`);
 }
 const nav=header.querySelector('nav');nav.querySelector('[data-tab="chaves"]').insertAdjacentHTML('beforebegin','<span class="architect-tools-label">Ferramentas</span>');
 document.body.insertAdjacentHTML('beforeend','<dialog id="glossaryDialog" class="glossary-dialog" aria-labelledby="glossaryTitle"><div class="glossary-heading"><h2 id="glossaryTitle">Códigos do projeto</h2><button id="closeGlossary" aria-label="Fechar glossário">×</button></div><p>Definições usadas neste projeto. Consulte a fonte; uma sigla não comprova conformidade ou execução.</p><label for="glossaryFilter">Encontrar um código ou palavra</label><input id="glossaryFilter" type="search" autocomplete="off" placeholder="P01, RT, fixação…"><div id="glossaryList" class="glossary-list"></div></dialog>');
 const dialog=document.getElementById('glossaryDialog'),filter=document.getElementById('glossaryFilter'),list=document.getElementById('glossaryList');let returnTarget;
 function render(){const query=GuedalaSearch.normalize(filter.value),rows=d.glossary.filter(g=>GuedalaSearch.normalize(g.term+' '+g.definition).includes(query));list.innerHTML=rows.length?rows.map(g=>`<article id="glossary-${g.id}" tabindex="-1"><h3>${e(g.term)}</h3><p>${e(g.definition)}</p><a href="${e(workDocUrl({path:g.path}))}">Fonte da definição →</a></article>`).join(''):'<p role="status">Nenhum código encontrado. Tente uma sigla ou menos palavras.</p>';}
 function open(id,returnTo){returnTarget=returnTo||(id?document.getElementById('globalSearch'):document.activeElement);filter.value='';render();if(!dialog.open)dialog.showModal();if(id)requestAnimationFrame(()=>{const row=document.getElementById('glossary-'+id);row?.scrollIntoView({block:'center'});row?.focus({preventScroll:true});});else filter.focus();}
 document.getElementById('glossaryButton').onclick=()=>open();document.getElementById('closeGlossary').onclick=()=>dialog.close();dialog.addEventListener('close',()=>returnTarget?.focus());filter.addEventListener('input',render);
 dialog.addEventListener('keydown',event=>{if(event.key==='Escape'){event.preventDefault();event.stopPropagation();dialog.close();}});
 const measure=()=>document.documentElement.style.setProperty('--mast-height',header.getBoundingClientRect().height+'px');new ResizeObserver(measure).observe(header);measure();
 globalThis.GuedalaGlossary={open};
 const toolLink=()=>{const id=GuedalaArchitect.hashTab(location.hash,WORK_TABS);let target;try{target=document.getElementById(decodeURIComponent(location.hash.slice(1)));}catch{return;}const page=id||target?.closest('.tabpage')?.id;if(page){tab(page);if(page==='documents')GuedalaWorkshop.drawDocuments();if(target)requestAnimationFrame(()=>target.scrollIntoView({block:'start'}));}};window.addEventListener('hashchange',toolLink);setTimeout(toolLink);
})();
