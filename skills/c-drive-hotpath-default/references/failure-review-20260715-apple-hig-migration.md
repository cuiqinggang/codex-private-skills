# Failure Review: Apple HIG Cross-Drive Migration

## Trigger

Use this review for Windows/PowerShell tasks involving drive-root discovery, reparse points, `robocopy`, SHA256 migration verification, or optional Git/CodeGraph checks.

## Failure 1: false zero candidate count

- Symptom: `Get-ChildItem H:\ -Directory -Recurse` returned zero Apple HIG candidates even though the exact source existed.
- Cause: `H:\AI` is a top-level reparse point and the drive-root recursion did not descend into it.
- Rule: inspect top-level attributes and explicitly scan the authoritative data root. Record scan scope and do not claim full-drive uniqueness from a scoped scan.

## Failure 2: optional Git probe aborted closeout

- Symptom: all copies and hash checks succeeded, but `git -C <runtime> rev-parse --show-toplevel` stopped the script before the final JSON summary.
- Cause: Windows PowerShell surfaced native Git stderr as a terminating error while `$ErrorActionPreference = 'Stop'` was active.
- Rule: persist the final migration result before optional probes and handle expected nonzero Git exit codes in a non-fatal block.

## Acceptance

- Exact source is path-safe and preserved.
- C runtime and requested backup contain the same relative file set and SHA256 values.
- Historical report mentions are not confused with runtime dependencies.
- Optional capability detection cannot erase or prevent the core result.

## Evidence

`C:\AI\workspaces\OPEN-DESIGN-APPLE-HIG-MIGRATION`
