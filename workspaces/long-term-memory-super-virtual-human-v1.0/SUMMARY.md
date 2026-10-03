# 长期记忆超级虚拟人 v1.0｜当前摘要

```ini
PROJECT=长期记忆超级虚拟人
WORKSPACE_VERSION=v1.0
SKILL_VERSION=v0.4.3
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

SESSION_CONTINUITY_TESTS=19_PASS_0_FAIL
ECC_LEASE_TAKEOVER_FAULT=59_PASS_0_FAIL
INDEPENDENT_BACKUP_BRAIN=PASS_REASONIX_DEEPSEEK
K_DRIVE_REPO_BACKUP_RESTORE=PASS

NATURAL_STALL_DETECTION_FULL_E2E=PASS_BY_SAFE_FAULT_INJECTION_R10
PAGE_RECOVERY_DEDICATED_BROWSER_REALITY=PASS_R25
CURRENT_SHARED_MCP_IN_PLACE_RECOVERY=DEGRADED_NO_CDP
DCR_LOGOFF_RELOGIN_REALITY=OPEN
MODEL_EFFORT_FULL_E2E=PASS_R14
REAL_VALUABLE_LONG_TASK_FINAL_VALID=OPEN
PAID_TO_FREE_OPEN_SOURCE_REPLACEMENT=V1_0_0_REGISTERED
FREE_SOFTWARE_CATALOG=2026-10-03-R1_96_ENTRIES
```

## 当前正式判断

- 技能包已升级为 **v0.4.3**；v0.4.1 补齐活跃长回答卡死自动恢复，v0.4.2 闭合模型/Thinking 完整 E2E，v0.4.3 修复专用浏览器重复 launch/造页死循环并冻结“一次开机最多一次自动 launch、后续只 attach”的硬规则。
- 当用户明确说“按长期记忆超级虚拟人运行/完成当前任务”时，当前任务自动启用：连续性监控、Checkpoint、长页提前轮换、真正 New chat、禁止 Branch、复用已打开 GPT 浏览器、exactly-once、全局 writer lease。
- 长任务不追求无限单页；页面较长、下一阶段复杂或已有卡顿历史时，在安全 checkpoint 能换就提前换。
- “连接已断开/正在重新连接”不等于后台任务失败；先观察后台进展，确认停滞后才恢复，避免重复执行。
- 页面只是工作内存；长期记忆、项目权威状态、TASK_CONTRACT 和 Checkpoint 才是恢复依据。

## 已通过的连续性 Reality

Reality R6 已真实证明：

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
GLOBAL_WRITER_LEASE=PASS
```

现有浏览器优先级：

```text
已有 shared-mcp GPT 浏览器
→ 直接复用
→ Playwright 可用则用
→ Playwright attach/DOM 确认不兼容则切 existing-browser raw CDP
→ profile 已被占用但控制面暂不可接管：fail closed，不重新 launch
→ 只有确认不存在现有 owner 时才允许首次启动
```

任务完成、主路失败或切独立备脑时均不得自动关闭持久 GPT 浏览器。

R15 进一步冻结：Watchdog 是唯一允许执行 bootstrap launch 的入口，同一次 Windows 启动最多 1 次；连续性 runtime 只能 attach/refresh/同浏览器切 true New chat，不允许 launch 第二浏览器，也不允许健康检查自动新建标签页。控制接口失效时 fail closed，保留现有浏览器。

## 已完成的其他基础能力

- ECC v3.1.1 lease / takeover / fault：59 PASS / 0 FAIL；
- Reasonix v1.38.6 + DeepSeek-V4.1-Flash 独立备脑 Reality PASS；
- GitHub + K 盘状态备份/恢复已有 PASS 证据；
- Windows 执行层已具备 Desktop Commander Remote + GitHub self-hosted runner 双路径基础；
- 模型/Thinking：R14 已完成现有浏览器复用、High → Medium、语义读回、exactly-once continuation、ACK、非法档位 fail-closed 与恢复原 High；`MODEL_EFFORT_FULL_E2E=PASS_R14`。
- **收费转免费·开源替代技能包 v1.0.0** 已注册为按需能力：目录 `2026-10-03-R1` 共 96 项；优先成熟 OSS/自托管与 Agent 可操作接口，强制区分免费/开源/开放核心/Source-available；本扩展不改变 v0.4.3 连续性 runtime 与 `FINAL_VALID=NO`。

## 页面恢复 Reality R25（2026-10-03）

- 独立 `profile\\tests` 浏览器以 CDP 9333 实测完成：活跃生成故障注入 → 8 秒无进展硬门槛 → 只读 probe → 停止旧 turn → checkpoint → 真正 New chat → exactly-once handoff → 指定 ACK；`R25_PAGE_RECOVERY_REALITY=PASS`。
- `submissionCount=1`、`markerCount=1`、`ackConfirmed=true`、`branchUsed=false`、runtime 未另启浏览器。
- 证据：`workspaces/long-term-memory-super-virtual-human-v1.0/evidence/LTMVH-PAGE-RECOVERY-R25.md`。
- 本 PASS 仅证明独立可控测试浏览器链；当前已运行但无 CDP 的 `shared-mcp` 生产浏览器仍为 DEGRADED，不能把 R25 冒充为其原地恢复 PASS；`FINAL_VALID=NO` 保持不变。

## 当前未完成且不得误报

1. Desktop Commander 实际注销/重登后的自动恢复 Reality（R12 进程重连 PASS 不能替代本门）；
2. 至少一组真实有价值长任务从开始到 FINAL_VALID 的完整回归；
3. 独立备脑完成真实业务 DONE_WHEN，而不仅是恢复/健康 ACK。

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
