# ROI Rules

Use these rules when deciding whether an old Hermes/OpenClaw/WSL skill deserves Windows Hermes migration.

## Value signals

High Windows value:

- Codex, Hermes, ChatGPT, GPT bridge, yesterday replay, model routing, or browser automation workflows.
- Cloud/GPU/model workflows that are still relevant and not already covered by active skills.
- A mature process that would take longer to recreate than to Windowsize.

High legacy value:

- OpenClaw migration or recovery procedures.
- Qwen/local model connector history.
- Old browser bridge or device automation patterns that explain previous successful paths.
- Baseline or backup evidence needed to reconstruct decisions.

Low daily value:

- WSL-only recovery commands.
- Old `.openclaw` workspace assumptions.
- `/mnt/...`, `/home/...`, `~/.openclaw`, old Chrome profile, or OpenWebUI paths with no current Windows equivalent.
- Repeated backup snapshots when one canonical preserved copy exists.

## Cost signals

Low rewrite cost:

- Pure `SKILL.md` text and prompt/process instructions.
- Commands that only need path and shell syntax updates.

Medium rewrite cost:

- Python or PowerShell helpers that need Windows path normalization.
- Browser or CLI workflows that need current tool verification.

High rewrite cost:

- `.sh` scripts, WSL process management, OpenClaw runtime commands, old Chrome profile assumptions, old local model endpoints, or deleted source paths.

## ROI classes

- `A_ALREADY_ACTIVE`: equivalent Windows Hermes skill exists; no migration.
- `B_ALREADY_ARCHIVED`: legacy equivalent exists under `.archive`; no daily migration.
- `C_REWRITE_SHORTLIST`: keep for future Windows rewrite after demand confirmation.
- `D_ARCHIVE_REFERENCE`: keep as reference only.
- `E_DELETE_CANDIDATE_*`: review-first deletion candidate; never delete automatically.

## Decision rule

Migrate only when Windows value is high enough and rewrite cost is lower than future rebuild cost. Otherwise, keep one canonical archive reference and mark duplicate preserved copies as review-first delete candidates.
