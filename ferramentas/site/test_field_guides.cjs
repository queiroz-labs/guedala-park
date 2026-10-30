const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const read=n=>fs.readFileSync(path.join(__dirname,n),'utf8'),context=vm.createContext({});
vm.runInContext(read('src/field-data.js')+read('src/field-guide-data.js'),context);
const rows=JSON.parse(vm.runInContext('JSON.stringify(GUEDALA_FIELD_ROWS)',context));
const data=JSON.parse(vm.runInContext('JSON.stringify(GUEDALA_FIELD_GUIDE)',context));
const guides=JSON.parse(read('guias_campo.json')),codes=rows.flatMap(r=>r.partes.map(p=>p.codigo));
assert(read('Cobertura_guias.csv').split(/\r?\n/)[0].endsWith(',foto_confere'));
assert.equal(new Set(guides.map(g=>g.codigo)).size,guides.length);
assert.deepEqual(guides.map(g=>g.codigo).sort(),[...codes].sort());
assert.deepEqual(data.guias,guides,'Regerar field-guide-data.js após editar o guia');
const plans=JSON.parse(fs.readFileSync(path.join(__dirname,'../../06_Entregas/Planta_cotada/Cotas.json'),'utf8')).pranchas;
const targetIds=new Set(plans.openings.concat(plans.points).map(r=>r.id));
const rooms=new Set([...read('../../06_Entregas/Planta_cotada/Planta_cotada.svg').matchAll(/data-fp-select="([^"]+)"/g)].map(m=>m[1]));
for(const g of guides){
 assert(g.titulo_simples&&g.como.length>=2&&g.como.length<=3&&g.instrumento);
 assert(rooms.has(g.onde.comodo)||g.onde.comodo==='all');
 if(g.onde.alvo){assert(targetIds.has(g.onde.alvo));assert(data.targets[g.onde.alvo]);assert(data.overlay.includes(`data-fp-target="${g.onde.alvo}"`));}
 else assert(g.onde.orientacao.includes('só cômodo'));
 const row=rows.find(r=>r.partes.some(p=>p.codigo===g.codigo));
 if(row.como_medir==='ver protocolo de datum')assert(g.como.some(s=>/ver protocolo de datum/i.test(s)),'Não inventar descrição: '+g.codigo);
 if(g.foto){assert(g.foto_confere?.trim(),'Descrever o que foi conferido: '+g.codigo);assert(fs.existsSync(path.resolve(__dirname,'../..',g.foto)));assert(data.photos[g.foto]?.startsWith('data:image/jpeg;base64,'));assert.equal(data.photo_info[g.foto].confere,g.foto_confere);}
}
// O JPEG deve ser reduzido; lê SOF sem dependência externa para o teste.
for(const photo of Object.values(data.photos)){
 const b=Buffer.from(photo.split(',')[1],'base64');let found=false;
 for(let i=2;i<b.length;){assert.equal(b[i],0xff);const marker=b[i+1],length=b.readUInt16BE(i+2);
  if([0xc0,0xc1,0xc2].includes(marker)){assert(b.readUInt16BE(i+7)<=800);found=true;break;}i+=2+length;
 }assert(found,'JPEG sem dimensões');
}
const mod={exports:{}};vm.runInNewContext(read('src/field-core.js'),{module:mod,Date});const api=mod.exports;
let saved=null;const clock=()=> '2026-10-30T06:00:00Z',storage=()=>({getItem:()=>saved,setItem:(k,v)=>{assert.equal(k,'guedala:medidas:v1');saved=v;}});
const store=api.createStore(codes,{storage,clock}),flow=api.createGuide(['PD-QUA','DIM-01/0','DIM-01/1'],store);
flow.update({valor_mm:2584});flow.next();flow.update({valor_mm:2442});flow.next();flow.update({valor_mm:2946});flow.next();assert.equal(flow.current(),null);assert.equal(flow.missing().length,0);
const reopened=api.createStore(codes,{storage,clock});assert.equal(reopened.get('PD-QUA').valor_mm,2584);
const listStore=api.createStore(codes,{storage:()=>null,clock});
listStore.update('PD-QUA',{valor_mm:2584});listStore.update('DIM-01/0',{valor_mm:2442});listStore.update('DIM-01/1',{valor_mm:2946});
assert.deepEqual(JSON.parse(JSON.stringify(flow.exportData())),JSON.parse(JSON.stringify(listStore.exportData())));
assert.equal(api.toCsv(flow.exportData()),api.toCsv(listStore.exportData()));
const skip=api.createGuide(['PD-SAL','PD-COZ'],store);const before=JSON.stringify(store.exportData());skip.next();skip.back();assert.equal(skip.current(),'PD-SAL');assert.equal(JSON.stringify(store.exportData()),before,'Pular/voltar não altera o exportado');
store.update('PD-QUA',{valor_mm:2590});flow.goTo('PD-QUA');assert.equal(store.get(flow.current()).valor_mm,2590,'Lista e guia compartilham o mesmo registro');
const offline=read('Dia_das_chaves.html');assert(Buffer.byteLength(offline)<1024*1024);assert(!offline.includes('<script src='));assert(offline.includes('inputmode="decimal"'));assert(offline.includes('field-guide-data')||offline.includes('GUEDALA_FIELD_GUIDE'));
console.log(JSON.stringify({guides:guides.length,roomOnly:guides.filter(g=>!g.onde.alvo).length,noPhoto:guides.filter(g=>!g.foto).length,photos:Object.keys(data.photos).length,offlineBytes:Buffer.byteLength(offline),sameStore:true,sameExport:true}));
