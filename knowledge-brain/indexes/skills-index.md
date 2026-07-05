# Skills Index

Generated: 2026-06-17 00:55:12

Codex skills: C:\Users\A\.codex\skills (85+ entries)
Hermes skills: C:\Users\A\.hermes\skills
K drive: K:\AI\skills

## Recent Skill Additions

- 2026-07-05: `C:\Users\A\.codex\skills\ultrafusion-low-cost-multi-model-extreme-fusion` — UltraFusion V7.0 semi-automatic ABCD upgrade
  - Purpose: reusable semi-automatic multi-layer answer workflow where Codex generates copy-paste question packages, the human only copies/pastes, external models answer, and Codex fuses, converges, scores, and judges gain.
  - Route label: `UF_V7_SEMI_AUTO_ABCD`.
  - Method: baseline `Score_0`, A extreme generation, B fusion enhancement, C strategy integration, D final convergence, then compare `Score_0` vs `SCORE_FINAL`.
  - Hard gate: `Gain = SCORE_FINAL - Score_0`; `Gain < 2.0` is `INVALID_CHAIN`.
  - Trigger phrases: `UltraFusion V7.0`, `半自动ABCD`, `ABCD问题包`, `复制粘贴多层推理`, `外部模型回答`, `Score_0 vs Score_FINAL`, `Gain < 2`.
  - Knowledge note: `C:\Users\A\.codex\obsidian-vaults\AI-COMPANY-KNOWLEDGE-OS\03_SKILL_ASSETS\UltraFusion-V7-Semi-Auto-ABCD-20260705.md`.
  - GitHub target: `cuiqinggang/codex-private-skills`, single package under `skills/ultrafusion-low-cost-multi-model-extreme-fusion`.
  - V15 canonical source correction: V7.0 ABCD packages must inject full `10-SPEC\V15_FULL_WITH_GUARD_v1.0.md`; SHA256 `BB836AC959885190A1BEC81ECA77454F0CD183D08BB3814070A977C39147514E`. User attachment from 2026-07-05 trim-matches the canonical 332-line V15+G source. Short summaries/placeholders/wrong V15 versions invalidate the layer.
  - C layer official prompt lock: C packages must use `30-TEMPLATES\C_LAYER_OFFICIAL_FUSION_PROMPT_v20260706.md`; SHA256 `8095B50C31E8FB31B506BC53278BC053C439743E17ACA40F37FACDBC99085BA2`. Required signals: `复检陌生稿规则`, `四维稠密融合`, evidence/data hard rules, reverse consistency checks, `【最终答案：C_Fusion】`, `【评审报告】`, `【版本说明】`. Simplified C prompts invalidate the layer.
  - D layer execution command first: D packages must start with `30-TEMPLATES\D_LAYER_EXECUTION_COMMAND_WRAPPER_v20260706.md`; first visible instruction must say `【执行命令：立即执行 UltraFusion V7.0 D 层，不要总结文件】`. If an external model summarizes the package as a framework/prompt-injection object instead of executing, send the correction command and treat the first output as invalid.

- 2026-07-05: `C:\Users\A\.codex\skills\one-person-saas-os`
  - Purpose: deployable low-stable one-person SaaS OS generator for Next.js App Router + TypeScript + Tailwind with Clerk, Supabase, PostHog, Vercel, and Git/GitHub-ready structure.
  - Method: use `scripts\create_one_person_saas_os.py` to generate the project instead of rewriting boilerplate; keep v1 free of Stripe, payment webhooks, Redis/Upstash, vector DB, multi-service orchestration, and complex backend layers.
  - Growth/payment update: preserved a complete first-dollar Codex SaaS case study; added copyable overseas link-platform table, X/Twitter comment tactic, Paddle/Creem/Stripe route notes, website readiness checklist, and Hong Kong Stripe anecdote with compliance boundaries.
  - Trigger phrases: `RUN one-person-saas-os`, `一人公司 SaaS`, `SaaS 操作系统`, `低成本 SaaS 部署`, `多智能体极限低成本答案 项目部署`, `Next.js Clerk Supabase PostHog Vercel`.
  - Validation: `quick_validate.py` PASS; smoke project generated; `npm install` PASS; `npm run build` PASS on Next.js 15.5.20.
  - Knowledge note: `C:\Users\A\.codex\obsidian-vaults\AI-COMPANY-KNOWLEDGE-OS\03_SKILL_ASSETS\One-Person-SaaS-OS-Skill-20260705.md`.
  - Acceptance: `C:\Users\A\Documents\Codex\2026-07-05\skill-name-one-person-saas-os\outputs\one-person-saas-os-skill-acceptance-20260705.html`.

- 2026-07-05: `C:\Users\A\.codex\skills\hermes-telegram-persistent-bridge`
  - Purpose: reusable repair route for Hermes Telegram/OpenWebUI stalls where phone Telegram shows `Working -- 3 min`, typing starts/stops, trivial messages are delayed, or C/H/K launch roots conflict.
  - Rule: `C:\Users\A\Hermes_Windows_Native_014` is the hot runtime path; `K:\AI`, `K:\Hermes...`, and `H:\Hermes...` are backup/reference/disaster-recovery unless explicitly requested.
  - Repair evidence: mixed gateway roots removed from editable hot-path scripts; diagnostic uses C-drive CLI; Telegram/API/OpenWebUI PASS; short API answer improved from 38.43s to 4.29s after C hot-path repair and API toolset narrowing.
  - Reference: `C:\Users\A\.codex\skills\hermes-telegram-persistent-bridge\references\incident-2026-07-05-c-hotpath-telegram-working-stall.md`.
  - Knowledge note: `C:\Users\A\.codex\obsidian-vaults\AI-COMPANY-KNOWLEDGE-OS\03_SKILL_ASSETS\Hermes-Telegram-C-Hotpath-Working-Stall-20260705.md`.

- 2026-07-04: `C:\Users\A\.codex\skills\c-drive-hotpath-default`
  - Purpose: enforce the user's default disk policy that active runtime, saves, generated outputs, caches, temp files, logs, app launchers, scheduled tasks, Codex work, AI tools, Knowledge Brain hot paths, and CodeGraph hot scans should use the C-drive SSD by default.
  - Method: preflight check for non-C hot-path leaks in command lines, scheduled tasks, process lists, temp paths, output/input/cache directories, and long-running workflows.
  - Root cause fixed: ComfyUI was running from `C:\AI` but input/output/temp were explicitly configured to `D:\AI_ComfyUI_Outputs`; future paths now use `C:\AI\ComfyUI_Aaki_v3\data`.
  - Trigger phrases: `D盘发热`, `机械盘很烫`, `默认放C盘`, `不要用D盘运行`, `输出到C盘`, `临时目录到C盘`, `机械盘只做普通盘`, `C盘热路径`.
  - Knowledge note: `C:\Users\A\.codex\obsidian-vaults\AI-COMPANY-KNOWLEDGE-OS\01_META\C-Drive-Hotpath-Default-Rule-20260704.md`.
  - Acceptance: `C:\Users\A\Documents\Codex\2026-07-04\new-chat\outputs\d-drive-heat-diagnostic-20260704.html`.

- 2026-07-03: `C:\Users\A\.codex\skills\cursor-kilo-supertool-mature-stack` — ASSET-SEARCH-PATHS update
  - Purpose: prevent AI assistant search-scope misjudgments by documenting the complete 4-layer asset architecture.
  - New file: `references\ASSET-SEARCH-PATHS.md` — documents all canonical paths for Kilo config, agent skills, knowledge brain indexes, and ecosystem station.
  - Updated: `SKILL.md` (added Step 0 to Start Workflow + Key References entry), `HANDOFF-SUMMARY.md` (added Asset Search Path Architecture section + updated date).
  - Root cause fix: 2026-07-03 session initially scored 30% maturity by scanning only Layer 1; actual maturity is 88% when all 4 layers are scanned.
  - Trigger phrases: `搜索路径`, `资产位置`, `成熟度评估`, `搜索范围`, `4层架构`, `asset search paths`.

- 2026-07-03: `C:\Users\A\.codex\skills\kilo-codex-claude-permission-guard`
  - Purpose: unified permission boundary for Codex Desktop, Kilo Code, Claude Code/ECC, and Hermes: ordinary project work runs directly; Windows core and network/proxy changes require approval.
  - Repair: Codex config drift found at `[windows] sandbox = 'unelevated'`; restored to `sandbox = "elevated"` after backups `20260703-212006`.
  - Kilo check: `openrouter/deepseek/deepseek-v4-pro` retained; `snapshot=false` retained; no API keys, gateway, Hermes, proxy, DNS, firewall, Docker, WSL, registry, services, or scheduled tasks changed.
  - Skill redeploy: C-drive Knowledge Brain first paths restored in `SKILL.md`; recent-use log updated.
  - Knowledge note: `C:\Users\A\.codex\obsidian-vaults\AI-COMPANY-KNOWLEDGE-OS\03_SKILL_ASSETS\Kilo-Codex-Claude-Hermes-Permission-Guard-Redeploy-20260703.md`.
  - Acceptance: `C:\Users\A\Documents\Codex\2026-07-03\codex-ki-lo-kilo\outputs\permission-guard-redeploy-20260703.md`.

- 2026-07-03: `C:\Users\A\.codex\skills\codex-quota-panel`
  - Purpose: repair and harden the compact bottom-right Codex quota label when it remains visible but stops showing live quota.
  - Root cause pattern: the 3-minute UI timer can keep repainting while internal `cclimits.py --codex --json` calls time out and the label repeats expired last-good cache.
  - Method: robust temp-file cclimits capture, full query process-tree kill on timeout, `QuotaPanelSelfHeal.ps1`, and Windows scheduled task `CodexQuotaPanelSelfHeal` every 5 minutes.
  - Proven result: installer returned `PASS: quota panel hardened`; log refreshed live value `71% 21:57 | 7天48% 3天20时`; scheduled task state `Ready`.
  - Knowledge note: `C:\Users\A\.codex\obsidian-vaults\AI-COMPANY-KNOWLEDGE-OS\03_SKILL_ASSETS\Codex-Quota-Panel-Self-Heal-20260703.md`.

- 2026-07-02: `C:\Users\A\.codex\skills\ultrafusion-6-0-kimi-no-deepseek`
  - Purpose: memorable alias for the long UltraFusion skill name; user-facing name is `6.0 大模型变动`.
  - Meaning: follows the v5.0 lineage but changes the official model route from DeepSeek-core to Kimi-core.
  - Canonical active skill: `C:\Users\A\.codex\skills\ultrafusion-low-cost-multi-model-extreme-fusion`.
  - Official 6.0 route: GPT official site + Kimi official membership + GLM-5.2 / GLM Coding Plan.
  - DeepSeek status: removed from official core route; retained only as backup/test/pure-reasoning/reverse-review.
  - Trigger phrases: `6.0`, `大模型变动`, `多智能体极限低成本回答6.0`, `Kimi替代DeepSeek`, `去DeepSeek`, `DeepSeek变Kimi`.
  - Backup: `K:\AI\skills\ultrafusion-6-0-kimi-no-deepseek`.

- 2026-07-02: `C:\Users\A\.codex\skills\knowledgebrain-cleanup-governance`
  - Purpose: reusable no-delete governance workflow for Knowledge Brain, Codex Documents, Obsidian, workspace, skill package, and agent reference cleanup.
  - Method: Knowledge Brain first; explicit-root inventory; classify into cold archive, rebuildable quarantine, keep-active, and human-review; plan mode before execute; manifest-backed moves; rollback commands; long-path residual mapping; post-cleanup audit, health check, and two light sync passes.
  - Proven result: Round 2 moved 330 manifest rows, 50,224 files, 3.885 GB; all-source audit `PARTIAL_TIMEOUTS=0`; health check PASS; two light sync passes with `TIMEOUT=0` and `ERROR=0`.
  - Backup: `K:\AI\skills\knowledgebrain-cleanup-governance`.
  - Report: `C:\Users\A\Desktop\KnowledgeBrain_Cleanup_Round2_Final_Report_20260702-033600.md`.

- 2026-07-01: `C:\Users\A\.codex\skills\digital-product-indie-site`
  - Purpose: reusable workflow and preserved source package for cloning overseas digital product indie sites that list digital products, collect USD/foreign-currency payments, and automatically deliver downloads or access after checkout.
  - Method: prefer Lemon Squeezy / Payhip / Gumroad hosted checkout and delivery first; use Next.js / Framer / Webflow for the indie-site shell; require product pages, license/refund terms, success page, email/download delivery, and seller order records.
  - Preserved package: original ZIP stored under `assets\original-package`; SHA256 `D4D75E8809110D6E5B7DBC34CFABD6962DD2004934A61C854B6EF2480E4A3595`.
  - Backup: `K:\AI\skills\digital-product-indie-site`.
  - Acceptance evidence: `C:\Users\A\Documents\Codex\2026-07-01\new-chat-6\outputs\digital-product-indie-site-skill-deployment-20260701.html`.
- 2026-06-28: `K:\AI\skills\best-answer-ai-service`
  - Purpose: durable project memory and execution guide for Best Answer AI / UltraFusion Engine, including product positioning, mature web SaaS path, UltraFusion A/B/C/D workflow, runtime parameters, pricing/cost control, web MVP, validation tests, and continuous memory rules.
  - Method: web-first, English-first, outcome-first; prove answer quality and willingness to pay before domains, trademarks, mobile apps, or complex architecture; preserve new decisions in structured `references/` files.
  - Proven result: deployed to K drive and Codex local skill path; archived original package; three-digit desktop delivery `C:\Users\A\Desktop\016.zip`; SHA256 `62B4A76C95FDEC15FE22D172676146817E2D8C35786A76B8C08E3C6F6913BD83`.
  - Codex trigger entry: `C:\Users\A\.codex\skills\best-answer-ai-service`.
- 2026-06-28: `K:\AI\skills\windows-c-drive-clone-cleanup`
  - Purpose: reusable Windows C drive scan, safe cleanup, and HDD-to-SSD system clone readiness workflow.
  - Method: scan-only first; classify temp/cache/recycle as safe cleanup; preserve Desktop, Codex, skills, Docker, models, and user project folders unless reviewed; compare C partition size with target SSD capacity before cloning.
  - Proven result: C used reduced from 211.08 GB to 204.61 GB on 2026-06-28; found C partition 3725.91 GB and target SSD 698.64 GB, so resize-aware migration is required.
  - Codex trigger entry: `C:\Users\A\.codex\skills\windows-c-drive-clone-cleanup`.
- 2026-06-27: `K:\AI\skills\skills-codegraph-governance-343`
  - Purpose: reusable governance workflow for skills, plugins, skill packs, large skills, quarantine/archive manifests, CodeGraph layer registration, and 326 writeback.
  - Method: asset-level inventory only, five-layer classification, large asset deep-clean gates, no-delete rollback records, and human-review blocking when risk remains.
  - Proven result: `SKILLS_343B_BLOCKED_NEEDS_HUMAN_REVIEW`, `CORE_VALIDATION_PASS`, `NO_SECRET_PATTERN_FOUND`, delivery `C:\Users\A\Desktop\008.zip`.
  - Codex trigger entry: `C:\Users\A\.codex\skills\skills-codegraph-governance-343`.
- 2026-06-27: `K:\AI\skills\326-karpathy-llm-wiki-first-real-ingest`
  - Purpose: preserve the proven 341 flow for 326 core + Obsidian + Karpathy LLM Wiki first real ingest.
  - Method: provider gate through Karpathy/OpenRouter, real plugin ingest, controlled 326 writeback, overflow page cleanup, three-digit ZIP delivery.
  - Proven result: `FIRST_REAL_INGEST_PASS`, `20/20 PASS`, `CORE_VALIDATION_PASS`, 15 active wiki pages, delivery `C:\Users\A\Desktop\006.zip`.
  - Codex trigger entry: `C:\Users\A\.codex\skills\326-karpathy-llm-wiki-first-real-ingest`.
- 2026-06-27: `K:\AI\skills\github-version-upgrade-mature-flow`
  - Purpose: fixed version-upgrade method for GitHub saves/releases.
  - Method: search mature skill packages first, then reuse the copied mature GitHub publish workflow.
  - Copied mature source: `C:\Users\A\.codex\plugins\cache\openai-curated-remote\github\0.1.5\skills\yeet\SKILL.md`.
  - Adoption route: `ADOPT_DIRECTLY`.
- 2026-06-27: `K:\AI\skills\github-version-save-profile`
  - Purpose: user GitHub version-save profile and trigger entry.
  - Bound workflow: routes future "保存版本 / 保存到 GitHub / 推送这个版本" requests to `K:\AI\skills\github-version-upgrade-mature-flow`.
- 2026-06-19: `C:\Users\A\.codex\skills\ui-setting-actual-open-self-verify-loop`
  - Purpose: enforce actual-open screenshot verification for UI settings, plugin settings, localization, model/provider selection, workspace restoration, and UI panel tasks.
  - Required final statuses: `ACTUAL_OPEN_VERIFY_PASS`, `PARTIAL_PASS_WITH_SCREENSHOT_EVIDENCE`, `FAIL_NEEDS_FURTHER_FIX`.
- 2026-06-20: `C:\Users\A\.codex\skills\cursor-kilo-supertool-mature-stack`
  - Purpose: preserve and reproduce the mature Cursor + Kilo Code + OpenRouter SuperTool route.
  - Core matrix: DeepSeek V4 Pro executor, GLM-5.2 controller, Qwen3-VL-235B-A22B-Instruct vision primary, Qwen3-VL Thinking backup.
  - Includes per-stage sync script: `scripts\sync_stage.py`.

- 2026-06-28: `K:\AI\skills\skills-codegraph-governance-343` 343C
  - Purpose: 9 HUMAN_REVIEW_REQUIRED targets received human-readable inspection, decision matrix, 343D candidate actions, blocked reasons, and medium-risk user questions.
  - Result: `SKILLS_343C_HUMAN_REVIEW_INSPECTION_PASS`; this is inspection pass, not cleanup pass.

- 2026-06-28: `K:\AI\skills\skills-codegraph-governance-343` 343D
  - Purpose: applied user-confirmed safe archive/tag-only/blocked decisions for 9 targets.
  - Method: copy-verify-archive for 3 archive candidates; no delete; metadata-only 326 writeback.

- 2026-06-28: `K:\AI\skills\skills-codegraph-governance-343` 344
  - Purpose: knowledge callability verification for 326 query/routing/writeback/new-skill-index/CodeGraph layer.
  - Result: `KNOWLEDGE_CALLABILITY_344_PASS`.

- 2026-06-28: `K:\AI\skills\skills-codegraph-governance-343` 344
  - Purpose: knowledge callability verification for 326 query/routing/writeback/new-skill-index/CodeGraph layer.
  - Result: `KNOWLEDGE_CALLABILITY_344_PASS`.

- 2026-06-28: `345S graph route decision`
  - Purpose: left/right candidate graph audit plus mature solution route decision for 326 visual graph upgrade.
  - Result: `GRAPH_ROUTE_DECISION_345S_PASS`; recommended `D + C` for 346 confirmation.

- 2026-06-28: `K:\AI\skills\cursor-kilo-terminal-paste-repair`
  - Purpose: reusable repair flow for Cursor/Kilo/Claude Code integrated terminal paste failures when the clipboard works elsewhere.
  - Root cause pattern: clipboard and Kilo can be healthy while Cursor fails to route `Ctrl+V` to `workbench.action.terminal.paste` under terminal focus.
  - Method: check clipboard formats, Kilo/Cursor process health, long-text converter status, then merge terminal-focused `Ctrl+V` and `Shift+Insert` keybindings with backup and visual verification.
  - Proven result: `TERMINAL_PASTE_REPAIR_PASS` on 2026-06-28; harmless probe pasted into the real Cursor/Kilo PowerShell terminal and was not executed.
  - Codex trigger entry: `C:\Users\A\.codex\skills\cursor-kilo-terminal-paste-repair`.

- 2026-06-30: `K:\AI\skills\codex-desktop-clean-reinstall-skill-recovery`
  - Purpose: reusable recovery workflow for Codex Desktop zombie-process syndrome, where Codex processes are running but no window appears.
  - Root cause pattern: all Codex processes have `MainWindowHandle=0` and empty `MainWindowTitle`, so relaunch attaches to stale background processes instead of opening a new UI.
  - Method: kill Codex processes first; only if needed, perform temporary skill cold-start with `.system` retained, verify a visible window, then restore all skills.
  - Proven result: Codex recovered on 2026-06-30 with 108 local skills restored; at least one Codex process has a visible window handle.
  - Codex trigger entry: `C:\Users\A\.codex\skills\codex-desktop-clean-reinstall-skill-recovery`.
- 2026-07-01: `C:\Users\A\.codex\skills` canonical runtime skill root; `K:\AI` backup/reference root
  - Purpose: mark C drive as the active Codex skill runtime and K drive as backup, history, reports, workspaces, knowledge indexes, and restore/reference material.
  - Method: update active `codex-video-to-usable-skill-loop` rules, templates, SOPs, and reusable asset scanner to prefer `C:\Users\A\.codex\skills`; keep `K:\AI\skills` as backup/reference and `H:\AI` only as historical context.
  - Trigger phrases: `搜索知识库`, `调用知识库`, `入知识库`, `同步到技能库`, `更新触发词`, `复用成熟技能包`, `C盘技能包主用`, `K盘只是备份`, `H盘已经不存在`.
  - Knowledge note: `K:\AI\obsidian-vaults\AI-COMPANY-KNOWLEDGE-OS\01_META\K-drive-canonical-path-rule-20260630.md`.
  - Codex trigger entry: `C:\Users\A\.codex\skills\codex-video-to-usable-skill-loop`.

- 2026-07-01: `C:\Users\A\.codex\skills\computer-use-visual-recovery`
  - Purpose: restore and verify full visual Computer Use capability: screenshot observation, visible button/marker recognition, coordinate positioning, one-step human-like action, and post-action verification.
  - Method: `look -> locate -> confirm unique target -> one small action -> look again -> verify`; coordinates are temporary execution addresses derived from the current screenshot, not durable proof.
  - Trigger phrases: `computer use`, `Any App`, `截图`, `按钮`, `标识`, `坐标`, `点击位置`, `像人一样操作`, `视觉定位`, `screenshot-guided click`, `能力恢复`, `修复`.
  - Knowledge note: `K:\AI\obsidian-vaults\AI-COMPANY-KNOWLEDGE-OS\01_META\Computer-Use-Visual-Recovery-Skill-20260701.md`.
  - Validation: `quick_validate.py` PASS; `check-visual-recovery.ps1` returned `VISUAL_RECOVERY_CHECK: PASS`.
  - Codex trigger entry: `C:\Users\A\.codex\skills\computer-use-visual-recovery`.
