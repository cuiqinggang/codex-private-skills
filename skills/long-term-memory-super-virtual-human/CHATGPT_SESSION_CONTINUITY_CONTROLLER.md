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

## Proactive session rotation

Do not wait for `连接已断开` / hard stall when the page is already becoming a high-risk long-flow context. Prefer a shorter fresh conversation at a durable checkpoint.

Rotation is allowed only at a safe checkpoint, never in the middle of an uncertain non-idempotent action.

Priority triggers:
1. **Hard trigger**: page reports connection lost/reconnecting or the current turn exceeds its task-specific silence window after a read-only probe.
2. **Preventive trigger**: a complex/high-thinking stage is about to start and the current conversation already carries substantial prior work.
3. **Growth trigger**: cumulative visible conversation text or turn count has grown materially since the last checkpoint; rotate before starting another large answer.
4. **History trigger**: the page has already suffered one transient disconnect/stall in the current task; use the next safe checkpoint to rotate rather than continue loading the same page.

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
SESSION_CONTINUITY_CONTROLLER=DESIGNED_FROM_MATURE_ASSETS
PROACTIVE_SESSION_ROTATION=DESIGNED_NOT_E2E_CERTIFIED
PAGE_FAILOVER_E2E=NO
SERVICE_FAILOVER_E2E=NO
```
