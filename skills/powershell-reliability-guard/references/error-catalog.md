# Verified PowerShell error catalog

Search this file before writing or repairing PowerShell. Add only reproduced or evidence-backed cases.

## PS-001 — UTF-8 configuration corruption on Windows PowerShell 5.1

- Symptom: previously valid non-ASCII configuration becomes mojibake or a parser reports a missing closing quote after a text edit.
- Environment: Windows PowerShell 5.1; UTF-8 file without BOM; default `Get-Content` plus `Set-Content` round trip.
- Root cause: the source can be decoded with the active ANSI code page and then rewritten with different bytes.
- Verified fix: restore the byte-for-byte backup; decode with strict UTF-8; write a separate candidate with explicit UTF-8; read it back and validate; atomically replace the live file.
- Prevention: never use default PowerShell 5.1 text encoding for important UTF-8 configuration files.

## PS-002 — Native stderr misclassified as command failure

- Symptom: a native tool emits a warning on stderr, PowerShell/Codex treats it as a terminating failure, but the native process actually succeeded.
- Environment: native executable launched from Windows PowerShell.
- Root cause: stderr presence was used as the success criterion instead of the native exit code and postcondition.
- Verified fix: capture stdout and stderr separately, read `$LASTEXITCODE` immediately, and verify the expected result.
- Prevention: never infer native failure from stderr alone.

## PS-003 — PowerShell 7 syntax sent to Windows PowerShell 5.1

- Symptom: parser errors around `&&`, `||`, `??`, `?.`, ternary syntax, or `ForEach-Object -Parallel`.
- Environment: `powershell.exe` 5.1.
- Root cause: the generating agent did not freeze the target host before writing code.
- Fix: rewrite with 5.1-compatible control flow or explicitly run a verified `pwsh.exe` 7+ host.
- Prevention: declare the host and run `Test-PowerShellArtifact.ps1` with the matching `-Target`.

## PS-004 — Long nested command loses quoting or variable boundaries

- Symptom: paths split at spaces, `$variables` expand in the wrong shell, quotes disappear, or a command works interactively but fails through CMD/Codex/task scheduler.
- Environment: one shell passes a long `-Command` string to another.
- Root cause: multiple parsers reinterpret quoting and escaping.
- Fix: write a `.ps1` file, pass named parameters, and use splatting/argument arrays.
- Prevention: do not use a long inline command when a script file is possible.

## PS-005 — Relative path resolves against the wrong directory

- Symptom: file/module not found or an output is created in an unexpected location.
- Environment: Codex, Cursor, task scheduler, elevated process, or another launcher changes the current directory.
- Root cause: script relies on the caller's location.
- Fix: anchor script resources to `$PSScriptRoot`; resolve user targets explicitly.
- Prevention: set the working directory explicitly and display resolved paths before mutation.

## Promotion rule

When one error class occurs twice after this catalog exists, add a deterministic check or template rule. Keep case IDs stable; merge duplicates instead of creating near-identical entries.

## Incident lifecycle

- `FAILURE_OPENED`: written automatically by `Invoke-GuardedPowerShell.ps1` for host mismatch, preflight failure, checker failure, or non-zero target exit.
- `FAILURE_VERIFIED_RESOLVED`: written only after the corrected target passes and the agent supplies a verified root cause, fix, and prevention rule.
- The verified repair is simultaneously added to `learned-errors.jsonl`, deduplicated by symptom, cause, and prevention.
- A second occurrence appends `REPEATED_OCCURRENCE` and returns `PROMOTION_REQUIRED`; completion is blocked until the prevention becomes an executable check or core rule and the guard self-test passes.
- Never promote an open incident directly into learned knowledge.
