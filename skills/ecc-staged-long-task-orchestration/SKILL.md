---
name: ecc-staged-long-task-orchestration
description: Use when orchestrating ECC/Codex staged long tasks, L4/L5 endurance validation, mature skill replay, complex Codex engineering tasks, GPT-Codex desktop closed loops, mature component discovery, or multi-stage multi-file verification work.
---

# ecc-staged-long-task-orchestration

这是 `ecc-endurance-ladder-unified` 的上层长任务编排技能包，不替代统一 ECC 技能包。它沉淀 GPT / Codex / Claude-style 复杂长任务的四阶段协作方法和 12 Layer 控制系统。

## 必读顺序

1. `CLAUDE-STYLE-12-LAYER-COMPACT-CORE.md`
2. `DO-NOT-REWRITE-12-LAYER-RULE.md`
3. `GPT-CODEX-12-LAYER-CLOSED-LOOP-RUNBOOK.md`
4. `TASK-PACKAGE-MUST-CLONE-12-LAYER.md`
5. `CODEX-EVIDENCE-RETURN-PACKET-RULE.md`
6. `CLAUDE-12-LAYER-FAILURE-LESSONS-PATCH-20260622.md`
7. 按任务阶段读取 P1 / P2 / P3 / P4 文件。
8. When the task mentions ECC 2.0, cross-harness work, MCP inventory,
   worktree lifecycle, control-pane, or `orch-*`, also read
   `ECC-2.0-CROSS-HARNESS-12L-PATCH-20260706.md`.

## ECC 2.0 read-only absorption

`ECC-2.0-CROSS-HARNESS-12L-PATCH-20260706.md` maps ECC v2.0.0
control-pane/session snapshots, MCP inventory, worktree lifecycle, and `orch-*`
operation routing into the existing 12 Layer system. It is a reference-only
patch: it does not approve installing ECC, copying hooks, changing MCP configs,
or modifying global Claude Code / Codex / Cursor settings.

## 四阶段

1. P1 GPT 总控细化设计：输出 detailed control specification。
2. P2 Codex 准备阶段，不执行真实任务：输出草案、gap audit、修正版任务包、skills / mature component 准备。
3. P3 GPT 最终整合：整合 P2 产物与 skills / mature component 补充，输出最终可执行任务包。
4. P4 Codex 正式执行：claim / acceptance / repair / final-acceptance 闭环。

## 12 Layer 硬规则

- Claude-style 12 Layer 不是普通 12 步。
- 不能改成普通 12 步。
- 不能改名、不能压缩、不能重解释。
- 不能用“目标确认 / 现状读取 / 风险识别 / 小步实现 / 回归验证”替代原始 12 层。
- 每个长任务命令包必须显式写出 12 个原始英文层名、中文名、目的、输入、动作、产物、验证、失败返回、证据路径和本任务中的具体应用。
- Execution Plane 只能 claim，不能 self-accept。
- Verification Plane 负责 acceptance / rejection。
- Repair Loop 处理 rejected claims。
- Final Acceptance 才是最终 PASS 权威；没有 final acceptance，没有 final PASS。
- Codex 不能只返回文件夹路径。

## GPT-Codex 闭环

默认执行方式：

```text
Codex 收集任务上下文 -> GPT 生成 Claude-style 12 Layer 命令包 -> Codex 执行并收集证据 -> Codex 回传证据包 -> GPT 做 Verification Plane / Final Acceptance -> Codex 归档、返修或停止。
```

## 适用场景

适用于 L4/L5、2H/8H、多文件、多阶段、skills 搜索、成熟组件发现、成熟路线复用、独立验证、GPT-Codex 桌面端闭环执行的 ECC / Codex 长任务。

## 成熟组件优先

遇到网站、dashboard、知识库、审批队列、任务看板、工作流、文档站、内部工具时，先加载 `MATURE-COMPONENT-FIRST-GATE.md`。

默认路线顺序：

```text
ADOPT_DIRECTLY > ADAPT_LIGHTLY > TRY_LIGHTLY > REFERENCE_ONLY > BUILD_FROM_SCRATCH
```

自研必须写 `NO_MATURE_COMPONENT_FOUND_REASON`。

## 成功状态码

```text
ECC_STAGED_LONG_TASK_ORCHESTRATION_SKILL_CREATED
ECC_FOUR_STAGE_GPT_CODEX_WORKFLOW_READY
ECC_SUBAGENT_EVIDENCE_GATE_INSTALLED
ECC_TIME_GATE_POLICY_INSTALLED
ECC_SKILL_SEARCH_AFTER_REVISED_DRAFT_RULE_READY
ECC_MATURE_COMPONENT_FIRST_GATE_INSTALLED
ECC_STAGED_LONG_TASK_12_LAYER_COMPACT_CORE_FLOW_PATCH_PASS
```

## 8H recovery-mode lessons

For any 4H/8H or longer long-running coding task, read these before P4 official execution:

```text
ENDURANCE-LADDER-SYSTEM-INDEX-20260613.md
FAILURE-HISTORY-20260613-T8H-RECOVERY-MODE.md
T8H-CONTINUOUS-RUNTIME-AND-RECOVERY-RULE.md
LAYER5-SUBAGENT-EVIDENCE-MODE-RULE.md
T8H-EVIDENCE-ALIAS-AND-FINAL-ACCEPTANCE-ADDENDUM-RULE.md
```

Core lesson:

```text
minimum_elapsed_minutes is only a time gate, not a runtime driver.
T8H official execution requires CONTINUOUS_RUNTIME_UNTIL_T8H_OR_BLOCKED,
explicit Layer 5 evidence mode, honest recovery checkpoints, Verification Plane,
Repair Loop, Final Acceptance, and non-path-only evidence return.
```

## 2026-06-22 failure lessons patch

任何 2H / 4H / 8H / SuperTool / Cursor / Kilo / Codex / Claude Code 长任务，尤其是涉及实际部署、模型路由、多智能体、checkpoint、handoff、Final Acceptance 的任务，必须读取：

```text
CLAUDE-12-LAYER-FAILURE-LESSONS-PATCH-20260622.md
```

核心硬规则：

```text
CHINESE_AUDITABLE_OUTPUT = true
NO_ENGLISH_ONLY_PLAN = true
CHINESE_EXPLANATION_REQUIRED = true
NO_EARLY_EXIT = true
NO_TIME_ONLY_LOOP = true
NO_INFINITE_LOOP = true
REAL_WORK_EVIDENCE_REQUIRED = true
MULTI_AGENT_EVIDENCE_REQUIRED = true
FINAL_TARGET_ALIGNMENT_REQUIRED = true
```

这份补丁来自实际 SuperTool 部署错误复盘。后续长任务不得重复以下错误：提前结束、纯耗时间型假执行、单点死循环、多智能体口头化、模型路由漂移、只给文件夹或报告、不提供动作级证据、英文纠错不可审计。

如果命令包或执行报告只写英文状态码而没有中文解释，或者 checkpoint 只记录 elapsed time / heartbeat 而没有产物变化，Verification Plane 必须拒绝该轮声明，并进入 Repair Loop。
## Claude Code 12 Layer 中文详细执行标准

复杂长任务、2H / 8H endurance validation、SkillOpt、Run Guard 和 T8H official run 必须读取：

`CLAUDE-CODE-12-LAYER-DETAILED-CHINESE-EXECUTION-STANDARD.md`

该文件是 12 Layer 的中文详细操作标准，规定每层的目的、输入、动作、产物、文件要求、内容要求、禁止项、时间门槛、多智能体验证、Verification Plane 接受条件和失败返回。

不得只列 12 个标题。
不得把 12 Layer 改写成普通 12 步。

## Runtime Gate Hard Standard

任何 2H / 4H / 8H / long-task / endurance / runtime / continuous runtime / 长任务 / 两小时 / 四小时 / 八小时任务，必须启用：

```text
RUNTIME-GATE-HARD-STANDARD.md
RUNTIME-EVIDENCE-SCHEMA.json
scripts/verify-runtime-gate.mjs
```

补丁安装任务可以几分钟完成，但只能声明 `PATCH_INSTALL_PASS`。运行时长任务必须真实达到 minimum runtime 和 checkpoint 要求；2H 任务 6 分钟完成时，`FINAL_STATUS = PASS` 被禁止。
