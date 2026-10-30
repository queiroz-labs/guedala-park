/* Abas continuam botões: setas/Home/End e revelação apenas horizontal. */
;(function(){
 const nav=document.querySelector('.mast nav'),api=GuedalaMobileUX;
 let strip=nav.closest('.mast-tab-strip');if(!strip){strip=document.createElement('div');strip.className='mast-tab-strip';nav.before(strip);strip.append(nav);}
 if(!document.getElementById('tabsHelp'))strip.insertAdjacentHTML('beforeend','<span id="tabsHelp" class="sr-only">Há mais seções à direita ou à esquerda. Use as setas, Home e End para escolher uma aba.</span>');
 nav.setAttribute('aria-describedby','tabsHelp');
 function hints(){const edges=api.tabEdges(nav.scrollLeft,nav.clientWidth,nav.scrollWidth);strip.classList.toggle('has-more-left',edges.left);strip.classList.toggle('has-more-right',edges.right);}
 function reveal(button=nav.querySelector('[data-tab].active')){
  if(!button){hints();return;}const box=nav.getBoundingClientRect(),r=button.getBoundingClientRect();
  nav.scrollLeft=api.tabScroll({left:r.left,right:r.right,viewLeft:box.left,viewRight:box.right,scrollLeft:nav.scrollLeft});hints();
 }
 nav.addEventListener('scroll',hints,{passive:true});
 nav.addEventListener('focusin',event=>{const b=event.target.closest('[data-tab]');if(b)reveal(b);});
 nav.addEventListener('keydown',event=>{
  if(!['ArrowLeft','ArrowRight','Home','End'].includes(event.key)||event.altKey||event.ctrlKey||event.metaKey)return;
  const buttons=[...nav.querySelectorAll('button[data-tab]')],current=buttons.indexOf(event.target);if(current<0)return;
  event.preventDefault();let index=event.key==='Home'?0:event.key==='End'?buttons.length-1:(current+(event.key==='ArrowRight'?1:-1)+buttons.length)%buttons.length;
  const button=buttons[index];button.click();button.focus({preventScroll:true});reveal(button);
 });
 window.addEventListener('guedala-tab-change',()=>requestAnimationFrame(()=>reveal()));
 window.addEventListener('resize',()=>reveal());new ResizeObserver(hints).observe(nav);requestAnimationFrame(()=>reveal());
 globalThis.GuedalaTabStrip={reveal,hints};
})();
