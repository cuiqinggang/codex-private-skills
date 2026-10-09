// B33 isolated offline regression harness. NO chatgpt.com access, no real browser identity.
// Reuses the existing formal business entrypoint without modifying it.
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const { chromium } = require('playwright');
const root = path.resolve(__dirname,'..');
const formalSource = fs.readFileSync(path.join(root,'skills','playwright-native-ai-browser','scripts','chatgpt-business-entry.js'),'utf8');
const formal = vm.runInNewContext('('+formalSource+')');
const code = '续接B|cuiqinggang/codex-private-skills|B_SINGLE_PAGE_MATURITY_20261009|B33-VM-F011';
const ack = 'ACK-B33-OFFLINE-HANDOFF-F011';
const html = `<!doctype html><html lang="zh"><meta charset="utf-8"><title>B33 offline fixture</title>
<body><main>
<button id="newchat" aria-label="新聊天">新聊天</button>
<div id="turns"><article data-message-author-role="user">B33_TEST_CHAT_OWNERSHIP:OFFLINE_FIXTURE</article></div>
<div role="textbox" contenteditable="true" aria-label="询问 ChatGPT"></div>
<button id="submit" type="submit" aria-label="发送">发送</button>
</main><script>
window.__sent=0; window.__new=0;
const turns=document.querySelector('#turns');
const composer=document.querySelector('[role="textbox"]');
document.querySelector('#newchat').onclick=()=>{
 window.__new++; turns.textContent=''; composer.textContent='';
 history.pushState({},'', '/'); 
};
document.querySelector('#submit').onclick=()=>{
 const text=composer.textContent;
 if (!text) return;
 window.__sent++;
 const u=document.createElement('article');
 u.setAttribute('data-message-author-role','user'); u.textContent=text; turns.append(u);
 const a=document.createElement('article');
 a.setAttribute('data-message-author-role','assistant');
 a.textContent='ACK-B33-OFFLINE-HANDOFF-F011';
 const copy=document.createElement('button');copy.setAttribute('data-testid','copy-turn-action');copy.textContent='Copy';
 a.append(copy);turns.append(a);composer.textContent='';
 history.pushState({},'','/c/offline-fixture');
};
</script></body></html>`;
(async ()=>{
 const started=Date.now();
 const browser=await chromium.launch({headless:true});
 try{
  const page=await browser.newPage();
  await page.route('http://b33-fixture.local/**',route=>route.fulfill({status:200,contentType:'text/html',body:html}));
  await page.goto('http://b33-fixture.local/c/original');
  assert.match(await page.locator('#turns').innerText(), /B33_TEST_CHAT_OWNERSHIP/);
  const beforeNew=Date.now();
  await page.getByRole('button',{name:'新聊天'}).click();
  const afterNew=Date.now();
  assert.equal(new URL(page.url()).pathname,'/');
  assert.equal(await page.locator('#turns article').count(),0);
  const withTask=async cfg=>{
   await page.evaluate(c=>sessionStorage.setItem('__pw_native_business_task_v1',JSON.stringify(c)),cfg);
   return formal(page);
  };
  const q0=await withTask({operation:'query',marker:code,answerMarker:ack});
  assert.equal(q0.userCount,0);
  const t1=Date.now();
  const send=await withTask({operation:'send',marker:code,prompt:code,answerMarker:ack});
  assert.equal(send.status,'SENT_CONFIRMED');
  assert.equal(send.submissionCount,1);
  const t2=Date.now();
  const q1=await withTask({operation:'query',marker:code,answerMarker:ack});
  assert.equal(q1.userCount,1);
  assert.equal(q1.answerMarkerPresent,true);
  const dupe=await withTask({operation:'send',marker:code,prompt:code,answerMarker:ack});
  assert.equal(dupe.status,'ALREADY_RECEIVED_NO_RESEND');
  assert.equal(dupe.submissionCount,0);
  const result=await withTask({operation:'wait_extract',marker:code,answerMarker:ack,requiredText:[ack],pollIntervalMs:20,answerTimeoutMs:4000});
  assert.equal(result.status,'COMPLETE_EXTRACTED');
  assert.match(result.answerMarkdown, /ACK-B33-OFFLINE-HANDOFF-F011/);
  assert.equal(await page.evaluate(()=>window.__sent),1);
  assert.equal(await page.evaluate(()=>window.__new),1);
  // Fault injection: response disappears after the user message was accepted.
  // The mature entry must never resend just because the ACK is temporarily absent.
  await page.evaluate(() => document.querySelector('[data-message-author-role="assistant"]').remove());
  const lostAck = await withTask({operation:'query',marker:code,answerMarker:ack});
  assert.equal(lostAck.userCount,1);
  assert.equal(lostAck.assistantFound,false);
  const noRetry = await withTask({operation:'send',marker:code,prompt:code,answerMarker:ack});
  assert.equal(noRetry.status,'ALREADY_RECEIVED_NO_RESEND');
  assert.equal(await page.evaluate(()=>window.__sent),1);
  await page.evaluate(ackText=>{
   const a=document.createElement('article');
   a.setAttribute('data-message-author-role','assistant');
   a.textContent=ackText;
   const copy=document.createElement('button');
   copy.setAttribute('data-testid','copy-turn-action');
   a.append(copy);
   document.querySelector('#turns').append(a);
  },ack);
  const recovered = await withTask({operation:'wait_extract',marker:code,answerMarker:ack,requiredText:[ack],pollIntervalMs:20,answerTimeoutMs:4000});
  assert.equal(recovered.status,'COMPLETE_EXTRACTED');
  assert.equal(await page.evaluate(()=>window.__sent),1);
  console.log(JSON.stringify({status:'B33_OFFLINE_MATURE_ENTRY_PASS',transport:'isolated mocked DOM only',newChatClicks:1,formalEntry: 'chatgpt-business-entry.js',queryBefore: q0.userCount,sendStatus:send.status,sendCount:1,queryAfter:q1.userCount,duplicateStatus:dupe.status,extracted:result.status,ack,resultUrl:page.url(),elapsedLocalFixtureMs:Date.now()-started,newChatClickMs:afterNew-beforeNew,formalSendMs:t2-t1,realChatGPTSubmissions:0}));
 }finally{await browser.close()}
})().catch(e=>{console.error(e.stack||String(e));process.exitCode=1});
