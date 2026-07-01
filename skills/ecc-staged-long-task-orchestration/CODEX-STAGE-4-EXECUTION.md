# CODEX-STAGE-4-EXECUTION

## 目标

Codex P4 执行 P3 最终可执行任务包。P4 是唯一真实执行阶段，但不能自我验收。

## 必须输出

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

## Claim / Acceptance 分离

- Execution Plane 只能 claim，不能 self-accept。
- Execution Plane 只能说做了什么、改了哪些文件、运行了哪些命令、生成了哪些证据。
- Verification Plane 负责 acceptance / rejection。
- claim 不能自动变成 acceptance。
- final report 不能替代 final acceptance。

## Codex 回传包

Codex 执行完成后必须按 `CODEX-EVIDENCE-RETURN-PACKET-RULE.md` 回传：

- 任务名称；
- 工作区路径；
- 使用的技能包；
- Claude-style 12 Layer 执行摘要；
- Layer 1 到 Layer 12 每层状态；
- Execution Plane claims；
- Scripts / Deterministic Checks 输出；
- Verification Plane acceptance / rejection；
- Repair Loop 记录；
- Compact / Handoff 摘要；
- final-acceptance.md 核心内容；
- final-acceptance.json 核心内容；
- 最终状态码；
- 仍然存在的问题；
- 请求 GPT 最终验收。

硬规则：

```text
只返回文件夹路径 = FAIL。
只返回“已完成” = FAIL。
没有核心证据摘要 = FAIL。
```

## Repair Loop

如果 Verification Plane rejection：

1. 定位失败层。
2. 返回对应层修复。
3. 记录 repair-loop-log。
4. 重新运行 deterministic checks。
5. 重新请求 verification。

Repair Loop 处理 rejected claims。不得把失败描述成 residual risk 后继续 PASS。

## Final Acceptance

Final Acceptance 才是最终 PASS 权威。没有 final acceptance，没有 final PASS。
