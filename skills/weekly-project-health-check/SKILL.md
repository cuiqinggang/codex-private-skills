---
name: weekly-project-health-check
description: Inspect and repair recurring workspace health checks for mixed local projects, especially Codex workspaces with standalone scripts, generated output, embedded subprojects, local Git ignore policy, optional Poetry/pip-audit checks, OpenAI reachability probes, and secret-like files that must not be read or committed.
---

# Weekly Project Health Check

## Workflow

1. Load the active `AGENTS.md` chain and `yesterday-replay-controlled-coding` first when the workspace requires it.
2. Read automation memory if an automation ID is present.
3. Identify project shape before running checks:
   - root manifests: `package.json`, `pyproject.toml`, `requirements*.txt`, `pytest.ini`, `tsconfig.json`, `go.mod`, `Cargo.toml`
   - embedded projects under `src/`, `apps/`, `packages/`, or tool-specific folders
   - local scripts and generated folders such as `output/`, `build/`, `runs/`
4. Prefer the narrowest existing checks. Do not run generators, deployers, or model/download commands unless the user asked for repair.
5. Treat secret-like files as inventory only. Report path, ignore status, and risk; do not print contents.
6. When repair is allowed, make small changes with backups and rerun the failing check.

## Reusable Script

Run the bundled script for a safe baseline:

```powershell
${REDACTED_SECRET}
```

The script reports:

- Git status, tracked file count, and local ignore source for blanket ignores.
- Root and embedded project manifests.
- Python AST parse for root/scripts `.py` files.
- PowerShell parser status for root/scripts `.ps1` files.
- Existing `health-check-20s.ps1` result when present.
- Tool availability for Python, PowerShell, Node, CMake, Poetry, and pip-audit.
- Secret-like filenames without reading secret contents.

## Check Selection

- Run `python -m pip check` when Python is available.
- Run `poetry check --directory <project>` only when a `pyproject.toml`/`poetry.lock` project exists and Poetry is installed.
- Run `pip-audit` when installed; install it only when the user asks to fix or deepen security checks.
- Run CMake configure/build only when writes are allowed and the target subproject is clearly selected.
- Run npm/yarn/pnpm checks only when the relevant package manifest exists.

## Reporting

Always report:

- project type
- files changed
- commands/checks run
- PASS/FAIL evidence
- skipped checks with reasons
- residual risks
- rollback path for any repair
