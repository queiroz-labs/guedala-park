const fs=require('node:fs'),vm=require('node:vm'),path=require('node:path'),assert=require('node:assert/strict');
const src=path.join(__dirname,'src'),app=fs.readFileSync(path.join(src,'app.js'),'utf8'),ctx=vm.createContext({matchMedia:()=>({matches:true})});
vm.runInContext(['data.js','cad-data.js','visual-finishes.js','cad-sync.js'].map(n=>fs.readFileSync(path.join(src,n),'utf8')).join('\n')+'\n'+app.slice(0,app.indexOf("const canvas=$('scene')")),ctx);
const run=s=>vm.runInContext(s,ctx),json=s=>JSON.parse(run('JSON.stringify('+s+')'));
const interiors=json('Object.keys(INTERNALS)');assert.equal(interiors.length,12);
run('buildScene()');const before=json('state'),original=json('nodes.map(n=>n.source||n.key)');
const checks=[];
for(const id of interiors){
 const result=json(`storageModel('${id}').map(n=>({source:n.source,module:n.module,cover:isInteriorCover(n)}))`),expected=json(`CAD_DATA.parts.filter(p=>STORAGE_MODULES['${id}'].includes(p.module)&&!isInteriorCover(p)).map(p=>p.source)`);
 assert(result.length,id);assert.deepEqual(result.map(n=>n.source),expected,id);assert(result.every(n=>!n.cover));
 checks.push({id,modules:json(`STORAGE_MODULES['${id}']`),parts:result.length});
}
assert.deepEqual(json('state'),before);assert.deepEqual(json('nodes.map(n=>n.source||n.key)'),original,'Modal must not change scene');
const covers=['FrenteVizinhaR18','FaixaQuinaAR04','FaixaQuinaBR04'];
for(const inside of [false,true]){
 run(`state.inside=${inside};buildScene()`);const ids=json('nodes.map(n=>n.source)');
 for(const id of covers)assert.equal(ids.includes(id),!inside,id);
 for(const support of ['ApoioPortaBR04','ApoioOpostoR002','LateralApoioPrincipal'])assert(ids.includes(support),support);
}
assert.equal(json("storageModel('wardrobe').filter(n=>n.front).length"),0);
assert.equal(run("INTERNALS.bathvanity.title.includes('portas de correr')"),true);
assert.equal(run("INTERNALS.bathmirror.status.includes('duas prateleiras')"),true);
assert(!app.includes('WARDROBE_IMAGE'));assert(!app.includes('kitchen-elevation'));
console.log(JSON.stringify({interiors:checks,allUseCurrentCad:true,coversOnlyHiddenInCut:true,sceneUnchanged:true}));
