const fs=require('node:fs'),vm=require('node:vm'),path=require('node:path'),assert=require('node:assert/strict');
const src=path.join(__dirname,'src'),read=n=>fs.readFileSync(path.join(src,n),'utf8');
const app=read('app.js'),shell=read('shell.html'),workshop=read('workshop.js');

// Quatro abas; a planta cotada é aberta de dentro do Apartamento.
const nav=shell.match(/<nav aria-label="Conteúdo">([\s\S]*?)<\/nav>/)[1];
assert.deepEqual([...nav.matchAll(/data-tab="(\w+)">([^<]+)</g)].map(m=>[m[1],m[2]]),[['model','Apartamento'],['mood','Cômodos'],['decisions','Escolhas'],['documents','Documentos']]);
assert(!nav.includes('floorplan'),'Planta com medidas não é aba');
assert(read('floorplan-ui.js').includes('.viewbar .viewtools'),'Botão da planta fica na barra do Apartamento');

// Selo único: todo item cai em um dos três grupos; "A conferir" é a quarta leitura.
const ctx=vm.createContext({});
vm.runInContext(read('data.js')+'\n'+app.slice(app.indexOf('const STATUS_GROUPS'),app.indexOf('function needsCheck')),ctx);
const groups=JSON.parse(vm.runInContext('JSON.stringify(Object.keys(STATUS_GROUPS))',ctx));
assert.deepEqual(groups,['Decidido','Em estudo','Futuro']);
const unmapped=JSON.parse(vm.runInContext('JSON.stringify([...new Set(ITEMS.map(o=>o.choice).filter(c=>!STATUS_OF[c]))])',ctx));
assert.deepEqual(unmapped,[],'Rótulo sem grupo: '+unmapped.join(', '));
const tally=JSON.parse(vm.runInContext('JSON.stringify(ITEMS.reduce((t,o)=>(t[statusGroup(o)]=(t[statusGroup(o)]||0)+1,t),{}))',ctx));
assert(Object.keys(tally).every(g=>groups.includes(g)));

// Cômodos lista nomes e selos; medidas e descrição ficam só em Escolhas e na ficha.
const mood=app.slice(app.indexOf('function buildMood'),app.indexOf('function renderMood'));
assert(!mood.includes('o.dimensions')&&!mood.includes('o.notes'),'Cômodos não repete medidas nem descrição');
assert(mood.includes('Documentos deste cômodo'));

// Endereços antigos continuam válidos.
const tabs=vm.runInContext(workshop.match(/const WORK_TABS=\{[^}]+\};/)[0]+'WORK_TABS',vm.createContext({}));
for(const [old,target] of [['materiais','mood'],['planta','floorplan'],['documentos','documents'],['ambientes','model'],['escolhas','decisions']])assert.equal(tabs[old],target,old);
console.log(JSON.stringify({tabs:4,status:tally,legacyLinks:Object.keys(tabs).length}));
