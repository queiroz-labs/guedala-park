;(function(){
  'use strict';
  const api=globalThis.GuedalaField,rows=globalThis.GUEDALA_FIELD_ROWS;
  const page=document.getElementById('chaves');if(!page||!api||!rows)return;
  const escape=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const byCode=new Map(rows.map(r=>[r.codigo,r])),parts=new Map(rows.flatMap(r=>r.partes.map(p=>[p.codigo,p])));
  const store=api.createStore([...parts.keys()]);let urls=[];
  const statusLabels={pendente:'Ainda não conferido',ok:'OK marcado por você',fora_do_esperado:'Fora do esperado — sua anotação'};
  const groups=[['sala','Sala e jantar'],['cozinha','Cozinha'],['lavanderia','Lavanderia'],['quarto','Quarto'],['escritorio','Escritório'],['banho','Banheiro'],['circulacao','Circulação'],['all','Geral']];
  const projectLink=p=>{const [file,anchor]=p.split('#');return (typeof workDocUrl==='function'?workDocUrl({path:file,available:true}):'docs/'+file+'.html')+(anchor?'#'+anchor:'');};
  const datumControl=id=>rows.some(r=>r.ambiente===id&&r.datum)?`<label class="field-datum"><input type="checkbox" data-datum-room="${id}"><span>Datum confirmado: as coordenadas desta seção já estão vinculadas aos eixos da planta. <a href="${escape(projectLink('07_Imovel/Roteiro_dia_das_chaves_R01.md#protocolo-de-datum--proposto'))}">Ver protocolo de datum</a></span></label>`:'';
  const fields=rows.map((r,i)=>`<article class="field-row" data-measure="${escape(r.codigo)}" data-field-room="${r.ambiente}">
    <div class="field-row-head"><code>${escape(r.codigo)}</code><span class="field-row-status"></span></div>
    <h3>${escape(r.descricao)}</h3><p class="field-nominal">Nominal: <strong>${escape(r.nominal)}</strong></p>
    ${r.como_medir?`<p class="field-method">${escape(r.como_medir)}${r.protocolo?` · <a href="${escape(projectLink(r.protocolo))}">Abrir protocolo de datum</a>`:''}</p>`:''}
    ${r.datum?'<p class="field-datum-warning">Sem datum confirmado, a coordenada fica como anotação e não será aplicada à cadeia.</p>':''}
    <div class="field-inputs">${r.partes.map((p,j)=>`<label for="field-${i}-${j}">${escape(p.label)} <span>mm</span><input id="field-${i}-${j}" data-measure-input="${escape(p.codigo)}" type="number" inputmode="decimal" step="any" autocomplete="off"><output data-difference="${escape(p.codigo)}" for="field-${i}-${j}"></output></label>`).join('')}</div>
    <p class="field-tolerance">Tolerância: ${escape(r.tolerancia)}. A diferença não classifica a medida.</p>
    <div class="field-review" role="group" aria-label="Sua conferência de ${escape(r.codigo)}"><button type="button" data-review="ok" aria-pressed="false">✓ OK</button><button type="button" data-review="fora_do_esperado" aria-pressed="false">Fora do esperado</button><button type="button" data-review="pendente" class="quiet" aria-label="Deixar ${escape(r.codigo)} pendente">Pendente</button></div>
    <label class="field-observation" for="field-note-${i}">Observação <textarea id="field-note-${i}" data-observation="${escape(r.codigo)}" rows="2" placeholder="Posição da cota, acabamento, foto…"></textarea></label>
  </article>`);
  page.innerHTML=`<div class="field-heading"><span class="eyebrow">LEVANTAMENTO NO IMÓVEL</span><h1>Dia das chaves</h1><p>Meça em milímetros. Registre o que encontrou e exporte uma cópia antes de sair.</p></div>
    <p id="fieldSaveState" class="field-save-state" role="status"></p>
    <div class="field-toolbar"><label for="fieldRoom">Cômodo<select id="fieldRoom"><option value="todos">Todos os cômodos</option>${groups.map(([id,name])=>`<option value="${id}">${name}</option>`).join('')}</select></label><div><span id="fieldProgress"></span><small>${rows.length} itens do roteiro · ${parts.size} campos</small></div></div>
    <div id="fieldGroups">${groups.map(([id,name])=>`<section data-field-group="${id}" class="field-group"><h2>${name}</h2>${datumControl(id)}${fields.filter((_,i)=>rows[i].ambiente===id).join('')}</section>`).join('')}</div>
    <aside id="fieldExportPanel" class="field-export-panel" aria-labelledby="fieldExportTitle" hidden><h2 id="fieldExportTitle">Guarde os dois arquivos</h2><p>JSON para reabrir e levar ao projeto; CSV para consultar. Seus dados continuam neste aparelho.</p><div id="fieldDownloads"></div><button type="button" id="fieldCloseExport" class="quiet">Fechar</button></aside>
    <div class="field-actions"><button type="button" id="fieldExport" class="primary-button">Exportar</button><button type="button" id="fieldImport">Importar JSON</button><input id="fieldImportFile" type="file" accept=".json,application/json" hidden><span id="fieldMessage" role="status"></span></div>`;
  function saveState(){
    const state=store.storageState(),el=document.getElementById('fieldSaveState');
    const text=state.persistent?'Salvo neste navegador. Exporte para guardar uma cópia.':`${state.error||'Armazenamento indisponível.'} Dados só nesta aba: exporte antes de fechar.`;
    if(el.textContent!==text)el.textContent=text;el.classList.toggle('field-memory-only',!state.persistent);
    const stats=store.stats();document.getElementById('fieldProgress').textContent=`${stats.reviewed} de ${stats.total} campos conferidos`;
  }
  function syncRow(r,restore=false){
    const article=page.querySelector(`[data-measure="${r.codigo}"]`),records=r.partes.map(p=>store.get(p.codigo));
    for(const [j,p] of r.partes.entries()){
      const record=records[j],input=article.querySelector(`[data-measure-input="${p.codigo}"]`);
      if(restore)input.value=record.valor_mm==null?'':String(record.valor_mm);
      const delta=api.difference(record.valor_mm,p.nominal_mm),output=article.querySelector(`[data-difference="${p.codigo}"]`);
      output.textContent=record.valor_mm==null?'Sem medida':delta==null?'Sem nominal numérico':`Diferença: ${delta>0?'+':''}${delta.toLocaleString('pt-BR')} mm`;
    }
    let status=records.every(r=>r.status==='ok')?'ok':records.some(r=>r.status==='fora_do_esperado')?'fora_do_esperado':'pendente';
    article.querySelector('.field-row-status').textContent=statusLabels[status];
    article.querySelectorAll('[data-review]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.review===status)));
    if(restore)article.querySelector('textarea').value=[...new Set(records.map(r=>r.observacao).filter(Boolean))].join('\n');
    saveState();
  }
  function message(text){document.getElementById('fieldMessage').textContent=text;}
  function syncDatum(){
    page.querySelectorAll('[data-datum-room]').forEach(input=>{
      const codes=rows.filter(r=>r.ambiente===input.dataset.datumRoom&&r.datum).flatMap(r=>r.partes.map(p=>p.codigo));
      input.checked=codes.length>0&&codes.every(c=>store.get(c).datum_confirmado===true);
    });
  }
  page.addEventListener('change',event=>{
    const input=event.target;if(!input.dataset.datumRoom)return;
    for(const r of rows.filter(r=>r.ambiente===input.dataset.datumRoom&&r.datum))
      for(const p of r.partes)store.update(p.codigo,{datum_confirmado:input.checked});
    saveState();
  });
  page.addEventListener('input',event=>{
    const input=event.target,code=input.dataset.measureInput,note=input.dataset.observation;
    try{
      if(code){store.update(code,{valor_mm:api.number(input.value)});syncRow(byCode.get(code.split('/')[0]));}
      if(note){const row=byCode.get(note);for(const p of row.partes)store.update(p.codigo,{observacao:input.value});syncRow(row);}
    }catch(e){message(e.message);}
  });
  page.addEventListener('click',event=>{
    const button=event.target.closest('[data-review]');if(!button)return;
    const r=byCode.get(button.closest('[data-measure]').dataset.measure);
    for(const p of r.partes)store.update(p.codigo,{status:button.dataset.review});syncRow(r);
  });
  document.getElementById('fieldRoom').addEventListener('change',event=>{
    for(const group of page.querySelectorAll('[data-field-group]'))group.hidden=event.target.value!=='todos'&&group.dataset.fieldGroup!==event.target.value;
  });
  function revoke(){urls.forEach(URL.revokeObjectURL);urls=[];}
  document.getElementById('fieldExport').onclick=()=>{
    revoke();const payload=store.exportData(),formats=[['Medidas_reais.json',JSON.stringify(payload,null,2),'application/json','Salvar JSON'],['Medidas_reais.csv',api.toCsv(payload),'text/csv;charset=utf-8','Salvar CSV']];
    const downloads=document.getElementById('fieldDownloads');downloads.replaceChildren();
    for(const [name,text,type,label] of formats){const link=document.createElement('a');link.href=URL.createObjectURL(new Blob([text],{type}));urls.push(link.href);link.download=name;link.textContent=label;downloads.appendChild(link);}
    const panel=document.getElementById('fieldExportPanel');panel.hidden=false;panel.scrollIntoView({block:'center',behavior:'instant'});downloads.querySelector('a').focus({preventScroll:true});message(`${payload.medidas.length} registros preparados.`);
  };
  document.getElementById('fieldCloseExport').onclick=()=>{document.getElementById('fieldExportPanel').hidden=true;document.getElementById('fieldExport').focus();revoke();};
  const fileInput=document.getElementById('fieldImportFile');document.getElementById('fieldImport').onclick=()=>fileInput.click();
  fileInput.addEventListener('change',async()=>{
    const file=fileInput.files[0];if(!file)return;
    try{if(file.size>2*1024*1024)throw new Error('Arquivo maior que 2 MB. Use uma exportação JSON do levantamento.');
      const result=store.importFile(await file.text());for(const r of rows)syncRow(r,true);syncDatum();
      message(`${result.imported} registros importados; ${result.older} antigos mantidos sem substituir os mais recentes.`);
    }catch(e){message('Importação não aplicada: '+e.message);}finally{fileInput.value='';}
  });
  window.addEventListener('beforeunload',revoke);for(const r of rows)syncRow(r,true);syncDatum();
  document.addEventListener('click',event=>{
    const button=event.target.closest('.mast [data-tab]');
    if(button)button.scrollIntoView({block:'nearest',inline:'nearest',behavior:'instant'});
  });
  setTimeout(()=>document.querySelector('.mast [data-tab].active')?.scrollIntoView({block:'nearest',inline:'nearest',behavior:'instant'}),0);
  window.GuedalaFieldUI={store};
})();
