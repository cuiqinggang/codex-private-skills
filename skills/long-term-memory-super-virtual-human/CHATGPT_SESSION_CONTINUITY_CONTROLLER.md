# ChatGPT Session Continuity Controller v0.4.5

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
5. open a **true New chat** at the ChatGPT new-conversation root; never use “Branch in new chat” as the recovery target;
6. verify the destination is not a branch/continuation of the old conversation;
7. continue exactly once using the existing validated browser business entrypoint.

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

### True-new-chat rule

Recovery freshness is semantic, not cosmetic:

```ini
RECOVERY_SESSION_KIND=NEW_CHAT_ONLY
BRANCH_IN_NEW_CHAT=FORBIDDEN
OLD_CONVERSATION_REPLAY=FORBIDDEN
```

A branch may look like a new page while still inheriting the old conversation tree/context burden. It is therefore excluded from the recovery path. The controller must open the normal ChatGPT New chat surface/root, then send only the minimal handoff.

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


## v0.4.5 unified clean page lifecycle

v0.4.5 has one production controller only. Historical recovery/page-continuity methods are indexed in `LEGACY_CONTINUITY_INDEX.md` and must not run as a second supervisor. v0.4.5 additionally freezes the clean dedicated-browser lifecycle proven by R18/R19.

Default role thresholds are intentionally preventive tuning values, not universal limits:

```ini
CEO_VISIBLE_TEXT_LIMIT=40000
CEO_USER_TURN_LIMIT=10
EXECUTOR_VISIBLE_TEXT_LIMIT=30000
EXECUTOR_USER_TURN_LIMIT=3
POLL_INTERVAL_APPROX_MS=1200
WAIT_UNTIL_SLOW=NO
IDLE_CHAT_PAGE_TARGET=1
IDLE_CHAT_PAGE_KIND=BLANK_NEW_CHAT_ROOT
CLOSE_FINISHED_EXECUTOR_PAGE=YES
CLOSE_FINISHED_CEO_PAGE_AFTER_PERSIST=YES
PREWARM_UNUSED_CHAT_PAGES=NO
T_STAR_OBSERVED_MS=51454
T_STAR_REALITY=R18
T_STAR_CONFIRMATION_R19_MS=54246
```

The controller accepts multiple page-failure signals under the same decision path: growth, prior disconnect/stall history, explicit UI failure, missing/unusable composer, response pending with no progress, active-turn hard stall, and service-level failure. The rule is not “always rotate”: when a disconnect or active response still has backend progress, keep observing the original turn. Rotate only when a safe checkpoint exists, or when a replay-safe confirmed stall has been fenced/aborted.

Reality 2026-10-04 R1 proved a forced CEO rotation using the existing authenticated shared-mcp browser: true New chat, one submission, one marker, ACK confirmed, no Branch, no second browser launch, page lease retained.


## Clean dedicated-browser lifecycle v0.4.5

The dedicated ChatGPT browser is a runtime resource, not long-term memory. When no task is active, the production target is exactly one blank ChatGPT New chat root page.

```text
ONE_BLANK_NEW_CHAT_ROOT
→ reuse as CEO-1
→ CEO-1 decomposes / defines DONE_WHEN only
→ create only the minimum required executor pages
→ persist minimal checkpoint
→ close old CEO
→ create a true New chat CEO-2
→ CEO-2 takes over from checkpoint; never redo accepted child work
→ collect original executor results
→ close each executor immediately after its result is durably accepted
→ final validation + evidence persist
→ close final CEO
→ restore exactly ONE_BLANK_NEW_CHAT_ROOT
```

Hard rules:

```ini
CLEAN_BASELINE_REQUIRED=YES
REUSE_BASELINE_AS_CEO1=YES
EXECUTOR_PAGE_COUNT=MIN_REQUIRED_ONLY
UNUSED_PAGE_PREWARM=NO
EXECUTOR_CLOSE_AFTER_ACCEPTED_RESULT=YES
OLD_CEO_CLOSE_AFTER_CHECKPOINT=YES
CEO2_SESSION_KIND=TRUE_NEW_CHAT
BRANCH_AS_CEO2=FORBIDDEN
FULL_OLD_CONVERSATION_REPLAY=FORBIDDEN
FINAL_BROWSER_STATE=ONE_BLANK_NEW_CHAT_ROOT
```

Reality R18: 51,454 ms, all lifecycle assertions PASS, checkpoint length 125 chars, final ChatGPT page count 1.
Reality R19: 54,246 ms, same contract PASS. Current observed `T*=min(T_VALID)=51,454 ms` from R18.

Rejected as default after Reality comparison: unused executor prewarm, Instant control chain, same physical CEO tab reuse, and deleting the separate takeover-confirmation round. These candidates did not reduce complete T_VALID in this environment; some were materially slower.

`51,454 ms` is the best observed valid result under the frozen contract, not a claim of a universal lower bound. Replace it only with a faster Reality that keeps the same VALID contract.

## Split-brain prevention

For long tasks, reuse ECC v3.1.1 lease/fencing concepts so only the current lease holder updates authoritative task state.

## Mature assets reused

- Playwright Native AI Browser: ChatGPT query/send/wait_extract and page recovery
- ECC v3.1.1: checkpoint, handoff, lease/fencing
- Reasonix Recovery Kit: context fallback, repair and runtime health checks

Current status:

```ini
SESSION_CONTINUITY_CONTROLLER=V0_4_5_CLEAN_LIFECYCLE_TSTAR_R18_R19
PROACTIVE_SESSION_ROTATION=REALITY_PASS_FORCE_ROTATE_R1
TRUE_NEW_CHAT_ONLY=YES
BRANCH_RECOVERY=FORBIDDEN
PAGE_FAILOVER_E2E=TRUE_NEW_CHAT_RECOVERY_PASS
STALL_DETECTION_FULL_E2E=PASS_SAFE_FAULT_INJECTION_R10
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


## v0.3.0 correction / 2026-10-03
- Recovery target is now explicitly **true New chat**, not “Branch in new chat”.
- User Reality observation: branch-based continuation immediately exhibited old-page-like latency/stall characteristics, so it is removed from the valid clean-session recovery candidates.
- The supervisor and runtime runner must reject branch-style recovery and use a minimal handoff into a true new conversation.
- This correction does not by itself certify the full page-failover E2E; Reality still requires old-page failure/stall → checkpoint → true New chat → exactly-once continuation.


## 单页持久租约 v0.3

专用 ChatGPT 浏览器页在任务生命周期内视为持久资源，不是一次性页面。

```text
任务开始
→ 优先复用已经打开的专用 ChatGPT 页
→ 建立 PAGE_LEASE
→ 保持同一 browser context + 同一 page 持续存活
→ 需要换会话时，仅在同一 leased page 内进入真正 New chat
→ FINAL_VALID / 明确 STOP / 页面不可恢复后才允许释放
```

硬规则：
- 已有可用专用 ChatGPT 页时，不为同一任务启动第二个 persistent context；
- “换页/新页”在恢复语义上指**新 conversation**，不是关闭浏览器再打开；
- 禁止使用 Branch；同一 leased page 导航到正常 New chat 根页后只投递最小 handoff；
- 子步骤失败、GPT 暂时不可用、切备脑，都不能自动关闭 leased page；
- refresh/recovery 允许，但不是默认；只有 page/browser 被证明不可恢复才重建；
- PAGE_LEASE 直到 FINAL_VALID、明确 STOP 或不可恢复才释放。


## Reality R6 / 2026-10-03｜复用已打开 GPT 浏览器

已真实验证：

```ini
EXISTING_BROWSER_REUSED=YES
EXISTING_BROWSER_PID=22140
SECOND_BROWSER_LAUNCHED=NO
TRUE_NEW_CHAT=PASS
BRANCH_USED=NO
MINIMAL_HANDOFF=PASS
SUBMISSION_COUNT=1
MARKER_COUNT=1
ACK_CONFIRMED=YES
PAGE_LEASE_RETAINED=YES
GLOBAL_WRITER_LEASE=ACTIVE
```

执行规则正式收敛为：

```text
已有 shared-mcp ChatGPT 浏览器
→ 优先 attach / DevTools-CDP 复用
→ 禁止第二次 launch
→ 同一浏览器内进入真正 New chat
→ 最小 handoff exactly-once 继续
→ 任务结束后保持 browser/page lease
```

若 Playwright attach 或发送 DOM 确认失败，但现有浏览器仍活着，不得因此重新启动浏览器；改走 existing-browser raw CDP。R15 起进一步收紧：自动 bootstrap launch 只允许由唯一 Watchdog 在同一次 Windows 启动中执行最多 1 次；连续性 runtime 永久 attach-only，不具备 launch 权限，也不因健康检查自动创建新标签页。控制接口不可接管时 fail closed 并保留现有浏览器。

本轮同时修复 PID reuse：旧 lease-state 不再凭“PID 数字仍活着”冒充 owner；全局 writer lease 必须确认 PID 对应进程确实是 `chatgpt-continuity-runtime.js`。

Reality 证据：`evidence/TRUE-NEW-CHAT-EXISTING-BROWSER-REALITY-20261003-R6.json`。

## Reality R15 / 2026-10-03｜单专用浏览器死循环修复

用户现场发现专用 ChatGPT 浏览器出现重复打开、标签页持续堆叠并导致电脑卡顿。取证确认旧 Watchdog 在 CDP/profile 状态抖动后重复 `browser_launch_once`，修复前累计 12 次；旧 continuity supervisor 同时仍具备 `browser_tabs new` 能力，注册表另有 Chromium AutoLaunch，形成多 owner 冲突。

v0.4.3 收敛为：

```ini
DEDICATED_BROWSER_BOOTSTRAP_OWNER=WATCHDOG_ONLY
AUTO_BROWSER_LAUNCH_MAX_PER_WINDOWS_BOOT=1
CONTINUITY_RUNTIME_BROWSER_LAUNCH=FORBIDDEN
CONTINUITY_RUNTIME_AUTO_NEW_PAGE=FORBIDDEN
EXISTING_DEDICATED_BROWSER_PRESENT=NO_RELAUNCH
CONTROL_LOSS=FAIL_CLOSED_KEEP_BROWSER
```

Reality：修复版运行 15 秒并追加观察 20 秒，`browser_launch_once` 计数保持 `12 → 12 → 12`；专用 Chrome-for-Testing 顶层窗口保持 1；现有浏览器没有被关闭。当前 CDP 不可用时 Watchdog 正确进入 `CDP_DEGRADED_EXISTING_BROWSER_NO_RELAUNCH`。

权威证据：`evidence/SINGLE-BROWSER-LOOP-FIX-REALITY-20261003-R15.json`。

## Reality R10 / 2026-10-03｜活跃卡死全链路故障注入

v0.4.1 已完成安全、无副作用的完整 Reality：

```text
同一 existing shared-mcp 浏览器
→ raw CDP 启动长文本 turn
→ 故障注入抑制进展信号
→ silence deadline exceeded
→ read-only probe
→ turnActive 仍为 true
→ ABORT_STALLED_TURN
→ stop=false / composer=true
→ checkpoint: CONFIRMED_STALL_ABORTED
→ 真正 New chat
→ raw CDP 最小 handoff
→ submissionCount=1
→ markerCount=1
→ ACK=true
```

同时验证 `branchUsed=false`、`newBrowserLaunched=false`、PAGE_LEASE 保留。确定性 supervisor 回归同步提升为 19/19。R8/R9/早期 R10 均按 fail-closed 记录失败，没有冒充 PASS。

权威证据：`evidence/STALL-DETECTION-FULL-E2E-REALITY-20261003-R10.json`。

## v0.4｜技能包激活即启用连续性运行

当“长期记忆超级虚拟人”被明确指定为当前任务运行技能包时，本控制器不再是可选附加项，而是默认运行层。

```ini
ACTIVATION_SCOPE=CURRENT_TASK_LIFECYCLE
MONITOR_CURRENT_CHAT=YES
PROACTIVE_ROTATION=YES
TRUE_NEW_CHAT_ONLY=YES
BRANCH=FORBIDDEN
EXISTING_BROWSER_FIRST=YES
KEEP_BROWSER_OPEN=YES
CHECKPOINT_REQUIRED=YES
EXACTLY_ONCE_REQUIRED=YES
```

长页面策略：能在安全 checkpoint 提前换就提前换，不以“已经彻底卡死”作为换页前提。页面发生异常时按故障分类处理：短暂断连先观察后台；确认停滞则 checkpoint → true New chat；服务级不可用则切独立备脑。恢复和换页都不得关闭已存在的 shared-mcp GPT 浏览器。


## Legacy policy status

All pre-v0.4.4 page-continuity/recovery policies remain available through Git history/evidence and `LEGACY_CONTINUITY_INDEX.md`. They are reference-only and must not be started in parallel with the v0.4.4 controller.
