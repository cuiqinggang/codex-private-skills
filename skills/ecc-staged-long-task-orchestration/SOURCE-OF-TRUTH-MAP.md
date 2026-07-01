# SOURCE-OF-TRUTH-MAP

## 主 source-of-truth

| 文件 | 权威范围 |
| --- | --- |
| `CLAUDE-STYLE-12-LAYER-COMPACT-CORE.md` | 12 Layer 简洁核心思想版 |
| `DO-NOT-REWRITE-12-LAYER-RULE.md` | 禁止改名、压缩、重解释、普通 12 步替换 |
| `TASK-PACKAGE-MUST-CLONE-12-LAYER.md` | 长任务命令包固定格式 |
| `GPT-CODEX-12-LAYER-CLOSED-LOOP-RUNBOOK.md` | GPT-Codex 桌面端闭环执行流程 |
| `CODEX-EVIDENCE-RETURN-PACKET-RULE.md` | Codex 执行回传包规则 |
| `FOUR-STAGE-WORKFLOW.md` | GPT/Codex 四阶段协作主流程 |
| `CLAUDE-STYLE-12-LAYER-REPLICA-RULE.md` | 12 层复刻规则 |
| `SUBAGENT-EVIDENCE-GATE.md` | L4/L5 子智能体硬门槛与证据字段 |
| `TIME-GATE-POLICY.md` | Endurance 与 production 时间策略分界 |
| `MATURE-COMPONENT-FIRST-GATE.md` | 常见功能成熟组件优先与四级搜索顺序 |
| `SKILL-SEARCH-AND-PREPARATION.md` | skills / mature component 搜索发生时机、范围、输出格式 |
| `CLAUDE-12-LAYER-FAILURE-LESSONS-PATCH-20260622.md` | 实际 SuperTool 部署错误复盘形成的 12 Layer 失败教训补丁：中文可审计输出、禁止提前结束、禁止纯耗时间型假执行、禁止单点死循环、多智能体证据、模型路由完整性、动作级证据和最终目标对齐 |
| `STATUS-CODES.md` | 状态码词典 |
| `MANIFEST.md` | 文件清单与验证边界 |

## 阶段文件

| 阶段 | 文件 |
| --- | --- |
| P1 | `GPT-STAGE-1-CONTROL-SPECIFICATION.md` |
| P2 | `CODEX-STAGE-2-PREPARATION.md` |
| P3 | `GPT-STAGE-3-FINAL-INTEGRATION.md` |
| P4 | `CODEX-STAGE-4-EXECUTION.md` |

## 验证 source-of-truth

`scripts/verify-staged-long-task-skill.mjs` 是本技能包结构和硬规则的确定性检查入口。

补丁验收报告在：

```text
reports/12-layer-compact-core-flow-patch-20260529/
reports/failure-lessons-patch-20260622/
```
## Claude Code 12 Layer 中文详细执行标准

`CLAUDE-CODE-12-LAYER-DETAILED-CHINESE-EXECUTION-STANDARD.md`

权威范围：

Claude Code / Claude-style 12 Layer 的中文详细操作、文件要求、内容要求、禁止项、时间门槛、多智能体验证要求、Verification Plane 接受条件、Final Acceptance 条件。

适用任务：

2H endurance validation、8H endurance validation、SkillOpt 长任务、Run Guard、T8H official run、复杂 Codex 工程任务。

## Runtime Gate Hard Standard

`RUNTIME-GATE-HARD-STANDARD.md`

权威范围：

2H / 4H / 8H / long-task / endurance / runtime / continuous runtime / 长任务 的真实运行时间门槛、checkpoint 数量、runtime evidence 字段、PASS/FAIL 规则。

配套文件：

```text
RUNTIME-EVIDENCE-SCHEMA.json
scripts/verify-runtime-gate.mjs
```

## 2026-06-22 Claude 12 Layer 失败教训补丁

`CLAUDE-12-LAYER-FAILURE-LESSONS-PATCH-20260622.md`

权威范围：

来自实际 SuperTool 部署错误的长任务反复盘规则，包括中文可审计输出、禁止提前结束、禁止纯耗时间型假执行、禁止单子任务无限循环、阶段产物推进、多智能体独立证据、模型路由完整性、动作级证据、可视化执行真实、Final Acceptance 最终验收权威。

适用任务：

2H / 4H / 8H / SuperTool / Cursor / Kilo / Codex / Claude Code 长任务，以及任何需要 checkpoint、handoff、Verification Plane、Repair Loop、Final Acceptance 的复杂编排任务。
