param([string]$BridgeWorkDir,[string]$TaskFile)
$ErrorActionPreference='Stop'
New-Item -ItemType Directory -Path $BridgeWorkDir -Force | Out-Null
$controller=@'
'use strict';
// Thin goal-loop adapter. The existing continuity runtime owns scheduling/lease.
const fs = require('node:fs');
const path = require('node:path');
const {createHash} = require('node:crypto');
const digest = value => createHash('sha256').update(JSON.stringify(value)).digest('hex');
const terminals = new Set(['CLOSED', 'BLOCKED', 'HUMAN_REQUIRED', 'STOPPED']);
function atomic(file, value) {
  const tmp = file + '.tmp';
  fs.writeFileSync(tmp, JSON.stringify(value, null, 2));
  fs.renameSync(tmp, file);
}
async function runGoal({contract, root, adapter, assertWriter, shouldStop = () => false}) {
  if (!contract?.taskId || !contract.goal || !contract.doneWhen?.length ||
      !contract.boundaries || !Number.isInteger(contract.maxRounds) || contract.maxRounds < 1 ||
      !Number.isFinite(contract.maxRuntimeMs) || contract.maxRuntimeMs <= 0 ||
      !adapter || typeof adapter.execute !== 'function' || typeof adapter.verify !== 'function' ||
      typeof assertWriter !== 'function') throw new Error('GOAL_CONTRACT_OR_ADAPTER_INVALID');
  assertWriter();
  fs.mkdirSync(root, {recursive:true});
  const stateFile = path.join(root, 'STATE.json');
  const contractFile = path.join(root, 'LOOP-CONTRACT.json');
  const logFile = path.join(root, 'RUN-LOG.jsonl');
  const hash = digest(contract);
  let s;
  if (fs.existsSync(stateFile)) {
    s = JSON.parse(fs.readFileSync(stateFile, 'utf8'));
    if (s.contractHash !== hash) throw new Error('CONTRACT_CHANGED_REQUIRES_EXPLICIT_NEW_TASK');
  } else {
    s = {taskId:contract.taskId, contractHash:hash, status:'RUNNING', round:0,
    startedAt:Date.now(), noProgress:0, repeatedFailure:0, pending:null, evidence:[], checkpoint:null,
    recoveryAttempts:0};
    atomic(contractFile, contract);
    atomic(stateFile, s);
  }
  const save = event => {
    assertWriter();
    s.updatedAt = new Date().toISOString();
    atomic(stateFile, s);
    fs.appendFileSync(logFile, JSON.stringify({event, ...s}) + '\n');
  };
  const stop = (status, reason) => {s.status=status; s.reason=reason; save(status); return s;};
  if (terminals.has(s.status)) return s;
  for (;;) {
    assertWriter();
    if (shouldStop() || fs.existsSync(path.join(root, 'STOP'))) return stop('STOPPED', 'USER_STOP');
    if (Date.now() - s.startedAt >= contract.maxRuntimeMs) return stop('BLOCKED', 'TIME_BUDGET');
    let v;
    try {v = await adapter.verify({contract, state:structuredClone(s)});}
    catch (e) {return stop('BLOCKED', 'VERIFIER_ERROR:' + e.message);}
    assertWriter();
    if (shouldStop() || fs.existsSync(path.join(root, 'STOP'))) return stop('STOPPED', 'USER_STOP');
    if (Date.now() - s.startedAt >= contract.maxRuntimeMs) return stop('BLOCKED', 'TIME_BUDGET');
    if (!v || typeof v.passed !== 'boolean' || !Array.isArray(v.evidence)) return stop('BLOCKED', 'INVALID_VERIFIER_RESULT');
    s.evidence=v.evidence;
    if (v.humanRequired) return stop('HUMAN_REQUIRED', v.reason || 'USER_DECISION_REQUIRED');
    if (v.blocked) return stop('BLOCKED', v.reason || 'NO_AUTHORIZED_VALID_ROUTE');
    if (v.passed) {
      if (!v.evidence.length || v.contractHash !== hash) return stop('BLOCKED', 'PASS_WITHOUT_CONTRACT_BOUND_EVIDENCE');
      s.pending=null;
      return stop('CLOSED', 'DONE_WHEN_VERIFIED');
    }
    if (s.pending) {
      // A crash may have happened after an external side effect. Never blindly repeat.
      if (!adapter.reconcile) return stop('BLOCKED', 'UNCERTAIN_ACTION_REQUIRES_RECONCILIATION');
      const r = await adapter.reconcile({contract, state:structuredClone(s), actionId:s.pending});
      assertWriter();
      if (r?.status === 'COMPLETED') {
        s.checkpoint=r.checkpoint ?? s.checkpoint; s.pending=null; save('RECONCILED'); continue;
      }
      if (r?.status !== 'NOT_STARTED') return stop('BLOCKED', 'UNCERTAIN_ACTION_NOT_REPLAYED');
      // NOT_STARTED is adapter-proven safe to execute using the same stable action ID.
    } else {
      if (s.round >= contract.maxRounds) return stop('BLOCKED', 'ROUND_BUDGET');
      if (typeof v.progressKey !== 'string' || !v.progressKey) return stop('BLOCKED', 'MEASURABLE_PROGRESS_REQUIRED');
      s.noProgress = s.lastProgress === v.progressKey ? s.noProgress + 1 : 0;
      s.repeatedFailure = v.failureKey && s.lastFailure === v.failureKey && s.lastStrategy === v.strategyKey
        ? s.repeatedFailure + 1 : 0;
      s.lastProgress=v.progressKey; s.lastFailure=v.failureKey; s.lastStrategy=v.strategyKey;
      if (s.noProgress >= 2) return stop('BLOCKED', 'TWO_ROUNDS_NO_PROGRESS');
      if (s.repeatedFailure >= 1) return stop('BLOCKED', 'SAME_FAILURE_WITHOUT_NEW_STRATEGY');
      s.round++;
      s.recoveryAttempts=0;
      s.pending=contract.taskId + ':round:' + s.round;
      save('ACTION_INTENT');
    }
    if (shouldStop() || fs.existsSync(path.join(root, 'STOP'))) return stop('STOPPED', 'USER_STOP');
    try {
      assertWriter();
      const result = await adapter.execute({contract, state:structuredClone(s), actionId:s.pending,
        verification:v, shouldStop});
      assertWriter();
      s.checkpoint=result?.checkpoint ?? s.checkpoint;
      s.pending=null; save('ACTION_RETURNED_REVERIFY_REQUIRED');
    } catch (e) {
      // Keep the uncertain action ID for safe reconciliation on restart.
      s.lastError=String(e.message || e); save('ACTION_UNCERTAIN');
      if (shouldStop() || fs.existsSync(path.join(root, 'STOP'))) return stop('STOPPED', 'USER_STOP');
      if (adapter.recover && adapter.reconcile && s.recoveryAttempts < (contract.maxRecoveryAttempts ?? 2)) {
        s.recoveryAttempts++; save('RECOVERY_BEGIN');
        // Reuse the existing continuity/failover chain. Recovery never changes business goals.
        const recovered=await adapter.recover({contract,state:structuredClone(s),actionId:s.pending,
          error:s.lastError,shouldStop});
        assertWriter();
        if (recovered?.humanRequired) return stop('HUMAN_REQUIRED',recovered.reason || 'RECOVERY_HUMAN_REQUIRED');
        if (recovered?.available === true) {save('RECOVERY_READY_RECONCILE_REQUIRED');continue;}
        return stop('BLOCKED',recovered?.reason || 'RECOVERY_PATH_UNAVAILABLE');
      }
      throw e;
    }
  }
}
module.exports={runGoal, digest};

'@
$reality=@'
'use strict';
// Real filesystem/process fixture. No browser/model claims are made by this harness.
const fs=require('node:fs');
const os=require('node:os');
const path=require('node:path');
const {spawnSync}=require('node:child_process');
const assert=require('node:assert/strict');
const {runGoal,digest}=require('./goal-loop-controller');
const mode=process.argv[2];
const root=process.argv[3];
function contract(id){return {taskId:id,goal:'write result 18 and verify actual artifact',doneWhen:['artifact.result === 18'],
 boundaries:{allowed:['fixture directory writes'],forbidden:['external changes']},maxRounds:4,maxRuntimeMs:60000};}
async function worker(){
 const c=contract(path.basename(root));
 const output=path.join(root,'result.json'),journal=path.join(root,'effects.jsonl');
 const read=()=>fs.existsSync(output)?JSON.parse(fs.readFileSync(output,'utf8')):null;
 const adapter={
  verify:async()=>{const v=read();return {passed:v?.result===18,evidence:v?[{path:output,result:v.result}]:[],
   contractHash:digest(c),progressKey:String(v?.result??'missing')};},
  execute:async({actionId,state})=>{
   const result=state.round===1?7:18;
   fs.writeFileSync(output,JSON.stringify({actionId,result}));
   fs.appendFileSync(journal,JSON.stringify({actionId,result})+'\n');
   if(mode==='crash-worker'&&state.round===1) process.exit(73);
   return {checkpoint:{actionId,result}};
  },
  reconcile:async({actionId})=>read()?.actionId===actionId?{status:'COMPLETED',checkpoint:read()}:{status:'UNKNOWN'}
 };
 if(mode==='blocked-worker')adapter.execute=async()=>{fs.writeFileSync(output,JSON.stringify({result:7}));};
 const s=await runGoal({contract:c,root,adapter,assertWriter:()=>{}});
 fs.writeFileSync(path.join(root,'worker-result.json'),JSON.stringify(s));
}
if(mode?.endsWith('worker'))worker().catch(e=>{console.error(e.stack);process.exitCode=1;});
else {
 const dir=fs.mkdtempSync(path.join(os.tmpdir(),'ltmvh-reality-'));
 const started=Date.now();const checks=[];
 function run(workerMode,caseRoot,expected=0){const r=spawnSync(process.execPath,[__filename,workerMode,caseRoot],{encoding:'utf8',timeout:20000});assert.equal(r.status,expected,r.stderr);return r;}
 try{
  const normal=path.join(dir,'repair');fs.mkdirSync(normal);run('normal-worker',normal);
  const normalState=JSON.parse(fs.readFileSync(path.join(normal,'worker-result.json')));
  assert.equal(normalState.status,'CLOSED');assert.equal(normalState.round,2);
  const effectsBefore=fs.readFileSync(path.join(normal,'effects.jsonl'),'utf8');run('normal-worker',normal);
  assert.equal(fs.readFileSync(path.join(normal,'effects.jsonl'),'utf8'),effectsBefore);
  checks.push({name:'real_file_fail_repair_verified_stop_and_no_duplicate',pass:true,actualResults:[7,18],rounds:2});
  const resume=path.join(dir,'resume');fs.mkdirSync(resume);run('crash-worker',resume,73);
  const interrupted=JSON.parse(fs.readFileSync(path.join(resume,'STATE.json')));assert.ok(interrupted.pending);
  run('normal-worker',resume);
  const lines=fs.readFileSync(path.join(resume,'effects.jsonl'),'utf8').trim().split('\n').map(JSON.parse);
  assert.equal(lines.length,2);assert.equal(new Set(lines.map(x=>x.actionId)).size,2);
  assert.equal(JSON.parse(fs.readFileSync(path.join(resume,'STATE.json'))).status,'CLOSED');
  checks.push({name:'real_process_exit_73_restart_reconcile_original_side_effect',pass:true,effects:lines,pendingBeforeRestart:interrupted.pending});
  const blocked=path.join(dir,'blocked');fs.mkdirSync(blocked);run('blocked-worker',blocked);
  const b=JSON.parse(fs.readFileSync(path.join(blocked,'STATE.json')));assert.equal(b.status,'BLOCKED');
  checks.push({name:'actual_unchanged_artifact_blocks_without_false_completion',pass:true,status:b.status,reason:b.reason});
  const stopped=path.join(dir,'stop');fs.mkdirSync(stopped);fs.writeFileSync(path.join(stopped,'STOP'),'');run('normal-worker',stopped);
  assert.equal(JSON.parse(fs.readFileSync(path.join(stopped,'STATE.json'))).status,'STOPPED');assert.equal(fs.existsSync(path.join(stopped,'result.json')),false);
  checks.push({name:'actual_stop_file_prevents_execution',pass:true});
  const report={version:'0.5.0',timestamp:new Date().toISOString(),environment:{platform:process.platform,node:process.version},
   elapsedMs:Date.now()-started,scope:'LOCAL_REAL_PROCESSES_AND_FILES_ONLY',checks,
   browserReality:'NOT_RUN',windowsDeployment:'NOT_PERFORMED',projectFinalValid:false};
  console.log(JSON.stringify(report,null,2));
 }finally{fs.rmSync(dir,{recursive:true,force:true});}
}

'@
[IO.File]::WriteAllText((Join-Path $BridgeWorkDir 'goal-loop-controller.js'),$controller,[Text.UTF8Encoding]::new($false))
[IO.File]::WriteAllText((Join-Path $BridgeWorkDir 'goal-loop-reality.js'),$reality,[Text.UTF8Encoding]::new($false))
$node=(Get-Command node -ErrorAction Stop).Source
& $node (Join-Path $BridgeWorkDir 'goal-loop-reality.js')
if($LASTEXITCODE -ne 0){throw 'GOAL_LOOP_REAL_PROCESS_REALITY_FAILED'}
[ordered]@{marker='LTMVH-V050-BRIDGE-REALITY-20261004-R1'; route='GITHUB_SELF_HOSTED_RUNNER'; machine=[Environment]::MachineName; result=(7+11); time=(Get-Date).ToString('o')} | ConvertTo-Json
if((7+11) -ne 18){throw 'HEALTH_RESULT_MISMATCH'}
