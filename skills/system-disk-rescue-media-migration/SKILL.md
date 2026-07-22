---
name: system-disk-rescue-media-migration
description: Use when preparing, auditing, backing up, changing, cloning, boot-verifying, or cleaning up rescue USB media and Windows system disks during hard drive or SSD replacement work, especially Macrium Reflect Rescue Media, Veeam Recovery Media, WinPE boot USBs, Kingston DataTraveler/VEEAMRE disks, ST4000NM0033-to-Great-Wall-GT6 cloning, ASUS P8Z77-V PRO boot menu/BIOS selection, old system disk retention, or any workflow where Codex must avoid formatting, partition changes, accidental writes, or wrong target-disk selection until the user explicitly authorizes the exact stage.
---

# System Disk Rescue Media Migration

## Core Safety Rule

Treat rescue USB changes and system disk replacement as staged operations. Never combine these stages unless the user explicitly authorizes the next stage in the same message:

1. Identify disks and rescue media.
2. Read-only inspect bootability and product identity.
3. Back up and hash-verify the existing rescue USB.
4. Capture BCD, boot.wim, disk, partition, volume, and file tree evidence.
5. Stop and report.
6. Only after explicit authorization, format or recreate rescue media.
7. Only after explicit authorization, proceed with disk clone, restore, boot repair, or hardware replacement.
8. After clone completion, verify boot from the target SSD before changing default boot order.
9. Retain the old system disk until multiple successful boots and normal work are confirmed.
10. Only after a later explicit cleanup authorization, plan old-disk deletion, merging, repartitioning, or reuse.

If there is any uncertainty about the target disk, stop before reading deeper and report the ambiguity.

## Non-Negotiable Guards

- Do not format, clean, initialize, shrink, extend, repartition, delete, or overwrite any disk unless the user explicitly authorizes that exact stage.
- Do not write to the rescue USB during inspection or backup stages.
- Do not modify known protected disks unless the current stage explicitly requires it and the user authorizes it:
  - Great Wall GT6 SSD.
  - ST4000NM0033 system disk.
  - WDC WD10EZEX knowledge/data partitions such as G/H/I/J/K.
- During clone execution, allow overwrite only of the exact intended target disk/volume that the user confirmed. In the 839 case this was `Great Wall GT6 1TB` / `SSD_PREP (S:)`, not the source disk, not the rescue USB, and not the data disks.
- Do not manually change C/D drive letters after cloning. Booting from the target SSD makes its Windows partition become `C:` automatically.
- Do not treat "Macrium clone completed" as sufficient. Confirm target-SSD boot and C: capacity after boot.
- During backup stages, only create a new backup/report directory on a non-USB destination with enough free space.
- Prefer `G:\USB_Backups\...` for rescue USB backups when it has enough free space.
- If multiple USB disks are present, require a user-confirmed target or an exact target tuple.

## Required Target Tuple

Before touching a rescue USB workflow, establish and log:

- DiskNumber.
- Model/FriendlyName.
- SerialNumber when available.
- Capacity.
- BusType.
- PartitionStyle.
- DriveLetter.
- Volume label.
- FileSystem.
- DriveType / Removable status.
- IsBoot and IsSystem.
- Partition table and partition-to-drive-letter mapping.

For the 2026-06-30 case, the confirmed target was:

- `Disk 4`
- `Kingston DataTraveler 3.0`
- serial `4E0985D154C9`
- USB, MBR, about 124GB physical size
- `D:`
- label `VEEAMRE`
- FAT32, Removable
- one accessible FAT32 partition about 32GB

The separate large USB data disk was:

- `Disk 3`
- `SSK SSK`
- USB, GPT, about 750GB
- `K:`
- data disk; do not file-check or modify it when the target is the small Kingston rescue USB.

## Rescue Media Judgment

Use file and boot evidence to classify the USB:

- `Macrium confirmed`: Macrium/Reflect markers plus WinPE boot structure.
- `Veeam likely`: label `VEEAMRE`, `BMRAnswerFile.xml`, WinPE boot structure, and no Macrium marker.
- `Windows/WinPE generic`: `EFI`, `boot`, `bootmgr`, `bootmgr.efi`, `BCD`, `sources\boot.wim`, but no vendor marker.
- `Not confirmed bootable`: missing common boot markers or inaccessible evidence.

For the 2026-06-30 Kingston case:

- It was structurally bootable WinPE media.
- BCD pointed to `\sources\boot.wim`.
- `winpe Yes` was present.
- DISM identified `boot.wim` as `Microsoft Windows Recovery Environment (x64)`.
- Label `VEEAMRE` and `BMRAnswerFile.xml` indicated likely Veeam Recovery Media.
- It was not confirmed as Macrium Reflect Rescue Media.

After Macrium Rescue Media creation, the same Kingston USB passed when it contained:

- `D:\Drivers\Macrium.oem`
- `D:\RMBuilder.xml`
- `RMBuilder="v10.0.8843"`
- complete `EFI`, `boot`, `bootmgr`, `bootmgr.efi`, and `sources\boot.wim` structure

Pass phrase: `MACRIUM_RESCUE_MEDIA_PASS`.

## Backup Requirement Before Reusing a Rescue USB

Before allowing a Veeam or unknown rescue USB to be reused for Macrium:

1. Confirm the exact target tuple.
2. Copy all accessible files, including hidden and system files.
3. Preserve root listing and full tree.
4. Export disk, partition, volume reports.
5. Export BCD stores when possible:
   - `D:\EFI\Microsoft\Boot\BCD`
   - `D:\boot\BCD`
6. Export `boot.wim` info with DISM when elevated.
7. Generate source file manifest, backup file manifest, source SHA256, backup SHA256, and hash comparison.
8. Report `BACKUP_AND_HASH_VERIFY_OK` only when counts and hashes match.
9. Stop without formatting or making Macrium.

File-copy backup may not preserve raw MBR boot code or hidden sectors. Say this clearly. If the user needs the strongest rollback path, recommend an additional full-disk image with a trusted imaging tool before formatting.

## Macrium System Disk Clone Flow

Use this flow for ST4000NM0033-to-Great-Wall-GT6 style Windows migration:

1. Preflight the source system:
   - Confirm used space fits the target SSD.
   - Confirm BitLocker is off.
   - Confirm SFC, DISM, chkdsk, VSS, and administrator status where applicable.
   - Confirm rescue media exists and is verified.
   - Confirm old OEM/preinstalled system evidence is backed up if the target SSD previously contained a valuable installation.

2. Identify roles by model, capacity, partition structure, and drive letter:
   - Source: `ST4000NM0033-9ZM170`, GPT, old Windows `C:`, about 3.64TB usable.
   - Target: `Great Wall GT6 1TB`, GPT, about 931GB, pre-clone temporary `S:\ SSD_PREP`.
   - Protected data disk: `WDC WD10EZEX`, G/H/I/J/K.
   - Protected data USB: `SSK SSK`, K: when present.
   - Protected rescue USB: `Kingston DataTraveler 3.0`, D: when present.

3. In Macrium, choose the source disk's "Clone this disk" action. Do not use "Select a different source disk" as a target selector.

4. Select the Great Wall GT6 SSD as the target. If Macrium warns that `S:\ SSD_PREP` will be overwritten, that is expected only when it is on the Great Wall target SSD.

5. Do not create a schedule for a one-time migration clone. Continue through the summary page after confirming source and target.

6. During clone execution:
   - Do not run Codex, Kilo, PowerShell, partition tools, antivirus full scans, system updates, big downloads, or big file copies.
   - Keep the mechanical source disk ventilated.
   - Do not move, shake, power off, restart, or cancel unless Macrium reports a hard error or the machine is unsafe.
   - Current progress may move while overall progress remains 0% during NTFS `$MFT` and filesystem analysis. Treat this as normal if the UI remains responsive.
   - The target SSD drive letter may disappear during overwrite. Do not open Disk Management to assign letters or format anything.

7. After Macrium reports clone completion:
   - Confirm the target SSD now has EFI/MSR/Windows structure in Macrium.
   - While booted from the old source, the cloned SSD Windows partition may appear as `D:`. This is normal.
   - Do not manually change cloned SSD `D:` to `C:`.

8. Boot verification:
   - On ASUS P8Z77-V PRO, use `Delete` for BIOS and `F8` for boot menu.
   - Select `Windows Boot Manager (P1: Great Wall GT6 1TB)`.
   - Do not select the bare `P2: Great Wall GT6 1TB` or similar non-Windows-Boot-Manager entry; it can produce `BOOTMGR is missing`.
   - GPT/UEFI Windows must boot via Windows Boot Manager, not the bare disk entry.

9. Post-boot success check:
   - `C:` about 931GB means the Great Wall SSD boot succeeded.
   - Old ST4000NM0033 becoming `D:` about 3.63TB means the old mechanical system disk is now retained as a fallback/data candidate.
   - `C:` about 3.63TB means the machine still booted from the old mechanical disk.

10. Default boot check:
   - Reboot once without pressing `F8`.
   - If `C:` remains about 931GB, default boot is already the SSD.
   - If not, set BIOS Boot Option #1 to `Windows Boot Manager (P1: Great Wall GT6 1TB)`, then save with `F10`.

## Old Disk Cleanup Gate

After successful SSD boot, do not immediately format, delete, merge, or repartition the old ST4000NM0033 disk.

Wait for an explicit old-disk cleanup task after:

- At least one normal reboot without using the boot menu.
- 1-3 days of normal work if possible.
- Confirmation that Codex, Kilo, browser, network, shutdown, restart, and common directories work normally.
- Confirmation that the old disk still contains no unpreserved data needed by the user.

For later old-disk merge/cleanup, start with read-only inventory and a separate plan. Treat old `D:` Windows deletion and partition merging as a new destructive stage.

## Reusable Scripts

- `scripts/inspect-rescue-usb-readonly.ps1`
  - Use for read-only identification and boot marker inspection.
  - Writes only to a new report directory.

- `scripts/backup-rescue-usb-readonly.ps1`
  - Use for file-copy backup plus manifests and SHA256 verification.
  - Defaults to exact Kingston/VEEAMRE guards but accepts parameters.
  - Writes only to a backup/report directory, never to the USB.

When a script requires elevated BCD or DISM output, request administrator execution and keep it read-only.

## Evidence From 2026-06-30

Read `references/2026-06-30-kingston-veeamre-case.md` when continuing this exact system/hard-drive replacement flow.
Read `references/839-macrium-reflect-st4000-to-greatwall-gt6-case.md` for the completed clone-and-boot verification record.

Important generated evidence from that run:

- Backup root: `G:\USB_Backups\VEEAMRE_Kingston_838B\backup_20260630-194103`
- Backup report: `G:\USB_Backups\VEEAMRE_Kingston_838B\backup_20260630-194103\reports\BACKUP_REPORT.txt`
- Elevated BCD/WIM report: `G:\USB_Backups\VEEAMRE_Kingston_838B\backup_20260630-194103\reports\ELEVATED_BCD_WIM_EXPORT_20260630-194320.txt`
- Hash verification table: `G:\USB_Backups\VEEAMRE_Kingston_838B\backup_20260630-194103\reports\HASH_VERIFY.csv`
- Result: 49 source files, 49 backup files, 49 hash comparisons, 0 mismatches.

Important 839 result:

- Macrium Reflect X Home v10.0.8843 installed at `C:\Program Files\Macrium\Reflect\`.
- Kingston rescue media verified with `MACRIUM_RESCUE_MEDIA_PASS`.
- Source `ST4000NM0033-9ZM170` cloned to `Great Wall GT6 1TB`.
- First bare SSD boot produced `BOOTMGR is missing`; correct boot entry was `Windows Boot Manager (P1: Great Wall GT6 1TB)`.
- Final state: `C:` about 931GB on Great Wall GT6 SSD, old 4TB ST4000NM0033 retained as `D:` about 3.63TB.
- Old 4TB disk must not be cleaned or merged until a later explicit cleanup task.

## Final Report Requirements

For every related task, report:

- Target disk identity and why it was accepted.
- What was read.
- What was written and where.
- What was not modified.
- Rescue media classification.
- Backup verification status.
- Whether the next destructive stage is still waiting for explicit user authorization.

If the task is also about preserving or replacing the Great Wall SSD, use this skill together with `greatwall-ssd-win10-recovery-backup`.
