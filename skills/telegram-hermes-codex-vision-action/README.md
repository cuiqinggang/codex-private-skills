# Telegram Hermes Codex Vision Action

This package defines a safe Windows workflow for Telegram media tasks:

Telegram phone message -> Hermes Telegram polling bridge -> local attachment file -> Codex CLI -> result files -> Telegram reply.

It is intentionally file-first and CLI-first. It does not use Codex desktop UI automation, mouse/keyboard control, window focus, clipboard paste, or screenshot transfer.

## Files

- `SKILL.md`: agent-facing operating rules and G01-G10 gate protocol.
- `DAILY-RUN.md`: copy-paste daily gates.
- `RECOVERY.md`: narrow failure recovery by layer.
- `TEST-REPORT.md`: latest verification state for this package.
- `scripts\Invoke-CodexImageExec.ps1`: skill copy of the image wrapper.
- `scripts\Invoke-CodexVideoExec.ps1`: skill copy of the video wrapper.

Runtime copies are also installed at:

- `C:\Users\A\Hermes_Tools\Invoke-CodexImageExec.ps1`
- `C:\Users\A\Hermes_Tools\Invoke-CodexVideoExec.ps1`

## Fixed Directories

- Images: `C:\Users\A\Desktop\1\input\telegram-media\images\`
- Videos: `C:\Users\A\Desktop\1\input\telegram-media\videos\`
- Frames: `C:\Users\A\Desktop\1\input\telegram-media\frames\<taskId>\`
- Results: `C:\Users\A\Desktop\1\output\CODEX-TELEGRAM-VISION-<taskId>\`

## Wrapper Use

Image:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\A\Hermes_Tools\Invoke-CodexImageExec.ps1" -RepoPath "C:\Users\A\Desktop\1" -Task "Analyze the image. Do not edit files." -ImagePaths "C:\Users\A\Desktop\1\input\telegram-media\images\sample.jpg" -TaskId "TGIMG-001"
```

Video:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\A\Hermes_Tools\Invoke-CodexVideoExec.ps1" -RepoPath "C:\Users\A\Desktop\1" -Task "Analyze the key frames. Do not edit files." -VideoPath "C:\Users\A\Desktop\1\input\telegram-media\videos\sample.mp4" -TaskId "TGVID-001"
```

Dry run:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\A\Hermes_Tools\Invoke-CodexVideoExec.ps1" -RepoPath "C:\Users\A\Desktop\1" -Task "dry run" -VideoPath "<video path>" -TaskId "TGVID-DRYRUN" -DryRun
```

## Important Status Boundary

Saving this package does not by itself modify Hermes router code or Hermes model configuration. If Hermes does not already route `/codeximg` and `/codexvideo` to these wrappers with local attachment paths, the correct status is `STOP_ROUTER_NOT_INSTALLED`, not PASS.

## G01 Runtime Boundary

G01 is split into two checks:

- `G01A Runtime Base Readiness`: blocks image/video tests only when the live runtime is not ready. It requires Hermes gateway running, Telegram connected, healthy 8642/3000 endpoints, `C:\Users\A\AppData\Roaming\npm\codex.cmd --version`, `codex.cmd login status`, `codex.cmd exec` smoke, and `ffmpeg -version`.
- `G01B Startup Persistence Check`: records whether `Hermes_Gateway.cmd` exists in the Windows Startup folder.

Missing startup persistence is a WARN, not a STOP, for `/codeximg` and `/codexvideo` testing. Current runtime status after R3 is:

`G01_RUNTIME_BASE_READY_WITH_STARTUP_ENTRY_MISSING`

Do not create a startup entry, change Hermes startup mode, change Telegram config, or touch DeepSeek/New API/Open WebUI as part of this status correction.
