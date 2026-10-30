/* Consulta do arquiteto; não modifica decisões ou dados de campo. */
;(function(root){
 const entryTab=search=>{const p=new URLSearchParams(search);return p.get('perfil')==='arquiteto'&&!p.has('aba')?'architect':null;};
 const owners=['Elias','Arquiteto','RT','Oficina/marceneiro','Construtora/condomínio','a definir'];
 const ownerItems=(rows,owner='todos')=>rows.filter(r=>owner==='todos'||r.owners.includes(owner));
 const ownerCounts=rows=>Object.fromEntries(owners.map(o=>[o,ownerItems(rows,o).length]));
 const api={entryTab,owners,ownerItems,ownerCounts};root.GuedalaArchitect=api;
 if(typeof module!=='undefined')module.exports=api;
})(globalThis);
