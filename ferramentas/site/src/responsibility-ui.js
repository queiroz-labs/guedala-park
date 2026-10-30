/* Papéis documentados, sem presumir contratação ou delegação técnica. */
;(function(){
 const d=GUEDALA_ARCHITECT,a=GuedalaArchitect,e=esc,host=document.querySelector('.arch-disciplines');
 const rows=[...d.disciplines,...d.itemResponsibilities],counts=a.ownerCounts(rows);
 const badges=r=>`<div class="owner-badges">${r.owners.map(o=>`<span>${e(o)}</span>`).join('')}${r.measurement?'<strong>Depende das medidas reais</strong>':''}</div>`;
 host.innerHTML=`<h2>Quem decide</h2><p>Papéis das fontes; contratação e revisão técnica continuam pendentes. Um item pode ter mais de um responsável.</p><div class="owner-filters" role="group" aria-label="Filtrar por responsável"><button data-owner="todos" aria-pressed="true">Todos · ${rows.length}</button>${a.owners.map(o=>`<button data-owner="${e(o)}" aria-pressed="false">${e(o)} · ${counts[o]}</button>`).join('')}</div><p id="ownerCount" role="status"></p><h3>Pendências por disciplina</h3><div id="ownerDisciplines" class="arch-disc-list"></div><details id="ownerRoomDetails"><summary>Conferências nos ambientes</summary><div id="ownerRooms" class="arch-disc-list"></div></details>`;
 function render(owner){
  const selected=a.ownerItems(rows,owner);document.getElementById('ownerCount').textContent=`${selected.length} itens · ${selected.filter(r=>r.measurement).length} dependem das medidas reais`;
  document.getElementById('ownerDisciplines').innerHTML=selected.filter(r=>!r.item).map(r=>`<article id="arch-${r.id}"><h3>${e(r.title)}</h3>${badges(r)}<p>${e(r.text)}</p><a href="${e(workDocUrl({path:r.path}))}">Ver estado e limites →</a><details><summary>Fonte do responsável</summary><p>${e(r.ownerQuote||'Responsável não indicado para esta pendência.')}</p></details></article>`).join('')||'<p>Nenhuma disciplina neste filtro. Confira os ambientes abaixo.</p>';
  document.getElementById('ownerRooms').innerHTML=selected.filter(r=>r.item).map(r=>`<article id="owner-${encodeURIComponent(r.item)}"><span class="eyebrow">${e(PROJECT.rooms.find(v=>v.id===r.room)?.name)}</span><h3>${e(r.title)}</h3>${badges(r)}<p>${e(r.text)}</p><button data-owner-item="${e(r.item)}">Abrir escolha →</button><details><summary>Fonte dos papéis</summary>${r.source?`<p>${e(r.roles.join(' · '))}</p><p>${e(r.codes.join(', '))}</p><a href="${e(workDocUrl({path:r.source}))}">Registro de medidas</a>`:'<p>A fonte não vincula um responsável específico a esta conferência.</p>'}</details></article>`).join('')||'<p>Nenhum item de ambiente neste filtro.</p>';
  host.querySelectorAll('[data-owner]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.owner===owner)));
  host.querySelectorAll('[data-owner-item]').forEach(b=>b.onclick=()=>{tab('decisions');document.getElementById('filterRoom').value='all';document.getElementById('filterStatus').value='all';renderDecisions();document.querySelector(`[data-choice="${b.dataset.ownerItem}"]`)?.scrollIntoView({block:'center'});});
 }
 host.querySelectorAll('[data-owner]').forEach(b=>b.onclick=()=>render(b.dataset.owner));render('todos');
 const byItem=new Map(d.itemResponsibilities.map(r=>[r.item,r]));
 const before=renderDecisions;renderDecisions=function(){before();document.querySelectorAll('[data-choice]').forEach(card=>{const r=byItem.get(card.dataset.choice);if(r)card.querySelector('h3').insertAdjacentHTML('afterend',badges(r));});};
 const mood=buildMood;buildMood=function(){mood();document.querySelectorAll('[data-room-item]').forEach(b=>{const r=byItem.get(b.dataset.roomItem);if(r)b.parentElement.insertAdjacentHTML('beforeend',badges(r));});};
 globalThis.GuedalaResponsibilities={rows,badges,filter:render};
})();
