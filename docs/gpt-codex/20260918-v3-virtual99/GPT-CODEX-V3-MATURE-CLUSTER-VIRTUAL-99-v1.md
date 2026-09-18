# GPT↔Codex 自动控制层 — v3 Mature Solution Cluster + Virtual-99 v1

状态：VIRTUAL_99_FROZEN_FOR_IMPLEMENTATION / L1_NOT_YET_EXECUTED

基线：
- source branch: codex/gpt-codex-convergence-orchestrator-v1.1.0
- source HEAD: 0a7b4759c56f5d263fd99de87a411eafc2f27a0f
- method: first-principles-physical-limit-convergence v3.0.0
- current maturity remains L0_SPEC_READY

## 1. Frozen task contract

目标不是重新发明可靠自动化，而是把现实成熟 primitive 组合成 GPT↔Codex 的最短可靠闭环。

~~~
CODEX = LOOP_OWNER / DETERMINISTIC_EXECUTOR
GPT = ON_DEMAND_PLANNER_JUDGE
GITHUB = REMOTE IMMUTABLE MESSAGE LOG + SHARED TRUTH
AI_BROWSER = WAKEUP/ACK TRANSPORT ONLY
LOCAL_SQLITE = DURABLE ACTION/INBOX/OUTBOX/LEASE LEDGER

NO_FREE_EXPLORATION=YES
CODEX_PLAN_AUTHORITY=NONE
GPT_PLAN_AUTHORITY=YES
BROWSER_LONG_PAYLOAD_TRANSPORT=NO
MANUAL_COPY_PASTE_TARGET=ZERO
NO_FORCE_PUSH=YES
NO_PROXY_CHANGE=YES
NO_H3_GPU_IN_L1=YES
~~~

唯一当前目标：以最短时间得到第一个满足全部 L1 VALID 的真实 Shadow Pilot。

## 2. Gate 0 — 成熟方案集群

不自创可靠性理论，直接吸收工业成熟语义：

1. Durable execution / checkpoint / replay
   - 持久状态；
   - 崩溃、重启、网络失败后从已提交历史恢复；
   - control flow 确定性；
   - 非确定性副作用放在 executor/activity；
   - in-flight workflow 版本隔离。

2. At-least-once delivery + idempotent consumer
   - 外部事件、wakeup、poll、activity 可以重复；
   - transport 重复是正常情况；
   - 目标不是“永不重复”，而是“重复不能产生第二次业务副作用”。

3. Retry / Catch / timeout
   - retry 必须由固定策略驱动；
   - failure 必须分类；
   - retry exhausted 后 BLOCKED/Catch；
   - 不允许失败后自由探索。

4. SQLite atomic local durability
   - sqlite3 transaction；
   - WAL；
   - BEGIN IMMEDIATE 用于短事务 claim/ledger/lease 更新；
   - SQLite 只做本机 durable ledger/cache，不替代 GitHub remote truth。

5. Git optimistic concurrency / CAS
   - 一条 logical message 的 envelope + payload 必须在同一个 Git commit；
   - commit parent 是发布者刚观察到的 remote HEAD；
   - branch ref 只允许 non-force fast-forward；
   - 冲突后 refetch，再发布同一个 logical event；
   - 禁止 force push。

## 3. v1.1.0 审计

### KEEP
- Codex-first loop owner；
- GPT-only business planning authority；
- GitHub numbered immutable bus；
- Browser wakeup-only；
- ACTION_ID / DO_NOT_REPEAT 思路；
- capacity failover 不改变业务计划；
- A1-A15、N1-N5；
- L0→L1→L2→L3→L4 maturity gate。

### MUST FIX BEFORE L1
1. 当前仓库没有可运行 orchestrator，只是 SKILL/reference/schema。
2. envelope 与 payload 尚无原子发布协议。
3. source_commit 身份模型不严谨：消息内容无法预写承载自己的 commit SHA。
4. 没有 durable inbox/outbox/action ledger。
5. 没有 crash-after-side-effect-before-DONE reconciliation。
6. 没有 logical-event 去重。
7. 没有 single-active-runner lease/fencing。
8. STATE.json 与 queue 可能形成双事实源。
9. 没有 protocol/orchestrator/task-contract version pinning。
10. 没有 side-effect safety class。
11. 没有 timeout/backoff/deadline 固定机制。
12. EVENTS.jsonl 是可变热点文件，不应作为并发 remote event log。

## 4. Virtual-99 final architecture

### 4.1 Dedicated runtime branch

每个任务使用独立 bus branch：

~~~
bus/<TASK_ID>
~~~

workspace：

~~~
workspaces/<TASK_ID>/
  TASK.md
  STATE.json              # DERIVED SNAPSHOT ONLY
  queue/
  payloads/
  ARTIFACTS.md
~~~

事实优先级：

~~~
1. Git commit history + immutable queue/payload
2. local SQLite durable ledger
3. STATE.json derived snapshot
~~~

STATE.json 必须记录 derived_from_remote_head、protocol_version、task_contract_hash。
若 snapshot 与 event history 不一致，重建 snapshot，不改历史。

### 4.2 Message envelope v2

最低字段：

~~~
protocol_version
task_id
seq
message_id
logical_event_id
parent_message_id
parent_commit
sender
receiver
type
status
payload_path
payload_sha256
task_contract_hash
created_at
~~~

删除“消息自身 commit SHA 必须预写进 envelope”的要求。

logical_event_id 使用稳定输入生成，至少包含：

~~~
task_id
parent_message_id
sender
receiver
type
semantic_action_id
~~~

duplicate wakeup / uncertain network retry 必须复用同一个 logical_event_id。

### 4.3 Atomic Git publish

~~~
FETCH REMOTE HEAD H0
-> scan max_seq + existing logical_event_id
-> if logical event exists: ACK_EXISTING
-> allocate seq=max+1
-> build payload + envelope
-> verify payload_sha256
-> create ONE commit parent=H0 containing envelope+payload
-> update branch ref force=false
   PASS -> remote verify commit/files/hash
   CONFLICT -> refetch
               search logical_event_id
               exists -> ACK_EXISTING
               absent -> reallocate seq and retry SAME logical event
~~~

### 4.4 Local durable ledger

路径：

C:\AI\GPT-Codex-Convergence-Orchestrator\state\orchestrator.db

SQLite WAL，至少包含：

~~~
inbox(message_id PK, logical_event_id UNIQUE, payload_sha256, remote_commit, status, received_at)

actions(action_id PK, message_id, action_type, safety_class, status,
        attempt_count, effect_fingerprint, started_at, completed_at, last_error)

outbox(logical_event_id PK, parent_message_id, message_type, payload_sha256,
       status, remote_seq, remote_commit)

leases(task_id PK, holder_id, fence_token, expires_at, heartbeat_at)

transport_attempts(transport_id, logical_event_id, kind, attempt_no,
                   status, started_at, completed_at, error)
~~~

ledger 状态变化必须在 SQLite transaction 中完成。

### 4.5 Single active runner

同一 TASK_ID 同时仅允许一个 active Codex orchestrator。

claim：

~~~
BEGIN IMMEDIATE
-> read lease
-> acquire/renew if absent or expired
-> increment fence_token on new holder
-> COMMIT
~~~

失去 lease 的旧 runner 不得继续执行新副作用或提交新状态。

### 4.6 Action identity

~~~
ACTION_ID =
SHA256(task_id | message_id | action_type | payload_sha256 | task_contract_hash)
~~~

模型切换、Windows restart、duplicate poll 不改变 ACTION_ID。

### 4.7 Side-effect safety classes

~~~
S0 PURE
S1 IDEMPOTENT_REPLACEABLE
S2 TARGET_IDEMPOTENCY_KEY
S3 READ_AFTER_WRITE_RECONCILABLE
S4 NON_IDEMPOTENT_UNVERIFIABLE
~~~

- S0/S1：可安全重试。
- S2：始终复用同一个 target idempotency key。
- S3：重启先 reconcile；确认目标效果存在则 RECOVERED_DONE，不再执行。
- S4：如果崩溃后无法判断副作用是否发生，禁止自动 replay，转 BLOCKED / REQUEST_GPT_OR_USER。

正式可靠性目标：

~~~
AT_LEAST_ONCE_INPUT
+ IDEMPOTENT_OR_RECONCILED_EFFECT
= NO_DUPLICATE_VALID_SIDE_EFFECT
~~~

不宣称全局 exactly-once。

### 4.8 Crash window protocol

~~~
DISCOVERED
-> CLAIMED
-> PRECHECK
-> RUNNING
-> EFFECT_VERIFIED
-> DONE
-> RESULT_OUTBOXED
-> RESULT_PUBLISHED
~~~

恢复：
- DISCOVERED/CLAIMED/PRECHECK：同 ACTION_ID 恢复。
- RUNNING：先 reconcile，绝不能直接 rerun。
- EFFECT_VERIFIED：只补 DONE/RESULT。
- DONE：只补 outbox/publish。
- RESULT_OUTBOXED：只补 Git publish。
- RESULT_PUBLISHED：不重复发布。

### 4.9 GPT duplicate wakeup

Browser wakeup 是 at-least-once transport。

GPT：

~~~
read request
-> derive expected reply logical_event_id
-> scan remote for same logical_event_id / parent_message_id
   exists -> ACK_EXISTING
   absent -> atomic CAS publish one reply
~~~

重复 wakeup 不依赖 Browser 自己做到 exactly-once。

### 4.10 Codex duplicate poll

~~~
inbox UNIQUE(message_id, logical_event_id)
-> ACTION_ID lookup
-> DONE? no replay
-> RUNNING? reconcile
-> otherwise execute according to safety_class
~~~

### 4.11 Timeout / retry

每类 transport 必须有：

~~~
initial_delay
max_delay
deadline
retryable_error_classes
~~~

L1 的具体时间参数仅作为 toy calibration，不升级为永久生产参数。
所有 retry 必须复用同 logical_event_id / ACTION_ID。

### 4.12 Version pinning

每个 task 冻结：

~~~
protocol_version
orchestrator_version
task_contract_hash
command_schema_version
~~~

未知 major / contract hash mismatch：

~~~
BLOCKED
~~~

不得 best-effort 兼容。

### 4.13 Capacity failover

Capacity Router 只能改变 executor model availability：

~~~
same task
same message
same ACTION_ID
same frozen command
same side-effect policy
~~~

failover 前后先查 ledger/reconcile；禁止 replay 已完成 work。

## 5. Minimal implementation

为最短 T_VALID，L1 不部署 Temporal/Azure/AWS 服务本体；复制成熟 durable semantics，并使用当前已有最小组件：

~~~
Python stdlib
+ sqlite3
+ native git
+ existing Playwright Native AI Browser
+ existing Capacity Router
~~~

目标：

~~~
C:\AI\GPT-Codex-Convergence-Orchestrator\
  orchestrator.py
  config.json
  protocol.py
  storage.py
  reconcile.py
  adapters\github_bus.py
  adapters\chatgpt_wakeup.py
  adapters\codex_executor.py
  adapters\capacity_router.py
  state\orchestrator.db
  logs\
  reports\
  tests\fault_injection.py
~~~

禁止新增另一套 browser stack、daemon framework 或 workflow engine，除非 frozen implementation 被真实证据证明不能满足 VALID。

## 6. L1 toy task

~~~
TASK_ID=gpt-codex-shadow-pilot-v3
output=toy-result.txt
exact content=GPT_CODEX_CODE_TO_CODE_OK
verify=readback+SHA256
NO_H3_GPU=YES
~~~

链：

~~~
Codex publish 000001 REQUEST
-> Browser wake GPT
-> GPT atomic publish 000002 COMMAND
-> Codex consume/reconcile/execute
-> Codex atomic publish 000003 RESULT
-> Browser wake GPT
-> GPT atomic publish 000004 DECISION
-> Codex FREEZE/BLOCKED
~~~

用户中间复制粘贴次数必须为 0。

## 7. L1 acceptance

保留 A1-A15、N1-N5，新增：

~~~
R1 envelope+payload atomic same commit
R2 non-force CAS conflict does not overwrite work
R3 duplicate logical_event_id cannot produce second semantic message
R4 crash after side effect before DONE -> reconcile, no duplicate effect
R5 crash after DONE before Git publish -> publish result only
R6 crash after Git publish before local ACK -> detect existing logical event
R7 stale runner after lease loss cannot commit/execute next action
R8 protocol/contract mismatch -> BLOCKED
R9 STATE snapshot loss/corruption -> rebuild from immutable remote history
R10 capacity failover preserves ACTION_ID and no completed-effect replay
~~~

任何 A/N/R 项失败：

~~~
AUTOMATION_MATURITY=L0_SPEC_READY
L1=FAIL
READY_FOR_ASSISTED_REAL_TASK_PILOT=NO
~~~

全部通过才允许：

~~~
AUTOMATION_MATURITY=L1_SHADOW_PILOT_PASS
READY_FOR_ASSISTED_REAL_TASK_PILOT=YES
~~~

## 8. Frozen conclusion

~~~
WORLD_SOLVED=YES
UNSOLVED_PRIMITIVE=NONE
REINVENTION_BAN=ON
NOVEL_RESEARCH_ALLOWED=NO

V1_1_DIRECTION=KEEP
V1_1_RUNTIME_COMPLETENESS=INSUFFICIENT

VIRTUAL_99_FINAL_ARCHITECTURE=
  IMMUTABLE_GIT_EVENT_LOG
  + AT_LEAST_ONCE_TRANSPORT
  + IDEMPOTENT/RECONCILED_EFFECTS
  + SQLITE_DURABLE_LEDGER
  + LEASE/FENCING
  + OUTBOX/INBOX
  + NON_FORCE_GIT_CAS
  + PROTOCOL_VERSION_PINNING
  + DETERMINISTIC_CODEX_STATE_MACHINE

NEXT_ACTION=
  IMPLEMENT_THIS_FROZEN_PLAN
  -> LOCAL_FAULT_INJECTION
  -> TRUE_L1_SHADOW_PILOT
~~~

此文档冻结“做什么”。Codex 仅可在不改变语义的前提下决定“怎么完成一个已授权动作”。
