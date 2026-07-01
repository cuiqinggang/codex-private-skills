# GPT-STAGE-1-CONTROL-SPECIFICATION

## 目标

GPT P1 负责把用户目标转换为可交给 Codex P2 的详细 control specification。P1 不是最终执行，也不是报告写作。

## 必须写入

```text
use_claude_style_12_layer_compact_core = true
must_clone_original_12_layer = true
must_not_rewrite_as_ordinary_12_steps = true
codex_evidence_return_packet_required = true
gpt_final_acceptance_required = true
```

## P1 必填字段

```text
task_id:
task_mode: ENDURANCE_VALIDATION | PRODUCTION_WITH_TIME_BUDGET
objective:
scope:
out_of_scope:
forbidden_actions:
base_skill_package:
required_claude_style_layers: 12
subagent_required_default:
claim_acceptance_separation:
final_acceptance_required:
time_policy:
p2_required_outputs:
p2_execute_real_task: false
p2_final_pass_allowed: false
```

## P1 的 12 Layer 要求

GPT 生成命令包时必须显式写出 12 Layer。每层使用：

```text
Layer X — 原始英文名
中文名：

本层目的：
本层输入：
本层动作：
本层产物：
本层验证：
失败返回：
证据路径：
本任务中的具体应用：
```

## 禁止事项

- 不得替 Codex 假装读取本地文件。
- 不得把任务写成普通 12 步。
- 不得使用“目标确认 / 现状读取 / 风险识别”等替代原始 12 层。
- 不得直接跳到 final executable package。
- 不得跳过 skills 搜索时机要求。
- 不得跳过 mature component first gate。
- 不得允许 Codex 只返回文件夹路径。
