# 2026-06-30 Kingston VEEAMRE Rescue USB Case

## Purpose

Record the exact rescue USB inspection and backup context used during the system/hard-drive replacement preparation flow.

## Disk Context

Observed disks during the safe read-only phase:

- Disk 0: `WDC WD10EZEX-08WN4A0`, SATA, MBR, about 1TB, partitions G/H/I/J. Knowledge/data disk. Do not delete files during rescue media work.
- Disk 1: `Great Wall GT6 1TB`, SATA, GPT, about 1TB, partition S `SSD_PREP`. Do not modify unless the user explicitly authorizes the Great Wall SSD stage.
- Disk 2: `ST4000NM0033-9ZM170`, SATA, GPT, about 4TB, system/boot disk, C:. Do not modify system partitions during rescue media work.
- Disk 3: `SSK SSK`, USB, GPT, about 750GB, K:. Large data USB disk. Not the target rescue media.
- Disk 4: `Kingston DataTraveler 3.0`, USB, MBR, about 124GB physical size, D:, label `VEEAMRE`, FAT32, Removable. Confirmed target rescue USB.

## Initial Classification

Disk 4 had the following boot files:

- `D:\EFI`
- `D:\boot`
- `D:\bootmgr`
- `D:\bootmgr.efi`
- `D:\sources`
- `D:\EFI\Boot\bootx64.efi`
- `D:\EFI\Microsoft\Boot\BCD`
- `D:\boot\BCD`
- `D:\sources\boot.wim`
- `D:\BMRAnswerFile.xml`

No obvious `D:\Macrium` or `Reflect` marker was found. The volume label `VEEAMRE` and `BMRAnswerFile.xml` make it likely Veeam Recovery Media rather than Macrium Reflect Rescue Media.

## Elevated Read-Only Boot Evidence

Administrator read-only export succeeded after UAC:

- `IsAdministrator=True`
- BCD EFI loader path: `\windows\system32\boot\winload.efi`
- BIOS/boot-folder loader path: `\windows\system32\boot\winload.exe`
- Both BCD stores point to `ramdisk=[boot]\sources\boot.wim`
- `winpe Yes`
- `ramdisksdipath \boot\boot.sdi`
- DISM image info:
  - Name: `Microsoft Windows Recovery Environment (x64)`
  - Description: `Microsoft Windows Recovery Environment (x64)`
  - Size: `3,177,556,800 bytes`

Conclusion: structurally valid WinPE-style rescue media, likely Veeam Recovery Media, not confirmed Macrium Reflect Rescue Media.

## Backup Evidence

Backup run:

- Backup root: `G:\USB_Backups\VEEAMRE_Kingston_838B\backup_20260630-194103`
- Files backup: `G:\USB_Backups\VEEAMRE_Kingston_838B\backup_20260630-194103\D_root_files`
- Reports: `G:\USB_Backups\VEEAMRE_Kingston_838B\backup_20260630-194103\reports`

Verification:

- Robocopy exit code: `1` (successful copy with files copied).
- Source files: `49`
- Backup files: `49`
- Hash compared: `49`
- Hash mismatches: `0`
- Final result: `BACKUP_AND_HASH_VERIFY_OK`

Key reports:

- `BACKUP_REPORT.txt`
- `ROBOCOPY_LOG.txt`
- `SOURCE_FILE_MANIFEST.csv`
- `BACKUP_FILE_MANIFEST.csv`
- `SOURCE_SHA256.csv`
- `BACKUP_SHA256.csv`
- `HASH_VERIFY.csv`
- `ELEVATED_BCD_WIM_EXPORT_20260630-194320.txt`

## Operational Lesson

Do not assume a file copy alone can restore every boot detail of a USB rescue drive. It captures accessible files and BCD/WIM evidence, but may not preserve raw MBR code, active flags, hidden sectors, or vendor-specific boot structures. Before reusing this Kingston USB for Macrium, prefer keeping this backup plus optionally creating a full physical disk image if the user wants maximum rollback confidence.

## Current State

Backup and verification are complete. The USB has not been formatted, erased, repartitioned, or written to by Codex. Any future Macrium Rescue Media creation requires explicit user authorization for the destructive/rewrite stage.
