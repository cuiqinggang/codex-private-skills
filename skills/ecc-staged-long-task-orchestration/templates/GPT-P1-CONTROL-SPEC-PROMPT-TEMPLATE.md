# GPT P1 Control Specification Prompt Template

任务：为以下目标创建 P1 control specification，不执行真实任务，不编造本地结果。

```text
task_id:
task_mode: ENDURANCE_VALIDATION | PRODUCTION_WITH_TIME_BUDGET
objective:
scope:
out_of_scope:
forbidden_actions:
base_skill_package:
```

必须包含：四阶段流程、Claude-style 12 层中文说明、P2 非执行要求、Subagent Evidence Gate、claim/acceptance 分离、Final Acceptance、时间策略、P2 必须输出文件。
