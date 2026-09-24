import fs from 'node:fs';

const [contractPath, ledgerPath, eventPath] = process.argv.slice(2);
if (!contractPath || !ledgerPath || !eventPath) {
  console.error('USAGE: node validate-state-transition-v4.7.2.mjs <contract.json> <ledger.json> <event.json>');
  process.exit(64);
}

const contract = JSON.parse(fs.readFileSync(contractPath, 'utf8'));
const ledger = JSON.parse(fs.readFileSync(ledgerPath, 'utf8'));
const event = JSON.parse(fs.readFileSync(eventPath, 'utf8'));

const errors = [];
const fail = (code, detail='') => errors.push(detail ? code + ':' + detail : code);
const stateMap = new Map(contract.states.map(s => [s.id, s]));
const allowed = new Set(contract.allowed_transitions.map(([a,b]) => a + '->' + b));

if (event.ENGINE_VERSION !== contract.method_version) fail('ENGINE_VERSION_MISMATCH');
if (event.TASK_TIME_ID !== ledger.task_time_id) fail('TASK_TIME_ID_MISMATCH');
if (event.CYCLE_ID !== ledger.cycle_id) fail('CYCLE_ID_MISMATCH');
if (event.FROM_STATE !== ledger.state_id) fail('FROM_STATE_MISMATCH');
if (event.STATE_ID !== event.TO_STATE) fail('STATE_ID_TO_STATE_MISMATCH');
if (!allowed.has(event.FROM_STATE + '->' + event.TO_STATE)) fail('ILLEGAL_TRANSITION');

for (const key of contract.universal_required_fields) {
  if (event[key] === undefined || event[key] === null || event[key] === '') fail('MISSING_UNIVERSAL_FIELD', key);
}

const target = stateMap.get(event.TO_STATE);
if (!target) fail('UNKNOWN_TARGET_STATE');
else if (event.PHASE !== target.phase) fail('PHASE_STATE_MISMATCH');

if (event.TIME_CORE_VISIBLE !== 'PASS') fail('TIME_CORE_NOT_VISIBLE');
const allowedNext = contract.next_state_rules[event.TO_STATE] || [];
if (!allowedNext.includes(event.NEXT_STATE)) fail('NEXT_STATE_MISMATCH');
if (event.T_CLOSED_REAL_START !== ledger.t_closed_real_start) fail('T_CLOSED_REAL_START_MISMATCH');

for (const key of (contract.state_requirements[event.TO_STATE] || [])) {
  if (event[key] === undefined || event[key] === null || event[key] === '') fail('MISSING_STATE_FIELD', key);
}

if (event.TO_STATE === 'E60') {
  const expected = String(Number(ledger.last_valid_sequence || 0) + 1).padStart(2,'0');
  if (String(event.NEXT_SEQUENCE).padStart(2,'0') !== expected) fail('SEQUENCE_EXPECTED_NEXT_MISMATCH');
  if (event.REAL_COMMAND_EMITTED !== 'YES' && event.REAL_DISPATCHED !== 'AUTO') fail('VIRTUAL_COMPLETE_WITHOUT_REAL_COMMAND');
}

if (event.TO_STATE === 'E70') {
  if (!ledger.current_freeze_id || event.FREEZE_ID !== ledger.current_freeze_id) fail('FREEZE_ID_MISMATCH');
  if (Number(ledger.real_release_count_for_current_freeze) !== 0) fail('REAL_RELEASE_ALREADY_USED');
  if (Number(event.REAL_RELEASE_COUNT) !== 1) fail('REAL_RELEASE_COUNT_INVALID');
  if (event.REAL_NO_REDESIGN !== 'YES') fail('REAL_NO_REDESIGN_REQUIRED');
}

if (event.FROM_STATE === 'E80' && event.TO_STATE === 'E20') {
  if (ledger.last_real_result !== 'FAIL') fail('FAIL_LOOP_REQUIRES_REAL_FAIL');
  if (event.CYCLE_ID !== ledger.next_cycle_id) fail('CYCLE_INCREMENT_REQUIRED');
  if (event.NEW_FREEZE_REQUIRED !== 'YES') fail('NEW_FREEZE_REQUIRED');
}

if (event.TO_STATE === 'E90') {
  if (ledger.last_real_result !== 'PASS') fail('FINAL_WITHOUT_VALID_REAL_PASS');
  if (event.GPT_FINAL_VALID !== 'YES') fail('GPT_FINAL_VALID_REQUIRED');
  if (event.TIME_ACCOUNTING_COMPLETE !== 'PASS') fail('FINAL_WITHOUT_TIME_ACCOUNTING_COMPLETE');
}

if (errors.length) {
  console.log(JSON.stringify({VALID:false, ACTION:'BLOCK', errors}, null, 2));
  process.exit(2);
}

console.log(JSON.stringify({VALID:true, ACTION:'ALLOW', transition:event.FROM_STATE + '->' + event.TO_STATE}, null, 2));
