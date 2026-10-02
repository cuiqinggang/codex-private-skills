# 长期记忆超级虚拟人｜主脑故障切换合同 v0.1

## 目的

GPT 本身完全不可用时，不能依赖 GPT 自己发现故障或发起恢复。

故障检测与接管必须位于主脑之外。

## 状态机

```text
PRIMARY_HEALTHY
→ PRIMARY_DEGRADED
→ PRIMARY_UNAVAILABLE
→ FAILOVER_ACTIVE
→ PRIMARY_RECOVERING
→ PRIMARY_HEALTHY
```

## 独立检测信号

外部 watchdog 只依据可观察事实：
- 主脑请求无法建立；
- 连续请求超出本任务允许 deadline；
- 明确的服务/登录/配额/权限错误；
- 当前会话无法继续且新会话也不可用；
- 已派发现实任务长期没有主脑确认/验收 heartbeat。

不要用 GPT 自报“我健康”作为唯一信号。

## Failover

```text
PRIMARY_UNAVAILABLE
→ 冻结主脑写权限 / lease
→ 读取最新 TASK_CONTRACT
→ 读取最新 Checkpoint / Evidence
→ 独立备脑（Reasonix / DeepSeek 等低相关候选）
→ 调用同一成熟工具池
→ 继续到 FINAL_VALID
```

备脑不能要求 GPT 与 Codex 同时健康。

## 防脑裂

主脑恢复时不能直接重新写现实状态。

优先复用 ECC v3.1.1：
- lease；
- fencing；
- action ledger；
- checkpoint/handoff。

只有当前 lease 持有者有写权限。过期主脑回归后先读最新状态，再决定接回或保持备脑执行。

## 备脑最低能力

至少必须能：
- 读取 GitHub / K盘权威状态；
- 理解 TASK_CONTRACT；
- 读取 Checkpoint；
- 访问网络；
- 访问 Windows 至少一条执行通道；
- 调用长流程能力；
- 验证 FINAL_VALID；
- 写回新的 Checkpoint/handoff。

## 当前候选

```ini
PRIMARY=GPT
BACKUP_BRAIN_CANDIDATE=Reasonix/DeepSeek
LONG_FLOW_BACKUP=ECC_v3.1.1
WINDOWS_PATH_A=Desktop_Commander_Remote
WINDOWS_PATH_B=GitHub_self_hosted_runner
STATE_STORAGE_A=GitHub_private_repo
STATE_STORAGE_B=K_drive_backup
```

## Reality 验收

只有完成一次真实的“主脑不可用模拟”才允许：
```ini
INDEPENDENT_STRONG_BACKUP_CERTIFIED=YES
```

测试必须证明：
1. 外部 watchdog 判定 primary unavailable；
2. 备脑读取同一任务合同/Checkpoint；
3. 不依赖 GPT/Codex 完成一个真实代表任务；
4. 写回 Reality 证据；
5. GPT 恢复后通过 fencing/handoff 无重复执行地接回。

当前：
```ini
INDEPENDENT_STRONG_BACKUP_CERTIFIED=NO
```
