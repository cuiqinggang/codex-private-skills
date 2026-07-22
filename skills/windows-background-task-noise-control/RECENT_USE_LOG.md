# Recent Use Log

## 2026-07-07

- Task: Quiet repeated blue/black console windows.
- Reused: `windows-background-task-noise-control` and Knowledge Brain first routing.
- Finding: Hermes gateway was running as a long-lived
  `cmd.exe -> python.exe -> conhost.exe` chain.
- Fix: Converted the Hermes gateway hidden launcher to `pythonw.exe` plus
  `run-hermes-gateway-hidden.py`, preserving stdout/stderr logs.
- Fallback: Task Scheduler edits were access denied, so target launchers were
  quieted instead.
- Verification: Hermes 8642 health/models PASS; no Hermes `cmd.exe` or
  `conhost.exe` remained; Knowledge Brain health PASS.

