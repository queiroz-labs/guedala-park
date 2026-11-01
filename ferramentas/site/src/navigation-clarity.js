/* Navegação curta; os destinos antigos continuam disponíveis por seus endereços. */
;(function(){
 const header=document.querySelector('.mast'),nav=header?.querySelector('nav');if(!nav)return;
 const brand=header.querySelector('.brand');brand.setAttribute('role','link');brand.setAttribute('tabindex','0');brand.setAttribute('aria-label','Comece aqui');
 const home=()=>tab('architect');brand.addEventListener('click',home);brand.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();home();}});
 const menu=document.createElement('details');menu.className='nav-more';menu.innerHTML='<summary>Mais</summary><div class="nav-more-content"><button type="button" data-destination="mood">Imagens e materiais</button><button type="button" data-destination="chaves">Dia das chaves</button><button type="button" data-destination="architect">Comece aqui</button></div>';
 nav.append(menu);menu.querySelectorAll('[data-destination]').forEach(b=>b.onclick=()=>{tab(b.dataset.destination);menu.open=false;});
 const help=document.getElementById('helpButton'),gloss=document.getElementById('glossaryButton');help.textContent='Ajuda';
 if(gloss){gloss.remove();const link=document.createElement('button');link.type='button';link.textContent='Códigos do projeto';link.onclick=()=>GuedalaGlossary.open();document.getElementById('helpDialog')?.querySelector('.help-footer')?.append(link);}
 const rooms=document.getElementById('rooms'),quick=document.querySelector('.room-quick');
 if(rooms&&quick){quick.remove();rooms.setAttribute('aria-label','Escolha um cômodo');}
 const workspace=document.querySelector('#model .workspace');
 if(workspace){const roomView=document.createElement('button');roomView.type='button';roomView.className='room-materials-link';roomView.textContent='Ver imagens e materiais deste cômodo →';roomView.onclick=()=>{state.moodRoom=state.room;tab('mood');};workspace.querySelector('.display-options')?.before(roomView);}
 const tools=document.querySelector('.viewtools'),floor=tools?.querySelector('[data-tab="floorplan"]');if(floor)floor.textContent='Ver planta com medidas';
 const info=document.querySelector('.welcome-copy');if(info){info.querySelector('.eyebrow')?.remove();const h=info.querySelector('h1');if(h)h.textContent='Explore o apartamento.';const p=info.querySelector('p');if(p)p.textContent='Escolha um cômodo e toque no desenho para ver medidas e detalhes.';}
 const notice=header.querySelector('.global-project-notice');if(notice)notice.textContent='Medidas do projeto; confira no imóvel.';
 const empty=document.querySelector('#selectedInfo .inspector-welcome');if(empty)empty.querySelectorAll('button[data-room]').forEach(b=>b.remove());
 const tally=document.getElementById('decisionTally');if(tally){const explain=document.createElement('p');explain.className='decision-explanation';explain.textContent='Uma escolha pode estar feita e ainda precisar de conferência antes da compra ou instalação.';tally.after(explain);}
 const docSearch=document.getElementById('docSearch');if(docSearch){docSearch.setAttribute('aria-label','Buscar documentos');docSearch.setAttribute('placeholder','Buscar documentos…');}
 const footer=document.querySelector('footer span');if(footer)footer.textContent='Medidas do projeto em cm no 3D e em mm nas fichas; confira antes de fabricar.';
})();
