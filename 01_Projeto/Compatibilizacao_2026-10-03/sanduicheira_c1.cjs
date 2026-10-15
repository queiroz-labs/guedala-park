const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
// Fontes: Conferencia_aereos_2026-09-25.md e C3_reserva.md.
// Envelopes são limites de estudo, sem modelo comercial ou pilha real.
const round = n => Math.round(n * 1000) / 1000;
const cases = [51.1, 48.6].map(width => ({
  width,
  approvedTwoStacks: { plateDiameters: [24, 21], gap: 2,
    lateralRemainder: round(width - 24 - 21 - 2),
    continuousRearStripMax: 7.4 },
  alternative: {
    sandwichMakerMax: [round(width - 24 - 2 - 2), 27.4, 14.6],
    plateStackMax: [24, 24, 14.6],
    plateCount: 12,
    support: 0.4,
    overheadMargin: 3,
    sideMargins: 1,
    gap: 2,
    shelfBase: 155,
    shelfClearHeight: 18,
    shelfDepth: 31.4,
  }
}));
const appliance = {name:'Sanduicheira: gabarito futuro',x:1,y:1,z:0.4,w:20,d:26,h:12};
const plates = {name:'12 pratos: pilha única hipotética',x:23,y:2.7,z:0.4,w:24,d:24,h:14.6};
const hit = (a,b) => a.x < b.x+b.w && a.x+a.w > b.x && a.y < b.y+b.d && a.y+a.d > b.y && a.z < b.z+b.h && a.z+a.h > b.z;
for (const c of cases) {
  for(const o of [appliance, plates]) {
    assert(o.x >= 1 && o.x+o.w <= c.width-1);
    assert(o.y >= 1 && o.y+o.d <= 31.4-3);
    assert(o.z+o.h <= 18-3+1e-8);
  }
  assert(!hit(appliance, plates));
}
const obstaclesByPath = {};
for(const item of [appliance, plates]) {
  const other = item === appliance ? plates : appliance;
  let collisions = 0;
  for(let i=0;i<=200;i++) {
    const moved = {...item,y:item.y+(32.4-item.y)*i/200};
    if(hit(moved,other)) collisions++;
  }
  assert.equal(collisions,0);
  obstaclesByPath[item.name] = {samples:201,collisions};
}
const result = {
  date:'2026-10-03', units:'cm', applianceOwnership:'Elias informou que não possui os quatro aparelhos consultados.',
  sources:['../Cozinha/Conferencia_aereos_2026-09-25.md','../Compatibilizacao_2026-09-30/C3_reserva.md','Saldo_da_pia.md'],
  cases, hypotheticalObjects:[appliance,plates], obstaclesByPath,
  result:'Encaixe geométrico de candidatura em C1 exige substituir duas pilhas aprovadas por uma pilha mista de 12 pratos. Altura/estabilidade/pega dessa pilha não demonstradas. Sem mudança adotada.',
  preserved:['6 copos e 4 canecas em C2','Panos e 10 potes plásticos em C3','B1/B2 com pratos de visitas e mantimentos','G1/G2/G3 e pia base C','Mixer candidato em R1'],
  unresolved:['Liquidificador completo','Batedeira completa','Potes e travessas de vidro','Bowls/tigelas/peneira/escorredor de macarrão','Cesto ventilado','Jarra e térmica'],
  limits:['Não há dimensões de sanduicheira comercial','Pratos são gabaritos anteriores, sem alturas reais','Portas, dobradiças, mãos, cabo, peso, apoio e alcance não modelados','C1 sobre a bancada a 155 cm não equivale a armário inferior','Amostragem não comprova operação física'],
};
fs.writeFileSync(path.join(__dirname,'Resultados_sanduicheira_c1.json'),JSON.stringify(result,null,2)+'\n');
const fmt = n => String(n).replace('.',',');
const table = cases.map(c=>`<tr><td>${fmt(c.width)}</td><td>${c.alternative.sandwichMakerMax.map(fmt).join(' × ')}</td><td>12 pratos juntos, até Ø24 × 14,6 de altura</td></tr>`).join('');
const diagram = `<svg viewBox="-2 -5 56 42" role="img" aria-label="C1: sanduicheira hipotética à esquerda e pilha única dos doze pratos à direita"><rect width="51.1" height="31.4" fill="#f2eee6" stroke="#355456" stroke-width=".3"/><rect x="1" y="1" width="20" height="26" rx="1" fill="#92b7a3" stroke="#355456" stroke-width=".3"/><circle cx="35" cy="14.7" r="12" fill="#c6dce2" stroke="#355456" stroke-width=".3"/><text x="11" y="13" text-anchor="middle">Sanduicheira</text><text x="11" y="16" text-anchor="middle">20 × 26 × 12</text><text x="35" y="14" text-anchor="middle">12 pratos</text><text x="35" y="17" text-anchor="middle">pilha até 14,6</text><text x="25.5" y="-2" text-anchor="middle">FUNDO · interior proposto 51,1</text><text x="25.5" y="36" text-anchor="middle">FRENTE · profundidade 31,4</text></svg>`;
const html = `<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Sanduicheira — alternativa de guarda em C1</title><style>*{box-sizing:border-box}body{margin:0;background:#f2eee7;color:#263f42;font:17px/1.6 system-ui}main{max-width:1040px;margin:auto;padding:32px}h1{font-size:clamp(29px,4vw,44px);line-height:1.15}h2{font-size:24px}.tag{font-size:13px;letter-spacing:.06em;text-transform:uppercase}.card{background:#fff;border-radius:16px;padding:24px;margin:22px 0}.note{border-left:4px solid #b18349;padding-left:16px}.grid{display:grid;grid-template-columns:1fr 1fr;gap:24px}svg{width:100%;max-height:410px}svg text{font:1.8px system-ui;fill:#263f42}table{width:100%;border-collapse:collapse;font-size:15px}td,th{border-bottom:1px solid #d7dedd;padding:10px;text-align:left}.scroll{overflow:auto}a{color:#236a73}@media(max-width:720px){main{padding:16px}.card{padding:18px}.grid{grid-template-columns:1fr}}</style></head><body><main><p class="tag">Guedala Park · 03/10/2026 · estudo local</p><h1>Uma reserva para a sanduicheira.<br>O custo seria reunir os pratos diários.</h1><p>Você informou que ainda não tem sanduicheira, liquidificador, batedeira ou mixer. Podemos usar o espaço para orientar tamanhos futuros, sem escolher marcas agora.</p><p class="note"><strong>Alternativa para avaliar, ainda não adotada.</strong> A organização aprovada continua com duas pilhas no C1. Este desenho mostra uma mudança possível e a condição que falta comprovar.</p><div class="grid"><section class="card"><h2>Organização aprovada</h2><p>C1: quatro rasos numa pilha; quatro fundos com quatro pequenos em outra. Gabaritos anteriores Ø24 e Ø21, com 2 cm entre pilhas, ocupam 47 cm de largura.</p><p>No interior proposto de 51,1, sobram 4,1 cm somados nas laterais. A faixa contínua atrás da maior pilha tem no máximo 7,4 cm antes de margens, se o prato chegar à frente.</p><p>Isso não demonstra uma reserva útil para o gabarito de sanduicheira 20 × 26 × 12. Não é prova de impossibilidade de todos os modelos ou arranjos.</p></section><section class="card"><h2>Alternativa: uma pilha + aparelho</h2>${diagram}<p>Sanduicheira hipotética à esquerda; todos os 12 pratos numa pilha à direita. O exemplo 20 × 26 × 12 cabe em planta nas duas larguras estudadas, com 2 cm entre grupos.</p><p><strong>O aparelho precisa caber completo:</strong> carcaça, alça, dobradiça, pés, cabo, plugue e qualquer acessório. Dimensões apenas da chapa não servem.</p></section></div><section class="card"><h2>Limites para a escolha futura</h2><div class="scroll"><table><tr><th>Largura interna de C1</th><th>Aparelho: largura × profundidade × altura máximas</th><th>Pilha de louça</th></tr>${table}</table></div><p>Contas: reservar 1 cm em cada lateral, 2 entre os grupos, 1 atrás, 3 à frente, apoio de 0,4 e 3 acima. São margens de ensaio. Dobradicas, mãos e abertura real podem exigir mais.</p><p>O limite maior de 23,1 na largura depende de C com 51,1 internos, ainda condicionado à compatibilização com a lavanderia. A referência anterior de 48,6 limita o aparelho a 20,6. <strong>20 × 26 × 12 é só um gabarito, sem pesquisa comercial.</strong></p></section><section class="card"><h2>O que precisa funcionar para essa mudança valer a pena</h2><p>A pilha inteira de 12 deve ficar até <strong>14,6 cm</strong>, incluindo as interfaces entre pratos diferentes, e ser estável. Não usar a altura dos pratos rasos para estimar automaticamente fundos e pequenos.</p><p>Para pegar os fundos, seria necessário tirar os pequenos; para pegar os rasos, também os fundos, na ordem ilustrativa rasos → fundos → pequenos. Essa dependência é maior que na organização aprovada. Precisa de apoio temporário e teste de manuseio.</p><p>C1 tem apoio a <strong>155 cm do piso</strong>, acima da bancada. É o nível mais baixo desse aéreo, mas não equivale a armário inferior nem comprova conforto para retirar um aparelho. Não operar a sanduicheira dentro do armário: retirar e usar na bancada na cena prevista.</p><p>A retirada frontal idealizada dos dois grupos foi amostrada em 201 posições por grupo, sem cruzamento entre eles. Portas, mãos, pesos e circulação não foram modelados. Não retirar os 12 pratos juntos como procedimento presumido.</p></section><section class="card"><h2>Saldo honesto da alternativa</h2><p>C2 continua com seis copos e quatro canecas; C3 com panos e dez potes plásticos; B1/B2, G1/G2/G3 e pia mantêm as funções anteriores. Mixer continua candidato a R1, com o custo de retirada do escorredor já identificado.</p><p>Liquidificador, batedeira, vidro, bowls/tigelas, peneira/escorredor de macarrão, cesto ventilado, jarra e térmica seguem sem destinos completos. Essa alternativa resolve apenas <strong>uma candidatura de guarda</strong>, se a pilha funcionar; não fecha o inventário.</p><p><strong>Encaminhamento:</strong> manter as duas pilhas aprovadas enquanto a pilha de 12 não estiver demonstrada. Preservar esta comparação para decidir uma mudança concreta, sem deslocar louça diária para o alto nem ocupar o baú automaticamente.</p><p><a href="Saldo_da_pia.html">Saldo da pia e mixer</a> · <a href="Resultados_sanduicheira_c1.json">Contas e hipóteses</a> · <a href="../Cozinha/Conferencia_aereos_2026-09-25.md">Organização vigente</a></p></section></main></body></html>`;
fs.writeFileSync(path.join(__dirname,'Sanduicheira_C1.html'),html);
console.log(JSON.stringify({cases,obstaclesByPath,result:result.result},null,2));
