# GPT-STAGE-3-FINAL-INTEGRATION

## 目标

GPT P3 读取 Codex P2 的准备产物，整合出最终可执行任务包。

## 必须读取的 P2 产物

```text
revised-task-package.md
gap-analysis.md
missing-hard-gates.md
failure-mode-review.md
skill-candidate-index.md
mature-path-index.md
skill-reuse-decision.md
skills-install-or-prepare-log.md
skills-integration-supplement.md
```

## P3 整合规则

- 必须读取 `CLAUDE-STYLE-12-LAYER-COMPACT-CORE.md`。
- 必须读取 `TASK-PACKAGE-MUST-CLONE-12-LAYER.md`。
- 必须读取 `DO-NOT-REWRITE-12-LAYER-RULE.md`。
- 必须输出 `FINAL-EXECUTABLE-TASK-PACKAGE`。
- 最终包必须显式写出 12 个原始英文层名和中文名。
- 不能把 12 Layer 改成普通 12 步。
- 不能改名、不能压缩、不能重解释。

## 成熟组件路线比较

P3 必须读取 `MATURE-COMPONENT-FIRST-GATE.md`，并比较三条路线：

- 直接采用
- 轻量适配
- 自研

如果最终选择自研，必须写 `NO_MATURE_COMPONENT_FOUND_REASON`。

## P3 输出格式

```text
FINAL-EXECUTABLE-TASK-PACKAGE
1. task_id
2. task_mode
3. objective
4. forbidden_actions
5. required_artifacts
6. mature component route comparison
7. Claude-style 12 Layer command pack
8. subagent evidence gate
9. deterministic checks
10. bad-case tests
11. claim/acceptance separation
12. repair loop
13. final acceptance criteria
14. Codex evidence return packet requirement
```
