/* Painéis atuais derivados do FreeCAD; estados de uso não são validação mecânica. */
// Geometry identity also invalidates caches when a new CAD revision is loaded.
const CAD_NORMALS=new WeakMap(),CAD_MESHES=new WeakMap();
function cadFaceColor(n,normal,triangle=null){
 const finish=n.visualFinish;
 if(!finish||n.finishHighlight)return n.c;
 if(triangle!==null&&finish.triangles)return color(finish.triangles[triangle]);
 if(finish.inner&&normal[finish.axis]*finish.outward<-.5)return color(finish.inner==='whiteTX'&&n.look?n.look:finish.inner);
 return n.c;
}
// Camera movement uses the same geometry and per-face finishes as the settled view.
// Meshes are cached in world coordinates; the renderer handles camera transforms.
function cadMesh(n){
 let variants=CAD_MESHES.get(n.v);if(!variants){variants=new Map();CAD_MESHES.set(n.v,variants);}
 const key=[n.x,n.y,n.z,n.c,n.opacity??1,!!n.finishHighlight,n.look||'',VISUAL_FINISHES.revision].join('|');
 if(variants.has(key))return variants.get(key);
 const finish=faces=>{if(variants.size>=4)variants.clear();variants.set(key,faces);return faces;};
 let cached=CAD_NORMALS.get(n.v)||n.preparedMesh;
 if(!cached){
  const normals=n.t.map(([a,b,c])=>{const A=n.v[a],B=n.v[b],C=n.v[c],u=B.map((v,i)=>v-A[i]),v=C.map((q,i)=>q-A[i]);const q=[u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]],l=Math.hypot(...q)||1;return q.map(v=>v/l);});
  // A tesselação duplica vértices entre faces. Unir por posição permite
  // desenhar as quinas reais sem expor diagonais internas dos triângulos.
  const keys=n.v.map(v=>v.join(',')),edges=new Map(),masks=n.t.map(()=>[true,true,true]);
  n.t.forEach((t,i)=>t.forEach((a,j)=>{const b=t[(j+1)%3],ka=keys[a],kb=keys[b],key=ka<kb?ka+'|'+kb:kb+'|'+ka;const e=edges.get(key)||[];e.push([i,j]);edges.set(key,e);}));
  for(const pair of edges.values())if(pair.length===2){const [a,b]=pair,dot=normals[a[0]].reduce((s,v,k)=>s+v*normals[b[0]][k],0);if(dot>Math.cos(Math.PI/9)){masks[a[0]][a[1]]=false;masks[b[0]][b[1]]=false;}}
  cached={normals,masks};CAD_NORMALS.set(n.v,cached);
 }
 return finish(n.t.map((f,i)=>({p:f.map(k=>[n.x+n.v[k][0],n.y+n.v[k][1],n.z+n.v[k][2]]),normal:cached.normals[i],edgeMask:cached.masks[i],c:cadFaceColor(n,cached.normals[i],i),alpha:n.opacity??1,id:n.id,room:n.room,node:n})));
}
// Covers not tagged as fronts in the R45 export. Fixed corner fascia is hidden
// only for the inspection cut; supports, geometry and quantities remain intact.
const INTERIOR_COVERS=new Set(['FrenteVizinhaR18','FaixaQuinaAR04','FaixaQuinaBR04']);
function isInteriorCover(part){return !!part.front||INTERIOR_COVERS.has(part.source);}
function applyCadSync(scene,st){
 const ids=new Set(CAD_DATA.replacements);
 const result=scene.filter(n=>!ids.has(n.id));
 for(const part of CAD_DATA.parts){
  if(part.scenario && part.scenario!==st.table)continue;
  if(st.moduleFilter && part.module!==st.moduleFilter)continue;
  if(st.inside&&isInteriorCover(part))continue;
  const n={...part};
  // Berlin: the native closed reference is 2+1; the open reference has
  // three chairs on the free side. Only the open use demonstration pulls out.
  if(n.id==='diningchairs'&&st.table==='extended'&&st.dining==='use')n.x-=34;
  n.visualFinish=VISUAL_FINISHES.parts[part.finishSource||part.source];
  // Só na visualização: onde a chapa seria Branco TX, o 3D usa a cor do próprio móvel (o acabamento real não muda).
  const code=(part.module||'').match(/P\d\d/)?.[0],look=VISUAL_FINISHES.modules[code];
  if(look&&look!=='mirror'&&look!=='whiteTX')n.look=look;
  if(n.visualFinish){n.mat=n.visualFinish.material==='whiteTX'&&n.look?n.look:n.visualFinish.material;n.c=color(n.mat);}
  if(Array.isArray(st.focusPart)?st.focusPart.includes(part.source):st.focusPart===part.source){n.c='#d49a51';n.finishHighlight=true;}
  result.push(n);
 }
 return st.moduleFilter?result.filter(n=>n.module===st.moduleFilter):result;
}
