// Presentation layer: the existing scene and its geometry remain the source of truth.
const ROOM_PRESENTATION={
  all:['home','O apê inteiro'],sala:['sofa','Conversar e receber'],quarto:['bed','Descansar e guardar'],
  escritorio:['desk','Trabalhar e hospedar'],cozinha:['kitchen','Cozinhar e compartilhar'],
  lavanderia:['laundry','Cuidar da rotina'],banho:['bath','Uma pausa no dia']
};
function uiIcon(name){
  const paths={home:'<path d="m3 10 9-7 9 7v10H3Z"/><path d="M9 20v-7h6v7"/>',sofa:'<path d="M5 12V7a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v5M5 18v3m14-3v3"/><path d="M3 11h3v4h12v-4h3v8H3Z"/>',bed:'<path d="M3 20V5m18 15V9H3m0 8h18M6 5h5v4"/>',desk:'<path d="M2 13h20M4 13v8m16-8v8M6 3h12v7H6Zm6 7v3"/>',kitchen:'<path d="M3 9h18v12H3Zm0 5h18M12 9v12M5 3h4v3H5Zm10 0h4v3h-4Z"/>',laundry:'<rect x="4" y="2" width="16" height="20" rx="2"/><circle cx="12" cy="14" r="5"/><path d="M4 7h16m-12-3h1m3 0h1m-6 10q3-3 5 0t5 0"/>',bath:'<path d="M3 12h18v3a5 5 0 0 1-5 5H8a5 5 0 0 1-5-5ZM5 12V5a2 2 0 0 1 4 0M6 20v2m12-2v2M7 7h4"/>',arrow:'<path d="M4 12h16m-6-6 6 6-6 6"/>',spark:'<path d="m12 3 2.5 6.5L21 12l-6.5 2.5L12 21l-2.5-6.5L3 12l6.5-2.5Z"/>',game:'<path d="M8 7h8q4 0 5 8t-5 1H8q-6 7-5-1t5-8Z"/><path d="M7 10v5m-2-2.5h4m7-1h.1m2 2h.1"/>'};
  return `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${paths[name]||paths.home}</svg>`;
}
const STATE_OPTIONS=[
  {id:'sofaState',key:'sofa',rooms:['sala'],icon:'sofa',title:'Sofá da sala',hint:'Do bate-papo ao filme no sofá.',choices:[['closed','Fechado','110 cm'],['open','Esticado','136 cm'],['storage','Abrir baú','Demonstração']]},
  {id:'tableState',key:'table',rooms:['sala'],icon:'kitchen',title:'Mesa de jantar',hint:'Uma mesa que cresce para receber.',choices:[['compact','Dia a dia','150 × 75 cm'],['extended','Mesa aberta','180 × 75 cm']]},
  {id:'diningState',key:'dining',rooms:['sala'],icon:'home',title:'Cadeiras',hint:'Seis lugares com a mesa aberta.',choices:[['stored','Guardadas','3 na lateral'],['use','Em uso','Afastadas da mesa']]},
  {id:'officeState',key:'office',rooms:['escritorio'],icon:'desk',title:'Escritório',hint:'O espaço de trabalho também recebe hóspedes.',choices:[['work','Trabalhar','Sofá fechado'],['guest','Hospedar','Cama aberta']]},
  {id:'consoleState',key:'console',rooms:['sala','escritorio'],icon:'game',title:'Onde jogar?',hint:'Um PS5, duas possibilidades.',choices:[['sala','Na sala','TV principal'],['escritorio','No escritório','TV de 43″']]},
  {id:'dryState',key:'dry',rooms:['lavanderia'],icon:'laundry',title:'Varal',hint:'Estados ilustrativos; posição e mecanismo em estudo.',choices:[['stored','Recolhido','Sem roupas'],['high','Secando','No alto'],['low','Carregar','Na altura de uso']]}
];
const SCENARIOS=[
  {id:'daily',icon:'home',title:'Dia a dia',detail:'Tudo pronto para a rotina',values:{sofa:'closed',office:'work',table:'compact',dining:'stored',console:'sala',dry:'stored'}},
  {id:'friends',icon:'kitchen',title:'Receber amigos',detail:'Mesa aberta e cadeiras em uso',values:{sofa:'closed',office:'work',table:'extended',dining:'use',console:'sala',dry:'stored'}},
  {id:'guests',icon:'bed',title:'Hospedar',detail:'Escritório com a cama aberta',values:{sofa:'closed',office:'guest',table:'compact',dining:'stored',console:'sala',dry:'stored'}}
];
const TOUR_STEPS=[
  ['sala','A casa se abre para receber.','Experimente esticar o sofá ou abrir a mesa nos botões abaixo do desenho. Toque em um móvel para conhecer os detalhes.'],
  ['escritorio','Trabalho durante o dia. Quarto de hóspedes à noite.','Alterne entre Trabalhar e Hospedar para ver a transformação do sofá-cama.'],
  ['cozinha','Cada coisa tem seu lugar.','Toque nos armários para descobrir a organização interna, os materiais e os equipamentos.'],
  ['lavanderia','Uma rotina bem pensada.','Veja os estados ilustrativos do varal. A ficha da bancada reúne as escolhas do tanque e do cesto; o encaixe ainda está em estudo.'],
  ['quarto','Um lugar para descansar.','Toque no guarda-roupa para conhecer a organização interna. Use Planta para entender a distribuição.'],
  ['banho','Os detalhes fecham o conjunto.','Conheça os metais, o espelho e os revestimentos. Depois, explore as cores e materiais na aba do início da página.']
];
let tourIndex=-1,infoReturnTarget=null;
function buildRoomNavigation(){
  $('rooms').innerHTML=PROJECT.rooms.map(r=>`<button type="button" data-room="${r.id}" aria-pressed="${r.id==='all'}" class="room-card ${r.id==='all'?'active':''}"><span class="room-icon">${uiIcon(ROOM_PRESENTATION[r.id][0])}</span><span><strong>${esc(r.id==='all'?'Visão geral':r.name)}</strong><small>${esc(ROOM_PRESENTATION[r.id][1])}</small></span><span class="room-check" aria-hidden="true">✓</span></button>`).join('');
  document.querySelectorAll('[data-room]').forEach(b=>b.onclick=()=>{endTour();setRoom(b.dataset.room);});
}
function roomWelcome(id){
  return `<div class="inspector-welcome"><span class="detail-illustration">${uiIcon(ROOM_PRESENTATION[id][0])}</span><h2>${id==='all'?'O projeto, de perto.':esc(PROJECT.rooms.find(r=>r.id===id).name)}</h2><p>Toque em um móvel no desenho${id==='all'?' ou escolha um ambiente acima':' ou na lista abaixo'} para ver materiais, medidas e decisões.</p><div class="detail-legend"><span><i class="dot approved"></i>Escolhido para o projeto</span><span><i class="dot pending"></i>Ainda precisa de conferência</span></div><small>Um estudo para imaginar a casa. As medidas finais e a execução ainda serão conferidas.</small></div>`;
}
function syncExperience(){
  if(!$('experiencePanel'))return;
  const overview=state.room==='all';
  $('scenarioPresets').hidden=!overview;
  $('stateCards').hidden=overview;
  $('experienceTitle').textContent=overview?'Como vamos usar o apê?':'Experimente as mudanças';
  $('experienceIntro').textContent=overview?'Escolha uma cena e veja o apartamento mudar.':'Toque em uma opção para ver a mudança no desenho.';
  let visible=0;
  STATE_OPTIONS.forEach(config=>{
    const select=$(config.id),card=select.closest('.stategroup');
    const show=config.rooms.includes(state.room);card.hidden=!show;if(show)visible++;
    select.value=state[config.key];
    card.querySelectorAll('[data-choice]').forEach(b=>{const active=b.dataset.choice===state[config.key];b.classList.toggle('active',active);b.setAttribute('aria-pressed',String(active));});
  });
  $('noRoomChanges').hidden=overview||visible>0;
  $('experienceIntro').hidden=!overview&&visible===0;
  $('resetExperience').hidden=!overview&&visible===0;
  document.querySelectorAll('[data-scenario]').forEach(b=>{const s=SCENARIOS.find(s=>s.id===b.dataset.scenario);const active=Object.entries(s.values).every(([key,value])=>state[key]===value);b.classList.toggle('active',active);b.setAttribute('aria-pressed',String(active));});
  $('objectList').hidden=overview;
  document.querySelector('.list-heading').hidden=overview;
}
function applyScenario(scenario){
  const from=new Map(nodes.map(n=>[n.key,{...n}]));
  Object.assign(state,scenario.values);
  motion=reducedMotion.matches?null:{from,start:performance.now(),duration:1700,key:'office',goal:state.office};
  updateMetrics();drawLists();syncExperience();requestRender();
  $('stateAnnouncement').textContent=`Cena ${scenario.title}: ${scenario.detail}.`;
}
function closeInspector(){
  $('inspector').classList.remove('open');$('inspector').removeAttribute('role');$('inspector').removeAttribute('aria-modal');
  if(infoReturnTarget?.isConnected)infoReturnTarget.focus({preventScroll:true});
  else $('mobileItems').focus({preventScroll:true});
}
function endTour(){tourIndex=-1;$('tourBar').hidden=true;}
function showTourStep(index){
  tourIndex=index;const [room,title,description]=TOUR_STEPS[index];
  setRoom(room);$('tourBar').hidden=false;
  $('tourProgress').textContent=`VISITA GUIADA · ${index+1} DE ${TOUR_STEPS.length}`;
  $('tourTitle').textContent=title;$('tourDescription').textContent=description;
  $('tourPrevious').disabled=index===0;
  $('tourNext').textContent=index===TOUR_STEPS.length-1?'Concluir visita ✓':'Próximo ambiente →';
  $('tourTitle').focus({preventScroll:true});$('tourBar').scrollIntoView({behavior:reducedMotion.matches?'instant':'smooth',block:'start'});
}
function initializeExperience(){
  STATE_OPTIONS.forEach(config=>{
    const select=$(config.id),card=select.closest('.stategroup');
    select.hidden=true;card.querySelector('label').hidden=true;
    card.insertAdjacentHTML('afterbegin',`<div class="state-card-heading"><span class="state-icon">${uiIcon(config.icon)}</span><div><h3 id="${config.id}Title">${config.title}</h3><p>${config.hint}</p></div></div><div class="choice-buttons" role="group" aria-labelledby="${config.id}Title">${config.choices.map(([value,label,note])=>`<button type="button" data-choice="${value}" aria-pressed="false"><strong>${label}</strong><small>${note}</small><span class="choice-check" aria-hidden="true">✓</span></button>`).join('')}</div>`);
    card.querySelectorAll('[data-choice]').forEach(b=>b.onclick=()=>{select.value=b.dataset.choice;select.dispatchEvent(new Event('change',{bubbles:true}));$('stateAnnouncement').textContent=`${config.title}: ${config.choices.find(c=>c[0]===b.dataset.choice)[1]}.`;});
  });
  $('scenarioPresets').innerHTML=SCENARIOS.map(s=>`<button type="button" data-scenario="${s.id}" aria-pressed="false"><span class="scenario-icon">${uiIcon(s.icon)}</span><strong>${s.title}</strong><small>${s.detail}</small><span class="choice-check" aria-hidden="true">✓</span></button>`).join('');
  document.querySelectorAll('[data-scenario]').forEach(b=>b.onclick=()=>applyScenario(SCENARIOS.find(s=>s.id===b.dataset.scenario)));
  $('seeScene').onclick=()=>$('stage').scrollIntoView({behavior:reducedMotion.matches?'instant':'smooth',block:'center'});
  $('resetExperience').onclick=()=>{applyScenario(SCENARIOS[0]);$('fit').click();toast('De volta à configuração do dia a dia.');};
  $('helpButton').onclick=()=>$('helpDialog').showModal();
  $('closeHelp').onclick=$('helpExplore').onclick=()=>$('helpDialog').close();
  $('startTour').onclick=()=>showTourStep(0);
  $('helpTour').onclick=()=>{$('helpDialog').close();tab('model');showTourStep(0);};
  $('tourPrevious').onclick=()=>showTourStep(Math.max(0,tourIndex-1));
  $('tourNext').onclick=()=>{if(tourIndex<TOUR_STEPS.length-1)showTourStep(tourIndex+1);else{endTour();setRoom('all');$('startTour').focus({preventScroll:true});$('rooms').scrollIntoView({behavior:'smooth',block:'center'});toast('Agora explore à vontade. As cores e materiais estão na aba do início.');}};
  $('tourExit').onclick=()=>{endTour();document.querySelector(`[data-room="${state.room}"]`).focus({preventScroll:true});};
  $('inspector').insertAdjacentHTML('beforebegin','<button id="inspectorBackdrop" class="inspector-backdrop" aria-label="Fechar detalhes do móvel" tabindex="-1"></button>');
  $('inspectorBackdrop').onclick=closeInspector;
  document.addEventListener('keydown',e=>{
    if(!$('inspector').classList.contains('open')||!matchMedia('(max-width:1150px)').matches)return;
    if(e.key==='Escape'){e.preventDefault();closeInspector();}
    if(e.key==='Tab'){
      const focusable=[...$('inspector').querySelectorAll('button,a[href],summary,[tabindex="0"]')].filter(el=>el.getClientRects().length);
      const first=focusable[0],last=focusable.at(-1);
      if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus();}
      else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus();}
    }
  });
  $('inspector').setAttribute('aria-label','Detalhes do móvel');
  syncExperience();
}
