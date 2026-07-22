# Hotpath Diagnostic Report

## Status

`PASS | PARTIAL_PASS | BLOCKED`

## User Rule

Default active runtime, saves, output, cache, temp, logs, and scheduled jobs stay on `C:`.
Non-C drives are opt-in only.

## Disk Identity

- Disk:
- Model:
- Serial:
- Drive letter:
- Media type:
- Health:

## Root Cause

Describe what was actually waking or writing to the mechanical drive.

## Fixed

- 

## Residuals

- 

## Verification

- Process scan:
- Disk I/O sample:
- App launcher/config:
- Scheduled tasks:
- Pagefile/temp:
- Knowledge Brain health:

## Next-Run Rule

Before related work, run `scripts/diagnose-hotpath.ps1` and apply the C-drive hotpath default rule.

