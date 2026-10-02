const fs=require('fs');
const path=require('path');
const {spawn,spawnSync}=require('child_process');

function arg(name,def=null){const i=process.argv.indexOf('--'+name);return i>=0?process.argv[i+1]:def}
const exe=arg('exe','C:\\Users\\A\\AppData\\Local\\ms-playwright\\chromium-1234\\chrome-win64\\chrome.exe');
const profile=arg('profile','C:\\AI\\Playwright-Native-AI-Browser\\profile\\shared-mcp');
const endpoint=arg('cdp','http://127.0.0.1:9223').replace(/\/$/,'');
const root=arg('state-root','C:\\AI\\Playwright-Native-AI-Browser\\state');
const intervalMs=Number(arg('interval-ms','5000'));
const lockPath=path.join(root,'chatgpt-browser-watchdog.json');
const statePath=path.join(root,'chatgpt-browser-health.json');
const logPath=path.join(root,'chatgpt-browser-watchdog.jsonl');
const disabledPath=path.join(root,'chatgpt-watchdog.disable');
fs.mkdirSync(root,{recursive:true});

function log(event,data={}){fs.appendFileSync(logPath,JSON.stringify({at:new Date().toISOString(),event,...data})+'\n')}
function writeState(v){fs.writeFileSync(statePath,JSON.stringify({at:new Date().toISOString(),...v},null,2))}
function pidAlive(pid){try{process.kill(Number(pid),0);return true}catch{return false}}
function readJson(p){try{return JSON.parse(fs.readFileSync(p,'utf8'))}catch{return null}}
const old=readJson(lockPath);
if(old&&pidAlive(old.pid)&&old.pid!==process.pid){console.log('WATCHDOG_ALREADY_ACTIVE pid='+old.pid);process.exit(0)}
fs.writeFileSync(lockPath,JSON.stringify({pid:process.pid,startedAt:new Date().toISOString()},null,2));

function profileProcessCount(){
 if(process.platform!=='win32')return 0;
 const escaped=profile.replace(/'/g,"''");
 const ps="$p='"+escaped+"'; @(Get-CimInstance Win32_Process | Where-Object {$_.CommandLine -and $_.CommandLine.Contains($p)}).Count";
 const r=spawnSync('powershell.exe',['-NoProfile','-Command',ps],{encoding:'utf8',windowsHide:true,timeout:5000});
 const n=Number(String(r.stdout||'').trim());return Number.isFinite(n)?n:0;
}
async function json(url){const c=new AbortController();const t=setTimeout(()=>c.abort(),2500);try{const r=await fetch(url,{signal:c.signal});if(!r.ok)throw new Error('HTTP_'+r.status);return await r.json()}finally{clearTimeout(t)}}
class Cdp{
 constructor(u){this.u=u;this.ws=null;this.id=0;this.p=new Map()}
 async open(){this.ws=new WebSocket(this.u);this.ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.id&&this.p.has(m.id)){const h=this.p.get(m.id);this.p.delete(m.id);m.error?h.j(new Error(JSON.stringify(m.error))):h.r(m.result||{})}};await new Promise((r,j)=>{this.ws.onopen=r;this.ws.onerror=j});return this}
 call(method,params={}){return new Promise((r,j)=>{const id=++this.id,t=setTimeout(()=>{this.p.delete(id);j(new Error('CDP_TIMEOUT_'+method))},5000);this.p.set(id,{r:v=>{clearTimeout(t);r(v)},j:e=>{clearTimeout(t);j(e)}});this.ws.send(JSON.stringify({id,method,params}))})}
 close(){try{this.ws.close()}catch{}}
}
async function ensureChatTarget(){
 const list=await json(endpoint+'/json/list');
 let page=list.find(x=>x.type==='page'&&String(x.url||'').startsWith('https://chatgpt.com/'));
 if(page)return {created:false,page};
 const ver=await json(endpoint+'/json/version');const c=await new Cdp(ver.webSocketDebuggerUrl).open();
 try{const r=await c.call('Target.createTarget',{url:'https://chatgpt.com/'});log('chatgpt_target_created',{targetId:r.targetId});return {created:true,targetId:r.targetId}}
 finally{c.close()}
}
async function pageHealth(){
 const list=await json(endpoint+'/json/list');const page=list.find(x=>x.type==='page'&&String(x.url||'').startsWith('https://chatgpt.com/'));if(!page)return {pagePresent:false};
 const c=await new Cdp(page.webSocketDebuggerUrl).open();
 try{
  const r=await c.call('Runtime.evaluate',{expression:"JSON.stringify((()=>{const b=document.body?.innerText||'';const vis=e=>!!(e&&e.getClientRects().length);const composer=[document.querySelector('#prompt-textarea'),...document.querySelectorAll('[contenteditable=\\\"true\\\"]'),...document.querySelectorAll('textarea')].find(vis);const stop=[...document.querySelectorAll('button')].some(x=>vis(x)&&(x.getAttribute('data-testid')==='stop-button'||/Stop generating|停止生成/i.test(x.getAttribute('aria-label')||'')));return {url:location.href,title:document.title,composer:!!composer,stop,human:/verify you are human|captcha|确认您是真人|just a moment|checking your browser|请稍候/i.test(b+' '+document.title),disconnected:/连接已断开|正在重新连接|disconnected|reconnecting/i.test(b)}})())",returnByValue:true});
  return {pagePresent:true,...JSON.parse(r.result.value)}
 }finally{c.close()}
}
function launchBrowser(){
 const child=spawn(exe,['--remote-debugging-address=127.0.0.1','--remote-debugging-port=9223','--user-data-dir='+profile,'--no-first-run','--no-default-browser-check','https://chatgpt.com/'],{detached:true,stdio:'ignore',windowsHide:false});
 child.unref();log('browser_launch_once',{pid:child.pid,profile});return child.pid;
}

let missingProcessStreak=0,stopping=false;
async function tick(){
 if(fs.existsSync(disabledPath)){writeState({status:'DISABLED'});return}
 try{
  await json(endpoint+'/json/version');missingProcessStreak=0;
  const t=await ensureChatTarget();const h=await pageHealth();
  const status=h.human?'HUMAN_VERIFICATION_REQUIRED':h.disconnected?'TRANSPORT_DEGRADED':h.pagePresent?'HEALTHY':'PAGE_MISSING';
  writeState({status,cdp:'PASS',createdPage:Boolean(t.created),...h});
 }catch(e){
  const owners=profileProcessCount();
  if(owners>0){missingProcessStreak=0;writeState({status:'CDP_DEGRADED_EXISTING_BROWSER_NO_RELAUNCH',cdp:'FAIL',profileProcesses:owners,error:String(e.message||e)});log('cdp_degraded_existing_browser',{owners,error:String(e.message||e)})}
  else{
   missingProcessStreak++;
   writeState({status:'BROWSER_PROCESS_MISSING_CONFIRMING',cdp:'FAIL',profileProcesses:0,missingProcessStreak,error:String(e.message||e)});
   if(missingProcessStreak>=2){launchBrowser();missingProcessStreak=0}
  }
 }
}
async function loop(){log('watchdog_started',{pid:process.pid,profile,endpoint});while(!stopping){await tick();await new Promise(r=>setTimeout(r,intervalMs))}}
function stop(sig){if(stopping)return;stopping=true;log('watchdog_stopped',{sig});try{const x=readJson(lockPath);if(x?.pid===process.pid)fs.unlinkSync(lockPath)}catch{};setTimeout(()=>process.exit(0),50)}
process.on('SIGINT',()=>stop('SIGINT'));process.on('SIGTERM',()=>stop('SIGTERM'));
loop().catch(e=>{log('watchdog_fatal',{error:String(e.stack||e)});writeState({status:'WATCHDOG_FATAL',error:String(e.message||e)});stop('FATAL')});
