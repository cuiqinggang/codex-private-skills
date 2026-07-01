# Failure Pattern Catalog

## 1. Rule Written But Not Verified

- symptom（症状 / 现象）: Rule exists in docs, but final PASS has no evidence.
- root cause（根因）: Documentation was treated as enforcement.
- blocking rule（阻断规则）: Hard rule must be verified.
- required fix（修复方法）: Add script or deterministic checklist.
- verification（怎么验证）: Run script and cite output.

## 2. Role Labels Without Independent Reports

- symptom: Multi-agent roles are named but no independent reports exist.
- root cause: Role label substituted for evidence.
- blocking rule: Role label is not agent evidence.
- required fix: Require per-agent report and evidence path.
- verification: verify-multi-agent-evidence or deterministic report checklist.

## 3. Gate PASS Without Verification Artifact

- symptom: Gxx_PASS is emitted without Gxx verification output.
- root cause: Gate completion relied on model self-claim.
- blocking rule: Gate PASS requires verification artifact.
- required fix: Add per-gate verification artifact.
- verification: verify-stage-gates.

## 4. Test/Build PASS Treated As Task PASS

- symptom: tests/build pass, final PASS emitted.
- root cause: Narrow command success confused with objective closure.
- blocking rule: Test PASS is not Task PASS.
- required fix: Completion Ledger and final objective coverage review.
- verification: verify-completion-ledger and final verification.

## 5. Reports Full-Read Pollutes Context

- symptom: Old reports dominate new task judgment.
- root cause: reports archive treated as active context.
- blocking rule: Do not read reports by default.
- required fix: Add reports/index and read only selected reports.
- verification: verify-context-budget.

## 6. Old Status Code Reused

- symptom: Previous PASS is copied into new task.
- root cause: Historical success was inherited without proof chain.
- blocking rule: Status code requires current evidence.
- required fix: Rebuild proof chain for current task.
- verification: verify-final-pass or deterministic status-code evidence check.

## 7. Untracked Artifacts Hidden As Residual Risk

- symptom: Task artifacts remain untracked/unhashed but PASS is claimed.
- root cause: Artifact checkpoint closure missing.
- blocking rule: Artifact gap cannot be residual risk.
- required fix: artifact manifest, sha256 manifest, git status, disposition.
- verification: verify-artifact-checkpoint.

## 8. Completion Ledger Not 100%

- symptom: Ledger has PARTIAL/NOT_STARTED/BLOCKED but PASS is claimed.
- root cause: Completion Ledger was advisory.
- blocking rule: Completion Ledger 100% required.
- required fix: complete, stop, or waive items.
- verification: verify-completion-ledger.

## 9. Status Code Without Proof Chain

- symptom: Final status exists but evidence chain is incomplete.
- root cause: Status code treated as proof.
- blocking rule: Status code without proof chain is hallucinated success.
- required fix: map status to evidence path.
- verification: verify-logical-100.

## 10. Model Self-Claim Treated As Verification

- symptom: "I checked" appears without files, commands, or logs.
- root cause: Model narrative substituted for deterministic check.
- blocking rule: Model self-claim is not verification.
- required fix: add script output or checklist.
- verification: verify-governance-skill.
