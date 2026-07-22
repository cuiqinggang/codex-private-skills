# Codex 开工前复用检查清单

复杂任务开始前，先检查 C 盘热库，不得为了普通预检自动唤醒机械备份盘。

## 1. 默认检查范围

${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}

检查是否已有成熟技能、失败复盘、SOP、验收规则和用户认可结果。

## 2. K 盘边界

- `K:\AI\skills` 与 `K:\AI\workspaces` 仅作备份、历史参考和灾备。
- 普通预检不得枚举 K 盘。
- 只有用户明确要求检查或恢复备份时，才运行：

```powershell
${REDACTED_SECRET}
```

- 从 K 盘找到的资产只能作为证据或恢复候选；恢复后应从 C 盘运行。

## 3. 决策

- 有成熟 C 盘路径：优先复用。
- 有失败复盘：先避免复犯。
- C 盘缺失：返回 `BLOCKED_C_SOURCE_MISSING`，不得自动启用备份扫描。
- C→K 备份：必须先验证 C 正式副本，再取得用户对本次备份的明确批准；否则返回 `BACKUP_NOT_AUTHORIZED`。
- 无成熟资料：才新建最小方案。

## 4. 输出

```text
PREFLIGHT_REUSE_CHECK_DONE
已检查热路径:
K盘备份扫描: 未启用 / 已明确启用
可复用内容:
必须避免的问题:
本次采用路径:
```
