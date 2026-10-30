;(function(){
  'use strict';
  const api=globalThis.GuedalaField,rows=globalThis.GUEDALA_FIELD_ROWS;
  const page=document.getElementById('chaves');if(!page||!api||!rows)return;
  const escape=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const byCode=new Map(rows.map(r=>[r.codigo,r])),parts=new Map(rows.flatMap(r=>r.partes.map(p=>[p.codigo,p])));
  const store=api.createStore([...parts.keys()]);let urls=[];
  const guideData=globalThis.GUEDALA_FIELD_GUIDE;
  const guides=new Map((guideData?.guias||[]).map(g=>[g.codigo,g]));
  let mode='guide',flow=null,guideRoom=null,guideCodes=[];
  const statusLabels={pendente:'Ainda não conferido',ok:'OK marcado por você',fora_do_esperado:'Fora do esperado — sua anotação'};
  const groups=[['sala','Sala e jantar'],['cozinha','Cozinha'],['lavanderia','Lavanderia'],['quarto','Quarto'],['escritorio','Escritório'],['banho','Banheiro'],['circulacao','Circulação'],['all','Geral']];
  const lightGuideUrl=location.pathname.includes('/09_Referencias/')?'../ferramentas/site/Dia_das_chaves.html':'Dia_das_chaves.html';
  const projectLink=p=>p.includes('Roteiro_dia_das_chaves')&&guideData?'#fieldDatumProtocol':(()=>{const [file,anchor]=p.split('#');return (typeof workDocUrl==='function'?workDocUrl({path:file,available:true}):'docs/'+file+'.html')+(anchor?'#'+anchor:'');})();
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
  const roomFields=id=>{
    const regular=fields.filter((_,i)=>rows[i].ambiente===id&&!rows[i].avancado).join('');
    const advanced=fields.filter((_,i)=>rows[i].ambiente===id&&rows[i].avancado);
    return regular+(advanced.length?`<details class="field-advanced"><summary>Pontos e panos (avançado) · ${advanced.length}</summary><p>Coordenadas da cadeia, condicionadas ao vínculo ao datum. Verifique a descrição antes de medir.</p>${advanced.join('')}</details>`:'');
  };
  page.innerHTML=`<div class="field-heading"><span class="eyebrow">LEVANTAMENTO NO IMÓVEL</span><h1>Dia das chaves</h1><p>Meça em milímetros. Registre o que encontrou e exporte uma cópia antes de sair.</p>${!globalThis.GUEDALA_PACKAGE&&!location.pathname.endsWith('/Dia_das_chaves.html')?`<a class="field-protocol-link" href="${lightGuideUrl}" download>Salvar guia leve para usar sem internet</a>`:''}</div>
    <p id="fieldSaveState" class="field-save-state" role="status"></p>
    <div class="field-modes" role="group" aria-label="Modo de levantamento"><button type="button" data-field-mode="guide" aria-pressed="true">Medir com guia</button><button type="button" data-field-mode="list" aria-pressed="false">Ver todos</button></div>
    <div id="fieldGuide"></div>
    <div id="fieldList" hidden><div class="field-toolbar"><label for="fieldRoom">Cômodo<select id="fieldRoom"><option value="todos">Todos os cômodos</option>${groups.map(([id,name])=>`<option value="${id}">${name}</option>`).join('')}</select></label><div><span id="fieldProgress"></span><small>${rows.length} itens do roteiro · ${parts.size} campos</small></div></div>
    <div id="fieldGroups">${groups.map(([id,name])=>`<section data-field-group="${id}" class="field-group"><h2>${name}</h2>${datumControl(id)}${roomFields(id)}</section>`).join('')}</div></div>
    ${guideData?`<details id="fieldDatumProtocol" class="field-protocol"><summary>Protocolo de datum · proposto</summary><p>Leia antes de marcar o datum como confirmado.</p>${guideData.protocolo_html}</details>`:''}
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
  const guideHost=document.getElementById('fieldGuide');
  // Referência dominante: tokens e planta do produto. Brief: uma cota por vez;
  // craft Refero: rótulos explícitos, foco visível, controles de toque >=44 px.
  function miniPlan(room,target=null,entry=false){
    const svg=globalThis.GuedalaFloorplan?.data.svg;
    if(!svg)return '<p>Planta indisponível nesta cópia. Escolha o cômodo na lista.</p>';
    return `<div class="field-mini${entry?' field-room-map':''}" data-guide-plan="${escape(room)}" data-guide-target="${escape(target||'')}">${svg.replace('</svg>',(guideData?.overlay||'')+'</svg>')}</div>`;
  }
  function decoratePlans(){
    guideHost.querySelectorAll('[data-guide-plan]').forEach(container=>{
      const room=container.dataset.guidePlan,target=container.dataset.guideTarget,svg=container.querySelector('svg');
      svg.removeAttribute('aria-labelledby');svg.setAttribute('aria-label','Planta aproximada · '+(groups.find(g=>g[0]===room)?.[1]||'escolher cômodo'));
      // O SVG é reutilizado com IDs locais únicos; as zonas preservam data-fp-select.
      svg.querySelectorAll('[id]').forEach(el=>el.removeAttribute('id'));
      svg.querySelectorAll('[data-fp-r]').forEach(el=>{
        const selected=el.dataset.fpR.split(' ').includes(room);
        el.classList.toggle('fp-muted',room!=='all'&&!selected);
        el.classList.toggle('fp-picked',selected&&!el.dataset.fpTarget);
      });
      svg.querySelectorAll('[data-fp-target]').forEach(el=>el.classList.toggle('fp-picked',el.dataset.fpTarget===target));
      if(!container.classList.contains('field-room-map')){
        svg.querySelectorAll('[data-fp-select]').forEach(el=>{el.removeAttribute('tabindex');el.removeAttribute('role');});
        const zones=[...svg.querySelectorAll(`[data-fp-select="${room}"]`)];
        if(zones.length){
          const boxes=zones.map(el=>el.getBBox()),x=Math.min(...boxes.map(b=>b.x)),y=Math.min(...boxes.map(b=>b.y));
          const right=Math.max(...boxes.map(b=>b.x+b.width)),bottom=Math.max(...boxes.map(b=>b.y+b.height));
          svg.setAttribute('viewBox',`${x-35} ${y-35} ${right-x+70} ${bottom-y+70}`);
        }
      }
    });
  }
  function renderGuide(focus=false){
    if(!guideData)return;
    if(!flow){
      guideHost.innerHTML=`<h2 tabindex="-1">Por onde vamos começar?</h2><p>Toque no cômodo ou escolha na lista. Você pode pular uma medida e voltar depois.</p>${miniPlan('all',null,true)}<div class="field-room-choices">${groups.map(([id,name])=>`<button type="button" data-guide-room="${id}">${name}<small>${rows.filter(r=>r.ambiente===id&&!r.avancado).reduce((n,r)=>n+r.partes.length,0)} campos principais</small></button>`).join('')}</div><label class="field-datum"><input type="checkbox" id="fieldGuideAdvanced"><span>Incluir pontos e panos (avançado)</span></label>`;
    }else if(flow.current()===null){
      const {total,recorded}=flow.progress(),missing=flow.missing();
      const unreviewed=guideCodes.filter(c=>store.get(c).status==='pendente'&&(store.get(c).valor_mm!==null||store.get(c).observacao.trim()));
      const datum=guideCodes.filter(c=>c.startsWith('PR-')&&store.get(c).valor_mm!==null&&!store.get(c).datum_confirmado);
      guideHost.innerHTML=`<h2 tabindex="-1">Revisar antes de sair</h2><p>${recorded} de ${total} campos deste percurso têm valor ou observação. ${missing.length} sem registro; ${unreviewed.length} com registro sem conferência manual; ${datum.length} coordenadas sem datum.</p><p>Revisar não confirma instalação ou encaixe. Exporte uma cópia mesmo se ainda faltar medir.</p><button type="button" data-guide-export class="primary-button">Exportar medidas</button><div class="field-guide-missing">${missing.map(c=>`<button type="button" data-guide-jump="${escape(c)}">${escape(guides.get(c).titulo_simples)}<small>Sem registro</small></button>`).join('')||'<p>Todos os campos deste percurso têm algum registro.</p>'}</div><div class="field-guide-nav"><button type="button" data-guide-back>Voltar</button><button type="button" data-guide-home>Outro cômodo</button></div>`;
    }else{
      const code=flow.current(),g=guides.get(code),r=byCode.get(code.split('/')[0]),p=parts.get(code),record=store.get(code),progress=flow.progress();
      const photo=g.foto&&guideData.photos[g.foto];
      guideHost.innerHTML=`<div class="field-guide-progress"><span>${escape(groups.find(v=>v[0]===guideRoom)[1])} · ${progress.index+1} de ${progress.total}</span><button type="button" data-guide-home>Trocar cômodo</button><progress max="${progress.total}" value="${progress.index}">${progress.index}/${progress.total}</progress></div>
        <h2 tabindex="-1">${escape(g.titulo_simples)}</h2><div class="field-guide-layout"><div class="field-guide-visual"><figure>${miniPlan(g.onde.comodo,g.onde.alvo)}<figcaption>${escape(g.onde.orientacao)}${g.onde.alvo?' · destaque nominal, a conferir':''}</figcaption></figure>${photo?`<details class="field-guide-photo"><summary>Ver foto de referência</summary><figure><img src="${photo}" width="800" height="450" alt="${escape(g.foto_confere)}"><figcaption>${escape(guideData.photo_info[g.foto].legenda)}. ${escape(g.foto_confere)}</figcaption></figure></details>`:'<p class="field-photo-missing">Sem foto associada a esta medida. Identifique o local no croqui.</p>'}</div>
        <div class="field-guide-form"><h3>Como medir</h3><ol>${g.como.map(line=>`<li>${escape(line)}</li>`).join('')}</ol>${g.como.some(s=>/protocolo de datum/i.test(s))?'<a href="#fieldDatumProtocol" class="field-protocol-link">Ver protocolo de datum</a>':''}<p class="field-guide-instrument">${escape(g.instrumento)}${g.altura_ref_mm!==null?' · referência horizontal: '+g.altura_ref_mm+' mm do piso acabado':''}</p>
        <p class="field-nominal">Nominal: <strong>${p.nominal_mm===null?'sem cota numérica':p.nominal_mm.toLocaleString('pt-BR')+' mm'}</strong></p>${p.nominal_mm===null?'<p>Verificação composta: use a observação para registrar o que encontrou. O número é opcional.</p>':''}
        <label class="field-guide-value" for="fieldGuideValue">${p.nominal_mm===null?'Número, se aplicável':'Valor medido'} <span>mm</span><input id="fieldGuideValue" data-guide-input="${escape(code)}" type="number" inputmode="decimal" step="any" autocomplete="off" value="${record.valor_mm??''}"></label><output id="fieldGuideDifference" for="fieldGuideValue"></output><p id="fieldGuideError" role="alert"></p>
        <p class="field-tolerance">Tolerância: ${escape(r.tolerancia)}. Diferença não significa aceitação.</p>${r.datum?datumControl(r.ambiente):''}<div class="field-review"><button type="button" data-guide-review="ok">✓ OK</button><button type="button" data-guide-review="fora_do_esperado">Fora do esperado</button><button type="button" data-guide-review="pendente">Pendente</button></div><label class="field-observation" for="fieldGuideNote">Observação <textarea id="fieldGuideNote" data-guide-note="${escape(code)}" rows="2">${escape(record.observacao)}</textarea></label><details class="field-guide-reference"><summary>Código e referência</summary><code>${escape(code)}</code><p>${escape(r.descricao)}</p><p>${escape(r.nominal)}</p></details></div></div>
        <div class="field-guide-nav"><button type="button" data-guide-back ${progress.index===0?'disabled':''}>Voltar</button><button type="button" data-guide-skip>Pular</button><button type="button" data-guide-next class="primary-button">${progress.index+1===progress.total?'Revisar':'Próxima'}</button></div>`;
      updateGuideDifference();syncDatum();
    }
    decoratePlans();saveState();
    if(focus){guideHost.querySelector('h2')?.focus({preventScroll:true});guideHost.scrollIntoView({block:'start',behavior:'instant'});}
  }
  function updateGuideDifference(){
    const code=flow?.current(),output=document.getElementById('fieldGuideDifference');if(!code||!output)return;
    const record=store.get(code),delta=api.difference(record.valor_mm,parts.get(code).nominal_mm);
    output.textContent=record.valor_mm===null?'Sem medida':delta===null?'Sem nominal numérico':`Diferença: ${delta>0?'+':''}${delta.toLocaleString('pt-BR')} mm`;
    guideHost.querySelectorAll('[data-guide-review]').forEach(el=>el.setAttribute('aria-pressed',String(record.status===el.dataset.guideReview)));
  }
  function setMode(next){
    mode=next;document.getElementById('fieldList').hidden=mode!=='list';guideHost.hidden=mode!=='guide';
    page.querySelectorAll('[data-field-mode]').forEach(el=>el.setAttribute('aria-pressed',String(el.dataset.fieldMode===mode)));
    if(mode==='list')for(const r of rows)syncRow(r,true);else renderGuide();
  }
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
    syncDatum();saveState();
  });
  page.addEventListener('input',event=>{
    const input=event.target,code=input.dataset.measureInput,note=input.dataset.observation;
    try{
      if(input.dataset.guideInput){
        if(input.validity.badInput)throw new Error('Use um número em milímetros.');
        flow.update({valor_mm:api.number(input.value)});syncRow(byCode.get(input.dataset.guideInput.split('/')[0]),true);updateGuideDifference();document.getElementById('fieldGuideError').textContent='';
      }
      if(input.dataset.guideNote){flow.update({observacao:input.value});syncRow(byCode.get(input.dataset.guideNote.split('/')[0]),true);}
      if(code){store.update(code,{valor_mm:api.number(input.value)});syncRow(byCode.get(code.split('/')[0]));}
      if(note){const row=byCode.get(note);for(const p of row.partes)store.update(p.codigo,{observacao:input.value});syncRow(row);}
    }catch(e){const error=document.getElementById('fieldGuideError');if(error)error.textContent=e.message;message(e.message);}
  });
  page.addEventListener('click',event=>{
    const target=event.target.closest('button,a,[data-fp-select]');
    if(target?.dataset.fieldMode){setMode(target.dataset.fieldMode);return;}
    const room=target?.dataset.guideRoom||(target?.closest('.field-room-map')?target.dataset.fpSelect:null);
    if(room){
      const advanced=document.getElementById('fieldGuideAdvanced')?.checked;
      guideRoom=room;guideCodes=rows.filter(r=>r.ambiente===room&&(advanced||!r.avancado)).flatMap(r=>r.partes.map(p=>p.codigo));flow=api.createGuide(guideCodes,store);renderGuide(true);return;
    }
    if(target?.hasAttribute('data-guide-home')){flow=null;renderGuide(true);return;}
    if(target?.hasAttribute('data-guide-back')){flow.back();renderGuide(true);return;}
    if(target?.hasAttribute('data-guide-next')||target?.hasAttribute('data-guide-skip')){
      if(document.getElementById('fieldGuideError')?.textContent){document.getElementById('fieldGuideValue').focus();return;}
      flow.next();renderGuide(true);return;
    }
    if(target?.dataset.guideJump){flow.goTo(target.dataset.guideJump);renderGuide(true);return;}
    if(target?.dataset.guideReview){flow.update({status:target.dataset.guideReview});syncRow(byCode.get(flow.current().split('/')[0]),true);updateGuideDifference();return;}
    if(target?.hasAttribute('data-guide-export')){document.getElementById('fieldExport').click();return;}
    if(target?.getAttribute('href')==='#fieldDatumProtocol'){
      const protocol=document.getElementById('fieldDatumProtocol');protocol.open=true;protocol.scrollIntoView({block:'start'});event.preventDefault();return;
    }
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
      const result=store.importFile(await file.text());for(const r of rows)syncRow(r,true);syncDatum();if(mode==='guide')renderGuide();
      message(`${result.imported} registros importados; ${result.older} antigos mantidos sem substituir os mais recentes.`);
    }catch(e){message('Importação não aplicada: '+e.message);}finally{fileInput.value='';}
  });
  window.addEventListener('beforeunload',revoke);for(const r of rows)syncRow(r,true);syncDatum();
  page.addEventListener('keydown',event=>{if(event.target.closest('.field-room-map')&&event.target.dataset.fpSelect&&(event.key==='Enter'||event.key===' ')){event.preventDefault();event.target.dispatchEvent(new MouseEvent('click',{bubbles:true}));}});
  if(guideData)renderGuide();else setMode('list');
  document.addEventListener('click',event=>{
    const button=event.target.closest('.mast [data-tab]');
    if(button)button.scrollIntoView({block:'nearest',inline:'nearest',behavior:'instant'});
  });
  setTimeout(()=>document.querySelector('.mast [data-tab].active')?.scrollIntoView({block:'nearest',inline:'nearest',behavior:'instant'}),0);
  window.GuedalaFieldUI={store,setMode};
})();
