# Runbook

Use this runbook when modifying, compressing, or governing a skill package.

## Standard Execution Order

1. 读取目标技能包短入口。
2. 读取目标技能包 source-of-truth map。
3. 判断本次是压缩 / 补规则 / 补脚本 / 做昨日重现 / 做报告归档。
4. 选择模板。
5. 建 Final Completion Contract。
6. 建 Completion Ledger。
7. 每个 gate 生成验证产物。
8. 运行脚本。
9. 生成 final report。
10. 更新目标技能包索引。
11. 运行最终验证。

## Stop Conditions

STOP if:

- target package is missing
- task would modify unrelated workspaces
- secret or production config is involved
- source-of-truth cannot be identified
- verification scripts fail and cannot be repaired
- final PASS would rely only on model self-claim

## Default Loading Rule

Do not read all reports, backups, templates, or unrelated skill packages by default. Use progressive disclosure.
