const {chromium}=require('C:/Users/Elias Queiroz/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('fs');const path=require('path');
const {pathToFileURL}=require('url');
(async()=>{
 let browser=await chromium.launch({headless:true,channel:'msedge'});
 const errors=[];let report=[];const url=pathToFileURL(path.join(__dirname,'Guedala_Park_Interativo.html')).href;
 for(const [name,size,mobile]of [['desktop',{width:1440,height:1100},false],['s24plus',{width:412,height:915},true]]){
  let ctx=await browser.newContext({viewport:size,deviceScaleFactor:mobile?3:1,isMobile:mobile,hasTouch:mobile});let p=await ctx.newPage();p.on('pageerror',e=>errors.push(name+': '+e.message));await p.goto(url);await p.waitForSelector('#scene[data-rendered="true"]');await p.waitForTimeout(500);
  report.push({name,overflow:await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth),canvas:await p.locator('#scene').boundingBox()});
  await p.screenshot({path:path.join(__dirname,'Vista_'+name+'.png'),fullPage:false});
  await p.selectOption('#sofaState','open');await p.selectOption('#officeState','guest');await p.selectOption('#diningState','use');await p.selectOption('#consoleState','escritorio');
  await p.waitForTimeout(100);report.push({name,states:await p.evaluate(()=>({state:GuedalaStudy.state,ps5:GuedalaStudy.buildScene().filter(n=>n.id==='ps5').length,metric:document.querySelector('#metrics').innerText}))});
  await p.locator('[data-room="sala"]').click();await p.locator('[data-view="top"]').click();await p.waitForTimeout(150);await p.screenshot({path:path.join(__dirname,'Sala_'+name+'.png')});
  await p.locator('[data-room="escritorio"]').click();await p.locator('[data-view="side"]').click();await p.selectOption('#sideDirection','east');await p.waitForTimeout(150);await p.screenshot({path:path.join(__dirname,'Escritorio_lateral_'+name+'.png')});
  await p.evaluate(()=>GuedalaStudy.selectItem('officecab'));await p.waitForTimeout(100);if(mobile)await p.locator('#closeInfo').click();
  await p.locator('[data-tab="mood"]').click();await p.waitForTimeout(400);await p.screenshot({path:path.join(__dirname,'Moodboard_'+name+'.png'),fullPage:!mobile});
  await p.locator('[data-tab="decisions"]').click();await p.selectOption('#filterRoom','quarto');report.push({name,bedCards:await p.locator('.decision-card').count(),decisionsOverflow:await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth)});
  await ctx.close();
 }
 await browser.close();fs.writeFileSync(path.join(__dirname,'Verificacao_R01.json'),JSON.stringify({errors,report},null,2));console.log(JSON.stringify({errors,report},null,2));if(errors.length)process.exitCode=1;
})().catch(e=>{console.error(e);process.exit(1);});
