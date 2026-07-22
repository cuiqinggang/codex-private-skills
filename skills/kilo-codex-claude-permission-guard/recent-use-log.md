# Recent Use Log

## 2026-07-07

- Status: BLACKLIST_MODE_DEPLOYED_AND_SKILL_UPDATED.
- Task: user requested one unified permission method for Codex, Kilo, and Hermes: only Windows system core operations and network/proxy-chain operations require approval; ordinary work should run without repeated prompts.
- Repair:
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
  - This skill package and `codex-permission-policy` were updated so future repairs reuse the same method.
- Safety:
  - No system proxy, browser proxy, DNS, hosts, firewall, route, Windows service, registry, scheduled task, Docker, WSL, Telegram, New API, Hermes Gateway, API key, or credential was intentionally changed.
  - Hermes was not switched to `approvals.mode: off` and no `--yolo` bypass was enabled.
- Next-run instruction:
  - For future permission-noise repairs, first classify whether the blocked action is in the two-item blacklist. If not, repair the relevant ordinary allow path; if yes or uncertain, ask the user in Chinese before executing.

## 2026-07-03

- Status: REDEPLOYED_AFTER_CONFIG_DRIFT.
- Task: user reported Kilo/Codex permission approval started appearing again and asked whether the mature permission guard skill was still deployed.
- Finding:
${REDACTED_SECRET}
  - Drift found: `[windows] sandbox` had changed to `unelevated`.
${REDACTED_SECRET}
  - Kilo route still showed `openrouter/deepseek/deepseek-v4-pro` and `snapshot=false`.
- Repair:
  - Backed up `config.toml` and `default.rules` with timestamp `20260703-212006`.
  - Restored only `[windows] sandbox = "elevated"`.
  - Updated this skill's knowledge deployment check from old K-drive-first paths to C-drive Knowledge Brain first; K remains backup/reference only.
- Safety:
  - No Windows registry, services, startup items, scheduled tasks, Docker, WSL, proxy, DNS, firewall, route, hosts, API keys, credentials, or Kilo provider settings were changed.
- Next-run instruction:
  - If permission prompts return after Codex Desktop repair/reinstall/restart, rerun this skill and check specifically for `[windows] sandbox` drift before touching any broader system setting.

## 2026-06-30

- Status: PASS_WITH_READ_ONLY_VALIDATION.
- Task: after reboot, verify whether Kilo/Codex/Claude/Hermes permission boundary survived and preserve it as a skill.
- Evidence:
  - Codex config contains `approval_policy = "on-request"`, `sandbox_mode = "danger-full-access"`, `approvals_reviewer = "auto_review"`, and `[windows] sandbox = "elevated"`.
  - Codex rules contain prompt gates for Windows/network/proxy-adjacent commands including `netsh`, `route`, `ipconfig`, `reg`, `sc`, `schtasks`, `docker`, `wsl`, `diskpart`, `format`, and `setx`.
  - Codex UI state targeted check found local mode set to `custom`.
  - Kilo config targeted check found `openrouter/deepseek/deepseek-v4-pro` and `snapshot=false`.
  - No protected Windows, proxy, DNS, firewall, route, service, registry, Docker, WSL, or scheduled-task mutation was executed.
- Caveat: visual menu screenshot was not taken in this run; file/state evidence is enough for config persistence, while UI proof remains optional.
