# 数字孪生交接

## Host / Codex R2
```text
HOST_R2_STATUS=REALITY_ANCHOR_COMPLETE
CRITICAL_UNKNOWN_COUNT_FINAL=0
CRITICAL_EXECUTION_STATE_COVERAGE_PERCENT=100.00
HOST_R2_TWIN_INPUT_READY=YES
ENVIRONMENT_99=NOT_YET
```

当前 Host 权威文件：
- `snapshots/2026-09-21-r2/45-REALITY-ENVIRONMENT-ANCHOR-R2-FINAL.json`
- `snapshots/2026-09-21-r2/46-REALITY-FINGERPRINT-V3.json`

Host Twin 必须复现：
`SetTokenInformation -> 1344 -> 3/3 -> child not running -> PATH NOT_REACHED -> NO_RUNNING_CHILD_PROCESS_TOKEN`。
不得用 COLLECTOR 能力替代 TARGET 行为。

## Browser R3
浏览器 Reality 不能从 Host R2 自动推导。必须使用 Browser R3 真实 Golden Task 采集：
```text
BROWSER_R3_REAL_CAPTURE=NOT_YET
BROWSER_R3_FINGERPRINT=NOT_YET
BROWSER_TWIN_INPUT_READY=NO
```

只有 `BROWSER-REALITY-R3-ACCEPTANCE.md` 全部通过后，才把新 Browser Reality Fingerprint 交给：
`first-principles-physical-limit-convergence@3.1.7/components/exact-reality-digital-twin@1.1.0`。
