# 长期记忆超级虚拟人 v0.3.0｜状态固化 2026-10-03

```ini
VERSION=0.3.0
STATUS=VIRTUAL_MATURE_RECOVERY_AUTOMATION_IMPLEMENTING
VIRTUAL_MATURE=YES
FINAL_VALID=NO
STATE_SNAPSHOT=FROZEN_FOR_CONTINUATION

OBJECTIVE=T*=min(T_VALID)
PRIMARY_BRAIN_CANDIDATE=GPT
LONG_TERM_MEMORY=REQUIRED

SESSION_CONTINUITY_SUPERVISOR=V0_3
SESSION_CONTINUITY_TESTS=17_PASS_0_FAIL
RECOVERY_TARGET=TRUE_NEW_CHAT
BRANCH_RECOVERY=FORBIDDEN
MINIMAL_HANDOFF=REQUIRED
FULL_OLD_CONTEXT_REPLAY=FORBIDDEN

ECC_LEASE_TAKEOVER_FAULT_REALITY=59_PASS_0_FAIL
INDEPENDENT_BACKUP_BRAIN=PASS_REASONIX_DEEPSEEK
K_DRIVE_REPO_BACKUP_RESTORE=PASS
WINDOWS_PRIMARY_PATH=DESKTOP_COMMANDER_REMOTE
WINDOWS_BACKUP_PATH=GITHUB_SELF_HOSTED_RUNNER

CHATGPT_PAGE_FAILOVER_E2E=IN_REALITY_VERIFICATION
GPT_SERVICE_FAILOVER=PASS
FINAL_VALID=NO
```

## 本次保存的已完成成果

- 轻入口 + 强能力池 + 按需路由架构已形成；
- 长任务 TASK_CONTRACT / Checkpoint / 防漂移规则已形成；
- Session Continuity Supervisor 已完成 v0.3 Branch 拒绝修正；
- ECC v3.1.1 lease / takeover / fault Reality 59/59；
- Reasonix + DeepSeek 独立备脑 Reality 已通过；
- GitHub + K 盘状态恢复已有通过证据；
- Windows 执行层已有 Desktop Commander Remote + GitHub runner 双路径基础；
- ChatGPT 模型/思考强度控制已有 Medium→High 读回 PASS，但完整 exactly-once E2E 仍未闭合。

## v0.3 关键修正

用户直接使用发现：“在新聊天中分支 / Branch”虽然视觉上像新页面，但实际继续工作时出现与老长页面相似的卡顿/等待表现。

因此 v0.3 正式排除它：

```text
旧会话异常
→ 只读探测是否仍有后台进展
→ 超过任务专属窗口且确认停滞
→ 保存最近可信 Checkpoint
→ 打开真正 New chat
→ 仅投递最小 handoff
→ unique marker 防重复
→ exactly-once 继续
```

## 当前仍未完成

1. 真正完成一次“老页/坏页 → true New chat → exactly-once continuation”的 ChatGPT Reality；
2. Desktop Commander 实际注销/重登恢复；
3. 模型/Thinking 控制完整 continuation + restore E2E；
4. 至少一组真实有价值长任务从开始到 FINAL_VALID 的完整回归；
5. GPT 服务不可用后的备脑完成业务任务级 DONE_WHEN，而不只是健康 ACK。

这些未完成前，不升级 v1.0，不宣布 FINAL_VALID。
