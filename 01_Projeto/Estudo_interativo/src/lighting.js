// Presentation only. World centimetres; independent of furniture dimensions/material choices.
const LIGHTING_CONFIG={
  rooms:['sala','cozinha'],
  ambient:.68,
  hemisphere:.14,
  key:{direction:[-.45,.82,-.35],intensity:.24,tint:[1,.985,.955]},
  edges:.86,
  contact:{strength:.25,softness:3,maxGap:22,maxPatches:48}
};
function enhancedLighting(st){return st.view==='iso'&&LIGHTING_CONFIG.rooms.includes(st.room)&&st.lighting!=='before';}
const FACE_LIGHT_CACHE=new WeakMap();
function faceLighting(f,enhanced){
  const source=f._mesh||f,slot=enhanced?1:0;
  let entry=FACE_LIGHT_CACHE.get(source);if(!entry){entry=[];FACE_LIGHT_CACHE.set(source,entry);}
  if(entry[slot])return entry[slot];
  return entry[slot]=computeFaceLighting(f,enhanced);
}
function computeFaceLighting(f,enhanced){
  if(!enhanced||!LIGHTING_CONFIG.rooms.includes(f.room))return rgb(shade(f.c,f.normal[1]?1.04:.80+.11*f.normal[0]-.07*f.normal[2])).map(v=>v/255);
  const c=LIGHTING_CONFIG,n=f.normal,l=c.key.direction,len=Math.hypot(...l)||1;
  const direct=Math.max(0,(n[0]*l[0]+n[1]*l[1]+n[2]*l[2])/len);
  const fill=c.ambient+c.hemisphere*(n[1]*.5+.5);
  // Bounded, gentle tint: preserve the material palette and avoid white clipping.
  return rgb(f.c).map((v,i)=>Math.min(1,v/255*(fill+direct*c.key.intensity*c.key.tint[i])));
}
function contactPatches(faces){
  const cfg=LIGHTING_CONFIG.contact,allowed=f=>LIGHTING_CONFIG.rooms.includes(f.room);
  const bounds=f=>{const xs=f.p.map(p=>p[0]),zs=f.p.map(p=>p[2]);return [Math.min(...xs),Math.min(...zs),Math.max(...xs),Math.max(...zs)];};
  const receivers=faces.filter(f=>allowed(f)&&f.normal[1]>.99&&(f.alpha??1)>.995&&f.node.kind!=='wall').map(f=>({f,b:bounds(f),y:f.p[0][1]}));
  const inside=(x,z,p)=>{let hit=false;for(let i=0,j=p.length-1;i<p.length;j=i++){const a=p[i],b=p[j];if((a[2]>z)!==(b[2]>z)&&x<(b[0]-a[0])*(z-a[2])/(b[2]-a[2])+a[0])hit=!hit;}return hit;};
  const patches=[];
  for(const f of faces){
    if(!allowed(f)||!f.id||f.normal[1]>-.99||(f.alpha??1)<.02||['glass','floor','wall','door'].includes(f.node.kind))continue;
    const b=bounds(f),x=(b[0]+b[2])/2,z=(b[1]+b[3])/2,y=f.p[0][1];
    if(b[2]-b[0]<.8||b[3]-b[1]<.8)continue;
    let support=null;
    for(const r of receivers){
      const gap=y-r.y;
      if(r.f.node.key===f.node.key||gap<-.05||gap>cfg.maxGap||x<r.b[0]||x>r.b[2]||z<r.b[1]||z>r.b[3]||!inside(x,z,r.f.p))continue;
      if(!support||r.y>support.y)support=r;
    }
    if(!support)continue;
    const gap=Math.max(0,y-support.y),strength=cfg.strength*(1-gap/cfg.maxGap)*(f.alpha??1);
    if(strength<.01)continue;
    patches.push({rect:[x,z,(b[2]-b[0])/2,(b[3]-b[1])/2],settings:[support.y,strength,cfg.softness+gap*.45,0],source:f.node.key});
  }
  // Prefer grounded contacts; max() in the shader prevents overlapping parts darkening repeatedly.
  patches.sort((a,b)=>b.settings[1]-a.settings[1]||b.rect[2]*b.rect[3]-a.rect[2]*a.rect[3]);
  return patches.slice(0,Math.min(48,cfg.maxPatches));
}
function syncLightingControls(){
  const available=LIGHTING_CONFIG.rooms.includes(state.room)&&state.view==='iso';
  const panel=document.getElementById('lightingComparison');if(!panel)return;
  panel.hidden=!available;
  for(const b of panel.querySelectorAll('[data-lighting]')){const active=b.dataset.lighting===state.lighting;b.classList.toggle('active',active);b.setAttribute('aria-pressed',String(active));}
  const status=document.getElementById('lightingStatus'),text=state.lighting==='before'?'Antes · iluminação original':'Depois · luz suave e sombras de contato';
  if(status.textContent!==text)status.textContent=text;
}
