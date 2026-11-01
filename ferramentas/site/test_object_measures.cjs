/* node test_object_measures.cjs [--browser <HTML> <pasta-de-capturas>]
   Playwright existente via NODE_PATH; saídas sempre fora do repositório. */
const fs=require('node:fs'),vm=require('node:vm'),path=require('node:path'),assert=require('node:assert/strict'),{pathToFileURL}=require('node:url');
const src=path.join(__dirname,'src'),read=n=>fs.readFileSync(path.join(src,n),'utf8'),app=read('app.js'),measure=read('object-measures.js');
const ctx=vm.createContext({console,matchMedia:()=>({matches:true})});
vm.runInContext(['data.js','cad-data.js','visual-finishes.js','site-copy.js','cad-sync.js'].map(read).join('\n')+'\n'+app.slice(0,app.indexOf("const canvas=$('scene')"))+'\n'+app.slice(app.indexOf('const STONE_PARTS='),app.indexOf('function hideStoneTip'))+'\nbuildScene();\n'+measure.slice(0,measure.lastIndexOf('initializeObjectMeasures();')),ctx);
const run=s=>vm.runInContext(s,ctx),get=s=>JSON.parse(run('JSON.stringify('+s+')'));
run('state.walls=true;buildScene()');
const record=filter=>get(`objectRecord(nodes.find(n=>${filter}))`);
assert.deepEqual(record("n.kind==='door'&&n.room==='escritorio'").box,{x:474,y:0,z:220,w:2,d:75,h:205});
assert.deepEqual(record("!n.id&&n.kind==='glass'&&n.room==='quarto'").box,{x:60,y:95,z:90,w:120,d:10,h:110});
assert.equal(record("n.kind==='door'").reliability,'estimativa gráfica');
assert.deepEqual(record("n.id==='washer'").box,{x:320,y:0,z:628,w:60,d:62,h:85});
assert.equal(record("n.id==='washer'").reliability,'projeto/nominal');
assert.deepEqual(record("n.id==='washer'").fields.filter(f=>f.name.startsWith('Parede próxima')).map(f=>f.value),['10 cm','65 cm']);
assert.deepEqual(record("n.id==='bed'").box,{x:5,y:0,z:136,w:188,d:128,h:64});
const stone=record("n.source==='Peca308'");assert.equal(stone.reliability,'projeto/nominal');assert.equal(stone.box.h,2);
assert(record("n.kind==='door'").fields.filter(f=>/Base|Topo|Parede|Posição/.test(f.name)).every(f=>f.confidence==='estimativa gráfica'));
const pending=get("objectRecord({id:'coffeemaker',key:'pending/coffeemaker',room:'lavanderia',w:99,d:99,h:99,x:0,y:0,z:0})");
assert.equal(pending.box,null);assert.equal(pending.reliability,'pendente');
assert(!run("objectCopy(objectRecord({id:'coffeemaker',key:'pending/coffeemaker',room:'lavanderia',w:99,d:99,h:99,x:0,y:0,z:0})).includes('99')"));
run('state.walls=false;buildScene()');assert.equal(record("n.kind==='door'").box.h,205);assert.equal(record("!n.id&&n.kind==='glass'").box.h,110);
assert.equal(new Set(get('objectRecords().map(r=>r.key)')).size,get('objectRecords().length'));
assert.equal(get("objectRecords().filter(r=>r.id==='bed').length"),1);
assert.equal(record("n.id==='bonnie'").reliability,'estimativa gráfica');
assert.equal(record("n.id==='daiane'").box.w,90);assert.equal(record("n.id==='daiane'").box.d,140);
const listSource=read('object-list.js');vm.runInContext(listSource.slice(0,listSource.indexOf('function initializeObjectList(')),ctx);
const csv=run('objectCSV(objectRecords())');assert(csv.includes('confiabilidade da posição'));assert(csv.includes('pending/coffeemaker'));assert(!csv.includes('undefined'));
run("state.moduleFilter='P01';buildScene()");assert(get('nodes').every(n=>n.module==='P01'));assert(get("objectRecords().find(r=>r.id==='washer').box"));assert(!run("objectRecords().find(r=>r.id==='washer').node.pending"));run('state.moduleFilter=null;buildScene()');
assert(run("objectCopy(objectRecord(nodes.find(n=>n.id==='washer'))).includes('60 × 62 × 85 cm [projeto/nominal]')"));
const mode=read('object-measure-mode.js');vm.runInContext(mode.slice(0,mode.indexOf("$('stage')")),ctx);
run("objectSelected=objectKey(nodes.find(n=>n.id==='washer'));objectMeasuring=true;globalThis.cotas=[];dimension=(ctx,pr,a,b,text)=>cotas.push({a,b,text});drawObjectMeasure({save(){},restore(){},beginPath(){},moveTo(){},lineTo(){},stroke(){}},p=>p,state)");
assert.deepEqual(get('cotas.map(c=>c.text)'),['60 cm','62 cm','85 cm']);
run('objectMeasuring=false;cotas=[];drawObjectMeasure({save(){},restore(){},beginPath(){},moveTo(){},lineTo(){},stroke(){}},p=>p,state)');assert.equal(run('cotas.length'),0);
// Exact triangle picking at screen coordinates, including transparent window faces.
const pick=app.slice(app.indexOf('function pickFace('),app.indexOf('// Pedras ('));
vm.runInContext(pick,ctx);
for(const [filter,expected]of [["n.kind==='door'",'porta'],["!n.id&&n.kind==='glass'",'janela'],["n.id==='washer'",'eletrodoméstico'],["n.id==='bed'",'móvel'],["n.source==='Peca308'",'pedra']]){
 run(`globalThis.target=nodes.find(n=>${filter});globalThis.faces=mesh(target).map(f=>({...f,points:f.p.map(p=>[p[0]+p[2]*.4,p[1]+p[2]*.2,p[2]-p[0]*.2])}));`);
 const category=run(`(()=>{for(const f of faces){const p=f.points.slice(0,3),x=p.reduce((s,p)=>s+p[0],0)/3,y=p.reduce((s,p)=>s+p[1],0)/3,hit=pickFace(x,y,faces);if(hit)return objectRecord(hit.node).category;}return null;})()`);
 assert.equal(category,expected);
}
console.log('Medidas: portas, janelas, aparelho, cama e pedra; selos por campo; corte sem reduzir altura; pendentes sem números; seleção por coordenadas OK.');

if(process.argv.includes('--browser'))browserTest().catch(e=>{console.error(e);process.exitCode=1;});
async function browserTest(){
 const {chromium}=require('playwright'),idx=process.argv.indexOf('--browser'),html=path.resolve(process.argv[idx+1]),out=path.resolve(process.argv[idx+2]);fs.mkdirSync(out,{recursive:true});
 const root=path.dirname(html),http=require('node:http'),server=http.createServer((req,res)=>{
  const file=path.resolve(root,'.'+decodeURIComponent(new URL(req.url,'http://localhost').pathname));
  if(!file.startsWith(root+path.sep)||!fs.existsSync(file)||!fs.statSync(file).isFile()){res.writeHead(404);res.end();return;}
  res.setHeader('Content-Type',({'.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.json':'application/json','.css':'text/css'})[path.extname(file)]||'application/octet-stream');fs.createReadStream(file).pipe(res);
 });await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
 const browser=await chromium.launch({headless:true,executablePath:process.env.GUEDALA_BROWSER_EXECUTABLE||undefined});
 try{for(const viewport of [{width:1280,height:900},{width:375,height:812}]){
  const page=await browser.newPage({viewport,hasTouch:true,isMobile:viewport.width===375}),errors=[];page.setDefaultTimeout(12000);page.on('pageerror',e=>errors.push(e.message));
  await page.context().grantPermissions(['clipboard-read','clipboard-write']);
  await page.goto('http://127.0.0.1:'+server.address().port+'/'+encodeURIComponent(path.basename(html))+'?aba=model');await page.waitForFunction(()=>window.GuedalaStudy&&document.querySelector('#scene')?.dataset.rendered).catch(async error=>{console.error('Erros da página:',errors);console.error((await page.locator('body').innerText()).slice(-700));throw error;});
  if(viewport.width===1280){const layout=await page.evaluate(()=>{const side=document.querySelector('#model .sidebar').getBoundingClientRect(),work=document.querySelector('#model .workspace').getBoundingClientRect();return {sideRight:side.right,workLeft:work.left};});assert(layout.sideRight<=layout.workLeft+1,'Lista de cômodos não pode cobrir o desenho');}
  else{const scroll=await page.evaluate(async()=>{window.scrollTo(0,800);await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));const height=document.querySelector('.mast').getBoundingClientRect().height;window.scrollBy(0,-150);await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));return {y:window.scrollY,height,afterHeight:document.querySelector('.mast').getBoundingClientRect().height};});assert(scroll.y<800,'Rolagem para cima deve subir');assert(Math.abs(scroll.height-scroll.afterHeight)<1,'Cabeçalho não deve mudar de altura ao rolar');}
  // Test the existing pointer handler against the fully loaded, occluding scene.
  for(const [name,filter,room,expected,confidence]of [
   ['porta',"!n.id&&n.kind==='door'&&n.room==='escritorio'",'escritorio','2 × 75 × 205 cm','estimativa gráfica'],
   ['janela',"!n.id&&n.kind==='glass'&&n.room==='quarto'",'quarto','120 × 10 × 110 cm','estimativa gráfica'],
   ['eletrodomestico',"n.id==='washer'",'lavanderia','60 × 62 × 85 cm','projeto/nominal'],
   ['cama',"n.id==='bed'",'quarto','188 × 128 × 64 cm','projeto/nominal'],
   ['bancada',"n.source==='Peca308'",'cozinha','186,9 × 63 × 2 cm','projeto/nominal']]){
    const target=await page.evaluate(async({filter,room})=>{
     setRoom(room);state.walls=true;state.upper=false;state.sideCut=false;setView('iso');state.angle=-.7;state.tilt=.92;buildScene();await render(canvas);
     const n=nodes.find(new Function('n','return '+filter)),r=objectRecord(n);return {key:r.key,expected:r.fields[0].value};
    },{filter,room});
    await page.locator('#scene').scrollIntoViewIfNeeded();
    let point=null;
    for(const view of ['iso','top','side'])for(const angle of [-.7,1,2.8,4.3]){
     if(point)break;
     point=await page.evaluate(async({key,view,angle})=>{
      state.view=view;state.angle=angle;state.side='east';await render(canvas);const n=nodes.find(n=>objectKey(n)===key),faces=mesh(n),rect=canvas.getBoundingClientRect();
      for(const f of faces){const p=f.p.map(lastProject.project);for(let i=1;i<p.length-1;i++){
       const tri=[p[0],p[i],p[i+1]],x=tri.reduce((s,p)=>s+p[0],0)/3,y=tri.reduce((s,p)=>s+p[1],0)/3;
       if(x<4||x>rect.width-4||y<4||y>rect.height-4)continue;
       const hit=pickFace(x,y,hitFaces);if(hit&&objectKey(hit.node)===key)return {x:rect.left+x,y:rect.top+y};
      }}return null;
     },{key:target.key,view,angle});
    }
    assert(point,'Objeto visível para clique: '+name);console.log('Clique '+viewport.width+' '+name+' '+JSON.stringify(point));if(viewport.width===375)await page.touchscreen.tap(point.x,point.y);else await page.mouse.click(point.x,point.y);
    const summary=page.locator(['porta','janela'].includes(name)?'#objectMeasureCard .object-measure-summary':'#selectedInfo .object-measure-summary');await page.waitForFunction(key=>document.querySelector('.object-measure-summary[data-object-key="'+CSS.escape(key)+'"]'),target.key);
    const text=await summary.textContent();assert(text.includes(expected||target.expected),name+': '+text);assert(text.includes(confidence));
    if(!['porta','janela'].includes(name)){
     const details=page.locator('#selectedInfo > .project-measures'),toggle=details.locator(':scope > summary');
     assert.equal(await details.evaluate(e=>e.open),false,'Detalhes do projeto começam recolhidos');assert.equal(await summary.isVisible(),false);
     assert(await page.locator('#selectedInfo .item-preview,#selectedInfo .work-measures').first().isVisible(),'Ficha ilustrada aparece primeiro');
     await toggle.focus();await toggle.press('Enter');assert(await summary.isVisible(),'Medidas aparecem no drill down');
     await toggle.press('Enter');assert.equal(await details.evaluate(e=>e.open),false);
    }
    if(await page.locator('#objectMeasureList').count())assert.equal(await page.locator('#objectMeasureRows tr[aria-selected=true]').getAttribute('data-object-row'),target.key,'Clique leva à linha');
    if(name==='eletrodomestico'){await page.locator('#selectedInfo > .project-measures > summary').click();await summary.locator('[data-copy-object=text]').click();await page.waitForFunction(()=>[...document.querySelectorAll('.object-copy-status')].some(e=>e.textContent==='Medidas copiadas.'));assert((await page.evaluate(()=>navigator.clipboard.readText())).includes('60 × 62 × 85 cm'));}
    if(name==='porta'||name==='eletrodomestico'){
     await summary.scrollIntoViewIfNeeded();await page.screenshot({path:path.join(out,name+'-'+viewport.width+'.png'),fullPage:false});
    }
    if(name==='porta'){
     const card=page.locator('#objectMeasureCard'),close=card.locator('button').first(),box=await close.boundingBox();assert(box.width>=44&&box.height>=44);
     const a=await card.boundingBox(),b=await page.locator('#scene').boundingBox();assert(a.y>=b.y+b.height,'Cartão fora da área do objeto');
    }
  }
  await page.evaluate(async()=>{setRoom('all');buildScene();const n=nodes.find(n=>n.module==='P01');await inspectObject(n);if(!document.querySelector('#selectedInfo .object-measure-summary'))throw Error('Ficha do módulo deve preservar medidas após mudar de cômodo');});
  const moduleDetails=page.locator('#selectedInfo > .project-measures');assert.equal(await moduleDetails.evaluate(e=>e.open),false);
  assert(await page.locator('#selectedInfo .work-measures').first().isVisible(),'Ficha do módulo visível');
  await page.locator('#isolateModule').click();assert.equal(await page.evaluate(()=>state.moduleFilter),'P01','Controles da ficha mantêm funcionamento');await page.locator('#isolateModule').click();
  await page.evaluate(async()=>showModule('P01'));assert(await page.locator('#selectedInfo .work-measures').first().isVisible(),'Consulta direta mostra ficha');
  await page.evaluate(()=>{setView('iso');canvas.scrollIntoView({block:'center',behavior:'instant'});});await page.evaluate(()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve))));const box=await page.locator('#scene').boundingBox(),before=await page.evaluate(()=>state.angle);
  const cdp=await page.context().newCDPSession(page),cx=box.x+box.width/2,cy=box.y+box.height/2;
  assert.equal(await page.evaluate(({cx,cy})=>document.elementFromPoint(cx,cy)?.id,{cx,cy}),'scene','Ficha não bloqueia os gestos');
  if(viewport.width===375){await cdp.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x:cx,y:cy,id:1}]});await cdp.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x:cx+35,y:cy+15,id:1}]});await cdp.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});}
  else{await page.mouse.move(cx,cy);await page.mouse.down();await page.mouse.move(cx+35,cy+15,{steps:4});await page.mouse.up();}
  assert.notEqual(await page.evaluate(()=>state.angle),before,'Arraste gira o modelo');
  if(await page.locator('#objectMeasureToggle').count()){
   await page.locator('#objectMeasureToggle').click();assert.equal(await page.locator('#objectMeasureToggle').getAttribute('aria-pressed'),'true');
   const count=await page.evaluate(async()=>{const before=dimension,calls=[];dimension=(...args)=>{calls.push(args[4]);before(...args);};try{await render(canvas);return calls.length;}finally{dimension=before;}});assert(count>=3,'Cotas do objeto no canvas');
  }
  const zoom=await page.evaluate(()=>state.zoom);
  // Real touch events through CDP generate native pointer events and pinch handling.
  await page.evaluate(()=>{canvas.scrollIntoView({block:'center',behavior:'instant'});});const pinch=await page.locator('#scene').boundingBox(),px=pinch.x+pinch.width/2,py=pinch.y+pinch.height/2;
  await cdp.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x:px-20,y:py,id:1},{x:px+20,y:py,id:2}]});
  await cdp.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x:px-45,y:py,id:1},{x:px+45,y:py,id:2}]});
  await cdp.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});assert((await page.evaluate(()=>state.zoom))>zoom,'Pinça aproxima');
  if(await page.locator('#objectMeasureList').count()){
   await page.locator('#objectMeasureList').evaluate(e=>e.open=true);await page.locator('#objectRoom').selectOption('all');await page.locator('#objectSearch').fill('cafeteira');assert((await page.locator('#objectMeasureRows').innerText()).includes('pendente'));
   await page.locator('#objectMeasureRows button').click();assert((await page.locator('#objectMeasureCard').innerText()).includes('Sem medida definida'));
   await page.locator('#objectRoom').selectOption('all');await page.locator('#objectCategory').selectOption('eletrodoméstico');await page.locator('#objectSearch').fill('Lava e seca');assert.equal(await page.locator('#objectMeasureRows tr').count(),1);
   const [csvDownload]=await Promise.all([page.waitForEvent('download'),page.locator('#objectCSV').click()]);const data=fs.readFileSync(await csvDownload.path(),'utf8');assert(data.includes('"60";"62";"85"'));assert.equal(data.split('\r\n').length,2);
   await page.locator('#objectMeasureRows button').click();assert.equal(await page.evaluate(()=>GuedalaStudy.getSelectedObject()),'washer/washer/1');
   assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'Sem overflow na página');
  }
  assert.deepEqual(errors,[]);await page.close();console.log('Navegador '+viewport.width+': 5 cliques, cartões/fichas, capturas, arraste, pinça e busca OK.');
 }}finally{await browser.close();await new Promise(resolve=>server.close(resolve));}
}
