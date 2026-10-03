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
DCR_LOGOFF_RELOGIN_REALITY=OPEN
MODEL_EFFORT_FULL_E2E=PASS_R14
REAL_VALUABLE_LONG_TASK_FINAL_VALID=OPEN
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
