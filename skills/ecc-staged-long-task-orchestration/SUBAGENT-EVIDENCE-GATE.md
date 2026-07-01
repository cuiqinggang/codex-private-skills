# SUBAGENT-EVIDENCE-GATE

## 定位

Subagents / Context Isolation 是 Claude-style Layer 5。对于 L4-2H、L5、多阶段、多文件、skills 搜索、独立审计任务，它是硬阻断门槛。

## 默认规则

```text
L4/L5 default: subagent_required = true
```

如果不使用 subagent，必须提供 Verification Plane 接受的 `no-subagent exception`。否则 Layer 5 = FAIL。

## 必需证据字段

```text
subagent assignment plan
per-subagent input scope
per-subagent forbidden scope
per-subagent output summary
start_time / end_time
files_read
files_written
evidence_paths
orchestrator receipt log
independent verification acceptance
```

## 建议证据目录

```text
reports/<task-id>/subagents/
  subagent-assignment-plan.md
  research-subagent-input.md
  research-subagent-output.md
  builder-subagent-input.md
  builder-subagent-output.md
  verifier-subagent-input.md
  verifier-subagent-output.md
  subagent-summary-index.md
  orchestrator-receipt-log.md
  subagent-evidence-verification.md
```

## 阻断规则

- 如果声称使用 subagent 但没有证据，视为未使用。
- 如果没有 subagent 证据，也没有 accepted no-subagent exception，Layer 5 = FAIL。
- 如果 Layer 5 FAIL，不能进入 final acceptance。
- Subagent 不等于 Verification Plane，不等于 final acceptance。
- Orchestrator 必须记录 receipt log，证明已经收到并整合 subagent 输出。
