# C Drive Hotpath Preflight Checklist

Use before launching, installing, or configuring a local app, AI tool, model workflow, Codex workflow, Knowledge Brain job, CodeGraph job, or scheduled task.

## Required Checks

- Confirm default runtime root is on `C:`.
- Confirm output/input/temp/cache/log paths are on `C:`.
- Confirm virtual environments and package caches are on `C:` unless explicitly requested otherwise.
- Confirm scheduled tasks do not point to `D:`, `H:`, or `K:` unless the user asked.
- Confirm old backup/reference paths are not silently reused as active paths.
- Reject every C-to-H write, mirror, sync, update, or backup.
- If C input is missing, stop with `BLOCKED_C_SOURCE_MISSING`; never fall back to H/K.
- Before any C-to-K backup, record C-source validation evidence and the user's explicit approval for this exact backup action; otherwise stop with `BACKUP_NOT_AUTHORIZED`.
- Before a cross-drive migration, inspect whether the drive's intended data root is a reparse point; do not treat a drive-root recursive scan returning zero as sufficient proof.
- Record the authoritative candidate-scan root and whether the result is scoped or truly full-drive.
- Verify `source -> C runtime -> requested backup` with relative-path SHA256 maps, stopping before the next copy layer on mismatch.
- Separate historical/evidence-only non-C references from executable/configuration/runtime references before replacing any paths.
- Make Git/CodeGraph capability probes non-fatal, and persist the migration summary before optional probes.

## Pass Criteria

`PASS` only when no active hot path uses a non-C drive, no C-to-H write path exists, and every C-to-K backup is protected by C validation plus explicit per-operation approval.
