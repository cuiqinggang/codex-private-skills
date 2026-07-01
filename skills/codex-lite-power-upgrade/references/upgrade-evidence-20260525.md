# 2026-05-25 Codex Lite Power Upgrade Evidence

Task ID: `CODEX-DESKTOP-LITE-POWER-UPGRADE-20260525`

Final status: `CODEX_DESKTOP_LITE_POWER_UPGRADE_PASS`

Evidence root:

```text
C:\Users\A\Desktop\1\output\CODEX-DESKTOP-LITE-POWER-UPGRADE-20260525
```

## Stable Version Evidence

- Codex CLI before/after: `codex-cli 0.133.0`
- npm global package before/after: `@openai/codex@0.133.0`
- npm `latest` dist-tag: `0.133.0`
- npm `alpha` dist-tag observed but not installed: `0.134.0-alpha.3`
- Codex Desktop app: `OpenAI.Codex 26.519.5221.0`
- winget/MS Store result: no newer Codex package available

Official sources used:

- `https://github.com/openai/codex/releases`
- `https://www.npmjs.com/package/@openai/codex`
- `winget` / Microsoft Store source for Desktop app

## Preserved State

- `C:\Users\A\.codex\config.toml` kept `model = "gpt-5.5"`.
- Superpowers plugin remained enabled.
- Browser/browser-use/Chrome capabilities remained enabled.
- GitHub CLI and GitHub skills remained available.
- DeepSeek-related local fallback/provider knowledge remained present but was not made default.
- Hermes/OpenWebUI/Xiaolongxia configurations were not changed.

## Backup And Rollback

Full backup:

```text
C:\Users\A\Desktop\1\output\CODEX-DESKTOP-LITE-POWER-UPGRADE-20260525\backup.codex-20260525-235342
```

Direct global AGENTS rollback:

```text
C:\Users\A\.codex\AGENTS.md.bak.lite-power.20260525-235736
```

To roll back only global rules, copy the direct AGENTS backup over:

```text
C:\Users\A\.codex\AGENTS.md
```

## Files Created Or Changed

- Changed: `C:\Users\A\.codex\AGENTS.md`
- Created: `G06-plugin-skill-curation.md`
- Created: `final-report.md`
- Created smoke project under `smoke-project\`

The global `AGENTS.md` was shortened to 78 lines / 3373 bytes and kept these rules:

- load `yesterday-replay-controlled-coding` first
- diagnose, plan, make minimal changes, verify
- use Superpowers-style workflow for non-trivial tasks
- prefer mature existing paths and official sources
- do not install unrelated dependencies or prerelease tools
- preserve rollback paths
- report PASS/FAIL evidence

## Plugin And Skill Curation

Keep/enabled:

- `superpowers@openai-curated`
- `browser@openai-bundled`
- `browser-use@openai-bundled`
- `chrome@openai-bundled`
- `yesterday-replay-controlled-coding`
- `chatgpt-screenshot-bridge`
- `openai-docs`, `playwright`, `screenshot`, `doc`, `pdf`, `spreadsheet`
- `gh-fix-ci`, `gh-address-comments`

Optional:

- `hyperframes@openai-curated`
- `hugging-face@openai-curated`
- `vercel@openai-curated`
- `remotion@openai-curated`
- domain-specific local skills for Hermes, Xiaolongxia, AI-token business, ComfyUI, and system evolution

Review later, no deletion performed:

- `chatgpt-cdp-browser`
- `chatgpt-clipboard-bridge`
- `plugins\cache\openai-curated\plugin-backup-k7QkR5`
- `plugins\cache\openai-curated\plugin-install-uf2Cck`

## Smoke Test Evidence

Created:

- `smoke-project\README.md`
- `smoke-project\smoke.py`
- `smoke-project\index.html`
- `smoke-project\codex-context-summary.md`

Python output:

```text
CODEX_LITE_POWER_UPGRADE_SMOKE_OK
PYTHON_EXIT_CODE=0
```

Browser output:

```text
OPEN_EXIT_CODE=0
SNAPSHOT_EXIT_CODE=0
SCREENSHOT_EXIT_CODE=0
SNAPSHOT_HAS_MARKER=True
```

Screenshot:

```text
C:\Users\A\Desktop\1\output\CODEX-DESKTOP-LITE-POWER-UPGRADE-20260525\logs\G07-smoke-page-rerun.png
```

## Known Pitfalls Found During The Upgrade

- Playwright CLI blocked direct `file:` protocol pages. Use a local HTTP server for smoke HTML.
- Playwright CLI screenshot option is `--filename`, not `--path`.
- A missing favicon can create console noise in the smoke page; use `<link rel="icon" href="data:,">`.
- Do not use lack of Store GUI interaction as a failure when winget/MS Store source already reports no newer stable package.
