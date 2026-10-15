const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const base='C:/Users/Elias/Documents/PROJETOS/Guedala park/guedala-park/01_Projeto';
const output=path.join(__dirname,'evidencia');fs.mkdirSync(output,{recursive:true});
for(const rel of ['Compatibilizacao_2026-09-28/calcular_micro_c2.cjs','Compatibilizacao_2026-09-28/calcular_torre_gavetas.cjs','Compatibilizacao_2026-09-30/luz_varal.cjs']){
 const filename=path.join(base,rel),src=fs.readFileSync(filename,'utf8'),writes=[];
 const safeFs={...fs,writeFileSync:(dest,data)=>{if(!dest.endsWith('.json'))return;const out=path.join(output,path.basename(dest));fs.writeFileSync(out,data);writes.push(path.basename(out));}};
 const log=[];vm.runInNewContext(src,{require:n=>n==='node:fs'?safeFs:require(n),__dirname:path.dirname(filename),console:{log:(v)=>log.push(v)},process,Buffer,URL},{filename});
 const jsonName=path.basename(filename).replace('.cjs','_log.txt');fs.writeFileSync(path.join(output,jsonName),log.join('\n'));
 console.log(JSON.stringify({source:rel,outputs:writes,log:jsonName}));
}

