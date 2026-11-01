/* O cabeçalho mantém a altura durante a rolagem, sem compensação de layout. */
;(function(){
 const mast=document.querySelector('.mast');
 document.querySelectorAll('.mast-compensation').forEach(n=>n.remove());mast.classList.remove('mast-compact');
 function measure(){
  const h=mast.getBoundingClientRect().height;
  document.documentElement.style.setProperty('--mast-h',h+'px');
 }
 window.addEventListener('resize',measure);new ResizeObserver(measure).observe(mast);measure();
 globalThis.GuedalaMobileHeader={expand:measure,measure,get compact(){return false;}};
})();
