/* Cinco desenhos de leitura; não representam medidas do imóvel. */
;(function(root){
  const shapes={
    altura:['Altura do chão','<path d="M20 78H140M20 12H140M80 20V70M72 28L80 20L88 28M72 62L80 70L88 62"/>'],
    largura:['Largura','<path d="M20 20V76M140 20V76M28 48H132M36 40L28 48L36 56M124 40L132 48L124 56"/>'],
    distancia:['Entre dois pontos','<circle cx="28" cy="68" r="7"/><circle cx="132" cy="24" r="7"/><path d="M40 63L120 29M50 65L40 63L46 54M110 27L120 29L114 38"/>'],
    nivel:['Chão reto ou inclinado','<path d="M20 72L140 54M20 38H140"/><rect x="45" y="22" width="70" height="24" rx="4"/><circle cx="80" cy="34" r="5"/>'],
    prumo:['Parede reta ou inclinada','<path d="M28 14V72M20 72L28 82L36 72ZM65 82L80 14M32 28H76M32 64H68"/>']
  };
  root.GuedalaFieldIcons=Object.fromEntries(Object.entries(shapes).map(([key,[label,shape]])=>[key,{label,
    svg:`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 96" role="img" aria-label="${label}" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">${shape}</svg>`}]));
})(globalThis);
