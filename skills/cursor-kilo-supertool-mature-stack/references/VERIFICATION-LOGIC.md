# Verification Logic

Use this reference when repairing validation, gate review, continuous verification, or acceptance logic.

## Problem To Avoid

Do not use failure-only verification. The bad pattern is:

- real execution happened
- API calls succeeded
- routing worked
- cycles completed
- but every cycle is labeled FAIL because the verifier only searches for anomaly strings

This creates false failure and hides actual system state.

## Bidirectional Verification Model

For every cycle, detect both success and failure signals.

Success signals:

- real API response received
- model routing executed
- tool invocation completed
- output generated from execution

Failure signals:

- missing execution output
- mock or static response
- routing not triggered
- tool not invoked

## Weighted Scoring

Recommended weights:

```text
execution_real = +3
routing_correct = +2
tool_invoked = +2
output_generated = +3

mock_detected = -4
missing_execution = -5
routing_bypass = -5
```

Decision:

```text
score >= 5  => OK
score 1..4  => DEGRADED
score <= 0  => FAIL
```

## Required Cycle Output

Each cycle should output:

```json
{
  "execution_verified": true,
  "routing_verified": true,
  "tool_verified": true,
  "output_valid": true,
  "score": 10,
  "status": "OK"
}
```

## Acceptance Rules

- Unknown is not automatically FAIL.
- Any anomaly is not automatically FAIL.
- A final report, script output, or ZIP is not final acceptance by itself.
- Final acceptance must compare claims against evidence.
- Rejected claims must go through repair loop or remain explicitly unresolved.
- Do not claim PASS if rejected claims or unresolved blockers remain.

## Reusable Repair Script

When the mature ecosystem station already contains real cycle logs but the report says `fail_cycles=30`, use:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "C:\Users\A\.codex\skills\cursor-kilo-supertool-mature-stack\scripts\repair_system_verification_logic.ps1"
```

The script:

- backs up the previous continuous verification report
- binds the existing OpenRouter live smoke evidence
- recalculates each cycle with bidirectional scoring
- rewrites `health`, `status`, `success_signals`, `failure_signals`, and `verification_score`
- updates `system_verification_report.json`, `system_verification_report.md`, and `final_verdict.txt`
- writes `verification_logic_repair\verification-logic-repair-report.md`

It must not call APIs, change model configuration, rebuild the station, print keys, modify Hermes Gateway, or touch Qwen direct vision config.
