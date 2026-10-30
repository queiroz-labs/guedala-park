const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const read=n=>fs.readFileSync(path.join(__dirname,n),'utf8'),root=path.resolve(__dirname,'../..');
const source=JSON.parse(read('downloads-source.json')),release=JSON.parse(read('current_release.json'));
const published=process.env.GUEDALA_DOWNLOADS_SITE?path.resolve(process.env.GUEDALA_DOWNLOADS_SITE):null;
const ctx=vm.createContext({});vm.runInContext(fs.readFileSync(published?path.join(published,'downloads-data.js'):path.join(__dirname,'src/downloads-data.js'),'utf8'),ctx);
const rows=JSON.parse(vm.runInContext('JSON.stringify(GUEDALA_DOWNLOADS)',ctx));
const expected=source.items.map(r=>({...r,path:r.releasePath?release.packageDirectory+'/'+release.packageFile:r.path}));
const imageRoot='03_Ambientes/Planta_mobiliada/',capture=JSON.parse(fs.readFileSync(path.join(root,imageRoot,'Captura.json'),'utf8')),crypto=require('node:crypto');
assert.equal(capture.revision,release.cadRevision,'Imagens devem acompanhar a cena vigente');assert.deepEqual(capture.imageSize,[1005,649]);
const images=['Planta_mobiliada_R03.png',...['00_Apartamento','01_Sala_e_jantar','02_Quarto','03_Escritorio','04_Cozinha','05_Lavanderia','06_Banheiro'].map(n=>'Vistas/'+n+'.png')];
assert.deepEqual(capture.images.map(r=>r.file).sort(),images.slice().sort());assert(!fs.existsSync(path.join(root,imageRoot,'Planta_mobiliada_R02.png')));
for(const image of capture.images){const bytes=fs.readFileSync(path.join(root,imageRoot,image.file));assert.equal(bytes.subarray(0,8).toString('hex'),'89504e470d0a1a0a');assert.deepEqual([bytes.readUInt32BE(16),bytes.readUInt32BE(20)],capture.imageSize);assert.equal(bytes.length,image.bytes);assert.equal(crypto.createHash('sha256').update(bytes).digest('hex'),image.sha256,image.file+' integridade');}
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
 const imagePage=fs.readFileSync(path.join(published,'docs',imageRoot,'README.md.html'),'utf8');
 for(const image of capture.images){const file=path.join(published,'docs',imageRoot,image.file);assert.equal(crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex'),image.sha256,image.file+' publicado');assert(imagePage.includes('href="'+image.file+'"'),image.file+' link ativo');}
 assert(imagePage.includes('href="Captura.json"'));assert(fs.existsSync(path.join(published,'docs',imageRoot,'Captura.json')));
}
console.log('Downloads: '+rows.length+' itens das fontes, revisões, busca e '+(published?'todos os bytes/destinos publicados':'metadados; publicação conferida após o build'));
