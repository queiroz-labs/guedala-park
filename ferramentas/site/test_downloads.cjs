const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const read=n=>fs.readFileSync(path.join(__dirname,n),'utf8'),root=path.resolve(__dirname,'../..');
const source=JSON.parse(read('downloads-source.json')),release=JSON.parse(read('current_release.json'));
const published=process.env.GUEDALA_DOWNLOADS_SITE?path.resolve(process.env.GUEDALA_DOWNLOADS_SITE):null;
const ctx=vm.createContext({});vm.runInContext(fs.readFileSync(published?path.join(published,'downloads-data.js'):path.join(__dirname,'src/downloads-data.js'),'utf8'),ctx);
const rows=JSON.parse(vm.runInContext('JSON.stringify(GUEDALA_DOWNLOADS)',ctx));
const expected=source.items.map(r=>({...r,path:r.releasePath?release.packageDirectory+'/'+release.packageFile:r.path}));
assert.equal(new Set(rows.map(r=>r.id)).size,rows.length);
assert.deepEqual(rows.map(r=>r.id).sort(),expected.filter(r=>published||!r.releasePath||rows.some(x=>x.id===r.id)).map(r=>r.id).sort());
const state=fs.readFileSync(path.join(root,'ESTADO_ATUAL.md'),'utf8');
for(const r of rows){
 const s=expected.find(x=>x.id===r.id);assert(s,'Download sem fonte: '+r.id);
 for(const key of ['title','description','path','status'])assert.equal(r[key],s[key],r.id+' '+key);
 const sourceFile=path.join(root,r.path),target=r.path+(r.path.endsWith('.md')?'.html':'');
 assert.equal(r.publishedPath,target);assert(!r.path.split('/').includes('..'));
 assert(Number.isInteger(r.bytes)&&r.bytes>0);assert(Number.isInteger(r.sourceBytes)&&r.sourceBytes>0);
 assert.equal(r.format,r.path.endsWith('.md')?'HTML':path.extname(r.path).slice(1).toUpperCase());
 assert(r.revision&&r.status);
 if(!['perguntas','destinatarios','reforma'].includes(r.id))assert(r.status.includes('nominal / a confirmar'),r.id+' limite nominal');
 if(s.revision.release)assert.equal(r.revision,(s.revision.prefix||'')+release[s.revision.release]);
 if(s.revision.state){const line=state.split(/\r?\n/).find(l=>l.startsWith('| '+s.revision.state+' |'));assert.equal(r.revision,line.match(/\bR\d+\b/)[0]);}
 if(published){assert.equal(fs.statSync(sourceFile).size,r.sourceBytes,r.id+' bytes da fonte');assert.equal(fs.statSync(path.join(published,'docs',target)).size,r.bytes,r.id+' bytes publicados');}
}
assert(rows.some(r=>r.id==='pranchas'&&r.revision==='R02'));assert(!rows.some(r=>/Pranchas_R00/.test(r.path)));
assert(rows.find(r=>r.id==='reforma').status.includes('sem validade formal'));
assert(rows.find(r=>r.id==='cotacao').status.includes('não enviado'));
const ui=read('src/downloads-ui.js');assert(ui.includes('GUEDALA_DOWNLOADS'));assert(ui.includes("['architect','documents']"));assert(!ui.includes('Pranchas A3'),'Itens vêm dos dados');
vm.runInContext(read('src/search-data.js')+read('src/search-core.js'),ctx);
const index=JSON.parse(vm.runInContext('JSON.stringify(GUEDALA_SEARCH_INDEX)',ctx)),api=vm.runInContext('GuedalaSearch',ctx);
for(const r of expected){assert(index.some(x=>x.kind==='download'&&x.id===r.id));assert(api.find(r.title,index,100).some(x=>x.key==='download:'+r.id));}
assert(read('src/search-ui.js').includes("GuedalaDownloads?.show(r.id,'documents')"));
const workshop=read('src/workshop.js'),resolver=workshop.slice(workshop.indexOf('const workDocBase='),workshop.indexOf('function workParts'));
for(const local of [false,true]){
 const links=vm.createContext({window:{GUEDALA_WEB:!local},location:{protocol:local?'file:':'https:',pathname:local?'/copia.html':'/guedala-park/'}});vm.runInContext(resolver,links);
 for(const r of rows){const href=vm.runInContext('workDocUrl('+JSON.stringify({path:r.path})+')',links);assert.equal(href,(local?'https://queiroz-labs.github.io/guedala-park/':'')+'docs/'+r.publishedPath);}
}
if(published){
 const manifest=JSON.parse(fs.readFileSync(path.join(published,'docs/downloads-manifest.json'),'utf8'));assert.deepEqual(manifest.items,rows);assert.equal(rows.length,expected.length);
 for(const r of rows)assert(manifest.files.includes(r.publishedPath));
 for(const name of manifest.files)assert(fs.statSync(path.join(published,'docs',name)).isFile(),'Arquivo não publicado: '+name);
 for(const p of source.support)assert(manifest.files.includes(p+(p.endsWith('.md')?'.html':'')),p);
 const questions=fs.readFileSync(path.join(published,'docs/01_Programa_e_decisoes/Perguntas_em_aberto/README.md.html'),'utf8');
 assert.equal((questions.match(/href="Mensagens\/[^\"]+\.md\.html"/g)||[]).length,8,'Oito destinatários com link ativo');
 const html=fs.readFileSync(path.join(published,'index.html'),'utf8');assert(!html.includes('data-downloads-loader'),'Web recebe catálogo medido sem loader local');
}
console.log('Downloads: '+rows.length+' itens das fontes, revisões, busca e '+(published?'todos os bytes/destinos publicados':'metadados; publicação conferida após o build'));
