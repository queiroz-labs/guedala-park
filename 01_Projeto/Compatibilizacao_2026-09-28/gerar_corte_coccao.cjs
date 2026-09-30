// Estudo geométrico documental. Todas as medidas em cm; não é projeto executivo.
const fs = require('node:fs');
const path = require('node:path');
const p = { modulo:60, lateral:1.8, corpoL:48.5, corpoP:56, corpoA:57,
  frenteL:51.7, externoA:61, externoP:61.5, aberturaL:49, aberturaA:60,
  folgaL:3, folgaP:5, bancadaA:92, bancadaP:63, cozinhaL:155,
  b:5, separacao:20, aberturaBaseL:38, aberturaBaseP:45 };
const round = x => Math.round(x*10000)/10000;
const n = x => new Intl.NumberFormat('pt-BR',{maximumFractionDigits:2}).format(x);
const r = {
  premissas:p,
  larguraUtil:round(p.modulo-2*p.lateral),
  folgaLateral:round((p.modulo-2*p.lateral-p.corpoL)/2),
  toleranciaLateral:round((p.modulo-2*p.lateral-p.corpoL)/2-p.folgaL),
  folgaGargalo:round((p.aberturaL-p.corpoL)/2),
  coberturaFrontal:round((p.frenteL-p.aberturaL)/2),
  nichoProfundidade:p.corpoP+p.folgaP,
  saldoProfundidade:61-p.corpoP-p.folgaP,
  // Condicional: mesma referência traseira para corpo e envelope total.
  envelopeCondicional:p.folgaP+p.externoP,
  passagemPedra:p.cozinhaL-p.bancadaP,
  passagemEnvelopeCondicional:p.cozinhaL-p.folgaP-p.externoP,
  avancamentoCondicional:p.folgaP+p.externoP-p.bancadaP,
  moduloCom10cm:round(p.corpoL+20+2*p.lateral),
  nichoCom10cm:p.corpoP+10,
  areaBase:p.aberturaBaseL*p.aberturaBaseP,
  suporteHipoteticoMinimo:3+1.8,
  vertical:[4,5,6,7,8].map(d=>({dHipotetico:d,topoForno:p.b+p.externoA,
    separacao:p.bancadaA-d-p.b-p.externoA,
    saldo:p.bancadaA-d-p.b-p.externoA-p.separacao,
    bMax:p.bancadaA-d-p.externoA-p.separacao})),
  verificacao:'Aritmética; não valida dimensões ausentes, ventilação efetiva ou instalação.'
};
// Conferências de fechamento e fronteiras do ensaio.
const equal=(a,b)=>{if(Math.abs(a-b)>1e-8)throw Error(`Fechamento inconsistente: ${a} != ${b}`)};
equal(2*p.lateral+p.corpoL+2*r.folgaLateral,p.modulo);
equal(p.bancadaP+r.passagemPedra,p.cozinhaL);
equal(r.envelopeCondicional+r.passagemEnvelopeCondicional,p.cozinhaL);
equal(r.vertical.find(x=>x.dHipotetico===6).saldo,0);
equal(91.5-5-(5.5+61),20); // d=5 com duas perdas independentes de 5 mm.
fs.writeFileSync(path.join(__dirname,'Resultados_coccao.json'),JSON.stringify(r,null,2)+'\n');
const txt=(x,y,t,cls='')=>`<text x="${x}" y="${y}" class="${cls}">${t}</text>`;
const line=(x1,y1,x2,y2,cls='dim')=>`<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" class="${cls}"/>`;
const rect=(x,y,w,h,cls)=>`<rect x="${x}" y="${y}" width="${w}" height="${h}" class="${cls}"/>`;
const dh=(x1,x2,y,label)=>line(x1,y,x2,y)+line(x1,y-5,x1,y+5)+line(x2,y-5,x2,y+5)+txt((x1+x2)/2,y-9,label,'center small');
const dv=(x,y1,y2,label)=>line(x,y1,x,y2)+line(x-5,y1,x+5,y1)+line(x-5,y2,x+5,y2)+`<text x="${x-10}" y="${(y1+y2)/2}" transform="rotate(-90 ${x-10} ${(y1+y2)/2})" class="center small">${label}</text>`;
// Elevação conservadora: só o envelope externo vertical é posicionado.
const s=4.5,X=118,Y=565,z=h=>Y-s*h;
let vertical=`<svg viewBox="0 0 670 660" role="img" aria-label="Elevação condicional: bancada a 92, frente do forno de 5 a 66 e cooktop com d hipotético de 6">`;
vertical+=line(70,Y,590,Y,'floor')+txt(480,Y+23,'Piso acabado','small');
vertical+=line(X,z(92),X+60*s,z(92),'stone')+txt(405,z(92)-10,'Tampo · 92','small');
vertical+=rect(X+4*s,z(92),52*s,6*s,'cook')+txt(X+26*s,z(92)+19,'d = 6 (HIPÓTESE)','center small');
vertical+=rect(X+(60-51.7)*s/2,z(66),51.7*s,61*s,'oven');
vertical+=txt(X+30*s,z(42),'VENAX GIII','center')+txt(X+30*s,z(36),'Frente externa: 61 A','center small');
vertical+=txt(X+30*s,z(28),'Corpo: 57 A','center small')+txt(X+30*s,z(22),'apoio ainda sem cota','center small');
vertical+=dv(70,z(92),Y,'92')+dv(445,z(86),z(66),'20 · limite')+dv(500,z(66),z(5),'61');
vertical+=line(X+52*s,z(86),462,z(86),'guide')+line(X+52*s,z(66),520,z(66),'guide');
vertical+=line(365,z(5),565,z(5),'guide')+txt(435,565-5*s-8,'Borda inferior · 5','small');
vertical+=txt(72,615,'Não posicionar o corpo/apoio pela frente externa.','small')+txt(72,638,'Com d = 6, a separação não possui tolerância adicional.','small')+'</svg>';
// Planta: escala única em ambas as direções; parte frontal projetada é condicional.
const k=5,px=105,py=87;
let plan=`<svg viewBox="0 0 670 560" role="img" aria-label="Planta cotada de câmara com 56,4 de largura e 61 de profundidade; projeção frontal condicional">`;
plan+=line(65,py,525,py,'wall')+txt(65,py-15,'Parede acabada','small');
plan+=rect(px,py,60*k,63*k,'stoneplan');
plan+=rect(px,py,1.8*k,61*k,'side')+rect(px+58.2*k,py,1.8*k,61*k,'side');
plan+=rect(px+(60-48.5)/2*k,py+5*k,48.5*k,56*k,'oven');
plan+=rect(px+(60-51.7)/2*k,py+5*k,51.7*k,61.5*k,'envelope');
plan+=txt(px+30*k,py+27*k,'Corpo 48,5 × 56','center');
plan+=txt(px+30*k,py+33*k,'Folgas laterais: 3,95','center small');
plan+=dh(px,px+60*k,45,'Módulo · 60');
plan+=dv(60,py,py+63*k,'Pedra · 63')+dv(470,py,py+61*k,'Nicho · 61');
plan+=line(px+60*k,py+61*k,570,py+61*k,'guide')+txt(487,py+61*k-8,'Plano 61','small');
plan+=line(px+55.85*k,py+66.5*k,570,py+66.5*k,'guide')+txt(486,py+66.5*k+19,'Extremo 66,5*','small');
plan+=txt(80,483,'* Somente se corpo e envelope tiverem a mesma face traseira.','small');
plan+=txt(80,509,'Pedra → 92 de passagem. Extremo condicional → 88,5.','small');
plan+=txt(80,535,'Porta fechada; abertura e puxador precisam de corte do GIII.','small')+'</svg>';
let throat=`<svg viewBox="0 0 1080 285" role="img" aria-label="Comparação horizontal entre câmara interna, abertura frontal e frente externa, e detalhe isolado de apoio">`;
const a=55,b=100,sk=7;
throat+=txt(55,28,'TRÊS LARGURAS · mesmo eixo','small');
for(const [w,yy,cl,label]of [[56.4,60,'side','Câmara · 56,4'],[49,112,'cook','Abertura frontal · 49'],[51.7,164,'oven','Frente externa · 51,7']]){
throat+=rect(a+(56.4-w)*sk/2,yy,w*sk,30,cl)+txt(a+56.4*sk/2,yy+21,label,'center small');}
throat+=txt(55,227,'Corpo de 48,5 passa na abertura com apenas 2,5 mm/lado.','small');
throat+=txt(605,28,'APOIO · detalhe isolado, sem posição no forno','small');
throat+=line(620,198,1010,198,'floor')+rect(645,115,270,31,'side');
throat+=txt(675,136,'Apoio hipotético · 1,8','small');
throat+=txt(675,179,'Canal de ar · 3 livres','small');
throat+=dv(970,115,198,'4,8 mín.*');
throat+=txt(605,227,'* Acima da base inferior do canal; suporte ainda não calculado.','small');
throat+=txt(55,265,'Enquadramento frontal, apoio vazado e caminho de ar precisam ser compatibilizados em um único detalhe.','small')+'</svg>';
const table=r.vertical.map(q=>`<tr><td>${n(q.dHipotetico)}</td><td>${n(q.separacao)}</td><td>${q.saldo>0?'+':''}${n(q.saldo)}</td><td>${q.saldo>0?'Há saldo no ensaio':q.saldo===0?'Limite sem tolerância':'Não atende com b = 5'}</td></tr>`).join('');
const html=`<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Guedala Park · corte de cocção</title><style>
:root{--ink:#263c3b;--teal:#35665f;--paper:#faf8f2;--line:#d6ded7;--amber:#9a561d}*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.6 system-ui,Segoe UI,sans-serif}main{max-width:1180px;margin:auto;padding:50px 34px}h1{font-size:clamp(32px,5vw,56px);line-height:1.08;letter-spacing:-.03em;margin:18px 0}h2{font-size:25px;line-height:1.2;margin:28px 0 12px}p{max-width:950px}a{color:var(--teal)}.eyebrow{font-size:12px;letter-spacing:.12em;font-weight:700;color:var(--teal)}.lead{font-size:19px;max-width:790px}.note{padding:18px 22px;border-left:4px solid var(--amber);background:#f4eadc;margin:26px 0}.grid{display:grid;grid-template-columns:1fr 1fr;gap:22px}.panel{background:white;border:1px solid var(--line);border-radius:12px;padding:18px}.panel h2{margin:4px 0 8px;font-size:20px}.panel p{font-size:14px;margin:8px 0}.metrics{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin:30px 0}.metric{border-top:2px solid var(--teal);padding-top:10px}.metric strong{font-size:32px;display:block}.metric span{font-size:14px}svg{width:100%;height:auto;display:block}svg text{font:16px system-ui,Segoe UI,sans-serif;fill:var(--ink)}svg .small{font-size:13px}svg .center{text-anchor:middle}svg .dim{stroke:#61716b;stroke-width:1}svg .guide{stroke:#869890;stroke-width:1;stroke-dasharray:4 4}svg .floor,svg .wall{stroke:#697773;stroke-width:3}svg .stone{stroke:#a98c67;stroke-width:5}svg .stoneplan{fill:#f3eadb;stroke:#ad906f}svg .side{fill:#d6c4a9;stroke:#8b785f}svg .oven{fill:#dce8e3;stroke:#35665f;stroke-width:2}svg .cook{fill:#ecdbba;stroke:#a46a22;stroke-dasharray:5 3}svg .envelope{fill:none;stroke:#9a561d;stroke-width:2;stroke-dasharray:7 5}table{width:100%;border-collapse:collapse;font-size:15px}th,td{text-align:left;padding:10px;border-bottom:1px solid var(--line)}th{background:#e9efeb}.tablewrap{overflow:auto}.footer{border-top:1px solid var(--line);margin-top:35px;padding-top:20px;font-size:13px}nav{display:flex;flex-wrap:wrap;gap:18px;margin:22px 0}.tag{font-size:13px;color:#6b736c}.full{margin-top:22px}@media(max-width:760px){main{padding:25px 18px}.grid{grid-template-columns:1fr}.metrics{grid-template-columns:1fr;gap:12px}.metric strong{font-size:27px}.panel{padding:12px}.full svg{min-width:860px}.full{overflow:auto}table{font-size:13px}}@media print{body{background:white}main{padding:0}.panel,.note,.metrics{break-inside:avoid}nav{display:none}h1{font-size:34px}}
</style><main><header><div class="eyebrow">GUEDALA PARK · COZINHA · 28 SET 2026</div><h1>O forno precisa caber<br>com suas folgas.</h1><p class="lead">Corte condicional do KE4GC + Venax GIII 50 L. Módulo de 60, bancada a 92 e pedra de 63 preservados como base do estudo.</p><p class="tag">Medidas em cm · hipóteses identificadas · sem liberação de fabricação</p><nav><a href="Caderno.html">Caderno geral</a><a href="Corte_coccao.md">Memória e fontes</a><a href="Resultados_coccao.json">Contas reproduzíveis</a></nav></header>
<div class="note"><strong>Uma divergência a resolver com a Venax.</strong> A tabela da p. 7 pede 3 cm nas laterais e 5 atrás; o texto da p. 10 pede 10 cm em toda a volta. As vistas abaixo seguem o ramo específico da tabela/desenho. Isso ainda não confirma a instalação.</div>
<div class="metrics"><div class="metric"><strong>9,5 mm</strong><span>saldo por lado além dos 3 cm da tabela</span></div><div class="metric"><strong>0 mm</strong><span>saldo no nicho de 61: corpo 56 + reserva 5</span></div><div class="metric"><strong>d ≤ 5 cm</strong><span>com frente a 5 e reserva de tolerância de 1 cm; d real ausente</span></div></div>
<div class="grid"><section class="panel"><h2>01 / Elevação condicional</h2><p>Desenho no limite nominal: d = 6 apenas para testar. A altura total publicada de 13,1 e o nicho de 15 não fornecem essa cota.</p>${vertical}</section><section class="panel"><h2>02 / Planta do envelope</h2><p>Tracejado: projeção externa condicional. A folga posterior precisa permanecer livre, com percurso próprio para as instalações.</p>${plan}</section></div>
<section class="panel full"><h2>03 / Encaixe e entrada de ar</h2><p>Abertura de base Venax: 38 × 45. Conferir também as passagens de 30 mm indicadas pela Electrolux e a continuidade até a saída.</p>${throat}</section>
<section><h2>A altura tolera quanto erro?</h2><p>Com borda inferior da frente a 5 e frente de 61, a separação é <strong>26 − d</strong>. Duas perdas de 5 mm — bancada mais baixa e forno mais alto — consomem 1 cm. O apoio real continua dependendo da seção do aparelho.</p><div class="tablewrap"><table><thead><tr><th>d hipotético</th><th>Separação</th><th>Saldo sobre 20</th><th>Leitura geométrica</th></tr></thead><tbody>${table}</tbody></table></div></section>
<section><h2>Impacto da divergência de manual</h2><p>Se os 10 cm fossem aplicados às laterais do corpo, o módulo passaria de <strong>60 para 72,1 cm</strong> com os painéis do ensaio. Atrás, seriam <strong>66 de nicho e 68 de pedra</strong>. Esses valores quantificam a dúvida; não alteram o layout escolhido.</p><p>No cenário da tabela específica, o envelope fechado pode avançar a <strong>66,5 da parede</strong> e reduzir a passagem local de 92 para <strong>88,5 cm</strong>, se as referências traseiras coincidirem. A porta aberta ainda precisa de geometria própria.</p></section>
<section><h2>Próximo dado, já definido</h2><p>A consulta técnica está pronta na memória: Electrolux precisa fornecer a cota inferior instalada; Venax precisa esclarecer as folgas divergentes e fornecer a posição de apoio, abas e referências do GIII. Até isso existir, não elevar a bancada, trocar aparelho ou consumir a pia para compensar uma medida presumida.</p></section>
<footer class="footer">Base: manuais locais Electrolux 250405XATF (páginas impressas 5, 8–9) e Venax cód. 375, ed. 2, R.21 (p. 6–7, 10–11). Pesquisa oficial conferida em 28/09. <a href="Corte_coccao.md">Fontes, hipóteses e consulta técnica completa</a>. Prancha gerada por gerar_corte_coccao.cjs; não escala de impressão.</footer></main></html>`;
fs.writeFileSync(path.join(__dirname,'Corte_coccao.html'),html);
console.log('Corte_coccao.html e Resultados_coccao.json gerados; 5 conferências geométricas passaram.');
