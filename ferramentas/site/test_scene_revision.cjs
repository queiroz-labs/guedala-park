// Regression checks for the R52 scene; no document or source mutations.
const fs=require('node:fs'),vm=require('node:vm'),path=require('node:path'),assert=require('node:assert/strict');
const src=path.join(__dirname,'src'),app=fs.readFileSync(path.join(src,'app.js'),'utf8'),shell=fs.readFileSync(path.join(src,'shell.html'),'utf8');
const ctx=vm.createContext({console,matchMedia:()=>({matches:true})});
vm.runInContext(['data.js','cad-data.js','visual-finishes.js','site-copy.js','cad-sync.js'].map(n=>fs.readFileSync(path.join(src,n),'utf8')).join('\n')+'\n'+app.slice(0,app.indexOf("const canvas=$('scene')")),ctx);
const run=s=>vm.runInContext(s,ctx),get=s=>JSON.parse(run('JSON.stringify('+s+')'));
const scene=values=>{run('Object.assign(state,'+JSON.stringify(values)+');buildScene()');return get('nodes');};
const overlap=(a,b)=>[['x','w'],['y','h'],['z','d']].every(([k,d])=>Math.min(a[k]+a[d],b[k]+b[d])-Math.max(a[k],b[k])>1e-6);
// Intersect chair triangles with the table height, then check their section
// segments against the rectangular native tabletop. Seating under it is allowed.
function crossesTable(chair,table){
 const eps=1e-6,left=table.x+eps,right=table.x+table.w-eps,near=table.z+eps,far=table.z+table.d-eps;
 for(const tri of chair.t){
  const v=tri.map(i=>[chair.x+chair.v[i][0],chair.y+chair.v[i][1],chair.z+chair.v[i][2]]),points=[];
  for(let j=0;j<3;j++){
   const a=v[j],b=v[(j+1)%3],da=a[1]-table.y,db=b[1]-table.y;
   if(Math.abs(da)<eps)points.push(a);
   if(da*db<0){const t=da/(da-db);points.push(a.map((x,k)=>x+(b[k]-x)*t));}
  }
  for(const p of points)if(p[0]>left&&p[0]<right&&p[2]>near&&p[2]<far)return true;
  for(let a=0;a<points.length;a++)for(let b=a+1;b<points.length;b++){
   let low=0,high=1,inside=true;
   for(const [axis,min,max]of [[0,left,right],[2,near,far]]){
    const origin=points[a][axis],delta=points[b][axis]-origin;
    if(Math.abs(delta)<eps){if(origin<=min||origin>=max)inside=false;}
    else{const t1=(min-origin)/delta,t2=(max-origin)/delta;low=Math.max(low,Math.min(t1,t2));high=Math.min(high,Math.max(t1,t2));}
   }
   if(inside&&low<high)return true;
  }
 }
 return false;
}
const cases=[];
for(const table of ['compact','extended'])for(const dining of ['stored','use'])for(const sofa of ['closed','open']){
 const ns=scene({table,dining,sofa}),chairs=ns.filter(n=>n.id==='diningchairs'),top=ns.find(n=>n.id==='table'&&n.source.endsWith('Tampo'));
 assert.equal(chairs.length,3,table+'/'+dining);assert(Math.abs(top.d-(table==='compact'?110:170))<1e-6);assert.equal(top.w,80);
 assert.equal(top.mat,'wood');assert.equal(ns.find(n=>n.id==='table'&&n.source.endsWith('Sapata')).mat,'black');
 assert(chairs.every(c=>!crossesTable(c,top)),'Chair back intersects tabletop');
 const couches=ns.filter(n=>n.id==='bonnie');assert(chairs.every(c=>couches.every(s=>!overlap(c,s))),'Chair intersects sofa envelope');
 for(const chair of chairs)assert.equal(run(`VISUAL_FINISHES.parts[${JSON.stringify(chair.finishSource||chair.source)}].triangles.length`),chair.t.length,'Preserve face finishes');
 cases.push({table,dining,sofa,chairs:chairs.length,topLengthCm:top.d});
}
const stored=scene({table:'extended',dining:'stored'}).filter(n=>n.id==='diningchairs'),used=scene({dining:'use'}).filter(n=>n.id==='diningchairs');
assert(used.every((n,i)=>Math.abs(n.x-stored[i].x+34)<1e-6));
run("updateMetrics=()=>{};drawLists=()=>{};syncExperience=()=>{};requestRender=()=>{};transitionState('table','compact')");assert.equal(run('state.dining'),'stored');
for(const dry of ['stored','high','low']){
 const ns=scene({dry}),racks=ns.filter(n=>n.id==='dishrack'),air=ns.find(n=>n.id==='airfryer');assert.equal(racks.length,dry==='stored'?2:0);assert(racks.every(r=>!overlap(r,air)));assert.equal(ns.filter(n=>n.id==='coffeemaker').length,0);
}
assert(!shell.includes('benchState'));assert(!fs.readFileSync(path.join(src,'experience.js'),'utf8').includes('benchState'));
assert(shell.includes('110 × 80')&&shell.includes('170 × 80'));assert.equal(scene({}).find(n=>n.id==='tv43').z,118);
assert(run("ITEMS.find(n=>n.id==='coffeemaker').notes.includes('não reserva')"));
assert.equal(run("diningClearance({table:'compact',dining:'stored'}).tableToFridge"),95.25);
assert.equal(run("diningClearance({table:'extended',dining:'stored'}).tableToFridge"),65.25);
assert.equal(run('PROJECT.revision'),'Consulta de marcenaria · FreeCAD R52 · iluminação CB02');assert.equal(run('PROJECT.date'),'26 outubro 2026');assert.match(run('CAD_DATA.current_source_sha256'),/^[a-f0-9]{64}$/);
console.log(JSON.stringify({revision:'R52',sourceSha256:run('CAD_DATA.current_source_sha256'),projectRevision:run('PROJECT.revision'),projectDate:run('PROJECT.date'),cases,chairsPresentInAllCases:true,chairMeshTableSectionsClear:true,chairSofaEnvelopesClear:true,openUseShiftCm:34,compactUseReset:true,dryStates:3,canceledBenchControlRemoved:true,coffeemakerUnmeasuredExplicit:true,tv43ZCm:118,manufacturingOrComfortCertified:false}));
// Height study is separate from confirmed site measurements and furniture geometry.
assert.equal(run('PROJECT.ceiling'),260);
assert.equal(run('PROJECT.officeCeilingStudy'),247);
assert.match(shell,/2,60 m = 260 cm = 2600 mm/);
assert.match(shell,/medida a confirmar/);
assert.match(shell,/não fabricação/);
const tallWalls=scene({walls:true}).filter(n=>n.kind==='wall'&&n.y===0);
assert(tallWalls.some(n=>n.room==='escritorio'));
for(const n of tallWalls)assert.equal(n.h,n.room==='escritorio'?247:260);
console.log(JSON.stringify({heightStudyCm:260,officeCeilingStudyCm:247,measured:false,manufacturing:false}));
