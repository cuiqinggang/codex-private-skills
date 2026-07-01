# Full Deploy Artifacts

Use this reference to recover the mature super tool station without re-reading the whole chat.

## Current Canonical Roots

- Station root: `C:\Users\A\Desktop\AI_Coding_SuperTool_Ecosystem_Station`
- Run root: `C:\Users\A\Desktop\ClaudeCode_Outputs\Mature_AI_Coding_SuperTool_Ecosystem_Station_Full_Deploy_Run`
- Main package: `C:\Users\A\Desktop\ClaudeCode_Outputs\Mature_AI_Coding_SuperTool_Ecosystem_Station_Full_Deploy_Package.zip`
- Latest compact handoff: `C:\Users\A\Desktop\391.zip`

## Important Files

- Model matrix: `C:\Users\A\Desktop\AI_Coding_SuperTool_Ecosystem_Station\models\model_matrix.json`
- Routing policy: `C:\Users\A\Desktop\AI_Coding_SuperTool_Ecosystem_Station\models\model_routing_policy.json`
- Live smoke evidence: `C:\Users\A\Desktop\ClaudeCode_Outputs\Mature_AI_Coding_SuperTool_Ecosystem_Station_Full_Deploy_Run\evidence\openrouter_live_model_smoke_verification.json`
- Live smoke report: `C:\Users\A\Desktop\ClaudeCode_Outputs\Mature_AI_Coding_SuperTool_Ecosystem_Station_Full_Deploy_Run\reports\OpenRouter_Live_Model_Smoke_Verification_Report.md`
- Continuous verification report: `C:\Users\A\Desktop\ClaudeCode_Outputs\Mature_AI_Coding_SuperTool_Ecosystem_Station_Full_Deploy_Run\continuous_system_verification\system_verification_report.json`
- Final verdict: `C:\Users\A\Desktop\ClaudeCode_Outputs\Mature_AI_Coding_SuperTool_Ecosystem_Station_Full_Deploy_Run\continuous_system_verification\final_verdict.txt`

## Latest Known Status

`ACCEPTED`

The four OpenRouter model routes were live-call verified:

- DeepSeek V4 Pro
- DeepSeek V4 Flash
- GLM-5.2
- Qwen3-VL-235B-A22B-Instruct

## Recovery Flow

1. Inspect `model_matrix.json` and `model_routing_policy.json`.
2. Inspect `final_verdict.txt`.
3. If live provider proof is required, run `scripts/run_openrouter_live_model_smoke.ps1`.
4. Rebuild the compact desktop numeric package with `scripts/create_desktop_numeric_package.ps1`.
5. Run `scripts/sync_stage.py` after any meaningful repair or verification.

## Cleanup Rule

Keep the station compact:

- Do not regenerate thousands of cycle files unless explicitly required.
- Keep checkpoints summarized when possible.
- Preserve final acceptance, evidence, reports, model matrix, routing policy, and package manifest.
- Exclude browser profiles, cache folders, `node_modules`, temp folders, and old ZIP staging roots from handoff ZIPs.
