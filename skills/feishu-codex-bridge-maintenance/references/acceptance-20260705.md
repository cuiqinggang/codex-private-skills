# Acceptance Evidence 2026-07-05

Status: PASS

Evidence:

- Feishu -> lark-channel-bridge -> Codex CLI was proven.
- `TEST_FEISHU_CODEX_OK.txt` was created in `K:\AI\remote-codex-workspace`.
- Profile permissions were corrected to `workspace/workspace`.
- `health-check.ps1` generated `health-latest.json` and `health-latest.md`.
- `watchdog.ps1` returned OK while recording Codex/model timeout warnings.
- `FeishuCodexBridgeWatchdog` scheduled task was created with `schtasks.exe`.
- Main slow layer was identified as Codex CLI/model requests, not Feishu WebSocket.

Key files:

```text
${REDACTED_SECRET}
${REDACTED_SECRET}
K:\AI\remote-codex-workspace\maintenance
```

## Slow Reply Repair Evidence

Status: PARTIAL PASS

Evidence:

- Profile `codex` fast display preferences were set:
  - `messageReply=text`
  - `showToolCalls=false`
  - `cotMessages=off`
  - `runIdleTimeoutMinutes=1`
- Bridge processes remained alive after restart.
- Skill first-line/frontmatter scan returned `ALL_SKILL_FIRST_LINES_OK`.
- Direct local `codex exec` test with a prompt that only replied `OK` still took about 126 seconds.
- The same test emitted four reconnect timeout events, proving the remaining slow layer is Codex CLI/model request latency.
- `gpt-5.5-mini` returned unsupported for the current ChatGPT account and was not written into the bridge profile.

Reusable conclusion:

Fast mode and skill cleanup are the correct first repair. If latency remains above 120 seconds with `request timed out` / `Reconnecting`, do not keep restarting Feishu; diagnose Codex/model connectivity or account-supported model choices next.
