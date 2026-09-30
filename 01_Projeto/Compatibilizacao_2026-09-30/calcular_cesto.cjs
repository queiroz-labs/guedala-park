// Estudo geométrico documental, cm. Não dimensiona ferragem, estrutura ou carga admissível.
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const rad=a=>a*Math.PI/180,deg=a=>a*180/Math.PI,r=x=>+x.toFixed(5);
const p={eixoY:56,eixoZ:12,angulo:55,cestoL:45,cestoP:25,cestoA:45,pedraP:75,pedraZ:92,pedraE:2,
 gabineteL:59,lateralE:1.8,secao:154,tanque:[21,70,60,90],hidraulica:[0,63,33,70],posteriorY:28,
 base:[0,8,58,9.8],frenteY:63,frenteE:1.8,frenteBaixo:15,frenteTopo:67.1,
 painelBaixo:67.5,painelTopo:89.7,rodapeY:58,rodapeTopo:11,folgaGiro:3,reservaAdicionalPainel:1,bag:[-22.5,2.5,-2.5,42.5],bagL:40,folgaExtracao:2};
const point=(u,v,a)=>[p.eixoY+u*Math.cos(rad(a))+v*Math.sin(rad(a)),p.eixoZ-u*Math.sin(rad(a))+v*Math.cos(rad(a))];
const rectPoints=b=>[[b[0],b[1]],[b[2],b[1]],[b[2],b[3]],[b[0],b[3]]];
const poly=(box,a,shift=0)=>rectPoints(box).map(([u,v])=>point(u,v+shift,a));
const bounds=q=>[Math.min(...q.map(x=>x[0])),Math.min(...q.map(x=>x[1])),Math.max(...q.map(x=>x[0])),Math.max(...q.map(x=>x[1]))];
// SAT convexo: confronta áreas inteiras, incluindo arestas/interiores.
function overlap(A,B){for(const P of [A,B])for(let i=0;i<P.length;i++){const q=P[i],v=P[(i+1)%P.length],axis=[q[1]-v[1],v[0]-q[0]],dot=t=>t[0]*axis[0]+t[1]*axis[1],aa=A.map(dot),bb=B.map(dot);if(Math.max(...aa)<=Math.min(...bb)+1e-9||Math.max(...bb)<=Math.min(...aa)+1e-9)return false;}return true;}
const basket=[-25,0,0,45],front=[p.frenteY-p.frenteE-p.eixoY,p.frenteBaixo-p.eixoZ,p.frenteY-p.eixoY,p.frenteTopo-p.eixoZ];
const upper=[p.frenteY-p.frenteE,p.painelBaixo,p.frenteY,p.painelTopo];
const obstacles={pedra:[0,90,75,92],tanque:p.tanque,hidraulica:p.hidraulica,posterior:[0,0,28,90],base:p.base,painel:upper,rodape:[56.2,0,58,p.rodapeTopo]};
const collision={};let minFloor=Infinity,minFrontY=Infinity,maxBasketZ=-Infinity,maxFrontY=-Infinity,minGapPanel=Infinity;
for(let i=0;i<=5500;i++){const a=i/100,B=poly(basket,a),F=poly(front,a),bb=bounds(B),fb=bounds(F);
 minFloor=Math.min(minFloor,fb[1]);minFrontY=Math.min(minFrontY,fb[0]);maxBasketZ=Math.max(maxBasketZ,bb[3]);maxFrontY=Math.max(maxFrontY,fb[2]);minGapPanel=Math.min(minGapPanel,p.painelBaixo-bb[3]);
 for(const [key,rect]of Object.entries(obstacles)){for(const [label,moving] of [['cesto',B],['frente',F]]){if(overlap(moving,rectPoints(rect)))collision[label+'_'+key]=(collision[label+'_'+key]||0)+1;}}
}
const fullFronts=[{nome:'Frente alta no plano ilustrativo 58',face:58,topo:89.7},{nome:'Frente alta no plano proposto 63',face:63,topo:89.7},{nome:'Frente dividida no plano proposto 63',face:63,topo:p.frenteTopo}].map(x=>{const b=bounds(poly([x.face-1.8-56,3,x.face-56,x.topo-12],55));return{...x,avanco:r(b[2]),saldoSecao:r(154-b[2])};});
// Saco: corpo carregado de teste, não molde/capacidade comercial. Mantém orientação até sair do aro.
const extracao=45-p.bag[1]+p.folgaExtracao,bagEnd=poly(p.bag,55,extracao),pivot=point(p.bag[0],p.bag[1]+extracao,55);
const bagP=p.bag[2]-p.bag[0],bagH=p.bag[3]-p.bag[1];
const rotateBag=a=>rectPoints([0,0,bagP,bagH]).map(([u,v])=>[pivot[0]+u*Math.cos(rad(a))+v*Math.sin(rad(a)),pivot[1]-u*Math.sin(rad(a))+v*Math.cos(rad(a))]);
const upright=bounds(rotateBag(0)),shiftForward=Math.max(0,75+3-upright[0]);
const bagChecks={};let bagMaxY=-Infinity,rotateMaxZ=-Infinity;
function inspectBag(q,phase){bagMaxY=Math.max(bagMaxY,...q.map(x=>x[0]));for(const [key,rect]of Object.entries(obstacles)){if(overlap(q,rectPoints(rect)))bagChecks[phase+'_'+key]=(bagChecks[phase+'_'+key]||0)+1;}
 if(overlap(q,poly(front,55)))bagChecks[phase+'_frenteMovel']=(bagChecks[phase+'_frenteMovel']||0)+1;
 if(phase!=='extrair'&&overlap(q,poly(basket,55)))bagChecks[phase+'_retornoAoCesto']=(bagChecks[phase+'_retornoAoCesto']||0)+1;
 // Bordas do recipiente têm espessura real desconhecida; verificação separada no sistema u/v.
}
for(let i=0;i<=890;i++)inspectBag(poly(p.bag,55,extracao*i/890),'extrair');
for(let i=0;i<=550;i++){const q=rotateBag(55-i/10);rotateMaxZ=Math.max(rotateMaxZ,...q.map(x=>x[1]));inspectBag(q,'endireitar');}
if(shiftForward>0)for(let i=0;i<=100;i++)inspectBag(rotateBag(0).map(([y,z])=>[y+shiftForward*i/100,z]),'avancar');
const openings=[1,1.5,2].map(aro=>({aro,aberturaL:45-2*aro,aberturaP:25-2*aro,corpoL:45-2*aro-2,corpoP:25-2*aro-2,folgaPorLado:1}));
const cargas=[[5,3],[8,3],[12,5]].map(([cesto,frenteM])=>{const u=(-12.5*cesto+(front[0]+front[2])/2*frenteM)/(cesto+frenteM),v=(22.5*cesto+(front[1]+front[3])/2*frenteM)/(cesto+frenteM);return{massaCestoEConteudo:cesto,massaFrente:frenteM,torqueFechadoNm:r(9.81*(cesto+frenteM)*u/100),torqueAbertoNm:r(9.81*(cesto+frenteM)*(u*Math.cos(rad(55))+v*Math.sin(rad(55)))/100),inversaoGraus:r(deg(Math.atan2(-u,v)))};});
const result={data:'2026-09-30',status:'proposta geométrica; sem fabricação ou produto selecionado',premissas:p,frenteLocal:front,
 giro:{colisoes:collision,posicoes:5501,pisoFrente:r(minFloor),frenteYMin:r(minFrontY),cestoZMax:r(maxBasketZ),frenteYMax:r(maxFrontY),saldoSecao:r(154-maxFrontY),folgaPainel:r(minGapPanel),folgaTanquePainel:r(upper[0]-60)},
 comparacaoFrentes:fullFronts,
 saco:{corpo:[40,20,40],extracao:r(extracao),deslocamentoY:r(extracao*Math.sin(rad(55))),deslocamentoZ:r(extracao*Math.cos(rad(55))),pivot:pivot.map(r),yMax:r(bagMaxY),saldoSecao:r(154-bagMaxY),alturaMaxAoEndireitar:r(rotateMaxZ),distanciaPedraAoEndireitar:r(pivot[0]-75),avancoFinal:r(shiftForward),uprightFinal:upright.map((x,i)=>r(x+(i%2===0?shiftForward:0))),colisoes:bagChecks,amostras:1442+(shiftForward>0?101:0)},aberturas:openings,cargas};
const checks=[];const test=(name,fn)=>{fn();checks.push(name);};
test('SAT detecta cruzamento de arestas mesmo sem quinas internas',()=>{assert.ok(overlap(rectPoints([-2,-.5,2,.5]),rectPoints([-.5,-2,.5,2])));assert.ok(!overlap(rectPoints([0,0,1,1]),rectPoints([2,2,3,3])));});
test('Rotação preserva distâncias e reproduz o pico analítico',()=>{assert.ok(Math.abs(Math.hypot(...point(-25,45,55).map((v,i)=>v-[56,12][i]))-Math.hypot(25,45))<1e-9);assert.ok(Math.abs(maxBasketZ-(12+Math.hypot(25,45)))<1e-6);});
test('Conjunto proposto sem interseções com obstáculos modelados em 5501 posições',()=>assert.deepEqual(collision,{}));
test('Saco sai do aro com 2 cm axiais; rotação posterior não retorna ao cesto e fica fora da pedra',()=>{assert.equal(p.bag[1]+extracao,47);assert.ok(pivot[0]>78);assert.deepEqual(bagChecks,{});assert.ok(upright[0]+shiftForward>=78);});
test('Painel superior preserva reserva global de 3 cm mais 1 cm de tolerância de estudo',()=>assert.ok(p.painelBaixo-(12+Math.hypot(25,45))>=4));
test('Retirada estritamente vertical excede a folga traseira do saco em menos de 3 cm',()=>{const maxLift=(p.bag[0]-(-25+1.5))/Math.sin(rad(55));assert.ok(maxLift>1&&maxLift<3);});
result.checks=checks;fs.writeFileSync(path.join(__dirname,'Resultados_cesto.json'),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify(result,null,2));
