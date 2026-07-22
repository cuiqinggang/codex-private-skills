# GPT P3 Final Executable Task Package Template

## FINAL-EXECUTABLE-TASK-PACKAGE

```text
task_id:
task_mode:
objective:
forbidden_actions:
required_artifacts:
```

## Claude-style 12 layers

逐层列出 Layer 1 到 Layer 12，每层必须包含中文名、执行位置、产物、验证方法、失败返回。

## Hard gates

- Subagent Evidence Gate
- Script / deterministic checks
- Bad-case tests
- Claim / Acceptance separation
- Repair Loop
- Final Acceptance

## Final PASS criteria

没有 final-acceptance.md / final-acceptance.json，不允许 final PASS。
