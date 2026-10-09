// B33 TEST-ONLY fixture: attacks on validated state and the mature formal ChatGPT entry.
// Completely offline; no chatgpt.com, real identity, proxy, or production CURRENT mutations.
const assert=require('node:assert/strict');
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const {chromium}=require('playwright');
const base=path.resolve(__dirname,'..');
const formalSource=fs.readFileSync(path.join(base,'skills','playwright-native-ai-browser','scripts','chatgpt-business-entry.js'),'utf8');
const formal=vm.runInNewContext('('+formalSource+')');
const task='B_SINGLE_PAGE_MATURITY_20261009',repo='cuiqinggang/codex-private-skills',freeze='B33-VM-F012';
const good='续接B|'+repo+'|'+task+'|'+freeze;
const userMarker='B33_TEST_CHAT_OWNERSHIP:'+task;
const ack='ACK-B33-VIRTUAL-F012';
let tested=0,passed=0,log=[];
function test(n,condition){tested++; const ok=!!condition; if(ok)passed++;log.push({case:n,pass:ok});if(!ok)throw Error('VIRTUAL_ASSERTION_FAIL '+n);}
function decideCode(s){
 const p=s.split('|'); if(p.length!==4||p[0]!=='续接B'||p[1]!==repo)return'BAD_FORMAT';
 if(p[2]!==task)return'WRONG_TASK';
 if(p[3]!==freeze)return'STALE_OR_WRONG_FREEZE';
 return'VALID_INDEX';
}
const html = `<!doctype html><html><meta charset="utf-8">
<body><button id="newchat" aria-label="新聊天">新聊天</button>
<div id="turns"><article data-message-author-role="user">B33_TEST_CHAT_OWNERSHIP:B_SINGLE_PAGE_MATURITY_20261009</article></div>
<div role="textbox" contenteditable="true"></div><button type="submit" aria-label="发送">发送</button>
<script>
window.__new=0; window.__sent=0;
const turns=document.querySelector('#turns');
const editor=document.querySelector('[role="textbox"]');
document.querySelector('#newchat').onclick=()=>{window.__new++;turns.textContent='';editor.textContent='';history.pushState({},'','/');};
document.querySelector('button[type="submit"]').onclick=()=>{
const msg=editor.textContent;if(!msg)return;window.__sent++;
const user=document.createElement('article');user.setAttribute('data-message-author-role','user');user.textContent=msg;turns.append(user);
const ans=document.createElement('article');ans.setAttribute('data-message-author-role','assistant');ans.textContent='ACK-B33-VIRTUAL-F012';
const copy=document.createElement('button');copy.setAttribute('data-testid','copy-turn-action');ans.append(copy);turns.append(ans);
editor.textContent='';history.pushState({},'','/c/virtual-'+window.__sent);
};
</script></body></html>`;
const run=async(page,config)=>{await page.evaluate(x=>sessionStorage.setItem('__pw_native_business_task_v1',JSON.stringify(x)),config);return formal(page)};
async function main(){
 const begin=Date.now();
 const browser=await chromium.launch({headless:true});
 try{
 test('state-code-current-valid',decideCode(good)==='VALID_INDEX');
 test('reject-stale-F011',decideCode(good.replace('F012','F011'))==='STALE_OR_WRONG_FREEZE');
 test('reject-other-task',decideCode(good.replace(task,'OTHER_TASK'))==='WRONG_TASK');
 test('reject-invalid-format',decideCode('F012')==='BAD_FORMAT');
 const results=[];
 // Independent browser contexts emulate independent owned tasks, never shared writable user sessions.
 for(let i=0;i<3;i++){
  const context=await browser.newContext();
  const page=await context.newPage();
  await page.route('http://b33-virtual.local/**',route=>route.fulfill({status:200,contentType:'text/html',body:html}));
  const started=Date.now(); await page.goto('http://b33-virtual.local/c/owner-'+i);
  test('owner-visible-'+i,(await page.locator('#turns').innerText()).includes(userMarker));
  test('exactly-one-newchat-'+i,await page.getByRole('button',{name:'新聊天'}).count()===1);
  await page.getByRole('button',{name:'新聊天'}).click();
  test('switched-to-root-'+i,new URL(page.url()).pathname==='/');
  const marker=good; // Exact four-field short code; identity isolation comes from independent contexts
  const first=await run(page,{operation:'query',marker,answerMarker:ack});
  test('query-before-send-0-'+i,first.userCount===0);
  const sent=await run(page,{operation:'send',marker,prompt:marker,answerMarker:ack});
  test('sent-confirmed-'+i,sent.status==='SENT_CONFIRMED'&&sent.submissionCount===1);
  const dupe=await run(page,{operation:'send',marker,prompt:marker,answerMarker:ack});
  test('duplicate-refused-'+i,dupe.status==='ALREADY_RECEIVED_NO_RESEND'&&dupe.submissionCount===0);
  const extracted=await run(page,{operation:'wait_extract',marker,answerMarker:ack,requiredText:[ack],pollIntervalMs:20,answerTimeoutMs:4000});
  test('scoped-ack-'+i,extracted.status==='COMPLETE_EXTRACTED'&&extracted.answerMarkdown.includes(ack));
  // Inject ACK-loss after user message was received.
  await page.evaluate(()=>document.querySelector('[data-message-author-role="assistant"]').remove());
  const missing=await run(page,{operation:'query',marker,answerMarker:ack});
  test('ack-loss-readonly-detected-'+i,missing.userCount===1&&!missing.assistantFound);
  const retry=await run(page,{operation:'send',marker,prompt:marker,answerMarker:ack});
  test('ack-loss-no-resend-'+i,retry.status==='ALREADY_RECEIVED_NO_RESEND'&&retry.submissionCount===0);
  await page.evaluate(a=>{let n=document.createElement('article');n.setAttribute('data-message-author-role','assistant');n.textContent=a;const b=document.createElement('button');b.setAttribute('data-testid','copy-turn-action');n.append(b);document.querySelector('#turns').append(n)},ack);
  const restored=await run(page,{operation:'wait_extract',marker,answerMarker:ack,requiredText:[ack],pollIntervalMs:20,answerTimeoutMs:4000});
  test('ack-returned-and-validated-'+i,restored.status==='COMPLETE_EXTRACTED');
  const count=await page.evaluate(()=>({sent:window.__sent,newchat:window.__new}));
  test('no-extra-newchat-after-valid-'+i,count.newchat===1);
  test('exactly-one-submission-'+i,count.sent===1);
  results.push({branch:i,elapsedMs:Date.now()-started,sent:count.sent,newchat:count.newchat});
  await context.close();
 }
 // Failure gates with no browser actions; these are deterministic task-specific contract assertions.
 const guard=(x)=>{
  if(x.final)return'NO_NEW_CHAT';
  if(!x.persisted)return'BLOCK_NOT_FROZEN';
  if(x.unknown)return'BLOCK_UNKNOWN';
  if(!x.isolated)return'BLOCK_UNOWNED';
  if(!x.platformAllowed)return'BLOCK_PLATFORM';
  if(x.writers!==1)return'BLOCK_WRITER';
  if(!x.selectedDocUnique)return'BLOCK_AMBIGUOUS_DOCUMENT';
  return'PREPARED_FOR_ONE_REALITY';
 };
 const valid={final:false,persisted:true,unknown:false,isolated:true,platformAllowed:true,writers:1,selectedDocUnique:true};
 for(const [label,delta,expected] of [
  ['done',{final:true},'NO_NEW_CHAT'],['no-freeze',{persisted:false},'BLOCK_NOT_FROZEN'],
  ['unknown',{unknown:true},'BLOCK_UNKNOWN'],['wrong-owner',{isolated:false},'BLOCK_UNOWNED'],
  ['safety-block',{platformAllowed:false},'BLOCK_PLATFORM'],
  ['multi-writer',{writers:2},'BLOCK_WRITER'],['doc-ambiguous',{selectedDocUnique:false},'BLOCK_AMBIGUOUS_DOCUMENT']
 ])test('fail-closed-'+label,guard({...valid,...delta})===expected);
 console.log(JSON.stringify({status:'PASS',mode:'OFFLINE_VIRTUAL_ONLY',task,freeze,formalEntryReused:true,assertions:{passed,total:tested},branches:results,completedMockWallMs:Date.now()-begin,realChatGPTSends:0,validity:'LOCAL_FIXTURE_ONLY',stopGate:'NOT_APPLICABLE_NO_REAL_BASELINE_OR_MODEL_LATENCY'}));
 }finally{await browser.close()}
}
main().catch(e=>{console.error(e.stack||String(e));process.exitCode=1});
