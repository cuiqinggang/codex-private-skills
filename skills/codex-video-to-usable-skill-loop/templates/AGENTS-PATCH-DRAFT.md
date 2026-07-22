# AGENTS.md 补丁草案模板

> 合并到目标项目的 `AGENTS.md` 前先备份原文件，不得直接覆盖用户规则。

## Codex 长期经验复用规则

复杂任务开始前，先检查成熟技能、SOP、失败复盘和验收结果。

默认热路径：

${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}

备份边界：

- `K:\AI\skills`、`K:\AI\workspaces` 只作备份、历史参考和灾备。
- 普通任务不得自动扫描 K。
- 只有用户明确要求查备份，或 C 盘缺失必要资产时，才显式启用 `--include-backups`。
- 从 K 恢复的资产必须回到 C 盘运行。

开工前输出：

```text
PREFLIGHT_REUSE_CHECK_DONE
已检查热路径:
K盘备份扫描: 未启用 / 已明确启用
可复用内容:
必须避免的问题:
本次采用路径:
```
