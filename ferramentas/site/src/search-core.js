/* Busca literal por prefixos de palavras; acentos/capitalização não interferem. */
;(function(root){
 const normalize=text=>String(text??'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/[^a-z0-9]+/g,' ').trim();
 function find(query,index,limit=40){
  const q=normalize(query);if(!q)return [];const terms=q.split(/\s+/);
  return index.filter(r=>terms.every(t=>r.tokens.split(' ').some(w=>w.startsWith(t)))).sort((a,b)=>{
   const rank=r=>normalize(r.title)===q?0:normalize(r.title).startsWith(q)?1:2;
   return rank(a)-rank(b)||a.title.localeCompare(b.title,'pt-BR');
  }).slice(0,limit);
 }
 function navigate(r,api){
  if(!r||!['pending','choice','room','module','document','glossary'].includes(r.kind))return false;
  api.tab(r.tab);api[r.kind](r);return true;
 }
 const api={normalize,find,navigate};root.GuedalaSearch=api;if(typeof module!=='undefined')module.exports=api;
})(globalThis);
