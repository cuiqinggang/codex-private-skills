const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict'),{createHash}=require('node:crypto');
const proof=__dirname,lease='C:/AI/Playwright-Native-AI-Browser/ltmvh-chatgpt-lease';
const checks=[];
function record(folder,name){return JSON.parse(fs.readFileSync(path.join(lease,folder,name)));}
async function dispatch(mode,adapterName){
 const marker='LTMVH-V050-AUTO-20261004-'+mode+'-R2',adapterPath=path.join(proof,adapterName),sha=createHash('sha256').update(fs.readFileSync(adapterPath)).digest('hex');
 const contract={taskId:marker,goal:'actual artifact sum 18',doneWhen:['actual sum is 18'],boundaries:{allowed:['fixture writes'],forbidden:['network changes']},adapterSha256:sha,maxRounds:4,maxRuntimeMs:120000,mode};
 if(mode==='stop'){const root=path.join(lease,'goal-loops',marker+'-'+sha.slice(0,12));fs.mkdirSync(root,{recursive:true});fs.writeFileSync(path.join(root,'STOP'),'');}
 const name=marker+'.json',tmp=path.join(lease,'inbox',name+'.tmp');fs.writeFileSync(tmp,JSON.stringify({marker,goalLoop:{adapterPath,contract}}));fs.renameSync(tmp,path.join(lease,'inbox',name));
 for(let i=0;i<100;i++){for(const folder of ['done','failed'])if(fs.existsSync(path.join(lease,folder,name)))return {folder,body:record(folder,name),marker};
 await new Promise(r=>setTimeout(r,300));}throw Error('INBOX_TIMEOUT '+marker);
}
(async()=>{
 const normal=record('done','LTMVH-V050-INBOX-20261004-normal-first.json');
 assert.equal(normal.result.goalLoop.status,'CLOSED');
 const effects=fs.readFileSync(path.join(proof,'LTMVH-V050-INBOX-20261004-normal','effects.jsonl'),'utf8').trim().split('\n').map(JSON.parse);assert.deepEqual(effects.map(x=>x.sum),[7,18]);
 assert.equal(record('done','LTMVH-V050-INBOX-20261004-normal-duplicate.json').result.goalLoop.status,'CLOSED');
 checks.push({case:'actual_runtime_repair_and_duplicate',pass:true,effects});
 const recovered=record('done','LTMVH-V050-INBOX-20261004-recover-resume.json');assert.equal(recovered.result.goalLoop.status,'CLOSED');
 const recoveryEffects=fs.readFileSync(path.join(proof,'LTMVH-V050-INBOX-20261004-recover','effects.jsonl'),'utf8').trim().split('\n').map(JSON.parse);assert.equal(recoveryEffects.length,2);
 checks.push({case:'actual_runtime_exception_requeue_reconcile',pass:true,effects:recoveryEffects});
 const blocked=record('failed','LTMVH-V050-INBOX-20261004-blocked-first.json');assert.equal(blocked.result.goalLoop.status,'BLOCKED');checks.push({case:'actual_runtime_no_progress_halts',pass:true,reason:blocked.result.goalLoop.reason});
 const auto=await dispatch('recover','runtime-auto-adapter.js');assert.equal(auto.folder,'done');assert.equal(auto.body.result.goalLoop.status,'CLOSED');
 const journal=fs.readFileSync(path.join(proof,auto.marker,'effects.jsonl'),'utf8').trim().split('\n').map(JSON.parse);assert.equal(journal.length,2);checks.push({case:'actual_file_exception_automatic_recover_reconcile_same_dispatch',pass:true,effects:journal});
 const stopped=await dispatch('stop','runtime-file-adapter.js');assert.equal(stopped.folder,'failed');assert.equal(stopped.body.result.goalLoop.status,'STOPPED');assert.equal(fs.existsSync(path.join(proof,stopped.marker,'artifact.json')),false);checks.push({case:'actual_runtime_stop_signal',pass:true});
 const report={version:'0.5.0',timestamp:new Date().toISOString(),scope:'ACTUAL_UNIQUE_WINDOWS_RUNTIME_INBOX_FILES',checks,browserReality:'BLOCKED_CDP_9223_UNAVAILABLE',projectFinalValid:false};
 fs.writeFileSync(path.join(proof,'runtime-inbox-reality.json'),JSON.stringify(report,null,2));console.log(JSON.stringify(report));
})().catch(e=>{console.error(e.stack);process.exitCode=1});