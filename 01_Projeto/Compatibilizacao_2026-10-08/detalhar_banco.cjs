const fs=require('node:fs'),p=require('node:path'),a=require('node:assert/strict');
const base=JSON.parse(fs.readFileSync(p.join(__dirname,'Armazenamento_resultados.json'),'utf8'));
const b=(id,x,y,z,w,d,h)=>({id,x,y,z,w,d,h}),eps=1e-8;
const hit=(r,s)=>r.x<s.x+s.w-eps&&s.x<r.x+r.w-eps&&r.y<s.y+s.d-eps&&s.y<r.y+r.d-eps&&r.z<s.z+s.h-eps&&s.z<r.z+r.h-eps;
const sweep=(r,s)=>{a([r.x!==s.x,r.y!==s.y,r.z!==s.z].filter(Boolean).length<=1);return b(r.id,Math.min(r.x,s.x),Math.min(r.y,s.y),Math.min(r.z,s.z),r.w+Math.abs(r.x-s.x),r.d+Math.abs(r.y-s.y),r.h+Math.abs(r.z-s.z));};
const pairs=items=>items.forEach((r,i)=>items.slice(i+1).forEach(s=>a(!hit(r,s),r.id+' / '+s.id)));
const world=r=>b(r.id,40.8-r.y-r.d,1.8+r.x,r.z,r.d,r.w,r.h);
// References: app.js line 80, R00 bench external 1800 x 550, and 03/10 bench.seatDepth=45.
const bench={length:180,bodyDepth:55,seatDepth:45,seatTop:47,backrest:{u:[45,55],height:[40,90]},insideDepth:39};
const construction={bucketLid:{depth:44.8,width:21.6,thickness:2,closedZ:[40,42],hingeU:44.8,hingeZ:42,openDegrees:90,longitudinal:[75.7,97.3]},drinksLid:{depth:44.8,width:36.8,thickness:2,closedZ:[40,42],hingeU:44.8,hingeZ:42,openDegrees:90,longitudinal:[38.9,75.7]},cushion:{depth:45,width:21.6,thickness:5,closedZ:[42,47],parkingV:[149,170.6],parkingZ:[47,52]},drinksCushion:{depth:45,width:36.8,thickness:5,closedZ:[42,47],parkingV:[110,146.8],parkingZ:[47,52]},supportBudget:2.4,seatLoadVerified:false,lidHingeModel:null,newRoutineAccepted:true};
// Convex polygon distance in the (u,z) section. Rotation tested with a Lipschitz bound between samples.
const table2=[[-70,72],[5,72],[5,75],[-70,75]];
function intersect(A,B){for(const poly of [A,B])for(let i=0;i<poly.length;i++){let [x,y]=poly[i],q=poly[(i+1)%poly.length],n=[-(q[1]-y),q[0]-x];let av=A.map(t=>t[0]*n[0]+t[1]*n[1]),bv=B.map(t=>t[0]*n[0]+t[1]*n[1]);if(Math.max(...av)<Math.min(...bv)-eps||Math.max(...bv)<Math.min(...av)-eps)return false;}return true;}
function pointSegment(P,A,B){let dx=B[0]-A[0],dy=B[1]-A[1],t=Math.max(0,Math.min(1,((P[0]-A[0])*dx+(P[1]-A[1])*dy)/(dx*dx+dy*dy)));return Math.hypot(P[0]-A[0]-t*dx,P[1]-A[1]-t*dy);}
function distance(A,B){if(intersect(A,B))return 0;let d=Infinity;for(const [X,Y] of [[A,B],[B,A]])for(const P of X)for(let j=0;j<Y.length;j++)d=Math.min(d,pointSegment(P,Y[j],Y[(j+1)%Y.length]));return d;}
function lidPolygon(deg,depth=44.8,thickness=2,pivotZ=42,pivotU=44.8){let t=deg*Math.PI/180,c=Math.cos(t),s=Math.sin(t);return [[-depth,-thickness],[0,-thickness],[0,0],[-depth,0]].map(([u,z])=>[pivotU+u*c+z*s,pivotZ-u*s+z*c]);}
let minDistance=Infinity,minAngle=0,maxU=-Infinity;
for(let i=0;i<=900;i++){let poly=lidPolygon(i/10),d=distance(poly,table2);a(d>0,'Lid hits table');if(d<minDistance){minDistance=d;minAngle=i/10;}maxU=Math.max(maxU,...poly.map(t=>t[0]));}
const rotationBound=Math.hypot(44.8,2)*Math.PI/180*.1/2;
const continuousGapLowerBound=minDistance-rotationBound;
a(continuousGapLowerBound>0);a(maxU<=44.8+eps);
const table=b('Mesa',-70,15,72,75,150,3),back=b('Encosto',45,0,40,10,180,50);
const lidClosed=b('Tampa fina fechada',0,75.7,40,44.8,21.6,2),lidOpen=b('Tampa fina aberta',42.8,75.7,42,2,21.6,44.8);
const cushion=b('Almofada do balde',0,75.7,42,45,21.6,5);
const cushionNodes=[cushion,{...cushion,z:48},{...cushion,y:149,z:48},{...cushion,y:149,z:47}];
const fixedSeats=[b('Assento limpo fechado',0,0,40,45,75.7,7),b('Assento da folha fechado',0,97.3,40,45,82.7,7)];
const fixedForPad=[table,back,lidClosed,...fixedSeats];
for(let i=1;i<cushionNodes.length;i++)for(const o of fixedForPad)a(!hit(sweep(cushionNodes[i-1],cushionNodes[i]),o),'Pad hits '+o.id);
const padPark=cushionNodes.at(-1);
a(padPark.y>=98.2&&padPark.y+padPark.d<=178.2);a(padPark.z===47);
// Bucket: first clear the tray lip; move 19 mm towards the back; then lift through the centered opening.
const bucket=world(base.bucket),bucketNodes=[bucket,{...bucket,z:13.5},{...bucket,x:7.4,z:13.5},{...bucket,x:7.4,z:97}];
const linerWalls=[b('Liner side left',75.7,1,10.3,.4,35,3),b('Liner side right',93.3,1,10.3,.4,35,3),b('Liner rear',76.1,1,10.3,17.2,.4,3),b('Liner front',76.1,35.6,10.3,17.2,.4,3)].map(world);
const caseParts=[b('Parede posterior',40.8,76.6,0,4,19.8,40),b('Parede frontal',0,76.6,0,1.8,19.8,40),b('Divisor da folha',0,96.4,0,45,1.8,40),...base.dividers.map(world)];
const fixedForBucket=[table,back,lidOpen,padPark,...fixedSeats,...caseParts,...linerWalls,...base.lower.map(world),...base.drinks.map(world),...base.pots.map(world),...base.panels.map(world)];
for(let i=1;i<bucketNodes.length;i++)for(const o of fixedForBucket)a(!hit(sweep(bucketNodes[i-1],bucketNodes[i]),o),'Bucket hits '+o.id+' segment '+i);
const opening=42.8-5,eachGap=(opening-bucket.w)/2;
a(Math.abs(eachGap-2.4)<eps);a(Math.abs(bucketNodes[2].x-5-eachGap)<eps);
// Counterexamples: a thick upholstered lid, and the old 08/10 6-cm model.
const accessComparison=[{name:'Antigo ensaio 6 cm',axis:45,thickness:6},{name:'Assento inteiro 7 cm do modelo',axis:45,thickness:7},{name:'Tampa 2 cm, almofada retirada',axis:44.8,thickness:2}].map(t=>({...t,opening:t.axis-t.thickness-5,totalExtra:t.axis-t.thickness-5-33,perSide:(t.axis-t.thickness-5-33)/2}));
a(accessComparison[1].totalExtra===0);a(accessComparison[2].perSide>accessComparison[0].perSide);
const targets=[0,1,2,2.5,3].map(g=>({extraEachSide:g,requiredOpening:33+2*g,passes:33+2*g<=opening+eps}));
a(targets.find(t=>t.extraEachSide===2).passes);a(!targets.find(t=>t.extraEachSide===2.5).passes);
// Removable shelves: actual cut blanks narrower than the box, retained old pot positions.
const boards=[b('Painel posterior de estudo',.3,.3,24.4,35.6,20.2,1.8),b('Painel frontal de estudo',.3,21,24.4,35.6,17.7,1.8)];
const ledges=boards.flatMap((t,i)=>[b('Faixa de suporte E'+i,0,t.y,23.8,1,t.d,.6),b('Faixa de suporte D'+i,35.2,t.y,23.8,1,t.d,.6)]);
pairs([...boards,...ledges,...base.pots,...base.lower.slice(0,2)]);
for(const pot of base.pots)a(boards.some(t=>pot.x>=t.x&&pot.y>=t.y&&pot.x+pot.w<=t.x+t.w+eps&&pot.y+pot.d<=t.y+t.d+eps),'Unsupported pot base');
const bearingPerSide=1-.3,span=35.2-1;
a(Math.abs(bearingPerSide-.7)<eps);a(Math.abs(span-34.2)<eps);
// Recheck clean-section access using the actual 7 cm upholstered thickness, not the old 6 cm proxy.
const cleanOpen=b('Assento limpo aberto 7 cm',38,1.8,47,7,73,45);
const cleanFixed=[table,back,cleanOpen,...base.dividers.map(world),...ledges.map(world)];
let cleanRemaining=[...base.pots,...boards,...base.lower,...base.drinks];const cleanRoutes=[];
for(const obj of [...base.pots,...boards,...base.lower.slice(0,2)]){
 const start=world(obj),z=obj.id.startsWith('Pote')?36.6:obj.id.startsWith('Painel')?31:obj.id==='Travessas'?21.3:start.z;
 const nodes=[start,{...start,z},{...start,x:8,z},{...start,x:8,z:97}];
 for(let i=1;i<nodes.length;i++)for(const o of [...cleanFixed,...cleanRemaining.filter(t=>t.id!==obj.id).map(world)])a(!hit(sweep(nodes[i-1],nodes[i]),o),obj.id+' clean route / '+o.id);
 cleanRoutes.push({id:obj.id,continuousBoxesClear:true});cleanRemaining=cleanRemaining.filter(t=>t.id!==obj.id);
}
const jar=world(base.drinks[1]),thermal=world(base.drinks[0]);
a(hit(sweep(jar,{...jar,z:41}),cleanOpen),'Negative test: old direct jar lift must fail against 7 cm lid');
const jarNodes=[jar,{...jar,x:jar.x-.8},{...jar,x:jar.x-.8,z:41},{...jar,x:8,z:41},{...jar,x:8,z:97}];
const thermalNodes=[thermal,{...thermal,z:41},{...thermal,x:8,z:41},{...thermal,x:8,z:97}];
for(const [obj,nodes] of [[base.drinks[1],jarNodes],[base.drinks[0],thermalNodes]])for(let i=1;i<nodes.length;i++)for(const o of [...cleanFixed,...[...base.pots,...boards,...base.lower,...base.drinks].filter(t=>t.id!==obj.id).map(world)])a(!hit(sweep(nodes[i-1],nodes[i]),o),'Independent '+obj.id+' / '+o.id);
const cleanAccess={lidThickness:7,potPanelLowerRoutes:cleanRoutes,thermalIndependent:true,jarDirectOldLiftRejected:true,jarNodes,jarAdvanceBeforeLift:.8,jarToThermalAfterAdvance:.2,jarToOpenLidAfterAdvance:.4,jarPhysicalAccessStillUnresolved:true};
// Proposed remedy for the middle compartment too: one separate 36.8-cm cushion, then a 2-cm lid.
const drinksPad=b('Almofada do setor limpo',0,38.9,42,45,36.8,5);
const drinksPadNodes=[drinksPad,{...drinksPad,z:48},{...drinksPad,y:110,z:48},{...drinksPad,y:110,z:47}];
const drinksLidClosed=b('Tampa fina limpa fechada',0,38.9,40,44.8,36.8,2);
for(let i=1;i<drinksPadNodes.length;i++)for(const o of [table,back,drinksLidClosed,b('Assento potes',0,0,40,45,38.9,7),b('Assento restante',0,75.7,40,45,104.3,7)])a(!hit(sweep(drinksPadNodes[i-1],drinksPadNodes[i]),o),'Drinks pad / '+o.id);
const drinksPadPark=drinksPadNodes.at(-1);a(!hit(drinksPadPark,padPark));a(drinksPadPark.y>=98.2&&padPark.y+padPark.d<=178.2);
const drinksOpen=b('Tampa fina limpa aberta',42.8,38.9,42,2,36.8,44.8);
const thinCleanFixed=[table,back,drinksOpen,drinksPadPark,padPark,...base.dividers.map(world)];
const thinDrinkRoutes=[];
for(const obj of base.drinks){const start=world(obj),nodes=[start,{...start,z:41},{...start,x:8,z:41},{...start,x:8,z:97}];for(let i=1;i<nodes.length;i++)for(const o of [...thinCleanFixed,...[...base.pots,...boards,...base.lower,...base.drinks].filter(t=>t.id!==obj.id).map(world)])a(!hit(sweep(nodes[i-1],nodes[i]),o),'Thin middle lid / '+obj.id+' / '+o.id);thinDrinkRoutes.push({id:obj.id,nodes,continuousBoxesClear:true});}
const middleAlternative={cushionNodes:drinksPadNodes,parkedWithBucketCushion:true,independentDrinks:thinDrinkRoutes,jarAdvanceNeeded:0,jarToOpenLid:4.4,dailyThermalAccessRequiresMovingCushion:true,acceptedByUser:true,physicalVerification:false};
const floor={top:8,assumedThickness:1.8,underside:6.2,freeBelowAssembly:3.5,ceiling:40,upperReserve:4,loadPath:'Assento -> paredes/apoios estruturais -> base/piso. Prateleiras removíveis não recebem carga do assento.',supportHeightAvailableBelowFloor:6.2,levelingAndDeflectionUnverified:true};
const sensitivity=[0,.2,.5,1].map(extra=>({unallocatedVerticalLoss:extra,resultingTopReserve:4-extra,passes:4-extra>=3.5-eps}));
a(sensitivity[2].passes&&!sensitivity[3].passes);
const result={date:'2026-10-08',status:'Organização e rotina das almofadas aprovadas; detalhamento construtivo pendente',acceptance:{"date":"2026-10-09","quote":"entendo q funciona sim","scope":"Retirar a almofada do setor das bebidas ou do balde e apoiá-la na ponta do banco antes de abrir a tampa, inclusive no acesso diário à térmica","functionalRoutineAccepted":true,"hardwareSelected":false,"fabricationReleased":false},bench,cleanAccess,middleAlternative,correction:{earlier45WasSeatNotWholeDepth:true,actualModelUpholsteredThickness:7,earlierRouteThickness:6,wrongWholeDepthDescriptionCorrected:true},construction,accessComparison,rotation:{sampleStepDegrees:.1,samples:901,minSampleDistance:minDistance,minAngle,betweenSampleBound:rotationBound,continuousTableDistanceLowerBound:continuousGapLowerBound,backrestGap:.2,hardwareAndSoftEdgesExcluded:true},cushion:{nodes:cushionNodes,continuousBoxesClear:true,parkingOnExistingSeat:true,handBodyWeightUnverified:true},bucket:{nodes:bucketNodes,continuousBoxesClear:true,opening,perSideExtra:eachGap,comparisonTargets:targets,temporaryNearTrayRearClearance:.4,transitionStillNearTableInitially:.5,fullHandleAndHandsUnknown:true},supports:{boards,ledges,bearingPerSide,clearSpan:span,totalVerticalEnvelope:2.4,retentionHardwareNotSelected:true,loadCapacityUnverified:true,sideAssemblyClearance:.3},floor,sensitivity,remaining:['Modelo comercial e desenho do balde incluindo alça/fechos','Mãos, pega, postura e transferência final do balde','Dobradiça e retenção aberta compatíveis com tampa e massa reais','Resistência da tampa de assento e apoios independentes','Dimensionamento do fundo a 8 cm, suporte e nivelamento','Rigidez/carga dos painéis, suporte de 6 mm e retenção removível','Produtos, pilhas e tolerâncias reais; 5 mm extras totais não são garantia']};
fs.writeFileSync(p.join(__dirname,'Detalhe_banco_resultados.json'),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({newOpening:opening,extraPerSide:eachGap,oldModel7cmExtra:0,rotationContinuousLowerGap:+continuousGapLowerBound.toFixed(3),padParkingClear:true,bucketClear:true,shelvesCut:[35.6,20.2,17.7],physicalValidation:false}));
