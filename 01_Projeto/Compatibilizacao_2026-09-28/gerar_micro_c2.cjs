const fs=require('node:fs'),path=require('node:path');
const r=JSON.parse(fs.readFileSync(path.join(__dirname,'Resultados_micro_c2.json'),'utf8'));
const n=x=>new Intl.NumberFormat('pt-BR',{maximumFractionDigits:1}).format(x),lux=x=>Math.round(x);
const text=(x,y,t,c='')=>`<text x="${x}" y="${y}" class="${c}">${t}</text>`;
const line=(x1,y1,x2,y2,c='dim')=>`<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" class="${c}"/>`;
const rect=(x,y,w,h,c)=>`<rect x="${x}" y="${y}" width="${w}" height="${h}" class="${c}"/>`;
const dh=(x1,x2,y,t)=>line(x1,y,x2,y)+line(x1,y-5,x1,y+5)+line(x2,y-5,x2,y+5)+text((x1+x2)/2,y-10,t,'center');
const y=h=>530-(h-90)*3,t=d=>80+5*d;
let corte='<svg viewBox="0 0 710 640" role="img" aria-label="Corte do apoio com profundidade de 47 cm, topo a 155, luz a 152,2 e reserva do purificador até 149">';
corte+=line(t(0),y(255),t(0),y(90),'wall')+rect(t(0),y(255),35*5,(255-194)*3,'wood');
corte+=text(t(17.5),y(220),'Guarda B · P 35','center');
corte+=rect(t(10),y(184),35.2*5,29*3,'micro')+text(t(27.6),y(169),'ME23P','center white');
corte+=rect(t(0),y(155),47*5,1.8*3,'wood')+line(t(42)-6,y(152.2),t(42)+6,y(152.2),'led');
corte+=rect(t(10),y(127),42*5,35*3,'filter')+text(t(31),y(109),'PE12G','center white');
corte+=rect(t(10),y(149),42*5,22*3,'reserve')+text(t(31),y(138),'Acesso superior · 22','center');
corte+=line(t(0),y(92),t(63),y(92),'stone')+text(t(64),y(92)+5,'Pedra · 92');
corte+=line(t(35),y(194),515,y(194),'guide')+text(430,y(194)-10,'Face inferior · 194');
corte+=line(t(45.2),y(184),515,y(184),'guide')+text(430,y(184)+20,'Topo do micro · 184');
corte+=text(430,y(194)+24,'10 cm escolhidos','amber');
corte+=line(t(47),y(155),515,y(155),'guide')+text(430,y(155)-11,'Apoio · 155');
corte+=line(t(42),y(152.2),515,y(152.2),'guide')+text(430,y(152.2)+20,'Luz · 152,2');
corte+=line(t(52),y(149),515,y(149),'guide')+text(430,y(149)+42,'Reserva até 149');
corte+=dh(t(0),t(47),579,'47 cm de apoio')+text(80,620,'Esquema: suporte estrutural e pés do aparelho a detalhar.')+'</svg>';
const k=4.4,px=60,py=62;
let plan='<svg viewBox="0 0 710 640" role="img" aria-label="Planta de B e C com apoio aberto, corpo do micro e dois perfis de luz">';
plan+=rect(px,py,69.7*k,47*k,'wood')+rect(px+69.7*k,py,54.7*k,35*k,'wood');
plan+=rect(px+11.8*k,py+10*k,46.1*k,35.2*k,'micro');
plan+=text(px+34.85*k,py+25*k,'ME23P','center white');
plan+=text(px+34.85*k,py-24,'B · 69,7','center')+text(px+(69.7+27.35)*k,py-24,'C · 54,7','center');
plan+=line(px+2*k,py+42*k,px+67.7*k,py+42*k,'led')+line(px+71.7*k,py+30*k,px+122.4*k,py+30*k,'led');
plan+=line(px,py+63*k,px+124.4*k,py+63*k,'stone')+text(px+60*k,py+63*k+25,'Frente da pedra · 63','center');
plan+=text(px+34.85*k,py+47*k+26,'Perfil B: 65,7 · eixo a 42','center')+text(px+(69.7+27.35)*k,py+35*k+26,'C: 50,7 · eixo a 30','center');
plan+=text(60,443,'Laterais abertas no apoio: 11,8 cm por lado até os limites de B.');
plan+=text(60,478,'Perfil amarelo aparece em projeção, sob o painel.');
plan+=text(60,513,'Armários fechados continuam com 35 cm de profundidade.');
plan+=text(60,566,'Fita ativa de teste: 62,5 + 47,5 = 110 cm.','bold');
plan+=text(60,606,'Tampas, terminais e passo de corte entram na conta.')+'</svg>';
const color=e=>e<100?'#4c5778':e<250?'#577f96':e<400?'#83aaa9':e<500?'#c2d1b1':e<650?'#efd48c':e<800?'#e6ab62':'#bf7444';
function heat(mode){
 const q=r.scenarios.find(x=>x.modo===mode&&x.pessoa),scale=5,ox=62,oy=60;
 let svg=`<svg viewBox="0 0 760 415" role="img" aria-label="Mapa da contribuição direta no plano da bancada: ${mode}; pessoa centralizada em cada região separadamente">`;
 svg+=rect(ox,oy,126.9*scale,50*scale,'unsampled');
 for(const [key,low,high] of [['preparo_livre',26,61.9],['pia',61.9,126.9]]){const dx=(high-low)/Math.ceil((high-low)/2.5);for(const a of q.areas[key].map){const value=a.teto+r.fluxoProposto*a.por_lm_m;svg+=`<rect x="${ox+(a.point[0]-dx/2)*scale}" y="${oy+(a.point[1]-10-1.25)*scale}" width="${dx*scale+.1}" height="12.6" fill="${color(value)}"/>`;}}
 svg+=rect(ox+5*scale,oy,16*scale,42*scale,'filter')+text(ox+13*scale,oy+21*scale,'Filtro','center white');
 if(mode==='airfryer')svg+=rect(ox+31*scale,oy,26.4*scale,36*scale,'micro')+text(ox+44.2*scale,oy+18*scale,'Air fryer','center white');
 svg+=`<rect x="${ox+72.9*scale}" y="${oy+3*scale}" width="${43*scale}" height="${37*scale}" fill="none" stroke="#263d3c" stroke-dasharray="5 4"/>`;
 svg+=line(ox+61.9*scale,oy,ox+61.9*scale,oy+250,'dim');
 svg+=text(ox+(26+35.9/2)*scale,30,'Preparo prioritário','center')+text(ox+(61.9+32.5)*scale,30,'Plano sobre pia','center');
 svg+=text(ox,340,'Parede acima · frente da bancada abaixo. Cinza: fora da avaliação.');
 svg+=text(ox,373,'Cuba tracejada: cálculo no plano a 92 cm, não no seu fundo.');
 svg+='</svg>';return svg;
}
const rows=r.scenarios.map(q=>`<tr><td>${q.modo==='normal'?'Normal':'Air fryer na cozinha'}${q.pessoa?', com pessoa':', sem pessoa'}</td><td>${lux(q.areas.preparo_livre.comProposto.media)} / ${lux(q.areas.preparo_livre.comProposto.min)}</td><td>${lux(q.areas.pia.comProposto.media)} / ${lux(q.areas.pia.comProposto.min)}</td></tr>`).join('');
const html=`<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Guedala Park · micro e luz C2</title><style>
*{box-sizing:border-box}body{margin:0;background:#faf8f2;color:#273f3b;font:16px/1.65 system-ui,Segoe UI,sans-serif}main{max-width:1240px;padding:45px 30px;margin:auto}h1{font-size:clamp(32px,5vw,54px);line-height:1.1;letter-spacing:-.03em}h2{font-size:25px;line-height:1.25}p{max-width:990px}a{color:#35665f}.kicker{font-size:12px;letter-spacing:.12em;color:#35665f;font-weight:700}.lead{font-size:20px;max-width:900px}.note{padding:18px 22px;background:#f3e7d5;border-left:4px solid #ac703b;margin:25px 0}.grid{display:grid;grid-template-columns:1fr 1fr;gap:22px}.panel{background:white;border:1px solid #d7dfd9;border-radius:12px;padding:20px}.panel h2{font-size:20px;margin:2px 0 10px}.panel p{font-size:14px}.metrics{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;margin:25px 0}.metric{border-top:2px solid #35665f;padding-top:12px}.metric strong{display:block;font-size:30px}.metric span{font-size:14px}.section{margin-top:35px}svg{width:100%;height:auto;display:block}svg text{font:16px system-ui,Segoe UI,sans-serif;fill:#273f3b}svg .center{text-anchor:middle}svg .white{fill:white}svg .bold{font-weight:600}svg .amber{fill:#97591f}svg .wood{fill:#dfccb0;stroke:#9d886a;stroke-width:1.5}svg .micro{fill:#414c49;stroke:#273f3b;stroke-width:1.5}svg .filter{fill:#436965;stroke:#273f3b}svg .reserve{fill:#e4eeea;stroke:#78948c;stroke-dasharray:6 4}svg .dim{stroke:#617871;stroke-width:1.2}svg .guide{stroke:#96a39b;stroke-dasharray:4 4}svg .wall{stroke:#78857d;stroke-width:3}svg .stone{stroke:#a58b68;stroke-width:5}svg .led{stroke:#f6bb43;stroke-width:6}svg .unsampled{fill:#e8e8e4;stroke:#9da9a3}.legend{display:flex;gap:15px;flex-wrap:wrap;font-size:13px;margin:15px 0}.chip{display:inline-block;width:20px;height:12px;margin-right:5px}.tablewrap{overflow:auto}table{width:100%;border-collapse:collapse;font-size:15px}td,th{text-align:left;padding:10px;border-bottom:1px solid #d7dfd9}th{background:#e7eee9}nav{display:flex;gap:18px;flex-wrap:wrap}footer{border-top:1px solid #ccd7cd;margin-top:35px;padding-top:18px;font-size:13px}@media(max-width:780px){main{padding:25px 17px}.grid{grid-template-columns:1fr}.metrics{grid-template-columns:1fr;gap:10px}.metric strong{font-size:27px}.panel{padding:12px}svg{min-width:550px}.drawing{overflow:auto}table{font-size:13px}}@media print{main{padding:0}body{background:white}.panel{break-inside:avoid}nav{display:none}h1{font-size:36px}}
</style><main><div class="kicker">GUEDALA PARK · DESENVOLVIMENTO TÉCNICO · 28 SET 2026</div><h1>Um apoio mais profundo.<br>Luz melhor distribuída.</h1><p class="lead">Prateleira aberta para o ME23P e dois trechos de luz sob B/C, preservando a organização aprovada dos aéreos.</p><nav><a href="Micro_C2.md">Memória, critérios e fontes</a><a href="Caderno.html">Caderno geral</a><a href="Resultados_micro_c2.json">Resultados reproduzíveis</a></nav>
<div class="note"><strong>Proposta de detalhamento.</strong> Apoio e luz avançam sem alterar a escolha de 10 cm acima do micro. Esse afastamento continua divergente dos 30 cm do manual; a instalação completa permanece não validada.</div>
<div class="metrics"><div class="metric"><strong>69,7 × 47 cm</strong><span>apoio aberto, topo a 155 cm; estrutura a dimensionar</span></div><div class="metric"><strong>11,8 cm</strong><span>por lado até os limites de B, sem laterais fechando o micro</span></div><div class="metric"><strong>3,2 cm</strong><span>entre o perfil de ensaio e a reserva superior do filtro</span></div></div>
<div class="grid"><section class="panel"><h2>01 / Corte lateral</h2><p>Profundidade do apoio cresce 12 cm além dos aéreos. O conjunto continua 16 cm atrás da borda da pedra.</p><div class="drawing">${corte}</div></section><section class="panel"><h2>02 / Apoio e perfis em planta</h2><p>Recuo de 5 cm da borda de cada apoio. Laterais e altura da guarda superior B/C permanecem.</p><div class="drawing">${plan}</div></section></div>
<section class="section"><h2>O perfil avançou e melhorou o mínimo com o mesmo fluxo.</h2><p>Foram comparadas 12 posições, incluindo o purificador e uma pessoa à frente. Levar B de 35 para <strong>42 cm da parede</strong> elevou o mínimo no preparo de 277 para <strong>308 lx diretos</strong>, cerca de 11%, enquanto a média mudou de 518 para 513 lx. C permanece a 30 cm.</p><p>Ensaio com <strong>800 lm/m úteis após difusor</strong>, regulável e 3000 K. Os perfis reservam 65,7 + 50,7 cm; com terminais e passo de corte hipotético de 2,5 cm, a fita ativa fica em <strong>62,5 + 47,5 cm</strong>. Total luminoso de referência: <strong>880 lm</strong>.</p></section>
<section class="section"><h2>A air fryer muda a área disponível e a sombra.</h2><p>A região prioritária de preparo tem 35,9 × 50 cm, depois da reserva do filtro. A air fryer ocupa <strong>52,9% dessa região</strong> antes das folgas de uso. A cena temporária continua possível como arranjo; ela não oferece a mesma superfície de preparo iluminada da cena normal.</p><div class="legend">${[['#4c5778','0–99'],['#577f96','100–249'],['#83aaa9','250–399'],['#c2d1b1','400–499'],['#efd48c','500–649'],['#e6ab62','650–799'],['#bf7444','800+']].map(([c,l])=>`<span><i class="chip" style="background:${c}"></i>${l} lx</span>`).join('')}</div><div class="grid"><section class="panel"><h2>Normal · com pessoa</h2><div class="drawing">${heat('normal')}</div></section><section class="panel"><h2>Air fryer · com pessoa</h2><div class="drawing">${heat('airfryer')}</div></section></div><p><small>Mapas com a pessoa centralizada em cada região separadamente. Contribuição direta inicial: sem reflexões, luz natural ou ótica real do perfil. Zero direto não significa escuridão absoluta. Não é laudo nem garantia de lux instalados.</small></p></section>
<section class="section"><h2>Comparação no plano a 92 cm</h2><div class="tablewrap"><table><thead><tr><th>Cena</th><th>Preparo: média / mínimo</th><th>Pia: média / mínimo</th></tr></thead><tbody>${rows}</tbody></table></div><p>500 lx médios é alvo comparativo do estudo. A região da pia inclui a projeção da cuba; a profundidade da cuba e louças não foram simuladas. Aumentar fluxo sozinho não elimina o bloqueio dos raios pelos aparelhos.</p></section>
<section class="section"><h2>O que fica definido para o próximo desenho</h2><p>Apoio aberto com envelope de 47 cm; perfis em dois trechos, a 42 e 30 cm da parede; mesma organização dos aéreos. Estrutura, pés do ME23P, fonte acessível, terminais e perfil real devem aparecer juntos no detalhe. Baixar o micro 20 cm invadiria em 16,8 cm a reserva do filtro, por isso essa hipótese não avançou.</p></section>
<footer>Base local: manual ME23P p. 3, guia dimensional, Aéreos R00, Aparelhos R03 e IES Stella arquivado. Sem nova seleção comercial, contato ou compra. <a href="Micro_C2.md">Memória completa</a>. Cotas em centímetros; medidas de estudo, sem escala de impressão.</footer></main></html>`;
fs.writeFileSync(path.join(__dirname,'Micro_C2.html'),html);console.log('Micro_C2.html gerado.');
