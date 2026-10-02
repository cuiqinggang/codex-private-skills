const fs=require('fs');
const path=require('path');
const {chromium}=require('playwright');
const {spawnSync}=require('child_process');
const {decide}=require('./session-continuity-supervisor');

function arg(name,def=null){const i=process.argv.indexOf('--'+name);return i>=0?process.argv[i+1]:def}
const profile=arg('profile');
const taskPath=arg('task');
const checkpointPath=arg('checkpoint',path.resolve('ltmvh-chatgpt-checkpoint.json'));
const backupResultPath=arg('backup-result',checkpointPath.replace(/\.json$/,'')+'.backup.json');
const pollMs=Number(arg('poll-ms','1200'));
const silenceMs=Number(arg('silence-ms','45000'));
const maxTurns=Number(arg('max-turns','24'));
const maxText=Number(arg('max-text','80000'));
const forceRotate=process.argv.includes('--force-rotate');
if(!profile||!taskPath) throw new Error('Usage: --profile <dir> --task <task.json> [--checkpoint <file>]');

const task=JSON.parse(fs.readFileSync(taskPath,'utf8'));
const backupEnabled=task.backupEnabled!==false;
const marker=task.marker||('LTMVH-'+Date.now());
const now=()=>Date.now();
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const rxDisconnect=/连接已断开|正在重新连接|disconnected|reconnecting/i;
const rxHuman=/verify you are human|captcha|确认您是真人|验证.*真人|just a moment|checking your browser|请稍候/i;
const rxService=/service unavailable|temporarily unavailable|bad gateway|internal server error/i;

async function observe(page){
 const o=await page.evaluate(({marker})=>{
  const txt=(document.body?.innerText||'');
  const users=[...document.querySelectorAll('[data-message-author-role="user"]')];
  const assistants=[...document.querySelectorAll('[data-message-author-role="assistant"]')];
  const visible=el=>!!(el&&el.getClientRects().length);
  const stop=[...document.querySelectorAll('button')].some(b=>visible(b)&&(
   b.getAttribute('data-testid')==='stop-button'||/Stop generating|停止生成/i.test(b.getAttribute('aria-label')||'')));
  const composer=[...document.querySelectorAll('[contenteditable="true"][role="textbox"]')].find(visible);
  const lastUser=users.at(-1)?.innerText||'';
  const lastAssistant=assistants.at(-1)?.innerText||'';
  const copyReady=!!assistants.at(-1)?.closest('article,[data-testid^="conversation-turn-"]')
    ?.querySelector('button[data-testid*="copy"],button[aria-label*="复制"],button[aria-label*="Copy"]');
  const markerPresent=users.some(x=>(x.innerText||'').includes(marker));
  return {txtLen:txt.length,userTurns:users.length,assistantTurns:assistants.length,stop,composer:!!composer,
   lastUser,lastAssistant,copyReady,markerPresent,url:location.href,title:document.title,bodyText:txt.slice(0,12000)};
 },{marker});
 const body=o.bodyText;
 return {...o,
  disconnected:rxDisconnect.test(body),
  humanVerification:rxHuman.test(body)||rxHuman.test(o.title||''),
  serviceUnavailable:rxService.test(body),
  safeCheckpoint:!o.stop&&o.composer&&o.assistantTurns>0&&o.copyReady};
}

function buildCheckpoint(obs,reason){
 const payload={
  schemaVersion:1,version:'0.3.0',createdAt:new Date().toISOString(),reason,
  marker,sourceConversationUrl:obs.url,
  taskContract:task.taskContract||task.goal||'',
  acceptedConclusion:(obs.lastAssistant||'').slice(0,12000),
  lastUser:(obs.lastUser||'').slice(0,6000),
  unresolvedItems:task.unresolvedItems||[],
  nextInstruction:task.nextInstruction||'根据以上接续上下文继续当前未完成任务，从下一步唯一动作开始，不重新讨论已冻结结论。',
  safetyBoundaries:task.safetyBoundaries||[],
 };
 fs.writeFileSync(checkpointPath,JSON.stringify(payload,null,2));
 return payload;
}

function backupHandoffText(cp,trigger){
 return [
  '[LTMVH_BACKUP_RECOVERY '+marker+']',
  'GPT/ChatGPT 主路当前不可用或恢复失败。你是独立备脑。读取同一个任务合同与 Checkpoint，继续到相同 DONE_WHEN；不要降低完成标准。',
  '【切换原因】\n'+trigger,
  '【任务合同】\n'+cp.taskContract,
  '【上一阶段已确认结论】\n'+cp.acceptedConclusion,
  '【未完成】\n'+JSON.stringify(cp.unresolvedItems),
  '【安全边界】\n'+JSON.stringify(cp.safetyBoundaries),
  '【下一步唯一动作】\n'+cp.nextInstruction,
  '不得修改 Windows 系统；不得修改 FlClash / Windows 网络代理；不可逆高风险、支付、账号安全动作必须停在权限门。'
 ].join('\n\n');
}

function runReasonixBackup(cp,trigger){
 if(!backupEnabled) return {status:'BACKUP_DISABLED',trigger};
 const prompt=backupHandoffText(cp,trigger);
 const started=Date.now();
 const opts={input:prompt,encoding:'utf8',timeout:180000,maxBuffer:8*1024*1024,windowsHide:true};
 const r=process.platform==='win32'
  ? spawnSync(process.env.ComSpec||'cmd.exe',['/d','/s','/c','reasonix run --output-format json'],opts)
  : spawnSync('reasonix',['run','--output-format','json'],opts);
 const stdout=(r.stdout||'').trim(), stderr=(r.stderr||'').trim();
 let parsed=null;
 for(const line of stdout.split(/\r?\n/).filter(Boolean).reverse()){
  try{parsed=JSON.parse(line);break}catch{}
 }
 const ok=!r.error&&r.status===0&&parsed&&parsed.subtype==='success'&&parsed.is_error===false;
 const out={schemaVersion:1,status:ok?'BACKUP_COMPLETED':'BACKUP_FAILED',trigger,startedAtEpochMs:started,
  durationMs:Date.now()-started,exitCode:r.status,error:r.error?String(r.error.message||r.error):null,
  reasonix:parsed,stderr:stderr.slice(0,4000),marker};
 fs.writeFileSync(backupResultPath,JSON.stringify(out,null,2));
 if(!ok) throw new Error('BACKUP_FAIL:'+JSON.stringify(out));
 return out;
}

function handoffText(cp){
 const text=[
  '[LTMVH_RECOVERY '+marker+']',
  '这是故障恢复后的真正新聊天，不是 Branch。只使用以下最小接续上下文继续。',
  '【任务合同】\n'+cp.taskContract,
  '【上一阶段已确认结论】\n'+cp.acceptedConclusion,
  '【未完成】\n'+JSON.stringify(cp.unresolvedItems),
  '【安全边界】\n'+JSON.stringify(cp.safetyBoundaries),
  '【下一步唯一动作】\n'+cp.nextInstruction
 ].join('\n\n');
 if(text.length>24000) throw new Error('HANDOFF_TOO_LARGE: '+text.length);
 return text;
}

async function markerExists(context){
 for(const p of context.pages()){
  if(!/chatgpt\.com/.test(p.url())) continue;
  try{
   const n=await p.locator('[data-message-author-role="user"]').filter({hasText:marker}).count();
   if(n>0) return p.url();
  }catch{}
 }
 return null;
}

async function rotateTrueNewChat(context,cp){
 const prior=await markerExists(context);
 if(prior) return {status:'ALREADY_DELIVERED_NO_RESEND',url:prior};
 const p=await context.newPage();
 await p.goto('https://chatgpt.com/',{waitUntil:'domcontentloaded',timeout:60000});
 await sleep(1200);
 const first=await observe(p);
 console.log(JSON.stringify({event:'NEW_CHAT_PROBE',url:p.url(),title:first.title,composer:first.composer,userTurns:first.userTurns,assistantTurns:first.assistantTurns,body:first.bodyText.slice(0,1600)}));
 if(first.humanVerification) throw new Error('HUMAN_VERIFICATION_REQUIRED');
 const u=new URL(p.url());
 if(/^\/c\//.test(u.pathname)||/branch/i.test(p.url())) throw new Error('NOT_TRUE_NEW_CHAT:'+p.url());
 const composer=p.locator('[contenteditable="true"][role="textbox"]:visible').last();
 await composer.waitFor({state:'visible',timeout:20000});
 await composer.fill(handoffText(cp));
 await composer.press('Enter');
 await p.waitForFunction(m=>[...document.querySelectorAll('[data-message-author-role="user"]')]
   .some(x=>(x.innerText||'').includes(m)),marker,{timeout:20000});
 return {status:'TRUE_NEW_CHAT_SENT_CONFIRMED',url:p.url(),source:cp.sourceConversationUrl};
}

let runtimeContext=null;
(async()=>{
 runtimeContext=await chromium.launchPersistentContext(profile,{headless:false,viewport:{width:1365,height:850}});
 const context=runtimeContext;
 let page=context.pages().find(p=>/chatgpt\.com/.test(p.url())&&/\/c\//.test(new URL(p.url()).pathname))
   ||context.pages().find(p=>/chatgpt\.com/.test(p.url()));
 if(!page){page=await context.newPage();await page.goto('https://chatgpt.com/',{waitUntil:'domcontentloaded'});}
 let lastSig='',lastProgress=now(),probeDone=false,priorDisconnect=0;
 if(forceRotate){
  const o=await observe(page);
  const cp=buildCheckpoint(o,'FORCED_REALITY_TEST');
  if(o.humanVerification){
   const b=runReasonixBackup(cp,'HUMAN_VERIFICATION_REQUIRED_SOURCE_PAGE');
   console.log(JSON.stringify({decision:{action:'FAILOVER_BACKUP'},backup:b,checkpoint:checkpointPath},null,2));
   await context.close(); runtimeContext=null; return;
  }
  try{
   const r=await rotateTrueNewChat(context,cp);
   console.log(JSON.stringify({decision:{action:'ROTATE_TO_NEW_CHAT'},recovery:r,checkpoint:checkpointPath},null,2));
  }catch(e){
   const b=runReasonixBackup(cp,'NEW_CHAT_RECOVERY_FAILED:'+String(e.message||e));
   console.log(JSON.stringify({decision:{action:'FAILOVER_BACKUP'},backup:b,checkpoint:checkpointPath},null,2));
  }
  await context.close(); runtimeContext=null; return;
 }
 for(;;){
  const o=await observe(page);
  const sig=[o.url,o.userTurns,o.assistantTurns,o.stop,o.lastAssistant.length,o.txtLen].join('|');
  if(sig!==lastSig){lastSig=sig;lastProgress=now();}
  if(o.humanVerification){
   const cp=buildCheckpoint(o,'HUMAN_VERIFICATION_REQUIRED');
   const b=runReasonixBackup(cp,'HUMAN_VERIFICATION_REQUIRED');
   console.log(JSON.stringify({decision:{action:'FAILOVER_BACKUP'},backup:b,checkpoint:checkpointPath},null,2));
   break;
  }
  if(o.disconnected) priorDisconnect++;
  const hard=now()-lastProgress>=silenceMs;
  const proactive=o.safeCheckpoint&&(o.userTurns>=maxTurns||o.txtLen>=maxText||priorDisconnect>0);
  const state={
   safeCheckpoint:o.safeCheckpoint,proactiveRotation:proactive,
   gptServiceAvailable:!o.serviceUnavailable,pageHealthy:o.composer||o.stop||o.assistantTurns>0,
   transportDisconnected:o.disconnected,backendActivityObserved:o.stop&&!hard,
   finalAnswerObserved:o.safeCheckpoint,readOnlyProbeDone:probeDone,hardDeadlineExceeded:hard,
   freshChatAvailable:true,freshSessionKind:'NEW_CHAT',fenceToken:task.fenceToken||0,
   writeOwner:'PRIMARY',primaryRecovered:false,humanVerificationRequired:false,
   primaryPathBlocked:false,alternateValidPathAvailable:false
  };
  const d=decide(state);
  if(d.action==='PROBE_PAGE'){probeDone=true;await sleep(pollMs);continue;}
  if(d.action==='ROTATE_TO_NEW_CHAT'||d.action==='OPEN_TRUE_NEW_CHAT'){
   const cp=buildCheckpoint(o,proactive?'PROACTIVE_ROTATION':'CONFIRMED_STALL');
   try{
    const r=await rotateTrueNewChat(context,cp);
    console.log(JSON.stringify({decision:d,recovery:r,checkpoint:checkpointPath},null,2));
   }catch(e){
    const b=runReasonixBackup(cp,'NEW_CHAT_RECOVERY_FAILED:'+String(e.message||e));
    console.log(JSON.stringify({decision:{action:'FAILOVER_BACKUP'},backup:b,checkpoint:checkpointPath},null,2));
   }
   break;
  }
  if(d.action==='FAILOVER_BACKUP'){
   const cp=buildCheckpoint(o,'GPT_SERVICE_UNAVAILABLE');
   const b=runReasonixBackup(cp,'GPT_SERVICE_UNAVAILABLE');
   console.log(JSON.stringify({decision:d,backup:b,checkpoint:checkpointPath},null,2));
   break;
  }
  await sleep(pollMs);
 }
 await context.close(); runtimeContext=null;
})().catch(async e=>{
 console.error('LTMVH_CONTINUITY_RUNTIME_FAIL',e.stack||e.message);
 try{if(runtimeContext) await runtimeContext.close();}catch{}
 runtimeContext=null;
 process.exitCode=1;
});