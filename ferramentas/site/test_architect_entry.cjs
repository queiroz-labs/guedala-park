const fs=require('node:fs'),vm=require('node:vm'),path=require('node:path'),assert=require('node:assert/strict');
const read=p=>fs.readFileSync(path.join(__dirname,p),'utf8'),ctx=vm.createContext({URLSearchParams});
vm.runInContext(read('src/architect-data.js')+read('src/architect-core.js'),ctx);const d=JSON.parse(vm.runInContext('JSON.stringify(GUEDALA_ARCHITECT)',ctx));
const core=vm.runInContext('GuedalaArchitect',ctx),state=read('../../ESTADO_ATUAL.md');
assert.equal(core.entryTab('?perfil=arquiteto'),'architect');assert.equal(core.entryTab(''),null);assert.equal(core.entryTab('?perfil=arquiteto&aba=materiais'),null);
assert.equal(d.progress.length,9);for(const p of d.progress){assert(state.includes(p.percent));assert(state.includes(p.stage));assert.equal(p.source,'ESTADO_ATUAL.md');}
assert.equal(d.overview.model,JSON.parse(read('current_release.json')).cadRevision);
assert(d.overview.project.includes('40,18'));assert(d.overview.project.includes('Não entregue'));
assert(d.overview.notice.includes('nominal'));assert.equal(d.shortcuts.length,6);assert.equal(d.disciplines.length,8);
for(const p of [...d.shortcuts,...d.disciplines])if(p.path)assert(fs.existsSync(path.resolve(__dirname,'../..',p.path)),p.path);
for(const p of d.disciplines)if(!p.owners.includes('a definir')){assert(p.ownerSource&&p.ownerQuote);assert(read('../../'+p.ownerSource).toLowerCase().includes(p.ownerQuote.toLowerCase()));}
vm.runInContext(read('src/data.js'),ctx);const pending=vm.runInContext('ITEMS.filter(o=>o.measure!=="Projeto aprovado").length',ctx);assert.equal(d.itemResponsibilities.length,pending);
for(const r of d.itemResponsibilities){assert(r.owners.length);if(!r.owners.includes('a definir'))assert(r.source&&r.codes.length&&r.roles.length);}
const rows=[...d.disciplines,...d.itemResponsibilities],counts=core.ownerCounts(rows);
assert.equal(core.ownerItems(rows,'todos').length,8+pending);assert(counts.RT>0);assert(counts['a definir']>0);
assert.equal(core.ownerItems(rows,'RT').length,counts.RT);assert(core.ownerItems(rows,'a definir').every(r=>r.owners.includes('a definir')));
assert(read('src/shell.html').includes('id="architect"'));assert(read('src/architect-ui.js').includes('GUEDALA_ARCHITECT'));assert(!read('src/shell.html').includes('Cury Guedala Park III'),'Textos vêm dos dados');
console.log('Entrada: 9 etapas da fonte, 8 disciplinas, 6 atalhos, responsáveis com fonte, perfil e links legados');
