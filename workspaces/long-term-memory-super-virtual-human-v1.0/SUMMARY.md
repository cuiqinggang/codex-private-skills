# 长期记忆超级虚拟人 v1.0｜当前摘要

```ini
PROJECT=长期记忆超级虚拟人
WORKSPACE_VERSION=v1.0
SKILL_VERSION=v0.4.5
SKILL_ENGLISH_NAME=Long-Term Memory Super Virtual Human

STATE=10
VIRTUAL_MATURE=YES
FINAL_VALID=NO

OBJECTIVE=T*=min(T_VALID)
PRIMARY_BRAIN_CANDIDATE=GPT
LONG_TERM_MEMORY=REQUIRED

CONSTITUTION=极限短时间智能体宪法 v0.3.1
METHOD_REFERENCE=极限短时间自动化闭环 v2.0
WINDOWS_BRIDGE=GPT直连Windows双路执行桥 v0.2.0

CONTINUITY_RUNTIME=ACTIVE_BY_SKILL_INVOCATION
TRUE_NEW_CHAT_RECOVERY=PASS
BRANCH_RECOVERY=FORBIDDEN
EXISTING_BROWSER_REUSE=PASS
SECOND_BROWSER_LAUNCH_WHEN_EXISTING=FORBIDDEN
AUTO_BROWSER_LAUNCH_MAX_PER_WINDOWS_BOOT=1
CONTINUITY_RUNTIME_BROWSER_LAUNCH=FORBIDDEN
CONTINUITY_RUNTIME_AUTO_NEW_PAGE=FORBIDDEN
SINGLE_BROWSER_LOOP_GUARD=PASS_R15
EXACTLY_ONCE_RECOVERY=PASS
PAGE_LEASE_RETAINED=PASS
GLOBAL_WRITER_LEASE=PASS
PID_REUSE_FALSE_OWNER=FIXED

SESSION_CONTINUITY_TESTS=25_PASS_0_FAIL
ECC_LEASE_TAKEOVER_FAULT=59_PASS_0_FAIL
INDEPENDENT_BACKUP_BRAIN=PASS_REASONIX_DEEPSEEK
K_DRIVE_REPO_BACKUP_RESTORE=PASS

NATURAL_STALL_DETECTION_FULL_E2E=PASS_BY_SAFE_FAULT_INJECTION_R10
PAGE_RECOVERY_DEDICATED_BROWSER_REALITY=PASS_R25
CURRENT_SHARED_MCP_IN_PLACE_RECOVERY=PASS_PREVENTIVE_ROTATION_R1
DCR_LOGOFF_RELOGIN_REALITY=OPEN
MODEL_EFFORT_FULL_E2E=PASS_R14
REAL_VALUABLE_LONG_TASK_FINAL_VALID=PASS_GATE_A_20261004
PAID_TO_FREE_OPEN_SOURCE_REPLACEMENT=V1_0_0_REGISTERED
SINGLE_PRODUCTION_CONTINUITY_PATH=YES
LEGACY_PARALLEL_SUPERVISOR=NO
CEO_VISIBLE_TEXT_LIMIT_DEFAULT=40000
CEO_USER_TURN_LIMIT_DEFAULT=10
EXECUTOR_VISIBLE_TEXT_LIMIT_DEFAULT=30000
EXECUTOR_USER_TURN_LIMIT_DEFAULT=3
PROACTIVE_ROTATION_REALITY=PASS_20261004_R1
CEO_CLEAN_LIFECYCLE_REALITY=PASS_R18_R19
CEO_CLEAN_LIFECYCLE_T_STAR_MS=51454
CEO_CLEAN_LIFECYCLE_R19_MS=54246
IDLE_CHAT_PAGE_TARGET=1
FINAL_BROWSER_STATE=ONE_BLANK_NEW_CHAT_ROOT
FREE_SOFTWARE_CATALOG=2026-10-03-R1_96_ENTRIES
```

## 当前正式判断

- 技能包已升级为 **v0.4.5**；页面连续性继续使用单一生产控制链，并新增专用浏览器 CEO 干净生命周期冻结合同。
- CEO/总控页默认按 `40,000 可见字符 OR 10 用户轮次` 预防性轮换；执行页默认 `30,000 OR 3 轮`；同页压缩只用于形成 handoff，不视为释放上下文。
- 页面/UI 异常、断连、无进展、活跃 turn 卡死进入同一状态机：后台仍推进则等待；确认停滞才 abort + checkpoint + true New chat + minimal handoff + exactly-once。
- Reality `LTMVH-CEO-ROTATE-REALITY-20261004-R1` 已证明：现有 shared-mcp 浏览器保留、真正 New chat、submissionCount=1、markerCount=1、ACK=true、Branch=false、未启动第二浏览器。
- 旧 `C:\\AI\\LTMVH-Reality\\chatgpt-continuity-v1\\` 及旧页面恢复策略退役为历史资产；索引为 `skills/long-term-memory-super-virtual-human/LEGACY_CONTINUITY_INDEX.md`，禁止作为第二套生产控制器并行运行。
- **收费转免费·开源替代技能包 v1.0.0** 继续作为按需能力；本次升级不改变 `FINAL_VALID=NO`。


## v0.4.5｜CEO 专用浏览器干净生命周期与极限短时间冻结

- 干净基线：专用浏览器空闲时只保留 **1 个空白 ChatGPT New chat 页**；该页直接复用为 CEO-1。
- 执行页只按当前业务的最小必要数量创建；结果已被权威状态/CEO 接受后立即关闭，不保留历史执行页。
- CEO-1 只负责理解、拆分、DONE_WHEN；生成最小 checkpoint 后关闭；CEO-2 必须是真正 New chat，禁止 Branch，禁止重做已接受的 A/B 原任务。
- 任务 FINAL_VALID 与证据持久化后关闭最终 CEO，并恢复 **恰好 1 个空白 New chat 页**。
- Reality R18：全门 PASS，`T_VALID=51,454 ms`，checkpoint=125 chars，最终 ChatGPT 页数=1。
- Reality R19：同构复验全门 PASS，`T_VALID=54,246 ms`，最终 ChatGPT 页数=1。
- 当前观测 `T*=min(T_VALID)=51,454 ms`，来源 R18；仅当后续 Reality 在不降低 VALID 合同的条件下更快，才允许替换。
- 已测但不采用为默认路径：A/B 提前预热、Instant 控制链、CEO 同物理 tab 复用、删除独立接管确认回合。

## 页面恢复 Reality R25（2026-10-03）

- 独立 `profile\\tests` 浏览器以 CDP 9333 实测完成：活跃生成故障注入 → 8 秒无进展硬门槛 → 只读 probe → 停止旧 turn → checkpoint → 真正 New chat → exactly-once handoff → 指定 ACK；`R25_PAGE_RECOVERY_REALITY=PASS`。
- `submissionCount=1`、`markerCount=1`、`ackConfirmed=true`、`branchUsed=false`、runtime 未另启浏览器。
- 证据：`workspaces/long-term-memory-super-virtual-human-v1.0/evidence/LTMVH-PAGE-RECOVERY-R25.md`。
- 本 PASS 仅证明独立可控测试浏览器链；当前已运行但无 CDP 的 `shared-mcp` 生产浏览器仍为 DEGRADED，不能把 R25 冒充为其原地恢复 PASS；`FINAL_VALID=NO` 保持不变。

## 当前未完成且不得误报

1. Desktop Commander 实际注销/重登后的自动恢复 Reality（R12 进程重连 PASS 不能替代本门）；
2. 独立备脑完成真实业务 DONE_WHEN，而不仅是恢复/健康 ACK。

以上未全部完成前，保持 FINAL_VALID=NO，不升级 v1.0 正式成熟版。

## 权威入口

技能：
`skills/long-term-memory-super-virtual-human/SKILL.md`

连续性控制：
`skills/long-term-memory-super-virtual-human/CHATGPT_SESSION_CONTINUITY_CONTROLLER.md`

最新 Reality：
`skills/long-term-memory-super-virtual-human/evidence/STALL-DETECTION-FULL-E2E-REALITY-20261003-R10.json`

前置恢复 Reality：
`skills/long-term-memory-super-virtual-human/evidence/TRUE-NEW-CHAT-EXISTING-BROWSER-REALITY-20261003-R6.json`

v0.4 状态：
`skills/long-term-memory-super-virtual-human/REALITY_STATUS_2026-10-03_V0.4.md`

## 独立强备份建设（2026-10-03 R1）

用户要求：完全不依赖 GPT、Codex，以 v0.4.3 的同等现实功能为目标，沿用自动化闭环 v2.0 与 T*=min(T_VALID)；先讨论，再建设。

- 方案与建设合同：[INDEPENDENT_BACKUP_DESIGN_20261003_R1.md](INDEPENDENT_BACKUP_DESIGN_20261003_R1.md)。
- 当前为 STATE=10 讨论基线；本轮没有部署或完成独立业务 Reality；STRONG_BACKUP_CERTIFIED=NO。
- 优先验证已有 Reasonix＋DeepSeek 最短组合；OpenCode/OpenClaw 为对照候选，按完整 T_VALID 选择。
- 整链路检查独立性，包含入口、监督器、记忆嵌入、搜索、账号接口、视觉/媒体、验收与通知；不得保留隐藏 OpenAI 必需依赖。
- 不再等待主路线 v1.0 毕业才启动备份建设；此变化依据用户本轮明确要求。
- v0.4.3 主技能及主项目 FINAL_VALID=NO 保持不变。


## Gate A｜真实有价值长任务端到端 FINAL_VALID（2026-10-04）

- Gate A 任务：对 LTMVH v0.4.4 生产连续性链执行完整生产稳定性治理与验收。
- GitHub main / Windows 当前运行态 / Startup 已核对并收敛到 v0.4.4 单一生产链；本机发现的 SKILL、Controller 文档漂移和缺失 Legacy Index 已按 main 精确修复。
- Reality：runtime=1、legacy supervisor=0、shared-mcp browser root=1、lease heartbeat 持续前进、CDP 9223 在线；未关闭现有浏览器、未启动第二浏览器、未修改 FlClash/Windows 代理。
- 确定性回归：SESSION_CONTINUITY_TESTS=25 PASS / 0 FAIL；核心 JS syntax checks 全部 exit 0。
- 机器可读证据：`workspaces/long-term-memory-super-virtual-human-v1.0/evidence/LTMVH-V044-GATE-A-20261004.json`。
- `REAL_VALUABLE_LONG_TASK_FINAL_VALID=PASS_GATE_A_20261004`；仅关闭本 Gate，不改变项目级 `FINAL_VALID=NO`。
