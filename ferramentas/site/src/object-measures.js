/* Consulta em cm. Nenhuma dimensão aqui é levantamento de obra. */
const OBJECT_GRAPHIC='estimativa gráfica',OBJECT_NOMINAL='projeto/nominal';
const OBJECT_PRODUCTS=new Set(['bed','bonnie','daiane','officechair','tv50','tv43','soundbar','ps5','fridge','cooktop','oven','microwave','hood','filter','washer','airfryer','heater','toilet','basin','dishrack','trash','recycling','table','diningchairs']);
const OBJECT_PENDING=new Set(['coffeemaker','hotwater','bathfinish','tower','counterlight','laundrypower','laundrylight']);
let objectSelected=null,objectReturn=null;
function objectKey(n){return n.source?'cad/'+n.source:n.key;}
function objectCategory(n){
 if(!n.id)return ({door:'porta',glass:'janela',wall:'parede',floor:'piso'})[n.kind]||'acabamento';
 if(n.mat==='stone')return 'pedra';
 if(['oven','microwave','fridge','cooktop','hood','filter','washer','airfryer','heater','coffeemaker'].includes(n.id))return 'eletrodoméstico';
 if(['tv50','tv43','soundbar','setup','ps5'].includes(n.id))return 'eletrônico';
 if(['sink','basin','bath tap','toilet','hygiene','shower','drying','bathshaft','tower','laundrypower','hotwater','power'].includes(n.id))return 'instalação';
 if(/light$/.test(n.id))return 'iluminação';
 return 'móvel';
}
function objectName(n){
 if(n.source){if(STONE_PARTS[n.id]&&n.mat==='stone')return STONE_PARTS[n.id][0];return (n.label||ITEMS.find(i=>i.id===n.id)?.name||n.source).replaceAll('_',' ').replace(/\bR\d{2,3}\b/g,'').replace(/\s+\d+$/,'').replace(/\s+/g,' ').trim();}
 if(n.id==='decor')return 'Vaso decorativo';
 if(n.id)return STONE_PARTS[n.id]&&n.mat==='stone'?STONE_PARTS[n.id][0]:ITEMS.find(i=>i.id===n.id)?.name||n.id;
 const room=PROJECT.rooms.find(r=>r.id===n.room)?.name||n.room;
 const finish=n.h===3?'Peitoril':n.h===33?'Persiana':n.h===8&&(n.w===1.5||n.d===1.5)?'Rodapé':'Peça de acabamento';
 return (({door:'Porta',glass:'Janela',wall:'Trecho de parede',floor:'Trecho de piso'})[n.kind]||finish)+' · '+room+' · '+n.key.split('/').pop();
}
function objectRecord(n,scene=nodes){
 const pending=n.pending||OBJECT_PENDING.has(n.id),category=objectCategory(n),room=PROJECT.rooms.find(r=>r.id===n.room)?.name||n.room;
 let box={x:n.x,y:n.y,z:n.z,w:n.w,d:n.d,h:n.h};
 // The bed body is explicitly 188 × 128 × 64; pillows are not the product height.
 if(n.id==='bed')box={x:state.headDepth,y:0,z:136,w:188,d:128,h:64};
 // Full-height architectural data, independent of the cutaway display height.
 if(!n.id&&n.kind==='door')box.h=205;
 if(!n.id&&n.kind==='glass')box.h=110;
 if(!n.id&&n.kind==='wall')box.h=n.underWindow?92:n.y>0?PROJECT.ceilingByRoom[n.room]-n.y:PROJECT.ceilingByRoom[n.room];
 const finite=!pending&&['x','y','z','w','d','h'].every(k=>Number.isFinite(box[k]));
 const reliability=finite?(n.source||OBJECT_PRODUCTS.has(n.id)?OBJECT_NOMINAL:OBJECT_GRAPHIC):'pendente';
 let reference=n.source?'Modelo · '+n.source:'Desenho do site · '+(n.id||n.key);
 const fields=[],add=(name,value,confidence)=>fields.push({name,value,confidence});
 const num=v=>cmTxt(v)+' cm';
 if(finite){
  add('Largura × profundidade × altura',[box.w,box.d,box.h].map(cmTxt).join(' × ')+' cm',reliability);
  add('Posição x / y / z',[box.x,box.y,box.z].map(cmTxt).join(' / ')+' cm',OBJECT_GRAPHIC);
  add('Base a partir do piso',num(box.y),OBJECT_GRAPHIC);add('Topo a partir do piso',num(box.y+box.h),OBJECT_GRAPHIC);
  if(!n.id&&['door','glass'].includes(n.kind)){
   add('Vão (largura × altura)',cmTxt(Math.max(box.w,box.d))+' × '+(n.kind==='door'?'205':'113')+' cm',OBJECT_GRAPHIC);
   if(n.kind==='glass')add('Peitoril',num(92),OBJECT_GRAPHIC);
   add('Sentido de abertura','A conferir', 'pendente');
  }
  // Shared boundaries are tagged to one room only in the drawing. Search all
  // wall segments and merge collinear pieces before choosing the closest two.
  const walls=scene.filter(q=>!q.id&&q.kind==='wall'&&q.y===0&&q.key!==n.key),lines=new Set();
  const nearest=walls.map(q=>({q,distance:Math.hypot(Math.max(q.x-(box.x+box.w),box.x-(q.x+q.w),0),Math.max(q.z-(box.z+box.d),box.z-(q.z+q.d),0))})).sort((a,b)=>a.distance-b.distance).filter(({q})=>{const line=q.w>q.d?'z/'+q.z:'x/'+q.x;if(lines.has(line))return false;lines.add(line);return true;}).slice(0,2);
  nearest.forEach(({distance},i)=>add('Parede próxima '+(i+1),num(distance),OBJECT_GRAPHIC));
  reference+=' · paredes: '+nearest.map(({q})=>q.key).join(', ');
  if(nearest.length<2)add('Distância às paredes','Referências insuficientes','pendente');
 }else add('Medidas','Sem medida definida','pendente');
 return {key:objectKey(n),id:n.id,module:n.module,name:objectName(n),room,roomId:n.room,category,box:finite?box:null,reliability,reference,fields,node:n};
}
function objectRecords(){
 const list=nodes.map(n=>objectRecord(n));
 for(const it of ITEMS.filter(i=>!nodes.some(n=>n.id===i.id)))list.push(objectRecord({id:it.id,key:'pending/'+it.id,room:activeRoom(it),pending:true}));
 return list;
}
function objectFieldsHTML(r){return `<div class="object-measure-summary" data-object-key="${esc(r.key)}"><strong>${esc(r.name)}</strong><p>${esc(r.room)} · ${esc(r.category)}</p><dl>${r.fields.map(f=>`<dt>${esc(f.name)}</dt><dd>${esc(f.value)} <span class="measure-confidence">${esc(f.confidence)}</span></dd>`).join('')}</dl><details><summary>Referência e eixos</summary><p>${esc(r.reference)}. Largura no eixo x; profundidade no eixo z; altura no eixo y. Posição pelo canto inferior do volume, no zero do desenho. Distâncias em planta até os trechos de parede representados; confira no imóvel. O volume não inclui todas as folgas de instalação.</p></details><div class="object-actions"><button type="button" data-copy-object="text">Copiar medidas</button><button type="button" data-copy-object="table">Copiar como tabela</button></div><p class="object-copy-status" role="status"></p></div>`;}
function objectCopy(r,table=false){
 const fields=[['Objeto',r.name,''],['Cômodo',r.room,''],['Categoria',r.category,''],...r.fields.map(f=>[f.name,f.value,f.confidence]),['Referência',r.reference,'']];
 return table?fields.map(row=>row.join('\t')).join('\n'):fields.map(([k,v,c])=>k+': '+v+(c?' ['+c+']':'')).join('\n');
}
async function copyObjectText(text,host){
 try{if(navigator.clipboard&&window.isSecureContext)await navigator.clipboard.writeText(text);else{const input=document.createElement('textarea');input.value=text;input.style.position='fixed';input.style.top='0';host.appendChild(input);input.select();const ok=document.execCommand('copy');input.remove();if(!ok)throw Error('copy');}host.querySelector('.object-copy-status').textContent='Medidas copiadas.';}
 catch{const input=document.createElement('textarea');input.readOnly=true;input.value=text;input.setAttribute('aria-label','Medidas para copiar');host.appendChild(input);input.focus();input.select();host.querySelector('.object-copy-status').textContent='Selecione o texto e copie.';}
}
function bindObjectCopy(host,r){host.querySelectorAll('[data-copy-object]').forEach(b=>b.onclick=()=>copyObjectText(objectCopy(r,b.dataset.copyObject==='table'),host));}
function closeObjectCard(){const card=$('objectMeasureCard');if(card)card.hidden=true;if(objectReturn?.isConnected)objectReturn.focus({preventScroll:true});}
function showObjectCard(r){
 let card=$('objectMeasureCard');if(!card){card=document.createElement('section');card.id='objectMeasureCard';card.className='object-measure-card';card.setAttribute('aria-label','Medidas do objeto');$('stage').insertAdjacentElement('afterend',card);}
 card.hidden=false;card.innerHTML='<button type="button" class="object-card-close" aria-label="Fechar medidas">×</button>'+objectFieldsHTML(r)+(ITEMS.some(i=>i.id===r.id)?'<button type="button" data-full-object>Ver ficha completa</button>':'');
 card.querySelector('.object-card-close').onclick=closeObjectCard;bindObjectCopy(card,r);
 const full=card.querySelector('[data-full-object]');if(full)full.onclick=()=>inspectObject(r.node,true);
 card.tabIndex=-1;card.focus({preventScroll:true});
}
function objectHighlight(r){
 objectSelected=r.key;state.selected=r.id||null;
 // Stable per-node outline, including anonymous architecture and individual CAD pieces.
 requestRender();if(typeof drawObjectList==='function')drawObjectList();
}
async function inspectObject(n,forceFicha=false){
 if(n.room!==state.room&&(state.room!=='all'||n.module))setRoom(n.room);
 const r=objectRecord(nodes.find(q=>objectKey(q)===objectKey(n))||n);objectReturn=document.activeElement;objectHighlight(r);closeObjectCard();
 if(r.module&&CAD_DATA.modules.some(m=>m.code===r.module))await showModule(r.module);
 else if(ITEMS.some(i=>i.id===r.id)&&(!n.pending||forceFicha))work.previousSelect(r.id,false);
 else {showObjectCard(r);return;}
 if(objectSelected!==r.key)return;
 const host=$('selectedInfo');host.insertAdjacentHTML('afterbegin',objectFieldsHTML(r));bindObjectCopy(host,r);
 $('inspector').classList.add('open');$('inspector').removeAttribute('aria-modal');$('inspector').removeAttribute('role');
 // Keep the model visible on touch screens: the sheet occupies normal document flow.
 if(matchMedia('(max-width:1150px)').matches)$('inspector').classList.add('object-inspector');
 requestRender();
}
function initializeObjectMeasures(){
 const beforeRoom=setRoom;setRoom=function(id){closeObjectCard();objectSelected=null;beforeRoom(id);if(typeof syncObjectList==='function')syncObjectList(id);};
 const beforeTransition=transitionState;transitionState=function(...args){closeObjectCard();beforeTransition(...args);};
 Object.assign(window.GuedalaStudy,{objectRecords,objectRecord,objectCopy,inspectObject,setRoom,transitionState,getSelectedObject:()=>objectSelected});
}
initializeObjectMeasures();
