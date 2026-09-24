import fs from 'node:fs';
const [contractPath,ledgerPath,eventPath]=process.argv.slice(2);
if(!contractPath||!ledgerPath||!eventPath){console.error('用法: node validate-minimal-state-v4.7.4.mjs <合同.json> <账本.json> <事件.json>');process.exit(64);}
const c=JSON.parse(fs.readFileSync(contractPath,'utf8'));
const l=JSON.parse(fs.readFileSync(ledgerPath,'utf8'));
const e=JSON.parse(fs.readFileSync(eventPath,'utf8'));
const errors=[]; const fail=x=>errors.push(x);
const parse=s=>{const m=/^(\d{2})-(\d{2})$/.exec(s||'');return m?{g:Number(m[1]),a:Number(m[2])}:null;};
const from=e.FROM_STATE==='INIT'?{init:true}:parse(e.FROM_STATE);
const to=e.TO_STATE==='FINAL'?{final:true}:parse(e.TO_STATE);
if(e.ENGINE_VERSION!==c.method_version)fail('ENGINE_VERSION_MISMATCH');
if(e.TASK_TIME_ID!==l.task_time_id)fail('TASK_TIME_ID_MISMATCH');
if(Number(e.T_MATURE_STAR_MS)!==c.t_mature_star_ms)fail('T_MATURE_STAR_MISMATCH');
if(!from||!to)fail('INVALID_STATE');
if(to&&!to.final&&(to.a<1||to.a>c.state.max_attempt))fail('ATTEMPT_OUT_OF_RANGE');
if(from?.init){
 if(!(to.g===1&&to.a===1&&e.TO_PHASE==='VIRTUAL'))fail('INVALID_INITIAL_STATE');
}else if(e.FROM_PHASE==='VIRTUAL'){
 if(!(to.g===from.g&&to.a===from.a&&e.TO_PHASE==='REAL'))fail('INVALID_VIRTUAL_TO_REAL');
 if(!e.FREEZE_ID)fail('FREEZE_ID_MISSING');
 if((l.used_freeze_ids||[]).includes(e.FREEZE_ID))fail('FREEZE_ID_REUSE');
 if(!e.REAL_WORKDIR)fail('REAL_WORKDIR_MISSING');
 if(e.REAL_WORKDIR_PROVEN!=='YES')fail('REAL_WORKDIR_NOT_PROVEN');
 const wd=String(e.REAL_WORKDIR).replace(/\//g,'\\');
 if(/^C:\\Users\\[^\\]+\\?$/i.test(wd))fail('USER_HOME_WORKDIR_FORBIDDEN');
 if(e.PROCESS_SPAWN_PRECHECK!=='PASS')fail('PROCESS_SPAWN_PRECHECK_REQUIRED');
 if(Number(l.real_release_count_for_current_freeze||0)!==0)fail('SECOND_REAL_SAME_FREEZE');
 if(e.REAL_COMMAND_EMITTED!=='YES'&&e.REAL_DISPATCHED!=='AUTO')fail('REAL_COMMAND_NOT_EMITTED');
}else if(e.FROM_PHASE==='REAL'){
 if(e.VALID_REAL==='PASS'){
  if(!to.final)fail('REAL_PASS_MUST_FINAL');
 }else if(e.VALID_REAL==='FAIL'){
  if(to.final)fail('REAL_FAIL_CANNOT_FINAL');
  const structural=e.STRUCTURAL_REASSEMBLY==='YES';
  if(from.a>=6||structural){
   if(!(to.g===from.g+1&&to.a===1&&e.TO_PHASE==='VIRTUAL'))fail('NEW_GENERATION_REQUIRED');
   if(e.PLAN_REASSEMBLY!=='YES')fail('PLAN_REASSEMBLY_REQUIRED');
  }else{
   if(!(to.g===from.g&&to.a===from.a+1&&e.TO_PHASE==='VIRTUAL'))fail('NEXT_ATTEMPT_REQUIRED');
  }
  if(!e.NEW_FREEZE_ID)fail('NEW_FREEZE_ID_REQUIRED');
  if(e.NEW_FREEZE_ID===e.FREEZE_ID)fail('FREEZE_ID_REUSE_AFTER_FAIL');
 }else fail('VALID_REAL_REQUIRED');
}
console.log(JSON.stringify({VALID:errors.length===0,执行动作:errors.length?'阻断':'允许',errors},null,2));
process.exit(errors.length?2:0);
