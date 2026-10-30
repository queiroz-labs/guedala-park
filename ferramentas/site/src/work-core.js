/* Marcação pessoal de execução; não interpreta nem resolve dependências técnicas. */
;(function(root){
  'use strict';
  const KEY='guedala:obra:v1';
  function validate(p){
    if(!p||p.versao!==1||p.projeto!=='guedala-park'||p.tipo!=='obra'||!Array.isArray(p.etapas)||!root.GuedalaField.dateValid(p.exportado_em))throw new Error('Arquivo de obra incompatível.');
    const seen=new Set();return p.etapas.map(r=>{
      if(!r||typeof r.id!=='string'||!/^etapa-[a-f0-9]{16}$/.test(r.id)||seen.has(r.id)||typeof r.feito!=='boolean'||!root.GuedalaField.dateValid(r.data_hora))throw new Error('Etapa inválida ou repetida.');
      seen.add(r.id);return {id:r.id,feito:r.feito,data_hora:r.data_hora};
    });
  }
  function createStore(ids,{storage=()=>root.localStorage,clock=()=>new Date().toISOString()}={}){
    const allowed=new Set(ids),records=Object.create(null);let persistent=true,unknown=0;
    function merge(rows){let applied=0,older=0,ignored=0;
      for(const r of rows){
        if(!allowed.has(r.id)){ignored++;continue;}
        if(records[r.id]&&Date.parse(records[r.id].data_hora)>Date.parse(r.data_hora)){older++;continue;}
        records[r.id]=r;applied++;
      }
      return {applied,older,ignored};
    }
    const payload=()=>({versao:1,projeto:'guedala-park',tipo:'obra',exportado_em:clock(),etapas:Object.values(records).map(r=>({...r}))});
    try{const s=storage();if(!s)persistent=false;else{const raw=s.getItem(KEY);if(raw)unknown=merge(validate(JSON.parse(raw))).ignored;}}
    catch(e){persistent=false;}
    function persist(){
      if(!persistent)return;
      try{const s=storage(),raw=s.getItem(KEY);if(raw)merge(validate(JSON.parse(raw)));s.setItem(KEY,JSON.stringify(payload()));}
      catch(e){persistent=false;}
    }
    return {
      get:id=>!!records[id]?.feito,
      set(id,feito){
        if(!allowed.has(id)||typeof feito!=='boolean')throw new Error('Etapa desconhecida.');
        records[id]={id,feito,data_hora:clock()};persist();
      },
      importFile(text){const rows=validate(JSON.parse(text)),result=merge(rows);unknown=result.ignored;persist();return result;},
      exportData:payload,
      state:()=>({persistent,unknown,done:Object.values(records).filter(r=>r.feito).length,total:allowed.size})
    };
  }
  root.GuedalaWork={KEY,validate,createStore};
  if(typeof module!=='undefined'&&module.exports)module.exports=root.GuedalaWork;
})(globalThis);
