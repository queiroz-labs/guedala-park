/* Dados do levantamento: sem rede, sem tolerância presumida, sem dependência do 3D. */
;(function(root){
  'use strict';
  const KEY='guedala:medidas:v1',STATUS=new Set(['pendente','ok','fora_do_esperado']);
  function number(value){
    if(value==null||String(value).trim()==='')return null;
    if(typeof value!=='number'&&!/^-?\d+(?:[.,]\d+)?$/.test(String(value).trim()))throw new Error('Use um número em milímetros.');
    const n=Number(String(value).trim().replace(',','.'));
    if(!Number.isFinite(n))throw new Error('Medida inválida.');return n;
  }
  function difference(value,nominal){return value==null||nominal==null?null:Math.round((value-nominal)*1000)/1000;}
  function dateValid(s){
    if(typeof s!=='string'||!/^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d{1,3})?(?:Z|[+-]\d\d:\d\d)$/.test(s)||!Number.isFinite(Date.parse(s)))return false;
    const [y,m,d]=s.slice(0,10).split('-').map(Number),dt=new Date(Date.UTC(y,m-1,d));
    return dt.getUTCFullYear()===y&&dt.getUTCMonth()===m-1&&dt.getUTCDate()===d;
  }
  function validate(payload,allowed){
    if(!payload||payload.versao!==1||payload.projeto!=='guedala-park'||!Array.isArray(payload.medidas))throw new Error('Arquivo de medidas incompatível.');
    if(!dateValid(payload.exportado_em))throw new Error('Data da exportação inválida.');
    const seen=new Set();return payload.medidas.map(r=>{
      if(!r||typeof r.codigo!=='string'||!allowed.has(r.codigo))throw new Error('Código desconhecido: '+String(r?.codigo));
      if(seen.has(r.codigo))throw new Error('Código repetido: '+r.codigo);seen.add(r.codigo);
      if(r.valor_mm!==null&&(typeof r.valor_mm!=='number'||!Number.isFinite(r.valor_mm)))throw new Error('Valor inválido: '+r.codigo);
      if(!STATUS.has(r.status)||typeof r.observacao!=='string'||!dateValid(r.data_hora))throw new Error('Registro inválido: '+r.codigo);
      return {codigo:r.codigo,valor_mm:r.valor_mm,status:r.status,observacao:r.observacao,data_hora:r.data_hora};
    });
  }
  function csvCell(value,freeText=false){
    let text=value==null?'':String(value);
    if(freeText&&/^[\s]*[=+@\-\t\r]/.test(text))text="'"+text;
    return '"'+text.replace(/"/g,'""')+'"';
  }
  function toCsv(payload){
    const fields=['codigo','valor_mm','status','observacao','data_hora'];
    return '\ufeff'+fields.join(';')+'\r\n'+payload.medidas.map(r=>fields.map(k=>csvCell(r[k],k==='observacao')).join(';')).join('\r\n')+'\r\n';
  }
  function createStore(codes,{storage=()=>root.localStorage,clock=()=>new Date().toISOString()}={}){
    const allowed=new Set(codes),records=Object.create(null);let persistent=true,error='';
    function payload(){return {versao:1,projeto:'guedala-park',exportado_em:clock(),medidas:Object.keys(records).sort().map(k=>({...records[k]}))};}
    try{
      const raw=storage()?.getItem(KEY);
      if(raw)for(const r of validate(JSON.parse(raw),allowed))records[r.codigo]=r;
      // Acesso sem objeto também é falta de armazenamento persistente.
      if(!storage())persistent=false;
    }catch(e){persistent=false;error='Não foi possível abrir o armazenamento deste navegador.';}
    function persist(){
      if(!persistent)return;
      try{
        const previous=storage().getItem(KEY);
        if(previous)for(const r of validate(JSON.parse(previous),allowed)){
          if(!records[r.codigo]||Date.parse(r.data_hora)>Date.parse(records[r.codigo].data_hora))records[r.codigo]=r;
        }
        storage().setItem(KEY,JSON.stringify(payload()));
      }
      catch(e){persistent=false;error='O navegador não conseguiu salvar no aparelho.';}
    }
    return {
      get:code=>records[code]?{...records[code]}:{codigo:code,valor_mm:null,status:'pendente',observacao:'',data_hora:''},
      update(code,change){
        if(!allowed.has(code))throw new Error('Código desconhecido: '+code);
        const old=this.get(code),next={...old,...change,codigo:code,data_hora:clock()};
        next.valor_mm=number(next.valor_mm);
        if('valor_mm' in change&&next.valor_mm!==old.valor_mm&&!('status' in change))next.status='pendente';
        validate({versao:1,projeto:'guedala-park',exportado_em:clock(),medidas:[next]},allowed);
        records[code]=next;persist();return {...next};
      },
      importFile(text){
        const incoming=validate(JSON.parse(text),allowed);let imported=0,older=0;
        for(const r of incoming){
          if(records[r.codigo]&&Date.parse(records[r.codigo].data_hora)>Date.parse(r.data_hora)){older++;continue;}
          records[r.codigo]=r;imported++;
        }
        persist();return {imported,older};
      },
      exportData:payload,
      storageState:()=>({persistent,error}),
      stats:()=>({recorded:Object.values(records).filter(r=>r.valor_mm!==null||r.status!=='pendente'||r.observacao).length,
                  reviewed:Object.values(records).filter(r=>r.status!=='pendente').length,total:allowed.size})
    };
  }
  const api={KEY,number,difference,dateValid,validate,toCsv,createStore};root.GuedalaField=api;
  if(typeof module!=='undefined'&&module.exports)module.exports=api;
})(globalThis);
