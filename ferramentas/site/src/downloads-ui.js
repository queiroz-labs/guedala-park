/* Mesmo componente nas duas entradas; catálogo medido no build, sem ZIP embutido. */
;(function(){
 const rows=globalThis.GUEDALA_DOWNLOADS||[],expanded=new Set(),e=esc;
 const size=n=>n<1024?n+' B':n<1048576?(n/1024).toLocaleString('pt-BR',{maximumFractionDigits:1})+' KB':(n/1048576).toLocaleString('pt-BR',{maximumFractionDigits:1})+' MB';
 function item(r,i,where,all){
  const href=workDocUrl({path:r.path});
  const action=href?`<a href="${e(href)}" ${r.format==='HTML'?'':'download'} aria-label="${r.format==='HTML'?'Abrir':'Baixar'} ${e(r.title)} · ${e(r.format)}">${r.format==='HTML'?'Abrir HTML':'Baixar '+e(r.format)} →</a>`:'<p>Arquivo não incluído nesta cópia.</p>';
  return `<li id="download-${where}-${r.id}" class="downloads-row" tabindex="-1"${!all&&i>=4?' hidden':''}><h3>${e(r.title)}</h3><p>${e(r.description)}</p><p class="download-meta"><strong>${e(r.revision)}</strong> · ${e(r.format)} · <span title="${r.bytes.toLocaleString('pt-BR')} bytes">${size(r.bytes)}</span></p><p class="download-status">${e(r.status)}</p>${action}</li>`;
 }
 function render(where){
  let section=document.getElementById('downloads-'+where);
  if(!section){section=document.createElement('section');section.id='downloads-'+where;section.className='downloads-centre';section.setAttribute('aria-labelledby','downloads-title-'+where);const before=document.querySelector(where==='architect'?'.arch-start':'.work-filters');before.before(section);}
  const all=expanded.has(where);
  const moreButton=rows.length>4?`<button type="button" class="downloads-more" aria-expanded="${all}" aria-controls="downloads-list-${where}">${all?'Mostrar menos':'Ver todos os '+rows.length+' arquivos'}</button>`:'';
  const content=globalThis.GUEDALA_PACKAGE?`<p>Esta cópia contém uma seleção. <a href="${e(GUEDALA_PACKAGE.root+'COMECE_AQUI.html')}">Abrir índice dos arquivos incluídos →</a></p>`:`<ul class="downloads-list">${rows.map((r,i)=>item(r,i,where,all)).join('')}</ul>${moreButton}`;
  section.innerHTML=`<div class="downloads-heading"><div><span class="eyebrow">ARQUIVOS DO PROJETO</span><h2 id="downloads-title-${where}">Baixar</h2></div><span>${rows.length} arquivos</span></div><p>Escolha os arquivos. Cada ZIP tem seu próprio escopo; extraia-o inteiro para consultar sem rede.</p>${content}`;
  section.querySelector('ul')?.setAttribute('id','downloads-list-'+where);
  const more=section.querySelector('button');if(more)more.onclick=()=>{all?expanded.delete(where):expanded.add(where);render(where);document.querySelector('#downloads-'+where+' .downloads-more')?.focus({preventScroll:true});};
 }
 function show(id,where='documents'){
  expanded.add(where);render(where);const target=document.getElementById('download-'+where+'-'+id)||document.getElementById('downloads-'+where);target.scrollIntoView({block:'center'});target.focus({preventScroll:true});
 }
 for(const where of ['architect','documents'])render(where);
 globalThis.GuedalaDownloads={show,render,size};
})();
