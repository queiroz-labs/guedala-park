// Atalhos da capa: abas e alvos existentes, fora de áreas ocultas por CSS, e pontos de encaixe que outros módulos usam.
const fs=require('node:fs'),vm=require('node:vm'),path=require('node:path'),assert=require('node:assert/strict');
const read=p=>fs.readFileSync(path.join(__dirname,p),'utf8'),ctx=vm.createContext({URLSearchParams});
vm.runInContext(read('src/architect-data.js'),ctx);const d=JSON.parse(vm.runInContext('JSON.stringify(GUEDALA_ARCHITECT)',ctx));
const shell=read('src/shell.html'),css=read('src/mobile-ux.css');
const tabs=new Set([...shell.matchAll(/data-tab="(\w+)"/g)].map(m=>m[1]).concat(['floorplan']));
// Ids criados em tempo de execução (downloads-ui.js e floorplan-ui.js) e ids estáticos do shell.
const runtimeIds=new Set(['downloads-architect','downloads-documents','floorplan']);
const staticIds=new Set([...shell.matchAll(/\sid="([\w-]+)"/g)].map(m=>m[1]));
const hidden=(css.match(/\.owner-badges[^{]*\{display:none!important\}/)||[''])[0];
for(const a of [...d.entryPaths,d.entryPlan]){
  assert(tabs.has(a.tab),'aba inexistente: '+a.tab);
  assert(staticIds.has(a.target)||runtimeIds.has(a.target)||a.target===a.tab,'alvo inexistente: '+a.target);
  assert(!/^(arch-|owner-|entry-responsibilities)/.test(a.target),'alvo em área oculta: '+a.target);
}
assert(hidden.includes('.arch-disciplines'),'"Quem decide" deveria estar oculto por CSS');
// downloads-ui.js encaixa a seção antes de um bloco da capa: esse bloco precisa existir em architect-ui.js.
const dl=read('src/downloads-ui.js'),ui=read('src/architect-ui.js');
const anchor=dl.match(/where==='architect'\?'\.([\w-]+)'/)[1];
assert(ui.includes('class="entry-more '+anchor+'"')||ui.includes('class="'+anchor+'"'),'ponto de encaixe dos downloads sumiu da capa: '+anchor);
// Busca: resultados "pending" não podem focar elementos ocultos.
const search=read('src/search-ui.js');
assert(!/pending:r=>\{[^}]*(owner-|'arch-)/.test(search),'busca ainda aponta para "Quem decide" oculto');
console.log('Atalhos da capa: abas, alvos, encaixe dos downloads e busca sem alvos ocultos OK');
