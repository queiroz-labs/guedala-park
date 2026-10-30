const fs=require('node:fs'),vm=require('node:vm'),path=require('node:path'),assert=require('node:assert/strict');
const read=n=>fs.readFileSync(path.join(__dirname,n),'utf8'),ctx=vm.createContext({});
vm.runInContext(read('src/search-data.js')+read('src/search-core.js'),ctx);
const api=vm.runInContext('GuedalaSearch',ctx),index=JSON.parse(vm.runInContext('JSON.stringify(GUEDALA_SEARCH_INDEX)',ctx));
const keys=q=>JSON.stringify(api.find(q,index).map(r=>r.key));
assert.equal(keys('FIXAÇÃO'),keys('fixacao'));assert.equal(keys('ELÉTRICA'),keys('eletrica'));
assert.equal(api.find('zxqwx-inexistente',index).length,0);assert.equal(api.find('  ',index).length,0);
for(const kind of ['pending','choice','room','module','document','glossary'])assert(index.some(r=>r.kind===kind),kind);
for(let n=1;n<=20;n++){const code='P'+String(n).padStart(2,'0');assert(api.find(code,index).some(r=>r.kind==='module'&&r.id===code));}
assert.equal(api.find('P01',index)[0].kind,'module','Código de móvel prioriza a ficha');
for(const term of ['BC43',JSON.parse(read('current_release.json')).cadRevision,'PR','PTO','E21','TUG','DR','RT','ART','RRT','5410','13103','15575','16280','D01','D06','T0'])assert(api.find(term,index).some(r=>r.kind==='glossary'),term+' no glossário');
assert.equal(new Set(index.map(r=>r.key)).size,index.length);
const destination={pending:'architect',choice:'decisions',room:'model',module:'model',document:'documents',glossary:'architect'};
for(const kind of new Set(index.map(r=>r.kind))){
 const r=index.find(x=>x.kind===kind),calls=[],adapter={tab:t=>calls.push(['tab',t])};for(const k of Object.keys(destination))adapter[k]=v=>calls.push(['item',v.id]);
 assert(api.navigate(r,adapter));assert.deepEqual(calls,[['tab',destination[kind]],['item',r.id]],'Navegar à aba e ao registro certo');
}
assert.equal(api.navigate({kind:'inexistente'},{}),false);
const ui=read('src/search-ui.js');assert(ui.includes('Nenhum resultado'));assert(ui.includes("event.key==='/'"));assert(ui.includes("event.key==='Escape'"));assert(ui.includes('scrollIntoView'));
console.log('Busca: acentos, caixa, tipos, P01–P20, sem resultado e rotas até cada registro');
