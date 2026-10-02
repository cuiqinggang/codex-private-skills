# 长期记忆超级虚拟人｜独立强备份合同 v1.0

```ini
STATUS=REQUIREMENTS_FROZEN
PRIMARY=GPT_SUPER_BRAIN_ROUTE
BACKUP_REQUIRED=YES
BACKUP_MAY_BE_SLOWER=YES
BACKUP_MUST_REACH_SAME_VALID=YES
BACKUP_MUST_NOT_REQUIRE_GPT=TRUE
BACKUP_MUST_NOT_REQUIRE_CODEX=TRUE
```

## 目标

主路线发生以下故障时，关键工作不能整体停止：

- GPT 服务不可用；
- ChatGPT 登录 / 会话 / 配额故障；
- GPT 页面长期无响应；
- Codex 同时不可用或权限不足；
- 单一供应商发生区域性或账号级故障。

## 备份必须具备

1. 能读取长期项目权威状态与最近 Checkpoint；
2. 能使用网络搜索 / 浏览器 / API 中至少一条成熟信息路径；
3. 能使用本地 Windows 执行通道或等价远程执行能力；
4. 能调用至少一个非 GPT、非 Codex 的成熟智能核心；
5. 能继续已有任务，而不是要求从零重新描述；
6. 能保存现实结果、错误、日志和新的 Checkpoint；
7. 能达到与主路线相同的 FINAL_VALID 定义。

## 候选能力池

候选而非固定答案：

- Reasonix + 可用高能力模型；
- DeepSeek 系成熟模型；
- 已验证浏览器自动化；
- GitHub Windows runner；
- n8n / OpenClaw 等成熟自动化；
- 本地 CLI / API；
- 其他后续 Reality 证明可用的成熟工具。

## 禁止的伪备份

以下不能算独立强备份：

- 只是换一个新的 ChatGPT 页面；
- GPT 不可用时仍要求 GPT 生成下一步；
- Codex 故障时仍必须由 Codex 执行；
- 只有文档，没有真实执行通路；
- 只能完成玩具任务，不能恢复正式任务。

## Reality Gate

备份路线必须在同一批正式任务上至少验证：

```text
主路线故意不可用
→ 从最近 Checkpoint 恢复
→ 读取权威项目状态
→ 独立判断 / 执行
→ 现实验收
→ FINAL_VALID
```

记录 `T_VALID_BACKUP`。

备份不参与日常并行竞争，除非主路线不可用，或 Reality 证明它在某类任务上反而更快。

## 当前状态

`STRONG_BACKUP_CERTIFIED=NO`

先完成 GPT 主路线 v1.0 的最小 Reality，再立即进入独立强备份 Reality；此项不得因主路线成功而取消。
