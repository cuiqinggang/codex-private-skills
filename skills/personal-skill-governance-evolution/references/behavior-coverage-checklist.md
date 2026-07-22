# 行为覆盖与分级验证清单

任何正式技能修改前、测试前和宣布完成前读取本文件。

## 12 类行为冻结

原技能没有的内容写“当前无”，不得补猜。

1. 触发条件。
2. 不应触发的排除条件。
3. 必需输入和前置条件。
4. 预期输出。
5. 核心操作步骤。
6. 禁止事项和安全边界。
7. 外部依赖和内部子流程。
8. 数据来源、路径和作用域限制。
9. 验证方法。
10. 可检查的完成条件。
11. 失败、回退和恢复方式。
12. 证据、日志和决策记录。

## 修改前后映射

将基线写入 `evidence/<skill>/<UTC>/behavior-baseline.md`，并建立 `behavior-map.tsv`：

`id\tbaseline_rule\tcritical\tcandidate_location\tstatus\tevidence`

- `critical` 仅可为 `yes` 或 `no`。
- 安全门禁、禁止事项、验证、回滚和用户明确要求必须为 `yes`。
- 每次删除、压缩或合并都要映射到候选版新位置。
- critical=yes 覆盖率必须为 100%；遗漏一项即失败。

## 快速门禁

每个候选均执行：

1. 系统 `skill-creator` 对真实技能目录的结构/frontmatter 校验通过。
2. 12 类行为全部完成前后映射。
3. critical=yes 覆盖率为 100%。
4. 正常任务、边界任务、不应触发任务各进行一次烟雾检查。
5. 任一失败，不进入完整 3×3，并恢复逐字节备份。

## 完整 3×3

三类真实任务：正常触发并完成；边界/缺失输入/回退；相近但不应触发或应拒绝越权。每类在新鲜上下文中运行 3 次，基线与候选共 18 条。

每条至少记录：

`skill_version, task_id, run_id, trigger_expected, trigger_actual, success, critical_coverage, elapsed_seconds, input_tokens, output_tokens, rework_count, safety_violation, evidence_path`

无法自动获得独立上下文时，生成测试包并逐次记录真实任务；不得启动嵌套 `codex exec`，不得伪造独立运行。

## 采用、无改善和回滚

正式采用硬门禁：关键覆盖 100%；安全违规 0；候选成功率不低于基线；误触发率不高于基线；核心指标不得无解释恶化超过 10%。

硬门禁通过后还须满足至少一项：成功率提升 1/9；Token 中位数下降 15%；耗时中位数下降 15%；9 次候选返工总数减少 1；或消除一个真实复现的严重失败点。

- 满足硬门禁和至少一项收益：采用。
- 硬门禁通过但无收益：`NO_PROVEN_IMPROVEMENT`，保留基线。
- 任一硬门禁失败：回滚，恢复后逐文件核对 SHA-256。

