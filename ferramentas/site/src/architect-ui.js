/* Mesmos tokens do site; entrada documental sem estado técnico novo. */
;(function(){
 const data=globalThis.GUEDALA_ARCHITECT,host=document.getElementById('architect');if(!host||!data)return;
 const e=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 const url=path=>workDocUrl({path});
 host.innerHTML=`<section class="entry-hero" aria-labelledby="heroHeading"><div class="entry-hero-copy"><span class="eyebrow">GUEDALA PARK</span><h1 id="heroHeading">O apartamento,<br>por dentro.</h1><p>Explore os ambientes, descubra os móveis e acompanhe as escolhas do projeto.</p><button type="button" class="entry-hero-button" data-entry-path="apartamento">Explorar o apartamento <span aria-hidden="true">→</span></button></div><figure class="entry-hero-art"><img src="{{COVER_IMAGE}}" width="1152" height="768" fetchpriority="high" alt="Sala e jantar em miniatura 3D, com sofá areia, cortinas e iluminação acolhedora."><figcaption>Ilustração de ambiente</figcaption></figure></section>
 <section class="entry-paths" aria-labelledby="entryHeading"><h2 id="entryHeading">${e(data.entryHeading)}</h2><div class="entry-route-list">${data.entryPaths.map(p=>`<button type="button" class="entry-route" data-entry-path="${e(p.id)}"><strong>${e(p.title)} →</strong><span>${e(p.description)}</span></button>`).join('')}</div><button type="button" class="entry-route entry-plan" data-entry-path="${e(data.entryPlan.id)}"><strong>${e(data.entryPlan.title)} →</strong><span>${e(data.entryPlan.description)}</span></button></section>
 <div class="arch-intro"><h2>Sobre o projeto</h2><p>Projeto de interiores e marcenaria de um apartamento de 40,18 m², com dois dormitórios.</p><dl class="arch-facts"><div><dt>Objetivo</dt><dd>Mudar para o apartamento cerca de três meses depois de pegar as chaves.</dd></div><div><dt>Verba de referência</dt><dd>${e(data.overview.budget)}</dd></div></dl></div>
 <details class="entry-more arch-progress"><summary>Onde estamos no projeto</summary><p>Percentuais documentais da fonte; não indicam conclusão da obra.</p><ul>${data.progress.map(p=>`<li><div><strong>${e(p.stage)}</strong><b>${e(p.percent)}</b></div><p>${e(p.reading)}</p></li>`).join('')}</ul></details>
 <details class="entry-more"><summary>Mais sobre o projeto</summary>
 <section class="arch-disciplines" id="entry-responsibilities"><h2>Pendências por disciplina</h2><div class="arch-disc-list">${data.disciplines.map(d=>`<article id="arch-${d.id}"><h3>${e(d.title)}</h3><p>${e(d.text)}</p><a href="${e(url(d.path))}">Ver estado e limites →</a></article>`).join('')}</div></section></details>`;
 host.querySelectorAll('[data-arch-room]').forEach(b=>b.onclick=()=>{tab('model');setRoom(b.dataset.archRoom);setView('iso');document.getElementById('scene').focus();});
 function follow(action){
  tab(action.tab);if(action.room){setRoom(action.room);setView('iso');}
  requestAnimationFrame(()=>{const target=document.getElementById(action.target);if(!target)return;if(target.tagName==='DETAILS')target.open=true;for(let parent=target.parentElement;parent;parent=parent.parentElement)if(parent.tagName==='DETAILS')parent.open=true;target.tabIndex=-1;target.scrollIntoView({block:'start'});target.focus({preventScroll:true});});
 }
 host.querySelectorAll('[data-entry-path]').forEach(b=>b.onclick=()=>follow([...data.entryPaths,data.entryPlan].find(p=>p.id===b.dataset.entryPath)));
 const params=new URLSearchParams(location.search),legacyMood=document.body.dataset.startTab==='mood'&&!params.has('perfil')&&!params.has('aba')&&!location.hash;
 const first=legacyMood?'mood':GuedalaArchitect.entryTab(location.search,location.hash,WORK_TABS);
 if(new URLSearchParams(location.search).get('perfil')==='arquiteto')document.body.classList.add('architect-profile');
 if(first)setTimeout(()=>tab(first));
})();
