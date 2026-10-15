const fs=require('fs'),p=require('path'),a=require('assert/strict');
const matrix=JSON.parse(fs.readFileSync(p.join(__dirname,'Matriz_espacos_800ml_termica.json'),'utf8'));
a(matrix); // Matrix compiled before testing destinations; no slot assumed empty.
const rect=(id,x,y,z,w,d,h)=>({id,x,y,z,w,d,h});
const within=(r,b)=>r.x>=b.x&&r.y>=b.y&&r.z>=b.z&&r.x+r.w<=b.x+b.w+1e-8&&r.y+r.d<=b.y+b.d+1e-8&&r.z+r.h<=b.z+b.h+1e-8;
const overlap=(r,s)=>r.x<s.x+s.w-1e-8&&s.x<r.x+r.w-1e-8&&r.y<s.y+s.d-1e-8&&s.y<r.y+r.d-1e-8&&r.z<s.z+s.h-1e-8&&s.z<r.z+r.h-1e-8;
const potStackH=2*4.7+0.2, panelBottom=15.8, supportBudget=0.8, pad=0.2;
const z=panelBottom+supportBudget+pad;
const bank=rect('left',0,0,0,36.2,39,30);
const stacks=[rect('Duralex800_stack1',1,1,z,14.5,19,potStackH),rect('Duralex800_stack2',16.5,1,z,14.5,19,potStackH),rect('Duralex800_stack3',1,21,z,19,14.5,potStackH)];
a(stacks.every(r=>within(r,bank)));
a(stacks.every((r,i)=>stacks.slice(i+1).every(s=>!overlap(r,s))));
a.equal(panelBottom-12.3,3.5); a(Math.abs(30-(z+potStackH)-3.6)<1e-8);
const lower=[rect('batedeira',3.1,1,.3,30,14,12),rect('travessas',1.1,16,.3,34,22,10)];
a(lower.every(r=>stacks.every(s=>!overlap(r,s))));
const bucketBay=rect('selection',0,0,0,30.8,35,26.2);
const candidates=[rect('TTS8L',0,0,.2,16,33,25),rect('TTC1500',17,17,.2,12.5,18,22.5),rect('Vilde1.5L',17,0,.2,11.5,16,23)];
a(candidates.every(r=>within(r,bucketBay))); a(candidates.every((r,i)=>candidates.slice(i+1).every(s=>!overlap(r,s))));
// New bay is a requirement envelope, not a location or approved cabinet.
const newBay=rect('newUsefulBay',0,0,0,59,37,27);
const combined=[rect('820stack1',1,1,.4,13.5,17.9,13.6),rect('820stack2',15.5,1,.4,13.5,17.9,13.6),rect('820stack3',1,19.9,.4,17.9,13.5,13.6),rect('Vilde1.5L',31.8,1,.4,11.5,16,23),rect('TTC1.5L',44.3,1,.4,12.5,18,22.5)];
a(combined.every(r=>within(r,newBay)));a(combined.every((r,i)=>combined.slice(i+1).every(s=>!overlap(r,s))));
a(combined.every(r=>newBay.h-r.z-r.h>=3.5));
const result={date:'2026-10-06',units:'cm',matrixCompiledBeforeTests:true,currentCompleteSolution:false,universalImpossibilityProven:false,
 bank800:{stacks,belowClearance:3.5,aboveClearance:3.6,totalSupportBudget:0.8,maxTotalSupportBudget:0.9,old1_8SupportRequiredHeight:30.9,nominalBodiesContained:true,priorVerticalClearancesPreserved:true,structureSelected:false,closedStackHeightAssumed:9.6,handRemovalValidated:false,completeProgrammeValidated:false},
 thermalBucket:{candidates,bay:bucketBay,nominalBodiesContained:true,bucketReplacementApproved:false,existingBucketCapacityUnknown:true,accessValidated:false,jarIncluded:true,thermalInFront:true,depthSpare:0,additionalSideBudget:1.3},
 conflicts:{oldBucketAndTTC:{requiredSeparateWidthOrDepth:38.5,bayWidth:30.8,bayDepth:35},R1:{mixerFootprint:192.42,thermalFootprint:225,sum:417.42,availableArea:285.44},R3:{bay:[10.5,23.3,17.6],Vilde:[11.5,16,23],TTC:[12.5,18,22.5]},jarAbovePanel:{height:23,potBase:z,requiredWithReserve:z+23+3.5,available:30}},
 additionalClosedBay:{bay:newBay,items:combined,nominalContained:true,potModel820ReferenceOnly:true,locationMeasured:false,withdrawalValidated:false,programmeDisplacementAllowed:false,decisionAdopted:false}};
fs.writeFileSync(p.join(__dirname,'Conjunto_800ml_guardado.json'),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({bank800NominalWithPreservedClearances:true,supportAssemblyMax:0.9,bucketThermalNominal:true,wholeEightExistingProgrammeResolved:false,newBayUseful:[59,37,27]}));
