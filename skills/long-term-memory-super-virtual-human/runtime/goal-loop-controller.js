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
