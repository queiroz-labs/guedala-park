const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const core={};vm.runInNewContext(fs.readFileSync(path.join(__dirname,'src/internal-measures-core.js'),'utf8')+';this.I=InternalMeasures;',core);const I=core.I;
const plain=x=>JSON.parse(JSON.stringify(x));
function box(source,x,y,z,w,d,h){
 const points=[[x,y,z],[x+w,y,z],[x+w,y+d,z],[x,y+d,z],[x,y,z+h],[x+w,y,z+h],[x+w,y+d,z+h],[x,y+d,z+h]];
 return {source,points,triangles:[[0,2,1],[0,3,2],[4,5,6],[4,6,7],[0,1,5],[0,5,4],[1,2,6],[1,6,5],[2,3,7],[2,7,6],[3,0,4],[3,4,7]]};
}
const cabinet=[box('left',0,0,0,18,400,900),box('right',582,0,0,18,400,900),box('bottom',18,0,0,564,400,18),box('top',18,0,882,564,400,18),box('shelf',18,0,300,564,400,18)];
const cut=I.section(cabinet,'front',200);
assert.deepEqual(plain(I.gaps(cut,0,500).gaps.map(g=>g.size)),[564]);
assert.deepEqual(plain(I.gaps(cut,1,200).gaps.map(g=>g.size)),[282,564]);
assert.deepEqual(plain(I.gaps(I.section(cabinet,'front',450),0,500).gaps),[],'A board absent at this depth cannot bound a gap');
assert.deepEqual(plain(I.gaps(I.section(cabinet,'top',500),0,200).gaps.map(g=>g.between)),[['left','right']]);
assert.equal(I.gaps([{source:'open',segments:[[[0,0],[0,100]]]}],0,50).uncertain,true);
assert(I.paths(cut[0].segments).every(p=>p.closed));
// Multiple solids / an actual hole must not become a bounding-box obstacle.
const ring=[box('one',0,0,0,18,400,900),box('one',582,0,0,18,400,900),box('one',18,0,0,564,400,18),box('one',18,0,882,564,400,18)];
const rings=I.section(ring,'front',200);assert.deepEqual(plain(I.gaps([{source:'ring',segments:rings.flatMap(p=>p.segments)}],0,500).gaps.map(g=>g.size)),[564]);
assert.deepEqual(plain(I.localPoint({x:700,y:10,z:20},[0,0,0],[[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]])),[-400,200,100]);
const ctx={};vm.runInNewContext(fs.readFileSync(path.join(__dirname,'src/cad-data.js'),'utf8')+';this.data=CAD_DATA;',ctx);
const frames=JSON.parse(fs.readFileSync(path.join(__dirname,'fabrication/module-frames.json'),'utf8'));
assert.equal(frames.sha256,ctx.data.current_source_sha256);
let checks=0;
for(const m of ctx.data.modules){
 const ps=I.panels(ctx.data.parts.filter(p=>p.module===m.code),frames.frames[m.code]);assert(ps.length,m.code);
 const b=I.bounds(ps);
 for(const view of ['front','side','top']){
  const [a,z,d]=I.axes[view],section=I.section(ps,view,(b.lo[d]+b.hi[d])/2);
  for(const [axis,other]of [[0,z],[1,a]]){
   const result=I.gaps(section,axis,b.lo[other]+.37*(b.hi[other]-b.lo[other]));
   for(const g of result.gaps){assert(Number.isFinite(g.size)&&g.size>.5);assert(g.between.every(id=>ps.some(p=>p.source===id)));checks++;}
  }
 }
}
console.log('Internal sections: fixture clearances, holes, open contours, coordinates and 20 native modules OK;',checks,'measured gaps');
