;(function(){
  'use strict';
  const plan=globalThis.GUEDALA_WORK_PLAN,page=document.getElementById('obra');if(!plan||!page)return;
  const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const store=globalThis.GuedalaWork.createStore(plan.etapas.map(r=>r.id));let download=null;
  const link=(path,title)=>{const url=workDocUrl({path,available:true});return url?`<a href="${esc(url)}">${esc(title)}</a>`:`<span>${esc(title)} · fora desta cópia</span>`;};
  const weeks=Array.from({length:Math.max(...plan.etapas.map(r=>r.fim))+1},(_,i)=>i);
  page.innerHTML=`<div class="field-heading"><span class="eyebrow">EXECUÇÃO NO APARTAMENTO</span><h1>Obra, semana a semana</h1><p>Semana 0 é a semana das chaves. Acompanhe a sequência prevista e marque o que foi feito.</p></div>
    <div class="work-source">${link(plan.fonte,'Cronograma da obra')} · ${link(plan.plano,'Plano de reforma')} · ${link(plan.revisao,'Dúvidas para o RT')}</div>
    <p class="work-note">Ordem e dependências do cronograma. Marcar “feito” registra seu acompanhamento; as condições técnicas continuam nos documentos.</p>
    <p id="workSaveState" class="field-save-state" role="status"></p>
    <div class="work-toolbar"><label for="workWeek">Semana<select id="workWeek"><option value="todas">Todas as semanas</option>${weeks.map(n=>`<option value="${n}">Semana ${n}</option>`).join('')}</select></label><strong id="workProgress"></strong></div>
    <div class="work-timeline">${weeks.map(w=>`<section class="work-week" data-work-week="${w}"><h2>Semana ${w}</h2>${plan.etapas.filter(r=>r.inicio<=w&&r.fim>=w).map(r=>`<article class="work-stage" data-work-stage="${r.id}"><label class="work-check" for="work-${w}-${r.id}"><input type="checkbox" id="work-${w}-${r.id}" data-work-check="${r.id}"><span><small>SEMANA ${esc(r.semana)}</small><strong>${esc(r.servico)}</strong><span class="work-check-text">Marcar como feito</span></span></label><p><b>Depende de:</b> ${esc(r.depende_de||'Não informado na fonte — a confirmar com RT.')}</p>${r.observacao?`<p>${esc(r.observacao)}</p>`:''}<div class="work-documents">${r.documentos.map(d=>link(d.caminho,d.titulo)).join(' · ')}</div></article>`).join('')||'<p>Sem etapa listada nesta semana.</p>'}</section>`).join('')}</div>
    <div id="workDownload" class="work-download" hidden></div>
    <div class="field-actions"><button type="button" id="workExport">Exportar obra</button><button type="button" id="workImport">Importar obra</button><input id="workImportFile" type="file" accept=".json,application/json" hidden><span id="workMessage" role="status"></span></div>`;
  function sync(){
    page.querySelectorAll('[data-work-check]').forEach(el=>{
      el.checked=store.get(el.dataset.workCheck);el.closest('article').classList.toggle('work-done',el.checked);
      el.parentElement.querySelector('.work-check-text').textContent=el.checked?'Feito — marcado por você':'Marcar como feito';
    });
    const state=store.state();document.getElementById('workProgress').textContent=`${state.done} de ${state.total} etapas feitas`;
    const el=document.getElementById('workSaveState');el.classList.toggle('field-memory-only',!state.persistent);
    el.textContent=(state.persistent?'Salvo neste navegador. Exporte uma cópia.':'Armazenamento indisponível: dados só nesta aba. Exporte antes de fechar.')+(state.unknown?' Etapas de outra versão foram ignoradas; confira o cronograma atual.':'');
  }
  function message(text){document.getElementById('workMessage').textContent=text;}
  function staleDownload(){if(download){URL.revokeObjectURL(download);download=null;}document.getElementById('workDownload').hidden=true;}
  page.addEventListener('change',event=>{const el=event.target;if(!el.dataset.workCheck)return;store.set(el.dataset.workCheck,el.checked);staleDownload();sync();});
  document.getElementById('workWeek').onchange=event=>page.querySelectorAll('[data-work-week]').forEach(el=>el.hidden=event.target.value!=='todas'&&el.dataset.workWeek!==event.target.value);
  document.getElementById('workExport').onclick=()=>{
    staleDownload();download=URL.createObjectURL(new Blob([JSON.stringify(store.exportData(),null,2)],{type:'application/json;charset=utf-8'}));
    const box=document.getElementById('workDownload');box.innerHTML=`<a href="${download}" download="Obra_real.json">Salvar Obra_real.json</a><p>Guarde o arquivo para reabrir em outro navegador ou aparelho.</p>`;box.hidden=false;box.scrollIntoView({block:'center'});message('Arquivo pronto para salvar.');
  };
  const input=document.getElementById('workImportFile');document.getElementById('workImport').onclick=()=>input.click();
  input.onchange=async()=>{const file=input.files[0];if(!file)return;try{
    const r=store.importFile(await file.text());staleDownload();sync();message(`${r.applied} etapas importadas; ${r.older} antigas e ${r.ignored} de outra versão ignoradas.`);
  }catch(e){message(e.message);}finally{input.value='';}};
  window.addEventListener('storage',event=>{if(event.key===GuedalaWork.KEY)message('Obra alterada em outra aba. Recarregue para atualizar a leitura.');});
  sync();
})();
