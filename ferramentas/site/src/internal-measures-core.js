/* Exact plane sections of exported panel meshes. All calculations in mm. */
const InternalMeasures=(()=>{
 const EPS=.002,axes={front:[0,2,1],side:[1,2,0],top:[0,1,2]};
 const unique=xs=>xs.sort((a,b)=>a-b).filter((v,i,a)=>!i||v-a[i-1]>EPS);
 function localPoint(part,v,frame){
  const p=[7400-(part.x+v[0])*10,(part.z+v[2])*10,(part.y+v[1])*10,1];
  const q=frame.slice(0,3).map(row=>row.reduce((s,n,i)=>s+n*p[i],0));return [-q[0],q[1],q[2]];
 }
 function panels(parts,frame){
  return parts.filter(p=>p.piece&&!p.front).map(p=>({source:p.source,label:p.label,c:p.c,points:p.v.map(v=>localPoint(p,v,frame)),triangles:p.t}));
 }
 function bounds(panels){
  const lo=[Infinity,Infinity,Infinity],hi=[-Infinity,-Infinity,-Infinity];
  for(const p of panels)for(const v of p.points)for(let k=0;k<3;k++){lo[k]=Math.min(lo[k],v[k]);hi[k]=Math.max(hi[k],v[k]);}
  return {lo,hi};
 }
 function section(panels,view,depth){
  const [a,b,c]=axes[view];
  return panels.map(panel=>{
   const segments=[],seen=new Set();
   for(const ids of panel.triangles){
    const points=[];
    for(let i=0;i<3;i++){
     const p=panel.points[ids[i]],q=panel.points[ids[(i+1)%3]],d=p[c]-depth,e=q[c]-depth;
     if(Math.abs(d)<EPS)points.push([p[a],p[b]]);
     if(d*e<0){const t=d/(d-e);points.push([p[a]+t*(q[a]-p[a]),p[b]+t*(q[b]-p[b])]);}
    }
    const distinct=[];for(const p of points)if(!distinct.some(q=>Math.hypot(p[0]-q[0],p[1]-q[1])<EPS))distinct.push(p);
    if(distinct.length!==2||Math.hypot(distinct[0][0]-distinct[1][0],distinct[0][1]-distinct[1][1])<EPS)continue;
    const key=distinct.map(p=>p.map(x=>Math.round(x/EPS)).join(',')).sort().join('|');
    if(!seen.has(key)){seen.add(key);segments.push(distinct);}
   }
   return {...panel,segments};
  }).filter(p=>p.segments.length);
 }
 function intervals(segments,axis,probe){
  const other=1-axis,hits=[];
  for(const [p,q] of segments)if((p[other]<=probe&&q[other]>probe)||(q[other]<=probe&&p[other]>probe)){
   const t=(probe-p[other])/(q[other]-p[other]);hits.push(p[axis]+t*(q[axis]-p[axis]));
  }
  const sorted=unique(hits);if(sorted.length%2)return null;
  const result=[];for(let i=0;i<sorted.length;i+=2)if(sorted[i+1]-sorted[i]>EPS)result.push([sorted[i],sorted[i+1]]);return result;
 }
 function gaps(cut,axis,probe){
  const solid=[];
  for(const p of cut){const ranges=intervals(p.segments,axis,probe);if(ranges===null)return {gaps:[],uncertain:true};for(const [lo,hi] of ranges)solid.push({lo,hi,start:p.source,end:p.source});}
  solid.sort((a,b)=>a.lo-b.lo);const union=[];
  for(const p of solid){const last=union.at(-1);if(last&&p.lo<=last.hi+EPS){if(p.hi>last.hi){last.hi=p.hi;last.end=p.end;}}else union.push({...p});}
  return {gaps:union.slice(1).map((p,i)=>({from:union[i].hi,to:p.lo,size:p.lo-union[i].hi,between:[union[i].end,p.start]})).filter(p=>p.size>.5),uncertain:false};
 }
 // Stitch the boundary for SVG even-odd fills, including panel cut-outs.
 function paths(segments){
  const key=p=>p.map(x=>Math.round(x/.02)).join(','),edges=segments.map(([a,b])=>({a,b,used:false})),at=new Map();
  for(const e of edges)for(const p of [e.a,e.b]){const k=key(p);if(!at.has(k))at.set(k,[]);at.get(k).push(e);}
  const loops=[];
  for(const e of edges){if(e.used)continue;e.used=true;const pts=[e.a,e.b];let end=e.b;
   while(key(end)!==key(pts[0])){const next=(at.get(key(end))||[]).find(e=>!e.used);if(!next)break;next.used=true;end=key(next.a)===key(end)?next.b:next.a;pts.push(end);}
   loops.push({points:pts,closed:key(end)===key(pts[0])});
  }return loops;
 }
 return {axes,panels,bounds,section,intervals,gaps,paths,localPoint};
})();
if(typeof module!=='undefined')module.exports=InternalMeasures;
