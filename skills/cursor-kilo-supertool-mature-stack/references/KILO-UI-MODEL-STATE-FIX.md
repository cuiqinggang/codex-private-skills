# Kilo UI Model State Minimal Fix

Use this when Cursor/Kilo UI shows `DeepSeek V3.2`, `deepseek-v3.2`, `deepseek/deepseek-v3`, or a login-gated Kilo model while the mature route should use OpenRouter DeepSeek V4 Pro.

## Scope

This is a small state repair, not a redeployment.

- Do not reinstall Cursor or Kilo.
- Do not clear all Cursor or Kilo configuration.
- Do not modify API keys.
- Do not print API keys.
- Do not change Hermes Gateway, Qwen vision config, proxy, or unrelated files.
- Prefer a single targeted edit with a backup.

## Target Search Locations

Search only the relevant Cursor/Kilo config surfaces first:

```text
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
```

Search terms:

```text
DeepSeek V3.2
deepseek-v3.2
deepseek/deepseek-v3
v3.2
```

Use filename-only search first. Do not dump large binary/state files to the console because they may contain unrelated secrets.

## Known Cursor State Location

Kilo's UI model picker can be stored inside Cursor's SQLite state database:

```text
${REDACTED_SECRET}
```

Known table/key pattern:

```text
table: ItemTable
key: kilocode.kilo-code
value: {"kilo.autocomplete.defaultClearMigrationV1":true,"recentModels":[...]}
```

Bad UI state example:

```json
{"providerID":"kilo","modelID":"deepseek/deepseek-v3.2"}
```

Mature-route replacement:

```json
{"providerID":"openrouter","modelID":"deepseek/deepseek-v4-pro"}
```

If the same value already contains an OpenRouter / DeepSeek V4 Pro entry, reuse that existing style. Do not invent a new provider/model format when the file already shows one.

## Revert-After-Reopen Fix

If Kilo UI returns to `DeepSeek V3.2` or a login-gated Kilo route after a previous edit, the stale `deepseek-v3.2` entry may already be gone, but a second recent model can still point to Kilo/Gateway instead of OpenRouter.

Observed state before the stronger fix:

```json
{
  "recentModels": [
    {"providerID":"openrouter","modelID":"deepseek/deepseek-v4-pro"},
    {"providerID":"kilo","modelID":"deepseek/deepseek-v4-pro"}
  ]
}
```

Fix: close Cursor first, back up `state.vscdb` plus sidecars, then set `recentModels` to the single intended OpenRouter route:

```json
{
  "recentModels": [
    {"providerID":"openrouter","modelID":"deepseek/deepseek-v4-pro"}
  ]
}
```

This removes both stale `DeepSeek V3.2` routes and login-gated Kilo/Gateway candidates. Do not edit Kilo extension model catalogs such as `models-snapshot.json`; those are product model inventories, not user state.

## Clean-State But UI Still Shows V3.2

Observed on 2026-06-30:

- Old Kilo/Cursor task still displayed `OpenRouter / DeepSeek V4 Pro`.
- A newly opened Kilo tab displayed `DeepSeek V3.2` plus a third selector row showing `None`.
${REDACTED_SECRET}
- `state.vscdb` key `kilocode.kilo-code` was already clean:

```json
{
  "recentModels": [
    {"providerID": "openrouter", "modelID": "deepseek/deepseek-v4-pro"}
  ]
}
```

Interpretation: this is not the original stale-database failure. If `HAS_DEEPSEEK_V3_2=False`, `HAS_OPENROUTER_V4PRO=True`, and `HAS_KILO_PROVIDER_IN_KILOCODE_STATE=False`, do not keep rewriting `state.vscdb`. Treat the visible `DeepSeek V3.2` as a running Cursor/Kilo webview/runtime-cache state or workspace-level override until proven otherwise.

Next diagnostic order:

1. Search `Cursor\User\workspaceStorage` for `deepseek-v3.2`, `deepseek/deepseek-v3`, `recentModels`, and `providerID`.
2. Confirm Kilo global config still points to OpenRouter V4 Pro and `snapshot=false`.
3. Use `Developer: Reload Window` or close/reopen Cursor after saving work.
4. Re-check `state.vscdb` after reload. If it remains clean but UI still shows V3.2, capture screenshot evidence and inspect Kilo webview/session state rather than editing the extension model catalog.

The extra `None` row in the new tab is a separate selector state symptom. Record it as `NEW_TAB_SECONDARY_SELECTOR_NONE_VISIBLE`; do not assume it is the model name. It becomes actionable only if it persists after reload while the primary route is still wrong.


## Backup Rule

Before editing `state.vscdb`, back up the database and sidecar files:

```text
state.vscdb
state.vscdb-shm
state.vscdb-wal
```

Use a timestamped folder under:

```text
${REDACTED_SECRET}
```

## Minimal Verification

After the edit, verify:

```text
HAS_DEEPSEEK_V3_2=False
HAS_OPENROUTER_V4PRO=True
```

For the stronger revert fix, also verify:

```text
HAS_KILO_PROVIDER_IN_KILOCODE_STATE=False
```

Then reopen Cursor once, close it again, and re-check the same three values. If they remain stable after reopen, the state repair persisted.

Do not claim UI runtime PASS from this alone. This only confirms the stored model state changed. Cursor must reload before the UI can pick it up.

## Required User-Facing Result

Report:

- edited file
- backup folder
- original state fragment
- replacement state fragment
- whether API keys were touched
- whether Cursor needs restart or `Developer: Reload Window`

Recommended final note:

```text
需要重启 Cursor，或者在 Cursor 里执行 Developer: Reload Window，Kilo 面板才会重新读取这个状态配置。
```

## Follow-Up Acceptance

For full UI acceptance, run actual Cursor/Kilo UI verification after reload:

1. Open the target workspace.
2. Open Kilo Code panel.
3. Confirm model/provider shown in the Kilo UI.
4. Submit a small read-only Chinese task.
5. Screenshot the returned answer.

Only then can the UI route be considered actually verified.

## Verified 2026-07-03: Code Mode Model-State File

If Kilo Settings shows the default model as `OpenRouter / DeepSeek V4 Pro`
but a real Code-mode request still says login is required, inspect the Kilo
backend model-state file:

```text
${REDACTED_SECRET}
```

The effective Code-mode state must be:

```json
{
  "model": {
    "code": {
      "providerID": "openrouter",
      "modelID": "deepseek/deepseek-v4-pro"
    }
  }
}
```

Known bad state:

```json
{
  "model": {
    "code": {
      "providerID": "kilo",
      "modelID": "deepseek/deepseek-v4-pro"
    }
  }
}
```

This bad state makes the bottom bar look like `DeepSeek V4 Pro` but routes the
request through Kilo Gateway, causing the login-required message.

Verified open route:

1. Open Cursor with the target workspace.
2. Press `Ctrl+Shift+P`.
3. Select `Kilo Code: Open in Tab`.
4. Do not use Cursor Agent `New Task` as acceptance evidence.
5. Do not use the far-right Cursor three-dot `Open in Tab` as Kilo OpenRouter
   acceptance evidence.
6. Verify the Kilo bottom bar shows `OpenRouter / DeepSeek V4 Pro`.
7. Send `请只回复：KILO_OPENROUTER_DEEPSEEK_V4_PRO_OK`.
8. PASS only if the reply contains `KILO_OPENROUTER_DEEPSEEK_V4_PRO_OK`.

2026-07-03 evidence path:

```text
${REDACTED_SECRET}
```

## Verified 2026-07-03: Blank Kilo Tab / Missing Model Bar After Model-State Fix

Use this when all three stored model states are already clean, but the Kilo tab
opens blank, shows only a loading cube, or does not show model information.

Clean-state indicators:

```text
${REDACTED_SECRET}
  code.providerID = openrouter
  code.modelID = deepseek/deepseek-v4-pro

${REDACTED_SECRET}
  model = openrouter/deepseek/deepseek-v4-pro
  snapshot = false

${REDACTED_SECRET}
  kilocode.kilo-code recentModels = only openrouter/deepseek/deepseek-v4-pro
```

Observed new root cause:

```text
${REDACTED_SECRET}
key: memento/workbench.parts.editor
value contains stale workbench.editors.webviewInput entries for:
  mainThreadWebview-kilo-code.new.TabPanel
  kilo-code.new.settingsPanel
```

This can make Cursor restore a stale Kilo webview tab from an old session. The
Kilo backend and model config can be correct while the UI keeps showing a blank
or partially loaded panel with no model bar.

Minimal repair:

1. Close Cursor and `kilo.exe`.
2. Back up the affected workspace `state.vscdb` plus sidecars.
3. Delete only the `memento/workbench.parts.editor` key from that workspace
   database.
4. Reopen Cursor.
5. Click inside Cursor first so keyboard focus is inside the workbench.
6. Press `F1`.
7. Select `Kilo Code: Open in Tab` from the command palette.
8. Verify the new Kilo tab shows `OpenRouter / DeepSeek V4 Pro`.
9. Send `请只回复：KILO_OPENROUTER_DEEPSEEK_V4_PRO_OK`.
10. PASS only if the reply contains `KILO_OPENROUTER_DEEPSEEK_V4_PRO_OK`.

Avoid:

- Do not rewrite `model.json` again when it is already OpenRouter.
- Do not use `Kilo Code: New Task`; it can land in Cursor Agent / Composer.
- Do not rely on keyboard shortcuts until Cursor has real focus. In this
  incident, `Ctrl+Shift+P` was captured by another app and opened a print
  dialog. Use `F1` after clicking inside Cursor, or directly click the command
  palette row.

2026-07-03 repair evidence path:

```text
${REDACTED_SECRET}
```
