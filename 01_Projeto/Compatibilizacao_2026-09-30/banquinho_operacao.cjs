// Conferência geométrica local; gabaritos paramétricos, não antropometria.
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const folder=__dirname;
const bed=[2,110,142,292],chair=[150,75,224.5,148],desk=[15,0,215,70],stored=[205,165,230,210];
const shift=(r,x,y)=>[r[0]+x,r[1]+y,r[2]+x,r[3]+y];
const overlap=(a,b)=>a[0]<b[2]&&a[2]>b[0]&&a[1]<b[3]&&a[3]>b[1];
function scene(stage,t,depth=40,width=50){
  let person=[187-depth,187.5-width/2,187,187.5+width/2],stool=stored;
  if(stage===0)person=shift(person,0,80*(1-t)); // aproximação já dentro do quarto
  if(stage===1)person=shift(person,15*t,0); // aproximação da pega
  if(stage===2){person=shift(person,15*(1-t),0);stool=shift(stored,-15*t,0);}
  if(stage===3){person=shift(person,0,80*t);stool=shift(stored,-15,80*t);}
  return {person,stool};
}
function check(depth,width){
  let collisions=0,outside=0,minBed=Infinity;
  for(let stage=0;stage<4;stage++)for(let step=0;step<=200;step++){
    const {person,stool}=scene(stage,step/200,depth,width);
    if(overlap(person,stool))collisions++;
    for(const r of [person,stool]){
      for(const obstacle of [bed,chair,desk])if(overlap(r,obstacle))collisions++;
      if(r[0]<0||r[1]<0||r[2]>230||r[3]>295)outside++;
    }
    minBed=Math.min(minBed,person[0]-bed[2]);
  }
  return {depth,width,samples:804,collisions,outside,minBodyBedClearance:minBed,carryGroupWidth:depth+28,idealDoorLeftClearance:42-depth};
}
const main=check(40,50),sensitivity=[30,35,40,45,50].map(d=>check(d,50));
assert.equal(main.collisions,0);assert.equal(main.outside,0);assert.equal(main.minBodyBedClearance,5);assert.equal(main.carryGroupWidth,68);assert.equal(main.idealDoorLeftClearance,2);
assert(sensitivity.find(x=>x.depth===50).collisions>0);assert.equal(sensitivity.find(x=>x.depth===45).minBodyBedClearance,0);
for(let stage=0;stage<3;stage++)assert.deepEqual(scene(stage,1),scene(stage+1,0));
const results={units:'cm',status:'Sequência geométrica candidata; não comprova ergonomia ou passagem pela porta real.',main,sensitivity,bodyWidthSensitivity:[45,50,55].map(w=>check(40,w)),door:'Aberta a 90 graus, folha ideal na linha x=220, y=220..295. Vão hipotético x=145..220; não é largura livre medida.',end:scene(3,1),sofaRigidClearance:205-(87+Math.hypot(45,70))};
fs.writeFileSync(path.join(folder,'Resultados_banquinho_operacao.json'),JSON.stringify(results,null,2)+'\n');
const rect=(r,color)=>`<rect x="${r[0]}" y="${r[1]}" width="${r[2]-r[0]}" height="${r[3]-r[1]}" fill="${color}"/>`;
function diagram(stage,t){const s=scene(stage,t);return `<svg viewBox="-10 -12 255 327" role="img" aria-label="Planta da etapa ${stage+1}: gabarito de pessoa em azul e banquinho em laranja"><path d="M145 295 H0 V0 H230 V295 H220" fill="#faf8f3" stroke="#344c50" stroke-width="2"/>${rect(desk,'#d9bea0')}${rect(bed,'#d9dee6')}${rect(chair,'#b7c5cc')}<path d="M220 220 V295" stroke="#8a6334" stroke-width="3"/>${rect(stored,'#f0dfce')}${rect(s.stool,'#d8954f')}${rect(s.person,'#238a94')}<text x="27" y="37">Bancada</text><text x="23" y="175">Cama aberta</text><text x="156" y="106">Cadeira</text><text x="5" y="312">230 × 295 cm · janela no topo</text></svg>`;}
const titles=['1. Aproximar-se pelo lado da cama','2. Posicionar-se junto ao banquinho','3. Recuar e puxar 15 cm','4. Transportar até perto da entrada'];
const desc=['O gabarito parte de dentro do quarto, perto da entrada, e segue para a TV. Porta já aberta; cama e cadeira permanecem nas posições estudadas.','Deslocamento lateral de 15 cm aproxima o gabarito da pega. Ainda não há simulação de braços ou flexão do tronco.','Pessoa e objeto recuam juntos. Restam 5 cm até a cama e 3 entre os dois gabaritos. O corpo não é uma medida de Elias.','Deslocamento de 80 cm rumo à entrada, sem girar o banquinho. A simulação termina antes da soleira; cruzamento e corredor externo não foram testados.'];
const html=`<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Banquinho — sequência de retirada</title><style>body{margin:0;background:#f3f0e9;color:#263e43;font:17px/1.55 system-ui}main{max-width:1120px;margin:auto;padding:28px}h1{font-size:32px;line-height:1.2}h2{font-size:21px}.cards{display:grid;grid-template-columns:repeat(2,1fr);gap:20px}.card{padding:22px;background:white;border-radius:14px;margin:18px 0}svg{display:block;width:100%;max-height:430px}svg text{font:10px system-ui;fill:#263e43}.tag{font-weight:700;color:#84612e}table{border-collapse:collapse;width:100%}th,td{padding:10px 6px;border-bottom:1px solid #ddd;text-align:left}.scroll{overflow:auto}a{color:#156a77}@media(max-width:700px){main{padding:16px}.cards{grid-template-columns:1fr}}</style><main><p class="tag">Estudo local · 30/09/2026 · candidato para gabarito</p><h1>Retirar o banquinho com a cama aberta</h1><p>Há uma sequência sem colisões entre os gabaritos idealizados, com o banquinho sempre na mesma orientação. <strong>Isso ainda não confirma acesso fácil:</strong> mãos, postura ao pegar a peça e porta real não estão representadas.</p><div class="card"><strong>Gabarito de teste: 40 × 50 cm em planta.</strong> Profundidade de 40 rumo à TV e largura de 50 paralela à parede. É uma hipótese paramétrica, não uma medida corporal nem uma norma. Azul: pessoa idealizada. Laranja: reserva do banquinho de 25 × 45.</div><div class="cards">${titles.map((title,i)=>`<section class="card"><h2>${title}</h2>${diagram(i,1)}<p>${desc[i]}</p></section>`).join('')}</div><section class="card"><h2>O limite mais sensível está na porta</h2><p>O conjunto transportado ocupa <strong>68 cm</strong>, de x=147 a 215. Comparado ao vão ideal de x=145 a 220, sobram <strong>2 cm de um lado e 5 do outro</strong>. A folha nominal de 75 cm não comprova esse vão livre: batentes, espessura, ferragens e corredor externo ainda precisam ser considerados.</p><p>Na retirada, a faixa de 48 cm permite um gabarito de 40 com 5 até a cama e 3 até o objeto. A profundidade máxima para manter 3 em ambos os lados seria <strong>42 cm</strong>, apenas um critério comparativo. Não vale como recomendação ergonômica.</p><div class="scroll"><table><tr><th>Profundidade do corpo hipotético</th><th>Folga à cama</th><th>Largura do conjunto</th><th>Margem esquerda no vão ideal</th></tr>${sensitivity.map(r=>`<tr><td>${r.depth} cm</td><td>${r.minBodyBedClearance} cm</td><td>${r.carryGroupWidth} cm</td><td>${r.idealDoorLeftClearance} cm</td></tr>`).join('')}</table></div><p>Valor zero significa contato de borda; negativo indica invasão. A tabela mantém a mesma trajetória, sem procurar uma manobra alternativa para cada gabarito.</p></section><section class="card"><h2>Encaminhamento do projeto</h2><p>Manter o local sob a TV como candidato secundário, sem fixar ferragens. A conta já permite testar uma sequência concreta; a limitação agora é conferir a pega real e a passagem na porta. O giro rígido do sofá fechado mantém 34,8 cm até a guarda; mecanismo de abertura e operador continuam fora dessa verificação.</p><p><a href="Banquinho_operacao.md">Memória e coordenadas</a> · <a href="Resultados_banquinho_operacao.json">Resultados reproduzíveis</a> · <a href="Banquinho_alternativa.html">Estudo anterior de guarda e altura</a></p></section></main></html>`;
fs.writeFileSync(path.join(folder,'Banquinho_operacao.html'),html);
console.log(JSON.stringify({main,sensitivity,continuity:'Três transições coincidentes; quatro etapas contínuas.'},null,2));
