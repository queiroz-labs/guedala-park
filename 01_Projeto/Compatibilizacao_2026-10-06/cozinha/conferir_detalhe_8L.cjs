const fs=require('fs'),p=require('path'),a=require('assert/strict');
const b=(id,x,y,z,w,d,h)=>({id,x,y,z,w,d,h});
const hit=(r,s)=>r.x<s.x+s.w-1e-8&&s.x<r.x+r.w-1e-8&&r.y<s.y+s.d-1e-8&&s.y<r.y+r.d-1e-8&&r.z<s.z+s.h-1e-8&&s.z<r.z+r.h-1e-8;
const swept=(r,s)=>b(r.id,Math.min(r.x,s.x),Math.min(r.y,s.y),Math.min(r.z,s.z),r.w+Math.abs(r.x-s.x),r.d+Math.abs(r.y-s.y),r.h+Math.abs(r.z-s.z));
const inside=(r,box)=>r.x>=box.x&&r.y>=box.y&&r.z>=box.z&&r.x+r.w<=box.x+box.w+1e-8&&r.y+r.d<=box.y+box.d+1e-8&&r.z+r.h<=box.z+box.h+1e-8;
const ceiling=30, bottom=15.8, support=.8, protect=.2;
const panels=[b('panelFront',0,21.5,bottom,36.2,17.5,support),b('panelRear',0,0,bottom,36.2,20.5,support)];
const stacks=[{x:1,y:1,w:14.5,d:19},{x:16.5,y:1,w:14.5,d:19},{x:1,y:21.5,w:19,d:14.5}];
const pots=stacks.flatMap((s,i)=>[b('pot'+i+'top',s.x,s.y,21.7,s.w,s.d,4.7),b('pot'+i+'bottom',s.x,s.y,16.8,s.w,s.d,4.7)]);
const lower=[b('travessas',1.1,16,.3,34,22,10),b('batedeira',3.1,1,.3,30,14,12),b('motor',39,1,.3,18,18,20),b('blendJar',39,20,.3,18,18,24)];
const divider=b('divider',36.2,0,0,1.8,39,30);
const all=[...pots,...panels,...lower,divider], box=b('clean',0,0,0,60,39,30);
a(all.every(r=>inside(r,box)));a(all.every((r,i)=>all.slice(i+1).every(s=>!hit(r,s))));
for(const r of pots)a(panels.some(s=>r.x>=s.x&&r.x+r.w<=s.x+s.w&&r.y>=s.y&&r.y+r.d<=s.y+s.d));
const world=r=>b(r.id,40.8-r.y-r.d,1.8+r.x,10+r.z,r.d,r.w,r.h);
const fixed=[b('openedSeatIdeal',39,1.8,47,6,60,45),b('table',-70,15,72,75,150,3),b('chair1',-79,18,0,47,44,94),b('chair2',-87.5,68,0,47,44,94),b('chair3',-79,118,0,47,44,94),world(divider)];
let remaining=all.filter(r=>r.id!=='divider');const routes=[];
for(const obj of [...pots,...panels,...lower.slice(0,2)]){
 const r=world(obj),other=remaining.filter(s=>s.id!==obj.id).map(world);
 const elevation=obj.id.startsWith('pot')?36.6:obj.id.startsWith('panel')?31:obj.id==='travessas'?23.3:r.z;
 const nodes=[r,{...r,z:elevation},{...r,x:8,z:elevation},{...r,x:8,z:97},{...r,x:-10-r.w/2,y:50-r.d/2,z:97},{...r,x:-10-r.w/2,y:50-r.d/2,z:75}];
 for(let i=0;i<nodes.length-1;i++)for(const o of [...fixed,...other])a(!hit(swept(nodes[i],nodes[i+1]),o),obj.id+' hits '+o.id+' segment '+i);
 routes.push({id:obj.id,nodes,continuousSweptVolumesClear:true,parkingValidated:false});remaining=remaining.filter(s=>s.id!==obj.id);
}
const thermal=[13.0175,16.51,24.765],bay=b('selection',0,0,0,30.8,35,26.2);
const recipients=[b('TTS8L',0,0,.2,16,33,25),b('Vilde',17,0,.2,11.5,16,23),b('SHHC15',17,17,.2,...thermal)];
a(recipients.every(r=>inside(r,bay)));a(recipients.every((r,i)=>recipients.slice(i+1).every(s=>!hit(r,s))));
const verticalRoutes=recipients.map(r=>{const target={...r,z:27};for(const other of recipients.filter(s=>s.id!==r.id))a(!hit(swept(r,target),other));return{id:r.id,deltaToBaseAboveSelection:27-r.z,objectsOnlyVerticalSweepClear:true,actualOpeningOrHandlesValidated:false};});
const result={date:'2026-10-06',units:'cm',approvedBucketFunctionalLitres:8,bucketModelSelected:false,containerModelsSelected:false,depthExactOldCandidateRejectedAsReady:true,
 supportStudy:{panels,pots,lowerObjectsPreserved:lower,totalSupportBudget:.8,maxWholeAssembly:.9,belowReserve:3.5,aboveReserve:3.6,allPotBasesOnNominalPanels:true,rearPanelSpareAtPotEdge:.5,frontPotRearSpare:0,structureOrStrengthApproved:false,hardwareAndEdgeDetailsUnknown:true},
 routes:{count:routes.length,routes,continuousObjectOnlyRoutesClear:true,handBodyActualHingesUnknown:true,parkingForSixPotsAndTwoPanelsUnknown:true,idealSeatGeometryFrom20261003:true},
 narrowerThermal:{id:'ZojirushiSHHC15',capacityLitres:1.5,approxJapan:[13,16.5,24.5],convertedUS:thermal,conversionNotManufacturingTolerance:true},
 drinksBucket:{recipients,bay,depthUsed:33.51,depthSpare:1.49,widthUsed:30.0175,widthSpare:.7825,highestTop:25.2,heightSpare:1,barrierAndAllLateralLossMaxBeforeTolerances:.7825,verticalRoutes,actualDrawingsAndTolerancesKnown:false,separationSanitaryValidated:false,wholePhysicalSolutionApproved:false},
 reserveSensitivity:{potSupport8mm:{combinedStackHeightBudget:9.7,assumedStackHeight:9.6,spare:.1},extra1mmConsumesAllAboveReserve:true},
 blockers:['actual closed double-stack dimension/mass','all support/frame/fixation <=9mm and structural calculation','sanitary partition/containment and cleanability drawing','dimensions/tolerances/handles folded and upright','seat hinges real opening and temporary parking','unquantified competing stock remains occupied']};
fs.writeFileSync(p.join(__dirname,'Detalhe_8L_resultados.json'),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({routes:routes.length,continuousBoxesOnly:true,depthSpare:1.49,lateralBudgetMm:7.825,previousClearancesPreserved:true,physicalSolution:false}));
