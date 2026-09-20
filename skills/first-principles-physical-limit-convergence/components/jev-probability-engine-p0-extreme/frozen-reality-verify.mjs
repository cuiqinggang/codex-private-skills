import { performance } from 'node:perf_hooks';
import { promises as fs, createWriteStream } from 'node:fs';
import { once } from 'node:events';
import path from 'node:path';
import crypto from 'node:crypto';
import process from 'node:process';
import { validateInput } from './validate-input.mjs';

const MODEL='typesafe/jev-1.13';
const ORIGIN='https://openrouter.ai';
const API_PATH='/api/alpha/decisions';
const ACTIONS=['EXECUTE','HOLD','ROUTE','REJECT'];
const OUTCOMES=['SUCCESS','FAIL_TEMP','FAIL_PERM'];
const TIMEOUT_MS=30000;
const WARMUPS=3;
const RUNS=30;
const BASELINE_MS=840.6046999999962;

const here=path.dirname(new URL(import.meta.url).pathname.replace(/^\/(?:[A-Za-z]:)/,m=>m.slice(1)));
const fixtureRoot=path.resolve(process.env.PE_P0_FIXTURE_ROOT?.trim() || here);
const publicFixture=path.join(fixtureRoot,'fixtures','public','pe-p0-general-01.input.json');
const oracleFile=path.join(fixtureRoot,'fixtures','private','pe-p0-general-01.oracle.json');
const outcomesFile=path.join(fixtureRoot,'fixtures','private','executor-outcomes.json');
const resultsRoot=path.join(fixtureRoot,'reality-test','results-v316-frozen');

const apiKey=process.env.OPENROUTER_API_KEY?.trim();
if(!apiKey){ console.error('OPENROUTER_API_KEY_MISSING'); process.exit(2); }

const oracle=JSON.parse(await fs.readFile(oracleFile,'utf8'));
const executorOutcomes=JSON.parse(await fs.readFile(outcomesFile,'utf8')).outcomes;
const oracleById=new Map(oracle.items.map(x=>[x.item_id,x]));

const { Pool } = await import('undici');
const pool=new Pool(ORIGIN,{connections:2,pipelining:1,keepAliveTimeout:60000,keepAliveMaxTimeout:60000});

const sha=v=>crypto.createHash('sha256').update(typeof v==='string'?v:JSON.stringify(v)).digest('hex');
const compact=x=>JSON.stringify(x);
const qCurrent=id=>({type:'choice',instructions:`Choose the permitted action for \`items.${id}\` now.`,criteria:Object.fromEntries(ACTIONS.map(a=>[a,`\`actions.${a}\``]))});
const qBranch=(id,result)=>({type:'choice',instructions:`If \`dependency.result\` is ${result}, choose the permitted action for \`items.${id}\`.`,criteria:Object.fromEntries(ACTIONS.map(a=>[a,`\`actions.${a}\``]))});

function buildUnits(input){
  const byId=new Map(input.items.map(x=>[x.item_id,x]));
  const units=[];
  for(let n=1;n<=16;n++){
    const id=String(n).padStart(2,'0');
    units.push({id:`u${id}`,itemIds:[id],questions:{[`item_${id}__current_action`]:qCurrent(id)}});
  }
  for(let n=17;n<=20;n++){
    const pred=String(n).padStart(2,'0');
    const dep=String(n+4).padStart(2,'0');
    const qs={[`item_${pred}__current_action`]:qCurrent(pred)};
    for(const r of OUTCOMES) qs[`item_${dep}__if_${pred}_${r}`]=qBranch(dep,r);
    units.push({id:`b${pred}-${dep}`,itemIds:[pred,dep],questions:qs,pred,dep});
  }
  for(const u of units) for(const id of u.itemIds) if(!byId.has(id)) throw new Error(`UNIT_ITEM_MISSING_${id}`);
  return units;
}
function projectedState(input,units){
  const byId=new Map(input.items.map(x=>[x.item_id,x]));
  const ids=[...new Set(units.flatMap(u=>u.itemIds))].sort();
  return {
    actions:input.action_ontology,
    items:Object.fromEntries(ids.map(id=>{
      const x=byId.get(id);
      return [id,{request:x.request,evidence:x.evidence,constraints:x.constraints}];
    }))
  };
}
function shardBody(input,units){
  const questions=Object.assign({},...units.map(u=>u.questions));
  return {model:MODEL,state:projectedState(input,units),questions};
}
function unitWeight(input,u){ return Buffer.byteLength(compact(shardBody(input,[u]))); }
function packTwo(input,units){
  const sorted=[...units].sort((a,b)=>unitWeight(input,b)-unitWeight(input,a) || a.id.localeCompare(b.id));
  const shards=[{units:[],weight:0},{units:[],weight:0}];
  for(const u of sorted){
    const t=shards[0].weight<=shards[1].weight?shards[0]:shards[1];
    const w=unitWeight(input,u);
    t.units.push(u); t.weight+=w;
  }
  return shards.map((s,index)=>{
    const body=shardBody(input,s.units);
    return {index,units:s.units,body,payload_bytes:Buffer.byteLength(compact(body))};
  });
}
function parseChoice(answer){
  if(!answer || answer.type!=='choice') throw new Error('CHOICE_SCHEMA_TYPE');
  if(typeof answer.choice!=='string' || !ACTIONS.includes(answer.choice)) throw new Error('CHOICE_SCHEMA_VALUE');
  return answer.choice;
}
async function requestDecision(body){
  const started=performance.now();
  const ac=new AbortController();
  const timer=setTimeout(()=>ac.abort(new Error('OPENROUTER_TIMEOUT')),TIMEOUT_MS);
  try{
    const r=await pool.request({
      path:API_PATH,method:'POST',signal:ac.signal,
      headers:{
        authorization:`Bearer ${apiKey}`,
        'content-type':'application/json',
        'x-openrouter-title':'JEV Probability Engine P0 v3.1.6 Frozen Verify'
      },
      body:compact(body)
    });
    const raw=await r.body.text();
    if(r.statusCode<200||r.statusCode>=300) throw new Error(`OPENROUTER_HTTP_${r.statusCode}:${raw.slice(0,300)}`);
    const json=JSON.parse(raw);
    if(!json.answers || typeof json.answers!=='object') throw new Error('ANSWERS_MISSING');
    const returned=String(json.model??'');
    if(!returned.startsWith('typesafe/jev-1.13')) throw new Error(`MODEL_FAMILY_DRIFT:${returned}`);
    return {answers:json.answers,model:returned,latency_ms:performance.now()-started};
  }finally{ clearTimeout(timer); }
}
async function authProbe(){
  const body={model:MODEL,state:{probe:'schema'},questions:{probe:{type:'choice',instructions:'Choose EXECUTE.',criteria:{EXECUTE:'correct',HOLD:'wrong',ROUTE:'wrong',REJECT:'wrong'}}}};
  const r=await requestDecision(body);
  if(parseChoice(r.answers.probe)!=='EXECUTE') throw new Error('AUTH_PROBE_DECISION');
}
function finalState(action,result){
  if(action==='HOLD') return 'ON_HOLD';
  if(action==='ROUTE') return 'ROUTED';
  if(action==='REJECT') return 'REJECTED';
  if(action==='EXECUTE'){
    if(result==='SUCCESS') return 'DONE';
    if(result==='FAIL_TEMP') return 'FAILED_RETRYABLE';
    return 'FAILED_FINAL';
  }
  throw new Error('BAD_ACTION');
}
function makeVerifier(){
  const seen=new Set(); const errors=[]; const receipts=[];
  function ingest(r){
    if(seen.has(r.item_id)) errors.push(`${r.item_id}:DUPLICATE`);
    seen.add(r.item_id); receipts.push(r);
    const exp=oracleById.get(r.item_id);
    if(!exp){ errors.push(`${r.item_id}:NO_ORACLE`); return; }
    if(r.action!==exp.expected_action) errors.push(`${r.item_id}:ACTION:${r.action}!=${exp.expected_action}`);
    if(r.executor_result!==exp.expected_executor_result) errors.push(`${r.item_id}:EXECUTOR`);
    if(r.final_state!==exp.expected_final_state) errors.push(`${r.item_id}:STATE`);
  }
  function finish(){
    if(seen.size!==24) errors.push('RECEIPT_CARDINALITY');
    const by=new Map(receipts.map(x=>[x.item_id,x]));
    for(const [dep,pred] of Object.entries(oracle.dependency_order)){
      const d=by.get(dep),p=by.get(pred);
      if(!d||!p) continue;
      if(d.start_ms<p.receipt_ms) errors.push(`${dep}:DEPENDENCY_ORDER`);
      if(d.dependency_receipt_item_id!==pred) errors.push(`${dep}:DEPENDENCY_RECEIPT`);
    }
    return {pass:errors.length===0,errors,receipts};
  }
  return {ingest,finish};
}
async function executeOne(log,item,action,depReceipt,verifier){
  const start=performance.now();
  const executor_result=action==='EXECUTE'?(executorOutcomes[item.item_id]??'FAIL_PERM'):null;
  const r={
    item_id:item.item_id,action,executor_result,
    final_state:finalState(action,executor_result),
    dependency_receipt_item_id:depReceipt?.item_id??null,
    start_ms:start,receipt_ms:performance.now()
  };
  verifier.ingest(r);
  if(!log.write(JSON.stringify(r)+'\n')) await once(log,'drain');
  return r;
}
async function processShard(input,shard,runDir,verifier){
  const api=await requestDecision(shard.body);
  const units=shard.units;
  const byId=new Map(input.items.map(x=>[x.item_id,x]));
  const tasks=units.map(async u=>{
    if(u.pred){
      const predChoice=parseChoice(api.answers[`item_${u.pred}__current_action`]);
      const predReceipt=await executeOne(verifier.log,byId.get(u.pred),predChoice,null,verifier);
      const branch=predReceipt.executor_result??'FAIL_PERM';
      const qid=`item_${u.dep}__if_${u.pred}_${branch}`;
      const depChoice=parseChoice(api.answers[qid]);
      return executeOne(verifier.log,byId.get(u.dep),depChoice,predReceipt,verifier);
    }
    const id=u.itemIds[0];
    const choice=parseChoice(api.answers[`item_${id}__current_action`]);
    return executeOne(verifier.log,byId.get(id),choice,null,verifier);
  });
  await Promise.all(tasks);
  return {latency_ms:api.latency_ms,model:api.model,payload_bytes:shard.payload_bytes};
}
async function runOnce(label){
  const runDir=path.join(resultsRoot,'.active',label);
  await fs.rm(runDir,{recursive:true,force:true}); await fs.mkdir(runDir,{recursive:true});
  const logPath=path.join(runDir,'receipts.jsonl');
  const t0=performance.now();
  const input=JSON.parse(await fs.readFile(publicFixture,'utf8'));
  const valid=validateInput(input); if(!valid.ok) throw new Error(`INPUT_SCHEMA:${valid.errors.join(',')}`);
  const units=buildUnits(input); const shards=packTwo(input,units);
  if(shards.length!==2) throw new Error('SHARD_COUNT');
  const qCount=shards.reduce((n,s)=>n+Object.keys(s.body.questions).length,0);
  if(qCount!==32) throw new Error(`QUESTION_COUNT_${qCount}`);
  for(const s of shards){
    for(const u of s.units){
      if(u.pred){
        for(const r of OUTCOMES) if(!s.body.questions[`item_${u.dep}__if_${u.pred}_${r}`]) throw new Error(`BUNDLE_SPLIT_${u.id}`);
      }
    }
  }
  const log=createWriteStream(logPath,{flags:'w'});
  const v=makeVerifier(); v.log=log;
  let api;
  try{ api=await Promise.all(shards.map(s=>processShard(input,s,runDir,v))); }
  finally{
    const closed=once(log,'close');
    log.end();
    await closed;
  }
  const fin=v.finish();
  const persisted=(await fs.readFile(logPath,'utf8')).trim().split(/\n/).filter(Boolean).map(JSON.parse);
  if(persisted.length!==24) fin.errors.push('PERSISTED_RECEIPT_CARDINALITY');
  const gate=fin.errors.length===0;
  const manifest={
    benchmark_id:input.benchmark_id,transport:'OPENROUTER_REAL',model_family:'typesafe/jev-1.13',
    commercial_gate:gate?'PASS':'FAIL',
    shard_count:2,payload_bytes:shards.map(s=>s.payload_bytes),
    input_sha256:sha(input),receipts_sha256:sha(persisted),verifier_errors:fin.errors
  };
  await fs.writeFile(path.join(runDir,'manifest.json'),JSON.stringify(manifest));
  const t1=performance.now();
  return {pass:gate,t_e2e_ms:t1-t0,api,payload_bytes:manifest.payload_bytes,errors:fin.errors};
}
function percentile(a,p){const s=[...a].sort((x,y)=>x-y);return s[Math.min(s.length-1,Math.max(0,Math.ceil(p*s.length)-1))];}
async function main(){
  await fs.mkdir(resultsRoot,{recursive:true});
  console.log('METHOD=first-principles-physical-limit-convergence v3.1.6');
  console.log('SOLUTION_FROZEN=YES');
  console.log('TOPOLOGY=s2-dependency-affinity-runtime-LPT');
  console.log(`BASELINE_MS=${BASELINE_MS}`);
  await Promise.all([authProbe(),authProbe()]);
  console.log('TRANSPORT_PREWARM=PASS CONNECTION_TARGET=2');
  for(let i=0;i<WARMUPS;i++){
    const r=await runOnce(`warm-${i+1}`);
    console.log(`WARM ${i+1}/${WARMUPS} PASS=${r.pass} T_E2E_MS=${r.t_e2e_ms.toFixed(3)} PAYLOAD=${r.payload_bytes.join('/')}`);
    if(!r.pass) throw new Error(`WARM_GATE_FAIL:${r.errors.join(',')}`);
  }
  const runs=[];
  for(let i=0;i<RUNS;i++){
    const r=await runOnce(`run-${i+1}`); runs.push(r);
    console.log(`RUN ${i+1}/${RUNS} PASS=${r.pass} T_E2E_MS=${r.t_e2e_ms.toFixed(3)} PAYLOAD=${r.payload_bytes.join('/')}`);
    if(!r.pass){ console.log('REALITY_DELTA=COMMERCIAL_GATE_FAIL'); process.exitCode=3; break; }
  }
  const allPass=runs.length===RUNS&&runs.every(r=>r.pass);
  const vals=runs.filter(r=>r.pass).map(r=>r.t_e2e_ms).sort((a,b)=>a-b);
  const min=vals[0]??null;
  const result={
    status:allPass&&min<BASELINE_MS?'PROMOTE':'REALITY_DELTA',
    baseline_ms:BASELINE_MS,measured_runs:runs.length,pass_runs:vals.length,
    min_ms:min,p50_ms:vals.length?percentile(vals,.50):null,p95_ms:vals.length?percentile(vals,.95):null,
    faster_than_baseline:allPass&&min<BASELINE_MS,
    REAL_CERTIFIED:allPass?'YES':'NO',
    next:allPass&&min<BASELINE_MS?'PROMOTE_NEW_BASELINE':'STOP_RETURN_TO_GPT'
  };
  await fs.writeFile(path.join(resultsRoot,'FROZEN-RESULT.json'),JSON.stringify(result,null,2));
  console.log(`COMMERCIAL_GATE_SERIES=${allPass?'PASS':'FAIL'}`);
  console.log(`FROZEN_MIN_MS=${min??'NA'}`);
  console.log(`BASELINE_BEAT=${result.faster_than_baseline?'YES':'NO'}`);
  console.log(`NEXT=${result.next}`);
  if(!result.faster_than_baseline) process.exitCode=4;
}
try{ await main(); } finally { await pool.close(); }
