// Geometry parsing and edge analysis run off the UI thread; no simplification.
self.onmessage=async({data:{url}})=>{
 try{
  const response=await fetch(url);if(!response.ok)throw Error('HTTP '+response.status);
  const parts=await response.json();
  for(const part of parts){
   const normals=part.t.map(([a,b,c])=>{
    const A=part.v[a],B=part.v[b],C=part.v[c],u=B.map((v,i)=>v-A[i]),v=C.map((q,i)=>q-A[i]);
    const q=[u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]],l=Math.hypot(...q)||1;
    return q.map(v=>v/l);
   });
   const keys=part.v.map(v=>v.join(',')),edges=new Map(),masks=part.t.map(()=>[true,true,true]);
   part.t.forEach((t,i)=>t.forEach((a,j)=>{
    const ka=keys[a],kb=keys[t[(j+1)%3]],key=ka<kb?ka+'|'+kb:kb+'|'+ka;
    const e=edges.get(key)||[];e.push([i,j]);edges.set(key,e);
   }));
   for(const pair of edges.values())if(pair.length===2){
    const [a,b]=pair,dot=normals[a[0]].reduce((s,v,k)=>s+v*normals[b[0]][k],0);
    if(dot>Math.cos(Math.PI/9)){masks[a[0]][a[1]]=false;masks[b[0]][b[1]]=false;}
   }
   part.preparedMesh={normals,masks};
   // Small messages avoid cloning the complete model in one long UI task.
   self.postMessage({part});
  }
  self.postMessage({done:true});
 }catch(error){self.postMessage({error:error.message});}
};
