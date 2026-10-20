/* Painéis atuais derivados do FreeCAD; estados de uso não são validação mecânica. */
const CAD_NORMALS=new Map();
function cadMesh(n){
 let cached=CAD_NORMALS.get(n.source);
 if(!cached){
  const normals=n.t.map(([a,b,c])=>{const A=n.v[a],B=n.v[b],C=n.v[c],u=B.map((v,i)=>v-A[i]),v=C.map((q,i)=>q-A[i]);const q=[u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]],l=Math.hypot(...q)||1;return q.map(v=>v/l);});
  // A tesselação duplica vértices entre faces. Unir por posição permite
  // desenhar as quinas reais sem expor diagonais internas dos triângulos.
  const keys=n.v.map(v=>v.join(',')),edges=new Map(),masks=n.t.map(()=>[true,true,true]);
  n.t.forEach((t,i)=>t.forEach((a,j)=>{const b=t[(j+1)%3],ka=keys[a],kb=keys[b],key=ka<kb?ka+'|'+kb:kb+'|'+ka;const e=edges.get(key)||[];e.push([i,j]);edges.set(key,e);}));
  for(const pair of edges.values())if(pair.length===2){const [a,b]=pair,dot=normals[a[0]].reduce((s,v,k)=>s+v*normals[b[0]][k],0);if(dot>Math.cos(Math.PI/9)){masks[a[0]][a[1]]=false;masks[b[0]][b[1]]=false;}}
  cached={normals,masks};CAD_NORMALS.set(n.source,cached);
 }
 return n.t.map((f,i)=>({p:f.map(k=>[n.x+n.v[k][0],n.y+n.v[k][1],n.z+n.v[k][2]]),normal:cached.normals[i],edgeMask:cached.masks[i],c:n.c,alpha:n.opacity??1,id:n.id,room:n.room,node:n}));
}
function applyCadSync(scene,st){
 const ids=new Set(CAD_DATA.replacements);
 const result=scene.filter(n=>!ids.has(n.id));
 for(const part of CAD_DATA.parts){
  if(st.inside&&part.front)continue;
  const n={...part};
  if(st.bench==='open'&&n.slide)n.z+=n.slide==='leaf'?84.3:72.3;
  result.push(n);
 }
 return result;
}
