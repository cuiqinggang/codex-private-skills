const { chromium }=require('C:/AI/Playwright-Native-AI-Browser/node_modules/playwright');
const fs=require('fs');
const ctrl=eval(fs.readFileSync('C:/Users/A/etal-recon/codex-private-skills/skills/long-term-memory-super-virtual-human/runtime/chatgpt-model-effort-controller.js','utf8'));
const entry=eval(fs.readFileSync('C:/AI/Playwright-Native-AI-Browser/skills/playwright-native-ai-browser/scripts/chatgpt-business-entry.js','utf8'));
(async()=>{
 const marker='LTMVH-MODEL-EFFORT-E2E-20261002-02', ack=marker+'-ACK';
 const out={schemaVersion:1,marker,startedAt:new Date().toISOString(),steps:[]}; let ctx,p,originalSetting;
 const setCfg=async v=>p.evaluate(v=>sessionStorage.setItem('__ltmvh_model_effort_v1',JSON.stringify(v)),v);
 const biz=async v=>{await p.evaluate(v=>sessionStorage.setItem('__pw_native_business_task_v1',JSON.stringify(v)),v);return entry(p);};
 try{
  ctx=await chromium.launchPersistentContext('C:/AI/Playwright-Native-AI-Browser/profile/shared-mcp',{headless:false});
  p=ctx.pages()[0]||await ctx.newPage(); if(!p.url().startsWith('https://chatgpt.com/')) await p.goto('https://chatgpt.com/',{waitUntil:'domcontentloaded',timeout:30000});
  await p.locator('[contenteditable="true"][role="textbox"]:visible').last().waitFor({state:'visible',timeout:45000});
  await setCfg({operation:'read'}); out.original=await ctrl(p); originalSetting=out.original.actual; out.steps.push('READ_ORIGINAL');
  await setCfg({operation:'set',target:'High'}); out.toHigh=await ctrl(p); if(out.toHigh.actual!=='High') throw Error('HIGH_READBACK_FAILED'); out.steps.push('HIGH_READBACK');
  out.queryBefore=await biz({operation:'query',marker}); out.steps.push('QUERY_BEFORE');
  const prompt=marker+'\n这是自动化闭环认证。请仅回复：'+ack;
  out.send=await biz({operation:'send',marker,prompt,actionTimeoutMs:10000}); out.steps.push('CONTINUE_ONCE');
  out.answer=await biz({operation:'wait_extract',marker,answerMarker:ack,requiredText:[ack],answerTimeoutMs:240000,pollIntervalMs:500,sendRecord:out.send}); out.steps.push('ANSWER_EXTRACTED');
  out.queryAfter=await biz({operation:'query',marker,answerMarker:ack}); if(out.queryAfter.userCount!==1) throw Error('DUPLICATE_OR_MISSING_SEND'); out.steps.push('EXACTLY_ONCE_CONFIRMED');
  await setCfg({operation:'set',target:'Impossible'}); out.invalid=await ctrl(p); if(out.invalid.changed) throw Error('INVALID_TARGET_CHANGED_UI'); out.steps.push('FAIL_CLOSED');
  out.result='PASS';
 }catch(e){out.result='FAIL';out.error=String(e&&e.stack||e);}
 finally{
  if(p&&originalSetting){try{await setCfg({operation:'set',target:originalSetting});out.restoreAttempt=await ctrl(p);if(out.restoreAttempt.actual===originalSetting)out.steps.push('RESTORED_ORIGINAL');}catch(e){out.restoreError=String(e&&e.message||e);}}
  try{if(ctx)await ctx.close();}catch{}
  out.completedAt=new Date().toISOString();
 }
 console.log(JSON.stringify(out,null,2)); process.exitCode=out.result==='PASS'&&out.restoreAttempt?.actual===originalSetting?0:2;
})();