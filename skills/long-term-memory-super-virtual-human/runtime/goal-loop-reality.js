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
