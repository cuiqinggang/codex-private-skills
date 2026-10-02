# 长期记忆超级虚拟人｜恢复阶梯 v0.3

```text
L0 当前会话正常执行
↓
L1 最小重试
↓
L2 Checkpoint + 真正 New chat 恢复（禁止 Branch）
↓
L3 工具主路切备路
↓
L4 换成熟等价执行器
↓
L5 GPT 不可用 → 独立强备份
↓
BLOCKED：持久化状态并等待依赖恢复
```

## Checkpoint 最小内容

- TASK_ID；
- 当前任务合同版本；
- 最终现实目标；
- 已完成；
- 未完成；
- 当前状态；
- 失败路径与根因；
- 当前工具/连接状态；
- 下一步唯一动作；
- 关键文件、Commit、Run ID、Artifact ID；
- FLOW_START 与当前时间轴状态。

恢复不是重新规划一个新项目，而是从最近可信状态继续原任务。


## v0.3 新会话恢复硬规则

```ini
RECOVERY_TARGET=TRUE_NEW_CHAT
BRANCH_RECOVERY=NO
FULL_HISTORY_REPLAY=NO
EXACTLY_ONCE_MARKER=YES
```

页面异常时，优先读取最近可信 Checkpoint；只有超过任务专属静默/恢复窗口且没有后台完成证据，才切换到真正 New chat。恢复包只携带任务合同、已确认结论、当前 checkpoint、未决项、下一条动作和安全边界。
