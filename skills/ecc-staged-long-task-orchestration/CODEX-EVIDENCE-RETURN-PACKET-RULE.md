# Codex Evidence Return Packet Rule

Codex 执行完成后，不能只返回路径。

必须返回：

```text
1. 任务名称；
2. 工作区路径；
3. 使用的技能包；
4. Claude-style 12 Layer 执行摘要；
5. Layer 1 到 Layer 12 每层状态；
6. Execution Plane claims；
7. Scripts / Deterministic Checks 输出；
8. Verification Plane acceptance / rejection；
9. Repair Loop 记录；
10. Compact / Handoff 摘要；
11. final-acceptance.md 核心内容；
12. final-acceptance.json 核心内容；
13. 最终状态码；
14. 仍然存在的问题；
15. 请求 GPT 最终验收。
```

硬规则：

```text
只返回文件夹路径 = FAIL。
只返回“已完成” = FAIL。
没有核心证据摘要 = FAIL。
```

## 最小合格回传结构

```text
TASK_ID:
Workspace:
Skills used:
12 Layer status:
Execution claims:
Deterministic checks:
Verification Plane result:
Repair Loop:
Handoff:
Final acceptance md summary:
Final acceptance json summary:
Final status codes:
Open issues:
Request GPT final acceptance: YES
```
