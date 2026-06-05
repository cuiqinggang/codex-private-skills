# PowerShell Command Gates

These gates are copy-paste friendly for Windows PowerShell. Run from any normal user shell unless a specific working directory matters.

## G01 - Diagnose Current State

Purpose: identify whether the failure is missing `gh`, auth, Git remote, or network.

```powershell
$ErrorActionPreference='Continue'
Write-Host 'gh command lookup'
Get-Command gh -All -ErrorAction SilentlyContinue | Format-List Source,Version,CommandType
Write-Host 'gh version'
gh --version 2>&1
Write-Host 'git version'
git --version 2>&1
Write-Host 'winget version'
winget --version 2>&1
Write-Host 'gh auth status'
gh auth status 2>&1
Write-Host 'git remotes'
git remote -v 2>&1
```

Success criteria: output distinguishes the failing layer.

Failure recovery:

- Missing `gh`: run G02.
- `gh` installed but logged out: run G05.
- Empty remotes: configure repo source separately.

## G02 - Official WinGet Install

Purpose: install GitHub CLI from the official WinGet package.

```powershell
winget install --id GitHub.cli -e --source winget --accept-package-agreements --accept-source-agreements --disable-interactivity
```

Success criteria:

```powershell
gh --version
```

prints a GitHub CLI version.

Failure criteria: command hangs for several minutes, permission prompt never resolves, or `gh` remains unavailable.

Failure recovery: run G03 and then G04.

## G03 - Inspect Hung Installer

Purpose: confirm whether WinGet/MSI is stuck on GitHub CLI.

```powershell
Get-CimInstance Win32_Process |
  Where-Object { $_.Name -in @('winget.exe','msiexec.exe') } |
  Select-Object Name,ProcessId,CommandLine |
  Format-List
```

Only stop processes whose command line clearly contains `GitHub.cli` or `gh_...windows_amd64.msi`:

```powershell
Get-CimInstance Win32_Process |
  Where-Object {
    ($_.Name -eq 'winget.exe' -and $_.CommandLine -like '*GitHub.cli*') -or
    ($_.Name -eq 'msiexec.exe' -and $_.CommandLine -like '*gh_*windows_amd64.msi*')
  } |
  ForEach-Object { Stop-Process -Id $_.ProcessId -Force }
```

Success criteria: GitHub CLI installer processes are gone.

Failure recovery: do not kill unrelated `msiexec.exe`; wait or ask the user if an installer UI is visible.

## G04 - Portable User-Scope Install

Purpose: install `gh.exe` without relying on MSI.

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
.\scripts\install-gh-cli-user-scope.ps1 -Version '2.92.0'
```

If running outside this skill folder, use the full script path.

Success criteria:

```powershell
gh --version
```

prints a GitHub CLI version.

Failure recovery: check whether GitHub release download is blocked; try the proxy used by the browser.

## G05 - Browser Login

Purpose: authenticate GitHub CLI through GitHub's official device flow.

```powershell
gh auth login --hostname github.com --git-protocol https --web --clipboard
```

Success criteria:

```powershell
gh auth status
```

shows a logged-in GitHub account.

Failure recovery: if the browser page says success but `gh auth status` is logged out, run G06.

## G06 - Proxy-Aware Browser Login

Purpose: fix the case where browser GitHub access works but `gh` token exchange fails.

Find browser proxy:

```powershell
Get-ItemProperty -Path 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Internet Settings' |
  Select-Object ProxyEnable,ProxyServer,AutoConfigURL |
  Format-List
```

Then rerun auth with that proxy value:

```powershell
$proxy = 'http://127.0.0.1:7890'
$env:HTTP_PROXY = $proxy
$env:HTTPS_PROXY = $proxy
gh auth login --hostname github.com --git-protocol https --web --clipboard
```

Success criteria:

```powershell
gh auth status
```

shows `Logged in to github.com account <username> (keyring)`.

## G07 - Final Integration Verification

Purpose: prove GitHub CLI and Git integration work.

```powershell
gh auth status
gh auth setup-git
gh repo list <github-username> --limit 5
```

Success criteria: auth status is logged in, setup-git returns exit 0, and repo list returns repositories.

Failure recovery:

- If API calls time out, repeat with `HTTP_PROXY` and `HTTPS_PROXY`.
- If repo list is empty but auth works, verify the username or account permissions.
- If Codex UI still says CLI unavailable, restart Codex so it reloads PATH.
