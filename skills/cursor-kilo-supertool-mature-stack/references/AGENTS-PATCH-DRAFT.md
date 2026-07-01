# AGENTS.md Patch Draft

Add this only if the user wants the rule promoted globally.

```markdown
## Cursor/Kilo SuperTool Mature Stack Rule

When tasks mention Cursor/Kilo super tool, Kilo First, OpenRouter model routing, DeepSeek V4 Pro, GLM-5.2, Qwen3-VL, provider/model verification, UI localization, Serena dashboard noise, mature stack deployment, or Stage4/Stage5 continuation, use:

`C:\Users\A\.codex\skills\cursor-kilo-supertool-mature-stack`

Before acting:

1. Read `references/HANDOFF-SUMMARY.md`.
2. Preserve safety boundaries: no full API key printing, no API key edits, no Hermes Gateway edits, no Qwen direct config edits, no proxy/network changes unless explicitly requested.
3. Keep DeepSeek V4 Pro as default executor, GLM-5.2 as strong controller, and Qwen3-VL-235B-A22B-Instruct as vision primary unless a newer verified report supersedes it.
4. After every completed stage, run `scripts/sync_stage.py` to append the stage outcome and artifact path into the skill log.
```
