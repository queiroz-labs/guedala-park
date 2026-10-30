/* Busca sempre alcançável; compensação conserva o fluxo quando a marca recolhe. */
;(function(){
 const mast=document.querySelector('.mast'),media=matchMedia('(max-width:760px)');
 document.querySelectorAll('.mast-compensation').forEach(n=>n.remove());mast.classList.remove('mast-compact');
 let compact=false,fullHeight=mast.getBoundingClientRect().height,lastY=scrollY,pending=false;
 const spacer=document.createElement('div');spacer.className='mast-compensation';spacer.setAttribute('aria-hidden','true');mast.after(spacer);
 function measure(){
  const h=mast.getBoundingClientRect().height;if(!compact)fullHeight=h;
  spacer.style.height=media.matches?Math.max(0,fullHeight-h)+'px':'0px';
 }
 function apply(next){compact=next;mast.classList.toggle('mast-compact',next);measure();}
 function scroll(){
  pending=false;const y=window.scrollY,delta=y-lastY;lastY=y;
  apply(GuedalaMobileUX.headerState(compact,{width:innerWidth,y,delta,searchFocused:!!document.activeElement?.closest('.global-search')}));
 }
 window.addEventListener('scroll',()=>{if(!pending){pending=true;requestAnimationFrame(scroll);}},{passive:true});
 mast.addEventListener('focusin',event=>{if(event.target.closest('.global-search'))apply(false);});
 function resize(){const previous=compact;mast.classList.remove('mast-compact');fullHeight=mast.getBoundingClientRect().height;apply(media.matches&&previous);}
 window.addEventListener('resize',resize);new ResizeObserver(measure).observe(mast);measure();
 globalThis.GuedalaMobileHeader={expand:()=>apply(false),measure,get compact(){return compact;}};
})();
