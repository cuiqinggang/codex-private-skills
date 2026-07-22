# ECC Staged Long Task Orchestration

本技能包保存一套稳定的复杂长任务组织方法：

```text
GPT 先做详细总控设计；
Codex 做准备和本地证据收集但不擅自执行；
GPT 整合最终可执行命令包；
Codex 执行并回传证据；
GPT / Verification Plane / Final Acceptance 做最终验收。
```

## 核心更新

本包现在正式包含：

- `CLAUDE-STYLE-12-LAYER-COMPACT-CORE.md`：Claude-style 12 Layer 简洁核心思想版。
- `GPT-CODEX-12-LAYER-CLOSED-LOOP-RUNBOOK.md`：GPT-Codex 桌面端闭环执行流程。
- `TASK-PACKAGE-MUST-CLONE-12-LAYER.md`：命令包必须克隆 12 Layer 的固定格式。
- `CODEX-EVIDENCE-RETURN-PACKET-RULE.md`：Codex 执行回传包规则。
- `DO-NOT-REWRITE-12-LAYER-RULE.md`：禁止改写 12 Layer 的硬规则。

## 关键边界

- 12 Layer 不是普通 12 步。
- 不能改名、不能压缩、不能重解释。
- Execution Plane 只能 claim，不能 self-accept。
- Verification Plane 负责 acceptance / rejection。
- Repair Loop 处理 rejected claims。
- Final Acceptance 才是最终 PASS 权威。
- Codex 不能只返回文件夹路径。

## 目录结构

```text
ecc-staged-long-task-orchestration/
  SKILL.md
  README.md
  RUNBOOK.md
  SOURCE-OF-TRUTH-MAP.md
  FOUR-STAGE-WORKFLOW.md
  CLAUDE-STYLE-12-LAYER-COMPACT-CORE.md
  GPT-CODEX-12-LAYER-CLOSED-LOOP-RUNBOOK.md
  TASK-PACKAGE-MUST-CLONE-12-LAYER.md
  CODEX-EVIDENCE-RETURN-PACKET-RULE.md
  DO-NOT-REWRITE-12-LAYER-RULE.md
  templates/
  scripts/
  reports/
```

## 验证

在技能包根目录运行：

```powershell
node .\scripts\verify-staged-long-task-skill.mjs --write-report
```

通过后应看到：

```text
VERIFICATION_PASS
ECC_STAGED_LONG_TASK_12_LAYER_COMPACT_CORE_FLOW_PATCH_PASS
```
