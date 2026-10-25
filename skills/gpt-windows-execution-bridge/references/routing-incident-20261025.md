# Windows execution bridge routing incident — 2026-10-25

Task: Docker / Hermes startup recovery  
Applicable contract: Windows Execution Bridge A → B → C  
Skill revision after repair: V12.0.2

## Incident

The user explicitly invoked Windows Execution Bridge V12.0.1 and expected the default A channel. The assistant initially called GPT-Windows-MCP-Bridge (B) for Windows diagnostics without first reading the local execution-bridge skill, without probing A, and without evidence that A had failed.

After the user corrected the route, Remote Desktop Commander (A) was discovered and used. A successfully inspected the Docker engine, startup scripts, Windows skills, WSL state, logs, and containers; it performed the controlled recovery and verified the services.

## Root cause

This was not an A-channel outage, and the user did not need to repeat the rule. The assistant skipped the mandatory skill preflight before its first Windows tool call. Tool discoverability and convenience incorrectly influenced the first choice.

The existing V12 rule already specified A as default, but the pre-call gate needed to be more explicit and easier to validate. The route script is a caller-supplied decision gate; it cannot physically intercept native tool calls from a GPT page that has not loaded the skill.

## Corrective action

- Upgraded the local skill entry to V12.0.2.
- Added an explicit mandatory pre-call gate: read this skill before any Windows-local tool call; dynamically discover A; run a no-side-effect probe; remain on A after PASS.
- B is permitted only after A's initial probe fails, the online device is rediscovered, one retry also fails, and the execution state is reconciled.
- C is permitted only after equivalent verified B failure.
- Added a deterministic static validation of the pre-call gate to verify_v12.py.
- Kept B and C available as backups. No proxy, FlClash, credentials, tunnel, system networking, or route mapping was changed.

## Evidence and boundaries

- Remote Desktop Commander A was online for DESKTOP-4A1EGTM and its diagnostic and recovery operations succeeded.
- Docker Engine recovered to 29.3.1; Open WebUI 3000, n8n 5678, Tymeslot 4352 and Windows-native Hermes 8642/health returned HTTP 200.
- The Docker startup script passed the PowerShell Reliability Guard and a healthy rerun did not restart or duplicate the backend.
- The modified route skill and validation script still require a live A→B failure-fallback test before claiming end-to-end enforcement.
- The new skill improves the pre-call rule but cannot guarantee every unrelated, already-running GPT page will load it automatically.
