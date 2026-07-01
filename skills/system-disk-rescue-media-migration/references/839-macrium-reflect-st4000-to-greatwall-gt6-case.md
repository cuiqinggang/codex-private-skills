# 839 Macrium Reflect ST4000NM0033 To Great Wall GT6 Case

## Purpose

Record the completed end-to-end system disk migration from a 4TB mechanical Windows system disk to a 1TB Great Wall GT6 SATA SSD, including rescue media preparation, clone execution, boot-menu mistakes, successful SSD boot verification, and the old-disk retention rule.

## Final Status

Result: system disk migration succeeded.

- Macrium Reflect installed: complete.
- Macrium Rescue Media created: complete.
- Target SSD preparation: complete.
- Source system disk cloned to Great Wall GT6: complete.
- Clone result verified in Macrium: complete.
- SSD boot menu verification: complete.
- SSD Windows Boot Manager boot: success.
- Current system disk: Great Wall GT6 1TB SSD.
- Old ST4000NM0033 4TB mechanical system disk: retained as old `D:` disk.

## Hardware And Disk Roles

Source system disk:

- Model: `ST4000NM0033-9ZM170`
- Capacity shown in workflow: about 3.64TB usable
- Partition style: GPT
- Original Windows system volume: `C:`
- Medium: mechanical hard disk
- Role: source only; never select as target.

Target SSD:

- Model: `Great Wall GT6 1TB`
- Capacity: about 931GB usable
- Partition style: GPT
- Pre-clone temporary volume: `S:\ SSD_PREP`
- Medium: SATA SSD
- Role: allowed overwrite target during the clone stage only.

Protected disks:

- `WDC WD10EZEX`: data/knowledge disk with G/H/I/J/K; do not modify during migration.
- `SSK SSK`: external/data disk, K: when present; do not modify.
- `Kingston DataTraveler 3.0`: rescue USB, D: when present; do not use as clone target or format except during explicit rescue-media creation.

## Pre-Clone Readiness

Completed before cloning:

- C: cleanup and scan tasks 831-834.
- Clone preflight task 837.
- Used C: space about 193GB-195GB.
- Target SSD capacity about 931GB, sufficient.
- BitLocker: off.
- SFC: pass.
- DISM: pass.
- chkdsk C: pass.
- chkdsk S: pass.
- VSS: pass.
- Administrator context: OK.

Judgment: source system was clone-ready and the target SSD had enough space.

## Target SSD Preparation And OEM Backup

Before overwriting the Great Wall GT6 SSD, the old preinstalled Windows 10 environment was preserved:

- 835C: original SSD preinstalled Windows 10 file-copy baseline.
- 835D: future bootable recovery preparation package.

Known backup locations:

- `G:\GreatWall_GT6_SSD_OEM_Win10_File_Copy_Backup_835C\FUTURE_BOOTABLE_RECOVERY_PACKAGE_835D`
- `C:\Users\A\Desktop\835D.zip`

Activation caveat: preserved files, EFI, registry hives, and drivers do not guarantee future OEM activation.

## Macrium Installation

Software used:

- Macrium Reflect X Home v10.0.8843, 64-bit.
- Install path: `C:\Program Files\Macrium\Reflect\`.

Installed components:

- CBT: installed.
- Image Guardian: installed.
- viBoot: not installed.
- Desktop shortcut: installed.

Macrium recognized all disks before cloning.

## Rescue Media Preparation

Original USB:

- `Disk 4 / Kingston DataTraveler 3.0 / D: / VEEAMRE / FAT32`

Original VEEAMRE backup:

- `G:\USB_Backups\VEEAMRE_Kingston_838B\backup_20260630-194103`

Backup verification:

- Source files: 49.
- Backup files: 49.
- Hash comparisons: 49.
- Mismatches: 0.
- Result: `BACKUP_AND_HASH_VERIFY_OK`.

Macrium Rescue Media verification:

- Result: `MACRIUM_RESCUE_MEDIA_PASS`.
- Key markers:
  - `D:\EFI`
  - `D:\EFI\Boot\bootx64.efi`
  - `D:\EFI\Microsoft\Boot\BCD`
  - `D:\boot`
  - `D:\boot\BCD`
  - `D:\bootmgr`
  - `D:\bootmgr.efi`
  - `D:\sources\boot.wim`
  - `D:\Drivers\Macrium.oem`
  - `D:\RMBuilder.xml`
  - `RMBuilder="v10.0.8843"`

Note: after Macrium creation, File Explorer may show only about 31.9GB for the USB because Macrium created a FAT32/UEFI boot partition. Do not "fix" this capacity immediately and do not format the USB.

## Disk Number Rule

Macrium disk numbers and Windows Disk Management numbers may not perfectly match. Use model + capacity + drive letter + partition structure. Do not rely on a disk number alone.

Protected role map from this case:

- Source: `ST4000NM0033-9ZM170`, 3.64TB, old `C:`.
- Target: `Great Wall GT6 1TB`, 931.51GB, pre-clone `S:\ SSD_PREP`.
- Protected data: `WDC WD10EZEX`, G/H/I/J/K.
- Protected data USB: `SSK SSK`, K: when present.
- Protected rescue USB: `Kingston DataTraveler 3.0`, D: when present.

## Correct Macrium Clone Steps

1. In Macrium main UI, select the source disk:
   - `ST4000NM0033-9ZM170`
   - GPT
   - about 3.64TB
   - contains a 16MB reserved partition, a FAT32 about 99MB boot partition, and the Windows `C:` partition.

2. Click `Clone this disk...` on the source disk.

3. Do not use "Select a different source disk..." to choose the target. That changes the source, not the target.

4. In the clone wizard lower target area, select:
   - `Great Wall GT6 1TB`
   - GPT
   - about 931.51GB
   - `SSD_PREP (S:)`

5. On the schedule page, leave the schedule list empty and continue. This was a one-time clone.

6. On the summary page, confirm:
   - Source: `ST4000NM0033-9ZM170`, about 3.64TB.
   - Target: `Great Wall GT6 1TB`, about 931.51GB.
   - Smart sector copy enabled.
   - Verify enabled.
   - Delta and SSD trim-related options enabled as shown by Macrium.
   - Operation list copies 16MB reserved, FAT32 boot, and Windows NTFS partition.

7. When the overwrite warning appears for `S:\ SSD_PREP`, check the confirmation box and continue only if `S:` is the Great Wall target SSD. This is expected and necessary.

## Clone-Time Observations

Normal behavior:

- Current progress may move while total progress remains 0%.
- Transfer speed and remaining time may be blank during filesystem analysis.
- Macrium may show "checking file system" and loading NTFS `$MFT`.
- The old `S:\ SSD_PREP` drive letter may disappear during clone.

Do not intervene:

- Do not cancel.
- Do not pause.
- Do not open Disk Management to assign drive letters.
- Do not format or initialize anything.
- Do not run Codex, Kilo, Claude Code, PowerShell, partition tools, antivirus full scans, Windows Update, big downloads, big copies, or games during the clone.

Allowed light activity:

- Watch videos.
- Browse light pages.
- Avoid downloads and installs.

Heat observation:

- The mechanical source disk may become noticeably warm due to sustained reading.
- A small fan for airflow is appropriate.
- Do not move or shake the disk.
- Do not use wet towels or ice.

Escalate only if:

- Macrium reports an error.
- The disk makes abnormal clicking/scraping sounds.
- There is a burning smell.
- The computer freezes.
- Progress is completely stuck for a long time and the window is unresponsive.
- The disk is too hot to touch.

No such abnormal condition occurred in this case.

## Clone Completion

Macrium reported clone completion:

- Total progress: 100%.
- Current progress: 100%.
- Duration observed: 03:18:32.
- `UpdateGPTMountedDevices`: success.
- `UpdateGPTBCD`: success.
- VSS shutdown stage completed.
- Observed transfer speed around 130.4 Mb/s.
- Observed read around 191.8 Mb/s.
- Observed write around 2.0 Gb/s.

Judgment: Macrium clone task succeeded.

## Post-Clone Partition View

Old source disk in Macrium:

- `ST4000NM0033-9ZM170`
- GPT
- about 3.64TB
- 16MB reserved
- FAT32 about 99MB boot
- Windows `C:` NTFS about 3.64TB

Target SSD in Macrium while still booted from the old system:

- `Great Wall GT6 1TB`
- GPT
- about 931.51GB
- 16MB reserved
- FAT32 about 99MB boot
- cloned Windows NTFS partition, temporarily shown as `D:`

This is normal. While the old system is running, the old mechanical disk remains `C:` and the cloned SSD may be `D:`.

## Boot Verification

Motherboard:

- ASUS P8Z77-V PRO.

Keys:

- BIOS setup: `Delete`.
- Boot menu: `F8`.

First wrong selection:

- Selected bare `P2: Great Wall GT6 1TB`.
- Result: `BOOTMGR is missing`.

Explanation:

- Bare disk entries can trigger Legacy/CSM boot.
- GPT/UEFI Windows must boot through Windows Boot Manager.
- Do not select the bare Great Wall disk entry.

Correct selection:

- `Windows Boot Manager (P1: Great Wall GT6 1TB)`.

Wrong entries to avoid:

- `Windows Boot Manager (P2: ST4000NM0033-9ZM170)` old source disk.
- `P2: Great Wall GT6 1TB` bare SSD.
- `P3: ST4000NM0033-9ZM170` bare old mechanical disk.
- `P1: WDC WD10EZEX` data disk.
- `SSK` data/external disk.

## Successful SSD Boot Evidence

After booting from `Windows Boot Manager (P1: Great Wall GT6 1TB)`:

- `C:` showed about 931GB total.
- Old 4TB mechanical disk appeared as `D:` about 3.63TB.

Judgment:

- Current `C:` is the Great Wall GT6 1TB SSD.
- Old ST4000NM0033 became retained `D:`.
- SSD boot verification succeeded.

Success phrase:

```text
C: 931GB = SSD boot success
C: 3.63TB = still booting from old mechanical disk
```

## Default Boot Verification

To confirm future automatic SSD boot:

1. Reboot normally.
2. Do not press `F8`.
3. Do not manually choose a boot menu entry.
4. After Windows starts, check `This PC`.

If `C:` remains about 931GB, default boot is the SSD.

If `C:` returns to about 3.63TB, BIOS still defaults to the old mechanical disk. Enter BIOS and set:

```text
Boot > Boot Option Priorities > Boot Option #1
Windows Boot Manager (P1: Great Wall GT6 1TB)
```

Do not set Boot Option #1 to bare `P2: Great Wall GT6 1TB`.

Save with `F10`.

## Old Disk Retention

After SSD boot success, old ST4000NM0033 as `D:` must remain untouched for now.

Do not:

- Format old `D:`.
- Delete old Windows.
- Clean old system partitions.
- Merge old disk partitions.
- Unplug the old disk immediately.

Recommended observation:

- Use normally for 1-3 days if possible.
- Confirm startup, shutdown, restart, network, Codex, Kilo, browser, and common software all work.
- Confirm repeated reboots still boot from the SSD.

Only after that should a separate old-disk cleanup or merge plan begin.

## Fixed Mantras

Main process:

```text
Back up first.
Then preflight.
Then clone.
Then confirm partitions.
Then temporary boot test.
Then set default boot.
Only then consider the old disk.
```

UEFI boot:

```text
Choose Windows Boot Manager + SSD.
Do not choose the bare SSD.
```

Boot success:

```text
C: 931GB = SSD boot success.
C: 3.63TB = old mechanical disk still booting.
```

Old disk:

```text
If SSD is not proven stable, do not touch the old disk.
```
