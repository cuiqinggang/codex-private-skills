---
name: windows-c-drive-final-cleanup-834
description: Use when performing final Windows C drive slimming before system-disk cloning, especially tasks like 834, C盘克隆前综合瘦身, Docker volume cleanup, hibernation cleanup, ComfyUI installer cleanup, cache cleanup, and preserving Codex, skills, proxy, Open WebUI, ComfyUI models/workflows, and user project outputs.
---

# Windows C Drive Final Cleanup 834

## Core Rule

This skill is for final cleanup before cloning Windows C drive. It may delete only explicitly disposable material. Protect working environments first.

Use `scripts/834_c_drive_final_cleanup.ps1` as the deterministic runner when the user explicitly requests 834-style cleanup.

## Safe Actions

- Delete explicit ComfyUI installer archives such as `ComfyUI-aki-v*.7z`.
- Clear cache directory contents, not parent profile directories.
- Clear recycle bin.
- Delete explicitly named installers such as Feishu installer when requested.
- Run Docker stopped-container, unused-image, build-cache, unused-network cleanup.
- Run Docker `volume prune` only when the user explicitly allows unused volume cleanup and Open WebUI active mounts have been recorded.
- Attempt `powercfg /h off`; never manually delete `hiberfil.sys`.

## Protected Items

Never delete automatically:

- `C:\Windows`, `C:\Program Files`, `C:\Program Files (x86)`, `C:\ProgramData`.
- `pagefile.sys`, `swapfile.sys`.
${REDACTED_SECRET}
- Proxy-related paths or installers such as FlClash/Clash.
- Browser profile roots such as Google or Edge user data; only cache subfolders may be cleaned.
- ComfyUI models, controlnet, custom_nodes, workflows, input, output.
- Desktop `4` AI model files.
- Open WebUI active volume.
- User images, videos, project outputs, and history projects unless separately confirmed.

## Required Evidence

Each run must save:

- before and after C drive state
- deleted installer/archive list
- hibernation log
- Docker before/after logs
- Open WebUI inspect/mount report
- cache cleanup log
- protected item check
- next manual confirmation list
- final report
- desktop zip package

## Proven 2026-06-29 Result

Task 834 released about 14.022 GB:

- C used: 205.155 GB -> 191.133 GB.
- C free: 3520.754 GB -> 3534.776 GB.
- Deleted explicit ComfyUI old archives: about 12.366 GB.
- Cleaned caches: about 2.581 GB.
- Docker volume prune reclaimed 0B; Open WebUI stayed healthy.
- Desktop `4`, ComfyUI models/workflows, Codex, skills, and FlClash were preserved.

## Knowledge Follow-up

After a run, update only the C-drive Knowledge Brain and C-drive skill indexes. Never copy, mirror, sync, or update H. A C-to-K backup is a separate operation permitted only after the C result validates and the user explicitly approves that exact backup.
