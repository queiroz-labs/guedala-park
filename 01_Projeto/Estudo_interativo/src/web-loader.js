// This file is only included in the web build. Offline HTML retains embedded data.
const moduleLoads=new Map();
window.loadModuleGuidance=async code=>{
 if(MODULE_GUIDANCE[code]?.fabrication)return;
 const path=GUEDALA_WEB.modules[code];if(!path)return;
 if(!moduleLoads.has(code))moduleLoads.set(code,fetch(new URL(path,document.baseURI)).then(async response=>{
  if(!response.ok)throw Error('HTTP '+response.status);
  MODULE_GUIDANCE[code].fabrication=await response.json();
 }).catch(error=>{moduleLoads.delete(code);throw error;}));
 return moduleLoads.get(code);
};
async function startGeometry(){
 const status=document.getElementById('sceneLoading');
 status.hidden=false;status.textContent='Carregando modelo 3D… As fichas já podem ser consultadas.';
 const parts=new Map(CAD_DATA.parts.map(part=>[part.source,part]));
 try{
  await new Promise((resolve,reject)=>{
   const worker=new Worker(new URL(GUEDALA_WEB.workerUrl,document.baseURI));
   const timer=setTimeout(()=>{worker.terminate();reject(Error('Tempo de carregamento excedido'));},60000);
   const end=(error)=>{clearTimeout(timer);worker.terminate();error?reject(error):resolve();};
   worker.onmessage=({data})=>{
    if(data.error){end(Error(data.error));return;}
    if(data.part)Object.assign(parts.get(data.part.source),data.part);
    if(data.done)end();
   };
   worker.onerror=()=>end(Error('Não foi possível preparar o modelo'));
   worker.postMessage({url:new URL(GUEDALA_WEB.geometryUrl,document.baseURI).href});
  });
  GUEDALA_WEB.geometryReady=true;lastSceneState='';window.dispatchEvent(new Event('guedala-geometry-ready'));
  status.textContent='Preparando a vista do apartamento…';
  requestRender();if(document.getElementById('mood').classList.contains('active'))renderMood();
 }catch(error){
  status.innerHTML='Não foi possível carregar o modelo. As fichas continuam disponíveis.<button type="button">Tentar novamente</button>';
  status.querySelector('button').onclick=startGeometry;
 }
}
if(document.body.dataset.startTab==='mood')tab('mood');
startGeometry();
