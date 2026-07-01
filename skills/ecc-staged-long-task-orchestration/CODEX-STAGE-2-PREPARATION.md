# CODEX-STAGE-2-PREPARATION

## 目标

Codex P2 在本地读取 P1 control specification，准备最终执行所需的详细任务包与 skills / mature-path 补充，但不执行真实任务。

## 硬字段

```text
execute_real_task = false
final_pass_allowed = false
artifact_writes_allowed = preparation_only
```

## 必须输出

```text
draft-task-package.md
gap-analysis.md
missing-hard-gates.md
failure-mode-review.md
revised-task-package.md
skill-candidate-index.md
mature-path-index.md
skill-reuse-decision.md
skills-install-or-prepare-log.md
skills-integration-supplement.md
```

## Draft -> Audit -> Revised Draft -> Skill Search / Preparation

1. Draft：创建 `draft-task-package.md`。
2. Audit：从反向验证角度找漏洞、冲突、不可验收点。
3. Missing Hard Gates：列出所有缺失的硬门槛。
4. Failure Mode Review：列出可预见失败路径和 bad-case。
5. Revised Draft：修正为 `revised-task-package.md`。
6. Skill Search / Preparation：只能基于修正版和 gap 分析进行，不允许空泛搜索。

## Mature Component First Rule

对于网站、dashboard、知识库、审批队列、任务看板、工作流、文档站、内部工具等常见功能，P2 必须读取 `MATURE-COMPONENT-FIRST-GATE.md`。

P2 必须先检查 Hermes 路径存在性：

```text
C:\Users\A\.hermes\skills
C:\Users\A\.hermes\skills-archive
```

如果路径不存在，记录：

```text
HERMES_SKILL_PATH_NOT_FOUND
```

P2 默认路线优先级：

```text
ADOPT_DIRECTLY > ADAPT_LIGHTLY > TRY_LIGHTLY > REFERENCE_ONLY > BUILD_FROM_SCRATCH
```

如果建议自研，必须写：

```text
NO_MATURE_COMPONENT_FOUND_REASON
```

外部搜索状态必须是：

```text
EXTERNAL_COMPONENT_SEARCH_COMPLETED
EXTERNAL_COMPONENT_SEARCH_PARTIAL
EXTERNAL_COMPONENT_SEARCH_NOT_COMPLETED
```

如果没有联网或外部搜索工具不可用，写 `EXTERNAL_SEARCH_NOT_COMPLETED`，不能写 `NO_EXTERNAL_COMPONENT_FOUND`。

## P2 停止条件

- 发现 P1 与本地事实冲突。
- 发现必须先人工确认的破坏性操作。
- 发现 skills 或 mature component 来源不可验证。
- 需要真实执行才能继续。

P2 遇到 STOP 时输出准备报告，不得包装成 PASS。
