/* Nomes comuns, prefixos e plurais; todas as palavras úteis devem corresponder. */
;(function(root){
 const normalize=text=>String(text??'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/[^a-z0-9]+/g,' ').trim();
 const stop=new Set(['a','as','o','os','e','de','da','das','do','dos','em','no','na','nos','nas','para','com']);
 const terms=text=>normalize(text).split(/\s+/).filter(t=>t&&!stop.has(t));
 const singular=t=>t.length>3?t.replace(/oes$/,'ao').replace(/ais$/,'al').replace(/eis$/,'el').replace(/s$/,''):t;
 const matches=(term,word)=>word.startsWith(term)||singular(word).startsWith(singular(term));
 function find(query,index,limit=40){
  const q=normalize(query),wanted=terms(q);if(!wanted.length)return [];
  const compact=q.replace(/ /g,''),model=/[a-z]/.test(compact)&&/\d/.test(compact)&&compact.length>=4;
  const hits=[];
  for(const r of index){
   const title=normalize(r.title),names=normalize(r.aliases),words=(title+' '+names+' '+r.tokens).split(' ');
   const joined=model&&(title+' '+names).replace(/ /g,'').includes(compact);
   if(!joined&&!wanted.every(t=>words.some(w=>matches(t,w))))continue;
   const titleWords=terms(title),nameWords=terms(names);
   const primary=[...titleWords,...nameWords];
   let rank=title===q?0:wanted.every(t=>primary.some(w=>singular(w)===singular(t)))?1:
    title.startsWith(q)?2:wanted.every(t=>titleWords.some(w=>matches(t,w)))?3:
    wanted.every(t=>primary.some(w=>matches(t,w)))||joined?4:5;
   if(/^p\d{2}$/.test(q)&&r.kind==='module'&&normalize(r.id)===q)rank=-1;
   hits.push({r,rank});
  }
  const priority={choice:0,room:1,module:2,document:3,download:4,glossary:5,pending:6};
  return hits.sort((a,b)=>a.rank-b.rank||priority[a.r.kind]-priority[b.r.kind]||a.r.title.localeCompare(b.r.title,'pt-BR')).slice(0,limit).map(h=>h.r);
 }
 function navigate(r,api){
  if(!r||!['pending','choice','room','module','document','glossary','download'].includes(r.kind))return false;
  api.tab(r.tab);api[r.kind](r);return true;
 }
 const api={normalize,find,navigate};root.GuedalaSearch=api;if(typeof module!=='undefined')module.exports=api;
})(globalThis);
