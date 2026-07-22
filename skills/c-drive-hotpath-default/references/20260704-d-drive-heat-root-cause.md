# 2026-07-04 D Drive Heat Root Cause

## Finding

The 3.64 TB mechanical disk is:

- Disk 2
- Model `ST4000NM0033-9ZM170`
- Serial `S1Z2Z2JS`
- Drive letter `D:`
- Label `系统`
- Size about 4 TB, visible in Windows as about 3.64 TB usable

The disk is healthy, but it contains old system-like contents:

- `Windows`
- `Program Files`
- `ProgramData`
- `Users`
- EFI/System partition
- old `pagefile.sys`, `hiberfil.sys`, and `swapfile.sys`

This makes Windows treat it as more than a plain empty data disk for mounting, metadata, recovery, and scanning behavior.

## Active Runtime Cause Found

ComfyUI was running from `C:\AI\ComfyUI_Aaki_v3`, but its launch arguments explicitly sent active runtime data to `D:`:

- `--output-directory D:\AI_ComfyUI_Outputs\ComfyUI_Aaki_v3\output`
- `--input-directory D:\AI_ComfyUI_Outputs\ComfyUI_Aaki_v3\input`
- `--temp-directory D:\AI_ComfyUI_Outputs\ComfyUI_Aaki_v3\temp`

Root cause: an earlier launcher was intentionally named/configured as `START_COMFYUI_C_DRIVE_OUTPUT_D`, meaning program on C drive but output/temp on D drive.

## Other Non-C Automation Found

Several scheduled tasks referenced old `H:` paths:

- `AI Knowledge Brain Light Sync`
- `AI Knowledge Brain Deep Sync`
- `CodeGraph Sync Important Repos`
- `CodeGraph Sync Important Repos Hourly`
- `Hermes_OpenWebUI_AutoStart`

One Knowledge Brain light sync process was running from `H:\AI\knowledge-brain`.
Hermes processes were also using `H:\Hermes_Windows_Native_014` in their command lines.

## Fixes Applied

- ComfyUI future input/output/temp path changed to `C:\AI\ComfyUI_Aaki_v3\data`.
- Current leaking D/H processes were stopped.
- `AI Knowledge Brain Deep Sync`, `AI Knowledge Brain Light Sync`, and `CodeGraph Sync Important Repos Hourly` were disabled where Windows permissions allowed.
- Disk idle timeout changed to 5 minutes on AC and DC power.
- Windows Search indexing query found no D/H indexed locations.
- Current pagefile usage was only on `C:\pagefile.sys`.
- User temp paths were already on `C:`.

## Residual Work

Two protected legacy tasks still need future elevated cleanup:

- `CodeGraph Sync Important Repos`
- `Hermes_OpenWebUI_AutoStart`

They were not running after the fix, but they remain enabled and point to old H paths.

