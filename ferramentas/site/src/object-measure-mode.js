/* Cotas do objeto escolhido, usando o mesmo desenho de cotas das passagens. */
let objectMeasuring=false;
function drawObjectMeasure(ctx,project,st){
 const r=objectRecords().find(r=>r.key===objectSelected);if(!r?.box||st.room!=='all'&&st.room!==r.roomId)return;
 const n=r.node,box=r.box;if(!visible(n,st)||st.moduleFilter&&st.moduleFilter!==n.module)return;
 ctx.save();ctx.strokeStyle='#c17b37';ctx.lineWidth=2;
 for(const part of nodes.filter(q=>objectKey(q)===r.key))for(const f of mesh(part)){ctx.beginPath();f.p.forEach((p,i)=>{if(f.edgeMask&&!f.edgeMask[i])return;const a=project(p),b=project(f.p[(i+1)%f.p.length]);ctx.moveTo(a[0],a[1]);ctx.lineTo(b[0],b[1]);});ctx.stroke();}
 if(objectMeasuring){const {x,y,z,w,d,h}=box;dimension(ctx,project,[x,y,z],[x+w,y,z],cmTxt(w)+' cm');dimension(ctx,project,[x,y,z],[x,y,z+d],cmTxt(d)+' cm');dimension(ctx,project,[x+w,y,z+d],[x+w,y+h,z+d],cmTxt(h)+' cm');}
 ctx.restore();
}
$('stage').insertAdjacentHTML('afterend','<div class="object-measure-tools"><button type="button" id="objectMeasureToggle" aria-pressed="false">Medir objeto</button></div>');
$('objectMeasureToggle').onclick=()=>{objectMeasuring=!objectMeasuring;$('objectMeasureToggle').setAttribute('aria-pressed',String(objectMeasuring));requestRender();};
