# ChatGPT Session Continuity Controller v0.2

## Purpose

Use an external supervisor for ChatGPT page continuity. The supervisor must not depend on the current ChatGPT turn being healthy.

## Two failure classes

### Session or page failure

Use the existing Playwright Native AI Browser to observe the current task marker, answer state, page errors, and last progress time.

If the task-specific silence window is exceeded:
1. perform a read-only query;
2. perform the existing browser recovery path;
3. query again;
4. if still stalled, save checkpoint and handoff;
5. open a fresh ChatGPT conversation;
6. continue exactly once using the existing validated browser business entrypoint.

### Service-level failure

If fresh ChatGPT conversations are also unavailable:
1. freeze the primary state writer;
2. load the latest TASK_CONTRACT and checkpoint;
3. hand off to an independent Reasonix/DeepSeek backup route;
4. continue toward the same FINAL_VALID;
5. when GPT returns, reconcile through the latest handoff before resuming writes.

## Timing

Do not use one global timeout. Each task contract records:
- expected_silence_window
- hard_deadline
- current_stage
- last_evidence
- current_turn_id

## Proactive session rotation

Default policy is **high-frequency preventive rotation, conservative post-disconnect failover**.

Do not wait until a long page is already unstable before starting the next large stage. At a durable safe checkpoint, prefer moving a large/complex next problem to a fresh conversation even if the old page still appears usable. For very large independent problems, one large problem per conversation is a valid default.

However, `连接已断开` / reconnecting is **not by itself proof that backend generation stopped**. A transport/UI disconnect can coexist with continued backend work and a later final answer. Therefore never immediately duplicate the task into a new page merely because the banner appears.

Rotation is allowed only at a safe checkpoint, never in the middle of an uncertain non-idempotent action.

Priority rules:
1. **Preventive trigger**: before a large/high-thinking next stage, if the current conversation already contains substantial prior work, rotate early.
2. **Growth trigger**: cumulative visible conversation text or turn count has grown materially since the last checkpoint; rotate before another large answer.
3. **History trigger**: the page has already suffered one transient disconnect/stall; use the next safe checkpoint for early rotation.
4. **Disconnect during an active turn**: first classify it as transport degraded, not task failed. Read-only probe and observe backend/final-answer evidence within the task-specific deadline.
5. **Confirmed stall trigger**: only after no backend progress/final answer is observed and the recovery/deadline gate is exceeded may the controller checkpoint, fence if needed, and open a fresh session exactly once.

The handoff payload stays minimal:
```text
TASK_CONTRACT
+ latest accepted conclusion
+ current checkpoint
+ unresolved items
+ next exact instruction
+ unique task/turn marker
```

Do not replay the entire old conversation. The objective is to trade a small re-read cost for lower disconnect/stall risk and shorter wasted wait time.

The controller records:
- conversation_age_turns
- visible_text_size
- last_rotation_at
- prior_disconnect_count
- next_stage_complexity
- rotation_reason

Default policy is intentionally biased toward **earlier rotation for complex work**. Thresholds are tuning parameters and must be calibrated from real T_VALID/failure evidence; they are not treated as universal constants.

## Split-brain prevention

For long tasks, reuse ECC v3.1.1 lease/fencing concepts so only the current lease holder updates authoritative task state.

## Mature assets reused

- Playwright Native AI Browser: ChatGPT query/send/wait_extract and page recovery
- ECC v3.1.1: checkpoint, handoff, lease/fencing
- Reasonix Recovery Kit: context fallback, repair and runtime health checks

Current status:

```ini
SESSION_CONTINUITY_CONTROLLER=VIRTUAL_MATURE
PROACTIVE_SESSION_ROTATION=VIRTUAL_MATURE_REALITY_OPEN
PAGE_FAILOVER_E2E=NO
SERVICE_FAILOVER_BACKUP_BRAIN=PASS
```

## Reality / Virtual-Maturity Closure 2026-10-02
- `runtime/session-continuity-supervisor.js` added as a thin external decision layer; it does not duplicate ECC checkpoint/lease/fencing or Playwright send/query/recovery.
- Deterministic supervisor tests: 9 PASS / 0 FAIL, covering CONTINUE, read-only probe, safe rotation, service failover, unsafe-checkpoint hold, backup writer ownership, and primary-recovery reconcile.
- ECC v3.1.1 direct tests: lease 30 PASS, takeover 8 PASS, fault injection 21 PASS; total 59 PASS / 0 FAIL.
- Independent backup-brain Reality: Reasonix v1.38.6 using OpenRouter/DeepSeek-V4.1-Flash returned `LTMVH-BACKUP-BRAIN-ACK` in 8045 ms without GPT.
- Remaining Reality gap: actual stalled ChatGPT page → fresh authenticated ChatGPT conversation → exactly-once continue is not certified because the shared-mcp profile entered a Cloudflare challenge during the model/effort run.
- Therefore controller is virtually mature, service-level backup route is Reality-proven, but page-failover E2E remains OPEN.

## Human verification / CAPTCHA gate

If the dedicated ChatGPT browser presents `Verify you are human` / CAPTCHA / account-security verification:
- treat it as `HUMAN_VERIFICATION_REQUIRED`, not as a model/controller failure;
- pause automation at the current checkpoint;
- do not try to bypass or repeatedly brute-force the challenge;
- after the user completes the required verification, re-read the page state and continue from the same task marker.

A challenge can appear even when the persistent profile was previously authenticated. Existing login state reduces login work but does not guarantee that anti-bot verification will never be requested.

## Valid-first failover

`T*=min(T_VALID)` means time is optimized **inside the set of routes that can actually reach VALID**. A route that is blocked, permission-denied, repeatedly unverifiable, or unable to satisfy DONE_WHEN is removed from the current VALID candidate set.

Therefore:
```text
fast primary path succeeds
→ keep it

fast primary path cannot reach VALID
→ do not wait indefinitely
→ switch to the next mature VALID-capable route
→ finish the task
→ optimize or retest the faster path later
```

This applies across Codex / Reasonix / GPT / browser / runner routes. A slower successful mature route is preferable to an indefinitely stalled faster route because only completed valid results participate in `T_VALID`.
