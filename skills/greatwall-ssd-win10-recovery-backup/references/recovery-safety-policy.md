# Recovery Safety Policy

## Never Do Without Explicit Final Confirmation

- Format D/E/F.
- Delete old SSD partitions.
- Merge old SSD partitions.
- Change partition sizes.
- Clean a disk.
- Remove the only remaining copy of the old Windows 10 files.

## Before Format Or Merge

Confirm all are true:

- 835C-style file backup exists on G:.
- 835D-style future bootable recovery package exists.
- EFI backup exists.
- Disk/partition layout files exist.
- `SYSTEM` and `SOFTWARE` registry hives were copied or the missing status is reported.
- Drivers were exported or the failure is reported.
- Activation evidence was captured or the activation uncertainty is reported.
- User explicitly says to proceed with formatting/merging after seeing the report.

## Acceptable Cleanup

It is acceptable to delete failed intermediate artifacts such as:

- incomplete WIM files from abandoned DISM attempts,
- small DISM test WIMs,
- scratch folders inside the failed WIM attempt directory.

Do not delete the 835C/835D backup package or reports unless the user explicitly asks.

## Report Language

Use direct status wording:

- `READY_WITH_MANUAL_RESTORE_STEPS`: future recovery package is usable as a source, but restoration remains manual.
- `PARTIAL`: do not format old partitions yet.
- `NOT_A_BOOTABLE_CLONE`: ordinary file copy cannot boot by itself.

Always tell the user whether C was touched and whether D/E/F were formatted, deleted, merged, or resized.
