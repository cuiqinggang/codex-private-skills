---
name: windows-github-cli-auth-repair
description: Use when GitHub CLI is unavailable on Windows, gh is not recognized, gh auth login succeeds in the browser but gh auth status is still logged out, or Codex cannot use GitHub integration because PATH, installer, proxy, or credential setup is broken.
---

# Windows GitHub CLI Auth Repair

## Overview

This skill repairs the common Windows state where Git works locally but GitHub CLI is unavailable or not authenticated. It is based on a verified Windows recovery path:

- `git` was installed and usable.
- `gh` was missing from PATH.
- `winget install GitHub.cli` found the official package but MSI installation hung.
- A portable GitHub CLI release zip installed successfully under the user profile.
- Browser device activation succeeded once but token exchange failed because terminal traffic did not use the browser proxy.
- Re-running `gh auth login` with `HTTP_PROXY` and `HTTPS_PROXY` set to `127.0.0.1:7890` completed authentication.

Never ask the user to share GitHub passwords or tokens. Use GitHub's browser device flow or a user-provided token only when the user explicitly chooses that route.

## When To Use

Use this skill when any of these are true:

- Codex UI says `GitHub CLI unavailable` or `GitHub CLI 不可用`.
- PowerShell shows `gh : The term 'gh' is not recognized`.
- `gh auth status` says `You are not logged into any GitHub hosts`.
- GitHub device activation page says success, but `gh auth status` remains logged out.
- Browser can open GitHub, but `gh auth login` fails with `oauth/access_token`, `wsarecv`, timeout, proxy, or connection errors.
- `winget install --id GitHub.cli` hangs or leaves `winget.exe` / `msiexec.exe` running.

Do not use this skill for creating repositories, pushing code, or fixing GitHub Actions after CLI authentication already works.

## Workflow

### 1. Diagnose before fixing

Run:

```powershell
Get-Command gh -All -ErrorAction SilentlyContinue
gh --version
git --version
winget --version
gh auth status
git remote -v
```

Interpretation:

- `git` works but `gh` is missing: install GitHub CLI.
- `gh` exists but auth status is logged out: run browser auth.
- `git remote -v` is empty: the local repo has no GitHub source yet; this is separate from GitHub CLI availability.

### 2. Try official WinGet install first

Run:

```powershell
winget install --id GitHub.cli -e --source winget --accept-package-agreements --accept-source-agreements --disable-interactivity
```

Then verify:

```powershell
gh --version
```

If WinGet hangs, inspect:

```powershell
Get-CimInstance Win32_Process |
  Where-Object { $_.Name -in @('winget.exe','msiexec.exe') } |
  Select-Object Name,ProcessId,CommandLine |
  Format-List
```

If the hanging command line is clearly for GitHub CLI, stop only those stuck installer processes and switch to the portable path.

### 3. Portable user-scope install fallback

Use `scripts/install-gh-cli-user-scope.ps1` or run the same logic manually:

- Download the official `gh_<version>_windows_amd64.zip` release from GitHub.
- Extract it under `%LOCALAPPDATA%\Programs\GitHub CLI\<version>`.
- Add the `bin` folder to the user PATH.
- Add the `bin` folder to the current process PATH before verifying.

Expected verification:

```powershell
gh version 2.92.0
```

Exact version may differ in future runs.

### 4. Browser auth

Start browser device auth:

```powershell
gh auth login --hostname github.com --git-protocol https --web --clipboard
```

The command prints and copies a one-time code and opens:

```text
https://github.com/login/device
```

The user must complete the GitHub browser authorization. Do not use or request the user's password.

### 5. If browser says success but gh stays logged out

Check the login log or terminal output for errors like:

```text
failed to authenticate via web browser: Post "https://github.com/login/oauth/access_token": ... wsarecv ...
```

Then compare browser proxy and terminal proxy:

```powershell
netsh winhttp show proxy
Get-ChildItem Env:HTTP_PROXY,Env:HTTPS_PROXY,Env:ALL_PROXY,Env:http_proxy,Env:https_proxy,Env:all_proxy -ErrorAction SilentlyContinue
Get-ItemProperty -Path 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Internet Settings' |
  Select-Object ProxyEnable,ProxyServer,AutoConfigURL |
  Format-List
```

If browser proxy is enabled, but terminal proxy env vars are empty, rerun auth with the same proxy:

```powershell
$env:HTTP_PROXY = 'http://127.0.0.1:7890'
$env:HTTPS_PROXY = 'http://127.0.0.1:7890'
gh auth login --hostname github.com --git-protocol https --web --clipboard
```

Use the actual browser proxy value found on the machine.

### 6. Final verification

Run:

```powershell
gh auth status
gh auth setup-git
gh repo list <github-username> --limit 5
```

Success looks like:

```text
Logged in to github.com account <username> (keyring)
Git operations protocol: https
Token scopes: 'gist', 'read:org', 'repo'
```

The token must be masked in all notes and reports.

## Safety Rules

- Do not ask the user to send passwords, recovery codes, personal access tokens, or one-time device codes unless they are actively completing the GitHub device flow themselves.
- If a password was pasted into chat, do not reuse it. Tell the user to rotate it.
- Do not store tokens in skill files, logs, screenshots, or summaries.
- Stop only installer processes whose command line clearly belongs to GitHub CLI.
- Do not delete unrelated files or alter unrelated PATH entries.

## References

- `references/install-auth-postmortem.md`: detailed real-world troubleshooting path and failure evidence.
- `references/commands.md`: copy-paste PowerShell command gates.
- `scripts/install-gh-cli-user-scope.ps1`: portable install fallback.
- `scripts/verify-gh-cli.ps1`: verification and auth-status check.
