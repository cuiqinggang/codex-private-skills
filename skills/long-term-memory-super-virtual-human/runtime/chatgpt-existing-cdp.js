const sleep=ms=>new Promise(r=>setTimeout(r,ms));

class CdpClient{
 constructor(wsUrl){this.wsUrl=wsUrl;this.ws=null;this.seq=0;this.pending=new Map()}
 async open(){
  this.ws=new WebSocket(this.wsUrl);
  this.ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.id&&this.pending.has(m.id)){const h=this.pending.get(m.id);this.pending.delete(m.id);m.error?h.reject(new Error(JSON.stringify(m.error))):h.resolve(m.result)}};
  await new Promise((resolve,reject)=>{this.ws.onopen=resolve;this.ws.onerror=()=>reject(new Error('CDP_WS_OPEN_FAIL'))});
  return this;
 }
 send(method,params={}){
  return new Promise((resolve,reject)=>{const id=++this.seq;this.pending.set(id,{resolve,reject});this.ws.send(JSON.stringify({id,method,params}))});
 }
 async eval(expression){
  const r=await this.send('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});
  return r.result?.value;
 }
 close(){try{this.ws?.close()}catch{}}
}

async function findChatgptTarget(endpoint){
 const base=endpoint.replace(/\/$/,'');
 const list=await (await fetch(base+'/json/list')).json();
 return list.find(x=>x.type==='page'&&String(x.url||'').startsWith('https://chatgpt.com/'))||null;
}

async function withChat(endpoint,fn){
 const target=await findChatgptTarget(endpoint);
 if(!target) throw new Error('NO_EXISTING_CHATGPT_TARGET');
 const c=await new CdpClient(target.webSocketDebuggerUrl).open();
 try{return await fn(c,target)}finally{c.close()}
}

async function observeExistingChat(endpoint='http://127.0.0.1:9223'){
 return withChat(endpoint,async c=>{
  const raw=await c.eval(`JSON.stringify((()=>{const txt=document.body?.innerText||'';const vis=e=>!!(e&&e.getClientRects().length);const users=[...document.querySelectorAll('[data-message-author-role="user"]')];const assistants=[...document.querySelectorAll('[data-message-author-role="assistant"]')];const stop=[...document.querySelectorAll('button')].some(b=>vis(b)&&(b.getAttribute('data-testid')==='stop-button'||/^(Stop generating|Stop|停止生成|停止)$/i.test(b.getAttribute('aria-label')||'')));const composer=[document.querySelector('#prompt-textarea'),...document.querySelectorAll('[contenteditable="true"]'),...document.querySelectorAll('textarea')].find(vis);const lastUser=users.at(-1)?.innerText||'';const lastAssistant=assistants.at(-1)?.innerText||'';const copyReady=!!assistants.at(-1)?.closest('article,[data-testid^="conversation-turn-"]')?.querySelector('button[data-testid*="copy"],button[aria-label*="复制"],button[aria-label*="Copy"]');return {txtLen:txt.length,userTurns:users.length,assistantTurns:assistants.length,stop,composer:!!composer,lastUser,lastAssistant,copyReady,url:location.href,title:document.title,bodyText:txt.slice(0,12000)}})())`);
  const o=JSON.parse(raw||'{}');
  return {...o,
   disconnected:/连接已断开|正在重新连接|disconnected|reconnecting/i.test(o.bodyText||''),
   humanVerification:/verify you are human|captcha|确认您是真人|验证.*真人|just a moment|checking your browser|请稍候/i.test((o.bodyText||'')+' '+(o.title||'')),
   serviceUnavailable:/service unavailable|temporarily unavailable|bad gateway|internal server error/i.test(o.bodyText||''),
   uiFailure:/something went wrong|try again|unable to load|network error|出了点问题|出现错误|重试|加载失败|网络错误/i.test(o.bodyText||''),
   safeCheckpoint:!o.stop&&o.composer&&o.assistantTurns>0&&o.copyReady
  };
 });
}

async function abortExistingChatTurn(endpoint='http://127.0.0.1:9223'){
 return withChat(endpoint,async c=>{
  const clicked=await c.eval(`(()=>{const vis=e=>!!(e&&e.getClientRects().length);const b=[...document.querySelectorAll('button')].find(x=>vis(x)&&(x.getAttribute('data-testid')==='stop-button'||/^(Stop generating|Stop|停止生成|停止)$/i.test(x.getAttribute('aria-label')||'')));if(!b)return false;b.click();return true})()`);
  if(!clicked) throw new Error('STALL_ABORT_BUTTON_NOT_FOUND');
  for(let i=0;i<60;i++){
   const done=await c.eval(`(()=>{const vis=e=>!!(e&&e.getClientRects().length);const stop=[...document.querySelectorAll('button')].some(b=>vis(b)&&(b.getAttribute('data-testid')==='stop-button'||/^(Stop generating|Stop|停止生成|停止)$/i.test(b.getAttribute('aria-label')||'')));const composer=[document.querySelector('#prompt-textarea'),...document.querySelectorAll('[contenteditable="true"]'),...document.querySelectorAll('textarea')].find(vis);return !stop&&!!composer})()`);
   if(done)return true;
   await sleep(250);
  }
  throw new Error('STALL_ABORT_NOT_CONFIRMED');
 });
}

async function recoverExistingChat({endpoint='http://127.0.0.1:9223',marker,prompt,expectedText='',timeoutMs=120000}){
 return withChat(endpoint,async c=>{
  const currentComposerText=await c.eval("(()=>{const e=document.querySelector('#prompt-textarea,[contenteditable=\"true\"][role=\"textbox\"],textarea');return e?(e.innerText||e.textContent||e.value||''):''})()");
  const currentBodyHasMarker=await c.eval("(document.body?.innerText||'').includes("+JSON.stringify(marker)+")");
  let submissionCount=0;
  if(currentComposerText&&currentComposerText.includes(marker)){
   let clickedDraft=false;
   for(let i=0;i<80;i++){
    clickedDraft=await c.eval("(()=>{const b=document.querySelector('button[aria-label=\"发送\"],button[data-testid=\"send-button\"],button[data-testid=\"composer-submit-button\"],button[aria-label*=\"Send\"]');if(!b||b.disabled||!b.getClientRects().length)return false;b.click();return true})()");
    if(clickedDraft)break;
    await sleep(250);
   }
   if(!clickedDraft) throw new Error('EXISTING_DRAFT_SEND_BUTTON_UNAVAILABLE');
   submissionCount=1;
  }else if(!currentBodyHasMarker){
   await c.send('Page.navigate',{url:'https://chatgpt.com/'});
   let composer=false;
   for(let i=0;i<40;i++){
    composer=await c.eval("Boolean(document.querySelector('#prompt-textarea,[contenteditable=\"true\"][role=\"textbox\"],textarea'))");
    if(composer)break;
    await sleep(500);
   }
   if(!composer) throw new Error('TRUE_NEW_CHAT_COMPOSER_NOT_READY');
   const pathname=await c.eval('location.pathname');
   if(pathname!=='/'&&pathname!=='') throw new Error('NOT_TRUE_NEW_CHAT:'+pathname);
   const focused=await c.eval("(()=>{const e=document.querySelector('#prompt-textarea,[contenteditable=\"true\"][role=\"textbox\"],textarea');if(!e)return false;e.focus();return true})()");
   if(!focused) throw new Error('NO_COMPOSER');
   await c.send('Input.insertText',{text:prompt});
   let clicked=false;
   for(let i=0;i<80;i++){
    clicked=await c.eval("(()=>{const b=document.querySelector('button[aria-label=\"发送\"],button[data-testid=\"send-button\"],button[data-testid=\"composer-submit-button\"],button[aria-label*=\"Send\"]');if(!b||b.disabled||!b.getClientRects().length)return false;b.click();return true})()");
    if(clicked)break;
    await sleep(250);
   }
   if(!clicked) throw new Error('NO_ENABLED_SEND_BUTTON');
   submissionCount=1;
  }
  let markerSeen=false;
  for(let i=0;i<40;i++){
   markerSeen=await c.eval("(document.body?.innerText||'').includes("+JSON.stringify(marker)+")");
   if(markerSeen)break;
   await sleep(500);
  }
  if(!markerSeen) throw new Error('MARKER_CONFIRM_FAIL');
  let ackSeen=!expectedText;
  const start=Date.now();
  while(!ackSeen&&Date.now()-start<timeoutMs){
   ackSeen=await c.eval("(document.body?.innerText||'').includes("+JSON.stringify(expectedText)+")");
   if(ackSeen)break;
   await sleep(500);
  }
  if(!ackSeen) throw new Error('ACK_TIMEOUT');
  return {status:submissionCount===0?'ALREADY_DELIVERED_NO_RESEND':'TRUE_NEW_CHAT_SENT_CONFIRMED',submissionCount,markerCount:1,ackConfirmed:ackSeen,
   url:await c.eval('location.href'),transport:'RAW_CDP_EXISTING_BROWSER',branchUsed:false,newBrowserLaunched:false};
 });
}

module.exports={recoverExistingChat,findChatgptTarget,observeExistingChat,abortExistingChatTurn};