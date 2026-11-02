/* Optional camera focus: remove this bundle to restore the previous selection behavior. */
(()=>{
 let saved=null,serial=0,frame=0,active=null,selecting=0;
 const keys=['room','view','angle','tilt','zoom','pan','upper','walls','inside','moduleFilter','focusPart','cameraBox'];
 const snapshot=()=>Object.fromEntries(keys.map(k=>[k,Array.isArray(state[k])?[...state[k]]:state[k]]));
 function stop(){cancelAnimationFrame(frame);frame=0;}
 function box(){const r=PROJECT.rooms.find(r=>r.id===state.room)||PROJECT.rooms[0];return state.cameraBox||[...r.bounds,0,PROJECT.ceiling];}
 function tween(target,done){stop();const from=snapshot(),start=performance.now(),a=box().slice(),b=target.cameraBox||a;state.view='iso';state.moduleFilter=null;
  const tick=now=>{const t=reducedMotion.matches?1:Math.min(1,(now-start)/800),e=t*t*(3-2*t);for(const k of ['angle','tilt','zoom'])state[k]=from[k]+(target[k]-from[k])*e;state.pan=from.pan.map((v,i)=>v+(target.pan[i]-v)*e);state.cameraBox=a.map((v,i)=>v+(b[i]-v)*e);moveCamera();requestRender();if(t<1)frame=requestAnimationFrame(tick);else{frame=0;done?.();}};frame=requestAnimationFrame(tick);
 }
 function restore(){if(!saved)return;const target=saved;saved=null;active=null;serial++;tween({...target,cameraBox:target.cameraBox||[...(PROJECT.rooms.find(r=>r.id===target.room)||PROJECT.rooms[0]).bounds,0,PROJECT.ceiling]},()=>{Object.assign(state,target);requestRender();});document.getElementById('moduleFocusActions')?.remove();}
 async function focus(code,request){if(window.GUEDALA_WEB&&!GUEDALA_WEB.geometryReady)await new Promise(resolve=>window.addEventListener('guedala-geometry-ready',resolve,{once:true}));if(request!==serial||work.module!==code||!INTERNAL_FRAMES[code])return;
  buildScene();const parts=nodes.filter(n=>n.module===code);if(!parts.some(n=>n.piece))return;
  saved??=snapshot();active=code;
  const b=[Math.min(...parts.map(n=>n.x))-10,Math.min(...parts.map(n=>n.z))-10,Math.max(...parts.map(n=>n.x+n.w))+10,Math.max(...parts.map(n=>n.z+n.d))+10,Math.min(...parts.map(n=>n.y))-8,Math.max(...parts.map(n=>n.y+n.h))+8];
  tween({cameraBox:b,angle:({quarto:-2.4,cozinha:2.8,lavanderia:2.5,banho:2.8,escritorio:-.7}[state.room]??state.angle),tilt:.35,zoom:1,pan:[0,0]});
  const host=$('selectedInfo');host.insertAdjacentHTML('afterbegin','<div id="moduleFocusActions" class="work-actions"><button data-focus="back">Voltar ao apartamento</button><button data-focus="inside">Ver por dentro</button><button data-focus="measure">Medidas internas</button></div>');
  host.querySelector('[data-focus="back"]').onclick=restore;
  host.querySelector('[data-focus="inside"]').onclick=()=>{stop();state.inside=!state.inside;requestRender();};
  host.querySelector('[data-focus="measure"]').onclick=()=>{const d=host.querySelector('.internal-consult');if(d){d.open=true;d.querySelector('.internal-expand')?.click();}};
 }
 const previous=showModule;showModule=async function(code){const request=++serial;stop();selecting++;try{await previous(code);}finally{selecting--;}if(request===serial)await focus(code,request);};window.GuedalaWorkshop.showModule=showModule;
 const room=setRoom;setRoom=function(id){stop();if(!selecting)serial++;if(saved){Object.assign(state,saved);saved=null;}active=null;return room(id);};window.GuedalaStudy.setRoom=setRoom;
 const canvas=$('scene');for(const event of ['pointerdown','wheel'])canvas.addEventListener(event,stop,{capture:true,passive:true});
 document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!document.querySelector('dialog[open]'))restore();});
 document.addEventListener('click',e=>{if(e.target.closest('#workBack'))restore();},true);
 window.GuedalaModuleFocus={restore,get active(){return active;},get animating(){return !!frame;}};
})();
