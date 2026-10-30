/* Consulta do arquiteto; não modifica decisões ou dados de campo. */
;(function(root){
 const entryTab=search=>{const p=new URLSearchParams(search);return p.get('perfil')==='arquiteto'&&!p.has('aba')?'architect':null;};
 const api={entryTab};root.GuedalaArchitect=api;
 if(typeof module!=='undefined')module.exports=api;
})(globalThis);
