/* Mesmos tokens do site; entrada documental sem estado técnico novo. */
;(function(){
 const data=globalThis.GUEDALA_ARCHITECT,host=document.getElementById('architect');if(!host||!data)return;
 const e=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 const url=path=>workDocUrl({path});
 host.innerHTML=`<div class="arch-intro"><span class="eyebrow">PARA O ARQUITETO</span><h1>Um ponto de partida<br>para conhecer o projeto.</h1><p>${e(data.overview.project)}</p><p class="arch-notice">${e(data.overview.notice)}</p><dl class="arch-facts"><div><dt>Objetivo</dt><dd>${e(data.overview.objective)}</dd></div><div><dt>Verba de referência</dt><dd>${e(data.overview.budget)}</dd></div><div><dt>Modelo vigente</dt><dd>${e(data.overview.model)} · cotas a conferir</dd></div></dl></div>
 <section class="arch-progress"><h2>Onde estamos</h2><p>Percentuais documentais da fonte; não indicam conclusão da obra.</p><ul>${data.progress.map(p=>`<li><div><strong>${e(p.stage)}</strong><b>${e(p.percent)}</b></div><p>${e(p.reading)}</p></li>`).join('')}</ul></section>
 <section class="arch-start"><h2>Por onde começar</h2><div class="arch-links">${data.shortcuts.map(s=>`<article><h3>${e(s.title)}</h3>${s.rooms?s.rooms.map(r=>`<button data-arch-room="${r}">${e(PROJECT.rooms.find(x=>x.id===r).name)} →</button>`).join(''):`<a href="${e(url(s.path))}">Abrir documento →</a>`}</article>`).join('')}</div></section>
 <section class="arch-disciplines"><h2>Pendências por disciplina</h2><div class="arch-disc-list">${data.disciplines.map(d=>`<article id="arch-${d.id}"><h3>${e(d.title)}</h3><p>${e(d.text)}</p><a href="${e(url(d.path))}">Ver estado e limites →</a></article>`).join('')}</div></section>`;
 host.querySelectorAll('[data-arch-room]').forEach(b=>b.onclick=()=>{tab('model');setRoom(b.dataset.archRoom);setView('iso');document.getElementById('scene').focus();});
 const first=GuedalaArchitect.entryTab(location.search);
 if(new URLSearchParams(location.search).get('perfil')==='arquiteto')document.body.classList.add('architect-profile');
 if(first)setTimeout(()=>tab(first));
})();
