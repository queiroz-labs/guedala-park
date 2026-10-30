/* Selos explicam os dados de origem; escolhas e responsabilidades não são alteradas. */
;(function(){
 const d=GUEDALA_ARCHITECT,e=esc,rows=[...d.disciplines,...d.itemResponsibilities];
 const definitions=new Map(d.statusHelp.flatMap(s=>s.labels.map(label=>[label,s])));
 document.getElementById('statusHelp')?.remove();
 document.body.insertAdjacentHTML('beforeend','<div id="statusHelp" class="status-popover" popover="auto" role="dialog" aria-labelledby="statusHelpTitle" tabindex="-1"></div>');
 const pop=document.getElementById('statusHelp');let trigger;
 function explain(button){
  const def=definitions.get(button.dataset.statusLabel);if(!def)return;
  trigger?.setAttribute('aria-expanded','false');trigger=button;const rowId=button.closest('[data-owner-row]')?.dataset.ownerRow,item=button.dataset.statusItem;
  const row=rows.find(r=>(rowId&&r.id===rowId)||(item&&r.item===item));
  const owner=button.dataset.statusLabel==='a definir'?'Quem decide: responsável a definir':row?'Papéis registrados: '+row.owners.map(o=>o==='a definir'?'responsável a definir':o).join(', '):'';
  const source=button.dataset.statusSource||(row&&(row.ownerSource||row.source))||def.path;
  pop.innerHTML=`<div class="status-help-heading"><h2 id="statusHelpTitle">${e(def.label)}</h2><button type="button" data-status-close aria-label="Fechar explicação">×</button></div><p>${e(def.definition)}</p>${owner?`<p>${e(owner)}</p>`:''}<a href="${e(workDocUrl({path:source}))}">Fonte no projeto →</a><button type="button" data-status-glossary="${e(def.id)}">Ver no glossário →</button>`;
  if(!pop.matches(':popover-open'))pop.showPopover();button.setAttribute('aria-expanded','true');pop.focus({preventScroll:true});
 }
 function decorate(root=document){
  root.querySelectorAll('.badge,.status-original,.owner-badges span,.owner-badges strong,.work-status,.work-material small,.fab-decision>small,.fab-finish>small').forEach(node=>{
   if(node.matches('button'))return;const label=node.textContent.trim(),def=definitions.get(label);if(!def)return;
   const button=document.createElement('button');button.type='button';button.className=node.className+' status-help-trigger';
   for(const name of ['data-status-item','data-status-source'])if(node.hasAttribute(name))button.setAttribute(name,node.getAttribute(name));
   button.dataset.statusLabel=label;button.textContent=def.label;button.setAttribute('aria-label',def.label+': explicar');button.setAttribute('aria-haspopup','dialog');button.setAttribute('aria-controls','statusHelp');button.setAttribute('aria-expanded','false');node.replaceWith(button);
   if(label==='a definir'){const note=document.createElement('small');note.className='status-owner-note';note.textContent='Quem decide: responsável a definir';button.after(note);}
  });
 }
 document.addEventListener('click',event=>{
  const button=event.target.closest('.status-help-trigger');if(button){event.preventDefault();event.stopPropagation();explain(button);return;}
  if(event.target.closest('[data-status-close]')){pop.hidePopover();trigger?.focus({preventScroll:true});}
  const glossary=event.target.closest('[data-status-glossary]');if(glossary){pop.hidePopover();GuedalaGlossary.open(glossary.dataset.statusGlossary,trigger);}
 });
 pop.addEventListener('toggle',event=>{if(event.newState==='closed'&&!pop.matches(':popover-open'))trigger?.setAttribute('aria-expanded','false');});
 pop.addEventListener('keydown',event=>{if(event.key==='Escape'){event.preventDefault();event.stopPropagation();pop.hidePopover();trigger?.focus({preventScroll:true});}});
 decorate();new MutationObserver(changes=>{for(const change of changes)for(const node of change.addedNodes)if(node.nodeType===1&&node!==pop&&!pop.contains(node))decorate(node.parentElement||node);}).observe(document.body,{childList:true,subtree:true});
 globalThis.GuedalaStatusHelp={decorate,definitions};
})();
