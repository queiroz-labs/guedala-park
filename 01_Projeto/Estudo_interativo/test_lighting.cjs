const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict'),path=require('node:path');
const src=path.join(__dirname,'src');
const ctx=vm.createContext({console,matchMedia:()=>({matches:false})});
const app=fs.readFileSync(path.join(src,'app.js'),'utf8');
vm.runInContext(['data.js','cad-data.js','cad-sync.js','lighting.js'].map(n=>fs.readFileSync(path.join(src,n),'utf8')).join('\n')+'\n'+app.slice(0,app.indexOf("const canvas=$('scene')")),ctx);
const run=s=>vm.runInContext(s,ctx);
assert.equal(run("enhancedLighting({room:'sala',view:'iso',lighting:'after'})"),true);
for(const room of ['all','quarto','banho','escritorio'])assert.equal(run(`enhancedLighting({room:'${room}',view:'iso',lighting:'after'})`),false);
assert.equal(run("enhancedLighting({room:'sala',view:'top',lighting:'after'})"),false);
run('buildScene();');
// Original factors remain exact in Before, including underside and rotated normals.
assert.equal(run(`nodes.flatMap(mesh).every(f=>JSON.stringify(faceLighting(f,false))===JSON.stringify(rgb(shade(f.c,f.normal[1]?1.04:.80+.11*f.normal[0]-.07*f.normal[2])).map(v=>v/255)))`),true);
const snapshot=()=>JSON.parse(run(`JSON.stringify(contactPatches(nodes.filter(n=>n.room==='sala').flatMap(mesh)))`));
const closed=snapshot();assert(closed.length>0&&closed.length<=48);
run("state.sofa='open';state.table='extended';state.dining='use';buildScene();");
const open=snapshot();assert.notDeepEqual(open.map(p=>p.rect),closed.map(p=>p.rect),'contacts must follow changed furniture');
const kitchen=JSON.parse(run("JSON.stringify(contactPatches(nodes.filter(n=>n.room==='cozinha').flatMap(mesh)))"));
assert(kitchen.length>0);
assert([...open,...kitchen].every(p=>p.rect.every(Number.isFinite)&&p.settings.every(Number.isFinite)&&p.settings[1]>0&&p.settings[1]<=.25));
// Suspended objects may not cast a floor contact across a large gap.
assert.equal(run(`(()=>{const f=nodes.filter(n=>n.room==='cozinha').flatMap(mesh);return contactPatches(f).every(p=>{const n=nodes.find(n=>n.key===p.source);return n.y-p.settings[0]<=LIGHTING_CONFIG.contact.maxGap+.1;});})()`),true);
console.log(JSON.stringify({ok:true,salaBefore:closed.length,salaMoved:open.length,cozinha:kitchen.length,beforeLightingExact:true,scopeRestricted:true,contactsFollowFurniture:true}));
