const fs=require('fs');
const path=require('path');
const {spawnSync}=require('child_process');
const {chromium}=require('playwright');
const {decide}=require('./session-continuity-supervisor');
const {pageLeaseDecision,conversationRotation}=require('./chatgpt-page-lease');
const {recoverExistingChat}=require('./chatgpt-existing-cdp');

function arg(name,def=null){const i=process.argv.indexOf('--'+name);return i>=0?process.argv[i+1]:def}
const profile=arg('profile');
const initialTaskPath=arg('task');
const root=arg('lease-root',path.resolve('ltmvh-chatgpt-lease'));
const statePath=path.join(root,'lease-state.json');
const inboxDir=path.join(root,'inbox');
const doneDir=path.join(root,'done');
const failDir=path.join(root,'failed');
const ledgerPath=path.join(root,'delivery-ledger.json');
const checkpointPath=arg('checkpoint',path.join(root,'checkpoint.json'));
const backupResultPath=arg('backup-result',path.join(root,'backup-result.json'));
const pollMs=Number(arg('poll-ms','1200'));
const silenceMs=Number(arg('silence-ms','45000'));
const maxTurns=Number(arg('max-turns','24'));
const maxText=Number(arg('max-text','80000'));
const cdpEndpoint=arg('cdp-endpoint','http://127.0.0.1:9223');
if(!profile) throw new Error('Usage: --profile <dir> [--task <task.json>] [--lease-root <dir>]');

for(const d of [root,inboxDir,doneDir,failDir]) fs.mkdirSync(d,{recursive:true});
const now=()=>Date.now();
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const rxDisconnect=/连接已断开|正在重新连接|disconnected|reconnecting/i;
const rxHuman=/verify you are human|captcha|确认您是真人|验证.*真人|just a moment|checking your browser|请稍候/i;
const rxService=/service unavailable|temporarily unavailable|bad gateway|internal server error/i;

function isPidAlive(pid){if(!pid)return false;try{process.kill(pid,0);return true}catch{return false}}
function readJson(p,fallback){try{return JSON.parse(fs.readFileSync(p,'utf8'))}catch{return fallback}}
function writeJson(p,v){fs.writeFileSync(p,JSON.stringify(v,null,2))}
function safeName(s){return String(s||Date.now()).replace(/[^a-zA-Z0-9._-]/g,'_').slice(0,120)}

function enqueueTask(taskPath){
 const task=JSON.parse(fs.readFileSync(taskPath,'utf8'));
 const marker=task.marker||('LTMVH-'+Date.now());
 task.marker=marker;
 const target=path.join(inboxDir,Date.now()+'-'+safeName(marker)+'.json');
 writeJson(target,task);
 return {status:'QUEUED_TO_EXISTING_PAGE_LEASE',marker,target};
}

const prior=readJson(statePath,null);
if(prior&&prior.status==='LEASE_ACTIVE'&&isPidAlive(prior.pid)&&prior.pid!==process.pid){
 if(initialTaskPath){console.log(JSON.stringify(enqueueTask(initialTaskPath),null,2));process.exit(0)}
 console.log(JSON.stringify({status:'LEASE_ALREADY_ACTIVE',pid:prior.pid,pageUrl:prior.pageUrl||null},null,2));
 process.exit(0);
}

let runtimeContext=null;
let leasedPage=null;
let attachedBrowser=null;
let externalBrowserAttached=false;
let lastAttachError=null;
let stopping=false;
let currentTask=null;
let lastSig='',lastProgress=now(),probeDone=false,priorDisconnect=0;

function leaseState(extra={}){
 const base={schemaVersion:1,status:'LEASE_ACTIVE',version:'0.3.0',pid:process.pid,profile,
  pageLease:true,browserMustStayOpen:true,updatedAt:new Date().toISOString(),pageUrl:leasedPage&&!leasedPage.isClosed()?leasedPage.url():null};
 writeJson(statePath,{...base,...extra});
}

async function observe(page){
 const o=await page.evaluate(()=>{
  const txt=(document.body?.innerText||'');
  const users=[...document.querySelectorAll('[data-message-author-role="user"]')];
  const assistants=[...document.querySelectorAll('[data-message-author-role="assistant"]')];
  const visible=el=>!!(el&&el.getClientRects().length);
  const stop=[...document.querySelectorAll('button')].some(b=>visible(b)&&(
   b.getAttribute('data-testid')==='stop-button'||/Stop generating|停止生成/i.test(b.getAttribute('aria-label')||'')));
  const composer=[
   document.querySelector('#prompt-textarea'),
   ...document.querySelectorAll('[contenteditable="true"]'),
   ...document.querySelectorAll('textarea')
  ].find(visible);
  const lastUser=users.at(-1)?.innerText||'';
  const lastAssistant=assistants.at(-1)?.innerText||'';
  const copyReady=!!assistants.at(-1)?.closest('article,[data-testid^="conversation-turn-"]')
    ?.querySelector('button[data-testid*="copy"],button[aria-label*="复制"],button[aria-label*="Copy"]');
  return {txtLen:txt.length,userTurns:users.length,assistantTurns:assistants.length,stop,composer:!!composer,
   lastUser,lastAssistant,copyReady,url:location.href,title:document.title,bodyText:txt.slice(0,12000)};
 });
 return {...o,
  disconnected:rxDisconnect.test(o.bodyText),
  humanVerification:rxHuman.test(o.bodyText)||rxHuman.test(o.title||''),
  serviceUnavailable:rxService.test(o.bodyText),
  safeCheckpoint:!o.stop&&o.composer&&o.assistantTurns>0&&o.copyReady};
}

function buildCheckpoint(task,obs,reason){
 const cp={schemaVersion:1,version:'0.3.0',createdAt:new Date().toISOString(),reason,
  marker:task.marker,sourceConversationUrl:obs.url,taskContract:task.taskContract||task.goal||'',
  acceptedConclusion:(obs.lastAssistant||'').slice(0,12000),lastUser:(obs.lastUser||'').slice(0,6000),
  unresolvedItems:task.unresolvedItems||[],nextInstruction:task.nextInstruction||
  '根据以上接续上下文继续当前未完成任务，从下一步唯一动作开始，不重新讨论已冻结结论。',
  safetyBoundaries:task.safetyBoundaries||[]};
 writeJson(checkpointPath,cp);return cp;
}

function handoffText(task,cp){
 const text=[
  '[LTMVH_RECOVERY '+task.marker+']',
  '这是故障恢复后的真正 New chat，不是 Branch。只使用以下最小接续上下文继续。',
  '【任务合同】\n'+cp.taskContract,
  '【上一阶段已确认结论】\n'+cp.acceptedConclusion,
  '【未完成】\n'+JSON.stringify(cp.unresolvedItems),
  '【安全边界】\n'+JSON.stringify(cp.safetyBoundaries),
  '【下一步唯一动作】\n'+cp.nextInstruction
 ].join('\n\n');
 if(text.length>24000) throw new Error('HANDOFF_TOO_LARGE:'+text.length);
 return text;
}

function backupText(task,cp,trigger){
 return [
  '[LTMVH_BACKUP_RECOVERY '+task.marker+']',
  'GPT/ChatGPT 主路当前不可用或恢复失败。你是独立备脑。读取同一个任务合同与 Checkpoint，继续到相同 DONE_WHEN；不要降低完成标准。',
  '【切换原因】\n'+trigger,'【任务合同】\n'+cp.taskContract,
  '【上一阶段已确认结论】\n'+cp.acceptedConclusion,'【未完成】\n'+JSON.stringify(cp.unresolvedItems),
  '【安全边界】\n'+JSON.stringify(cp.safetyBoundaries),'【下一步唯一动作】\n'+cp.nextInstruction,
  '不得修改 Windows 系统；不得修改 FlClash / Windows 网络代理；不可逆高风险、支付、账号安全动作必须停在权限门。'
 ].join('\n\n');
}

function runReasonixBackup(task,cp,trigger){
 if(task.backupEnabled===false)return {status:'BACKUP_DISABLED',trigger};
 const started=Date.now(),opts={input:backupText(task,cp,trigger),encoding:'utf8',timeout:180000,maxBuffer:8*1024*1024,windowsHide:true};
 const r=process.platform==='win32'?spawnSync(process.env.ComSpec||'cmd.exe',['/d','/s','/c','reasonix run --output-format json'],opts):
  spawnSync('reasonix',['run','--output-format','json'],opts);
 const stdout=(r.stdout||'').trim(),stderr=(r.stderr||'').trim();let parsed=null;
 for(const line of stdout.split(/\r?\n/).filter(Boolean).reverse()){try{parsed=JSON.parse(line);break}catch{}}
 const ok=!r.error&&r.status===0&&parsed&&parsed.subtype==='success'&&parsed.is_error===false;
 const out={schemaVersion:1,status:ok?'BACKUP_COMPLETED':'BACKUP_FAILED',trigger,startedAtEpochMs:started,
  durationMs:Date.now()-started,exitCode:r.status,error:r.error?String(r.error.message||r.error):null,
  reasonix:parsed,stderr:stderr.slice(0,4000),marker:task.marker,pageLeaseRetained:true};
 writeJson(backupResultPath,out);if(!ok)throw new Error('BACKUP_FAIL:'+JSON.stringify(out));return out;
}

function ledger(){return readJson(ledgerPath,{schemaVersion:1,markers:{}})}
function ledgerSet(marker,data){const x=ledger();x.markers[marker]={...(x.markers[marker]||{}),...data,updatedAt:new Date().toISOString()};writeJson(ledgerPath,x)}
function delivered(marker){return Boolean(ledger().markers[marker]?.sentConfirmed)}

function externalProfileProcessCount(){
 if(process.platform!=='win32') return 0;
 const escaped=profile.replace(/'/g,"''");
 const ps="$p='"+escaped+"'; @(Get-CimInstance Win32_Process | Where-Object {$_.CommandLine -and $_.CommandLine.Contains($p)}).Count";
 const r=spawnSync('powershell.exe',['-NoProfile','-Command',ps],{encoding:'utf8',windowsHide:true,timeout:5000});
 const n=Number(String(r.stdout||'').trim());
 return Number.isFinite(n)?n:0;
}

async function attachExistingBrowser(){
 try{
  const b=await Promise.race([
   chromium.connectOverCDP(cdpEndpoint),
   new Promise((_,reject)=>setTimeout(()=>reject(new Error('CDP_ATTACH_TIMEOUT')),8000))
  ]);
  const contexts=b.contexts();
  if(!contexts.length){lastAttachError='CDP_NO_CONTEXT';return null}
  attachedBrowser=b;externalBrowserAttached=true;runtimeContext=contexts[0];
  const pages=runtimeContext.pages();
  leasedPage=pages.find(p=>/chatgpt\.com/.test(p.url()))||null;
  if(!leasedPage) leasedPage=await runtimeContext.newPage();
  lastAttachError=null;
  leaseState({acquiredAt:new Date().toISOString(),attachedVia:'CDP',cdpEndpoint,externalBrowserAttached:true});
  return leasedPage;
 }catch(e){lastAttachError=String(e.message||e);return null}
}

async function ensureLeasedPage(){
 const decision=pageLeaseDecision({taskFinalValid:false,explicitStop:false,
  existingUsablePage:Boolean(leasedPage&&!leasedPage.isClosed()),pageLeaseActive:Boolean(runtimeContext),pageRecoverable:true});
 if(decision.action==='REUSE_EXISTING_PAGE'||decision.action==='KEEP_PAGE_OPEN') return leasedPage;
 if(!runtimeContext){
  const attached=await attachExistingBrowser();
  if(attached) return attached;
  const owners=externalProfileProcessCount();
  if(owners>0) throw new Error('EXISTING_BROWSER_PRESENT_NO_SECOND_LAUNCH owners='+owners+' attach='+String(lastAttachError||'UNKNOWN'));
  runtimeContext=await chromium.launchPersistentContext(profile,{headless:false,viewport:{width:1365,height:850}});
 }
 const pages=runtimeContext.pages();
 leasedPage=pages.find(p=>/chatgpt\.com/.test(p.url()))||pages[0]||await runtimeContext.newPage();
 if(!/chatgpt\.com/.test(leasedPage.url())) await leasedPage.goto('https://chatgpt.com/',{waitUntil:'domcontentloaded',timeout:60000});
 leaseState({acquiredAt:new Date().toISOString(),attachedVia:externalBrowserAttached?'CDP':'LAUNCH',externalBrowserAttached});return leasedPage;
}

async function rotateTrueNewChatSamePage(task,cp){
 const rot=conversationRotation({safeCheckpoint:true,pageLeaseActive:true});
 if(rot.action!=='NEW_CONVERSATION_SAME_PAGE') throw new Error('PAGE_LEASE_ROTATION_BLOCKED:'+rot.action);
 if(delivered(task.marker)) return {status:'ALREADY_DELIVERED_NO_RESEND',submissionCount:0,markerCount:1,pageLeaseRetained:true};
 const p=await ensureLeasedPage();
 await p.goto('https://chatgpt.com/',{waitUntil:'domcontentloaded',timeout:60000});
 await sleep(1200);
 const first=await observe(p);
 console.log(JSON.stringify({event:'NEW_CHAT_PROBE',url:p.url(),title:first.title,composer:first.composer,
  userTurns:first.userTurns,assistantTurns:first.assistantTurns,pageLeaseRetained:true}));
 if(first.humanVerification) throw new Error('HUMAN_VERIFICATION_REQUIRED');
 const u=new URL(p.url());if(/^\/c\//.test(u.pathname)||/branch/i.test(p.url()))throw new Error('NOT_TRUE_NEW_CHAT:'+p.url());
 const composer=p.locator('#prompt-textarea:visible, [contenteditable="true"]:visible, textarea:visible').last();
 await composer.waitFor({state:'visible',timeout:20000});
 await composer.fill(handoffText(task,cp));
 const sendButton=p.locator('button[data-testid="send-button"]:visible, button[aria-label*="Send"]:visible, button[aria-label*="发送"]:visible').last();
 if(await sendButton.count() && await sendButton.isEnabled()) await sendButton.click();
 else await composer.press('Enter');
 await p.waitForFunction(m=>[...document.querySelectorAll('[data-message-author-role="user"]')].some(x=>(x.innerText||'').includes(m)),
  task.marker,{timeout:20000});
 const markerCount=await p.locator('[data-message-author-role="user"]').filter({hasText:task.marker}).count();
 if(markerCount!==1)throw new Error('EXACTLY_ONCE_VIOLATION:'+markerCount);
 ledgerSet(task.marker,{sentConfirmed:true,conversationUrl:p.url()});
 let assistantAck=null;
 if(task.expectedRecoveryText){
  assistantAck=await p.waitForFunction(expected=>{
   const a=[...document.querySelectorAll('[data-message-author-role="assistant"]')];
   const hit=a.find(x=>(x.innerText||x.textContent||'').includes(expected));return hit?(hit.innerText||hit.textContent||''):null;
  },task.expectedRecoveryText,{timeout:120000}).then(h=>h.jsonValue());
  ledgerSet(task.marker,{ackConfirmed:true,assistantAck});
 }
 leaseState({pageUrl:p.url(),lastMarker:task.marker,lastAction:'NEW_CONVERSATION_SAME_PAGE'});
 return {status:'TRUE_NEW_CHAT_SENT_CONFIRMED',url:p.url(),submissionCount:1,markerCount,assistantAck,pageLeaseRetained:true};
}

async function processTask(task){
 currentTask=task;lastSig='';lastProgress=now();probeDone=false;priorDisconnect=0;
 const p=await ensureLeasedPage();let o=await observe(p);
 const cp0=buildCheckpoint(task,o,task.forceRotate?'FORCED_REALITY_TEST':'TASK_MONITOR_START');
 if(task.forceRotate){
  try{return {decision:{action:'ROTATE_TO_NEW_CHAT'},recovery:await rotateTrueNewChatSamePage(task,cp0),checkpoint:checkpointPath}}
  catch(e){
   try{
    const raw=await recoverExistingChat({endpoint:cdpEndpoint,marker:task.marker,prompt:handoffText(task,cp0),
     expectedText:task.expectedRecoveryText||'',timeoutMs:task.answerTimeoutMs||120000});
    ledgerSet(task.marker,{sentConfirmed:true,conversationUrl:raw.url,rawCdp:true,ackConfirmed:raw.ackConfirmed||false});
    return {decision:{action:'ROTATE_TO_NEW_CHAT_RAW_CDP_RECOVERY'},recovery:raw,checkpoint:checkpointPath,pageLeaseRetained:true}
   }catch(rawErr){
    return {decision:{action:'FAILOVER_BACKUP'},backup:runReasonixBackup(task,cp0,
     'NEW_CHAT_RECOVERY_FAILED:'+String(e.message||e)+'; RAW_CDP_FAILED:'+String(rawErr.message||rawErr)),
     checkpoint:checkpointPath,pageLeaseRetained:true}
   }
  }
 }
 for(;;){
  o=await observe(p);const sig=[o.url,o.userTurns,o.assistantTurns,o.stop,o.lastAssistant.length,o.txtLen].join('|');
  if(sig!==lastSig){lastSig=sig;lastProgress=now();}
  if(o.humanVerification){const cp=buildCheckpoint(task,o,'HUMAN_VERIFICATION_REQUIRED');
   return {decision:{action:'FAILOVER_BACKUP'},backup:runReasonixBackup(task,cp,'HUMAN_VERIFICATION_REQUIRED'),checkpoint:checkpointPath,pageLeaseRetained:true}}
  if(o.disconnected)priorDisconnect++;
  const hard=now()-lastProgress>=silenceMs;
  const proactive=o.safeCheckpoint&&(o.userTurns>=maxTurns||o.txtLen>=maxText||priorDisconnect>0);
  const s={safeCheckpoint:o.safeCheckpoint,proactiveRotation:proactive,gptServiceAvailable:!o.serviceUnavailable,
   pageHealthy:o.composer||o.stop||o.assistantTurns>0,transportDisconnected:o.disconnected,
   backendActivityObserved:o.stop&&!hard,finalAnswerObserved:o.safeCheckpoint,readOnlyProbeDone:probeDone,
   hardDeadlineExceeded:hard,freshChatAvailable:true,freshSessionKind:'NEW_CHAT',fenceToken:task.fenceToken||0,
   writeOwner:'PRIMARY',primaryRecovered:false,humanVerificationRequired:false,primaryPathBlocked:false,alternateValidPathAvailable:false};
  const d=decide(s);
  if(d.action==='PROBE_PAGE'){probeDone=true;await sleep(pollMs);continue}
  if(d.action==='ROTATE_TO_NEW_CHAT'||d.action==='OPEN_TRUE_NEW_CHAT'){const cp=buildCheckpoint(task,o,proactive?'PROACTIVE_ROTATION':'CONFIRMED_STALL');
   try{return {decision:d,recovery:await rotateTrueNewChatSamePage(task,cp),checkpoint:checkpointPath}}
   catch(e){
    try{
     const raw=await recoverExistingChat({endpoint:cdpEndpoint,marker:task.marker,prompt:handoffText(task,cp),
      expectedText:task.expectedRecoveryText||'',timeoutMs:task.answerTimeoutMs||120000});
     ledgerSet(task.marker,{sentConfirmed:true,conversationUrl:raw.url,rawCdp:true,ackConfirmed:raw.ackConfirmed||false});
     return {decision:{...d,action:'ROTATE_TO_NEW_CHAT_RAW_CDP_RECOVERY'},recovery:raw,checkpoint:checkpointPath,pageLeaseRetained:true}
    }catch(rawErr){
     return {decision:{action:'FAILOVER_BACKUP'},backup:runReasonixBackup(task,cp,
      'NEW_CHAT_RECOVERY_FAILED:'+String(e.message||e)+'; RAW_CDP_FAILED:'+String(rawErr.message||rawErr)),
      checkpoint:checkpointPath,pageLeaseRetained:true}
    }
   }}
  if(d.action==='FAILOVER_BACKUP'){const cp=buildCheckpoint(task,o,'GPT_SERVICE_UNAVAILABLE');
   return {decision:d,backup:runReasonixBackup(task,cp,'GPT_SERVICE_UNAVAILABLE'),checkpoint:checkpointPath,pageLeaseRetained:true}}
  await sleep(pollMs);
 }
}

async function claimTaskFile(){
 const files=fs.readdirSync(inboxDir).filter(x=>x.endsWith('.json')).sort();if(!files.length)return null;
 const src=path.join(inboxDir,files[0]);return {src,name:files[0],task:readJson(src,null)};
}

async function rawCdpOwnerLoop(trigger){
 leaseState({status:'LEASE_ACTIVE',attachedVia:'RAW_CDP_EXISTING_BROWSER',cdpEndpoint,externalBrowserAttached:true,
  pageLease:true,browserMustStayOpen:true,attachFallbackReason:trigger});
 if(initialTaskPath){const q=enqueueTask(initialTaskPath);console.log(JSON.stringify(q))}
 for(;;){
  if(stopping)break;
  const item=await claimTaskFile();
  if(item&&item.task){
   const task=item.task;
   const priorCp=readJson(checkpointPath,null);
   const cp=priorCp&&priorCp.marker===task.marker?priorCp:{
    schemaVersion:1,version:'0.3.0',createdAt:new Date().toISOString(),reason:'RAW_CDP_EXISTING_BROWSER_RECOVERY',
    marker:task.marker,sourceConversationUrl:'EXISTING_CHATGPT_PAGE',taskContract:task.taskContract||task.goal||'',
    acceptedConclusion:task.acceptedConclusion||'',lastUser:'',unresolvedItems:task.unresolvedItems||[],
    nextInstruction:task.nextInstruction||'根据以上接续上下文继续当前未完成任务，从下一步唯一动作开始，不重新讨论已冻结结论。',
    safetyBoundaries:task.safetyBoundaries||[]
   };
   writeJson(checkpointPath,cp);
   try{
    const result=await recoverExistingChat({endpoint:cdpEndpoint,marker:task.marker,prompt:handoffText(task,cp),
      expectedText:task.expectedRecoveryText||'',timeoutMs:task.answerTimeoutMs||120000});
    ledgerSet(task.marker,{sentConfirmed:true,conversationUrl:result.url,rawCdp:true,ackConfirmed:result.ackConfirmed||false});
    writeJson(path.join(doneDir,item.name),{task,result:{decision:{action:'ROTATE_TO_NEW_CHAT'},recovery:result,checkpoint:checkpointPath,
      pageLeaseRetained:true},finishedAt:new Date().toISOString()});
    fs.unlinkSync(item.src);
    console.log(JSON.stringify({decision:{action:'ROTATE_TO_NEW_CHAT'},recovery:result,checkpoint:checkpointPath,pageLeaseRetained:true},null,2));
   }catch(e){
    const result={task,error:String(e.stack||e),failedAt:new Date().toISOString(),pageLeaseRetained:true};
    writeJson(path.join(failDir,item.name),result);fs.unlinkSync(item.src);console.error('RAW_CDP_TASK_FAIL',e.stack||e);
   }
  }
  leaseState({status:'LEASE_ACTIVE',attachedVia:'RAW_CDP_EXISTING_BROWSER',cdpEndpoint,externalBrowserAttached:true});
  await sleep(1000);
 }
}

async function ownerLoop(){
 try{await ensureLeasedPage()}
 catch(e){
  const msg=String(e.message||e);
  if(msg.startsWith('EXISTING_BROWSER_PRESENT_NO_SECOND_LAUNCH')) return rawCdpOwnerLoop(msg);
  throw e;
 }
 if(initialTaskPath){const q=enqueueTask(initialTaskPath);console.log(JSON.stringify(q))}
 for(;;){
  if(stopping)break;
  if(!leasedPage||leasedPage.isClosed()){
   leasedPage=null;
   try{await ensureLeasedPage();leaseState({lastAction:'REBUILT_AFTER_UNRECOVERABLE_PAGE_CLOSE'})}
   catch(e){leaseState({status:'LEASE_DEGRADED',error:String(e.message||e)})}
  }
  const item=await claimTaskFile();
  if(item&&item.task){
   try{const result=await processTask(item.task);console.log(JSON.stringify(result,null,2));
    writeJson(path.join(doneDir,item.name),{task:item.task,result,finishedAt:new Date().toISOString()});fs.unlinkSync(item.src);}
   catch(e){writeJson(path.join(failDir,item.name),{task:item.task,error:String(e.stack||e),failedAt:new Date().toISOString()});fs.unlinkSync(item.src);
    console.error('TASK_FAIL',e.stack||e);}
  }
  leaseState({currentTaskMarker:currentTask?.marker||null});
  await sleep(1000);
 }
}

async function explicitStop(signal){
 if(stopping)return;stopping=true;
 writeJson(statePath,{schemaVersion:1,status:'LEASE_RELEASED_EXPLICIT_STOP',pid:process.pid,signal,updatedAt:new Date().toISOString()});
 try{if(runtimeContext&&!externalBrowserAttached)await runtimeContext.close()}catch{}
 process.exit(0);
}
process.on('SIGINT',()=>explicitStop('SIGINT'));process.on('SIGTERM',()=>explicitStop('SIGTERM'));

ownerLoop().catch(async e=>{
 console.error('LTMVH_LEASE_OWNER_FATAL',e.stack||e);
 leaseState({status:'LEASE_FATAL',error:String(e.message||e),browserCloseRequested:false});
 // Fail closed without ordinary context.close(): the page lease remains until the owner itself is explicitly stopped
 await new Promise(()=>{});
});
