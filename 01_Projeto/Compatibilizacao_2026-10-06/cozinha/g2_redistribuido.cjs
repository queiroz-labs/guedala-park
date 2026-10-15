const fs=require('fs'),path=require('path');
const eps=1e-8,r=n=>Math.round(n*1e6)/1e6;
const mods={longo:[19.2,45.2],largo:[30.4,45.2]};
// Coordenadas locais x/y/z; z=0 superficie do fundo da gaveta.
// z=.4 reserva o fundo hipotetico do organizador; .2 separa pilhas.
const items=[
{id:'concha',sku:'25157100',mod:'longo',p:[.5,.5,.4],d:[8.3,29.6,5.8]},
{id:'lisa',sku:'25855160',mod:'longo',p:[.5,.5,6.4],d:[5,27.3,1.65],above:'concha'},
{id:'escumadeira',sku:'25158100',mod:'longo',p:[9.6,.5,.4],d:[8.9,29.9,6.2]},
{id:'vazada',sku:'20352270',mod:'longo',p:[9.6,.5,6.8],d:[7,28.3,2],above:'escumadeira'},
{id:'frigideira',sku:'20260720',mod:'largo',p:[.5,.5,.4],d:[21,35.3,9.7]},
{id:'citrico',sku:'25609100',mod:'largo',p:[22.9,.5,.4],d:[6.8,20.5,3.5],condition:'posicao_fechada_nao_comprovada'},
{id:'alho',sku:'25601100',mod:'largo',p:[22.9,22,.4],d:[4.7,16,4.7],condition:'gabarito_conservador;fechado_nao_comprovado'},
{id:'peneira',sku:'12812270',mod:'largo',p:[.5,37.2,.4],d:[20.5,7,3]},
{id:'ralador',sku:'747375',mod:'largo',p:[.5,37.2,3.6],d:[20.32,3.175,.635],above:'peneira',condition:'envelope_com_capa_nao_comprovado'}
];
const hit=(a,b)=>a.mod===b.mod && [0,1,2].every(k=>a.p[k]<b.p[k]+b.d[k]-eps && a.p[k]+a.d[k]>b.p[k]+eps);
const collisions=[];for(let i=0;i<items.length;i++)for(let j=i+1;j<items.length;j++)if(hit(items[i],items[j]))collisions.push([items[i].id,items[j].id]);
const bounds=items.map(a=>({id:a.id,contido:a.p[0]>=0&&a.p[1]>=0&&a.p[0]+a.d[0]<=mods[a.mod][0]+eps&&a.p[1]+a.d[1]<=mods[a.mod][1]+eps,extremos:a.p.map((n,i)=>r(n+a.d[i])),H_com_margem:r(a.p[2]+a.d[2]+1)}));
const H=r(Math.max(...bounds.map(x=>x.H_com_margem)));
const guides=[{id:'guia_longo',mod:'longo',p:[9,.5],d:[.4,30.4]},{id:'guia_lateral_largo',mod:'largo',p:[22,.5],d:[.4,44.2]}];
const guideHits=[];for(const g of guides)for(const a of items)if(g.mod===a.mod&&[0,1].every(k=>g.p[k]<a.p[k]+a.d[k]-eps&&g.p[k]+g.d[k]>a.p[k]+eps))guideHits.push([g.id,a.id]);
function sweep(id,remaining,mode){const a=items.find(x=>x.id===id);const blockers=new Set();if(remaining.some(b=>b.above===id))remaining.filter(b=>b.above===id).forEach(b=>blockers.add(b.id+'(apoio)'));
// Varredura continua exata para translacao retilinea monotona de AABB.
const swept={...a,p:[...a.p],d:[...a.d]};swept.d[mode==='frontal'?1:2]+=mode==='frontal'?(mods[a.mod][1]+a.d[1]):15;
for(const other of remaining)if(other.id!==id&&hit(swept,other))blockers.add(other.id);
for(let n=0;n<=400;n++){const b={...a,p:[...a.p]};if(mode==='frontal')b.p[1]+=n/400*(mods[a.mod][1]+a.d[1]);else b.p[2]+=n/400*15;
for(const other of remaining)if(other.id!==id&&hit(b,other))blockers.add(other.id);}
return [...blockers];}
const initial=items.map(a=>({id:a.id,frontal_bloqueadores:sweep(a.id,items,'frontal'),vertical_bloqueadores:sweep(a.id,items,'vertical')}));
const order=['lisa','vazada','ralador','peneira','alho','citrico','concha','escumadeira','frigideira'];let remaining=[...items];
const extraction=order.map(id=>{const blockers=sweep(id,remaining,'frontal');remaining=remaining.filter(a=>a.id!==id);return{id,modo:'frontal',varredura_continua_AABB:true,amostras_adicionais:401,bloqueadores:blockers};});
const out={data:'2026-10-06',escopo:'ensaio nominal de nove envelopes;nao fabricacao nem prova de guarda completa',modulos:mods,items,bounds,colisoes_estaticas:collisions,guias:guides,colisoes_guias_em_planta:guideHits,H_min_nominal_com_margem:H,testes_H:[8,10,11.1,12].map(h=>({H:h,passa:h>=H-eps})),retiradas_iniciais:initial,sequencia_frontal:extraction,nominal_pass:bounds.every(x=>x.contido)&&!collisions.length&&!guideHits.length&&extraction.every(x=>!x.bloqueadores.length),limites_reais:['H medido e gaveta aberta/curso ferragens','envelopes fechados dos dois espremedores','ralador com capa','estabilidade/apoio/protecao das tres pilhas','pega e montagem;guias sao hipoteticas']};
if(items.length!==9||new Set(items.map(x=>x.id)).size!==9)throw Error('programa incompleto');
if(!out.nominal_pass)throw Error(JSON.stringify(out));
fs.writeFileSync(path.join(__dirname,'g2_redistribuido.json'),JSON.stringify(out,null,2)+'\n');console.log(JSON.stringify({n:items.length,H,colisoes:collisions.length,sequencia_pass:extraction.every(x=>!x.bloqueadores.length),nominal_pass:out.nominal_pass}));
