# MATURE-COMPONENT-FIRST-GATE

本文件是成熟组件优先的上位规则。它覆盖常见功能块的路线选择，不替代四阶段流程、12 层复刻规则、Subagent Evidence Gate 或 Time Gate Policy。

## 适用场景

遇到下列功能时，默认触发：

- website / 网站
- dashboard
- knowledge base / 知识库
- approval queue / 审批队列
- task board / 任务看板
- workflow / 工作流
- documentation site / 文档站
- internal tool / 内部工具

触发后，P1 必须登记：

```text
mature_solution_discovery_required = true
```

## 上位 / 子规则关系

本文件是上位规则。若同一技能包中存在下列文件，它们是子规则，必须交叉引用本文件，不得重复定义另一套冲突流程：

- `EXTERNAL-FUNCTION-BLOCK-REUSE-GATE.md`
- `REUSE-BEFORE-BUILD-RULE.md`
- `FUNCTION-BLOCK-ADAPTATION-WORKFLOW.md`
- `MATURE-SOLUTION-FIRST-GATE.md`

如果这些子规则不存在，不要为了补丁制造重复文件。由本文件统一承载成熟组件优先规则。

## 四级搜索顺序

常见功能默认先找成熟组件和外部功能块，再考虑自研。四级搜索顺序为：

1. 本地技能与本地历史资产：当前任务目录、当前技能包、`H:\AI\skills` 的关键词窄搜索、`H:\CodexSkills`、`H:\Hermes_Skills`。
2. Hermes 技能路径：先检查 `C:\Users\A\.hermes\skills` 和 `C:\Users\A\.hermes\skills-archive` 是否存在；不存在时记录 `HERMES_SKILL_PATH_NOT_FOUND`，不得假装已搜索。
3. 外部成熟组件：GitHub、npm、Docker Hub、官方文档、模板市场、平台示例。
4. 轻量自研：只有找不到、不能用、风险太高、许可证不合适、维护成本过高或本地约束不允许时，才允许最小自研。

## 默认路线优先级

P2 / P3 / P4 必须使用同一优先级：

```text
ADOPT_DIRECTLY > ADAPT_LIGHTLY > TRY_LIGHTLY > REFERENCE_ONLY > BUILD_FROM_SCRATCH
```

含义：

- `ADOPT_DIRECTLY`：直接采用成熟组件或模板。
- `ADAPT_LIGHTLY`：轻量适配成熟组件。
- `TRY_LIGHTLY`：小范围试跑或 demo 验证，不承诺生产采用。
- `REFERENCE_ONLY`：只借鉴结构、交互、数据模型或验证策略。
- `BUILD_FROM_SCRATCH`：最小自研。

如果选择自研，必须写：

```text
NO_MATURE_COMPONENT_FOUND_REASON
```

理由必须具体到来源、风险、不可用点或约束，不能只写“没找到”。

## 外部搜索状态

外部成熟组件搜索必须区分三种状态：

- `EXTERNAL_COMPONENT_SEARCH_COMPLETED`：确实完成 GitHub / npm / Docker Hub / 官方文档 / 模板 / 平台搜索。
- `EXTERNAL_COMPONENT_SEARCH_PARTIAL`：只完成部分来源搜索。
- `EXTERNAL_COMPONENT_SEARCH_NOT_COMPLETED`：没有联网、工具不可用、权限不允许或任务明确禁止外部搜索。

没有外部搜索能力时，不能写 `NO_EXTERNAL_COMPONENT_FOUND`，只能写：

```text
EXTERNAL_SEARCH_NOT_COMPLETED
```

只有在外部搜索完成后，才允许写 `NO_EXTERNAL_COMPONENT_FOUND`。

## P2 要求

P2 准备阶段必须：

- 在 `revised-task-package.md` 和 `gap-analysis.md` 之后执行成熟组件搜索。
- 检查 Hermes 两个候选路径存在性。
- 记录本地技能、Hermes 活跃技能、Hermes 归档技能、GitHub、npm、Docker Hub、官方文档、模板、平台示例的搜索状态。
- 输出采用路线：`ADOPT_DIRECTLY`、`ADAPT_LIGHTLY`、`TRY_LIGHTLY`、`REFERENCE_ONLY` 或 `BUILD_FROM_SCRATCH`。
- 自研时写 `NO_MATURE_COMPONENT_FOUND_REASON`。

## P3 要求

P3 最终整合必须比较三条路线：

- 直接采用
- 轻量适配
- 自研

整合结果必须说明为什么选择当前路线，以及为什么没有选择其他路线。

## P4 要求

P4 执行时必须区分：

- 外部 demo：来自外部组件、模板、平台示例或文档的演示结果。
- 本地实际成果：在本机目标目录生成、运行或验证过的实际产物。

外部 demo 不能冒充本地实际成果。本地 PASS 必须有本地产物和本地验证证据。
