/* Painéis atuais derivados do FreeCAD; estados de uso não são validação mecânica. */
// Geometry identity also invalidates caches when a new CAD revision is loaded.
const CAD_NORMALS=new WeakMap(),CAD_MESHES=new WeakMap();
function cadOverview(list){
 const groups=new Map(),out=[];
 for(const n of list){
  if(!n.module){out.push(n.kind==='cad'?n:{...n,kind:['floor','wall','glass'].includes(n.kind)?n.kind:'box'});continue;}
  let g=groups.get(n.module);
  if(!g){g={...n,kind:'box',x:n.x,y:n.y,z:n.z,xmax:n.x+n.w,ymax:n.y+n.h,zmax:n.z+n.d,colorWeight:-1};groups.set(n.module,g);}
  g.x=Math.min(g.x,n.x);g.y=Math.min(g.y,n.y);g.z=Math.min(g.z,n.z);
  g.xmax=Math.max(g.xmax,n.x+n.w);g.ymax=Math.max(g.ymax,n.y+n.h);g.zmax=Math.max(g.zmax,n.z+n.d);
  const weight=(n.front?1000:1)*Math.max(n.w*n.h,n.w*n.d,n.h*n.d);
  if(weight>g.colorWeight){g.colorWeight=weight;g.c=n.c;}
 }
 for(const g of groups.values()){g.w=g.xmax-g.x;g.h=g.ymax-g.y;g.d=g.zmax-g.z;out.push(g);}
 return out;
}
function cadMesh(n,interactive=false){
 let variants=CAD_MESHES.get(n.v);if(!variants){variants=new Map();CAD_MESHES.set(n.v,variants);}
 // Preserve simple panels exactly. Dense curved hardware/props use their envelope
 // only while the camera moves; the complete tessellation returns after settling.
 const coarse=interactive&&n.t.length>96,key=[coarse,n.x,n.y,n.z,n.c,n.opacity??1].join('|');
 if(variants.has(key))return variants.get(key);
 const finish=faces=>{if(variants.size>=4)variants.clear();variants.set(key,faces);return faces;};
 if(coarse){
  const lo=[0,1,2].map(i=>Math.min(...n.v.map(p=>p[i]))),hi=[0,1,2].map(i=>Math.max(...n.v.map(p=>p[i])));
  const v=[[0,0,0],[1,0,0],[1,1,0],[0,1,0],[0,0,1],[1,0,1],[1,1,1],[0,1,1]].map(p=>p.map((q,i)=>[n.x,n.y,n.z][i]+(q?hi[i]:lo[i])));
  return finish([[[0,3,2,1],[0,0,-1]],[[4,5,6,7],[0,0,1]],[[0,4,7,3],[-1,0,0]],[[1,2,6,5],[1,0,0]],[[0,1,5,4],[0,-1,0]],[[3,7,6,2],[0,1,0]]].map(([indices,normal])=>({p:indices.map(i=>v[i]),normal,c:n.c,alpha:n.opacity??1,id:n.id,room:n.room,node:n,coarse:true})));
 }
 let cached=CAD_NORMALS.get(n.v);
 if(!cached){
  const normals=n.t.map(([a,b,c])=>{const A=n.v[a],B=n.v[b],C=n.v[c],u=B.map((v,i)=>v-A[i]),v=C.map((q,i)=>q-A[i]);const q=[u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]],l=Math.hypot(...q)||1;return q.map(v=>v/l);});
  // A tesselação duplica vértices entre faces. Unir por posição permite
  // desenhar as quinas reais sem expor diagonais internas dos triângulos.
  const keys=n.v.map(v=>v.join(',')),edges=new Map(),masks=n.t.map(()=>[true,true,true]);
  n.t.forEach((t,i)=>t.forEach((a,j)=>{const b=t[(j+1)%3],ka=keys[a],kb=keys[b],key=ka<kb?ka+'|'+kb:kb+'|'+ka;const e=edges.get(key)||[];e.push([i,j]);edges.set(key,e);}));
  for(const pair of edges.values())if(pair.length===2){const [a,b]=pair,dot=normals[a[0]].reduce((s,v,k)=>s+v*normals[b[0]][k],0);if(dot>Math.cos(Math.PI/9)){masks[a[0]][a[1]]=false;masks[b[0]][b[1]]=false;}}
  cached={normals,masks};CAD_NORMALS.set(n.v,cached);
 }
 return finish(n.t.map((f,i)=>({p:f.map(k=>[n.x+n.v[k][0],n.y+n.v[k][1],n.z+n.v[k][2]]),normal:cached.normals[i],edgeMask:cached.masks[i],c:n.c,alpha:n.opacity??1,id:n.id,room:n.room,node:n})));
}
function applyCadSync(scene,st){
 const ids=new Set(CAD_DATA.replacements);
 const result=scene.filter(n=>!ids.has(n.id));
 for(const part of CAD_DATA.parts){
  if(part.scenario && part.scenario!==st.table)continue;
  if(st.moduleFilter && part.module!==st.moduleFilter)continue;
  if(st.inside&&part.front)continue;
  const n={...part};
  if(st.focusPart===part.source)n.c='#d49a51';
  result.push(n);
 }
 return st.moduleFilter?result.filter(n=>n.module===st.moduleFilter):result;
}
