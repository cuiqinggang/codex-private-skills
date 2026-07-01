# FOUR-STAGE-WORKFLOW

## 总规则

复杂 ECC / Codex 长任务不得从“目标”直接跳到“执行”。必须走完整四阶段：

```text
P1：GPT 总控细化设计
P2：Codex 准备阶段，不执行
P3：GPT 最终整合
P4：Codex 正式执行
```

四阶段必须使用 Claude-style 12 Layer 原始结构。12 Layer 不能改成普通 12 步，不能改名、不能压缩、不能重解释。

## P1：GPT 总控细化设计

GPT 输出 control specification，并显式要求：

- 使用 `CLAUDE-STYLE-12-LAYER-COMPACT-CORE.md`。
- 使用 `TASK-PACKAGE-MUST-CLONE-12-LAYER.md` 的固定格式。
- 使用 `GPT-CODEX-12-LAYER-CLOSED-LOOP-RUNBOOK.md` 的闭环流程。
- Codex 不能只返回文件夹路径。

## P2：Codex 准备阶段，不执行

Codex 只做准备，不执行真实任务。P2 产物包括 draft、gap analysis、missing hard gates、failure mode review、revised task package、skills / mature component supplement。

## P3：GPT 最终整合

GPT 读取 P2 产物，输出 `FINAL-EXECUTABLE-TASK-PACKAGE`。P3 必须显式写出 Layer 1 到 Layer 12，每层使用固定格式。

## P4：Codex 正式执行

Codex 执行 P3 命令包，收集每层证据，并按 `CODEX-EVIDENCE-RETURN-PACKET-RULE.md` 回传。

关键要求：Codex 回传证据包，不能只返回文件夹路径。

P4 不能在 GPT 未验收前宣布最终完成。

## 闭环验收

GPT 根据 Layer 9 Verification Plane 和 Layer 12 Final Acceptance 做最终验收。Codex 根据 GPT 结论归档、修复或停止。
