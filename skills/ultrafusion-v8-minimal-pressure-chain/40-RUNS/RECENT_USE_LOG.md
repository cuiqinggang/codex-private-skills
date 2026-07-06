# UltraFusion V8 Recent Use Log

## 2026-07-06 - V8.2 Minimal Gate Patch

- Event: upgraded `ultrafusion-v8-minimal-pressure-chain` from V8.1-style minimal pressure chain to UltraFusion V8.2 Minimal Gate Patch.
- Version marker: `UltraFusion V8.2 Minimal Gate Patch`.
- Core rule: V8.2 = V8.1 + Before-A route gate + per-layer EARLY_WARNING + B/C/D anti-degradation validation + D final insurance check.
- Added: `Before_A_Route_Gate` with 2-of-5 route criteria before A; this is not a new layer.
- Added: per-layer `EARLY_WARNING` in A/B/C/D with high/medium/low/none process rules.
- Added: `B_VALIDATION`, `C_VALIDATION`, `D_VALIDATION`, and `D_Final_Insurance_Check`.
- Strengthened: `Score_Consistency_Gate` so concrete Deduction must precede SelfScore and RepairDone; high score with empty/generic deduction must be lowered or rewritten.
- Strengthened: Balance verdict rules for `TOO_THIN`, `TOO_HEAVY`, and `TOO_SLOW`.
- Boundary preserved: no extra layer, no full heavy injection restoration, no long C/D benchmark template restoration.
- Validation target: run `quick_validate.py` if present; otherwise use manual file/gate checks.

## 2026-07-06

- Event: initial skill deployment.
- Source material: `C:\Users\A\Desktop\UltraFusion_V8.0_极简压力链_高性价比版 (1).md`.
- Route bound: `UF_V8_ABCD_MIN`.
- Default role: daily high-cost-performance UltraFusion production chain.
- V7 boundary: keep `ultrafusion-low-cost-multi-model-extreme-fusion` for heavy benchmark / full V15 / official external copy-paste packages.

## 2026-07-06 Network Upload

- Event: uploaded skill package to GitHub.
- Repository: `cuiqinggang/codex-private-skills`.
- Remote path: `skills/ultrafusion-v8-minimal-pressure-chain`.
- Commit: `e678e705d2528f121cb27a30c55e0de76e921b39`.
- Verified URL: `https://github.com/cuiqinggang/codex-private-skills/blob/main/skills/ultrafusion-v8-minimal-pressure-chain/SKILL.md`.

## 2026-07-06 Official Web Critique Test

- Test route: ordinary coordinate screenshot method on official DeepSeek and Qwen pages.
- DeepSeek official page: PASS for prompt paste/send/answer generation after UI repair.
- Qwen official page: PARTIAL; current `?bizPassParams=...externalH5` page did not accept input focus through existing mature coordinates and needs a new coordinate branch or standard-entry normalization.
- V8 content finding: the first V8 template can cause mixed or repeated scoring blocks; templates now require exactly one final `Deduction / SelfScore / RepairDone` block.
- Product finding: V8 must optimize `quality / architecture / speed`, not quality alone.
- Skill update: added `Quality-Architecture-Speed Balance Gate`, anti-degradation gates for B/C/D, and `Balance` output fields.

## 2026-07-06 - DeepSeek upload-safe 140 package

- Issue: Desktop 139 package triggered DeepSeek upload warnings: unsupported format and max 50 files.
- Cause: 139 had 189 files and 139.zip was not accepted by DeepSeek web upload.
- Fix: created Desktop\140 as TXT-only flattened upload package.
- Reusable rule: see references\DEEPSEEK_UPLOAD_SAFE_PACKAGE_RULE_20260706.md.

## 2026-07-06 - Qwen single-document 141 package

- Issue: Qwen upload UI showed document upload constraints after 140.
- Cause: 140 is upload-safe for DeepSeek, but Qwen is more reliable with one Word document than a folder/multi-file pack.
- Fix: created Desktop\141 and Desktop\141_先上传这个到千问.docx.
- Reusable rule: see references\QWEN_SINGLE_DOC_UPLOAD_RULE_20260706.md.

## 2026-07-06 - Qwen single-document 141 package

- Issue: Qwen upload UI showed document upload constraints after 140.
- Cause: 140 is upload-safe for DeepSeek, but Qwen is more reliable with one Word document than a folder/multi-file pack.
- Fix: created Desktop\141 and Desktop\141_先上传这个到千问.docx.
- Reusable rule: see references\QWEN_SINGLE_DOC_UPLOAD_RULE_20260706.md.
