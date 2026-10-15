const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const box = (id,x,y,z,w,d,h) => ({id,x,y,z,w,d,h});
const eps=1e-7;
const hit=(a,b)=>a.x<b.x+b.w-eps&&b.x<a.x+a.w-eps&&a.y<b.y+b.d-eps&&b.y<a.y+a.d-eps&&a.z<b.z+b.h-eps&&b.z<a.z+a.h-eps;
const contains=(a,b)=>b.x>=a.x-eps&&b.y>=a.y-eps&&b.z>=a.z-eps&&b.x+b.w<=a.x+a.w+eps&&b.y+b.d<=a.y+a.d+eps&&b.z+b.h<=a.z+a.h+eps;
const noHits=xs=>xs.forEach((a,i)=>xs.slice(i+1).forEach(b=>assert(!hit(a,b),a.id+' / '+b.id)));
const swept=(a,b)=>{
  assert([a.x!==b.x,a.y!==b.y,a.z!==b.z].filter(Boolean).length<=1,'Only axis-aligned translations');
  return box(a.id,Math.min(a.x,b.x),Math.min(a.y,b.y),Math.min(a.z,b.z),a.w+Math.abs(b.x-a.x),a.d+Math.abs(b.y-a.y),a.h+Math.abs(b.z-a.z));
};
// x: length from the inner left side; y: back to front; z: finished-floor elevation.
const section=[
  box('Potes, travessas e batedeira',0,0,8,36.2,39,32),
  box('Liquidificador e bebidas',38,0,10,35,39,30),
  box('Balde',74.8,0,10,19.8,39,30)
];
const dividers=[box('Divisória limpa',36.2,0,8,1.8,39,32),box('Separação do balde',73,0,8,1.8,39,32)];
assert(Math.abs(section[2].x+section[2].w-94.6)<eps);
assert(Math.abs(1.8+94.6+1.8-98.2)<eps); // Original leaf niche starts at global bench 98.2.
const lower=[box('Travessas',1.1,16,8.3,34,22,10),box('Batedeira',3.1,1,8.3,30,14,12),box('Motor',39,1,10.3,18,18,20),box('Jarra do liquidificador',39,20,10.3,18,18,24)];
const panels=[box('Apoio frontal',0,21,23.8,36.2,18,2.4),box('Apoio posterior',0,0,23.8,36.2,20.5,2.4)];
// 24 mm is a complete construction envelope, not a proven material or load rating.
const footprints=[{x:1,y:1,w:14.5,d:19},{x:16.5,y:1,w:14.5,d:19},{x:8.6,y:22,w:19,d:14.5}];
const pots=footprints.flatMap((p,i)=>[box('Pote '+(2*i+1),p.x,p.y,31.3,p.w,p.d,4.7),box('Pote '+(2*i+2),p.x,p.y,26.4,p.w,p.d,4.7)]);
const drinks=[box('Térmica vazia e seca',58.5,19.4,10.3,13.0175,16.51,24.765),box('Jarra 1,5 L',59.25,2.4,10.3,11.5,16,23)];
const bucket=box('Balde 8 L',76.7,2.3,10.3,16,33,25);
const tray={outer:box('Contenção removível',75.7,1,10,18,35,3.3),inside:box('Interior da contenção',76.1,1.4,10.3,17.2,34.2,3)};
const trayWalls=[box('Fundo da contenção',75.7,1,10,18,35,.3),box('Lateral esquerda da contenção',75.7,1,10.3,.4,35,3),box('Lateral direita da contenção',93.3,1,10.3,.4,35,3),box('Traseira da contenção',76.1,1,10.3,17.2,.4,3),box('Frente da contenção',76.1,35.6,10.3,17.2,.4,3)];
const stored=[...lower,...pots,...panels,...drinks,bucket,...dividers,...trayWalls];
noHits(stored);
for(const b of [...pots,...panels,...lower.slice(0,2)])assert(contains(section[0],b),b.id);
for(const b of [...lower.slice(2),...drinks])assert(contains(section[1],b),b.id);
assert(contains(section[2],bucket));assert(contains(section[2],tray.outer));
assert(bucket.x>=tray.inside.x&&bucket.x+bucket.w<=tray.inside.x+tray.inside.w);
assert(bucket.y>=tray.inside.y&&bucket.y+bucket.d<=tray.inside.y+tray.inside.d);
for(const p of pots)assert(panels.some(s=>p.x>=s.x&&p.x+p.w<=s.x+s.w&&p.y>=s.y&&p.y+p.d<=s.y+s.d));
const below=panels[0].z-(lower[1].z+lower[1].h),above=40-(pots[0].z+pots[0].h);
assert(Math.abs(below-3.5)<eps);assert(Math.abs(above-4)<eps);
const assemblyMax=32-15.8-.2-2*4.7-.2-3.5;
assert(Math.abs(assemblyMax-2.9)<eps);
// Static parking: six separate pots, two EMPTY panels and both lower groups.
// Table-local coordinates; turning empty panels occurs above the table, not proved as a route.
const parking=[...Array.from({length:6},(_,i)=>box('Pote estacionado '+(i+1),2+(i%2)*20,2+Math.floor(i/2)*15.5,0,19,14.5,4.7)),box('Apoio posterior estacionado',44,2,0,20.5,36.2,2.4),box('Apoio frontal estacionado',44,40,0,18,36.2,2.4),box('Travessas estacionadas',2,51,0,34,22,10),box('Batedeira estacionada',2,77,0,30,14,12)];
noHits(parking);
for(const b of parking)assert(contains(box('Área de apoio',0,0,0,67,95,50),b));
assert(67<=75&&95<=150);
// Transform to original room coordinates. Tests use the IDEAL open lid and original table/chairs.
const world=b=>box(b.id,40.8-b.y-b.d,1.8+b.x,b.z,b.d,b.w,b.h);
const obstacles=[box('Assento aberto ideal',39,1.8,47,6,94.6,45),box('Mesa',-70,15,72,75,150,3),box('Cadeira 1',-79,18,0,47,44,94),box('Cadeira 2',-87.5,68,0,47,44,94),box('Cadeira 3',-79,118,0,47,44,94),...dividers.map(world),...trayWalls.map(world)];
let remain=[...pots,...panels,...lower,...drinks,bucket];
const routes=[];
for(const b of [...pots,...panels,...lower.slice(0,2),...drinks,bucket]){
  const start=world(b);
  const elevation=b.id.startsWith('Pote')?36.6:b.id.startsWith('Apoio')?31:b.id==='Travessas'?21.3:b.id==='Batedeira'?start.z:41;
  const exitX=b.id==='Balde 8 L'?start.x:8;
  const nodes=[start,{...start,z:elevation},{...start,x:exitX,z:elevation},{...start,x:exitX,z:97}];
  const others=remain.filter(t=>t.id!==b.id).map(world);
  for(let j=1;j<nodes.length;j++)for(const obstacle of [...obstacles,...others])assert(!hit(swept(nodes[j-1],nodes[j]),obstacle),b.id+' hits '+obstacle.id);
  routes.push({id:b.id,nodes,objectOnlyExtractionClear:true,transferToParkingAndHumanAccessValidated:false});
  remain=remain.filter(t=>t.id!==b.id);
}
// Drinks must be accessible independently, without removal of pots or blender.
for(const b of drinks){const start=world(b),lift={...start,z:41},front={...lift,x:8},up={...front,z:97};for(const [a,c] of [[start,lift],[lift,front],[front,up]])for(const o of [...obstacles,...stored.filter(t=>t.id!==b.id&&!t.id.startsWith('Divisória')&&!t.id.startsWith('Separação')&&!trayWalls.includes(t)).map(world)])assert(!hit(swept(a,c),o),'Independent drinks: '+b.id+' / '+o.id);}
const produceBins=[box('Batatas',.4,.4,.4,17.2,16,13.6),box('Cebolas',.4,16.8,.4,10,12.8,13.6),box('Alho',10.8,16.8,.4,6.8,12.8,13.6)];
noHits(produceBins);produceBins.forEach(b=>assert(contains(box('Base da fruteira',0,0,0,18,30,16),b)));
const produce={userQuantity:'Poucas unidades; sem quantidade exata',status:'Direção funcional aceita em 08/10: fruteira com base ventilada. Dimensões são de estudo, sem produto ou fabricação aprovados.',location:'Base ventilada da fruteira sobre a mesa, reaproveitando o destino funcional da fruteira, sem afirmar mesma dimensão do objeto existente',outside:[18,30,16],fruitTrayOutside:[18,30,5.4],totalNominalHeight:21.4,bins:produceBins,foodCapacityInUnitsOrKg:null,unverified:['Dimensões/quantidade dos alimentos','Ventilação e material','Volume de frutas','Posição durante refeições e extensão','Lugar temporário quando a mesa servir ao banco']};
const result={date:'2026-10-08',units:'cm',status:'Organização funcional aprovada em 08/10/2026; execução condicionada às verificações técnicas',approval:{date:'2026-10-08',quote:'ok, aprovado',scope:'Organização da cozinha e do banco apresentada na prancha, incluindo a fruteira com base ventilada',functionalLayoutApproved:true,executiveDimensionsValidated:false,fabricationReleased:false},newUserFacts:{thermalStored:'Vazia e seca após o uso',produceStock:'Poucas unidades'},outsideBench:[180,55,47],seatDepth:45,routeModel:{lidThickness:6,status:"Ensaio inicial histórico; ver Detalhe_banco_resultados.json para revisão com assento real de 7 cm e alternativa de tampas finas"},section,dividers,pots,panels,lower,drinks,bucket,tray,leaf:{unchangedStart:98.2,unchangedEnd:178.2,niche:[80,35,7],underCells:[39.1,39,20.2],selectionEach:[37.1,35,16.4],vacuumAndGamesStillHypothetical:true},clearances:{below,above,assemblyMax,assemblyBudget:2.4,positiveExtraAboveRequired:.5,drinkSideToBucketPartition:73-(58.5+13.0175),cleanFloor:8,oldFloor:10,assumedFloorThickness:1.8,underCleanFloor:6.2},parking:{area:[67,95],table:[75,150],items:parking,staticOnly:true,tableMustBeCleared:true},routes,produce,limitations:['Lower floor at 8 instead of 10 is a NEW construction hypothesis; underside 6.2 cm only if floor is 18 mm. No existing support or plinth may be cut by inference.','Support 24 mm is the complete construction envelope. Strength, retention, hinges and loads not dimensioned.','Actual product tolerances, handles and double-stack dimensions remain unknown. Existing product references are not new purchasing recommendations.','Separate clean/bucket lids and full-height partition are requirements; hinges, seals, access and spills not validated by these boxes.','Static table parking does not prove hand/body access, panel rotation or transfer trajectory.','Stock, G3 packages, C4 cups/glasses, mixer accessories, games, cycling and bags remain unquantified or without final physical fit.']};
fs.writeFileSync(path.join(__dirname,'Armazenamento_resultados.json'),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({storedNoCollisions:true,extractions:routes.length,independentDrinks:true,above,below,assemblyBudgetMm:24,assemblyMaxMm:Math.round(assemblyMax*10),parkingAllItems:true,unchangedLeaf:true,physicalValidation:false}));
