# RUNBOOK

## G00：确认任务类型

- `ENDURANCE_VALIDATION`：验证 2H/8H 长时间执行能力，必须跑满最低时间。
- `PRODUCTION_WITH_TIME_BUDGET`：真实生产或 mature skill replay，完成 gates 即停止，不强制耗满时间。

## G01：读取 12 Layer 核心规则

先读取：

```text
CLAUDE-STYLE-12-LAYER-COMPACT-CORE.md
DO-NOT-REWRITE-12-LAYER-RULE.md
TASK-PACKAGE-MUST-CLONE-12-LAYER.md
CLAUDE-12-LAYER-FAILURE-LESSONS-PATCH-20260622.md
```

确认：

- 12 Layer 不是普通 12 步。
- 不能改名、不能压缩、不能重解释。
- 每层必须有中文名、核心作用、边界、连接关系、失败条件。
- 必须启用中文可审计输出，禁止纯英文计划、纯英文纠错和纯英文验收。
- 必须同时防止提前结束型假完成和纯耗时间型假执行。
- 每个阶段必须有产物、证据、最大时间、最大重试和失败跳转。

## G02：GPT-Codex 闭环

读取：

```text
GPT-CODEX-12-LAYER-CLOSED-LOOP-RUNBOOK.md
CODEX-EVIDENCE-RETURN-PACKET-RULE.md
```

默认流程：

```text
用户任务 -> Codex 收集上下文 -> GPT 生成 12 Layer 命令包 -> Codex 执行并收集证据 -> Codex 回传证据包 -> GPT 最终验收 -> Codex 归档、返修或停止。
```

## G03：P1 GPT 总控细化设计

GPT 只输出详细 control specification，不直接伪造本地文件结构。GPT 生成命令包时必须显式写出 12 Layer。

## G04：P2 Codex 准备，不执行真实任务

P2 必须生成草案、gap analysis、missing hard gates、failure-mode review、revised task package、skills / mature component 准备结果。

硬条件：

```text
execute_real_task = false
```

## G05：P3 GPT 最终整合

GPT 读取 P2 输出，整合成：

```text
FINAL-EXECUTABLE-TASK-PACKAGE
```

命令包必须使用 `TASK-PACKAGE-MUST-CLONE-12-LAYER.md` 的固定格式。

## G06：P4 Codex 正式执行

P4 输出：

```text
execution-claims.md
artifact-manifest.md
script-verification-result.md
independent-verification.md
claim-acceptance-matrix.md
repair-loop-log.md
compact-handoff.md
final-acceptance.md
final-acceptance.json
final-report.md
```

P4 还必须遵守 2026-06-22 失败教训补丁：

```text
NO_EARLY_EXIT：未达到命令包声明的最低运行时间，不得 final PASS。
NO_TIME_ONLY_LOOP：只写 elapsed time / heartbeat / waiting，不算执行。
NO_INFINITE_LOOP：单个子任务超过时间盒或重试次数，必须记录并跳转。
EVIDENCE_BEFORE_ACCEPTANCE：没有文件级、命令级、agent 级证据，不能验收。
CHINESE_AUDITABLE_OUTPUT：错误、修复、验收必须中文优先，英文术语必须有中文解释。
```

## G08: T8H / long-runtime recovery rules

For 4H/8H or longer official execution, read:

```text
ENDURANCE-LADDER-SYSTEM-INDEX-20260613.md
FAILURE-HISTORY-20260613-T8H-RECOVERY-MODE.md
T8H-CONTINUOUS-RUNTIME-AND-RECOVERY-RULE.md
LAYER5-SUBAGENT-EVIDENCE-MODE-RULE.md
T8H-EVIDENCE-ALIAS-AND-FINAL-ACCEPTANCE-ADDENDUM-RULE.md
```

Hard gates:

```text
Time gate is not runtime driver.
minimum_elapsed_minutes prevents early PASS, but does not ensure continuous execution.
CONTINUOUS_RUNTIME_UNTIL_T8H_OR_BLOCKED must be explicit.
PARTIAL_STARTED is not a valid stop state before T+8h.
Late recovery checkpoints are acceptable only when disclosed and verified.
Forged checkpoint timestamps are fatal.
Layer 5 evidence mode must be explicit.
Codex return packet must not be path-only and should request GPT final acceptance.
```

Codex 不能只返回文件夹路径，必须按 `CODEX-EVIDENCE-RETURN-PACKET-RULE.md` 回传核心证据摘要。

## G07：最终验收

只有以下全部成立才允许 final PASS：

1. Execution claims 完整。
2. Verification Plane 接受关键 claims。
3. Repair Loop 处理所有 rejection。
4. Artifact manifest 完整。
5. Deterministic checks 通过。
6. `final-acceptance.md` 存在。
7. `final-acceptance.json` 可解析且 `final_pass=true`。
8. Final acceptance 中列出的硬门槛全部为 true。

## STOP 条件

- 把 12 Layer 改成普通 12 步。
- 使用“目标确认 / 现状读取 / 风险识别”等替代原始 12 层。
- Execution Plane 自己宣布 final PASS。
- Verification Plane 缺失。
- Repair Loop 缺失。
- Final Acceptance 缺失。
- Codex 只返回文件夹路径。
- checkpoint 只记录时间或 heartbeat，没有产物变化。
- 多智能体只有口头描述，没有独立上下文、独立文件和独立证据。
- claim acceptance matrix 或修复计划只有英文，用户无法审计。
## Claude Code 12 Layer 中文详细执行标准

复杂长任务、2H / 8H endurance validation、SkillOpt、Run Guard 和 T8H official run 必须读取：

```text
CLAUDE-CODE-12-LAYER-DETAILED-CHINESE-EXECUTION-STANDARD.md
```

该文件规定每层中文详细操作、文件要求、内容要求、禁止项、时间门槛、多智能体 / 上下文隔离要求、Verification Plane 接受条件和失败返回。

## Runtime Gate Hard Standard

运行时长任务必须读取：

```text
RUNTIME-GATE-HARD-STANDARD.md
RUNTIME-EVIDENCE-SCHEMA.json
scripts/verify-runtime-gate.mjs
```

任务名称、TASK_ID 或命令包包含 2H、4H、8H、long-task、endurance、runtime、continuous runtime、长任务、两小时、四小时、八小时时，必须输出 `outputs/runtime-evidence.json` 和 `checkpoint-timeline.html`，并通过 runtime verifier。

补丁安装任务可以快速 PASS，但只能是 `PATCH_INSTALL_PASS`；不得声明 `2H_RUNTIME_PASS`。
