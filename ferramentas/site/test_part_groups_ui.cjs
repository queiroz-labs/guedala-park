const fs=require('node:fs'),vm=require('node:vm'),path=require('node:path'),assert=require('node:assert/strict');
const src=path.join(__dirname,'src'),ui=fs.readFileSync(path.join(src,'fabrication-ui.js'),'utf8');
const dataContext=vm.createContext({});vm.runInContext(fs.readFileSync(path.join(src,'fabrication-data.js'),'utf8'),dataContext);
const modules=JSON.parse(vm.runInContext('JSON.stringify(FABRICATION_DATA.modules)',dataContext));let csvBlob;
const ctx=vm.createContext({Blob,esc:s=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/"/g,'&quot;'),mm:n=>String(n),workGuide:m=>({fabrication:modules[m.code]}),previousPartsTable:()=>'',download:b=>{csvBlob=b;}});
vm.runInContext(ui.slice(ui.indexOf('function fabPartGroups'),ui.indexOf('const previousShowModule'))+'\n'+ui.slice(ui.indexOf('exportPieces=function'),ui.indexOf('\nprintModule=')),ctx);
(async()=>{
 for(const [code,f] of Object.entries(modules)){
  const html=vm.runInContext(`partsTable({code:'${code}'})`,ctx),print=vm.runInContext(`partsTable({code:'${code}'},true)`,ctx);
  assert.equal((html.match(/data-piece-row=/g)||[]).length,f.panelGroups.length);
  assert.equal((print.match(/data-piece-row=/g)||[]).length,f.panelGroups.length);
  for(const p of f.panels){assert(print.includes(p.id));assert(html.includes(p.id));}
  assert(!print.includes('<button'));
  vm.runInContext(`exportPieces({code:'${code}'})`,ctx);const lines=(await csvBlob.text()).trim().split('\r\n');
  assert.equal(lines.length-1,f.panelGroups.length);
  const quantities=lines.slice(1).map(line=>Number(line.match(/^(?:"(?:[^"]|"")*";){3}"(\d+)"/)[1]));
  assert.equal(quantities.reduce((a,b)=>a+b,0),f.panels.length);
 }
 const scene=vm.createContext({matchMedia:()=>({matches:true})}),app=fs.readFileSync(path.join(src,'app.js'),'utf8');
 vm.runInContext(['data.js','cad-data.js','visual-finishes.js','cad-sync.js'].map(n=>fs.readFileSync(path.join(src,n),'utf8')).join('\n')+'\n'+app.slice(0,app.indexOf("const canvas=$('scene')")),scene);
 const ids=modules.P01.panelGroups.find(g=>g.ids.includes('Peca211')).ids;
 vm.runInContext(`state.focusPart=${JSON.stringify(ids)};buildScene()`,scene);
 assert.deepEqual(JSON.parse(vm.runInContext('JSON.stringify(nodes.filter(n=>n.finishHighlight).map(n=>n.source))',scene)).sort(),[...ids].sort());
 vm.runInContext("state.focusPart='Peca211';buildScene()",scene);
 assert.equal(vm.runInContext('nodes.filter(n=>n.finishHighlight).length',scene),1);
 console.log(JSON.stringify({modules:20,webPrintCsvConsistent:true,groupSelection:ids.length,singleSelection:1}));
})().catch(error=>{console.error(error);process.exitCode=1;});
