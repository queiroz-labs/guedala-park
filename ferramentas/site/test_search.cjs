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
for(const term of ['BC43',JSON.parse(read('current_release.json')).cadRevision,'PR','PTO','E21','GN','TUG','DR','RT','ART','RRT','5410','13103','15575','16280','D01','D02','D03','D04','D05','D06','T0',...Array.from({length:9},(_,i)=>'T0'+(i+1))])assert(api.find(term,index).some(r=>r.kind==='glossary'),term+' no glossário');
assert.equal(new Set(index.map(r=>r.key)).size,index.length);
const destination={pending:'architect',choice:'decisions',room:'model',module:'model',document:'documents',glossary:'architect',download:'documents'};
for(const kind of new Set(index.map(r=>r.kind))){
 const r=index.find(x=>x.kind===kind),calls=[],adapter={tab:t=>calls.push(['tab',t])};for(const k of Object.keys(destination))adapter[k]=v=>calls.push(['item',v.id]);
 assert(api.navigate(r,adapter));assert.deepEqual(calls,[['tab',destination[kind]],['item',r.id]],'Navegar à aba e ao registro certo');
}
assert.equal(api.navigate({kind:'inexistente'},{}),false);
const ui=read('src/search-ui.js');assert(ui.includes('Nenhum resultado'));assert(ui.includes("event.key==='/'"));assert(ui.includes("event.key==='Escape'"));assert(ui.includes('scrollIntoView'));
console.log('Busca: acentos, caixa, tipos, P01–P20, sem resultado e rotas até cada registro');

for(const term of ['Detalhamento pendente','Responsável a definir','Opção para comparar'])assert(api.find(term,index).some(r=>r.kind==='glossary'),term);

// Casos de uso: o nome comercial sozinho não descreve o que o aparelho faz.
for(const query of ['máquina de lavar','maquina de lavar','lavar','lava e seca','lava','lg','lavadora','secadora','LGVC4','VC4','roupa lavar','máquinas de lavar','lavar na lavanderia']){
 const results=api.find(query,index);
 assert.equal(results[0]?.key,'choice:washer',query+' deve priorizar a máquina');
}
for(const [query,id] of [
 ['refrigerador','fridge'],['fogão','cooktop'],['fritadeira sem óleo','airfryer'],
 ['microondas','microwave'],['máquina de café','coffeemaker'],['filtro de água','filter'],
 ['aquecedor a gás','heater'],['privada','toilet'],['vaso sanitário','toilet'],
 ['chuveiro','shower'],['torneira banheiro','bath tap'],['espelheira','bathmirror'],
 ['televisão sala','tv50'],['televisor escritório','tv43'],['caixa de som','soundbar'],
 ['playstation','ps5'],['escrivaninha','desk'],['roupeiro','wardrobe'],
 ['cesto roupa suja','laundrybasket'],['lixo reciclável','recycling'],
 ['lâmpada cozinha','kitchenlight'],['tomadas lavanderia','laundrypower']
])assert(api.find(query,index).some(r=>r.key==='choice:'+id),query+' deve encontrar '+id);
assert(api.find('preços',index).some(r=>r.kind==='document'),'Sinônimos também nos documentos');
assert.equal(api.find('de e para',index).length,0,'Preposições sozinhas não buscam tudo');
assert.equal(api.find('máquina de lavar inexistente',index).length,0,'Não descarta palavras desconhecidas');
assert.equal(api.find('P01',index)[0].key,'module:P01','Código exato preservado');
const dataContext=vm.createContext({});vm.runInContext(read('src/data.js'),dataContext);
const items=JSON.parse(vm.runInContext('JSON.stringify(ITEMS)',dataContext));
const aliases=JSON.parse(read('search_aliases.json'));
assert.deepEqual(Object.keys(aliases).sort(),items.map(r=>r.id).sort(),'Todo item deve ter nomes comuns revisados');
for(const item of items){
 assert(api.find(item.name,index,index.length).some(r=>r.key==='choice:'+item.id),'Nome completo: '+item.id);
}
console.log('Busca ampliada: nomes comuns de todos os itens, sinônimos, plurais, contexto e prioridade');

for(const [query,id] of [
 ['geladera','fridge'],['geladiera','fridge'],['geladdeira','fridge'],['geladejra','fridge'],
 ['geladera electrolux','fridge'],['microondas','microwave'],['microondsa','microwave'],
 ['microndas','microwave'],['maquina de lavra','washer'],['purificadr','filter'],
 ['escrivanina','desk'],['refrijerador','fridge']
])assert(api.find(query,index).some(r=>r.key==='choice:'+id),query+' deve encontrar '+id);
assert.equal(api.find('geladera',index)[0]?.key,'choice:fridge');
const sample=[
 {key:'choice:mesa',kind:'choice',id:'mesa',title:'Mesa',tokens:''},
 {key:'choice:meta',kind:'choice',id:'meta',title:'Meta',tokens:''},
 {key:'module:P01',kind:'module',id:'P01',title:'P01',tokens:''}
];
assert.equal(api.find('meta',sample)[0]?.key,'choice:meta','Exato antes de palavra parecida');
assert.equal(api.find('P02',sample).length,0,'Não corrige código para outro móvel');
assert.equal(api.find('P0I',sample).length,0,'Não corrige identificadores alfanuméricos');
assert.equal(api.find('5411',index).some(r=>r.id==='5410'),false,'Não troca número de norma');
assert.equal(api.find('gldrxzz',index).length,0,'Não aproxima palavra distante');
assert.equal(api.find('geladera xzqwx',index).length,0,'Todas as palavras continuam necessárias');
console.log('Erros de digitação: omissão, repetição, substituição, inversão; exatos e códigos preservados');
