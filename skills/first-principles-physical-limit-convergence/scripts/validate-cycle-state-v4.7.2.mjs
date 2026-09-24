import fs from 'node:fs';

const [contractPath, ledgerPath, eventPath] = process.argv.slice(2);
if (!contractPath || !ledgerPath || !eventPath) {
  console.error('用法: node validate-cycle-state-v4.7.2.mjs <合同.json> <账本.json> <事件.json>');
  process.exit(64);
}
const c=JSON.parse(fs.readFileSync(contractPath,'utf8'));
const l=JSON.parse(fs.readFileSync(ledgerPath,'utf8'));
const e=JSON.parse(fs.readFileSync(eventPath,'utf8'));
const errors=[];
const fail=(x)=>errors.push(x);
const parse=(s)=>{
  const m=/^G(\d+)-A(\d+)-([VR])$/.exec(s||'');
  return m?{g:Number(m[1]),a:Number(m[2]),p:m[3]}:null;
};
const from=e.FROM_STATE_CODE==='INIT'?{g:0,a:0,p:'I'}:parse(e.FROM_STATE_CODE);
const to=e.TO_STATE_CODE==='FINAL'?{g:-1,a:-1,p:'F'}:parse(e.TO_STATE_CODE);

if(e.ENGINE_VERSION!==c.method_version) fail('ENGINE_VERSION_MISMATCH');
if(e.TASK_TIME_ID!==l.task_time_id) fail('TASK_TIME_ID_MISMATCH');
if(!from||!to) fail('INVALID_STATE_CODE');

for(const k of c.time_anchor.required_fields){
  if(e[k]===undefined||e[k]===null||e[k]==='') fail('MISSING_TIME_ANCHOR:'+k);
}
if(Number.isFinite(Number(e.T_MATURE_STAR_MS)) && Math.abs(Number(e.T_MATURE_STAR_MS)-c.time_anchor.t_mature_star_ms)>0.001) fail('T_MATURE_STAR_MISMATCH');
if(Number.isFinite(Number(e.T_CLOSED_REAL_NOW_MS)) && Number.isFinite(Number(e.TIME_GAP_MS))){
  const expected=Number(e.T_CLOSED_REAL_NOW_MS)-c.time_anchor.t_mature_star_ms;
  if(Math.abs(expected-Number(e.TIME_GAP_MS))>1) fail('TIME_ARITHMETIC_MISMATCH');
  const state=expected<=0?'WITHIN_TARGET':'OVER_TARGET';
  if(e.TIME_STATE!==state) fail('TIME_STATE_MISMATCH');
}
if(e.T_CLOSED_REAL_START_TIMESTAMP!==l.t_closed_real_start) fail('T_CLOSED_REAL_START_MISMATCH');

if(to && to.p!=='F' && (to.a<1 || to.a>c.max_attempts_per_generation)) fail('ATTEMPT_OUT_OF_RANGE');

if(from?.p==='I'){
  if(!(to.g===1&&to.a===1&&to.p==='V')) fail('ILLEGAL_INITIAL_TRANSITION');
} else if(from?.p==='V'){
  if(!(to.g===from.g&&to.a===from.a&&to.p==='R')) fail('ILLEGAL_VIRTUAL_TO_REAL_TRANSITION');
  if(e.VIRTUAL_COMPLETE!=='YES') fail('VIRTUAL_NOT_COMPLETE');
  if(e.TIME_LEDGER_READY!=='PASS') fail('TIME_LEDGER_NOT_READY');
  if(!e.FREEZE_ID) fail('FREEZE_ID_MISSING');
  if((l.used_freeze_ids||[]).includes(e.FREEZE_ID)) fail('FREEZE_ID_REUSE');
  if(Number(e.REAL_RELEASE_COUNT_FOR_FREEZE)!==1 || Number(l.real_release_count_for_current_freeze||0)!==0) fail('SECOND_REAL_SAME_FREEZE');
  if(e.REAL_COMMAND_EMITTED!=='YES' && e.REAL_DISPATCHED!=='AUTO') fail('VIRTUAL_COMPLETE_WITHOUT_REAL_COMMAND');
  if(e.REAL_NO_REDESIGN!=='YES') fail('REAL_NO_REDESIGN_REQUIRED');
} else if(from?.p==='R'){
  if(e.VALID_REAL==='PASS'){
    if(e.TO_STATE_CODE!=='FINAL') fail('REAL_PASS_MUST_FINAL');
    if(e.GPT_FINAL_VALID!=='YES') fail('GPT_FINAL_VALID_REQUIRED');
    if(e.TIME_ACCOUNTING_COMPLETE!=='PASS') fail('FINAL_WITHOUT_TIME_ACCOUNTING_COMPLETE');
  } else if(e.VALID_REAL==='FAIL'){
    if(e.TO_STATE_CODE==='FINAL') fail('FINAL_WITH_REAL_FAIL');
    if(to.p!=='V') fail('REAL_FAIL_MUST_RETURN_VIRTUAL');
    const structural=e.STRUCTURAL_REASSEMBLY==='YES';
    if(from.a>=c.max_attempts_per_generation || structural){
      if(!(to.g===from.g+1&&to.a===1)) fail('ATTEMPT_LIMIT_REQUIRES_NEW_GENERATION');
      if(e.PLAN_REASSEMBLY!=='YES') fail('PLAN_REASSEMBLY_REQUIRED');
    } else {
      if(!(to.g===from.g&&to.a===from.a+1)) fail('FAIL_RETRY_SEQUENCE_MISMATCH');
      if(e.PLAN_REASSEMBLY==='YES') fail('UNEXPECTED_REASSEMBLY_FLAG');
    }
    if(e.NEW_FREEZE_REQUIRED!=='YES') fail('NEW_FREEZE_REQUIRED');
  } else fail('VALID_REAL_REQUIRED');
}

if(to?.p!=='F' && to.a>=7) fail('ATTEMPT_7_OR_HIGHER');

console.log(JSON.stringify({
  VALID:errors.length===0,
  执行动作:errors.length===0?'允许':'阻断',
  errors
},null,2));
process.exit(errors.length?2:0);
