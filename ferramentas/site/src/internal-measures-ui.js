/* Consulta visual de vãos entre faces; no CAD mutations or manufacturing allowances. */
(()=>{
 const cache=new Map(),cm=n=>(n/10).toLocaleString('pt-BR',{maximumFractionDigits:2}),safe=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 function get(code){if(!cache.has(code))cache.set(code,InternalMeasures.panels(CAD_DATA.parts.filter(p=>p.module===code),INTERNAL_FRAMES[code]));return cache.get(code);}
 function mount(code){
  const host=document.getElementById('selectedInfo'),m=CAD_DATA.modules.find(m=>m.code===code);if(!host||!m||!INTERNAL_FRAMES[code])return;
  const panels=get(code);if(!panels.length)return;const box=InternalMeasures.bounds(panels);
  const details=document.createElement('details');details.className='work-accordion internal-consult';details.innerHTML=`<summary>Medidas internas no desenho</summary><p>Escolha a vista e toque no desenho para medir entre as chapas. As cotas verdes mostram os vãos nas duas linhas de consulta.</p><button type="button" class="internal-expand">Abrir consulta maior</button><div class="internal-toolbar"><label>Vista<select data-internal="view"><option value="front">Frente</option><option value="side">Lateral</option><option value="top">Planta</option></select></label><label>Desenho<select data-internal="zoom"><option value="1">Ajustar à tela</option><option value="1.6">Ampliar 160%</option><option value="2">Ampliar 200%</option></select></label></div><div class="internal-sliders"></div><div class="internal-scroll" tabindex="0" aria-label="Desenho com vãos internos; ao ampliar, role para os lados"><svg xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Corte das chapas e cotas dos vãos internos" viewBox="0 0 720 600"></svg></div><div class="internal-values" aria-live="polite"></div><p class="work-note">Medidas do projeto, calculadas entre faces neste corte. Frentes retiradas para consulta. Ferragens e peças sem classificação de chapa não entram; um vão cotado não garante acesso ou espaço livre para uso. Confira no local e antes de fabricar.</p>`;
  host.querySelector('.work-measures')?.insertAdjacentElement('afterend',details);
  details.querySelector('.internal-expand').onclick=()=>{
   const marker=document.createComment('internal-consult'),dialog=document.createElement('dialog');dialog.className='internal-dialog';
   details.before(marker);dialog.innerHTML='<button type="button" class="internal-close">Fechar consulta</button>';document.body.append(dialog);dialog.append(details);details.open=true;
   dialog.querySelector('button').onclick=()=>dialog.close();dialog.addEventListener('close',()=>{marker.replaceWith(details);dialog.remove();details.querySelector('.internal-expand').focus();},{once:true});dialog.showModal();
  };
  let view='front',probes=[.27,.52],depthRatio=.5,cut=[],frame;
  const svg=details.querySelector('svg'),select=details.querySelector('[data-internal="view"]'),sliders=details.querySelector('.internal-sliders');
  function slider(label,kind,value){return `<label>${label} <output data-value="${kind}"></output><input type="range" min="0" max="1000" step="1" value="${value}" data-probe="${kind}" aria-label="${label}"></label>`;}
  function reset(){sliders.innerHTML=slider('Posição do corte','depth',500)+slider('Linha vertical','a',270)+slider('Linha horizontal','b',520);for(const input of sliders.querySelectorAll('input'))input.oninput=()=>{const n=Number(input.value)/1000;if(input.dataset.probe==='depth')depthRatio=n;else probes[input.dataset.probe==='a'?0:1]=n;draw();};draw();}
  function draw(){
   const [a,b,c]=InternalMeasures.axes[view],w=box.hi[a]-box.lo[a],h=box.hi[b]-box.lo[b],d=box.hi[c]-box.lo[c];
   const depth=box.lo[c]+Math.max(.05,Math.min(d-.05,depthRatio*d));cut=InternalMeasures.section(panels,view,depth);
   const scale=Math.min(620/Math.max(w,1),500/Math.max(h,1)),ox=(720-w*scale)/2,oy=(600-h*scale)/2;
   const X=n=>ox+(n-box.lo[a])*scale,Y=n=>600-oy-(n-box.lo[b])*scale;
   const px=box.lo[a]+probes[0]*w,py=box.lo[b]+probes[1]*h;frame={a,b,X,Y,ox,oy,w,h,scale};
   const horizontal=InternalMeasures.gaps(cut,0,py),vertical=InternalMeasures.gaps(cut,1,px);
   let html=cut.map(p=>`<g><title>${safe(p.label)} · ${safe(p.source)}</title>${InternalMeasures.paths(p.segments).map(loop=>`<path d="${loop.points.map((v,i)=>(i?'L':'M')+X(v[0]).toFixed(2)+' '+Y(v[1]).toFixed(2)).join(' ')}${loop.closed?' Z':''}" fill="${loop.closed?'#b59671':'none'}" fill-rule="evenodd" stroke="#775e42" stroke-width="1.2"/>`).join('')}</g>`).join('');
   html+=`<path d="M${ox} ${Y(py)}H${720-ox}M${X(px)} ${oy}V${600-oy}" stroke="#678a76" stroke-width="1" stroke-dasharray="5 5"/>`;
   const label=(x,y,text)=>`<g><rect x="${x-31}" y="${y-12}" width="62" height="24" fill="#fafbf7"/><text x="${x}" y="${y+6}" fill="#275f48" font-size="19" font-family="Arial,sans-serif" font-weight="600" text-anchor="middle">${text}</text></g>`;
   const line=(x1,y1,x2,y2)=>`<path d="M${x1} ${y1}L${x2} ${y2}" stroke="#377057" stroke-width="2"/>`;
   horizontal.gaps.forEach(g=>{const x1=X(g.from),x2=X(g.to),y=Y(py);html+=line(x1,y,x2,y)+line(x1,y-5,x1,y+5)+line(x2,y-5,x2,y+5);if(x2-x1>40)html+=label((x1+x2)/2,y-17,cm(g.size));});
   vertical.gaps.forEach(g=>{const y1=Y(g.from),y2=Y(g.to),x=X(px);html+=line(x,y1,x,y2)+line(x-5,y1,x+5,y1)+line(x-5,y2,x+5,y2);if(y1-y2>28)html+=label(x+35,(y1+y2)/2,cm(g.size));});
   svg.innerHTML=`<title>${safe(m.name)}: vãos internos em centímetros</title>${html}<text x="20" y="25" fill="#275f48" font-size="18">Cotas em cm · ${safe({front:'frente',side:'lateral',top:'planta'}[view])}</text>`;
   for(const [key,val] of [['depth',depth-box.lo[c]],['a',px-box.lo[a]],['b',py-box.lo[b]]])details.querySelector(`[data-value="${key}"]`).textContent=cm(val)+' cm';
   const list=(title,result)=>`<div><strong>${title}</strong>${result.uncertain?'<p>Contorno aberto neste ponto; mova a linha para medir.</p>':result.gaps.length?`<ol>${result.gaps.map(g=>`<li><b>${cm(g.size)} cm</b><small>${safe(g.between.join(' ↔ '))}</small></li>`).join('')}</ol>`:'<p>Nenhum vão limitado por duas chapas nessa linha.</p>'}</div>`;
   details.querySelector('.internal-values').innerHTML=list('Vãos na linha horizontal',horizontal)+list('Vãos na linha vertical',vertical);
  }
  select.onchange=()=>{view=select.value;probes=[.27,.52];depthRatio=.5;reset();};
  details.querySelector('[data-internal="zoom"]').onchange=e=>{svg.style.width=Number(e.target.value)*100+'%';};
  svg.onclick=e=>{if(!frame)return;const p=svg.createSVGPoint();p.x=e.clientX;p.y=e.clientY;const q=p.matrixTransform(svg.getScreenCTM().inverse());probes=[Math.max(.001,Math.min(.999,(q.x-frame.ox)/(frame.w*frame.scale))),Math.max(.001,Math.min(.999,(600-frame.oy-q.y)/(frame.h*frame.scale)))];sliders.querySelector('[data-probe="a"]').value=probes[0]*1000;sliders.querySelector('[data-probe="b"]').value=probes[1]*1000;draw();};
  details.addEventListener('toggle',()=>{if(details.open&&!svg.childElementCount)reset();});
 }
 const previous=showModule;showModule=function(code){const result=previous(code);mount(code);return result;};
 window.GuedalaWorkshop.showModule=showModule;
})();
