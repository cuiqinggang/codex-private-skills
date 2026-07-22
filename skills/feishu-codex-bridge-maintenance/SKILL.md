---
name: feishu-codex-bridge-maintenance
description: Maintain and diagnose the user's local Feishu/Lark to Codex CLI bridge on Windows, especially tasks mentioning 飞书, lark-channel-bridge, Codex CLI remote access, 崔清岗的智能助手, FeishuCodexBridgeWatchdog, health-check.ps1, watchdog.ps1, bridge no reply, request timed out, workspace/workspace permissions, or keeping the Feishu Codex bridge alive without replacing the proven bridge.
---

# Feishu Codex Bridge Maintenance

Use this skill to preserve, diagnose, and maintain the already-proven local path:

```text
Feishu/Lark -> lark-channel-bridge -> local Codex CLI -> Feishu reply
```

Do not replace the working bridge with another runtime unless the user explicitly asks.

## Current Proven State

- Primary runtime: `lark-channel-bridge@0.5.4`.
- Active profile: `codex`.
- Bot name observed: `崔清岗的智能助手`.
${REDACTED_SECRET}
${REDACTED_SECRET}
- Backup/reference copy: `K:\AI\remote-codex-workspace` (never the active watchdog or bridge working directory).
- Required permission profile: `defaultAccess=workspace`, `maxAccess=workspace`.
${REDACTED_SECRET}
- Watchdog task: `FeishuCodexBridgeWatchdog`.

Read `references/runbook.md` when repairing, extending, or reporting on this bridge.

## Hard Safety Rules

- Never change permissions back to `full/full`.
- Never use `danger-full-access` as the default bridge profile.
- Never print App Secret, token, API key, password, `.env`, `secrets.enc`, WebSocket ticket, or access key.
- Never kill all `node.exe`; only manage processes whose command line matches `lark-channel-bridge`.
- Never modify proxy, VPN, DNS, hosts, firewall, `C:\Windows`, or system directories.
- Do not install Startup/HKCU Run fallbacks unless the user explicitly approves.
- Preserve current config before any meaningful edit.

## First Response Pattern

When the user says the bot is slow, silent, disconnected, or needs maintenance:

1. Check bridge processes by command line, not by process name alone.
${REDACTED_SECRET}
${REDACTED_SECRET}
4. Distinguish:
   - Feishu/WebSocket or bridge down.
   - Bridge process alive but log stale: likely fake-alive bridge, restart only matched bridge processes.
   - Bridge receives messages but Codex run is slow: model/Codex CLI layer, not bridge.
   - Skill load errors: startup noise and secondary latency source.
5. Prefer running the bundled health script before hand-built diagnosis.

## Fast Response Mode / Slow Reply Repair

When Feishu shows "thinking" for a long time but `/status` or `/help` can reply, treat it as a slow Codex/model layer first, not as a broken Feishu bridge.

Apply this reusable repair sequence:

1. Confirm bridge is alive by process command line and latest log timestamp.
2. Confirm profile `codex` still has `permissions.defaultAccess=workspace` and `permissions.maxAccess=workspace`.
3. Set profile-level fast display preferences, preserving a config backup first:
   - `preferences.messageReply = "text"`
   - `preferences.showToolCalls = false`
   - `preferences.cotMessages = "off"`
   - `preferences.runIdleTimeoutMinutes = 1`
   - `preferences.messageReplyMigrated = true`
4. Restart only matched `lark-channel-bridge` processes so the profile reloads.
${REDACTED_SECRET}
6. If the test still takes 120+ seconds and logs show repeated `request timed out` / `Reconnecting`, report that the slow layer is Codex CLI/model request, not Feishu WebSocket.
7. If startup prints skill errors, fix skill frontmatter/YAML/UTF-8 with backups. Do not delete skill directories.
8. Do not switch global model/provider blindly. Test model names first; if a model is unsupported for the account, do not write it into the Feishu profile.

Known 2026-07-05 result:

- Fast display mode was applied successfully.
- Skill first-line/BOM issues were cleaned.
- A direct local `codex exec` prompt that only replied `OK` still took about 126 seconds because Codex CLI emitted four `request timed out` reconnect events.
- `gpt-5.5-mini` was tested and rejected as unsupported for the current ChatGPT account, so it must not be configured as the bridge model.

Conclusion rule: fast display mode can reduce Feishu clutter and stop long tool-call cards, but it cannot fix upstream Codex/model request timeouts by itself.

## Scripts

Use the bundled scripts as templates or copy them into the active maintenance directory:

- `scripts/health-check.ps1`: generate `health-latest.json` and `health-latest.md`.
- `scripts/watchdog.ps1`: call health-check, restart only matched bridge processes when needed, and write `restart-history.md`.

Canonical active copies live at:

```text
${REDACTED_SECRET}
${REDACTED_SECRET}
```

Run manually:

```powershell
${REDACTED_SECRET}
${REDACTED_SECRET}
```

## Key Diagnostics

Bridge process:

```powershell
Get-CimInstance Win32_Process |
  Where-Object { $_.CommandLine -like '*lark-channel-bridge*' -or $_.CommandLine -like '*.lark-channel*' } |
  Select-Object ProcessId,Name,CommandLine
```

Bridge CLI:

```powershell
lark-channel-bridge ps
lark-channel-bridge status --profile codex
lark-channel-bridge --help
```

Permission check:

```powershell
$j = Get-Content "$env:USERPROFILE\.lark-channel\config.json" -Raw | ConvertFrom-Json
$j.profiles.codex.permissions
```

Healthy profile must show:

```text
defaultAccess : workspace
maxAccess     : workspace
```

## Known Failure Modes

- `request timed out` / repeated `Reconnecting`: Codex CLI/model request layer is slow. Watchdog should record this, not restart the bridge for this alone.
- Latest bridge log does not update after the user sends a message: bridge/WebSocket may be fake-alive. Restart only matched `lark-channel-bridge` processes.
- `/status` and `/help` respond but normal tasks are slow: bridge is healthy; Codex/model layer is slow.
- `failed to load skill ... missing YAML frontmatter` or invalid YAML/UTF-8: skill metadata noise. List and recommend fixes; do not delete skills.
- `full/full` or `danger-full-access`: critical safety violation. Stop bridge and alert.

## Output Style For Feishu

Keep Feishu replies short. Put long reports in files such as:

```text
${REDACTED_SECRET}
${REDACTED_SECRET}
```

In chat, summarize in one screen:

```text
结论：bridge 正常 / 假活已重启 / 慢点在 Codex CLI。
关键证据：...
下一步：...
```

## Acceptance Criteria

Claim PASS only when:

- `health-check.ps1` produces JSON and Markdown.
- `watchdog.ps1` runs without unsafe permission changes.
- `FeishuCodexBridgeWatchdog` exists or the report explains why Task Scheduler is unavailable.
- The bridge profile remains `workspace/workspace`.
- The report states whether the slow layer is Feishu/WebSocket, bridge runtime, Codex CLI/model, or skill loading.
- No secrets are printed.
