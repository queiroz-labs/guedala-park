// Reproduzir: node 01_Projeto/Compatibilizacao_2026-09-28/calcular.cjs
// Unidades geométricas: cm. Resultados são estudos, não levantamento/fabricação.
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const root = path.resolve(__dirname, '../..');
const round = (x, n = 3) => Number(x.toFixed(n));
const rad = x => x * Math.PI / 180;
const deg = x => x * 180 / Math.PI;
const origin = {
  cotas: '01_Projeto/Medidas/Dados_das_medidas_R00.json',
  aparelhos: '01_Projeto/Cozinha/Aparelhos_compatibilizacao_R03_2026-09-27.md',
  bancada: '01_Projeto/Cozinha/Detalhamento_dimensional_R00.md',
  gavetas: '01_Projeto/Cozinha/Interior_gavetas_2026-09-25.md',
  torre: '01_Projeto/Cozinha/Torres_retrateis_avaliacao_2026-09-27.md',
  cesto: '01_Projeto/Lavanderia/Tanque_cesto_compatibilizacao_R08.md',
  mesa: '01_Projeto/Sala_e_jantar/Mesa_circulacao_entrada_2026-09-23.md',
  escritorio: '01_Projeto/Escritorio/Sofa_e_porta_R11.md',
  fotometria: '03_Referencias/Pesquisas_2026-09-27/EVO_STH21967-30.ies',
  cena: '01_Projeto/Estudo_interativo/src/app.js'
};
for (const f of Object.values(origin)) assert.ok(fs.existsSync(path.join(root, f)), f);
const cotas = JSON.parse(fs.readFileSync(path.join(root, origin.cotas), 'utf8')).cotas_oficiais_m;
const kitchen = {
  comprimento: cotas.cozinha_trecho_longitudinal * 100,
  largura: cotas.cozinha_transversal * 100,
  modulos: [60, 65, 61.9, 80.1, 85],
  pedra: 63,
  soma: 60 + 65 + 61.9 + 80.1 + 85,
  passagem_pedra: 155 - 63,
  passagem_geladeira: 155 - 84.75,
  saldo_instalacao_longitudinal: 352 - (60 + 65 + 61.9 + 80.1 + 85),
  pia_margem_lateral_envelope: (65 - 43) / 2,
  preparo: {
    coordenadas: 's=0 na ponta do gaveteiro junto à geladeira; t=0 na parede; altura desde o piso',
    filtro: {s: [5,21], t: [10,52], h: [92,127]},
    airfryer: {s: [31,57.4], t: [10,46], h: [92,121.5]},
    cuba: {s: [72.9,115.9], largura_externa: 43},
    vao_compartilhado_entre_corpos: 10,
    limite_lateral_reserva_airfryer: 67.4,
    avanco_reserva_sobre_modulo_pia: 67.4 - 61.9,
    reserva_ate_envelope_cuba: 72.9 - 67.4,
    modelo_r09_gap_corpos: 552 - (520 + 26.4),
    alerta: 'Vão geométrico compartilhado, sem somar folgas adjacentes duas vezes. Água, calor, cabo e retirada da gaveta da air fryer continuam por validar. Escorredor guardado durante esta cena.'
  },
  forno: [4,5,6,7,8].map(d => ({descida_cooktop:d, topo_maximo:72-d, borda_inferior_maxima:11-d})),
  torre: [5,7,9,12].map(faixa => ({faixa_traseira:faixa, diametro_furo:6.5, reserva_geometrica_por_lado:1, saldo:faixa-6.5-2})),
  gaveta_encurtar_50_para_45: {util_atual:[52.7,47], util_alternativo:[52.7,42], perda_area_percentual:100*5/47, aplicada:false},
  temperos: [[6,4],[6,3],[5,4]].map(([nx,ny])=>({quantidade:nx*ny, colunas:nx, filas:ny, envelope_frasco:[(27.7-1-(nx-1)*.2)/nx,(19-1-(ny-1)*.2)/ny], hipotese:'margem externa 0,5 cm e divisórias 0,2 cm; dimensões externas de tampa/corpo'}))
};
const basket = (axis=56, counter=75, angle=55) => {
  const a=rad(angle), back=axis-25*Math.cos(a)+45*Math.sin(a), front=axis+45*Math.sin(a);
  return {eixo:axis,pedra:counter,angulo:angle,boca_traseira:back,boca_dianteira:front,
    boca_fora_pedra:back-counter,saldo_apos_reserva_3:back-counter-3,passagem_restante:154-front};
};
const cesto = {
  nominal:basket(),
  angulo_minimo_boca_3cm:deg(Math.atan2(25,45)+Math.asin((75+3-56)/Math.hypot(25,45))),
  sensibilidades:[basket(56,75,54),basket(56,75,55),basket(56,76,55),basket(55,75,55),basket(56,75,56)],
  largura_interna:59-3.6, reserva_lateral_total:59-3.6-45,
  raio:Math.hypot(25,45),
  altura_maxima_giro:12+Math.hypot(25,45),
  altura_maxima_faixa_y_ate36:12+Math.sqrt(25**2+45**2-(56-36)**2),
  solucao:'Preservar eixo/curso nominais no estudo e especificar verificação da boca com frente real. Não mover eixo sem recalcular hidráulica e ferragem.'
};
const office = [
  [220,75,140,2,3], [220,75,141,2,3], [218,75,140,2,3],
  [220,80,140,2,3], [218,75,141,2,3]
].map(([eixo,folha,largura,recuo_lateral,recuo_fundo])=>({eixo,folha,largura,recuo_lateral,recuo_fundo,
  folga_setor_ideal:Math.hypot(eixo-largura-recuo_lateral,recuo_fundo)-folha}));
const table = [12,16,20,24].map(coluna=>({diametro_coluna:coluna,insercao:37.5-coluna/2-2,
  projecao_cadeira:47-(37.5-coluna/2-2),passagem_nominal:120-(47-(37.5-coluna/2-2))}));
const quarto = {nominal:295-20-160-60-1, parede_2cm_menor:293-20-160-60-1,
  porta_50cm_aberta:54-50, porta_40cm_aberta:54-40, observacao:'Apenas subtração dos envelopes; não escolhe portas nem comprova uso por pessoa.'};

// Fotometria tipo C (tipo 1 no LM-63), interpolação bilinear e simetria de quadrantes.
// Nenhum acesso à rede. Fonte pontual equivalente; não inclui reflexões/manutenção.
const ies = fs.readFileSync(path.join(root, origin.fotometria),'utf8');
assert.ok(ies.includes('TILT=NONE'));
const nums=ies.split('TILT=NONE')[1].trim().split(/\s+/).map(Number);
const [lamps,lumens,mult,nv,nh,type,units,w,l,h,ballast,future,watts] = nums;
assert.equal(type,1); assert.equal(units,2); assert.equal(nv,91); assert.equal(nh,3);
const va=nums.slice(13,13+nv), ha=nums.slice(13+nv,13+nv+nh);
const values=Array.from({length:nh},(_,j)=>nums.slice(13+nv+nh+j*nv,13+nv+nh+(j+1)*nv).map(v=>v*mult));
assert.equal(nums.length,13+nv+nh+nv*nh); assert.deepEqual(ha,[0,45,90]);
function sampleRow(row,theta){
  if(theta<0||theta>90)return 0;
  const i=Math.min(89,Math.floor(theta));return row[i]+(row[i+1]-row[i])*(theta-i);
}
function intensity(theta,phi){
  let p=((phi%360)+360)%360; if(p>180)p=360-p;if(p>90)p=180-p;
  const j=p<=45?0:1, q=(p-ha[j])/45;
  return sampleRow(values[j],theta)*(1-q)+sampleRow(values[j+1],theta)*q;
}
function intersects(a,b,box){
  let lo=0,hi=1;
  for(let i=0;i<3;i++){
    const d=b[i]-a[i];
    if(Math.abs(d)<1e-10){if(a[i]<box[i]||a[i]>box[i+3])return false;continue;}
    let t0=(box[i]-a[i])/d,t1=(box[i+3]-a[i])/d;if(t0>t1)[t0,t1]=[t1,t0];
    lo=Math.max(lo,t0);hi=Math.min(hi,t1);if(lo>hi)return false;
  }
  return hi>1e-6&&lo<1-1e-6;
}
// x longitudinal desde a cocção, y desde a parede, z altura.
const obstacles=[
  {nome:'D',box:[-2.5,0,197.6,62.5,35,255]},
  {nome:'C',box:[62.5,0,155,117.2,35,255]},
  {nome:'B',box:[117.2,0,194,186.9,35,255]},
  {nome:'A',box:[186.9,0,198.4,267,35,255]},
  {nome:'ME23P',box:[128.5,10,155,174.6,45.2,184]},
  {nome:'Suggar',box:[0,0,174,60,30,191.6]}
];
function illuminance(point,lamp,shadows=true,orientation=0){
  if(shadows&&obstacles.some(o=>intersects(lamp,point,o.box)))return 0;
  const dx=point[0]-lamp[0],dy=point[1]-lamp[1],dz=lamp[2]-point[2];
  if(dz<=0)return 0;
  const r=Math.hypot(dx,dy,dz),theta=deg(Math.atan2(Math.hypot(dx,dy),dz));
  return intensity(theta,deg(Math.atan2(dy,dx))-orientation)*(dz/r)/(r/100)**2;
}
const grid=(x0,x1,y0,y1,z,nx,ny)=>Array.from({length:nx*ny},(_,i)=>[x0+(Math.floor(i/ny)+.5)*(x1-x0)/nx,y0+(i%ny+.5)*(y1-y0)/ny,z]);
const stats = vals => ({min:Math.min(...vals),media:vals.reduce((a,b)=>a+b,0)/vals.length,max:Math.max(...vals),pontos:vals.length,sombreados:vals.filter(v=>v===0).length});
const grids={preparo:grid(126.9,186.9,10,60,92,12,10),pia:grid(60,125,10,60,92,13,10),circulacao:grid(0,267,95,150,0,27,11)};
const light={fonte:origin.fotometria,lumens_ies:lumens,watts_ies:watts,
  dimensoes_luminosas_ies_m:[w,l,h],corpo_ficha_cm:[41,41,3.8],lampada_cm:[133.5,109,253.2],
  metodo:'E=I(theta,phi)*cos(theta)/r²; modelo pontual direto inicial, sem luz natural, reflexões, fator de manutenção, pessoa, purificador e utensílios. Aéreos tratados como envelopes opacos; sombras conservadoras. Não equivale a lux instalados ou a conformidade normativa.',
  stats:{},sensibilidade_teto:[],grids:{},obstacles};
for(const [name,points] of Object.entries(grids)){
  const direct=points.map(p=>illuminance(p,light.lampada_cm,false));
  const shaded=points.map(p=>illuminance(p,light.lampada_cm,true));
  light.stats[name]={sem_obstaculos:stats(direct),com_envelopes:stats(shaded),rotacao90:stats(points.map(p=>illuminance(p,light.lampada_cm,true,90)))};
  light.grids[name]=points.map((p,i)=>({p,E:shaded[i],E_sem_obstaculos:direct[i]}));
}
for(const teto of [247,252,257]){
  const lamp=[133.5,109,teto-3.8];
  light.sensibilidade_teto.push({teto,nota:'Só altera fonte; não redimensiona armários. Variação matemática, não cenário construtivo completo.',preparo_sem_obstaculos:stats(grids.preparo.map(p=>illuminance(p,lamp,false)))});
}
// Complemento de bancada: fonte linear ideal lambertiana, fluxo JÁ após difusor.
// C: 54,7 - 4 = 50,7 cm; B: 69,7 - 4 = 65,7 cm. Recuos de 2 cm nas pontas são hipótese.
const strips=[{nome:'C',x0:64.5,x1:115.2,y:30,z:152.2},{nome:'B',x0:119.2,x1:184.9,y:35,z:152.2}];
function linearLight(point,lmPerM){
  let E=0;
  for(const strip of strips){
    const n=Math.ceil((strip.x1-strip.x0)/1), length=(strip.x1-strip.x0)/100, flux=length*lmPerM/n;
    for(let i=0;i<n;i++){
      const dx=(strip.x0+(i+.5)*(strip.x1-strip.x0)/n-point[0])/100;
      const dy=(strip.y-point[1])/100,dz=(strip.z-point[2])/100;
      const r2=dx*dx+dy*dy+dz*dz;
      if(dz>0)E+=(flux/Math.PI)*dz*dz/(r2*r2);
    }
  }
  return E;
}
light.complemento={strips,comprimento_total_m:strips.reduce((s,t)=>s+(t.x1-t.x0)/100,0),
  criterio:'500 lx médios como alvo comparativo escolhido neste estudo para preparo; sem reivindicação normativa.',
  limite:'Distribuição lambertiana ideal. lm/m úteis após perfil/difusor; não são especificação de fita nua. Não inclui sombras dos aparelhos sobre a bancada. Suporte do micro deve existir e ser compatibilizado.',cenarios:[]};
for(const lm_m of [400,600,800]){
  const result={lm_m_apos_difusor:lm_m};
  for(const name of ['preparo','pia']){
    const cx=name==='preparo'?156.9:92.5;
    const person=[cx-22.5,72,0,cx+22.5,102,175];
    result[name]={teto_com_pessoa:stats(grids[name].map(p=>intersects(light.lampada_cm,p,person)?0:illuminance(p,light.lampada_cm))),
      combinado_com_pessoa:stats(grids[name].map(p=>linearLight(p,lm_m)+(intersects(light.lampada_cm,p,person)?0:illuminance(p,light.lampada_cm)))),
      combinado_sem_pessoa:stats(grids[name].map(p=>linearLight(p,lm_m)+illuminance(p,light.lampada_cm)))};
  }
  light.complemento.cenarios.push(result);
}
// Integração numérica independente da distribuição em toda a semiesfera inferior.
let flux=0;
for(let t=.25;t<90;t+=.5)for(let p=1;p<360;p+=2)flux+=intensity(t,p)*Math.sin(rad(t))*rad(.5)*rad(2);
light.integral_fluxo_inferior_lm=flux;
light.diferenca_integral_versus_cabecalho_percentual=100*(flux-lumens)/lumens;
const checkResults=[];
function check(name,fn){fn();checkResults.push(name);}
check('LM-63: dimensões, contagem e simetria de quadrantes',()=>{assert.equal(intensity(30,30),intensity(30,150));assert.equal(intensity(30,30),intensity(30,330));});
check('Iluminância no nadir e lei do inverso do quadrado',()=>{const e=illuminance([0,0,0],[0,0,200],false);assert.ok(Math.abs(e-values[0][0]/4)<1e-8);assert.equal(illuminance([0,0,0],[0,0,400],false),e/4);});
check('Oclusão: raio interno bloqueado, raio externo livre',()=>{assert.ok(intersects([0,0,0],[10,0,0],[4,-1,-1,6,1,1]));assert.ok(!intersects([0,2,0],[10,2,0],[4,-1,-1,6,1,1]));});
check('Fonte linear: fluxo dobrado duplica a contribuição',()=>assert.ok(Math.abs(linearLight([90,35,92],800)-2*linearLight([90,35,92],400))<1e-8));
check('Conservação: integral fotométrica a menos de 5% do cabeçalho',()=>assert.ok(Math.abs(flux/lumens-1)<.05));
check('Cesto: pico analítico confirmado por varredura 0–55°',()=>{
  let peak=-Infinity;
  for(let i=0;i<=5500;i++){const a=rad(i/100);peak=Math.max(peak,12+25*Math.sin(a)+45*Math.cos(a));}
  assert.ok(Math.abs(peak-cesto.altura_maxima_giro)<.001);
  assert.ok(basket(56,75,cesto.angulo_minimo_boca_3cm).saldo_apos_reserva_3<1e-8);
});
check('Composição longitudinal fecha em 352 cm, sem saldo de montagem',()=>assert.equal(kitchen.saldo_instalacao_longitudinal,0));
const result={data:'2026-09-28',estado:'ESTUDO DOCUMENTAL; SEM LEVANTAMENTO LOCAL',fontes:origin,kitchen,cesto,office,table,quarto,light,verificacao:checkResults};
fs.writeFileSync(path.join(__dirname,'Resultados.json'),JSON.stringify(result,(k,v)=>typeof v==='number'?round(v,5):v,2)+'\n');
console.log(JSON.stringify({arquivo:'Resultados.json',luz:light.stats,complemento:light.complemento,integral_lm:round(flux),verificacoes:checkResults},null,2));
