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

async function recoverExistingChat({endpoint='http://127.0.0.1:9223',marker,prompt,expectedText='',timeoutMs=120000}){
 const target=await findChatgptTarget(endpoint);
 if(!target) throw new Error('NO_EXISTING_CHATGPT_TARGET');
 const c=await new CdpClient(target.webSocketDebuggerUrl).open();
 try{
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
   const path=await c.eval('location.pathname');
   if(path!=='/'&&path!=='') throw new Error('NOT_TRUE_NEW_CHAT:'+path);
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
 }finally{c.close()}
}

module.exports={recoverExistingChat,findChatgptTarget};
