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
C:\Users\A\AppData\Roaming\Cursor\User\settings.json
C:\Users\A\AppData\Roaming\Cursor\User\globalStorage\kilocode.kilo-code
C:\Users\A\AppData\Roaming\Cursor\User\globalStorage
C:\Users\A\.cursor
C:\Users\A\.kilocode
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
C:\Users\A\AppData\Roaming\Cursor\User\globalStorage\state.vscdb
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
- `C:\Users\A\.config\kilo\kilo.jsonc` still had `model = openrouter/deepseek/deepseek-v4-pro` and `snapshot = false`.
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
C:\Users\A\Desktop\ClaudeCode_Outputs\kilo-model-config-backup-YYYYMMDD-HHMMSS
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
