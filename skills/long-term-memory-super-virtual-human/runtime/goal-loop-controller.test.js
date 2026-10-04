const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const {runGoal,digest}=require('./goal-loop-controller');
const contract={taskId:'fixture',goal:'produce verified result',doneWhen:['result=18'],
  boundaries:{allowed:['fixture only'],forbidden:['external effects']},maxRounds:6,maxRuntimeMs:10000};
function setup(t){const root=fs.mkdtempSync(path.join(os.tmpdir(),'goal-test-'));t.after(()=>fs.rmSync(root,{recursive:true,force:true}));return root;}
const fail=(progressKey='0',extra={})=>({passed:false,evidence:[],progressKey,...extra});
const pass=()=>({passed:true,evidence:[{check:'result equals 18'}],contractHash:digest(contract)});
test('failed first result is repaired, verified, and terminal task never executes again',async t=>{
 const root=setup(t);let value=0,calls=0;
 const adapter={verify:async()=>value===18?pass():fail(String(value)),execute:async()=>{calls++;value=calls===1?7:18;return {checkpoint:{value}};}};
 const args={contract,root,adapter,assertWriter:()=>{}};
 const s=await runGoal(args);assert.equal(s.status,'CLOSED');assert.equal(calls,2);
 await runGoal(args);assert.equal(calls,2);
});
test('crash after side effect reconciles original action without repeating it',async t=>{
 const root=setup(t);let effects=0,value=0;
 const adapter={verify:async()=>value===18?pass():fail(String(value)),execute:async()=>{effects++;value=7;throw new Error('crash after write');}};
 await assert.rejects(runGoal({contract,root,adapter,assertWriter:()=>{}}));
 adapter.reconcile=async()=>({status:'COMPLETED',checkpoint:{value}});
 adapter.execute=async()=>{effects++;value=18;};
 const s=await runGoal({contract,root,adapter,assertWriter:()=>{}});
 assert.equal(s.status,'CLOSED');assert.equal(effects,2);assert.equal(s.round,2);
});
test('uncertain side effect is blocked without reconciliation',async t=>{
 const root=setup(t);let calls=0;
 const adapter={verify:async()=>fail(),execute:async()=>{calls++;throw new Error('uncertain');}};
 await assert.rejects(runGoal({contract,root,adapter,assertWriter:()=>{}}));
 const s=await runGoal({contract,root,adapter,assertWriter:()=>{}});assert.equal(s.status,'BLOCKED');assert.equal(calls,1);
});
test('two completed rounds without progress halt',async t=>{
 let calls=0;const s=await runGoal({contract,root:setup(t),assertWriter:()=>{},adapter:{verify:async()=>fail(),execute:async()=>{calls++;}}});
 assert.equal(s.reason,'TWO_ROUNDS_NO_PROGRESS');assert.equal(calls,2);
});
test('same failure without a new strategy halts',async t=>{
 let calls=0;const s=await runGoal({contract,root:setup(t),assertWriter:()=>{},adapter:{verify:async()=>fail(String(calls),{failureKey:'same',strategyKey:'same'}),execute:async()=>{calls++;}}});
 assert.equal(s.reason,'SAME_FAILURE_WITHOUT_NEW_STRATEGY');assert.equal(calls,1);
});
test('model completion claim without evidence is rejected',async t=>{
 const s=await runGoal({contract,root:setup(t),assertWriter:()=>{},adapter:{verify:async()=>({...pass(),evidence:[]}),execute:async()=>assert.fail()}});
 assert.equal(s.status,'BLOCKED');
});
test('STOP is honored before execution',async t=>{
 const root=setup(t);fs.writeFileSync(path.join(root,'STOP'),'');
 const s=await runGoal({contract,root,assertWriter:()=>{},adapter:{verify:async()=>assert.fail(),execute:async()=>assert.fail()}});
 assert.equal(s.status,'STOPPED');
});
test('contract drift is rejected on resume',async t=>{
 const root=setup(t);const adapter={verify:async()=>pass(),execute:async()=>assert.fail()};
 await runGoal({contract,root,adapter,assertWriter:()=>{}});
 await assert.rejects(runGoal({contract:{...contract,goal:'different'},root,adapter,assertWriter:()=>{}}),/CONTRACT_CHANGED/);
});
test('loss of writer ownership prevents action',async t=>{
 let checks=0;await assert.rejects(runGoal({contract,root:setup(t),assertWriter:()=>{if(++checks>1)throw new Error('lease lost');},adapter:{verify:async()=>fail(),execute:async()=>assert.fail()}}),/lease lost/);
});
test('budget exhaustion does not announce completion',async t=>{
 let calls=0;const c={...contract,maxRounds:1};
 const s=await runGoal({contract:c,root:setup(t),assertWriter:()=>{},adapter:{verify:async()=>fail(String(calls)),execute:async()=>{calls++;}}});
 assert.equal(s.reason,'ROUND_BUDGET');assert.equal(calls,1);
});
test('transport recovery reuses action ID without consuming a business round',async t=>{
 const root=setup(t);let executions=0,recoveries=0,value=0;
 const adapter={verify:async()=>value===18?pass():fail(String(value)),
   execute:async({actionId})=>{assert.equal(actionId,'fixture:round:1');executions++;if(executions===1)throw new Error('page disconnected');value=18;},
   recover:async()=>{recoveries++;return {available:true};},
   reconcile:async()=>({status:'NOT_STARTED'})};
 const s=await runGoal({contract,root,adapter,assertWriter:()=>{}});
 assert.equal(s.status,'CLOSED');assert.equal(s.round,1);assert.equal(recoveries,1);assert.equal(executions,2);
});
test('human verification during recovery pauses instead of bypassing',async t=>{
 const adapter={verify:async()=>fail(),execute:async()=>{throw new Error('captcha');},
   recover:async()=>({humanRequired:true,reason:'HUMAN_VERIFICATION_REQUIRED'}),reconcile:async()=>({status:'UNKNOWN'})};
 const s=await runGoal({contract,root:setup(t),adapter,assertWriter:()=>{}});
 assert.equal(s.status,'HUMAN_REQUIRED');assert.ok(s.pending);
});
