# Rule Patch 2026-07-06: UltraFusion V8 Minimal Pressure Chain

## Trigger Phrases

- UltraFusion V8.0
- 极简压力链
- 高性价比生产版
- ABCD 极简
- UF_V8_ABCD_MIN
- SelfScore / Deduction / RepairDone
- Gain 验收

## Rule

For daily complex/high-value answer work, prefer `ultrafusion-v8-minimal-pressure-chain` over the heavier V7.0 benchmark skill unless the user explicitly asks for full V15, official C/D prompt packages, external model copy-paste benchmarking, or complete audit trace.

## Boundary

Keep `ultrafusion-low-cost-multi-model-extreme-fusion` as the V7.0 heavy benchmark route.

## Acceptance Criteria

- Skill has valid `SKILL.md` frontmatter.
- A/B/C/D templates exist.
- Recent-use log exists.
- Failure-review entry exists.
- Knowledge note exists in the Obsidian AI Company OS vault.
- Knowledge Brain health check and hot sync are run after deployment.
