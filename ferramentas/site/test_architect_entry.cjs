const fs=require('node:fs'),vm=require('node:vm'),path=require('node:path'),assert=require('node:assert/strict');
const read=p=>fs.readFileSync(path.join(__dirname,p),'utf8'),ctx=vm.createContext({URLSearchParams});
vm.runInContext(read('src/architect-data.js')+read('src/architect-core.js'),ctx);const d=JSON.parse(vm.runInContext('JSON.stringify(GUEDALA_ARCHITECT)',ctx));
const core=vm.runInContext('GuedalaArchitect',ctx),state=read('../../ESTADO_ATUAL.md');
assert.equal(core.entryTab('?perfil=arquiteto'),'architect');assert.equal(core.entryTab(''),'architect');assert.equal(core.entryTab('?perfil=arquiteto&aba=materiais'),null);
for(const id of ['model','mood','decisions','documents','chaves','obra','floorplan']){assert.equal(core.entryTab('','#'+id),null);assert.equal(core.hashTab('#'+id),id);}
assert.equal(core.hashTab('#planta-pe-direito'),'floorplan');assert.equal(core.hashTab('#scene'),'model');assert.equal(core.hashTab('#%XX'),null);
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
assert.equal(d.glossary.filter(g=>/^P\d{2}$/.test(g.term)).length,20);
for(const g of d.glossary)assert(fs.existsSync(path.resolve(__dirname,'../..',g.path)),g.path);
assert.deepEqual(Object.keys(d.tabContexts).sort(),['architect','chaves','decisions','documents','floorplan','model','mood','obra']);
for(const c of Object.values(d.tabContexts))assert(c.text&&c.revision);
const release=JSON.parse(read('current_release.json'));assert.equal(d.tabContexts.decisions.revision,release.cadRevision+'/'+release.lightingRevision);assert.equal(d.tabContexts.documents.revision,release.packageRevision+'/'+release.fabricationRevision);
assert.equal(d.globalNotice,'Tudo aqui é de projeto; medidas reais só depois das chaves');
assert(read('src/context-ui.js').includes('glossaryDialog'));assert(read('src/context-ui.js').includes('architect-tools-label'));
console.log('Entrada: 9 etapas da fonte, 8 disciplinas, 6 atalhos, responsáveis com fonte, perfil e links legados');

const sealLabels=new Set(d.statusHelp.flatMap(s=>s.labels));
for(const label of vm.runInContext('ITEMS.map(o=>o.choice).concat(PROJECT.materials.map(m=>m.status))',ctx))assert(sealLabels.has(label),'Selo sem definição: '+label);
for(const label of ['Decidido','a definir','Depende das medidas reais','Atual','Conferir antes de fabricar'])assert(sealLabels.has(label));
for(const seal of d.statusHelp){assert(d.glossary.some(g=>g.id===seal.id&&g.definition===seal.definition));assert(!/aprovad|liberad/i.test(seal.label));}

vm.runInContext(read('src/workshop-docs.js'),ctx);
for(const label of vm.runInContext('Object.values(MODULE_GUIDANCE).flatMap(m=>[...(m.fabrication?.hardwareRows||[]),...(m.fabrication?.decisions||[]),...(m.fabrication?.finishSpecs||[])].map(r=>r.status))',ctx))assert(sealLabels.has(label),'Selo de ficha sem definição: '+label);
assert(sealLabels.has('Confira antes de fabricar'));
