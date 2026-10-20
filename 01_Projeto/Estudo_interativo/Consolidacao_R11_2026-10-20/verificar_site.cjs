const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict'),{pathToFileURL}=require('node:url');
const {chromium}=require(path.join(process.env.USERPROFILE,'.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright'));
const dir=__dirname,study=path.dirname(dir),errors=[],requests=[];
(async()=>{
 const b=await chromium.launch({headless:true,channel:'msedge'});
 const context=await b.newContext({viewport:{width:1440,height:1100},reducedMotion:'reduce',acceptDownloads:true});
 const p=await context.newPage();p.on('pageerror',e=>errors.push(e.message));p.on('request',r=>{if(/^https?:/.test(r.url()))requests.push(r.url());});
 const start=Date.now();await p.goto(pathToFileURL(path.join(study,'Guedala_Park_Interativo.html')).href);await p.waitForSelector('#scene[data-rendered]',{timeout:60000});
 const initial=await p.evaluate(()=>({revision:GuedalaStudy.project.revision,renderer:document.querySelector('#scene').dataset.renderer,native:CAD_DATA.parts.length,triangles:CAD_DATA.parts.reduce((s,n)=>s+n.t.length,0),mirrored:PROJECT.mirrored,bankNote:ITEMS.find(i=>i.id==='bench').notes}));
 assert.match(initial.revision,/R11/);assert(initial.native>150);assert.equal(initial.mirrored,true);assert.match(initial.bankNote,/não gostou/);
 const rooms=await p.evaluate(()=>PROJECT.rooms.map(r=>r.id));
 let combinations=0;
 for(const room of rooms){
  await p.evaluate(r=>GuedalaStudy.setRoom(r),room);
  for(const view of ['top','iso','side']){
   await p.evaluate(v=>GuedalaStudy.setView(v),view);await p.waitForTimeout(80);
   assert.equal(await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false,room+'/'+view+' overflow');combinations++;
  }
 }
 await p.evaluate(()=>{GuedalaStudy.setRoom('cozinha');GuedalaStudy.setView('iso');GuedalaStudy.selectItem('oven');});
 await p.waitForTimeout(120);assert.match(await p.locator('#selectedInfo').innerText(),/Fischer/);assert.doesNotMatch(await p.locator('#selectedInfo').innerText(),/Venax Totale/);
 await p.screenshot({path:path.join(dir,'Cozinha_R11.png')});
 await p.evaluate(()=>{GuedalaStudy.setRoom('quarto');GuedalaStudy.selectItem('queen');});assert.match(await p.locator('#selectedInfo').innerText(),/viúvo/);assert.match(await p.locator('#selectedInfo').innerText(),/futura/);
 await p.evaluate(()=>GuedalaStudy.selectItem('wardrobe'));await p.locator('.ward-detail summary').click();assert.equal(await p.locator('.ward-detail img').evaluate(i=>i.complete&&i.naturalWidth>0),true);
 await p.screenshot({path:path.join(dir,'Quarto_R11.png')});
 await p.evaluate(()=>{GuedalaStudy.setRoom('sala');GuedalaStudy.setView('iso');GuedalaStudy.selectItem('bench');});
 const closed=await p.evaluate(()=>GuedalaStudy.buildScene().find(n=>n.source==='BancoFolhaR31').z);
 const choose=async(id,value)=>p.locator('#'+id).locator('..').locator('[data-choice="'+value+'"]').click();
 await choose('benchState','open');await p.waitForTimeout(100);
 const open=await p.evaluate(()=>GuedalaStudy.buildScene().find(n=>n.source==='BancoFolhaR31').z);assert(Math.abs(open-closed-84.3)<1e-4);
 assert.match(await p.locator('#selectedInfo').innerText(),/sem alterar agora/);
 await choose('benchState','closed');
 await choose('sofaState','open');await choose('tableState','extended');await choose('consoleState','escritorio');
 const nodes=await p.evaluate(()=>({finite:GuedalaStudy.buildScene().flatMap(mesh).every(f=>f.p.every(p=>p.every(Number.isFinite))),ps5:GuedalaStudy.buildScene().filter(n=>n.id==='ps5').length}));assert(nodes.finite);assert.equal(nodes.ps5,1);
 await p.setViewportSize({width:412,height:915});await p.evaluate(()=>{GuedalaStudy.setRoom('cozinha');GuedalaStudy.setView('iso');});await p.keyboard.press('Escape');await p.waitForTimeout(100);
 assert.equal(await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);await p.screenshot({path:path.join(dir,'Mobile_R11.png')});
 for(const t of ['mood','decisions']){await p.locator('[data-tab="'+t+'"]').click();await p.waitForTimeout(100);assert.equal(await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);}
 const downloadEvent=p.waitForEvent('download');await p.locator('#downloadHTML2').click();const download=await downloadEvent;
 const copy=path.join(dir,'Copia_QA.html');await download.saveAs(copy);await p.goto(pathToFileURL(copy).href);await p.waitForSelector('#scene[data-rendered]',{timeout:60000});assert.equal(await p.evaluate(()=>GuedalaStudy.state.bench),'closed');fs.unlinkSync(copy);
 assert.equal(errors.length,0,errors.join(';'));assert.equal(requests.length,0,'Dependências de rede inesperadas.');
 const report={status:'PASSOU',date:'2026-10-20',initial,room_view_combinations:combinations,viewports:['1440x1100','412x915'],bed_current_future_correct:true,bank_preference_recorded_no_conventional_reversal:true,native_bank_motion_mm:843,copy_reopened:true,errors,external_requests:requests,elapsed_ms:Date.now()-start};
 fs.writeFileSync(path.join(dir,'Verificacao_site_R11.json'),JSON.stringify(report,null,2));console.log(JSON.stringify(report));await b.close();
})().catch(e=>{console.error(e);process.exit(1);});
