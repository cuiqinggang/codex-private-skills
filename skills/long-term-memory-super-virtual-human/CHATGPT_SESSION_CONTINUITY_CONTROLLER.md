# ChatGPT Session Continuity Controller v0.1

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

## Split-brain prevention

For long tasks, reuse ECC v3.1.1 lease/fencing concepts so only the current lease holder updates authoritative task state.

## Mature assets reused

- Playwright Native AI Browser: ChatGPT query/send/wait_extract and page recovery
- ECC v3.1.1: checkpoint, handoff, lease/fencing
- Reasonix Recovery Kit: context fallback, repair and runtime health checks

Current status:

```ini
SESSION_CONTINUITY_CONTROLLER=DESIGNED_FROM_MATURE_ASSETS
PAGE_FAILOVER_E2E=NO
SERVICE_FAILOVER_E2E=NO
```
