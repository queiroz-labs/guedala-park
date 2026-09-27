const fs=require('fs'),vm=require('vm'),assert=require('node:assert/strict'),path=require('path');
const root=path.resolve(__dirname,'../..'),src=path.join(root,'01_Projeto/Estudo_interativo/src');
const data=fs.readFileSync(path.join(src,'data.js'),'utf8'),app=fs.readFileSync(path.join(src,'app.js'),'utf8');
const context={matchMedia:()=>({matches:true}),document:{getElementById:()=>null}};
vm.createContext(context);
vm.runInContext(data+'\n'+app.slice(0,app.indexOf("const canvas=$('scene')")),context);
const check=function(){
const cases=[];
for(const dry of ['stored','high','low'])for(const inside of [false,true])for(const office of ['work','guest']){
state.dry=dry;state.inside=inside;state.office=office;buildScene();
if(nodes.some(n=>['x','y','z','w','d','h'].some(k=>!Number.isFinite(n[k]))||n.w<=0||n.d<=0||n.h<=0))throw Error('Invalid geometry');
if(nodes.filter(n=>n.id==='ps5').length!==1)throw Error('Duplicate PS5');
for(const node of nodes)if(node.id&&node.id!=='decor'&&!ITEMS.some(o=>o.id===node.id))throw Error('Missing item '+node.id);
cases.push({dry,inside,office,nodes:nodes.length});
}
if(new Set(ITEMS.map(o=>o.id)).size!==ITEMS.length)throw Error('Duplicate ids');
for(const id of Object.keys(INTERNALS))if(!ITEMS.some(o=>o.id===id))throw Error('Missing internal item '+id);
const get=id=>ITEMS.find(o=>o.id===id);
if(!get('lowdrawer').notes.includes('cabeças retiradas'))throw Error('Low drawer decision missing');
if(!get('kitchenlight').notes.includes('abertura livre'))throw Error('Door condition missing');
if(!INTERNALS.kitchenbase.rows.some(r=>r[0].includes('40 cm')))throw Error('Drawer size missing');
if(!PROJECT.materials.find(m=>m.id==='paint').rooms.includes('lavanderia'))throw Error('Paint continuity missing');
return {revision:PROJECT.revision,items:ITEMS.length,interiors:Object.keys(INTERNALS).length,cases,checks:['Unique item ids','12 combinations of drying/cutaway/office states','Finite positive dimensions','Exactly one PS5','Every drawn item has a card','G1/G2/G3 and fixed cleaning handles','Ceiling lamp door clearance condition','Laundry paint continuity']};
};
const result=vm.runInContext('('+check.toString()+')()',context);
assert.equal(result.cases.length,12);
for(const f of ['app.js','data.js','experience.js','depth-renderer.js'])new vm.Script(fs.readFileSync(path.join(src,f),'utf8'));
for(const f of ['.site/index.html','.site/moodboard/index.html']){
const html=fs.readFileSync(path.join(root,f),'utf8');assert.ok(html.includes('R09 · cozinha e lavanderia'));
assert.ok(!/\/\*(CSS|DATA|APP|DEPTH|EXPERIENCE_JS|EXPERIENCE_CSS|WARDROBE)\*\//.test(html));
assert.ok(html.includes('saco removível'));assert.ok(html.includes('20 A'));assert.ok(html.includes('frentes retas'));
}
fs.writeFileSync(path.join(root,'01_Projeto/Estudo_interativo/Verificacao_R09.json'),JSON.stringify({result:'PASSOU',...result},null,2)+'\n');
console.log(JSON.stringify({result:'PASSOU',items:result.items,cases:result.cases.length,checks:result.checks},null,2));
