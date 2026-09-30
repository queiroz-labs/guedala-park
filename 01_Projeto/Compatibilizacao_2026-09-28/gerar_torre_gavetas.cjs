const fs=require('node:fs'),path=require('node:path');
const R=JSON.parse(fs.readFileSync(path.join(__dirname,'Resultados_torre_gavetas.json'),'utf8'));
const n=x=>new Intl.NumberFormat('pt-BR',{maximumFractionDigits:2}).format(x);
const txt=(x,y,s,cl='')=>`<text x="${x}" y="${y}" class="${cl}">${s}</text>`;
const rect=(x,y,w,h,cl)=>`<rect x="${x}" y="${y}" width="${w}" height="${h}" class="${cl}"/>`;
const line=(x,y,x2,y2,cl='line')=>`<line x1="${x}" y1="${y}" x2="${x2}" y2="${y2}" class="${cl}"/>`;
const dim=(x,y,x2,s)=>line(x,y,x2,y)+line(x,y-4,x,y+4)+line(x2,y-4,x2,y+4)+txt((x+x2)/2,y-8,s,'center small');
// Planta na mesma escala s/t. Círculos A/B/C são ensaios, não furos executivos.
const k=6.3,X=s=>66+s*k,Y=t=>67+t*k;
let plan=rect(X(0),Y(0),126.9*k,63*k,'stone');
plan+=rect(X(0),Y(0),61.9*k,9.2*k,'rear');
plan+=rect(X(0),Y(0),126.9*k,2*k,'wood');
plan+=rect(X(3.1),Y(9.2),55.7*k,50*k,'box dash');
plan+=line(X(61.9),Y(0),X(61.9),Y(63),'line dash');
plan+=rect(X(5),Y(10),16*k,42*k,'filter')+rect(X(31),Y(10),26.4*k,36*k,'air');
plan+=rect(X(72.9),Y(13),43*k,37*k,'sink');
plan+=txt(X(13),Y(30),'PE12G','center white')+txt(X(44.2),Y(26),'AIR FRYER','center')+txt(X(44.2),Y(30),'temporária','center small');
plan+=txt(X(94.4),Y(30),'CUBA','center')+txt(X(94.4),Y(34),'43 × 37 • envelope','center small');
for(const q of R.testesPosicao){plan+=`<circle cx="${X(q.s)}" cy="${Y(q.t)}" r="${3.8*k}" class="point"/>`+txt(X(q.s),Y(q.t)+5,q.id,'center bold');}
plan+=txt(66,32,'PAREDE / t = 0','small')+txt(865,32,'s cresce em direção à pia →','small end');
plan+=dim(X(0),505,X(61.9),'61,9 · preparo / gavetas')+dim(X(61.9),505,X(126.9),'65 · pia');
plan+=txt(66,540,'Tracejado: caixa de gaveta fechada. Faixa azul: 9,2 cm brutos, antes do fundo e das travessas.','small');
plan+=txt(66,565,'A / B / C são posições de teste; nenhuma está liberada para furação.','small bold');
// Corte em profundidade: escala igual horizontal/vertical, z desde piso.
const K=8.6,T=t=>76+t*K,Z=z=>950-z*K;
let section=rect(T(0),Z(92),63*K,2*K,'stone')+rect(T(0),Z(90),1.8*K,72*K,'wood');
section+=rect(T(2.3),Z(92),6.4*K,20.6*K,'tower')+rect(T(4.8),Z(71.4),1.4*K,3.5*K,'tower');
section+=rect(T(1.7),Z(100.98),7.6*K,.5*K,'tower')+rect(T(2.8),Z(100.48),5.4*K,8.48*K,'tower');
section+=rect(T(0),Z(102),2*K,10*K,'wood');
section+=rect(T(1.7),Z(92.33),7.6*K,.33*K,'tower');
// Esquema das faixas das caixas, não alturas executivas de caixa.
for(const [top,bottom,name] of [[90,74,'G1 · frente 16'],[74,58,'G2 · frente 16'],[58,18,'G3 · frente 40']]){
 section+=rect(T(9.2),Z(top),50*K,(top-bottom)*K,'box dash')+rect(T(59.2),Z(top),1.8*K,(top-bottom)*K,'wood');
 section+=txt(T(35),Z((top+bottom)/2)+5,name,'center');
}
section+=line(T(8.7),Z(88),T(9.2),Z(88),'red');
section+=txt(680,185,'Pedra a 92 / esp. 2','bold')+line(T(63),Z(91),660,180);
section+=txt(680,233,'Anel: Ø e altura ausentes','warn')+txt(680,257,'Não representado em escala.','small');
section+=txt(680,337,'Corpo até z = 71,4','bold')+line(T(8.7),Z(71.4),658,332);
section+=txt(680,377,'Terminal até z = 67,9')+line(T(6.2),Z(67.9),658,372);
section+=txt(680,425,'Cabo e curva não cotados.','warn')+txt(680,449,'A reserva pode aumentar.','small');
section+=txt(680,532,'Faixas G1/G2 atravessadas','bold')+txt(680,556,'pela altura da torre;','small')+txt(680,580,'avaliar folga em profundidade.','small');
section+=txt(680,670,'G3 não foi reduzido.','bold')+txt(680,694,'Caixas reais, juntas e trilhos','small')+txt(680,718,'a detalhar dentro das frentes.','small');
section+=dim(T(0),835,T(9.2),'9,2')+dim(T(9.2),835,T(59.2),'50 · caixa')+dim(T(0),882,T(61),'61 · face da frente');
section+=txt(76,38,'CORTE DE TESTE • EIXO t = 5,5 cm','small')+txt(76,63,'Torre desenhada pela ficha 10 A: não comprova a variante 20 A.','small warn');
section+=txt(76,925,'Fundo de 18 mm e corpo Ø6,4: 5 mm por lado, sem tolerância adicional.','small');
// Ampliação para distinguir corpo, furo, tampa e rodabanca.
const a=30,U=t=>80+t*a;
let detail=rect(U(0),75,2*a,85,'wood')+rect(U(9.2),195,6*a,90,'box')+rect(U(1.8),195,1*a,0,'wood');
detail+=rect(U(1.7),95,7.6*a,25,'tower')+rect(U(2.3),175,6.4*a,75,'tower');
detail+=rect(U(0),160,1.8*a,125,'wood');
detail+=line(U(2.25),145,U(8.75),145,'red');
detail+=txt(600,112,'Tampa Ø7,6','bold')+txt(600,145,'Furo Ø6,5','warn')+txt(600,210,'Corpo Ø6,4','bold');
detail+=txt(80,38,'MESMO EIXO, OBSTÁCULOS EM ALTURAS DIFERENTES','small');
detail+=dim(U(1.8),325,U(9.2),'7,4 livres entre fundo e caixa');
detail+=txt(80,366,'Rodabanca de teste: 2 cm. Tampa começa em t=1,7 → sobreposição de 3 mm.','small warn');
detail+=txt(80,391,'Mover o eixo para t=5,8 elimina essa sobreposição, mas deixa só 2 mm até a caixa.','small');
const rows=R.cenarios.map(q=>`<tr><td>${n(q.fundo)}</td><td>${n(q.recuo)}</td><td>${n(q.faixa)}</td><td><b>${n(q.diametroMax)}</b></td><td class="${q.saldoCorpo<0?'bad':''}">${n(q.saldoCorpo)}</td></tr>`).join('');
const pos=R.testesPosicao.map(q=>`<tr><td><b>${q.id}</b><br>(${n(q.s)}; ${n(q.t)})</td><td>${n(q.distanciaCuba)} cm</td><td>${q.intersecaoCaixa?'Invade caixas':'Fora da caixa'}</td><td>${q.nota}</td></tr>`).join('');
const html=`<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Torre × gavetas — Guedala Park</title><style>
:root{--ink:#243d3f;--muted:#607477;--bg:#f2f1eb;--accent:#99623b}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 system-ui,sans-serif}main{max-width:1140px;margin:auto;padding:44px 30px 80px}header{border-bottom:2px solid #bcc9c3;padding-bottom:26px}h1{font-size:42px;line-height:1.15;letter-spacing:-1.5px;margin:12px 0}h2{font-size:24px;line-height:1.3;margin:0 0 18px}h3{font-size:18px;margin:0 0 8px}p{margin:10px 0 15px}.eyebrow{font-size:12px;letter-spacing:2px;font-weight:700}.lede{max-width:880px;font-size:19px}a{color:#376e76}.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:28px 0}.card{padding:20px;background:#e2e9e3;border-radius:10px}.big{display:block;font-size:32px;line-height:1.3;font-weight:700}.card small{display:block;color:#486161}.sheet{background:#fff;border-radius:12px;padding:28px;margin:24px 0}.note{padding:15px 20px;background:#f5ecdf;border-left:4px solid #ac7348}.diagram{overflow:auto}svg{display:block;width:100%;min-width:780px;height:auto}svg text{font:17px system-ui,sans-serif;fill:#243d3f}.small{font-size:14px}.center{text-anchor:middle}.end{text-anchor:end}.bold{font-weight:700}.white{fill:white}.warn{fill:#975127}.line{stroke:#6b7b7b;stroke-width:1}.red{stroke:#ae4934;stroke-width:2}.stone{fill:#eeede7;stroke:#87918b}.rear{fill:#c9e0e5}.wood{fill:#c6ad88;stroke:#99856d}.box{fill:#e5ecdf;stroke:#718170;stroke-width:1.3}.dash{stroke-dasharray:6 5}.filter{fill:#4d696d;stroke:#304d50}.air{fill:#edddc4;stroke:#ad8d65}.sink{fill:#d9e7ed;stroke:#7c9baa}.point{fill:#f8d3a9;stroke:#a25835;stroke-width:2}.tower{fill:#415056;stroke:#25383b}table{width:100%;border-collapse:collapse;font-size:15px}td,th{padding:11px 12px;text-align:left;border-bottom:1px solid #dfe5e2;vertical-align:top}th{background:#eef1ec}td.bad{color:#a64630;font-weight:700}.table{overflow:auto}footer{font-size:13px;color:#5d6d6e;margin-top:30px}ul{padding-left:23px}li{margin:8px 0}@media(max-width:700px){main{padding:24px 14px}.cards{grid-template-columns:1fr}h1{font-size:33px}.sheet{padding:18px}.table table{min-width:620px}}@media print{main{padding:0}.sheet{break-inside:avoid}.cards{grid-template-columns:repeat(3,1fr)}a{color:inherit}.diagram{overflow:visible}svg{min-width:0}}
</style><main><header><div class="eyebrow">GUEDALA PARK / COMPATIBILIZAÇÃO / 28 SET 2026</div><h1>Torre automática × gavetas</h1><p class="lede">Preservar as caixas de 50 cm. A faixa traseira pode acomodar um corpo estreito, mas fundo, anel e acesso por cima ainda precisam fechar juntos.</p><p><a href="Torre_gavetas.md">Memória completa e consulta técnica</a> · <a href="README.md">Índice da rodada</a></p></header>
<div class="cards"><div class="card"><span class="big">9,2 cm</span><small>Faixa bruta no corte 61 − 1,8 − 50</small></div><div class="card"><span class="big">7,4 cm</span><small>Faixa com fundo traseiro de 18 mm</small></div><div class="card"><span class="big">50 cm</span><small>Caixa preservada · 47 cm internos</small></div></div>
<div class="note"><b>Direção mantida:</b> automática por pressão, tampa preta e tomada que receba plugue 20 A em 127 V. Modelo e furação continuam sem liberação. Medidas da torre abaixo são de uma ficha 10 A, usadas para investigar o encaixe.</div>
<section class="sheet"><h2>01 / Caber por baixo não resolve o uso por cima</h2><p>Purificador e cuba permanecem na implantação estudada. A, B e C expõem os conflitos; não são alternativas prontas para escolha.</p><div class="diagram"><svg viewBox="0 0 940 600" role="img" aria-label="Planta de preparo e pia com três posições de teste da torre">${plan}</svg></div><div class="table"><table><thead><tr><th>Teste (s; t)</th><th>Até a cuba¹</th><th>Por baixo</th><th>Conflito restante</th></tr></thead><tbody>${pos}</tbody></table></div><p><small>¹ Distância entre borda da tampa e envelope externo da cuba. O manual online QTMOV publica 60 cm até áreas úmidas; seu PDF não repete a frase. Este ensaio não transforma isso em regra universal da NBR, nem considera a cuba toda a área molhada. Em t=5,5, o limite calculado é s≤${n(R.medidas.limiteS60)} cm.</small></p></section>
<section class="sheet"><h2>02 / O espaço traseiro nasce da construção do móvel</h2><p>Face aplicada em t=61, espessura 1,8 e caixa de 50: traseira em t=9,2. São planos propostos, sujeitos a medição e ferragem real. Abrir a gaveta afasta sua caixa da torre traseira.</p><div class="diagram"><svg viewBox="0 0 980 955" role="img" aria-label="Corte com caixa de 50 centímetros e torre na faixa traseira">${section}</svg></div><div class="note">O envelope vertical de referência atravessa G1 e G2. Isso não demonstra necessidade de cortar G3. Anel, cabos, travessas e espaço para retirar a torre precisam entrar no corte real.</div></section>
<section class="sheet"><h2>03 / Furo, corpo e tampa exigem espaços diferentes</h2><div class="diagram"><svg viewBox="0 0 940 425" role="img" aria-label="Detalhe ampliado da tampa, corpo, rodabanca e caixa">${detail}</svg></div><p>Os 5 mm por lado são uma reserva deste ensaio. Não comprovam resistência da pedra, acesso de ferramenta ou afastamento elétrico. Diâmetro e altura do anel não foram fornecidos na ficha.</p><div class="table"><table><thead><tr><th>Fundo (cm)</th><th>Recuo extra</th><th>Faixa livre</th><th>Ø máximo²</th><th>Saldo para Ø6,4</th></tr></thead><tbody>${rows}</tbody></table></div><p><small>² Com 5 mm de cada lado, na altura das caixas. Fundo 18 mm + recuo zero deixa Ø6,4 no limite. Fundo de 6 mm ou uma faixa sem painel são cenários para detalhamento estrutural, sem alteração aprovada.</small></p></section>
<section class="sheet"><h2>04 / Critério pronto para selecionar sem perder armazenamento</h2><ul><li><b>Produto:</b> vincular um código preto 20 A ao desenho instalado aberto e fechado. A ficha QM12200 disponível descreve 10 A.</li><li><b>Montagem:</b> corpo, anel e cabo dentro da faixa real; acesso para apertar e retirar por baixo após remover gavetas.</li><li><b>Implantação:</b> botão, plugue e mão acessíveis com o purificador no lugar, além do critério de água e da rodabanca.</li><li><b>Gavetas:</b> manter 50 cm como objetivo. Reduzir para 45 tiraria ${n(R.medidas.perdaArea50a45)}% da área interna de cada caixa. Nenhuma redução aplicada.</li></ul><p>A consulta técnica está pronta na <a href="Torre_gavetas.md">memória</a>. Próxima frente independente: mecanismo do cesto e retirada do saco sob o tanque.</p></section>
<footer>Base documental, sem medição da unidade ou liberação de fabricação. <a href="Fontes_torre/QTMOV_ficha_10A.pdf">Ficha QTMOV 10 A</a> · <a href="Fontes_torre/QTMOV_manual.pdf">Manual QTMOV</a> · <a href="https://qtmov.com.br/manuais/mini-totem-automatico/">Manual online</a> · <a href="Resultados_torre_gavetas.json">Contas e cinco verificações</a>. Diagramas esquemáticos; faixas de G1/G2/G3 representam as frentes, não as alturas executivas das caixas.</footer></main></html>`;
fs.writeFileSync(path.join(__dirname,'Torre_gavetas.html'),html);
console.log('Torre_gavetas.html gerado.');
