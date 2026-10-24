// Gera 01_Projeto/Caderno_de_especificacoes_R01.md a partir de src/data.js (mesma fonte do site).
// Uso: node gerar_caderno.cjs
const fs=require('fs'),path=require('path');
const src=fs.readFileSync(path.join(__dirname,'src/data.js'),'utf8');
const {PROJECT,ITEMS}=new Function(src+';return {PROJECT,ITEMS};')();

const cell=s=>String(s??'').replace(/\|/g,'/').replace(/\s+/g,' ').trim();
const first=s=>{s=cell(s);const m=s.match(/^.{20,240}?[.;](\s|$)/);return (m?m[0].trim():s.slice(0,240)).replace(/;$/,'.');};
const rooms=PROJECT.rooms.filter(r=>r.id!=='all');

let out=`# Caderno de especificações — R01

Gerado em ${new Date().toISOString().slice(0,10)} por \`Estudo_interativo/gerar_caderno.cjs\`, a partir dos mesmos dados do site interativo (geometria ${PROJECT.revision.split('·').pop().trim()}). Para atualizar, corrija \`src/data.js\` e rode o script de novo; não edite este arquivo à mão.

**Como ler a coluna "Situação":** *Escolhido/Aprovado* = decisão tomada; *Aprovado para desenvolver/Direção aprovada* = o quê está decidido e o como segue nas [pendências](../05_Entregas/Fichas_fabricacao_R13/Pendencias.html); *Parcial/Em estudo/Futuro/Existente* = ainda aberto, adiado ou bem já existente. Medidas são de referência, não executivas. Nenhum item está comprado.

Unidade: ${PROJECT.name} · ${PROJECT.unit} · ${PROJECT.area} · 127 V · gás natural. Programa: [Programa de necessidades R01](Programa_de_necessidades_R01.md).

## 1. Materiais e acabamentos

| Material | Ambientes | Situação | Observação |
|---|---|---|---|
`;
const roomName=id=>id==='all'?'Todos':(rooms.find(r=>r.id===id)||{name:id}).name;
for(const m of PROJECT.materials){if(!m.rooms.length)continue;out+=`| ${cell(m.name)} | ${m.rooms.map(roomName).join(', ')} | ${cell(m.status)} | ${first(m.note)} |\n`;}

out+='\n## 2. Itens por ambiente\n';
let n=2;
for(const r of rooms){
  const its=ITEMS.filter(i=>i.room===r.id);if(!its.length)continue;
  out+=`\n### 2.${++n-2}. ${r.name}\n\n| Item | Situação | Medidas de referência | Observação |\n|---|---|---|---|\n`;
  for(const i of its)out+=`| ${cell(i.name)} | ${cell(i.choice)} | ${cell(i.dimensions)} | ${first(i.notes)} |\n`;
}
const kind=c=>/desenvolver|Direção|plano/.test(c)?'dev':/^(Aprovado|Escolhido|Modelo escolhido|Primeira opção|Temperaturas)/.test(c)?'ok':'open';
const tally=k=>ITEMS.filter(i=>kind(i.choice||'')===k).length;
out+=`\n## 3. Resumo\n\n${ITEMS.length} itens: ${tally('ok')} decididos, ${tally('dev')} decididos com execução em desenvolvimento e ${tally('open')} parciais, futuros, existentes ou em revisão.\n\nEspecificação técnica de marcenaria (chapas, ferragens, furação por peça): [fichas R14](../05_Entregas/Fichas_fabricacao_R13/index.html).\n`;
fs.writeFileSync(path.join(__dirname,'..','Caderno_de_especificacoes_R01.md'),out,'utf8');
console.log('ok',ITEMS.length,'itens');
