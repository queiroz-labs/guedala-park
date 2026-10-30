const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const read=n=>fs.readFileSync(path.join(__dirname,'src',n),'utf8'),context=vm.createContext({Date});
vm.runInContext(read('field-core.js')+'\n'+read('work-core.js')+'\n'+read('work-data.js'),context);
const api=context.GuedalaWork,rows=context.GUEDALA_WORK_PLAN.etapas,ids=rows.map(r=>r.id);
const clean=x=>JSON.parse(JSON.stringify(x));
let time='2026-10-30T10:00:00.000Z',content={};
const storage={getItem:k=>content[k]??null,setItem:(k,v)=>{content[k]=v;}};
const options={storage:()=>storage,clock:()=>time};
const a=api.createStore(ids,options);assert.equal(a.state().done,0);
a.set(ids[1],true);assert.equal(a.state().done,1);assert.equal(a.get(ids[1]),true);
const b=api.createStore(ids,options);assert.equal(b.get(ids[1]),true,'Reabertura preserva a marcação');
time='2026-10-30T10:01:00.000Z';b.set(ids[2],true);
time='2026-10-30T10:02:00.000Z';a.set(ids[1],false);
const c=api.createStore(ids,options);assert.equal(c.get(ids[1]),false);assert.equal(c.get(ids[2]),true,'Abas não apagam outras etapas');
assert.notEqual(api.KEY,context.GuedalaField.KEY,'Obra não colide com levantamento');
const exported=JSON.stringify(c.exportData()),d=api.createStore(ids,{storage:()=>null,clock:()=>time});
assert.equal(d.state().persistent,false);d.importFile(exported);assert.equal(d.get(ids[2]),true);
time='2026-10-30T10:03:00.000Z';d.set(ids[2],false);assert.equal(d.importFile(exported).older,1);assert.equal(d.get(ids[2]),false);
const before=clean(d.exportData());
for(const corrupt of [p=>p.etapas.push(p.etapas[0]),p=>p.etapas[0].feito='sim',p=>p.etapas[0].data_hora='2026-02-30T10:00:00Z',p=>p.tipo='medidas',p=>p.etapas.push({id:ids[3],feito:true,data_hora:'ontem'})]){
  const p=JSON.parse(exported);corrupt(p);assert.throws(()=>d.importFile(JSON.stringify(p)));
  assert.deepEqual(clean(d.exportData()),before,'Importação inválida é atômica');
}
const revised=api.createStore(ids.slice(2),options);assert.equal(revised.state().unknown,1);assert.equal(revised.state().done,1,'Etapa alterada não herda feito');
const importedOld=JSON.parse(exported);importedOld.etapas.push({id:'etapa-ffffffffffffffff',feito:true,data_hora:time});
assert.equal(d.importFile(JSON.stringify(importedOld)).ignored,1);assert.equal(d.get('etapa-ffffffffffffffff'),false);
const broken=api.createStore(ids,{storage:()=>{throw Error('SecurityError');},clock:()=>time});broken.set(ids[0],true);assert.equal(broken.get(ids[0]),true);assert.equal(broken.exportData().etapas.length,1);
let badStorage={getItem:()=>null,setItem:()=>{throw Error('QuotaExceededError');}};
const full=api.createStore(ids,{storage:()=>badStorage,clock:()=>time});full.set(ids[0],true);assert.equal(full.state().persistent,false);assert.equal(full.get(ids[0]),true);
badStorage={getItem:()=>'{quebrado',setItem:()=>{throw Error('Não sobrescrever o original');}};
const corrupt=api.createStore(ids,{storage:()=>badStorage,clock:()=>time});corrupt.set(ids[0],true);assert.equal(corrupt.state().persistent,false);
// O mesmo id identifica as repetições semanais; a contagem é por etapa única.
assert.equal(ids.length,10);assert.equal(new Set(ids).size,10);
assert(rows.some(r=>r.inicio===0&&r.fim===1));
assert(read('shell.html').includes('id="obra"'));assert(read('work-ui.js').includes('workDocUrl'));
console.log('Obra: salvar/reabrir, duas abas, desfazer, backup/importação atômica, revisão de etapa e fallback OK');
