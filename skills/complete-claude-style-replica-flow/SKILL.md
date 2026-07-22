---
name: complete-claude-style-replica-flow
description: Use when creating, auditing, repairing, or executing Claude-style 12 Layer long-task command packages, GPT-Codex closed-loop plans, ECC-style staged orchestration, independent verification, repair loops, handoff compression, or final acceptance artifacts.
---

# 完整 Claude-style 复刻流程

## Core Rule

Use this skill to preserve the user's Claude-style 12 Layer control system exactly as a long-task governance model. Do not treat it as a generic checklist, a normal 12-step workflow, or a simplified planning template.

Read `references/CLAUDE-STYLE-12-LAYER-DETAILED-CHINESE-GUIDE.md` whenever the task asks to generate, review, fix, package, or execute a Claude-style 12 Layer command pack.

## Required Behavior

- 保留 12 层原始英文名、中文名、顺序、核心作用、边界条件、输入输出、前后层关系和失败条件。
- 不要把 12 Layer 改写成普通 12 步。
- 不要把 `Control Plane / Orchestrator`、`Execution Plane`、`Verification Plane`、`Repair Loop`、`Compact / Handoff`、`Final Acceptance` 改名、合并、压缩或重解释。
- Execution Plane 只能提交 execution claims，不能 self-accept，不能宣布 final PASS。
- Verification Plane 只读 claims、产物和确定性检查结果，负责 accepted / rejected。
- Repair Loop 必须处理 rejected claims，不能把失败包装成 residual risk 后继续 PASS。
- Final Acceptance 必须生成 `final-acceptance.md` 和 `final-acceptance.json`；没有这两个产物就没有 final PASS。

## Workflow

1. Load the detailed guide before drafting or auditing any task package.
2. Check whether the requested work needs the GPT-Codex four-stage loop or can run locally.
3. For each of the 12 layers, require this exact task-package field set:
   `本层目的`, `本层输入`, `本层动作`, `本层产物`, `本层验证`, `失败返回`, `证据路径`, `是否允许跳过`, `本任务中的具体应用`.
4. If a mechanism is no-op for the current task, require a reason, replacement safeguards, and a Verification Plane decision on whether the no-op / exception is accepted.
5. Reject packages or execution reports that omit any layer, collapse execution and verification, skip repair, return only a folder path, or lack final acceptance artifacts.

## Resources

- `references/CLAUDE-STYLE-12-LAYER-DETAILED-CHINESE-GUIDE.md`: complete Chinese source-of-truth guide and layer analysis.
- `scripts/verify-complete-claude-style-replica-flow.mjs`: deterministic structure check for this skill package.

## Status Code

Use this status code when the detailed guide is present and structure validation passes:

```text
CLAUDE_STYLE_12_LAYER_EFFECTIVE_CORE_LOGIC_EXPANDED
```
