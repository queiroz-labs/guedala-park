// Publish a light shell and versioned assets, keeping the standalone download.
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {build,transform} from 'esbuild';
const study=path.dirname(fileURLToPath(import.meta.url)),src=path.join(study,'src');
const site=process.argv[2]?path.resolve(process.argv[2]):path.resolve(study,'../../.site'),assets=path.join(site,'assets');
if(!process.argv[2]&&fs.existsSync(site)&&fs.readdirSync(site).length)throw Error('Existing .site preserved; pass an isolated output directory.');
fs.mkdirSync(assets,{recursive:true});
// Mesma interface de campo em arquivo leve, com planta/fotos e sem rede.
fs.copyFileSync(path.join(study,'Dia_das_chaves.html'),path.join(site,'Dia_das_chaves.html'));
const read=name=>fs.readFileSync(path.join(src,name),'utf8').replace(/\r\n/g,'\n');
const digest=data=>crypto.createHash('sha256').update(data).digest('hex').slice(0,12);
const writeAsset=(stem,extension,data)=>{const name=`${stem}-${digest(data)}.${extension}`;fs.writeFileSync(path.join(assets,name),data);return 'assets/'+name;};
const context=vm.createContext({});
vm.runInContext(read('cad-data.js')+read('workshop-docs.js'),context);
const cad=JSON.parse(vm.runInContext('JSON.stringify(CAD_DATA)',context));
const docs=JSON.parse(vm.runInContext('JSON.stringify(WORKSHOP_DOCS)',context));
const guidance=JSON.parse(vm.runInContext('JSON.stringify(MODULE_GUIDANCE)',context));
const geometry=cad.parts.map(({source,v,t})=>({source,v,t}));
for(const part of cad.parts){delete part.v;delete part.t;}
const modules={};
for(const [code,guide]of Object.entries(guidance))if(guide.fabrication){
 modules[code]=writeAsset(code,'json',JSON.stringify(guide.fabrication));delete guide.fabrication;
}
const geometryUrl=writeAsset('geometry','json',JSON.stringify(geometry));
const worker=await transform(read('geometry-worker.js'),{minify:true,target:'es2020'});
const workerUrl=writeAsset('geometry-worker','js',worker.code);
const offline=fs.readFileSync(path.join(study,'Guedala_Park_Interativo.html'),'utf8').replace(/\r\n/g,'\n');
// Download asset lives under /assets; its relative documentation links use site root.
const offlineDownload=offline.replace('<head>','<head><base href="../">');
const offlineUrl=writeAsset('Guedala_Park_Interativo','html',offlineDownload);
const settings={geometryUrl,workerUrl,offlineUrl,modules,geometryReady:false};
// Only images required by detail dialogs stay external to the entry bundle.
const imageAssets=new Map();
function externalImages(code){return code.replace(/data:image\/(png|svg\+xml|webp|jpeg);base64,([A-Za-z0-9+/=]+)/g,(whole,type,b64)=>{
 if(!imageAssets.has(whole))imageAssets.set(whole,writeAsset('detail',type==='svg+xml'?'svg':type==='jpeg'?'jpg':type,Buffer.from(b64,'base64')));
 return imageAssets.get(whole);
});}
let scripts=[...offline.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m=>m[1]);
for(const name of ['cad-data.js','workshop-docs.js'])if(!scripts.some(code=>code.includes(read(name))))throw Error('Cannot externalize '+name);
scripts=scripts.map(code=>code.replace(read('cad-data.js'),`const CAD_DATA=${JSON.stringify(cad)};`).replace(read('workshop-docs.js'),`const WORKSHOP_DOCS=${JSON.stringify(docs)};const MODULE_GUIDANCE=${JSON.stringify(guidance)};`));
const runtime='globalThis.GUEDALA_WEB='+JSON.stringify(settings)+';\n'+scripts.map(externalImages).join('\n')+'\n'+read('web-loader.js');
const entryName=`app-${digest(runtime)}.js`;
await build({stdin:{contents:runtime,sourcefile:'guedala-runtime.js',resolveDir:src},bundle:false,minify:true,sourcemap:true,sourcesContent:true,target:'es2020',outfile:path.join(assets,entryName),legalComments:'none'});
// Render the room navigation during the build, using the same template as the UI.
const elements={rooms:{innerHTML:''}};
const navContext=vm.createContext({document:{querySelectorAll:()=>[]}});
navContext.$=id=>elements[id];navContext.esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
vm.runInContext(read('data.js')+read('experience.js')+'\nbuildRoomNavigation();',navContext);
const base=offline.replace(/<script>[\s\S]*?<\/script>/g,'').replace('<div id="rooms" class="roomlist"></div>',`<div id="rooms" class="roomlist">${elements.rooms.innerHTML}</div>`)
 .replace('<div class="stage" id="stage">','<div class="stage" id="stage"><div id="sceneLoading" class="scene-loading" role="status">Carregando modelo 3D… As fichas já podem ser consultadas.</div>');
const css=base.match(/<style>([\s\S]*?)<\/style>/)[1];
const minCss=(await transform(css,{loader:'css',minify:true,target:'es2020'})).code;
const page=base.replace('<h2 class="material-title">Biblioteca de materiais</h2>','<p><a href="moodboard.png" target="_blank" rel="noopener">Abrir painel visual de materiais</a></p><h2 class="material-title">Biblioteca de materiais</h2>').replace(/<style>[\s\S]*?<\/style>/,`<style>${minCss}</style>`).replace('</head>',`<script defer src="assets/${entryName}"></script></head>`);
fs.writeFileSync(path.join(site,'index.html'),page);
// Relative URLs are kept valid in the existing /moodboard/ entry point.
fs.writeFileSync(path.join(site,'moodboard/index.html'),page.replace('<head>','<head><base href="../">').replace('<body>','<body data-start-tab="mood">'));
// Approved day/night gallery: separate assets keep the 3D entry bundle light.
const references=path.resolve(study,'../../09_Referencias'),gallery=path.join(site,'galeria');
fs.mkdirSync(gallery,{recursive:true});
const mood=JSON.parse(fs.readFileSync(path.join(references,'Moodboard.json'),'utf8'));
const galleryFiles=['Moodboard.json','Moodboard_paineis.pdf','Moodboard_ambientes_A3.pdf',
 'Moodboard_Dia.png','Moodboard_Noite.png','Moodboard_Dia_leve.png','Moodboard_Noite_leve.png'];
for(const scene of mood.cenas)galleryFiles.push(scene.arquivo,scene.arquivo.replace('.png','_web.webp'));
for(const file of galleryFiles)fs.copyFileSync(path.join(references,file),path.join(gallery,file));
fs.writeFileSync(path.join(gallery,'index.html'),fs.readFileSync(path.join(references,'Moodboard.html'),'utf8')
 .replace('../ferramentas/site/Guedala_Park_Interativo.html','../index.html'));
fs.writeFileSync(path.join(assets,'manifest.json'),JSON.stringify({entry:'assets/'+entryName,...settings,htmlBytes:Buffer.byteLength(page),geometryParts:geometry.length,triangles:geometry.reduce((n,p)=>n+p.t.length,0)},null,2));
console.log(`Web shell: ${Buffer.byteLength(page)} bytes; geometry: ${geometry.length} parts, loaded by worker.`);
