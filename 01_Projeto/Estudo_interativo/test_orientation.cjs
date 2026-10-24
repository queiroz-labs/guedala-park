// Orientation against the official Torre 2, final 06 floor plan.
const fs=require('node:fs'),vm=require('node:vm'),path=require('node:path'),assert=require('node:assert/strict');
const src=path.join(__dirname,'src'),app=fs.readFileSync(path.join(src,'app.js'),'utf8');
const ctx=vm.createContext({console,matchMedia:()=>({matches:true})});
vm.runInContext(['data.js','cad-data.js','visual-finishes.js','cad-sync.js'].map(n=>fs.readFileSync(path.join(src,n),'utf8')).join('\n')+'\n'+app.slice(0,app.indexOf("const canvas=$('scene')")),ctx);
const run=s=>vm.runInContext(s,ctx),json=s=>JSON.parse(run('JSON.stringify('+s+')'));
assert.equal(run('PROJECT.mirrored'),false);
run('buildScene()');
const rooms=json('PROJECT.rooms'),bounds=rooms.find(r=>r.id==='all').bounds;
const project=(p,view='top',angle=0)=>json(`camera({...state,view:'${view}',angle:${angle}},1000,1000,${JSON.stringify(bounds)}).project(${JSON.stringify(p)})`);
// Bedroom left, office above centre, living right; bathroom above laundry.
const q=project([122.5,0,247.5]),o=project([370,0,147.5]),s=project([617.5,0,375]);
assert(q[0]<o[0]&&o[0]<s[0]);assert(o[1]<q[1]);assert(project([350,0,467])[1]<project([320,0,620])[1]);
for(const view of ['top','iso'])for(const angle of [-2.4,-.62,0,.7,2.8]){
 const a=project([0,0,0],view,angle),b=project([100,0,0],view,angle),c=project([0,0,100],view,angle);
 assert((b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])>0,'Camera must not reflect floor winding');
 for(const p of [[0,0,0],[740,0,690],[255,205,295]]){
  const matrix=json(`Array.from(camera({...state,view:'${view}',angle:${angle}},1000,1000,${JSON.stringify(bounds)}).matrix)`),screen=project(p,view,angle);
  const clip=[0,1,2].map(i=>matrix[i]*p[0]+matrix[4+i]*p[1]+matrix[8+i]*p[2]+matrix[12+i]);
  assert(Math.abs(clip[0]-(screen[0]/500-1))<1e-5);assert(Math.abs(clip[1]-(1-screen[1]/500))<1e-5);
 }
}
const nodes=json('nodes');
const windows=nodes.filter(n=>!n.id&&n.kind==='glass');assert.equal(windows.length,5);
for(const [room,x,z,w,d]of [['quarto',60,90,120,10],['escritorio',315,-10,115,10],['sala',533,175,139,10],['lavanderia',245,569,10,106],['banho',245,435,10,40]]){
 const n=windows.find(n=>n.room===room);assert.deepEqual([n.x,n.z,n.w,n.d],[x,z,w,d]);
}
const doors=nodes.filter(n=>n.kind==='door');assert.equal(doors.length,4);
// Hinges and closed leaves coincide with the four reconstructed wall openings.
const openings=[['quarto',[365,315],[365,390]],['escritorio',[400,295],[475,295]],['banho',[385,405],[455,405]],['cozinha',[740,615],[740,690]]];
for(const [room,a,b]of openings){const door=doors.find(n=>n.room===room),length=Math.hypot(b[0]-a[0],b[1]-a[1]);assert.equal(Math.max(door.w,door.d),length);}
const entrance=doors.find(n=>n.room==='cozinha');assert.equal(entrance.x+entrance.w,740);assert.equal(entrance.z+entrance.d,690);
const mean=id=>{const ns=nodes.filter(n=>n.id===id);assert(ns.length,id);return [ns.reduce((s,n)=>s+n.x+n.w/2,0)/ns.length,ns.reduce((s,n)=>s+n.z+n.d/2,0)/ns.length];};
// Fixed fixtures from the official plan: shower / WC / basin, tank left of kitchen sink.
assert(mean('shower')[0]<mean('toilet')[0]);assert(mean('toilet')[0]<mean('basin')[0]);assert(mean('laundrybase')[0]<mean('sink')[0]);
const modules=json('CAD_DATA.modules');
for(const m of modules){const ns=nodes.filter(n=>n.module===m.code);assert(ns.length,m.code);const r=rooms.find(r=>r.id===m.room).bounds;const cx=(Math.min(...ns.map(n=>n.x))+Math.max(...ns.map(n=>n.x+n.w)))/2,cz=(Math.min(...ns.map(n=>n.z))+Math.max(...ns.map(n=>n.z+n.d)))/2;assert(cx>=r[0]&&cx<=r[2]&&cz>=r[1]&&cz<=r[3],m.code+' outside its room');}
console.log(JSON.stringify({orientation:'official',cameraCases:10,gpuCpuConsistent:true,windows:5,doors:4,modulesInCorrectRooms:modules.length,fixedFixtures:'correct relative positions'}));
