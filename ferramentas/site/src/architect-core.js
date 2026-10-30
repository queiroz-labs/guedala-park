/* Consulta do arquiteto; não modifica decisões ou dados de campo. */
;(function(root){
 const pageIds=['architect','model','mood','decisions','documents','floorplan','chaves','obra'];
 function hashTab(hash,aliases={}){
  let name;try{name=decodeURIComponent(hash.replace(/^#/,'' )).toLowerCase();}catch{return null;}
  const id=aliases[name]||({'planta-pe-direito':'floorplan',scene:'model','downloads-architect':'architect','downloads-documents':'documents'})[name]||name;
  return pageIds.includes(id)?id:null;
 }
 const entryTab=(search,hash='',aliases={})=>{const p=new URLSearchParams(search);return p.has('aba')||hashTab(hash,aliases)?null:'architect';};
 const owners=['Elias','Arquiteto','RT','Oficina/marceneiro','Construtora/condomínio','a definir'];
 const ownerItems=(rows,owner='todos')=>rows.filter(r=>owner==='todos'||r.owners.includes(owner));
 const ownerCounts=rows=>Object.fromEntries(owners.map(o=>[o,ownerItems(rows,o).length]));
 const toolTab=hash=>({'#chaves':'chaves','#obra':'obra'})[hash]||null;
 const api={entryTab,hashTab,toolTab,owners,ownerItems,ownerCounts};root.GuedalaArchitect=api;
 if(typeof module!=='undefined')module.exports=api;
})(globalThis);
