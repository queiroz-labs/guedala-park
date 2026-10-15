const fs=require('node:fs'), assert=require('node:assert/strict');
const pots=[
 {id:'Ou PFL100',volumeML:370,w:10,d:14,h:6.5,massG:330},
 {id:'Ou PFL200',volumeML:725,w:12,d:17,h:7.5,massG:550},
 {id:'Invicta 101528291773',volumeML:520,w:14,d:14,h:6.5,massG:440},
 {id:'Invicta 101528291769',volumeML:640,w:13.5,d:17.9,h:6.3,massG:460},
 {id:'Invicta 101528291770',volumeML:1000,w:15.3,d:20.4,h:6.9,massG:732}
];
const trays=[[26.2,18],[19.2,12]], r1=[12.8,22.3,22.8], r3=[10.5,23.3,17.6];
const grid=(a,b,w,d)=>Math.max(Math.floor(a/w)*Math.floor(b/d),Math.floor(a/d)*Math.floor(b/w));
const results=pots.map(p=>({ ...p, sixVolumeL:6*p.volumeML/1000,sixMassKg:6*p.massG/1000,
 trayGridPerLayer:trays.map(t=>grid(...t,p.w,p.d)),
 sixArea:6*p.w*p.d,trayArea:trays.reduce((s,t)=>s+t[0]*t[1],0),
 singleLayerAreaImpossible:6*p.w*p.d>702,
 twoLayersHeight:2*p.h+.2,twoLayersFitBenchHeight:2*p.h+.2<=8.5,
 r1GridEmptyUpright:grid(r1[0],r1[1],p.w,p.d),r1StackEmptyNoProtection:Math.floor(r1[2]/p.h),
 r1ActualAdditionalCapacityWithMixer:0
}));
// Explicit six-container alternative on EXISTING proposed panel surfaces, trays omitted.
// All coordinates are the original bench local coordinates, in centimetres.
const positions=[1,21].flatMap(y=>[.8,11.8,22.8].map(x=>({x,y,z:17.8,w:10,d:14,h:6.5})));
const panels=[{x:0,y:0,w:36.2,d:19},{x:0,y:20,w:36.2,d:19}];
const lower=[{x:1.1,y:16,z:.3,w:34,d:22,h:10},{x:3.1,y:1,z:.3,w:30,d:14,h:12},{x:39,y:1,z:.3,w:18,d:18,h:20},{x:39,y:20,z:.3,w:18,d:18,h:24}];
const hit=(a,b)=>a.x<b.x+b.w&&a.x+a.w>b.x&&a.y<b.y+b.d&&a.y+a.d>b.y&&a.z<b.z+b.h&&a.z+a.h>b.z;
for(const p of positions){assert(panels.some(q=>p.x>=q.x&&p.x+p.w<=q.x+q.w&&p.y>=q.y&&p.y+p.d<=q.y+q.d));assert(p.z+p.h+.5+3<=30);for(const q of lower)assert(!hit(p,q));}
for(let i=0;i<6;i++)for(let j=i+1;j<6;j++)assert(!hit(positions[i],positions[j]));
const recipients=[{id:'Ou JB2100NT',volumeL:1.5,w:9.5,d:15.5,h:27,massG:450,frequency:'semanal'},{id:'alfi 3527205150',volumeL:1.5,w:13.5,d:15.6,h:26.3,massG:1012,frequency:'diária'}].map(p=>({...p,r3Upright:grid(r3[0],r3[1],p.w,p.d)>0&&p.h<=r3[2],r1EmptyUpright:grid(r1[0],r1[1],p.w,p.d)>0&&p.h<=r1[2],r3HeightExcess:p.h-r3[2],r1HeightExcess:p.h-r1[2],massFilledWith1500gWaterKg:(p.massG+1500)/1000}));
assert(results.every(p=>p.singleLayerAreaImpossible&&!p.twoLayersFitBenchHeight));assert(recipients.every(p=>!p.r3Upright&&!p.r1EmptyUpright));
const output={date:'2026-10-06',units:'cm; g; L',status:'Conferência nominal; sem produto escolhido ou liberação de fabricação',pots:results,recipients,benchSix370Alternative:{positions,lowerPreserved:lower,allInsidePanels:true,staticCollisions:0,structuralApproval:false,extractionRevalidated:false,traysOmitted:true,adopted:false},method:'Grades ortogonais como layouts testados; área como limite necessário; sem encaixe de potes vazios ou remoção de tampas presumidos. Massa com água: hipótese 1 g/mL, não carga técnica.'};
fs.writeFileSync(__dirname+'/Resultados_vidros_15L.json',JSON.stringify(output,null,2));console.log('Conferências de área, altura, variante e 6 posições: PASSOU. Layout não adotado.');
