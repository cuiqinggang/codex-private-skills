---
name: powershell-reliability-guard
description: Write, review, repair, or run PowerShell commands and .ps1/.psm1/.psd1 files reliably for the user's Windows machine through a fail-closed unified execution gate and verified repair archive. Use whenever a task creates or changes PowerShell, diagnoses a PowerShell error, passes complex commands through Codex/Cursor/CMD, handles Windows PowerShell 5.1 versus pwsh 7 compatibility, or should prevent a recurring failure from being repeated.
---

# PowerShell Reliability Guard

用户固定要求：以后编写、审核 Windows 命令包或命令行脚本时，先参考本技能；不要仅在报错后才使用。先读 [2026-09-08 实测规则与证据](references/ps51-codex-acceptance-20260908.md)。这些规则降低已知错误风险，不保证所有脚本无错。

Treat every PowerShell artifact as a small tested program, not disposable command text. Use one fail-closed execution entry and archive verified repairs automatically.

## Required workflow

1. Read `references/machine-profile.md`. Never invent an unknown local fact.
   If facts are missing, run `scripts/Get-PowerShellMachineProfile.ps1` in the actual Windows session and update the profile only from that output.
2. For a reported failure, search `references/error-catalog.md` by symptom, error text, command, and environment before proposing a fix.
3. Freeze the target host: `powershell.exe` 5.1, `pwsh.exe` 7+, or both. For this user, prefer the verified PowerShell 7.6.5 workflow unless the task requests 5.1; for 5.1 deliver 5.1-compatible syntax. Verify current versions rather than pinning historical values blindly. A launcher version does not establish the actual execution shell.
4. Prefer a `.ps1` file plus named parameters over a long nested `-Command` string. Use splatting for many arguments. Avoid backtick line continuation.
5. Keep inspection, planning, mutation, and verification separate. Make destructive behavior opt-in and preserve exact targets.
6. Never execute a generated or modified target script directly. Route it through the unified entry:

```powershell
powershell.exe -NoProfile -File .\scripts\Invoke-GuardedPowerShell.ps1 `
  -Path .\target.ps1 -Target WindowsPowerShell51 -ScriptArguments @('-Mode', 'Audit')
```

Launch the entry with `pwsh.exe` for `-Target PowerShell7`. A host/target mismatch, parser error, compatibility error, required analyzer failure, or target non-zero exit code must produce `BLOCKED`, append an incident with evidence, and return exit code 1. The target must not start when preflight fails. Do not install modules silently.
7. Add focused Pester tests for non-trivial branching, path selection, state transitions, destructive actions, quoting, or external-process results. Mock mutations and prove the exact target. Pester absence is a reported limitation, never a reason to claim tests passed.
8. Execute the smallest non-destructive path first. Capture host version, exact command, exit code, stdout, stderr, and changed files. For native commands, judge success by `$LASTEXITCODE`; do not equate any stderr output with failure.
9. After fixing an incident, rerun the same target through the unified entry and supply the verified repair fields:

```powershell
powershell.exe -NoProfile -File .\scripts\Invoke-GuardedPowerShell.ps1 `
  -Path .\target.ps1 -Target WindowsPowerShell51 `
  -ResolveIncidentId '<incident-id>' -RootCause '<verified cause>' `
  -Fix '<verified correction>' -Prevention '<write-time or preflight rule>'
```

Archive only after preflight and execution both pass. The entry links failure and passing hashes, exit code, environment, and incident ID, then deduplicates the learned error. Do not add guesses. When the archive returns `PROMOTION_REQUIRED`, update the checker or this core workflow and rerun the self-test before reporting the repair complete.

## Write-time rules

- Save PowerShell 5.1 scripts containing non-ASCII characters as UTF-8 with BOM; inspect the actual EF BB BF prefix. Script decoding and data-file encoding are separate. Do not blindly add BOM to existing configuration or JSON files.
- Verify Chinese path names and file contents against an independent expected Unicode value (for example ASCII-only code-point fixtures), not just a round-trip of the same potentially misdecoded literal. Equal corrupted strings are not a passing test.
- For literal directory creation with brackets, use a verified literal-safe API such as .NET Directory.CreateDirectory; New-Item has no general LiteralPath replacement. Use LiteralPath on cmdlets that support it and inspect the actual created name. Do not infer all New-Item failures have one cause.
- Avoid passing PowerShell through Bash double-quoted command strings: $_ and other variables can expand before PowerShell sees them. Prefer a saved script plus argument array.
- Use a narrow project working directory for Codex tests. Keep launcher, default Codex shell, and explicitly invoked powershell.exe versions separate in evidence.
- Preserve approval boundaries and execution policy. Do not add Bypass, alter sandbox modes, or retry a rejected action through another host. The unified entry performs runtime validation, not a second command-package score.


- Use single quotes for literal strings and double quotes only when expansion is required. Use `${name}` beside punctuation and prefer format strings for complex interpolation.
- Use `-LiteralPath` for user-supplied or exact paths. Resolve and display exact mutation targets before changing them.
- Use `Join-Path`, explicit working directories, and named parameters. Do not depend on the caller's current directory or profile.
- Do not repurpose `$HOME`, `$PROFILE`, `$Error`, `$Args`, or common preference variables as ordinary variables.
- On Windows PowerShell 5.1, do not round-trip UTF-8-without-BOM configuration files through default `Get-Content`/`Set-Content`. Use explicit .NET UTF-8 encoding and a candidate-file/readback/atomic-replace flow.
- Do not use PowerShell 7-only syntax or parameters in a 5.1 target: `&&`, `||`, `??`, `?.`, ternary expressions, pipeline-chain operators, `ForEach-Object -Parallel`, or `$PSNativeCommandUseErrorActionPreference`.
- Do not build shell syntax by concatenating untrusted strings. Pass an argument array or use `ProcessStartInfo` when native quoting is fragile.
- Use `try/catch/finally` around operations that can fail, add `-ErrorAction Stop` only where terminating behavior is intended, and retain the original exception.
- Verify content encoding, parse success, analyzer result, optional tests, runtime exit code, and intended postcondition separately.

## Repair protocol

Reproduce the smallest failing case, classify it as parser/quoting/host-version/path/encoding/permission/module/native-process/state/idempotency, and change one cause at a time. Re-run the same failing input plus one nearby negative case. Report the root cause, exact fix, verification evidence, and whether a reusable prevention rule was added.

Use `references/error-catalog.md` for accumulated verified failures and `references/upstream-foundation.md` for the mature components this skill composes.

Run `scripts/Test-GuardedPowerShell.ps1` after changing the entry or checker. It must prove that invalid syntax is blocked before side effects, an incident is created, and a valid script executes successfully.
