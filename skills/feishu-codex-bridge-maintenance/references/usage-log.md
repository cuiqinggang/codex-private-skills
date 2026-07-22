# Usage Log

## 2026-07-05

User asked to preserve the working Feishu -> lark-channel-bridge -> Codex CLI setup and maintenance system into a reusable skill and knowledge base.

Actions:

- Created C-drive skill `feishu-codex-bridge-maintenance`.
- Copied verified `health-check.ps1` and `watchdog.ps1` into the skill package.
- Added runbook and acceptance evidence.
- Stored knowledge note in AI Company Knowledge OS.

Result: PASS.

## 2026-07-05 Slow Reply Repair

User reported that Feishu replies were too slow and the bot stayed in thinking state.

Actions:

- Confirmed bridge process was alive and profile permissions remained `workspace/workspace`.
- Enabled fast display mode in the `codex` profile: text final reply, no tool-call display, COT off, 1-minute idle timeout.
- Restarted only matched `lark-channel-bridge` processes.
- Cleaned malformed skill metadata that caused Codex startup warnings: BOM/frontmatter, YAML description quoting, and UTF-8 issues.
- Timed a direct local `codex exec` prompt that only replied `OK`.
- Verified `gpt-5.5-mini` is unsupported for the current ChatGPT account and should not be configured.

Result: PARTIAL PASS. Feishu display mode and skill metadata noise were repaired; remaining 120+ second latency is from Codex CLI/model request timeouts, not the Feishu bridge.
