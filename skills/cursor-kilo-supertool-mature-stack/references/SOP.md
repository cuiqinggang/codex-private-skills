# SOP: Reproduce Cursor + Kilo SuperTool Mature Stack

## 1. Preflight

1. Confirm the user wants mature reproduction, not experimental tool search.
${REDACTED_SECRET}
3. Check current Kilo config without printing secrets:
${REDACTED_SECRET}
4. Confirm:
   - default model remains DeepSeek V4 Pro
   - snapshot is false
   - Auto Free and Gateway are not forced
   - API keys are not printed or changed

## 2. Tool Route

1. Use Cursor + Kilo Code as main agent route.
2. Keep Cline as fallback only.
3. Do not continue Claude Code login bypass.
4. Do not install extra agents during analysis-only stages.

## 3. Provider Route

1. Use OpenRouter provider IDs visible through Kilo.
2. Keep direct keys private.
3. Avoid environment/network/proxy changes unless explicitly requested.
4. If the user asks whether a provider/model really works, run live smoke verification; do not accept config-only proof as final.
5. Use `LIVE-SMOKE-RECOVERY.md` and `scripts/run_openrouter_live_model_smoke.ps1` when OpenRouter live verification is authorized.

## 4. Model Routing

1. Normal code: DeepSeek V4 Pro.
2. Complex instructions, gate review, repair loops: GLM-5.2.
3. Screenshot/UI/OCR/chart/video keyframes: Qwen3-VL-235B-A22B-Instruct.
4. Hard visual reasoning: Qwen3-VL-235B-A22B-Thinking.
5. Light tasks: DeepSeek V4 Flash only if stable.

## 5. Visual/Video Route

1. Prefer image attachments and contact sheets.
2. Use video keyframes for recording analysis.
3. Record direct-video status as:
   `DIRECT_VIDEO_INPUT_NOT_TESTED_KEYFRAME_ROUTE_USED`
4. Do not claim direct video PASS unless it was actually tested.

## 6. UI Verification Route

1. For UI settings/model selection/localization, use actual open + screenshot evidence.
2. If the user says visible UI automation is surprising or unwanted, stop UI automation.
3. Use CLI/log evidence instead and mark UI verification caveats honestly.
4. If Kilo UI falls back to `DeepSeek V3.2` or a login-gated Kilo model while the intended route is OpenRouter DeepSeek V4 Pro, use `KILO-UI-MODEL-STATE-FIX.md` for the minimal Cursor state repair. Do not redeploy the whole stack for this issue.

## 7. Packaging

${REDACTED_SECRET}
2. Include evidence, logs, model results, benchmark files, and secret-scan summary.
3. Create a ZIP package.
4. Always create a compact desktop numeric handoff package after a completed report/task:
   - If the user names a number, use that exact number.
${REDACTED_SECRET}
${REDACTED_SECRET}
   - Include the final report, evidence ZIP, and key files/README.
   - Back up existing same-name folder/ZIP before replacing.
   - Exclude browser profiles, caches, node_modules, and bulky source trees unless explicitly requested.
5. Mention the desktop numeric ZIP path in the final answer.

## 8. Continuous Skill Sync

After each completed stage, run `scripts/sync_stage.py` with:

- stage name
- final status
- report or package path
- short lesson

This keeps mature experience from being lost before a final summary.

## 9. Recovery And Verification Logic

1. For restoring the mature station, start from `FULL-DEPLOY-ARTIFACTS.md`.
2. For gate/verification bugs, apply `VERIFICATION-LOGIC.md`.
3. Verification must detect success signals and failure signals. Do not mark all cycles FAIL only because one anomaly pattern exists.
4. Final acceptance requires evidence-backed claim review, not only script output or ZIP existence.
