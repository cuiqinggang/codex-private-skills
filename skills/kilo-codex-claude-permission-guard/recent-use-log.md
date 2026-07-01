# Recent Use Log

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

