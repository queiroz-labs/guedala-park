'use strict';
const $=id=>document.getElementById(id), esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const MAT=Object.fromEntries(PROJECT.materials.map(m=>[m.id,m]));
const WARDROBE_IMAGE='/*WARDROBE*/';
const state={room:'all',view:'iso',angle:-.62,tilt:.92,side:'east',sideCut:true,zoom:1,pan:[0,0],sofa:'closed',office:'work',dining:'stored',table:'compact',console:'sala',dry:'stored',sofaGap:0,rackDepth:37,headDepth:5,upper:true,walls:false,measures:true,inside:false,selected:null};
// Nominal body-to-body distances; handles, people and door swings are separate.
function diningClearance(st=state){const length=st.table==='compact'?150:180,end=465+length/2;return {length,start:465-length/2,end,gain:(180-length)/2,tableToFridge:615.25-end,headChairToFridge:615.25-561,entryWidth:85};}
const cm=n=>String(Math.round(n*100)/100).replace('.',',');
let nodes=[],hitFaces=[],lastProject=null,renderQueued=false,nodeSequence={},motion=null;
const reducedMotion=matchMedia('(prefers-reduced-motion: reduce)');
function transitionState(key,value){
  const from=new Map(nodes.map(n=>[n.key,{...n}]));state[key]=value;
  motion=reducedMotion.matches?null:{from,start:performance.now(),duration:key==='office'?1700:850,key,goal:value};
  updateMetrics();drawLists();requestRender();
}
function sampleMotion(now){
  if(!motion)return;
  const elapsed=(now-motion.start)/motion.duration,seen=new Set();
  const ease=t=>{t=Math.max(0,Math.min(1,t));return t*t*(3-2*t);};
  nodes=nodes.map(n=>{
    seen.add(n.key);const a=motion.from.get(n.key);let t=elapsed;
    if(motion.key==='office'){
      const chairFirst=motion.goal==='guest';
      if(n.id==='officechair')t=chairFirst?elapsed/.35:(elapsed-.65)/.35;
      if(n.id==='daiane')t=chairFirst?(elapsed-.3)/.7:elapsed/.7;
    }
    const u=ease(t);if(!a)return {...n,opacity:u};
    const out={...n};for(const k of ['x','y','z','w','d','h','tiltZ','yaw','rootX','rootZ'])out[k]=(a[k]||0)+((n[k]||0)-(a[k]||0))*u;
    let delta=(n.rot||0)-(a.rot||0);delta=Math.atan2(Math.sin(delta),Math.cos(delta));out.rot=(a.rot||0)+delta*u;
    out.opacity=(a.opacity??1)+((n.opacity??1)-(a.opacity??1))*u;return out;
  });
  for(const [key,n] of motion.from)if(!seen.has(key))nodes.push({...n,opacity:(n.opacity??1)*(1-ease(elapsed))});
  if(elapsed>=1)motion=null;
}
function cabinet(id,room,x,z,w,d,y,h,mat,shelves=[],dividers=[],flags={}){
 if(!state.inside){add(id,room,x,z,w,d,y,h,mat,'box',flags);add(id,room,x+w/2-.2,z-.2,.4,.4,y,h,'#b4ae9e','box',flags);return;}
 const a=(xx,zz,ww,dd,yy,hh,m=mat)=>add(id,room,xx,zz,ww,dd,yy,hh,m,'box',flags);
 a(x,z+d-1.8,w,1.8,y,h);a(x,z,1.8,d,y,h);a(x+w-1.8,z,1.8,d,y,h);a(x,z,w,d,y,1.8);a(x,z,w,d,y+h-1.8,1.8);
 for(const yy of shelves)a(x+1.8,z,w-3.6,d-1.8,yy,1.8,'offwhite');
 for(const xx of dividers)a(xx,z,1.8,d-1.8,y+1.8,h-3.6,'offwhite');
}
function color(id){return MAT[id]?.color||id;}
function rgb(hex){let h=hex.replace('#','');if(h.length===3)h=h.split('').map(c=>c+c).join('');return [0,2,4].map(i=>parseInt(h.slice(i,i+2),16));}
function shade(c,f){if(!c?.startsWith('#'))return c;return '#'+rgb(c).map(n=>Math.max(0,Math.min(255,Math.round(n*f))).toString(16).padStart(2,'0')).join('');}
function add(id,room,x,z,w,d,y,h,mat,kind='box',extra={}){const group=(id||room)+'/'+kind;const key=group+'/'+(nodeSequence[group]=(nodeSequence[group]||0)+1);nodes.push({key,id,room,x,z,w,d,y,h,c:color(mat),mat,kind,...extra});}
function slab(id,room,x,z,w,d,y,h,mat,r=0){add(id,room,x,z,w,d,y,h,mat,r?'round':'box',{r});}
function upper(id,room,x,z,w,d,y,h,mat,along='x',doors=3){add(id,room,x,z,w,d,y,h,mat,'box',{upper:true});for(let i=1;i<doors;i++){if(along==='x')add(id,room,x+w*i/doors-.25,z-.25,.5,d+.5,y,h,'#c9c7bb','box',{upper:true});else add(id,room,x-.25,z+d*i/doors-.25,w+.5,.5,y,h,'#c9c7bb','box',{upper:true});}}
function leg(id,room,x,z,y,h){add(id,room,x,z,3,3,y,h,'black');}
function chairDining(x,z,r){const id='diningchairs',room='sala';add(id,room,x,z,42,44,0,85,'head','chair',{rot:r});}
function buildScene(){nodes=[];nodeSequence={};
  // Physical footprint: documentary room dimensions and graphically reconstructed connections.
  const floors=[['quarto',0,100,245,295,'vinyl'],['quarto',245,305,120,90,'vinyl'],['escritorio',255,0,230,295,'vinyl'],['sala',495,185,245,380,'vinyl'],['sala',465,405,30,140,'vinyl'],['circulacao',365,305,130,90,'vinyl'],['cozinha',388,545,352,155,'vinyl'],['lavanderia',255,539,129,161,'ivory'],['banho',255,405,209,124,'greige']];
  for(const [r,x,z,w,d,m]of floors)add(null,r,x,z,w,d,-5,5,m,'floor');
  const H=state.walls?247:32;
  const walls=[['quarto',-10,90,70,10],['quarto',180,90,75,10],['quarto',-10,100,10,295],['quarto',-10,395,265,10],['quarto',245,100,10,195],['escritorio',245,-10,70,10],['escritorio',430,-10,65,10],['escritorio',245,0,10,100],['escritorio',485,-10,10,315],['escritorio',255,295,145,10,['quarto']],['escritorio',475,295,20,10],['sala',495,175,38,10],['sala',672,175,78,10],['sala',740,185,10,430],['cozinha',740,690,10,20],['cozinha',255,700,495,10],['lavanderia',245,539,10,30],['lavanderia',245,675,10,25],['banho',245,405,10,30],['banho',245,475,10,64],['banho',255,529,219,10],['banho',464,395,10,134],['banho',255,395,130,10,['quarto']],['banho',455,395,19,10],['quarto',365,305,10,10],['quarto',365,390,10,5]];
  for(const [r,x,z,w,d,sharedRooms]of walls)add(null,r,x,z,w,d,0,H,'#e4dfd2','wall',{sharedRooms});
  // P01 / F120: continuous bathroom partition, separate bedroom access on its east side.
  // Opening and leaf dimensions remain graphic estimates, not construction measurements.
  if(state.walls)add(null,'quarto',365,315,10,75,205,H-205,'#e4dfd2','wall');
  for(const[r,x,z,w,d]of [['quarto',60,90,120,10],['escritorio',315,-10,115,10],['sala',533,175,139,10],['lavanderia',245,569,10,106],['banho',245,435,10,40]]){add(null,r,x,z,w,d,95,state.walls?110:6,'#aabeb5','glass');add(null,r,x,z,w,d,92,3,'offwhite');}
  // Original doors, graphic envelopes only. Cutaway leaves keep furniture visible.
  for(const [r,x,z,w,d]of [['escritorio',474,220,2,75],['quarto',290,388,75,2],['banho',454,405,2,70],['cozinha',655,698,85,2]])add(null,r,x,z,w,d,0,state.walls?205:5,'#b39c7b','door');
  // Sala: narrow TV wall, current Bonnie, no obsolete detachable chaise.
  const open=state.sofa!=='closed',sd=open?136:110,sx=740-state.sofaGap-sd;
  slab('bonnie','sala',sx,185,sd,180,9,29,'beige',5);
  slab('bonnie','sala',sx+8,195,sd-29,160,37,1,'#665446',3);
  for(let i=0;i<2;i++)add('bonnie','sala',sx+4,199+i*77,sd-32,74,38,13,'beige','round',{r:4,tiltZ:state.sofa==='storage'?-1.05:0,pivot:[740-state.sofaGap-28,38,0]});
  slab('bonnie','sala',740-state.sofaGap-25,189,23,172,36,open?43:64,'head',5);
  for(const zz of[185,351])slab('bonnie','sala',sx+8,zz,sd-8,14,35,31,'beige',3);
  add('panel','sala',495,187.5,2,115,25,165,'offwhite');
  add('racks','sala',497,190,state.rackDepth-2,110,32,3,'wood');add('racks','sala',497,190,25,110,162,3,'wood');
  add('power','sala',497,192,15,20,35,12,'wood');
  // Screen luminous dark face along x, Ambilight is only a muted visual cue.
  add('tv50','sala',504,189.45,8.8,111.1,77,64.9,'black','screenX');
  add('soundbar','sala',505,200,10.5,90,60,7,'black','round',{r:3});
  add('decor','sala',505,193,7,5,60,12,'sage','vase');
  // Jantar: 150/180 x 75, fixed center; base remains an unvalidated graphic envelope.
  add('bench','sala',685,375,55,180,0,40,'wood');slab('bench','sala',685,375,45,180,40,7,'head',3);slab('bench','sala',730,375,10,180,40,50,'head',3);
  const dining=diningClearance();
  add('table','sala',615,dining.start,75,75,72,3,'wood','tableHalf',{r:15,end:'near'});
  add('table','sala',615,dining.end-75,75,75,72,3,'wood','tableHalf',{r:15,end:'far'});
  // The removable leaf is shown in place only when extended; storage in the bench is documented.
  if(state.table==='extended')add('table','sala',615,450,75,30,72,3,'wood','tableLeaf');
  // Visible joint lines; geometry remains nominal, not a tolerance/cutting drawing.
  for(const zz of state.table==='compact'?[465]:[450,480])add('table','sala',615,zz-.07,75,.14,75,.015,'#9c825f');
  slab('table','sala',646.5,459,12,12,2,65.3,'black',6);slab('table','sala',639.5,450,26,30,0,2,'black',13);
  for(const xx of [628,674])add('table','sala',xx,420,3,90,67.3,4.7,'black');
  add('table','sala',631,448,43,34,64.3,3,'black');
  // Keep chair positions fixed: shrinking the top does not certify deeper chair storage.
  if(state.dining==='stored'){chairDining(609,384,Math.PI/2);chairDining(609,473,Math.PI/2);chairDining(631.5,517,-Math.PI);}else{for(let i=0;i<3;i++)chairDining(560,384+i*60,Math.PI/2);}
  // Quarto: more space at wardrobe; no TV and no blue furniture.
  const hx=state.headDepth;
  slab('queen','quarto',hx,120,200,160,0,34,'head',3);slab('queen','quarto',hx,120,200,160,34,26,'offwhite',5);
  slab('queen','quarto',hx+65,121,134,158,60,2,'#c9c1ae',3);
  slab('queen','quarto',hx+5,130,44,62,60,9,'#faf8ee',6);slab('queen','quarto',hx+5,207,44,62,60,9,'#faf8ee',6);
  slab('headboard','quarto',0,120,hx,160,20,95,'head',2);
  cabinet('wardrobe','quarto',0,335,200,60,0,240,'offwhite',[215],[99.1]);
  if(state.inside){
    for(const x of [1.8,162.7])for(const y of [8,34,60,80,95,110])add('wardrobe','quarto',x,337,35.5,53,y,1.8,'wood');
    for(const x of [37.3,73.7,124.5,160.9])add('wardrobe','quarto',x,337,1.8,53,8,102,'offwhite');
    for(const x of [1.8,126.3])add('wardrobe','quarto',x,337,71.9,53,110,1.8,'offwhite');
    for(const x of [1.8,100.9])add('wardrobe','quarto',x,362,97.3,2,205,2,'black');
    for(const x of [39.1,126.3])add('wardrobe','quarto',x,362,33.2,2,103,2,'black');
  }
  add('mirror','quarto',200,340,.5,50,20,180,'#b9d0d3','glass');
  upper('bedcabinet','quarto',0,110,25,180,205,35,'offwhite','z',3);
  add('ledges','quarto',hx+3,120,15,20,69,2,'wood');add('ledges','quarto',hx+3,260,15,20,69,2,'wood');
  // Escritório. Global origin [255,0], same local coordinates as R07.
  slab('desk','escritorio',270,0,200,70,72,3,'wood',1);
  add('drawers','escritorio',270,25,40,45,48,24,'wood');add('drawers','escritorio',270,69.8,40,.4,59.5,.5,'black');
  for(const x of[275,460])leg('desk','escritorio',x,12,0,72);
  // laptop, 2 monitors and cabinet: reserves from R10.
  slab('setup','escritorio',272,30,36,25,75,1.5,'#7c8381',1);add('setup','escritorio',272,29,36,1.5,76,22,'black','screenZ');
  for(const x of[310,374]){add('setup','escritorio',x,19,62,3,93,35,'black','screenZ');add('setup','escritorio',x+30,20,2,9,75,19,'black');}
  add('setup','escritorio',443.25,15,21.5,42.8,75,43.1,'black');add('setup','escritorio',443,18,.4,34,80,31,'#526b70','glass');
  slab('setup','escritorio',368,48,47,15,75,1,'#555b59',1);
  const guest=state.office==='guest',bedDepth=guest?182:90;
  const sofaPose={rootX:guest?327:257,rootZ:guest?292:222,yaw:guest?0:-Math.PI/2};
  const sofaPart=(x,z,w,d,y,h,mat,extra={})=>add('daiane','escritorio',sofaPose.rootX+x,sofaPose.rootZ+z,w,d,y,h,mat,'round',{r:3,...sofaPose,...extra});
  sofaPart(-70,-bedDepth,140,bedDepth,8,28,'grey');
  sofaPart(-66,-bedDepth+3,132,bedDepth-22,36,11,'grey');
  sofaPart(-68,-19,136,19,35,guest?12:47,'#969da0');
  for(const x of [-70,56])sofaPart(x,-bedDepth+1,14,bedDepth-19,35,guest?12:26,'grey');
  for(const x of [-59,3])sofaPart(x,-46,56,31,47,7,'offwhite',{opacity:guest?1:0});
  add('officechair','escritorio',guest?405:367.75,guest?75:80,74.5,73,0,120,'black','officechair');
  upper('officecab','escritorio',255,90,35,200,192,55,'offwhite','z',5);
  add('officeshelf','escritorio',450,105,35,110,192,3,'wood','box',{upper:true});
  add('tv43','escritorio',473,128,5,97,82,56,'black','screenX');
  if(state.console==='sala'){add('ps5','sala',507,226.1,21.6,35.8,35,8,'offwhite','console');}else{add('ps5','escritorio',453.4,115,21.6,35.8,195,8,'offwhite','console',{upper:true});}
  // Cozinha: composição funcional aprovada; cotas continuam de estudo.
  // Open oven niche: a solid cabinet here hides the appliance with depth rendering.
  for(const x of [388,445.5])add('kitchenbase','cozinha',x,639,7.5,61,8,81,'wood');
  add('kitchenbase','cozinha',395.5,639,50,61,8,16,'wood');
  add('kitchenbase','cozinha',395.5,639,50,61,59,30,'wood');
  add('kitchenbase','cozinha',395.5,698.2,50,1.8,24,35,'wood');
  cabinet('sinkstorage','cozinha',453,639,60,61,22,67,'wood',[48.2],[]);
  cabinet('kitchenbase','cozinha',513,639,61.9,61,18,71,'wood',[44.2,62.2],[]);
  slab('kitchenbase','cozinha',388,639,186.9,61,89,3,'stone',1);
  for(const x of[453,513])add('kitchenbase','cozinha',x,638.9,.6,1,18,71,'#9c825f');
  add('sinkstorage','cozinha',482.7,638.7,.6,1,18,71,'#9c825f');
  for(const y of[44.2,62.2])add('kitchenbase','cozinha',513,638.7,61.9,1,y,.6,'#9c825f');
  add('lowdrawer','cozinha',453,647,121.9,40.6,4.5,10,'wood');
  add('oven','cozinha',395.5,641,50,55,24,35,'black','oven');add('cooktop','cozinha',392,646,56,46,92,1.5,'black','cooktop');
  add('sink','cozinha',461.5,650,43,37,90,2.6,'#959d97','sink');add('sink','cozinha',505,678,2,2,92,43,'black');add('sink','cozinha',489,677,17,2,133,2,'black');
  // Fridge body with the 10 cm rear clearance, not the old placement.
  add('fridge','cozinha',584.9,615.25,60.1,74.75,0,186.6,'inox','fridge');
  cabinet('kitchenupper','cozinha',388,665,65,35,197.6,57.4,'petrol',[],[419.6],{upper:true});
  cabinet('kitchenupper','cozinha',453,665,52.2,35,155,100,'petrol',[173,194,221.6],[],{upper:true});
  cabinet('kitchenupper','cozinha',505.2,665,69.7,35,194,61,'petrol',[221.6],[],{upper:true});
  cabinet('kitchenupper','cozinha',574.9,665,80.1,35,198.4,56.6,'petrol',[],[614.05],{upper:true});
  add('microwave','cozinha',516.5,657,46.1,35.2,155,29,'black','microwave',{upper:true});
  add('hood','cozinha',390.5,666,60,32,158,7,'#afb4b0','box',{upper:true});
  add('filter','cozinha',552,653,16,42,92,35,'black','box');
  add('trash','cozinha',474,508,34,21,0,45,'inox','round',{r:3});
  add('trash','cozinha',474,508,34,21,45,2,'black','round',{r:3});
  add('trash','cozinha',505,514,5,9,1,2,'black');
  add('recycling','lavanderia',257,541,29,29,0,42,'inox','round',{r:14.5});
  add('recycling','lavanderia',257,541,29,29,42,1.7,'black','round',{r:14.5});
  add('recycling','lavanderia',267,568,9,5,1,2,'black');
  add('dishrack','cozinha',514,641,27.8,19.9,92,2,'black','round',{r:2});
  add('dishrack','cozinha',514,641,27.8,2,94,10.6,'black');
  // Lavanderia: state is intention only, not an engineered mechanism.
  add('washer','lavanderia',320,628,60,62,0,85.5,'inox','washer');slab('laundrybase','lavanderia',255,625,129,75,89,3,'stone',1);
  cabinet('laundrybase','lavanderia',255,642,59,58,8,81,'wood',[],[]);add('laundrybase','lavanderia',263,649,42,39,90,2,'#aaa99b','sink');
  if(state.dry==='stored')add('airfryer','lavanderia',349,651,26.4,36,92,29.5,'black','round',{r:5});
  else add('airfryer','cozinha',520,651,26.4,36,92,29.5,'black','round',{r:5});
  upper('laundryupper','lavanderia',302,665,86,35,165,58,'wood','x',2);
  add('heater','lavanderia',262,675,35,15.7,157,53,'offwhite');add('heater','lavanderia',276,679,8,8,210,35,'#afb3ae');
  const dy=state.dry==='stored'?231:state.dry==='high'?204:145,dz=state.dry==='stored'?639:564;
  add('drying','lavanderia',270,dz,100,50,dy,3,'wood','drying',{upper:true});
  add('laundryupper','lavanderia',255,636,133,3,223,17,'wood','box',{upper:true});
  if(state.dry!=='stored')for(const x of[281,303,327,349])add('drying','lavanderia',x,dz+12,13,2,dy-75,74,'#dddccf','box',{upper:true});
  // Bathroom decisions 18/09; dimensional envelopes remain a study.
  add('shower','banho',255,405,80,124,0,2,'greige','floor');
  add('bathshaft','banho',255,499,80,30,2,18,'greige');
  add('shower','banho',255,527,80,2,0,225,'sage','box',{upper:true});
  add('shower','banho',334,405,1,124,0,210,'#9fb2aa','glass');
  for(const zz of [405,528])add('shower','banho',333.5,zz,2,1,0,210,'black');
  add('shower','banho',333.5,405,2,124,209,1,'black');
  add('shower','banho',290,485,2,42,207,2,'black');add('shower','banho',284.4,478,13.2,13.2,205,2,'black','round',{r:6.6});
  add('shower','banho',305,524,3,3,120,15,'black');
  for(let i=0;i<16;i++){let a=i/15*Math.PI;add('shower','banho',301+12*Math.cos(a),521,1,1,108-23*Math.sin(a),2,'black');}
  add('bath shelf','banho',270,517,28,10,115,2,'stone');
  cabinet('bathvanity','banho',404,487,60,42,20,54.5,'bathbeige',[],[]);
  add('bathvanity','banho',404,487,1.8,42,20,54.5,'lightwood');add('bathvanity','banho',462.2,487,1.8,42,20,54.5,'lightwood');
  slab('bathvanity','banho',404,484,60,45,74.5,2,'stone');
  add('basin','banho',414,489,40,30,76.5,13.5,'offwhite','sink');
  add('bath tap','banho',432,522,4,4,76.5,30,'black');add('bath tap','banho',432,507,4,18,104.5,2,'black');
  cabinet('bathmirror','banho',404,514,60,15,115,75,'lightwood',[],[],{upper:true});
  if(!state.inside)add('bathmirror','banho',404,513.5,60,.6,115,75,'#b8cdcf','box',{upper:true});
  for(const x of [405,461])add('bathlight','banho',x,513,2,.7,115,75,'#fff4cf','box',{upper:true});
  add('toilet','banho',350.75,470,37.5,59,0,80,'offwhite','toilet');
  add('hygiene','banho',400,524,2,2,60,13,'black');
  for(let i=0;i<14;i++){let a=i/13*Math.PI;add('hygiene','banho',396+6*Math.cos(a),524,1,1,53-17*Math.sin(a),2,'black');}
  return nodes;
}

// Mesh generation: actual 3D coordinates; orthographic camera with orbit and elevations.
function ring(w,d,r=0,end=null){r=Math.min(r,w/2,d/2);if(!r)return [[0,0],[w,0],[w,d],[0,d]];let a=[];for(const[cx,cz,start,side]of [[w-r,r,-Math.PI/2,'near'],[w-r,d-r,0,'far'],[r,d-r,Math.PI/2,'far'],[r,r,Math.PI,'near']]){if(end&&side!==end){a.push([cx>w/2?w:0,side==='near'?0:d]);continue;}for(let i=0;i<=5;i++){const q=start+i*Math.PI/10;a.push([cx+r*Math.cos(q),cz+r*Math.sin(q)]);}}return a;}
function mesh(n){const out=[];
  function extrude(x,z,w,d,y,h,c,r=0,alpha=1,end=null){let p=ring(w,d,r,end),bottom=p.map(([a,b])=>[x+a,y,z+b]),top=p.map(([a,b])=>[x+a,y+h,z+b]);out.push({p:top,c,alpha,normal:[0,1,0]},{p:bottom,c,alpha,normal:[0,-1,0]});for(let i=0;i<p.length;i++){let j=(i+1)%p.length,dx=p[j][0]-p[i][0],dz=p[j][1]-p[i][1],l=Math.hypot(dx,dz)||1;out.push({p:[bottom[i],bottom[j],top[j],top[i]],c,alpha,normal:[dz/l,0,-dx/l]});}}
  const {x,z,w,d,y,h,c,kind}=n;
  if(kind==='chair'){
    // Local chair points into +z. rotation aligns compact body with dining edges.
    const local=[];const old=out;
    extrude(0,0,42,6,43,42,shade(c,.91),2);extrude(0,6,42,38,43,5,c,3);
    for(const[xx,zz]of [[3,7],[36,7],[3,37],[36,37]])extrude(xx,zz,3,3,0,43,'#45453f');
    let r=n.rot||0,seen=new Set();for(const f of out)for(const p of f.p){if(seen.has(p))continue;seen.add(p);let xx=p[0]-21,zz=p[2]-22;p[0]=x+21+Math.abs(Math.sin(r))+xx*Math.cos(r)+zz*Math.sin(r);p[2]=z+22-Math.abs(Math.sin(r))-xx*Math.sin(r)+zz*Math.cos(r);}
  }else if(kind==='officechair'){
    extrude(x+7,z+9,w-14,d-24,43,7,'#636d6b',9);extrude(x+9,z+d-18,w-18,9,49,h-49,'#3b4d4c',4);extrude(x+w/2-3,z+d/2-3,6,6,8,35,'#555b56');extrude(x+3,z+d/2,w-6,4,7,3,'#333b39');extrude(x+w/2,z+3,4,d-6,7,3,'#333b39');
    for(const xx of[x+1,x+w-6]){extrude(xx,z+15,5,30,65,4,'#303b37');extrude(xx,z+25,4,4,49,16,'#515c57');}
  }else if(kind==='screenX'||kind==='screenZ'){
    extrude(x,z,w,d,y,h,c,1);if(kind==='screenX'){extrude(x+w+.15,z+2,.2,d-4,y+2,h-4,'#527c7b');}else extrude(x+2,z+d+.15,w-4,.2,y+2,h-4,'#527c7b');
  }else if(kind==='console'){
    extrude(x,z,w,d,y+1,h-2,'#222e32',2);extrude(x,z,w,d,y,.8,'#f2f0e8',2);extrude(x,z,w,d,y+h-.8,.8,'#f2f0e8',2);
  }else if(kind==='washer'){
    extrude(x,z,w,d,y,h,c,1);extrude(x+11,z-.6,38,1,y+22,38,'#373f43',18);extrude(x+16,z-1,28,1,y+27,28,'#899a9d',13);extrude(x+5,z-.7,w-10,1,y+71,6,'#d2d4cf');
  }else if(kind==='fridge'){
    extrude(x,z,w,d,y,h,c,1.5);extrude(x,z-.5,w,.5,y+70,.7,'#b8bdb9');extrude(x+4,z-1.5,3,1.5,y+83,28,'#aeb7b2');extrude(x+4,z-1.5,3,1.5,y+33,25,'#aeb7b2');
  }else if(kind==='sink'){
    extrude(x,z,w,d,y,h,c,5);extrude(x+3,z+3,w-6,d-6,y+h,.1,shade(c,.75),4);
  }else if(kind==='cooktop'){
    extrude(x,z,w,d,y,h,c,2);for(const xx of[x+6,x+w-20])for(const zz of[z+5,z+d-18])extrude(xx,zz,13,13,y+h,.5,'#7b8078',6);
  }else if(kind==='oven'||kind==='microwave'){
    extrude(x,z,w,d,y,h,c,1);extrude(x+4,z-.5,w-8,.7,y+4,h-10,'#405357',1);extrude(x+4,z-2,w-8,2,y+h-5,2,'#9faaa7');
  }else if(kind==='drying'){
    for(const xx of[x,x+w-2])extrude(xx,z,2,d,y,3,c);for(let zz=z;zz<=z+d;zz+=10)extrude(x,zz,w,1,y,1,'#737f74');
  }else if(kind==='toilet'){
    extrude(x,z+d-18,w,18,y+38,h-38,c,3);extrude(x+5,z+6,w-10,d-20,y,36,c,9);extrude(x,z,w,d-12,y+36,7,c,14);extrude(x+6,z+6,w-12,d-26,y+43,.5,'#b4b8ac',9);
  }else if(kind==='vase'){extrude(x,z,w,d,y,h,c,3);}
  else extrude(x,z,w,d,y,h,c,kind==='round'||kind==='tableHalf'?n.r:0,kind==='glass'?.32:1,n.end||null);
  if(n.yaw){const r=n.yaw,seen=new Set();for(const f of out){for(const p of f.p){if(seen.has(p))continue;seen.add(p);const a=p[0]-n.rootX,b=p[2]-n.rootZ;p[0]=n.rootX+a*Math.cos(r)+b*Math.sin(r);p[2]=n.rootZ-a*Math.sin(r)+b*Math.cos(r);}const[a,b,c]=f.normal;f.normal=[a*Math.cos(r)+c*Math.sin(r),b,-a*Math.sin(r)+c*Math.cos(r)];}}
  if(n.tiltZ){const [px,py]=n.pivot,seen=new Set();for(const f of out){for(const p of f.p){if(seen.has(p))continue;seen.add(p);const a=p[0]-px,b=p[1]-py;p[0]=px+a*Math.cos(n.tiltZ)-b*Math.sin(n.tiltZ);p[1]=py+a*Math.sin(n.tiltZ)+b*Math.cos(n.tiltZ);}const [a,b,c]=f.normal;f.normal=[a*Math.cos(n.tiltZ)-b*Math.sin(n.tiltZ),a*Math.sin(n.tiltZ)+b*Math.cos(n.tiltZ),c];}}
  if(kind==='chair'){const r=n.rot||0;for(const f of out){const [a,b,c]=f.normal;f.normal=[a*Math.cos(r)+c*Math.sin(r),b,-a*Math.sin(r)+c*Math.cos(r)];}}
  return out.map(f=>({...f,alpha:f.alpha*(n.opacity??1),id:n.id,room:n.room,node:n}));
}
function camera(st,w,h,bounds){let [xmin,zmin,xmax,zmax]=bounds;let a=st.angle,t=st.tilt;
  if(st.view==='top')t=Math.PI/2,a=0;
  if(st.view==='side'){t=0;a={east:-Math.PI/2,west:Math.PI/2,south:0,north:Math.PI}[st.side];}
  const raw=p=>{let X=p[0]-(xmin+xmax)/2,Z=p[2]-(zmin+zmax)/2,Y=p[1],u=X*Math.cos(a)+Z*Math.sin(a),v=-X*Math.sin(a)+Z*Math.cos(a);return[u,v*Math.sin(t)-Y*Math.cos(t),v*Math.cos(t)+Y*Math.sin(t)];};
  let q=[];for(const x of[xmin,xmax])for(const z of[zmin,zmax])for(const y of[0,st.view==='top'?0:(st.ymax||247)])q.push(raw([x,y,z]));
  let minx=Math.min(...q.map(p=>p[0])),maxx=Math.max(...q.map(p=>p[0])),miny=Math.min(...q.map(p=>p[1])),maxy=Math.max(...q.map(p=>p[1]));
  let pad=w<500?28:45,spaceTop=st.mini?12:78,spaceBottom=st.mini?12:52;
  const scale=Math.min((w-pad*2)/(maxx-minx||1),(h-spaceTop-spaceBottom)/(maxy-miny||1))*st.zoom;
  const cx=w/2-(minx+maxx)/2*scale+st.pan[0],cy=spaceTop+(h-spaceTop-spaceBottom)/2-(miny+maxy)/2*scale+st.pan[1];
  return{project:p=>{const q=raw(p);return[cx+q[0]*scale,cy+q[1]*scale,q[2]];},raw,scale};
}
function visible(n,st){return(st.room==='all'||n.room===st.room||n.sharedRooms?.includes(st.room))&&(!n.upper||st.upper)&&(st.view!=='side'||n.kind!=='wall'||st.walls);}
// Only upward floor faces receive a finish; furniture using the same palette stays unchanged.
function floorStyle(f){return f.node?.kind==='floor'&&f.normal[1]>.99?({vinyl:1,greige:2,ivory:3}[f.node.mat]||0):0;}
function drawFloorFallback(ctx,f,project){
  const style=floorStyle(f);if(!style)return;
  const xs=f.p.map(p=>p[0]),zs=f.p.map(p=>p[2]),xmin=Math.min(...xs),xmax=Math.max(...xs),zmin=Math.min(...zs),zmax=Math.max(...zs),y=f.p[0][1];
  const width=style===1?20.845:90,length=style===1?123.03:90;
  const hash=(x,z)=>{const n=Math.sin(x*127.1+z*311.7)*43758.5453;return n-Math.floor(n);};
  const path=points=>{ctx.beginPath();points.forEach((p,i)=>{const q=project([p[0],y,p[1]]);if(i)ctx.lineTo(q[0],q[1]);else ctx.moveTo(q[0],q[1]);});};
  ctx.save();ctx.clip();
  for(let col=Math.floor(xmin/width);col*width<xmax;col++){
    const offset=style===1?((col%3+3)%3)*41.01:0;
    for(let row=Math.floor((zmin+offset)/length);row*length-offset<zmax;row++){
      const x=col*width,z=row*length-offset,seed=hash(col,row);
      path([[x,z],[x+width,z],[x+width,z+length],[x,z+length]]);ctx.closePath();
      ctx.fillStyle=shade(f.c,1.04*(.975+(seed-.5)*(style===1?.065:.025)));ctx.fill();
      ctx.strokeStyle=shade(f.c,.91);ctx.lineWidth=.35;ctx.stroke();
      if(style===1){
        ctx.strokeStyle=shade(f.c,.99);ctx.lineWidth=.45;
        for(let i=1;i<=7;i++){
          const points=[];for(let j=0;j<=12;j++)points.push([x+width*i/8+Math.sin(j*.6+seed*12+i)*.35,z+j*length/12]);
          path(points);ctx.stroke();
        }
      }
    }
  }
  ctx.restore();
  // Restore the face outline for selection after the decorative paths.
  ctx.beginPath();f.points.forEach((p,i)=>{if(i)ctx.lineTo(p[0],p[1]);else ctx.moveTo(p[0],p[1]);});ctx.closePath();
}
function render(canvas,st=state,mini=false,selectionOnly=null){if(!canvas)return;let rect=canvas.getBoundingClientRect(),w=rect.width||canvas.width||800,h=rect.height||canvas.height||500;const ratio=Math.min(window.devicePixelRatio||1,2);canvas.width=Math.round(w*ratio);canvas.height=Math.round(h*ratio);const ctx=canvas.getContext('2d');ctx.scale(ratio,ratio);ctx.clearRect(0,0,w,h);ctx.fillStyle='#eeece3';ctx.fillRect(0,0,w,h);
  let room=PROJECT.rooms.find(r=>r.id===st.room)||PROJECT.rooms[0];let list=nodes.filter(n=>visible(n,st));let bounds=room.bounds;
  if(st.room!=='all')list=list.map(n=>{if(n.id)return n;const x=Math.max(n.x,bounds[0]),z=Math.max(n.z,bounds[1]),w=Math.min(n.x+n.w,bounds[2])-x,d=Math.min(n.z+n.d,bounds[3])-z;return {...n,x,z,w,d};}).filter(n=>n.w>0&&n.d>0);
  if(st.view==='side'&&st.sideCut&&!selectionOnly){const midx=(bounds[0]+bounds[2])/2,midz=(bounds[1]+bounds[3])/2;list=list.filter(n=>!n.id||(st.side==='east'?n.x+n.w>=midx:st.side==='west'?n.x<=midx:st.side==='south'?n.z+n.d>=midz:n.z<=midz));}
  if(selectionOnly){list=nodes.filter(n=>n.id===selectionOnly&&(n.opacity??1)>.01);if(!list.length)return;const vertices=list.flatMap(n=>mesh(n).flatMap(f=>f.p));bounds=[Math.min(...vertices.map(p=>p[0]))-8,Math.min(...vertices.map(p=>p[2]))-8,Math.max(...vertices.map(p=>p[0]))+8,Math.max(...vertices.map(p=>p[2]))+8];const base=Math.min(...list.map(n=>n.y));list=list.map(n=>({...n,y:n.y-base,pivot:n.pivot?[n.pivot[0],n.pivot[1]-base,n.pivot[2]]:undefined}));}
  const view={...st,mini,...(selectionOnly?{ymax:Math.max(...list.map(n=>n.y+n.h))}: {})},cam=camera(view,w,h,bounds),project=cam.project;let fs=[];
  for(const n of list){for(const f of mesh(n)){let p=f.p.map(project),depth=p.reduce((s,p)=>s+p[2],0)/p.length;fs.push({...f,points:p,depth});}}
  fs.sort((a,b)=>(a.node.kind==='floor'?0:1)-(b.node.kind==='floor'?0:1)||a.depth-b.depth);
  const main=canvas.id==='scene';if(main){hitFaces=[];lastProject=cam;}
  const depthOK=renderDepth(ctx,fs,w,h,ratio,main?st.selected:null);
  if(main){hitFaces=fs;canvas.dataset.renderer=depthOK?'depth':'simplified';}
  if(!depthOK)for(const f of fs){const p=f.points;ctx.beginPath();ctx.moveTo(p[0][0],p[0][1]);for(let i=1;i<p.length;i++)ctx.lineTo(p[i][0],p[i][1]);ctx.closePath();ctx.globalAlpha=f.alpha;let lighting=f.normal[1]?1.04:.80+.11*f.normal[0]-.07*f.normal[2];ctx.fillStyle=shade(f.c,lighting);ctx.fill();
    if(floorStyle(f))drawFloorFallback(ctx,f,project);
    else{ctx.strokeStyle=shade(f.c,.72);ctx.lineWidth=mini?.25:.4;ctx.stroke();}ctx.globalAlpha=1;
    if(main&&st.selected&&st.selected===f.id){ctx.strokeStyle='#c17b37';ctx.lineWidth=1.6;ctx.stroke();}
  }
  if(!mini&&!selectionOnly){drawAnnotations(ctx,project,cam,w,h,st);}
  if(main)canvas.dataset.rendered='true';
}
function label(ctx,x,y,text,fill='#203d3b',size=11,bg=true){ctx.font=`600 ${size}px Segoe UI,Arial`;let m=ctx.measureText(text);if(bg){ctx.fillStyle='#fffff3ed';ctx.fillRect(x-m.width/2-5,y-size-3,m.width+10,size+8);}ctx.fillStyle=fill;ctx.textAlign='center';ctx.fillText(text,x,y);}
function dimension(ctx,project,a,b,text){let p=project(a),q=project(b),dx=q[0]-p[0],dy=q[1]-p[1],len=Math.hypot(dx,dy);if(len<12)return;let nx=-dy/len*4,ny=dx/len*4;ctx.strokeStyle='#406952';ctx.lineWidth=1.3;ctx.beginPath();ctx.moveTo(p[0],p[1]);ctx.lineTo(q[0],q[1]);for(const r of[p,q]){ctx.moveTo(r[0]-nx,r[1]-ny);ctx.lineTo(r[0]+nx,r[1]+ny);}ctx.stroke();label(ctx,(p[0]+q[0])/2,(p[1]+q[1])/2-6,text,'#295e44',11);}
function drawAnnotations(ctx,pr,cam,w,h,st){
  if(st.room==='all'&&st.view==='top'){for(const[r,x,z]of [['quarto',125,305],['escritorio',388,175],['sala',565,330],['cozinha',688,570],['banho',379,445],['lavanderia',320,568]]){const p=pr([x,2,z]);label(ctx,p[0],p[1],PROJECT.rooms.find(q=>q.id===r).name.toUpperCase(),'#384d46',w<500?8:10);}}
  if(st.view==='top'){
    ctx.strokeStyle='#9b7652';ctx.lineWidth=1;ctx.setLineDash([3,3]);for(const [r,x,z,radius,start,end]of [['quarto',365,390,75,Math.PI,Math.PI*1.5],['escritorio',475,295,75,Math.PI,Math.PI*1.5],['cozinha',740,700,85,Math.PI,Math.PI*1.5],['banho',455,405,70,Math.PI/2,Math.PI]]){if(st.room!=='all'&&st.room!==r)continue;ctx.beginPath();for(let i=0;i<=32;i++){let a=start+(end-start)*i/32,p=pr([x+radius*Math.cos(a),2,z+radius*Math.sin(a)]);if(i)ctx.lineTo(p[0],p[1]);else ctx.moveTo(p[0],p[1]);}ctx.stroke();}ctx.setLineDash([]);
  }
  if(st.measures&&st.view!=='side'){
    if(st.room==='sala'||st.room==='all'){const depth=st.sofa==='closed'?110:136,gap=245-depth-st.rackDepth-st.sofaGap,dc=diningClearance(st);dimension(ctx,pr,[495+st.rackDepth,2,268],[740-depth-st.sofaGap,2,268],gap+' cm*');if(st.room==='sala')dimension(ctx,pr,[705,2,dc.start],[705,2,dc.end],dc.length+' cm · mesa');}
    if(st.room==='quarto'){dimension(ctx,pr,[150,2,280],[150,2,335],'55 cm*');dimension(ctx,pr,[200+st.headDepth,2,215],[245,2,215],(45-st.headDepth)+' cm*');dimension(ctx,pr,[100,2,100],[100,2,120],'20 cm*');}
    if(st.room==='escritorio'){if(st.office==='guest'){dimension(ctx,pr,[355,2,70],[355,2,110],'40 cm*');dimension(ctx,pr,[397,2,200],[485,2,200],'88 cm*');}else dimension(ctx,pr,[337,2,70],[337,2,152],'82 cm*');}
    if(st.room==='cozinha'){dimension(ctx,pr,[655,2,580],[740,2,580],'85 cm*');}
    if(st.room==='all'||st.room==='cozinha'){const dc=diningClearance(st);dimension(ctx,pr,[625,76,dc.end],[625,76,615.25],cm(dc.tableToFridge)+' cm · tampo/IB6*');}
  }
  if(st.room!=='all'&&st.view==='side'&&st.measures){let bounds=PROJECT.rooms.find(r=>r.id===st.room).bounds;const a=[bounds[0]+7,0,bounds[1]+7],b=[...a];b[1]=st.room==='escritorio'?195:st.room==='quarto'?205:60;dimension(ctx,pr,a,b,b[1]+' cm*');}
  // Physical scale independent of camera rotation in top view.
  if(st.view==='top'){let width=100*cam.scale;let x=15,y=h-17;ctx.strokeStyle='#647062';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(x,y-5);ctx.lineTo(x,y);ctx.lineTo(x+width,y);ctx.lineTo(x+width,y-5);ctx.stroke();ctx.fillStyle='#566556';ctx.font='9px Segoe UI';ctx.textAlign='left';ctx.fillText('0',x,y-8);ctx.fillText('1 m',x+width-14,y-8);}
}

function chosen(o){return /Aprovado|aprovada|Existente|Entrega/.test(o.choice);}
function needsCheck(o){return !/^Projeto aprovado$/.test(o.measure);}
function activeRoom(o){if(o.id==='ps5')return state.console;if(o.id==='airfryer')return state.dry==='stored'?'lavanderia':'cozinha';return o.room;}
function roomItems(room=state.room){return ITEMS.filter(o=>room==='all'||activeRoom(o)===room);}
function selectItem(id,open=true){let it=ITEMS.find(o=>o.id===id);if(!it)return;state.selected=id;
  $('selectedInfo').innerHTML=`<h2>${esc(it.name)}</h2><span class="badge ${chosen(it)?'':'study'}">${esc(it.choice)}</span><span class="badge ${needsCheck(it)?'study':''}">${esc(it.measure)}</span><canvas id="itemPreview" class="item-preview" aria-label="Volume ilustrativo do móvel selecionado"></canvas><div class="dimensions">${esc(it.dimensions)}</div><dl><dt>Material / cor</dt><dd>${esc(MAT[it.material]?.name||it.material)}</dd>${it.budget?'<dt>Orçamento registrado</dt><dd>'+esc(it.budget)+'</dd>':''}<dt>Conferir antes de executar</dt><dd>${esc(it.notes)}</dd></dl><h3>Origem da decisão</h3><p>${esc(it.source)}</p>`;
  if(id==='wardrobe')$('selectedInfo').insertAdjacentHTML('beforeend',`<details class="ward-detail"><summary>Organização interna R02 aprovada</summary><a href="${WARDROBE_IMAGE}" target="_blank" rel="noopener"><img src="${WARDROBE_IMAGE}" alt="Desenho cotado do guarda-roupa R02, dois lados iguais com cabides, quatro gavetas e dez pares de tênis" style="width:100%;height:auto"></a><p>Toque no desenho para ampliar. As medidas reais e ferragens continuam a conferir.</p></details>`);
  if(INTERNALS[id]){$('selectedInfo').insertAdjacentHTML('beforeend','<button id="itemStorage" class="storage-link">Ver organização interna →</button>');$('itemStorage').onclick=()=>openStorage(id);}
  if(open)$('inspector').classList.add('open');drawLists();requestRender();setTimeout(()=>render($('itemPreview'),{...state,room:'all',view:'iso',angle:-.7,tilt:.7,zoom:1,pan:[0,0],upper:true,selected:null},true,id),0);
}
function drawLists(){let list=roomItems();const markup=list.map(o=>`<button data-item="${o.id}" class="${state.selected===o.id?'active':''}"><span class="color-square" style="background:${color(o.material)}"></span><span>${esc(o.name)}<br><span class="source-label">${esc(o.choice)}</span></span></button>`).join('');$('objectList').innerHTML=markup;$('inlineItems').innerHTML=markup;for(const parent of[$('objectList'),$('inlineItems')])parent.querySelectorAll('[data-item]').forEach(b=>b.onclick=()=>selectItem(b.dataset.item));}
function setRoom(id){state.room=id;state.zoom=1;state.pan=[0,0];state.angle=({quarto:-2.4,cozinha:2.8,lavanderia:2.5,banho:2.8})[id]??-.62;let room=PROJECT.rooms.find(r=>r.id===id);$('roomHeading').textContent=room.name;$('roomSubtitle').textContent=room.sub.toUpperCase();$('roomNote').textContent=ROOM_NOTES[id];document.querySelectorAll('[data-room]').forEach(b=>b.classList.toggle('active',b.dataset.room===id));if(state.selected&&!roomItems().some(o=>o.id===state.selected))state.selected=null;drawLists();if(!state.selected){$('selectedInfo').innerHTML=`<h2>${esc(room.name)}</h2><p>${esc(ROOM_NOTES[id])}</p><p>Selecione um móvel no desenho ou na lista para consultar medidas e pendências.</p>`;}updateMetrics();requestRender();}
function setView(v){state.view=v;state.zoom=1;state.pan=[0,0];document.querySelectorAll('[data-view]').forEach(b=>{b.classList.toggle('active',b.dataset.view===v);b.setAttribute('aria-pressed',b.dataset.view===v);});$('sideLabel').hidden=v!=='side';$('sideCutLabel').hidden=v!=='side';$('gestureHint').textContent=v==='iso'?'Arraste para girar · pinça ou roda para aproximar':'Arraste para deslocar · pinça ou roda para aproximar';requestRender();}
function updateMetrics(){let list=[],pass=245-(state.sofa==='closed'?110:136)-state.sofaGap-state.rackDepth;const metric=(value,title,note,warn=false)=>({value,title,note,warn});
  const dc=diningClearance(),diningMetrics=[metric(cm(dc.tableToFridge)+' cm*','Tampo → frente da IB6','60,25 → 75,25 cm; ganho bruto de 15 cm',true),metric(state.dining==='stored'?cm(dc.headChairToFridge)+' cm*':'Sem cadeira na ponta','Cabeceira → frente da IB6',state.dining==='stored'?'Guarda 2+1: faixa não aumenta ao recolher':'Cadeiras na lateral; seis lugares só com mesa aberta',true),metric('85 cm*','Largura da entrada','Reserva transversal; não muda com a mesa',true)];
  if(['all','sala'].includes(state.room)){list=[metric(pass+' cm','Frente do sofá','Estimativa; '+(state.sofa==='closed'?'fechado':'aberto'),pass<75),metric(state.dining==='stored'?'114 cm*':'65 cm*','Lateral do jantar',state.dining==='stored'?'Gabarito; encaixe real das cadeiras pendente':'Cadeira ocupada 55 cm; largura da mesa igual',true),...diningMetrics];}
  else if(state.room==='quarto')list=[metric('55 cm*','Frente do armário','Cama de reserva 160 cm',true),metric((45-state.headDepth)+' cm*','Aos pés da cama','Reserva200 + cabeceira'+state.headDepth,true),metric('20 cm*','Lado da janela','Faixa estreita aceita',true)];
  else if(state.room==='escritorio')list=state.office==='guest'?[metric('40 cm*','Cama → bancada','Sem usuário na estação',true),metric('88 cm*','Lateral da cama','Brutos, fora da cadeira',true),metric('3 cm*','Porta → cama','Margem gráfica crítica',true)]:[metric('82 cm*','Bancada → sofá','Antes da cadeira ocupada',true),metric('195 cm','Topo prateleira','Altura aprovada'),metric('200 × 70','Bancada · cm','Largura ainda proposta',true)];
  else if(state.room==='cozinha')list=[...diningMetrics,metric('61,9 cm*','Filtro + preparo','Faixa compartilhada',true)];
  else if(state.room==='lavanderia')list=[metric('100 × 50','Grelha · cm','Escolhida'),metric('72 cm*','Reserva VC4 fechada','Corpo +10cm atrás'),metric(state.dry==='stored'?'Aparelhos aqui':'Aparelhos na cozinha','Uso da bancada','Sem operar sob roupas',true),metric('Pendente','Recolhimento varal','Conflito com E21',true)];
  else list=[metric('209 × 124','Banheiro · cm','Cotas de planta'),metric('65 cm*','Frente do VIP','Nominal; conferir instalação',true),metric('60 × 45*','Bancada · cm','Borda da cuba a 90 cm no ensaio',true)];
  $('metrics').innerHTML=list.map(m=>`<div class="metric ${m.warn?'warning':''}"><b>${m.value}</b><span>${m.title}</span><small>${m.note}</small></div>`).join('');
  $('gapValue').textContent=state.sofaGap+' cm';$('rackValue').textContent=state.rackDepth+' cm';$('headValue').textContent=state.headDepth+' cm';
}
function requestRender(){if(renderQueued)return;renderQueued=true;requestAnimationFrame(now=>{renderQueued=false;const moving=!!motion;buildScene();sampleMotion(now);if($('model').classList.contains('active'))render($('scene'));if(moving&&!motion&&state.selected)render($('itemPreview'),{...state,view:'iso',angle:-.7,tilt:.7,zoom:1,pan:[0,0],upper:true},true,state.selected);if(motion)requestRender();});}
function toast(s){$('toast').textContent=s;$('toast').style.opacity=1;clearTimeout(toast.timer);toast.timer=setTimeout(()=>$('toast').style.opacity=0,3000);}
function tab(id){document.querySelectorAll('.tabpage').forEach(e=>e.classList.toggle('active',e.id===id));document.querySelectorAll('[data-tab]').forEach(e=>{e.classList.toggle('active',e.dataset.tab===id);e.setAttribute('aria-pressed',e.dataset.tab===id);});$('inspector').classList.remove('open');if(id==='mood')renderMood();if(id==='decisions')renderDecisions();if(id==='model')requestRender();window.scrollTo({top:0,behavior:'instant'});}
function materialStyle(m){return`background-color:${m.color}`;}
function storageDiagram(id){
 const kind=INTERNALS[id].diagram;
 if(kind==='wardrobe')return `<img class="storage-plan" src="${WARDROBE_IMAGE}" alt="Interior aprovado R02 do guarda-roupa, com dois lados iguais, quatro gavetas e espaços para cabides e tênis">`;
 if(kind==='kitchen'){
  const modules=[['D','Depurador',65,197.6,[],true],['C','Pia',52.2,155,[174.8,195.8,223.4],false],['B','Micro-ondas',69.7,194,[223.4],false],['A','Geladeira',80.1,198.4,[],true]];
  return `<div class="storage-schematic" role="img" aria-label="Aéreos vistos de frente: D e A divididos verticalmente; C com quatro níveis e B com dois. Cotas preliminares."><div class="kitchen-elevation">${modules.map(([letter,name,width,base,shelves,vertical])=>`<div class="elevation-module" style="flex:${width};height:${(255-base)*2}px"><div class="module-box">${vertical?'<i class="vertical-divider"></i>':''}${shelves.map(y=>`<i class="horizontal-divider" style="bottom:${(y-base)/(255-base)*100}%"></i>`).join('')}<strong>${letter}</strong></div><span>${name}<small>${String(width).replace('.',',')} cm</small></span></div>`).join('')}</div><p>Vista frontal · divisões aprovadas · larguras externas de estudo</p></div>`;
 }
 const levels=kind==='sink'?['Panelas: duas pilhas de pequena + média','Pressão 3 L · tampas · frigideira · tábuas · escorredor']:kind==='drawers'?['Talheres e facas','Utensílios de preparo','Temperos']:null;
 return levels?`<div class="storage-levels" role="img" aria-label="Organização de cima para baixo">${levels.map((s,i)=>`<div><span>${i+1}</span>${s}</div>`).join('')}</div><p class="diagram-caption">Esquema de organização; não representa o tamanho dos utensílios.</p>`:'';
}
function showStorage(id){
 const data=INTERNALS[id];if(!data)return;
 $('storageSelect').value=id;
 $('storageContent').innerHTML=`<h3>${esc(data.title)}</h3><span class="badge study">${esc(data.status)}</span>${storageDiagram(id)}<dl class="storage-details">${data.rows.map(([a,b])=>`<div><dt>${esc(a)}</dt><dd>${esc(b)}</dd></div>`).join('')}</dl><p class="storage-note">${esc(data.note)}</p><button id="storageInScene">Ver este armário no 3D</button>`;
 $('storageInScene').onclick=()=>{$('storageDialog').close();tab('model');setRoom(ITEMS.find(o=>o.id===id).room);state.inside=true;state.upper=true;$('insideToggle').checked=true;$('upperToggle').checked=true;selectItem(id,false);requestRender();};
}
function openStorage(id){
 id=INTERNALS[id]?id:Object.keys(INTERNALS).find(key=>ITEMS.find(o=>o.id===key)?.room===state.room)||'kitchenupper';
 showStorage(id);if(!$('storageDialog').open)$('storageDialog').showModal();
}
function buildMood(){let highlights={sala:['bonnie','table','bench','diningchairs','racks','tv50'],quarto:['queen','wardrobe','mirror','headboard','bedcabinet','ledges'],escritorio:['daiane','desk','officecab','officeshelf','drawers','officechair'],cozinha:['kitchenbase','sinkstorage','lowdrawer','kitchenupper','fridge','sink','filter','dishrack','pressurecooker','trash','cooktop','oven','microwave','hood'],lavanderia:['washer','laundrybase','recycling','airfryer','coffeemaker','laundryupper','drying','heater'],banho:['bathvanity','basin','bath tap','bathmirror','bathlight','toilet','shower','bath shelf','hygiene','hotwater','bathfinish']};
  $('moodRooms').innerHTML=PROJECT.rooms.filter(r=>r.id!=='all').map(r=>`<article class="mood-room"><canvas id="mood-${r.id}" aria-label="Volumetria proporcional: ${esc(r.name)}"></canvas><div class="content"><span class="eyebrow">${r.id==='quarto'?'NEUTROS · SEM TV · SEM AZUL':r.id==='escritorio'?'TRABALHO + HÓSPEDES':'PALETA E MOBILIÁRIO'}</span><h2>${esc(r.name)}</h2><div class="mini-palette">${PROJECT.materials.filter(m=>m.rooms.includes(r.id)&&m.id!=='altblue').slice(0,6).map(m=>`<i style="background:${m.color}" title="${esc(m.name)}"></i>`).join('')}</div><ul>${highlights[r.id].map(id=>{let o=ITEMS.find(o=>o.id===id);return`<li><strong>${esc(o.name)}</strong><span>${esc(o.dimensions)}<br><small>${esc(o.measure)}</small></span></li>`;}).join('')}</ul><p style="margin-top:14px">${esc(ROOM_NOTES[r.id])}</p><button data-explore="${r.id}">Explorar este ambiente</button></div></article>`).join('');
  $('materials').innerHTML=PROJECT.materials.map(m=>`<article class="material"><div class="swatch ${m.type}" style="${materialStyle(m)}"></div><div class="body"><strong>${esc(m.name)}</strong><span class="badge ${m.status==='Alternativa'?'study':''}">${esc(m.status)}</span><p>${esc(m.note)}</p></div></article>`).join('');
  document.querySelectorAll('[data-explore]').forEach(b=>b.onclick=()=>{setRoom(b.dataset.explore);tab('model');});
}
function renderMood(){buildScene();requestAnimationFrame(()=>{for(const r of PROJECT.rooms.filter(r=>r.id!=='all'))render($('mood-'+r.id),{...state,room:r.id,view:'iso',angle:({quarto:-2.4,cozinha:2.8,lavanderia:2.5,banho:2.8})[r.id]??-.7,tilt:.92,zoom:1,pan:[0,0],upper:true,selected:null},true);});}
function renderDecisions(){const room=$('filterRoom').value,filter=$('filterStatus').value;let list=ITEMS.filter(o=>(room==='all'||o.room===room)&&(filter==='all'||filter==='chosen'&&chosen(o)||filter==='pending'&&needsCheck(o)));
  $('decisionCards').innerHTML=list.map(o=>`<article class="decision-card ${needsCheck(o)?'pending':''}"><span class="source-label">${esc(PROJECT.rooms.find(r=>r.id===o.room)?.name)} · ${esc(o.source)}</span><h3>${esc(o.name)}</h3><span class="badge ${chosen(o)?'':'study'}">${esc(o.choice)}</span><span class="badge ${needsCheck(o)?'study':''}">${esc(o.measure)}</span><p class="dimensions">${esc(o.dimensions)}</p><p><strong>Material:</strong> ${esc(MAT[o.material]?.name||o.material)}</p><p>${esc(o.notes)}</p>${o.budget?'<p><strong>'+esc(o.budget)+'</strong></p>':''}${INTERNALS[o.id]?'<button data-storage="'+o.id+'" class="storage-link">Ver organização interna →</button>':''}</article>`).join('');
  $('decisionCards').querySelectorAll('[data-storage]').forEach(b=>b.onclick=()=>openStorage(b.dataset.storage));
}
function download(blob,name){let url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),2000);}
function saveHTML(){// Keep the initial executable document, not transient DOM/canvas state.
  const copy=document.documentElement.cloneNode(true);copy.querySelectorAll('canvas').forEach(c=>{c.width=300;c.height=150;});copy.querySelectorAll('dialog').forEach(d=>d.removeAttribute('open'));copy.querySelectorAll('.inspector').forEach(e=>e.classList.remove('open'));download(new Blob(['<!doctype html>\n'+copy.outerHTML],{type:'text/html;charset=utf-8'}),'Guedala_Park_Interativo.html');toast('HTML salvo. Abra a cópia no navegador do computador ou celular.');}
// Pointer gestures: drag orbit, shift/right-drag pan, pinch zoom, keyboard alternatives.
const canvas=$('scene'),pointers=new Map();let lastPoint=null,down=null,pinchDistance=0;
canvas.addEventListener('pointerdown',e=>{canvas.setPointerCapture(e.pointerId);pointers.set(e.pointerId,{x:e.clientX,y:e.clientY});lastPoint={x:e.clientX,y:e.clientY};down={x:e.clientX,y:e.clientY,moved:false};if(pointers.size===2){let p=[...pointers.values()];pinchDistance=Math.hypot(p[0].x-p[1].x,p[0].y-p[1].y);}});
canvas.addEventListener('pointermove',e=>{if(!pointers.has(e.pointerId))return;const prev=lastPoint;pointers.set(e.pointerId,{x:e.clientX,y:e.clientY});if(pointers.size>=2){let p=[...pointers.values()],dist=Math.hypot(p[0].x-p[1].x,p[0].y-p[1].y);if(pinchDistance>1)state.zoom=Math.max(.45,Math.min(5,state.zoom*dist/pinchDistance));pinchDistance=dist;if(down)down.moved=true;}else if(prev){let dx=e.clientX-prev.x,dy=e.clientY-prev.y;if(down&&Math.hypot(e.clientX-down.x,e.clientY-down.y)>5)down.moved=true;if(state.view==='iso'&&!e.shiftKey&&e.buttons!==2){state.angle+=dx*.008;state.tilt=Math.max(.16,Math.min(1.42,state.tilt-dy*.006));}else{state.pan[0]+=dx;state.pan[1]+=dy;}}lastPoint={x:e.clientX,y:e.clientY};requestRender();});
function pickFace(x,y,faces){
 let best=null,depth=-Infinity;
 for(const f of faces){if((f.alpha??1)<.5)continue;const p=f.points;
  for(let i=1;i<p.length-1;i++){const a=p[0],b=p[i],c=p[i+1],det=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1]);if(Math.abs(det)<1e-8)continue;
   const u=((b[1]-c[1])*(x-c[0])+(c[0]-b[0])*(y-c[1]))/det,v=((c[1]-a[1])*(x-c[0])+(a[0]-c[0])*(y-c[1]))/det,t=1-u-v;
   if(u>=0&&v>=0&&t>=0){const z=u*a[2]+v*b[2]+t*c[2];if(z>depth){depth=z;best=f;}}
  }
 }return best;
}
function release(e){if(e.type==='pointerup'&&down&&!down.moved&&pointers.size===1){const r=canvas.getBoundingClientRect(),x=e.clientX-r.left,y=e.clientY-r.top;const face=pickFace(x,y,hitFaces);if(face&&ITEMS.some(o=>o.id===face.id))selectItem(face.id);}pointers.delete(e.pointerId);lastPoint=pointers.size?[...pointers.values()][0]:null;down=null;pinchDistance=0;}
canvas.addEventListener('pointerup',release);canvas.addEventListener('pointercancel',release);canvas.addEventListener('contextmenu',e=>e.preventDefault());
canvas.addEventListener('wheel',e=>{e.preventDefault();state.zoom=Math.max(.45,Math.min(5,state.zoom*Math.exp(-e.deltaY*.001)));requestRender();},{passive:false});
function inPolygon(x,y,p){let inside=false;for(let i=0,j=p.length-1;i<p.length;j=i++){let a=p[i],b=p[j];if(((a[1]>y)!==(b[1]>y))&&(x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]))inside=!inside;}return inside;}
canvas.addEventListener('keydown',e=>{if(['ArrowLeft','ArrowRight','ArrowUp','ArrowDown','+','-','0'].includes(e.key)){e.preventDefault();if(e.key==='ArrowLeft')state.angle-=.15;if(e.key==='ArrowRight')state.angle+=.15;if(e.key==='ArrowUp')state.tilt=Math.min(1.42,state.tilt+.1);if(e.key==='ArrowDown')state.tilt=Math.max(.16,state.tilt-.1);if(e.key==='+')state.zoom=Math.min(5,state.zoom*1.15);if(e.key==='-')state.zoom=Math.max(.45,state.zoom/1.15);if(e.key==='0'){state.zoom=1;state.pan=[0,0];}requestRender();}});
function init(){
  $('storageSelect').innerHTML=Object.keys(INTERNALS).map(id=>`<option value="${id}">${esc(ITEMS.find(o=>o.id===id).name)}</option>`).join('');
  $('storageSelect').onchange=e=>showStorage(e.target.value);
  $('openStorage').onclick=()=>openStorage(state.selected);
  $('closeStorage').onclick=()=>$('storageDialog').close();
  $('storageDialog').addEventListener('click',e=>{const r=e.currentTarget.getBoundingClientRect();if(e.target===e.currentTarget&&(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom))e.currentTarget.close();});

  $('rooms').innerHTML=PROJECT.rooms.map(r=>`<button data-room="${r.id}" class="${r.id==='all'?'active':''}"><strong>${esc(r.name)}</strong><small>${esc(r.sub)}</small></button>`).join('');document.querySelectorAll('[data-room]').forEach(b=>b.onclick=()=>setRoom(b.dataset.room));
  document.querySelectorAll('[data-view]').forEach(b=>b.onclick=()=>setView(b.dataset.view));document.querySelectorAll('[data-tab]').forEach(b=>b.onclick=()=>tab(b.dataset.tab));
  $('sideCut').onchange=e=>{state.sideCut=e.target.checked;requestRender();};$('sideDirection').onchange=e=>{state.side=e.target.value;requestRender();};
  for(const[id,key]of [['sofaState','sofa'],['officeState','office'],['diningState','dining'],['tableState','table'],['consoleState','console'],['dryState','dry']])$(id).onchange=e=>{transitionState(key,e.target.value);if(key==='dry')toast(state.dry==='stored'?'Sem roupas: aparelhos permanecem na pedra da lavanderia.':'Com roupas: air fryer e cafeteira vão temporariamente para a cozinha.');if(key==='table')toast(state.table==='compact'?'Mesa com 150 cm: recuo de 15 cm por ponta. Cadeira da cabeceira e banco permanecem no lugar.':'Mesa com 180 cm: folha central de 30 cm para seis lugares.');};
  for(const[id,key]of [['sofaGap','sofaGap'],['rackDepth','rackDepth'],['headDepth','headDepth']])$(id).oninput=e=>{state[key]=Number(e.target.value);updateMetrics();requestRender();};
  for(const[id,key]of [['measureToggle','measures'],['upperToggle','upper'],['wallToggle','walls'],['insideToggle','inside']])$(id).onchange=e=>{state[key]=e.target.checked;requestRender();};
  $('zoomIn').onclick=()=>{state.zoom=Math.min(5,state.zoom*1.2);requestRender();};$('zoomOut').onclick=()=>{state.zoom=Math.max(.45,state.zoom/1.2);requestRender();};$('fit').onclick=()=>{state.zoom=1;state.pan=[0,0];state.angle=({quarto:-2.4,cozinha:2.8,lavanderia:2.5,banho:2.8})[state.room]??-.62;state.tilt=.92;requestRender();};
  $('rotateLeft').onclick=()=>{state.angle-=Math.PI/6;requestRender();};$('rotateRight').onclick=()=>{state.angle+=Math.PI/6;requestRender();};
  $('closeInfo').onclick=()=>$('inspector').classList.remove('open');$('mobileItems').onclick=()=>{$('inlineItems').hidden=!$('inlineItems').hidden;};
  $('snapshot').onclick=()=>{buildScene();render(canvas);canvas.toBlob(b=>download(b,'Guedala_'+state.room+'_'+state.view+'.png'));};$('downloadHTML').onclick=saveHTML;$('downloadHTML2').onclick=saveHTML;
  $('printMood').onclick=()=>window.print();$('exportData').onclick=()=>download(new Blob([JSON.stringify({project:PROJECT,items:ITEMS,interiors:INTERNALS,notes:ROOM_NOTES},null,2)],{type:'application/json'}),'Guedala_escolhas_R06.json');
  $('filterRoom').innerHTML=PROJECT.rooms.map(r=>`<option value="${r.id}">${esc(r.name)}</option>`).join('');$('filterRoom').onchange=renderDecisions;$('filterStatus').onchange=renderDecisions;
  $('sources').innerHTML=SOURCES.map(([s,n])=>`<div class="source"><strong>${esc(s)}</strong><span>${esc(n)}</span></div>`).join('');
  buildMood();buildScene();setRoom('all');setView('iso');selectItem('bonnie',false);$('inspector').classList.remove('open');new ResizeObserver(()=>{if($('model').classList.contains('active'))requestRender();if($('mood').classList.contains('active'))renderMood();}).observe($('stage'));window.addEventListener('resize',()=>{requestRender();if($('mood').classList.contains('active'))renderMood();});
  // A downloaded copy is initialized to the documented state; no edits persist silently.
  document.querySelectorAll('[data-tab]').forEach(b=>b.classList.toggle('active',b.dataset.tab==='model'));document.querySelectorAll('.tabpage').forEach(b=>b.classList.toggle('active',b.id==='model'));
  for(const[id,value]of [['sofaState','closed'],['officeState','work'],['diningState','stored'],['tableState','compact'],['consoleState','sala'],['dryState','stored'],['sofaGap','0'],['rackDepth','37'],['headDepth','5']])$(id).value=value;
  $('measureToggle').checked=true;$('upperToggle').checked=true;$('wallToggle').checked=false;$('insideToggle').checked=false;
  window.GuedalaStudy={state,items:ITEMS,project:PROJECT,transitionState,pickFace,diningClearance,getNodes:()=>nodes,buildScene:()=>{buildScene();return nodes;},render,tab,setRoom,setView,selectItem};
}
init();
