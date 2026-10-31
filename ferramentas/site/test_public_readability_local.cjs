/* Opcional: node test_public_readability_local.cjs <site-gerado> <relatorio.json>.
   Usa Playwright já instalado (também via NODE_PATH); não instala dependências. */
const fs=require('node:fs'),path=require('node:path'),{pathToFileURL}=require('node:url');
const config=JSON.parse(fs.readFileSync(path.join(__dirname,'publicacao_documentos.json'),'utf8')).teste_local;
let chromium;try{({chromium}=require('playwright'));}catch{console.error('Teste local opcional: Playwright ausente. Aponte NODE_PATH para uma instalação existente.');process.exit(2);}
const root=path.resolve(process.argv[2]||''),report=process.argv[3];
if(!report||!fs.existsSync(path.join(root,'docs')))throw Error('Informe o site gerado e o relatório fora do repositório.');
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:process.env.GUEDALA_BROWSER_EXECUTABLE||undefined}),rows=[];
 try{
  for(const width of config.larguras){
   const context=await browser.newContext({viewport:{width,height:config.altura},isMobile:true,deviceScaleFactor:1,offline:true});
   const page=await context.newPage();
   for(const name of config.paginas){
    await page.goto(pathToFileURL(path.join(root,'docs',name)).href,{waitUntil:'load'});
    const result=await page.evaluate(cfg=>{
     const visible=el=>{
      if(el.closest(cfg.excluir_texto))return false;
      for(let parent=el;parent;parent=parent.parentElement)if(parent.tagName==='DETAILS'&&!parent.open&&!parent.querySelector('summary')?.contains(el))return false;
      const s=getComputedStyle(el),r=el.getBoundingClientRect();return s.display!=='none'&&s.visibility!=='hidden'&&r.width>0&&r.height>0;
     };
     const elements=[...document.querySelectorAll('main *,body.public-document *')].filter(visible);
     const texts=elements.filter(el=>[...el.childNodes].some(n=>n.nodeType===3&&n.textContent.trim()));
     const small=texts.filter(el=>parseFloat(getComputedStyle(el).fontSize)<cfg.fonte_minima).map(el=>({tag:el.tagName,text:el.textContent.slice(0,70),px:parseFloat(getComputedStyle(el).fontSize)}));
     const targets=[...document.querySelectorAll('a[href],button,input,select,summary')].filter(visible);
     const tiny=targets.filter(el=>{const target=el.matches('input[type=checkbox]')?el.closest('label')||el:el,r=target.getBoundingClientRect();return r.height<cfg.alvo_minimo-0.5||r.width<cfg.alvo_minimo-0.5;}).map(el=>({tag:el.tagName,text:el.textContent.slice(0,70),width:el.getBoundingClientRect().width,height:el.getBoundingClientRect().height}));
     const first=texts.filter(el=>{const r=el.getBoundingClientRect();return r.top<innerHeight&&r.bottom>0;}).map(el=>[...el.childNodes].filter(n=>n.nodeType===3).map(n=>n.textContent).join(' ')).join(' ');
     return {overflow:document.documentElement.scrollWidth-innerWidth,fontes_pequenas:small,alvos_pequenos:tiny,palavras_primeira_tela:first.trim().split(/\s+/).length,altura_sem_recolher:document.documentElement.scrollHeight,links_visiveis:targets.filter(el=>el.tagName==='A').length};
    },config);
    rows.push({width,page:name,...result});
   }
   await context.close();
  }
 }finally{await browser.close();}
 fs.writeFileSync(report,JSON.stringify(rows,null,2)+'\n');
 const bad=rows.filter(r=>r.overflow>1||r.fontes_pequenas.length||r.alvos_pequenos.length);
 console.log(`${rows.length} verificações locais; ${bad.length} com problemas; relatório: ${report}`);
 process.exitCode=bad.length?1:0;
})().catch(error=>{console.error(error);process.exitCode=1;});
