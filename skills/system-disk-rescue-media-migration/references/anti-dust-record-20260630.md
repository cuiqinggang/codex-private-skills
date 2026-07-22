# Anti-Dust Record 2026-06-30

## Material Value Judgment

High value. This workflow prevents destructive mistakes during system disk replacement and rescue USB reuse. It includes confirmed disk identities, read-only inspection, backup, hash verification, elevated BCD/WIM evidence, and a clear stop-before-format boundary.

## Trigger Keywords

- Macrium Reflect Rescue Media
- Veeam Recovery Media
- VEEAMRE
- Kingston DataTraveler
- rescue USB
- boot USB
- system disk replacement
- hard drive replacement
- Great Wall GT6 SSD
- ST4000NM0033
- back up U disk before formatting
- boot.wim / BCD / WinPE

## Preflight Action

Before similar work, run or mentally apply:

```powershell
${REDACTED_SECRET}
```

Then read:

${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}

## Failure Review Entry Point

If any future rescue media or disk migration step fails, append the failure mode to this file and update `SKILL.md` if a new guardrail or checklist item would prevent recurrence.

## Recent Use Log

- 2026-06-30: Created after successful read-only inspection and backup of `Disk 4 / Kingston DataTraveler 3.0 / D: / VEEAMRE`. Backup verified with 49/49 SHA256 matches. Elevated BCD/WIM export confirmed WinPE boot structure and Windows Recovery Environment boot.wim.
- 2026-07-01: Updated after completed Macrium Reflect system migration from `ST4000NM0033-9ZM170` to `Great Wall GT6 1TB`. Captured the full 839 clone workflow, Macrium Rescue Media pass evidence, boot-menu mistake (`BOOTMGR is missing` from bare SSD entry), correct UEFI boot entry (`Windows Boot Manager (P1: Great Wall GT6 1TB)`), final `C:` 931GB SSD boot success, and old 4TB disk retention rule.

## AGENTS.md Patch Draft

Add this to global or project AGENTS rules if needed:

```markdown
## Rescue Media + System Disk Migration Safety

${REDACTED_SECRET}

Require exact target disk identity. During inspection/backup stages, do not modify the USB or protected disks. Back up and hash-verify existing rescue media before reusing it. Stop after backup/report generation until the user explicitly authorizes the destructive next stage.

For Macrium system disk cloning, verify source and target by model + capacity + drive letter + partition structure. Use Windows Boot Manager entries for GPT/UEFI boot verification. Do not clean, delete, merge, or repartition the old system disk until the SSD has booted successfully multiple times and the user explicitly authorizes old-disk cleanup.
```

## Acceptance Evidence

Skill deployed at:

${REDACTED_SECRET}

Validation targets:

- `SKILL.md`
- `scripts\inspect-rescue-usb-readonly.ps1`
- `scripts\backup-rescue-usb-readonly.ps1`
- `references\2026-06-30-kingston-veeamre-case.md`
- `references\839-macrium-reflect-st4000-to-greatwall-gt6-case.md`
