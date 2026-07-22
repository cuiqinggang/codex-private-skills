# Recent Use

## 2026-07-04

Triggered by user report that the 3.64 TB mechanical `D:` drive was hot even though work should run on the C-drive SSD.

Result:

- Diagnosed Disk 2 `ST4000NM0033-9ZM170` as `D:`.
- Found ComfyUI output/input/temp were explicitly configured to `D:\AI_ComfyUI_Outputs`.
- Changed ComfyUI future runtime data to `C:\AI\ComfyUI_Aaki_v3\data`.
- Stopped current D/H leaking processes.
- Disabled several H-drive scheduled sync tasks where permissions allowed.
- Set disk idle timeout to 5 minutes.
- Preserved user rule: C drive is default hot path; D/H/K are opt-in only.

Follow-up update:

- Expanded the result into a reusable skill package with scripts, checklists, templates, root-cause reference, Obsidian/Knowledge Brain note, and acceptance evidence.
- Added `scripts/diagnose-hotpath.ps1` for future read-only diagnostics.
- Added AGENTS.md patch draft for future global-rule promotion.

## 2026-07-07

User clarified that the runtime disk should now be the C-drive system disk for future runs.

Result:

- Preserved the durable rule: active runtime, launchers, logs, caches, temp, outputs, and scheduled jobs default to `C:`.
${REDACTED_SECRET}
- Converted the old `H:\AI\scripts\codegraph-sync-important-repos.ps1` target into a compatibility shim only.
- Confirmed the old Hermes OpenWebUI H-drive task target is a compatibility shim to the C-drive launcher.
- Recorded that old protected scheduled tasks should be changed to direct C-drive actions when Windows permissions allow.

## 2026-07-10 — Knowledge/Obsidian/runtime C-drive convergence

- Canonical runtime: C-drive Knowledge Brain, Obsidian Vault, skills, CodeGraph launcher, Hermes launcher, and Feishu bridge workspace.
- K drive: one-way backup/additional skill storage only.
- H drive: historical reference only; no active Vault or scheduled-task runtime.
- Acceptance requires task-action scan, process scan, actual Obsidian open, and screenshot evidence.

## 2026-07-13 — K-drive heat and hot-path leak repair

Triggered by the user's report that K remained hot after active runtime was moved to C.

Result:

- Identified K as a USB-attached mechanical disk (`Performs Normal Seeks`, TRIM unsupported).
- Changed ordinary reuse preflight and reusable-asset scans to C-only defaults; K backup/history now requires explicit `--include-backups`.
- Moved learning-material intake and acceptance output defaults from K to C.
- Changed Matt adapter report generation so K backup verification is disabled unless `--backup-path` is explicitly supplied.
- Restarted Hermes through its C-drive launcher; the real 8642 listener and parent process now both run from C.
- Verified standard Hermes diagnostics PASS and a real authenticated local chat completion returned content.
- Verified default preflight caused zero K I/O samples; final K quiet test also returned zero nonzero samples.
- Residual: Windows denied updates to two protected tasks whose actions still name H. Their H targets were verified as compatibility shims that immediately forward to C.

## 2026-07-15 — Apple HIG reference migration

Triggered by a request to preserve `H:\AI\tools\open-design\skills\apple-hig` as history, create the active C-drive reference, and then create a K-drive backup.

Result:

- Found that the supplied `Get-ChildItem H:\ -Recurse` scan returned zero because `H:\AI` is a reparse-point root.
- Re-ran candidate discovery from the authoritative `H:\AI\tools` root and found exactly one candidate.
- Copied one `SKILL.md` to C and then K; all three SHA256 values matched: `7353DB31E05F6BFD78549F0A512339AC063B77ACF8894303FDF834932F547D73`.
- Found seven RC4.2 H-path mentions, all in historical `APPLE_REFERENCE_SOURCE.md` evidence/report copies; no runtime dependency was found and no bulk replacement was performed.
- Recorded a second failure mode: with `$ErrorActionPreference = 'Stop'`, a non-repository `git rev-parse` probe aborted final summary generation. Future probes are explicitly non-fatal and summaries are persisted first.
- Evidence: `C:\AI\workspaces\OPEN-DESIGN-APPLE-HIG-MIGRATION`.

## 2026-07-16 — C→H cancellation and C→K approval gate

User established a stricter durable disk rule after a read-only path audit.

Result:

- Removed the automatic C-to-H copy from the daily System Evolution runner.
- Converted legacy H sync/install scripts into fail-closed entrypoints returning `C_TO_H_FORBIDDEN`.
- Changed Codex reinstall preservation targets from H to K and added mandatory `-CValidated` plus `-UserApprovedBackup` gates.
- Disabled K sources for Knowledge Brain health/light/deep sync policy.
- Removed C-missing fallback permission from global and reusable-material preflight rules.
- Updated active C-drive skill instructions that previously mirrored results to H.
- No H/K content was read, changed, or backed up during deployment.
