# v4.5.5 Virtual -> Real Handoff

This handoff is part of VIRTUAL completion. It preserves Codex as the REAL executor.

## Whole-loop principle

```text
GPT -> Codex -> deterministic tools -> local evidence -> Codex result -> GPT final judgment
```

PowerShell is an internal deterministic tool. It does not replace Codex in the default closed loop.

## Frozen real artifact

- repository: cuiqinggang/codex-private-skills
- branch: codex/first-principles-physical-limit-convergence-v4.5.5
- frozen commit: ba4b82004102fa8e833f45b3f88404b10a576a3e
- frozen path: docs/first-principles/20260923-v4.5.5/REAL-ENTRY-FROZEN.ps1
- git blob sha: 901b8ee53237f11e5a8d9f643d0341cea4f88cf4
- no Temp/AppData script write
- Codex streams the frozen script directly from git object to PowerShell

## Timing relay

The outer PowerShell wrapper surrounds the entire `codex exec` process:

```text
CODEX_HANDOFF_START_TIMESTAMP
CODEX_PROCESS_ACTIVE_MS
CODEX_PROCESS_END_TIMESTAMP
```

The wrapper also records the Windows time source using `w32tm /query /source`.

## Frozen Codex contract

1. Do not read Skill files; this contract is self-contained.
2. Check whether frozen commit exists locally.
3. If missing, fetch only branch codex/first-principles-physical-limit-convergence-v4.5.5; retry once only for transport failure; never change proxy/system settings.
4. Confirm the frozen commit exists.
5. Do not write the frozen script to Temp/AppData or another staging path.
6. Stream the exact frozen git object directly into PowerShell 7:
   `git show <commit>:<path> | pwsh -NoProfile -Command -`
7. Return the reality output verbatim. Do not redesign, repair, or alter the frozen artifact.
8. On functional failure, stop and return the minimum Reality Delta to GPT.
