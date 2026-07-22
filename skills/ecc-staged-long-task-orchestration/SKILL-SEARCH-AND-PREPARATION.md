# SKILL-SEARCH-AND-PREPARATION

## 总规则

Skills 搜索和成熟组件搜索不能太早。必须在 Codex P2 生成下列材料之后再搜索：

```text
revised-task-package.md
gap-analysis.md
missing-hard-gates.md
failure-mode-review.md
verification requirements
```

也就是说，搜索发生在 `revised-task-package.md` 和 `gap-analysis.md` 之后。

## 搜索范围

必须按任务关键词窄搜索，不得全量盲扫：

```text
本地技能：当前任务目录内已有 skills、当前技能包、H:\AI\skills 关键词窄搜索、H:\CodexSkills、H:\Hermes_Skills
${REDACTED_SECRET}
${REDACTED_SECRET}
GitHub
npm
Docker Hub
官方文档
模板市场
平台示例
```

Hermes 技能路径必须先检查存在性。候选路径：

```text
${REDACTED_SECRET}
${REDACTED_SECRET}
```

如果路径不存在，记录：

```text
HERMES_SKILL_PATH_NOT_FOUND
```

不得假装已经搜索不存在的 Hermes 路径。

## 成熟组件优先

常见功能默认读取 `MATURE-COMPONENT-FIRST-GATE.md`，并使用：

```text
ADOPT_DIRECTLY > ADAPT_LIGHTLY > TRY_LIGHTLY > REFERENCE_ONLY > BUILD_FROM_SCRATCH
```

自研必须包含：

```text
NO_MATURE_COMPONENT_FOUND_REASON
```

## 外部搜索状态

外部成熟组件搜索必须写明状态：

```text
EXTERNAL_COMPONENT_SEARCH_COMPLETED
EXTERNAL_COMPONENT_SEARCH_PARTIAL
EXTERNAL_COMPONENT_SEARCH_NOT_COMPLETED
```

没有外部搜索能力时，不能写 `NO_EXTERNAL_COMPONENT_FOUND`，只能写：

```text
EXTERNAL_SEARCH_NOT_COMPLETED
```

只有确实完成 GitHub / npm / Docker Hub / 官方文档 / 模板 / 平台搜索后，才允许写 `NO_EXTERNAL_COMPONENT_FOUND`。

## 输出文件

```text
skill-candidate-index.md
mature-path-index.md
skill-reuse-decision.md
skills-install-or-prepare-log.md
skills-integration-supplement.md
```

## 如果找到 skill 或 mature component

必须记录：

1. 本地路径或来源。
2. 验证可读证据。
3. 加入哪一层或哪一阶段。
4. 解决哪个缺口。
5. 是否引入冲突。
6. 是否需要额外安装、联网或生产配置变更。
7. 采用路线：`ADOPT_DIRECTLY`、`ADAPT_LIGHTLY`、`TRY_LIGHTLY`、`REFERENCE_ONLY` 或 `BUILD_FROM_SCRATCH`。

## 如果找不到 skill

输出：

```text
NO_MATCHING_SKILL_FOUND
fallback_to_revised_task_package
```

不得因为没找到 skill 而放弃任务；但必须明确未复用 mature path 的风险与补偿验证。
