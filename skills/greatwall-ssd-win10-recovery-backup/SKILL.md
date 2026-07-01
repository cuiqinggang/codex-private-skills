---
name: greatwall-ssd-win10-recovery-backup
description: Use when preserving, auditing, or preparing an old Great Wall GT6 SSD preinstalled Windows 10 environment before formatting, merging, deleting, or repurposing D/E/F partitions; includes simple file-copy backup, future bootable recovery package creation, EFI/registry/driver/OEM activation evidence capture, and format-readiness judgment.
---

# Great Wall SSD Win10 Recovery Backup

## Core Rule

Treat format/merge/delete of the old SSD partitions as irreversible. Do not format D/E/F until the user explicitly confirms after seeing the final backup readiness report.

This skill is for preserving an old Great Wall GT6 SSD Windows 10 installation as a future recovery source. It does not promise a one-click clone. It creates a practical file-based recovery package that a future agent or technician can use to rebuild a bootable Windows 10 installation when needed.

## Decision Flow

1. Identify the source disk and partitions.
   - Confirm the Great Wall GT6 SSD disk number.
   - Record System/EFI, MSR, Windows, software, and document partitions.
   - Confirm which partition contains `Windows\System32`.

2. Make a simple file-copy baseline.
   - Copy D/E/F into a dedicated G: backup folder.
   - Exclude only pagefile, hiberfil, swapfile, recycle bin, System Volume Information, and common temp/cache folders.
   - Do not use WIM, DISM capture, compression, or deep verification unless the user explicitly asks.

3. Upgrade the baseline into a future bootable recovery package.
   - Save the EFI System Partition.
   - Save disk and partition layout.
   - Save Windows registry hives from `Windows\System32\config`.
   - Export drivers from the offline Windows partition.
   - Preserve OEM activation/license evidence and SPP/ClipSVC/AppRepository files where available.
   - Write restore scripts and a plain-language README.

4. Judge readiness.
   - `READY_WITH_MANUAL_RESTORE_STEPS` means the package is suitable as a future recovery source, not that it is already bootable.
   - `PARTIAL` means do not format/merge/delete old partitions until the missing items are understood.

5. Only after explicit user confirmation, proceed with formatting or merging old D/E/F.

## Reusable Scripts

- `scripts/simple-ssd-file-copy-backup.ps1`
  - Creates the 835C-style D/E/F file-copy baseline on G:.
  - Does not use WIM, DISM, compression, delete, format, or partition changes.

- `scripts/make-future-bootable-recovery-package.ps1`
  - Creates the 835D-style future recovery package inside the 835C backup root.
  - Requires administrator rights because it temporarily assigns a letter to the EFI partition and reads protected registry/license locations.
  - Does not format, merge, delete, shrink, or resize partitions.

Read `references/recovery-safety-policy.md` before running any format/merge step.

## Activation Judgment

Do not tell the user that Windows activation is guaranteed unless there is direct evidence.

Windows 10 OEM activation often depends on firmware MSDM/OA3 key or a Microsoft digital license tied to the same hardware. Files alone are not enough to guarantee activation. Preserve:

- masked OA3xOriginalProductKey evidence if present,
- current Windows licensing channel evidence,
- `Windows\System32\spp`,
- `ProgramData\Microsoft\Windows\ClipSVC`,
- `ProgramData\Microsoft\Windows\AppRepository`,
- offline drivers and EFI.

If firmware OEM key is not found or the active channel is `VOLUME_KMSCLIENT`, report that activation is uncertain. On the same hardware, reactivation may still happen through Microsoft digital license; on different hardware, do not rely on it.

## Restore Reality

For future restoration, expect manual steps:

1. Prepare a GPT target disk.
2. Create a FAT32 EFI partition, about 300MB.
3. Create a Windows NTFS partition.
4. Copy `D_system_original` to the Windows partition.
5. Run `bcdboot <WindowsPath> /s <EfiDrive> /f UEFI`.
6. Use Windows Recovery / Startup Repair if the first boot fails.

This package is a preserved recovery source, not a bootable disk image.
