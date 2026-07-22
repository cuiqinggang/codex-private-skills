# Failure Modes And Fixes

## Claude Code Login Block

Do not keep trying to bypass official login. Switch to Cursor + Kilo route.

## Tool Name Confusion

Do not choose a tool because the name resembles Roo/Cline. Evaluate activity, usage, docs, provider maturity, install source, and reproducibility.

## Cheap Model Trap

Do not select low-cost 8B/30B visual models as primary for high-reliability visual work.

## UI Automation Surprise

If visible Cursor command palette or UI actions surprise the user, stop UI automation. Continue with file/CLI evidence and record the limitation.

## ZIP Contains Only Directories

After compression, inspect the ZIP entries. Confirm evidence images and model logs are inside.

## PowerShell NativeCommandError Around Kilo CLI

Kilo CLI may write progress/status to stderr. Inspect the actual model output before treating it as a model failure.

## Direct Video Overreach

Do not test direct video input unless safe and necessary. Prefer contact-sheet/keyframe route.

## Context Bloat

Keep active context to:
- current user request
- current matrix
- latest report paths
- safety boundaries
- exact next action

Move stage detail into reports and skill references.

## Config-Only Provider Proof

Do not claim a model route is live verified from settings, local reports, user decision, or provider catalog alone. Use `live_call_verified=false` until an actual provider call returns non-empty assistant text.

## Empty Content With Provider Response Id

Some models may return a provider response id but empty assistant content for a given prompt. Treat that as useful transport evidence but not a live-call PASS. Retry with tiny plain-text prompts. If content remains empty, report PARTIAL.

## Failure-Only Verification

Do not label every cycle FAIL by searching only for anomalies. Verification must detect success signals and failure signals, score both, and output OK / DEGRADED / FAIL.

## Kilo UI Falls Back To DeepSeek V3.2

${REDACTED_SECRET}

If the issue returns after reopening Cursor, remove every Kilo/Gateway recent model candidate too. The stable state should have `recentModels` containing only `{"providerID":"openrouter","modelID":"deepseek/deepseek-v4-pro"}`. Do not delete or patch Kilo extension files such as `models-snapshot.json`; their V3.2 entries are catalog entries, not the active user selection.

## Kilo Code Mode Still Uses Kilo Gateway

Symptom: Kilo Settings default model shows `OpenRouter / DeepSeek V4 Pro`, but
the bottom bar only shows `DeepSeek V4 Pro`, and a real request returns a login
requirement. Root cause can be:

```text
${REDACTED_SECRET}
```

with:

```json
"code": {"providerID": "kilo", "modelID": "deepseek/deepseek-v4-pro"}
```

Fix it to:

```json
"code": {"providerID": "openrouter", "modelID": "deepseek/deepseek-v4-pro"}
```

Then restart Cursor/Kilo and open Kilo through `Ctrl+Shift+P` →
`Kilo Code: Open in Tab`. Use screenshot plus a real reply containing
`KILO_OPENROUTER_DEEPSEEK_V4_PRO_OK` before calling the route verified.

Do not promote `Kilo Code: New Task` as the verified route if it opens Cursor
Agent/Composer. Do not use the far-right Cursor three-dot `Open in Tab` as proof
for Kilo OpenRouter routing.

## Kilo Tab Opens Blank Or Has No Model Bar While Stored Config Is Correct

Symptom: `model.json`, `kilo.jsonc`, and Cursor `kilocode.kilo-code` state all
point to OpenRouter DeepSeek V4 Pro, but the visible Kilo tab is blank, stuck on
a loading cube, or shows no model information.

Root cause observed on 2026-07-03: the workspace editor layout state restored a
stale Kilo webview from:

```text
${REDACTED_SECRET}
key: memento/workbench.parts.editor
```

The stale value contained `mainThreadWebview-kilo-code.new.TabPanel` and
`kilo-code.new.settingsPanel` webview inputs from an old session. Clearing
Service Worker / GPU / session cache alone was not enough.

Fix: close Cursor and Kilo, back up the workspace `state.vscdb`, delete only
`memento/workbench.parts.editor`, reopen Cursor, click inside the workbench,
press `F1`, and select `Kilo Code: Open in Tab`. Verify the bottom bar shows
`OpenRouter / DeepSeek V4 Pro`, then send the fixed reply test. Do not call PASS
until the real response contains `KILO_OPENROUTER_DEEPSEEK_V4_PRO_OK`.

## Cursor Opens English Agents Page Instead Of Chinese Kilo IDE

Symptom: Cursor opens a page titled `New Agent` / `Cursor Agents` with English
menus such as `File`, `Edit`, `View`, `Help`; the left rail shows `New Agent`,
`Search`, `Automations`, `Customize`; Kilo Code is not visible. This is the
Cursor Agents/Glass entry, not the verified Kilo Code IDE route.

Do not diagnose this as Kilo provider loss if the following files are still
correct:

```text
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
```

Observed root cause on 2026-07-04: Cursor global state still had
`cursor/unifiedAppLayout = agent`, so a normal Cursor launch could restore the
English Agents entry even though the Chinese language pack and Kilo model state
were still present.

Verified recovery route:

```powershell
${REDACTED_SECRET}
```

Then use `Ctrl+Shift+P` and run:

```text
Kilo Code: Open in Tab
```

Acceptance screenshots must show all of the following:

- Chinese Cursor IDE menu, for example `文件(F)`, `编辑(E)`, `查看(V)`.
- A `Kilo Code` editor tab, not `New Agent`.
- Kilo page text in Chinese.
- Bottom model bar: `Code` plus `OpenRouter / DeepSeek V4 Pro`.

2026-07-04 evidence:

```text
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
```

A durable desktop shortcut was created:

```text
${REDACTED_SECRET}
```

Use that shortcut for user-facing validation to avoid falling back to the
English Agents entry.

## Cursor Classic Kilo Opens Correctly But Top Menubar Stays English

Symptom: Cursor opens the correct Kilo Code IDE workspace, Kilo page text is
Chinese, and the model remains `OpenRouter / DeepSeek V4 Pro`, but the top
menubar still shows `File`, `Edit`, `Selection`, `View`, `Go`, `Terminal`, and
`Help`. Only `Run` may show as Chinese.

Do not keep rebuilding only:

```text
${REDACTED_SECRET}
```

Observed root cause on 2026-07-07 with Cursor `3.10.17`: the bundled
`workbench.desktop.main.js` and `workbench.glass.main.js` register those
top-level menu title values as fixed English strings. The zh-cn cache can be
healthy while this visible menu layer stays English.

Use `CURSOR-MENUBAR-LOCALIZATION-FIX-20260707.md`: back up the app resources,
patch only the top-level menu title values to Chinese, update
`product.json -> checksums["vs/workbench/workbench.desktop.main.js"]`, restart
Cursor through the mature `--classic --locale zh-cn` route, and verify with two
screenshots. Do not modify Kilo model files, API keys, Hermes, Qwen direct
vision config, or Windows proxy/network settings.

## Cursor/Kilo Long Text Paste Does Not Become @file

Symptom: long text still cannot be pasted into Kilo/Cursor after the old
terminal paste repair is present. `keybindings.json` already contains terminal
`ctrl+v` and `shift+insert`, but Kilo chat direct paste still fails or is too
large.

Do not keep treating this as a terminal shortcut bug. Use the long-text
converter route in `LONGTEXT-PASTE-RESTORE.md`.

Observed root cause on 2026-07-04: the converter was started with:

```text
${REDACTED_SECRET}
```

but that path was a 3-byte file, not a directory. The log showed:

```text
KILO_WORKSPACE_MISSING
```

Fix: restart the converter with the real mature station directory:

```powershell
${REDACTED_SECRET}
```

Expected log:

```text
ACTIVATED kilo mention for CursorKilo mention=@.kilo-longtext/...
```

The generated file must exist under:

```text
${REDACTED_SECRET}
```

Also make sure the desktop Kilo shortcut opens the real folder, not the old
`kilo-validation` file:

```text
${REDACTED_SECRET}
```
