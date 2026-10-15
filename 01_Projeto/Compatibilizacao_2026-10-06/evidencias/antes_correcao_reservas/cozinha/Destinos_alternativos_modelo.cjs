const fs=require('fs'),path=require('path');
const src=String.raw`C:\Users\Elias\Documents\PROJETOS\Guedala park\guedala-park\01_Projeto`;
const read=p=>JSON.parse(fs.readFileSync(path.join(src,p),'utf8'));
const clean=read('Compatibilizacao_2026-10-03/Resultados_banco_limpo.json');
const priority=read('Compatibilizacao_2026-10-03/Resultados_bau_saldo.json');
const complete=read('Compatibilizacao_2026-10-03/Resultados_conjunto_armazenamento.json');
const r=x=>Math.round(x*1e6)/1e6,eps=1e-8;
const box=(id,x,y,z,w,d,h)=>({id,x,y,z,w,d,h});
const hit=(a,b)=>['x','y','z'].every((k,i)=>a[k]<b[k]+b[['w','d','h'][i]]-eps&&a[k]+a[['w','d','h'][i]]>b[k]+eps);
const inside=clean.inside,lower=clean.objects.map((a,i)=>({...a,id:'inferior'+i}));
const divider={...clean.partition,id:'divisoria'};
const world=a=>box(a.id,40.8-a.y-a.d,1.8+a.x,10+a.z,a.d,a.w,a.h);
const fixed=[box('assento90',39,1.8,47,6,60,45),box('mesa',-70,15,72,75,150,3),box('cadeira1',-79,18,0,47,44,94),box('cadeira2',-87.5,68,0,47,44,94),box('cadeira3',-79,118,0,47,44,94),world(divider)];
function sweep(a,b,obstacles){const swept={...a};for(const [k,d] of [['x','w'],['y','d'],['z','h']]){swept[k]=Math.min(a[k],b[k]);swept[d]=a[d]+Math.abs(a[k]-b[k]);}return obstacles.filter(o=>hit(swept,o)).map(o=>o.id);}
function trial(kind,t){
 const panelBottom=12.3+.5,panelTop=panelBottom+t,potZ=panelTop+.2;
 // Novas juntas hipoteticas; dois paineis removiveis, nenhum pote na junta.
 const panels=[box('painel_frontal',0,22.5,panelBottom,36.2,16.5,t),box('painel_posterior',0,0,panelBottom,36.2,21.5,t)];
 const pots=[];if(kind==='Ou725'){
  [[.5,1],[18.5,1],[.5,23],[18.5,23]].forEach(([x,y],i)=>pots.push(box('pote'+(i+1),x,y,potZ,17,12,7.5)));
  [2,3].forEach((i,j)=>pots.push(box('pote'+(5+j),pots[i].x,pots[i].y,potZ+7.5+.2,17,12,7.5)));
 }else{
  const dims={Invicta1L:[20.4,15.3,6.9],Luminarc820:[17.9,13.5,6.7],KeepnBox820:[17.9,13.3,6.2]}[kind], [D,W,H]=dims;
  [[.5,.5,W,D],[1.5+W,.5,W,D],[.5,23,D,W]].forEach(([x,y,w,d],i)=>{pots.push(box('pote'+(i+1),x,y,potZ,w,d,H));pots.push(box('pote'+(i+4),x,y,potZ+H+.2,w,d,H));});
 }
 const objects=[...lower,divider,...panels,...pots];const collisions=[];for(let i=0;i<objects.length;i++)for(let j=i+1;j<objects.length;j++)if(hit(objects[i],objects[j]))collisions.push([objects[i].id,objects[j].id]);
 const support=pots.map(a=>({id:a.id,painel:panels.filter(p=>a.x>=p.x-eps&&a.y>=p.y-eps&&a.x+a.w<=p.x+p.w+eps&&a.y+a.d<=p.y+p.d+eps).map(p=>p.id)}));
 const maxTop=Math.max(...pots.map(a=>a.z+a.h)),closedGap=inside[2]-maxTop;
 const order=kind==='Ou725'?['pote5','pote6','pote1','pote2','pote3','pote4']:['pote6','pote4','pote5','pote3','pote1','pote2'];
 let remaining=objects.filter(a=>a.id!=='divisoria');const extraction=[];
 for(const id of [...order,'painel_frontal','painel_posterior']){
  const object=remaining.find(a=>a.id===id),a=world(object),others=remaining.filter(b=>b.id!==id).map(world);
  const elevation=id.startsWith('painel')?31:(kind==='Invicta1L'?39:36);
  const points=[a,{...a,z:elevation},{...a,x:8,z:elevation},{...a,x:8,z:97},{...a,x:-10-a.w/2,y:50-a.d/2,z:97},{...a,x:-10-a.w/2,y:50-a.d/2,z:75}];
  const blocks=new Set();for(let p=0;p<points.length-1;p++){const A=points[p],B=points[p+1];sweep(A,B,[...fixed,...others]).forEach(x=>blocks.add(x));}
  extraction.push({id,waypoints:points,continuousAxisAligned:true,blocked:[...blocks]});remaining=remaining.filter(b=>b.id!==id);
 }
 const lowerOriginalPathsUnchanged=remaining.length===4;
 return {kind,panelThicknessHypothesis:t,panelBottom:r(panelBottom),panelTop:r(panelTop),pad:.2,potZ:r(potZ),panels,pots,lowerPreserved:lower,contained:objects.every(a=>a.x>=0&&a.y>=0&&a.z>=0&&a.x+a.w<=inside[0]+eps&&a.y+a.d<=inside[1]+eps&&a.z+a.h<=inside[2]+eps),support,collisions,maxTop:r(maxTop),closedGap:r(closedGap),passesOldReserve:closedGap>=3.5-eps,shortOldReserve:r(Math.max(0,3.5-closedGap)),extraction,lowerOriginalPathsUnchanged,nominalConditioned:closedGap>eps&&!collisions.length&&support.every(a=>a.painel.length===1)&&extraction.every(a=>!a.blocked.length),limitations:['t e novas juntas nao sao especificacao estrutural','sem passo de nesting: cada pote completo mais.2 entre eles','pega aberta nao certificada pela sobra fechada','carga/retencao/ferragens/massa com comida nao verificadas']};
}
const studies=['Ou725','Invicta1L','Luminarc820','KeepnBox820'].flatMap(k=>[.4,1.8].map(t=>trial(k,t)));
const jar=[9.5,15.5,27],therm=[13.5,15.6,26.3];
const cases=[{zone:'PiaR3',limit:[10.5,23.3,17.6],status:'reserva estreita proposta;nao adotar'},{zone:'PiaR1',limit:[12.8,22.3,22.8],status:'mixer preservado;zero saldo adicional'},{zone:'PiaR2',limit:[5.6,29.5,22.8],status:'tabua carnes candidata preservada'},{zone:'C3_altura',limit:[51.1,31.4,25.8],status:'panos e dez potes aprovados;sem saldo livre'},{zone:'C4_altura_com_reserva',limit:[51.1,31.4,26.5],status:'seis tacas/seis xicaras/seis pires candidatos preservados;nao area livre'}];
const checks=cases.map(c=>({...c,objects:[{id:'jarraSense',dims:jar},{id:'termicaAlfi',dims:therm}].map(a=>({...a,unitFit:[a.dims,[a.dims[1],a.dims[0],a.dims[2]]].some(d=>d.every((n,i)=>n<=c.limit[i]+eps)),heightBeyond:r(a.dims[2]-c.limit[2])}))}));
const out={date:'2026-10-06',units:'cm',status:'estudo novo condicionado;nenhum destino adotado',preservedPriority:{upperRemaining:priority.upperRemaining,bucket:priority.trial.bucket,underLeaf:priority.hypotheticalUnderLeaf,selectionLimits:priority.selectionLimits,vacuum:priority.trial.vacuumComplete,gamesHeight:priority.gameTwoHeight,clean60:clean.inside,cleanStatus:'alternativa compativel com prioridade;nao adotada',noClean94_6:complete.status,noCleanDisplaces:complete.groupsWithoutDestinationInNewBenchOption},studies,jarThermChecks:checks,benchVessels:{leftArea:36.2*39,leftExistingArea:34*22+30*14,jarThermArea:r(jar[0]*jar[1]+therm[0]*therm[1]),leftAreaBeyondIfBoth:r(34*22+30*14+jar[0]*jar[1]+therm[0]*therm[1]-36.2*39),rightArea:22*39,rightMotorAndJarArea:2*18*18,rightSpare:22*39-2*18*18,thermBase:r(13.5*15.6),thermBeyondRightArea:r(13.5*15.6-(22*39-2*18*18)),bucketSideMaximum:r(32.8-25),aboveBucketMaximum:r(30-.3-25),jarsStanding:true},compactThermos:{TTC1500pro:[12.5,18,22.5],THX1500:[12.5,19,23],R3width:10.5,R1occupied:true,destinationResolved:false},wholeTargetGroupResolved:false};
out.priorityNominalChecks={vacuumFitsExistingCell:priority.trial.vacuumComplete.every((n,i)=>n<=priority.selectionLimits.underCell[i]+eps),twoGamesFitsExistingCell:priority.gameTwoHeight<=priority.selectionLimits.underCell[2]+eps,bucketFitsExistingUpperReserve:priority.trial.bucket.every((n,i)=>n<=priority.selectionLimits.upperRemaining[i]+eps),underLeafUnchanged:true,cleanFourLowerEnvelopesUnchanged:true,newOccupationsOutsideClean60:false};
out.bucketJarThermSensitivity={currentUpperSelection:priority.selectionLimits.upperRemaining,jarHeightBeyond:r(27-priority.selectionLimits.upperRemaining[2]),alfiHeightBeyond:r(26.3-priority.selectionLimits.upperRemaining[2]),depthBucket25PlusAlfiMinDepth13_5:38.5,nominalDepth:39,totalDepthLeftForBackGapFront:.5,legacyUsefulDepth:35,shortUsefulDepth:3.5,status:'mesmo sem reserva de altura, alinhamento bruto precisaria reduzir reservas; nao validado'};
out.sources={localRoot:src,localFiles:['Compatibilizacao_2026-10-03/Resultados_banco_limpo.json','Compatibilizacao_2026-10-03/Resultados_bau_saldo.json','Compatibilizacao_2026-10-03/Resultados_conjunto_armazenamento.json'],productQueryDate:'2026-10-06',Luminarc820:'https://www.latabledarc.com/products/boite-de-conservation-rectangulaire-82-cl-pure-box-active',KeepnBox820:'https://www.latabledarc.com/products/boite-de-conservation-rectangulaire-82-cl-keepn-box',Ou725:'https://www.ou.com.br/products/pote-de-vidro-hermetico-ou-725ml-linha-fresh-lock',Invicta1L:'https://www.invictaonline.com.br/kit-com-6-potes-de-vidro-hermetico-1000ml-retangular-invicta/p'};
if(studies.some(s=>s.collisions.length))throw Error('colisao estatica inesperada');
for(const s of studies){if(s.pots.length!==6||!s.contained||s.support.some(a=>a.painel.length!==1)||s.extraction.some(e=>e.blocked.length)||!s.lowerOriginalPathsUnchanged)throw Error('estudo nominal incompleto '+s.kind);}
if(!Object.values(out.priorityNominalChecks).slice(0,5).every(Boolean)||out.priorityNominalChecks.newOccupationsOutsideClean60)throw Error('programa de prioridade nao preservado');
const positive=studies.find(s=>s.kind==='Luminarc820'&&s.panelThicknessHypothesis===1.8);if(!positive.nominalConditioned||positive.closedGap!==1.6||positive.passesOldReserve)throw Error('resultado V5495 incoerente');
fs.writeFileSync(path.join(__dirname,'Destinos_alternativos_modelo.json'),JSON.stringify(out,null,2)+'\n');
console.log(JSON.stringify({studies:studies.map(s=>({kind:s.kind,t:s.panelThicknessHypothesis,contained:s.contained,gap:s.closedGap,oldReserve:s.passesOldReserve,nominalConditioned:s.nominalConditioned,blocked:s.extraction.filter(e=>e.blocked.length).map(e=>({id:e.id,b:e.blocked}))})),wholeTargetGroupResolved:false}));
