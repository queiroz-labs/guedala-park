// Interactive frontal study of kitchen cabinet C. Geometry and objects are illustrative.
const KitchenCabinetTour=(()=>{
 const levels={
  C1:{title:'Pratos do dia a dia',status:'Organização aprovada',description:'Quatro pratos rasos em uma pilha. Na outra, quatro pratos de sobremesa ficam sobre quatro pratos fundos; levante os de sobremesa para pegar os fundos.',check:'Diâmetros, altura das pilhas, folga das dobradiças e retirada ainda precisam de conferência.'},
  C2:{title:'Copos e canecas',status:'Organização aprovada',description:'Seis copos e quatro canecas. Dois copos e duas canecas ficam na frente; as demais peças ficam atrás.',check:'Conferir altura, alças e alcance da fileira traseira com as peças reais.'},
  C3:{title:'Potes vazios e panos limpos',status:'Organização funcional aprovada',description:'Potes vazios em bandeja removível, tampas separadas e panos limpos em uma caixa. A posição dos organizadores é uma proposta de estudo.',check:'Tamanho dos potes, bandeja, caixa e acesso em altura ainda precisam de teste.'},
  C4:{title:'Reserva superior',status:'Conteúdo em estudo',description:'Nível alto reservado para itens leves e pouco usados. Ainda não há um conjunto de objetos aprovado para este espaço.',check:'Taças, xícaras e pires dependem de medidas, estabilidade e acesso antes de aparecerem como conteúdo definitivo.'}
 };
 const objects={
  C4:'<span class="ct-reserve">Reserva em estudo</span>',
  C3:'<span class="ct-bin ct-towels">Panos</span><span class="ct-bin ct-pots">Potes e tampas</span>',
  C2:'<span class="ct-cups" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i><i></i></span><span class="ct-mugs" aria-hidden="true"><i></i><i></i><i></i><i></i></span>',
  C1:'<span class="ct-plates ct-plates-left" aria-hidden="true"><i></i><i></i><i></i><i></i></span><span class="ct-plates ct-plates-right" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></span>'
 };
 function markup(){return `<section class="cabinet-tour" aria-label="Explorar o armário C da cozinha">
  <div class="ct-intro"><span class="eyebrow">COZINHA · AÉREO SOBRE A PIA</span><h4>Abra o armário C</h4><p>Toque nas portas e escolha um nível para entender a organização interna.</p></div>
  <div class="ct-layout"><div class="ct-visual"><div class="ct-box" data-left="closed" data-right="closed">
   <div class="ct-interior">${['C4','C3','C2','C1'].map(id=>`<button type="button" class="ct-shelf" data-level="${id}" aria-label="Ver ${id}: ${levels[id].title}"><strong>${id}</strong><span class="ct-objects">${objects[id]}</span></button>`).join('')}</div>
   <button type="button" class="ct-door ct-left" data-door="left" aria-label="Abrir porta esquerda" aria-expanded="false"><span></span></button>
   <button type="button" class="ct-door ct-right" data-door="right" aria-label="Abrir porta direita" aria-expanded="false"><span></span></button>
  </div><p class="ct-visual-caption">Vista frontal ilustrativa · portas e objetos sem medidas executivas</p></div>
  <div class="ct-controls"><button type="button" class="ct-both primary-button">Abrir as duas portas</button><p class="ct-prompt">Depois, selecione uma prateleira:</p><div class="ct-level-buttons">${['C1','C2','C3','C4'].map(id=>`<button type="button" data-choose="${id}" aria-pressed="false">${id}</button>`).join('')}</div><div class="ct-detail" role="status" aria-live="polite"><h5>Interior do armário</h5><p>Abra as portas para explorar as quatro divisões aprovadas.</p></div><p class="ct-caveat">As alturas e o cabimento são hipóteses de projeto. A animação mostra a organização, sem validar ferragens ou movimentos reais.</p></div></div>
 </section>`;}
 function bind(parent){
  const tour=parent.querySelector('.cabinet-tour'),box=tour.querySelector('.ct-box'),both=tour.querySelector('.ct-both'),detail=tour.querySelector('.ct-detail');
  function update(){
   for(const side of ['left','right']){const button=tour.querySelector(`[data-door="${side}"]`),open=box.dataset[side]==='open';button.setAttribute('aria-expanded',String(open));button.setAttribute('aria-label',`${open?'Fechar':'Abrir'} porta ${side==='left'?'esquerda':'direita'}`);}
   const open=box.dataset.left==='open'&&box.dataset.right==='open';both.textContent=open?'Fechar as duas portas':'Abrir as duas portas';
  }
  function choose(id){box.dataset.left='open';box.dataset.right='open';update();tour.querySelectorAll('[data-level]').forEach(b=>b.classList.toggle('selected',b.dataset.level===id));tour.querySelectorAll('[data-choose]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.choose===id)));
   const level=levels[id];detail.innerHTML=`<span class="ct-detail-label">${id} · ${level.status}</span><h5>${level.title}</h5><p>${level.description}</p><small>${level.check}</small>`;
  }
  tour.querySelectorAll('[data-door]').forEach(button=>button.onclick=()=>{const side=button.dataset.door;box.dataset[side]=box.dataset[side]==='open'?'closed':'open';update();});
  both.onclick=()=>{const open=box.dataset.left==='open'&&box.dataset.right==='open';box.dataset.left=box.dataset.right=open?'closed':'open';update();};
  tour.querySelectorAll('[data-level]').forEach(button=>button.onclick=()=>choose(button.dataset.level));
  tour.querySelectorAll('[data-choose]').forEach(button=>button.onclick=()=>choose(button.dataset.choose));
 }
 return {markup,bind};
})();
