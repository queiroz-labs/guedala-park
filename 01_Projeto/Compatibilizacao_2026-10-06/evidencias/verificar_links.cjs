const fs=require('node:fs'),path=require('node:path');
const root='C:/Users/Elias/Documents/PROJETOS/Guedala park/guedala-park';
function walk(p){return fs.readdirSync(p,{withFileTypes:true}).flatMap(e=>e.isDirectory()?walk(path.join(p,e.name)):[path.join(p,e.name)]);}
const files=[path.join(root,'README.md'),...walk(path.join(root,'01_Projeto')).filter(f=>f.endsWith('.md'))];
let checked=0;const broken=[];
for(const f of files){const content=fs.readFileSync(f,'utf8');for(const m of content.matchAll(/\[[^\]\n]*\]\(([^)\n]+)\)/g)){let ref=m[1].trim().replace(/^<|>$/g,'');if(/^[a-z][a-z\d+.-]*:/i.test(ref)||ref.startsWith('#'))continue;ref=ref.split('#')[0];try{ref=decodeURIComponent(ref);}catch{}const dest=path.resolve(path.dirname(f),ref);checked++;if(!fs.existsSync(dest))broken.push({source:path.relative(root,f).replaceAll('\\','/'),line:content.slice(0,m.index).split('\n').length,reference:m[1],resolved:dest});}}
const result={date:'2026-10-06',scope:'README e Markdown de 01_Projeto; arquivos de arquivo/cache excluídos; links web e âncoras não verificados',files:files.length,checked,broken};fs.writeFileSync(path.join(__dirname,'Links_locais.json'),JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify(result,null,2));
