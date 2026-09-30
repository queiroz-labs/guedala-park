// Micro/C2: estudo geométrico e fotométrico direto; cm e lm/m úteis após difusor.
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..'),rad=x=>x*Math.PI/180,deg=x=>x*180/Math.PI;
const round=(x,n=3)=>Number(x.toFixed(n));
const p={apoioA:155,apoioP:47,chapa:1.8,B:69.7,C:54.7,microL:46.1,microA:29,microP:35.2,
  traseira:10,perfilDescida:1,perfilB:65.7,perfilC:50.7,reservaExtremidade:1};
const geometria={premissas:p,microS:[(p.B-p.microL)/2,(p.B+p.microL)/2],
  folgaCaixaFechada:(p.B-2*p.chapa-p.microL)/2,folgaApoioAberto:(p.B-p.microL)/2,
  reservaP:p.traseira+p.microP,saldoP:p.apoioP-p.traseira-p.microP,
  avancoApoio:p.apoioP-35,recuoAtePedra:63-p.apoioP,
  baseInferior:p.apoioA-p.chapa,emissor:p.apoioA-p.chapa-p.perfilDescida,
  topoReservaFiltro:92+35+22,folgaPerfilReservaFiltro:p.apoioA-p.chapa-p.perfilDescida-(92+35+22),
  folgaSuperiorEscolhida:194-(p.apoioA+p.microA),deficitSuperior:30-(194-p.apoioA-p.microA),
  apoioSeBaixar20:135,emissorSeBaixar20:135-p.chapa-p.perfilDescida,
  folgaSeBaixar20:135-p.chapa-p.perfilDescida-(92+35+22)};
const cortes=[2.5,5,10].map(passo=>{const B=Math.floor((p.perfilB-2*p.reservaExtremidade)/passo)*passo,C=Math.floor((p.perfilC-2*p.reservaExtremidade)/passo)*passo;return{passo,B,C,total:B+C,fluxo800:(B+C)*8};});
const fonte='03_Referencias/Pesquisas_2026-09-27/EVO_STH21967-30.ies';
const nums=fs.readFileSync(path.join(root,fonte),'utf8').split('TILT=NONE')[1].trim().split(/\s+/).map(Number);
const [lamps,lumens,mult,nv,nh,type,units]=nums;
assert.equal(type,1);assert.equal(units,2);assert.equal(nv,91);assert.equal(nh,3);
const angles=nums.slice(13+nv,13+nv+nh);assert.deepEqual(angles,[0,45,90]);
const rows=Array.from({length:nh},(_,j)=>nums.slice(13+nv+nh+j*nv,13+nv+nh+(j+1)*nv).map(x=>x*mult));
function intensity(theta,phi){if(theta<0||theta>90)return 0;let q=((phi%360)+360)%360;if(q>180)q=360-q;if(q>90)q=180-q;const j=q<=45?0:1,u=(q-angles[j])/45,i=Math.min(89,Math.floor(theta));const row=k=>rows[k][i]+(rows[k][i+1]-rows[k][i])*(theta-i);return row(j)*(1-u)+row(j+1)*u;}
function hit(a,b,box){let lo=0,hi=1;for(let i=0;i<3;i++){const d=b[i]-a[i];if(Math.abs(d)<1e-10){if(a[i]<box[i]||a[i]>box[i+3])return false;continue;}let u=(box[i]-a[i])/d,v=(box[i+3]-a[i])/d;if(u>v)[u,v]=[v,u];lo=Math.max(lo,u);hi=Math.min(hi,v);if(lo>hi)return false;}return hi>1e-6&&lo<1-1e-6;}
// s desde o começo do preparo junto à geladeira; t desde a parede; z desde piso.
const fixos=[[-80.1,0,198.4,0,35,255],[0,0,194,69.7,35,255],
  [69.7,0,153.2,124.4,35,255],[124.4,0,197.6,189.4,35,255],
  [126.9,0,174,186.9,30,191.6],[11.8,10,155,57.9,45.2,184],[0,0,153.2,69.7,47,155]];
const filtro=[5,10,92,21,52,127],air=[31,10,92,57.4,46,121.5];
const lamp=[53.4,109,253.2];
function lightCeiling(point,boxes){if(boxes.some(b=>hit(lamp,point,b)))return 0;const dx=point[0]-lamp[0],dy=point[1]-lamp[1],dz=lamp[2]-point[2],r=Math.hypot(dx,dy,dz);return intensity(deg(Math.atan2(Math.hypot(dx,dy),dz)),deg(Math.atan2(dy,dx)))*dz/r/(r/100)**2;}
function strips(Bt,Ct,BL=62.5,CL=47.5){return[{nome:'B',s0:(69.7-BL)/2,s1:(69.7+BL)/2,t:Bt,z:152.2},{nome:'C',s0:69.7+(54.7-CL)/2,s1:69.7+(54.7+CL)/2,t:Ct,z:152.2}];}
function lineLight(point,lines,boxes,flux=1){let E=0;for(const q of lines){const N=Math.ceil((q.s1-q.s0)*2),f=(q.s1-q.s0)/100*flux/N;for(let i=0;i<N;i++){const source=[q.s0+(i+.5)*(q.s1-q.s0)/N,q.t,q.z];if(boxes.some(b=>hit(source,point,b)))continue;const dx=(source[0]-point[0])/100,dy=(source[1]-point[1])/100,dz=(source[2]-point[2])/100,r2=dx*dx+dy*dy+dz*dz;if(dz>0)E+=f/Math.PI*dz*dz/(r2*r2);}}return E;}
function grid(s0,s1,mode){const nx=Math.ceil((s1-s0)/2.5),ny=20,out=[];for(let i=0;i<nx;i++)for(let j=0;j<ny;j++){const point=[s0+(i+.5)*(s1-s0)/nx,10+(j+.5)*2.5,92];if([filtro,...(mode==='airfryer'?[air]:[])].some(b=>point[0]>=b[0]&&point[0]<=b[3]&&point[1]>=b[1]&&point[1]<=b[4]))continue;out.push(point);}return out;}
function stats(v){const sort=[...v].sort((a,b)=>a-b),mean=v.reduce((a,b)=>a+b,0)/v.length;return{media:mean,min:sort[0],p10:sort[Math.floor((v.length-1)*.1)],max:sort.at(-1),uniformidade:sort[0]/mean,pontos:v.length};}
const comparison=[];
for(const Bt of [30,35,40,42])for(const Ct of [25,30,32]){
 const obj={Bt,Ct,areas:{}};for(const [name,s0,s1]of [['preparo',0,61.9],['preparo_livre',26,61.9],['pia',61.9,126.9]]){const pts=grid(s0,s1,'normal'),person=[(s0+s1)/2-22.5,72,0,(s0+s1)/2+22.5,102,175],boxes=[...fixos,filtro,person];const base=pts.map(q=>lightCeiling(q,boxes)),per=pts.map(q=>lineLight(q,strips(Bt,Ct),boxes));obj.areas[name]={teto:stats(base),com800:stats(base.map((v,i)=>v+800*per[i])),lm_m_para_media500:Math.max(0,(500-stats(base).media)/stats(per).media)};}comparison.push(obj);
}
const chosen=comparison.find(x=>x.Bt===42&&x.Ct===30);
const fluxoProposto=Math.ceil(Math.max(...[chosen.areas.preparo_livre,chosen.areas.pia].map(a=>a.lm_m_para_media500))/100)*100;
const scenarios=[];
for(const mode of ['normal','airfryer'])for(const pessoa of [false,true]){
 const q={modo:mode,pessoa,areas:{}};
 for(const [name,s0,s1]of [['preparo',0,61.9],['preparo_livre',26,61.9],['pia',61.9,126.9]]){
  const pts=grid(s0,s1,mode),person=[(s0+s1)/2-22.5,72,0,(s0+s1)/2+22.5,102,175],boxes=[...fixos,filtro,...(mode==='airfryer'?[air]:[]),...(pessoa?[person]:[])];
  const map=pts.map(point=>({point,teto:lightCeiling(point,boxes),por_lm_m:lineLight(point,strips(42,30),boxes)}));
  q.areas[name]={teto:stats(map.map(v=>v.teto)),com800:stats(map.map(v=>v.teto+800*v.por_lm_m)),comProposto:stats(map.map(v=>v.teto+fluxoProposto*v.por_lm_m)),map};
 }scenarios.push(q);
}
const checks=[];function test(name,fn){fn();checks.push(name);}
test('Vão lateral nominal e tolerância de descentralização',()=>{assert.ok(Math.abs(geometria.folgaCaixaFechada-10)<1e-8);assert.ok(Math.abs(geometria.folgaApoioAberto-11.8)<1e-8);});
test('Sombra física: aumento de luz não atravessa filtro opaco',()=>{const source=[13,42,152.2],target=[13,55,92];assert.ok(hit(source,target,filtro));assert.ok(!hit(source,[40,55,92],filtro));});
test('Linearidade independente da oclusão',()=>{const a=lineLight([40,55,92],strips(42,30),[filtro],500),b=lineLight([40,55,92],strips(42,30),[filtro],1000);assert.ok(Math.abs(2*a-b)<1e-8);});
test('Comprimentos reais nunca excedem perfis menos terminais',()=>{for(const c of cortes){assert.ok(c.B+2<=65.7);assert.ok(c.C+2<=50.7);}});
const result={data:'2026-09-28',estado:'Estudo; mantém escolha de 10 cm superiores, sem validar instalação ME23P.',geometria,cortes,fonteIES:fonte,fluxoProposto,linhasPropostas:strips(42,30),comparison,scenarios,checks,
 metodo:'Fonte pontual IES no teto e linhas lambertianas com integração em passos <=0,5 cm. Paredes/objetos como caixas opacas; contribuição direta inicial no plano a 92 cm. Pontos sobre corpos excluídos. Pia inclui projeção da cuba, não representa seu fundo. Pessoa de 45×30×175 a 72 cm da parede, centrada em cada zona separadamente. Sem reflexões, luz natural, depreciação, ofuscamento ou perfil real. 500 lx médios é alvo comparativo, não norma.'};
fs.writeFileSync(path.join(__dirname,'Resultados_micro_c2.json'),JSON.stringify(result,(k,v)=>typeof v==='number'?round(v,5):v,2)+'\n');
console.log(JSON.stringify({geometria,cortes,fluxoProposto,comparison,scenarios:scenarios.map(q=>({...q,areas:Object.fromEntries(Object.entries(q.areas).map(([k,v])=>[k,{...v,map:undefined}]))})),checks},null,2));
