# UltraFusion V8 Recent Use Log

## 2026-07-06 - V8.2-RC2 Minimal Repair Patch

- Event: upgraded V8.2-RC1 to V8.2-RC2 with the smallest remaining gate repairs.
- P0 landed: A/B/C/D output now requires per-layer `EARLY_WARNING` with `Balance: OK / WARN`.
- P1 landed: C now has `C_Content_Density_Gate` to prevent placeholder FusionNotes from passing.
- P2 landed: B and D rerun instructions now include negative examples for commentary-only and polishing-only failures.
- Score gate landed: SKILL.md and A/B/C/D templates now include numeric caps: 0 concrete deductions => SelfScore <= 7.0; 1 concrete deduction => SelfScore <= 8.0; 2+ concrete deductions may be 8.5+.
- Run summary updated: added `V8_2_RC2_Checks`.
- Failure review updated: added C placeholder/generic-field failures, final-only Balance failure, missing layer EARLY_WARNING, and generic Deduction with high SelfScore.
- Boundary preserved: no extra layer, no full heavy injection restoration, no long C/D benchmark template restoration.
- Network upload: GitHub `cuiqinggang/codex-private-skills`, path `skills/ultrafusion-v8-minimal-pressure-chain`.
- Network commit verified: `2a2c405f071331a73b21378604358b95f0ae464a`.
- Remote check: `SKILL.md` contains `UltraFusion V8.2-RC2 Minimal Gate Patch`, `C_Content_Density_Gate`, and `SelfScore MUST be <= 7.0`.

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

## 2026-07-06 - Desktop 451 dual upload package

- Event: created a platform-specific upload package for the already accepted V8.1 -> V8.2 material.
- Desktop path: `C:\Users\A\Desktop\451`.
- DeepSeek route: use `01_DeepSeek_TXT版_上传这个\451_先上传这个到DeepSeek.txt`; do not upload ZIP or the whole folder.
- Qwen route: use `02_阿里千问_Qwen_DOCX版_上传这个\451_先上传这个到阿里千问.docx`; upload the DOCX file itself, not the folder.
- Qwen fallback: use `451_阿里千问_DOCX失败时再用这个TXT.txt` only if DOCX upload fails.
- Local reference: `03_本地完整参考_不用上传`.
- Validation: DeepSeek package has 3 files; Qwen package has 1 primary DOCX; no ZIP files in `451`; DOCX contains standard `word/document.xml`.

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
