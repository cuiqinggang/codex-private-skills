# 长期记忆超级虚拟人 v0.4.2｜状态固化 2026-10-03

```ini
VERSION=0.4.2
STATUS=VIRTUAL_MATURE_CONTINUITY_RUNTIME_ACTIVE
VIRTUAL_MATURE=YES
FINAL_VALID=NO
STATE_SNAPSHOT=FROZEN_FOR_NEXT_CHAT

OBJECTIVE=T*=min(T_VALID)
PRIMARY_BRAIN_CANDIDATE=GPT
LONG_TERM_MEMORY=REQUIRED

SKILL_INVOCATION_ACTIVATES_CONTINUITY=YES
CONTINUITY_MONITORING=REQUIRED
EARLY_ROTATION_FOR_LONG_TASKS=YES
CHECKPOINT_BEFORE_ROTATION=YES

RECOVERY_TARGET=TRUE_NEW_CHAT
BRANCH_RECOVERY=FORBIDDEN
MINIMAL_HANDOFF=REQUIRED
EXACTLY_ONCE_RECOVERY=PASS

EXISTING_BROWSER_REUSE=PASS
SECOND_BROWSER_LAUNCH_WHEN_EXISTING=FORBIDDEN
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

## v0.4 的版本含义

v0.4 不再把页面恢复视为“出了问题才手工调用的附加功能”。

当用户明确指定“长期记忆超级虚拟人”运行当前任务时，连续性运行合同自动生效：

```text
监控当前会话健康
→ 长页/复杂下一阶段时在安全 checkpoint 提前轮换
→ 断连先判断后台是否仍推进
→ 确认停滞后保存最小 Checkpoint
→ 复用已经打开且登录的 shared-mcp GPT 浏览器
→ 同一浏览器进入真正 New chat
→ 禁止 Branch
→ 最小 handoff exactly-once 继续
→ 任务完成后浏览器仍保持打开
```

## 已通过 Reality

R6：
- 复用既有 shared-mcp 登录浏览器：PASS；
- 未启动第二个浏览器：PASS；
- 真正 New chat：PASS；
- Branch：未使用且正式禁止；
- 最小 handoff：PASS；
- submissionCount=1；
- markerCount=1；
- ACK：PASS；
- PAGE_LEASE 保留：PASS；
- 全局 writer lease：PASS；
- PID reuse 假 owner：已修。

权威证据：
`evidence/TRUE-NEW-CHAT-EXISTING-BROWSER-REALITY-20261003-R6.json`

R10（v0.4.1）：
- 安全长文本故障注入启动：PASS；
- 活跃 turn 静默超时识别：PASS；
- read-only probe：PASS；
- 旧 turn 自动停止并确认：PASS；
- Checkpoint reason=`CONFIRMED_STALL_ABORTED`；
- 真正 New chat：PASS；
- raw CDP 最小 handoff：PASS；
- submissionCount=1 / markerCount=1 / ACK=true；
- Branch=false / newBrowserLaunched=false；
- PAGE_LEASE 保留：PASS。
权威证据：`evidence/STALL-DETECTION-FULL-E2E-REALITY-20261003-R10.json`。
正式常驻 v0.4.1 runtime 复位证据：`evidence/RUNTIME-ACTIVATION-20261003-V041-R11.json`。

R14（v0.4.2）：
- 复用现有 shared-mcp 浏览器：PASS；未启动第二浏览器；
- 中文 UI `高/中` 与 canonical `High/Medium` 归一化：PASS；
- High → Medium 实际切换与语义读回：PASS；
- continuation 只提交一次，ACK：PASS；
- exactly-once：PASS；非法档位 fail-closed：PASS；
- finally 恢复原 High：PASS。
权威证据：`evidence/MODEL-EFFORT-FULL-E2E-REALITY-20261003-R14.json`。

补充：`DCR_PROCESS_RECONNECT_R12=PASS` 只证明 Desktop Commander Remote 进程断连后的自动重连，不等于 Windows 注销/重登 Reality。

## 当前仍未完成

1. Desktop Commander 真正注销/重登 Reality；
2. 真实有价值长任务完整 FINAL_VALID；
3. 独立备脑完成业务级 DONE_WHEN。

这些门槛未全部满足前，不宣布 FINAL_VALID，不升级 v1.0 正式成熟版。
