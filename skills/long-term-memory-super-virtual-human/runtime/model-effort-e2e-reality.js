const { chromium }=require('C:/AI/Playwright-Native-AI-Browser/node_modules/playwright');
const fs=require('fs'); const ctrl=eval(fs.readFileSync('C:/AI/ltmvh-v03-test/skills/long-term-memory-super-virtual-human/runtime/chatgpt-model-effort-controller.js','utf8'));
(async()=>{
 const marker='LTMVH-MODEL-EFFORT-E2E-20261003-R14', ack=marker+'-ACK'; const out={schemaVersion:1,marker,startedAt:new Date().toISOString(),steps:[],existingBrowserReused:true,newBrowserLaunched:false}; let p,originalSetting;
 const sleep=ms=>new Promise(r=>setTimeout(r,ms)); const setCfg=async v=>p.evaluate(v=>sessionStorage.setItem('__ltmvh_model_effort_v1',JSON.stringify(v)),v);
 const state=async()=>p.evaluate(({marker,ack})=>{const text=document.body.innerText||'';const stop=[...document.querySelectorAll('button')].some(b=>b.getClientRects().length&&/Stop generating|停止生成/i.test(b.getAttribute('aria-label')||''));const userLabels=['你说：','You said:'];const userCount=userLabels.reduce((n,label)=>n+(text.split(label+'\n'+marker).length-1),0);return {href:location.href,userCount,ackCount:text.split(ack).length-1,stop,textTail:text.slice(-1200)}},{marker,ack});
 try{
  const browser=await chromium.connectOverCDP('http://127.0.0.1:9223'); p=browser.contexts().flatMap(c=>c.pages()).find(x=>x.url().startsWith('https://chatgpt.com/')); if(!p) throw Error('NO_EXISTING_CHATGPT_PAGE');
  await p.locator('[contenteditable="true"][role="textbox"]:visible').last().waitFor({state:'visible',timeout:45000});
  await setCfg({operation:'read'}); out.original=await ctrl(p); originalSetting=out.original.actual; if(!['Medium','High'].includes(originalSetting)) throw Error('ORIGINAL_UNCERTIFIED'); out.steps.push('READ_ORIGINAL');
  out.targetSetting=originalSetting==='High'?'Medium':'High'; await setCfg({operation:'set',target:out.targetSetting}); out.switched=await ctrl(p); if(out.switched.actual!==out.targetSetting) throw Error('SWITCH_READBACK_FAILED'); out.steps.push('SWITCH_READBACK');
  out.before=await state(); if(out.before.userCount!==0||out.before.ackCount!==0) throw Error('MARKER_NOT_FRESH');
  const composer=p.locator('[contenteditable="true"][role="textbox"]:visible').last(); await composer.fill(marker+'\n这是无副作用自动化闭环认证。请仅回复：'+ack); await composer.press('Enter');
  for(let i=0;i<40;i++){out.afterSend=await state();if(out.afterSend.userCount===1)break;await sleep(250)} if(out.afterSend.userCount!==1) throw Error('SEND_CONFIRM_FAILED'); out.steps.push('CONTINUE_ONCE');
  for(let i=0;i<480;i++){out.answer=await state();if(out.answer.ackCount>=1&&!out.answer.stop)break;await sleep(250)} if(out.answer.ackCount<1||out.answer.stop) throw Error('ACK_TIMEOUT'); out.steps.push('ANSWER_EXTRACTED');
  out.finalState=await state(); if(out.finalState.userCount!==1) throw Error('DUPLICATE_OR_MISSING_SEND'); out.steps.push('EXACTLY_ONCE_CONFIRMED');
  await setCfg({operation:'set',target:'Impossible'}); out.invalid=await ctrl(p); if(out.invalid.changed) throw Error('INVALID_TARGET_CHANGED_UI'); out.steps.push('FAIL_CLOSED'); out.result='PASS';
 }catch(e){out.result='FAIL';out.error=String(e&&e.stack||e);}
 finally{if(p&&originalSetting){try{await setCfg({operation:'set',target:originalSetting});out.restoreAttempt=await ctrl(p);if(out.restoreAttempt.actual===originalSetting)out.steps.push('RESTORED_ORIGINAL');}catch(e){out.restoreError=String(e&&e.message||e);}} out.completedAt=new Date().toISOString();}
 console.log(JSON.stringify(out,null,2)); process.exitCode=out.result==='PASS'&&out.restoreAttempt?.actual===originalSetting?0:2;
})().catch(e=>{console.error(e);process.exit(3)});