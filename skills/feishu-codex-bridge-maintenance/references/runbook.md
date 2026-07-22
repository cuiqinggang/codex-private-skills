# Feishu Codex Bridge Maintenance Runbook

## Evidence From First Successful Deployment

${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
- `lark-channel-bridge@0.5.4` was installed and bound by QR.
- First generated profile defaulted to unsafe `full/full`; it was backed up and corrected to `workspace/workspace`.
${REDACTED_SECRET}

## Layered Diagnosis

Use this order:

1. Process layer: find only processes with `lark-channel-bridge` in command line.
2. Config layer: confirm profile `codex`, workspace path, and `workspace/workspace`.
${REDACTED_SECRET}
4. Feishu command layer: `/status` and `/help` should be fast.
5. Codex task layer: normal tasks may take 120-160 seconds due to model request timeouts.
6. Skill metadata layer: Codex startup may print malformed skill warnings.

## 2026-07-05 Slow Reply Repair Record

Observed symptom:

- Feishu showed the bot "thinking" for a long time.
- `/status` and `/help` were able to reply.
- Normal Codex tasks took roughly 120-166 seconds.

Confirmed causes:

- The bridge process was alive.
- The profile remained safely limited to `workspace/workspace`.
- Latest logs contained repeated `request timed out` and `Reconnecting... 2/5` through `5/5`.
- Direct local `codex exec` tests reproduced the same latency without Feishu, proving the main slow layer was Codex CLI/model request, not Feishu WebSocket.
- Several local skills had malformed metadata: UTF-8 BOM before `---`, invalid YAML descriptions, or non-UTF-8 content. These caused startup noise and should be cleaned, but they were not the main 120+ second delay.

Repair actions that should be reused:

${REDACTED_SECRET}
2. Set profile `codex` fast display preferences:
   - `messageReply: text`
   - `showToolCalls: false`
   - `cotMessages: off`
   - `runIdleTimeoutMinutes: 1`
   - `messageReplyMigrated: true`
3. Restart only `lark-channel-bridge` matched processes.
4. Fix malformed skill files with backups:
   - Remove UTF-8 BOM before frontmatter.
   - Quote YAML descriptions containing colon-like text.
   - Convert invalid/non-UTF-8 `SKILL.md` files to UTF-8.
   - Never delete skills as the first fix.
5. Run a short timing test: `only reply OK`.
6. If timing is still 120+ seconds with reconnect timeouts, tell the user the remaining bottleneck is the Codex/model request path.
7. Do not configure unsupported models. On 2026-07-05, `gpt-5.5-mini` returned "model is not supported when using Codex with a ChatGPT account".

Fast mode expected effect:

- Less Feishu-side clutter.
- No visible long tool-call blocks.
- Idle stuck runs end faster.
- It does not guarantee fast model responses when upstream Codex requests are timing out.

## Safe Restart

Restart only matched processes:

```powershell
$targets = Get-CimInstance Win32_Process |
  Where-Object {
    $_.CommandLine -and
    ($_.CommandLine -like '*lark-channel-bridge*' -or $_.CommandLine -like '*.lark-channel*') -and
    $_.Name -in @('node.exe','cmd.exe')
  }
foreach ($p in $targets) {
  Stop-Process -Id $p.ProcessId -Force -ErrorAction SilentlyContinue
}
Start-Process -FilePath "$env:APPDATA\npm\lark-channel-bridge.cmd" `
  -ArgumentList @('run','--profile','codex') `
${REDACTED_SECRET}
  -WindowStyle Hidden
```

## Maintenance Scripts

Canonical active scripts:

```text
${REDACTED_SECRET}
${REDACTED_SECRET}
```

Expected files:

```text
health-latest.json
health-latest.md
restart-history.md
SKILL_ERRORS.md
TASK_SCHEDULER_RESULT.md
```

## Task Scheduler

Known task:

```text
FeishuCodexBridgeWatchdog
```

It was created with `schtasks.exe` every 5 minutes after the PowerShell ScheduledTasks API returned access denied.

Rollback:

```powershell
schtasks.exe /Delete /TN FeishuCodexBridgeWatchdog /F
```

## Known Skill Load Error Sources

Observed examples include:

- `chatgpt-cdp-browser`
- `claude-code-cursor-super-tool-predeploy`
- `codex-chaos-normalizer`
- `codex-deepseek-v4pro-ccx-ccswitch-replay`
- `codex-video-to-usable-skill-loop`
- `github-version-save-profile`
- `kilo-codex-claude-permission-guard`
- `new-api-local-deploy`
- `ppt-showcase-video`
- `ultrafusion-6-0-kimi-no-deepseek`
- `ultrafusion-low-cost-multi-model-extreme-fusion`
- `universal-playwright-cli-browser-automation`
- `windows-hermes-operations`

Do not delete them. Recommend fixing frontmatter, YAML syntax, or UTF-8 encoding.

## Reporting Template

Use concise Chinese:

```text
结论：...
证据：...
处理：...
风险：bridge guard 只能恢复 bridge，不能保证 Codex CLI/外部模型永远不超时。
```
