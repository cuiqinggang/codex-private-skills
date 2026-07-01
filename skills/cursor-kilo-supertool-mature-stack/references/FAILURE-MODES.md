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

Cursor/Kilo UI can keep a stale recent-model state even when `C:\Users\A\.config\kilo\kilo.jsonc` already points to OpenRouter DeepSeek V4 Pro. Symptom: Kilo panel shows `DeepSeek V3.2` and returns a login requirement. Fix with the minimal state repair in `KILO-UI-MODEL-STATE-FIX.md`: back up `state.vscdb` plus sidecars, replace only the stale recent model with `providerID=openrouter` and `modelID=deepseek/deepseek-v4-pro`, then reload Cursor. Do not modify API keys or redeploy the stack.

If the issue returns after reopening Cursor, remove every Kilo/Gateway recent model candidate too. The stable state should have `recentModels` containing only `{"providerID":"openrouter","modelID":"deepseek/deepseek-v4-pro"}`. Do not delete or patch Kilo extension files such as `models-snapshot.json`; their V3.2 entries are catalog entries, not the active user selection.
