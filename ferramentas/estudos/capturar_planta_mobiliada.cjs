// Captura local do canvas existente; Playwright não participa do build/CI.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),assert=require('node:assert/strict'),{pathToFileURL}=require('node:url');
const root=path.resolve(__dirname,'../..'),args=process.argv.slice(2);
function option(name,fallback){const at=args.indexOf('--'+name);return at<0?fallback:args[at+1];}
if(args.includes('--help')||!option('output-dir')){console.log('node ferramentas/estudos/capturar_planta_mobiliada.cjs --output-dir PASTA_EXTERNA [--html ARQUIVO] [--browser EXECUTAVEL] [--revision R54]');process.exit(args.includes('--help')?0:1);}
const output=path.resolve(option('output-dir')),html=path.resolve(option('html',path.join(root,'ferramentas/site/Guedala_Park_Interativo.html'))),revision=option('revision','R54');
if(output===root||output.startsWith(root+path.sep))throw Error('Capture fora do repositório; confira as imagens antes de substituir as vigentes.');
if(!/^R\d+$/.test(revision))throw Error('Revisão inválida');
// Câmeras da R02: app.js de 1b4aeaa (R45). O ymax histórico é só enquadramento.
const views=[
 ['Planta_mobiliada_R03.png','all','top',-.62],
 ['Vistas/00_Apartamento.png','all','iso',-.62],
 ['Vistas/01_Sala_e_jantar.png','sala','iso',-.62],
 ['Vistas/02_Quarto.png','quarto','iso',-2.4],
 ['Vistas/03_Escritorio.png','escritorio','iso',-.62],
 ['Vistas/04_Cozinha.png','cozinha','iso',2.8],
 ['Vistas/05_Lavanderia.png','lavanderia','iso',2.5],
 ['Vistas/06_Banheiro.png','banho','iso',2.8]
];
for(const [file]of views)if(fs.existsSync(path.join(output,file)))throw Error('Saída já existe: '+file);
async function main(){
 const {chromium}=require('playwright');
 const browserFile=option('browser',process.env.GP_BROWSER||'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe');
 const browser=await chromium.launch({executablePath:browserFile,headless:true});
 try{
  const page=await browser.newPage({viewport:{width:1400,height:1000},deviceScaleFactor:1,offline:true,reducedMotion:'reduce'}),errors=[];
  page.on('pageerror',e=>errors.push(e.message));await page.goto(pathToFileURL(html).href+'?aba=apartamento');
  await page.waitForFunction(()=>!!window.GuedalaStudy&&document.querySelector('#scene').dataset.rendered==='true');
  await page.evaluate(()=>document.fonts.ready);
  const actual=await page.evaluate(()=>CAD_DATA.current_revision||CAD_DATA.revision);assert.equal(actual,revision,'Revisão da cena diverge do pedido');
  await page.addStyleTag({content:'.mast{visibility:hidden!important}#stage{position:fixed!important;left:0!important;top:0!important;z-index:9999!important;width:1005px!important;height:649px!important;min-height:0!important;max-height:none!important;margin:0!important;box-sizing:border-box!important}#stage .stage-heading{display:block!important}'});
  const results=[];
  for(const [file,room,view,angle]of views){
   await page.evaluate(async config=>{
    const api=GuedalaStudy;api.tab('model');api.setRoom(config.room);api.setView(config.view);
    Object.assign(api.state,{lighting:'after',angle:config.angle,tilt:.92,ymax:247,zoom:1,pan:[0,0],sofa:'closed',office:'work',table:'compact',dining:'stored',console:'sala',dry:'stored',upper:true,walls:false,measures:false,inside:false,selected:null,moduleFilter:null,focusPart:null});
    api.buildScene();await api.render(document.getElementById('scene'));
    document.getElementById('gestureHint').textContent='Imagem ilustrativa · sem cotas · medidas a conferir';
    document.querySelector('.stage-tag').textContent='Geometria '+config.revision+' · cores aproximadas';
   },{room,view,angle,revision});
   await page.waitForFunction(()=>!renderQueued&&!renderDirty&&!motion);
   const info=await page.evaluate(()=>{
    const canvas=document.getElementById('scene'),st=GuedalaStudy.state,list=GuedalaStudy.getNodes().filter(n=>n.id&&visible(n,st));
    const bounds=[Infinity,Infinity,-Infinity,-Infinity];
    for(const n of list)for(const f of mesh(n))for(const p of f.p){const q=lastProject.project(p);bounds[0]=Math.min(bounds[0],q[0]);bounds[1]=Math.min(bounds[1],q[1]);bounds[2]=Math.max(bounds[2],q[0]);bounds[3]=Math.max(bounds[3],q[1]);}
    return {canvas:[canvas.width,canvas.height],renderer:canvas.dataset.renderer,camera:{room:st.room,view:st.view,angle:st.angle,tilt:st.tilt,zoom:st.zoom,pan:st.pan,ymax:st.ymax},projectedBounds:bounds};
   });
   if(info.projectedBounds){const [x,y,xx,yy]=info.projectedBounds;assert(x>=0&&y>=0&&xx<=info.canvas[0]&&yy<=info.canvas[1],file+': móvel fora do enquadramento');}
   const target=path.join(output,file);fs.mkdirSync(path.dirname(target),{recursive:true});
   await page.locator('#stage').screenshot({path:target});results.push({file,...info,bytes:fs.statSync(target).size,sha256:crypto.createHash('sha256').update(fs.readFileSync(target)).digest('hex')});
  }
  assert.deepEqual(errors,[],'Erros JavaScript durante a captura');
  const metadata={revision,sourceHTMLSHA256:crypto.createHash('sha256').update(fs.readFileSync(html)).digest('hex'),browser:browser.version(),imageSize:[1005,649],cameraSource:'1b4aeaa:01_Projeto/Estudo_interativo/src/app.js',note:'ymax=247 é o envelope óptico histórico; não altera o pé-direito nem a geometria.',images:results};
  fs.writeFileSync(path.join(output,'captura.json'),JSON.stringify(metadata,null,2)+'\n');console.log(JSON.stringify({output,images:results.length,revision,size:metadata.imageSize}));
 }finally{await browser.close();}
}
main().catch(e=>{console.error(e);process.exitCode=1;});
