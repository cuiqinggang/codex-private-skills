# Reality Smoke Task R1｜极限短时间自动化闭环 v2.0

```ini
TASK_ID=ETAL-v2.0-REALITY-001
ROUND=R1
STATE=10
TYPE=REAL_USER_WORK
CANDIDATES=ChatGPT Work;Manus 2.0
OBJECTIVE=T*=min(T_VALID)
NO_MANUAL_MESSAGE_RELAY=TRUE
```

## 1. 任务目的

这不是专门制造的 Benchmark。

它本身就是当前项目需要完成的真实工作：

> 从共同私库恢复“极限短时间自动化闭环 v2.0”的当前状态，独立核验两个最终候选的当前官方能力，形成一份可复用 Reality 证据，并把结果真实写回共同私库 main；完成后远端回读验证。

## 2. 用户只给一次目标

候选收到本任务后，除以下情况外不得要求用户继续复制、转发或搬运中间信息：

- 必须本人登录 / MFA；
- 必须本人授权 GitHub 或相关账户；
- 平台强制的重要操作审批；
- 出现只有用户本人知道的现实事实。

普通搜索词选择、来源选择、失败重试、页面恢复、GitHub 文件写入与验收必须自行处理。

## 3. 必须读取

共同私库：

`cuiqinggang/codex-private-skills`

至少读取：

1. `00_START_HERE/COMMON-ENTRY.md`
2. `skills/extreme-time-agent-constitution/SKILL.md`
3. `workspaces/extreme-time-automation-loop-v2.0/README.md`
4. `workspaces/extreme-time-automation-loop-v2.0/REALITY_CONTRACT.md`
5. `workspaces/extreme-time-automation-loop-v2.0/MATURE_SOLUTION_COMPETITION_R1.md`

## 4. 必须独立核验的现实信息

只用当前官方来源重新核验：

### ChatGPT Work
- 长任务 / 多步骤定位；
- Projects / 上下文连续；
- Plugins / connected apps；
- Cloud Browser；
- Desktop Local Work / 本地文件或应用；
- Scheduled / event-triggered tasks；
- 重要操作审批；
- 已知限制。

### Manus 2.0
- Cascade；
- Studio；
- Cloud Computer；
- Computer Use / Remote Control；
- Automations；
- 浏览器能力；
- 已知限制。

如果官方资料与仓库 R1 报告发生变化，必须指出 Delta。

## 5. 必须产生的现实产物

在 main 创建：

`workspaces/extreme-time-automation-loop-v2.0/reality/REALITY-001-OUTPUT.md`

必须包含：

```ini
TASK_ID=ETAL-v2.0-REALITY-001
CANDIDATE_EXECUTOR=<ChatGPT Work 或 Manus 2.0>
FLOW_START=<平台可确认的现实开始时间>
FLOW_END=<完成远端验证的现实时间>
T_VALID=<端到端有效耗时；能可靠得到则填写>
RESULT=PASS|FAIL
USER_INTERVENTIONS=<次数>
RECOVERY_EVENTS=<次数>
FALSE_COMPLETION_EVENTS=<次数>
```

正文至少包含：
- 读取到的 v2.0 当前状态；
- 官方来源清单；
- 与 `MATURE_SOLUTION_COMPETITION_R1.md` 的 Delta；
- 执行中发生的失败 / 恢复；
- 人工介入原因；
- 远端写入验证证据。

## 6. FINAL_VALID

只有同时满足以下条件才 PASS：

1. 上述目标文件真实存在于 GitHub main；
2. 文件内容完整；
3. 官方来源是当前可访问来源；
4. 完成写入后重新从远端读取，而不是只相信写入返回；
5. 回读内容包含正确的 `TASK_ID=ETAL-v2.0-REALITY-001`；
6. 没有要求用户做人肉中间消息总线；
7. 任何失败 / 用户介入都如实记录；
8. 不以“我已经完成”自报替代远端事实。

## 7. 失败恢复规则

普通失败：
```text
观察
→ 根因
→ 使用当前成熟能力恢复
→ 继续同一任务
```

不得因为普通工具失败就让用户复制错误给另一个智能体。

如果候选自身无法完成，应真实写：
`RESULT=FAIL`
并记录阻塞点；不得临时设计新的自研系统绕过。

## 8. 时间边界

```text
FLOW_START =
候选已经收到本任务，且完成任何不可替代的首次登录/授权后，
开始读取共同私库的现实时间。

FLOW_END =
目标文件已经写入 GitHub main，并完成远端重新读取验证的现实时间。
```

所有搜索、等待、失败、恢复、重试均计入。

## 9. 比较原则

两个候选必须执行同一任务。

比较时优先：

`VALID → T_VALID`

以下只用于解释 T_VALID：
- USER_INTERVENTIONS
- RECOVERY_EVENTS
- FALSE_COMPLETION_EVENTS

## 10. 下一轮条件

若 R1 已经明显暴露完整候选不具备某项关键能力，不为测试而继续测试。

若两者都 PASS 且差异仍不足以决定主路径，再设计 R2，优先覆盖：
- 本地 Windows；
- 中断 / 跨设备恢复；
- 定时 / 触发；
- 真正长任务。
