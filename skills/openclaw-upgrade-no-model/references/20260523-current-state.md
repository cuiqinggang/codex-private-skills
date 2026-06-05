# current-state.md

TASK_ID: OPENCLAW-UPGRADE-REPLAY-AUTOLOGIN-SKILL-UPDATE-20260523
Generated: 2026-05-23

## Windows OpenClaw

- Node: v24.14.0.
- npm: 11.9.0.
- openclaw command: C:\Users\A\AppData\Roaming\npm\openclaw.cmd.
- Current OpenClaw version: 2026.3.13 (61d171a).
- npm global package: openclaw@2026.3.13 under C:\Users\A\AppData\Roaming\npm\node_modules\openclaw.
- Current package engines.node: >=22.16.0.
- Official npm latest observed: openclaw@2026.5.20, engines.node >=22.19.0.
- 18789 listener at G02: none.
- Expected desktop script: C:\Users\A\Desktop\OpenClaw-Edge-Token-Start.ps1 is missing.
- Current OpenClaw config file C:\Users\A\.openclaw\openclaw.json is missing.
- models status default model: anthropic/claude-opus-4-6.
- providers in agent models file: local ollama models only; no active OpenRouter auth profile detected by models status.
- openclaw update status registry fetch inside OpenClaw failed, but npm registry queries from npm worked.

## WSL

- Actual distro list includes Ubuntu-24.04, docker-desktop, and Ubuntu-24.04-Restore.
- Ubuntu-24.04 became Running during probes.
- root /bin/echo in Ubuntu-24.04 timed out after 30s.
- id u123456 via root timed out after 30s.
- u123456 /bin/echo returned Wsl/Service/E_UNEXPECTED.
- Conclusion: WSL execution layer is currently unhealthy; do not use WSL paths as current execution facts until repaired.

## Official/Package Route Evidence

- npm registry metadata says latest is 2026.5.20 and Node requirement is >=22.19.0.
- npm README excerpt recommends Node 24 or Node 22.19+, npm install -g openclaw@latest, openclaw onboard --install-daemon, and update guide/openclaw doctor.
- openclaw update --dry-run --tag latest --no-restart --json succeeded and selected npm package update from 2026.3.13 to 2026.5.20.
