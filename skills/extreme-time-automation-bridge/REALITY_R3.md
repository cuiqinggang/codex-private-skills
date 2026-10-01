# Reality R3｜Windows Reality Smoke PASS

```ini
VERSION=0.1.3
SCOPE=WINDOWS_REALITY_SMOKE

WORKFLOW_RUN_ID=36899361139
SOURCE_COMMIT=5f0451d96ee25850b0de2348b588ec55414e766e
TASK_ID=ETAL-BRIDGE-SMOKE-001

RUNNER_NAME=DESKTOP-4A1EGTM-etal
RUNNER_LABELS=self-hosted,Windows,X64
RUNNER_MODE=TEMPORARY_NON_PERSISTENT

CONTRACT_STATIC=PASS
WINDOWS_PICKUP=YES
PAYLOAD_EXECUTED=YES
RESULT_JSON=PASS
STDOUT=PASS
STDERR=PASS_EMPTY
ARTIFACT=PASS
ARTIFACT_ID=11186888753
ARTIFACT_NAME=etal-bridge-ETAL-BRIDGE-SMOKE-001-36899361139
ARTIFACT_DIGEST=sha256:7cc79439b8979d53be906e5a2ce3dc1808cf4fc9405e158c8f6a8491e3b656aa

RESULT_STATUS=PASS
RESULT_EXIT_CODE=0
RESULT_DURATION_MS=9316.85
USER_INTERVENTIONS_DURING_SMOKE=0

WINDOWS_REALITY=PASS
PERSISTENCE_CONFIGURED=NO
CALLBACK_TESTED=NO
BRIDGE_REALITY=PARTIAL
REALITY_CERTIFIED=NO
```

## 独立核验

GitHub Actions 显示：
- `contract-static` completed/success；
- `windows-reality` completed/success；
- Execute task、Upload machine evidence 均 success。

artifact 实际下载并检查：
- `result.json`：status=PASS，exit_code=0，runner_name=DESKTOP-4A1EGTM-etal；
- `stdout.txt`：smoke status=PASS，PowerShell 7.6.6，Windows NT 10.0.19045.0；
- `stderr.txt`：0 字节。

因此不能再把 Windows 层描述为“等待 runner”。

## 当前边界

这次只证明：

```text
GitHub task
→ self-hosted Windows pickup
→ payload real execution
→ result.json/stdout/stderr
→ artifact
→ PASS
```

尚未证明：

```text
常驻 runner
→ callback
→ GPT 自动继续判断
→ 自动派发下一任务
→ 再次 Windows Reality
```

完整桥 Reality 仍为 PARTIAL。
