# GitHub CLI Windows Install/Auth Postmortem

This reference captures the real troubleshooting path that led from `GitHub CLI 不可用` to a working `gh` login. It is intentionally detailed so a future agent can recognize the same failure pattern.

## Starting State

The user saw a Codex side panel with:

- Git section present.
- Current branch: `master`.
- `GitHub CLI 不可用`.
- `来源：暂无来源`.

Initial checks showed:

```powershell
Get-Command gh -All -ErrorAction SilentlyContinue
gh --version
git --version
winget --version
```

Evidence:

```text
gh : The term 'gh' is not recognized as the name of a cmdlet...
git version 2.53.0.windows.1
winget v1.28.240
```

Root cause at this layer: Git was installed, but GitHub CLI was not available in PATH.

Separate finding:

```powershell
git remote -v
```

returned no remotes. This explained `来源：暂无来源`, but it was separate from `GitHub CLI 不可用`.

## Official Package Discovery Worked

The official GitHub CLI package was available through WinGet:

```powershell
winget show --id GitHub.cli -e --source winget --disable-interactivity
```

Evidence:

```text
已找到 GitHub CLI [GitHub.cli]
版本: 2.92.0
安装程序类型: wix
安装程序 URL: https://github.com/cli/cli/releases/download/v2.92.0/gh_2.92.0_windows_amd64.msi
```

So the problem was not package discovery.

## WinGet Install Hung

The first install attempt was:

```powershell
winget install --id GitHub.cli -e --source winget --accept-package-agreements --accept-source-agreements
```

It timed out after five minutes. A second attempt with `--disable-interactivity` timed out after ten minutes:

```powershell
winget install --id GitHub.cli -e --source winget --accept-package-agreements --accept-source-agreements --disable-interactivity
```

Process inspection showed stuck installer processes:

```powershell
Get-CimInstance Win32_Process |
  Where-Object { $_.Name -in @('winget.exe','msiexec.exe') } |
  Select-Object Name,ProcessId,CommandLine |
  Format-List
```

Evidence:

```text
winget.exe install --id GitHub.cli ...
msiexec.exe /i "...WinGet\GitHub.cli.2.92.0\gh_2.92.0_windows_amd64.msi" /passive /norestart /log ...
```

The MSI log file existed but had almost no content:

```text
Length: 2
```

Conclusion: WinGet had downloaded and launched the official MSI, but the Windows Installer path stalled before useful logging.

## Recovery Path: Portable User-Scope Install

The stuck GitHub CLI install processes were stopped only after confirming their command lines belonged to `GitHub.cli`.

Then the official release zip was downloaded and extracted manually:

```powershell
$version = '2.92.0'
$base = Join-Path $env:LOCALAPPDATA 'Programs\GitHub CLI'
$versionDir = Join-Path $base $version
$zip = Join-Path $env:TEMP "gh_$version`_windows_amd64.zip"
$url = "https://github.com/cli/cli/releases/download/v$version/gh_$version`_windows_amd64.zip"
New-Item -ItemType Directory -Force -Path $versionDir | Out-Null
Invoke-WebRequest -Uri $url -OutFile $zip
Expand-Archive -LiteralPath $zip -DestinationPath $versionDir -Force
```

Result:

```text
C:\Users\A\AppData\Local\Programs\GitHub CLI\2.92.0\bin\gh.exe
```

The `bin` folder was added to the user PATH and current process PATH:

```powershell
$ghBin = 'C:\Users\A\AppData\Local\Programs\GitHub CLI\2.92.0\bin'
$currentUserPath = [Environment]::GetEnvironmentVariable('Path', 'User')
$parts = @()
if ($currentUserPath) { $parts = $currentUserPath -split ';' | Where-Object { $_ } }
if ($parts -notcontains $ghBin) {
    $newUserPath = (($parts + $ghBin) -join ';')
    [Environment]::SetEnvironmentVariable('Path', $newUserPath, 'User')
}
if (($env:Path -split ';') -notcontains $ghBin) { $env:Path = $env:Path + ';' + $ghBin }
gh --version
```

Success evidence:

```text
gh version 2.92.0 (2026-04-28)
```

## Auth Attempt 1: Browser Success, Local Token Exchange Failed

Command:

```powershell
gh auth login --hostname github.com --git-protocol https --web --clipboard
```

The GitHub browser page displayed:

```text
Congratulations, you're all set!
Your device is now connected.
```

But local verification still failed:

```powershell
gh auth status
```

Evidence:

```text
You are not logged into any GitHub hosts. To log in, run: gh auth login
```

The `gh auth login` stderr log explained the real failure:

```text
failed to authenticate via web browser: Post "https://github.com/login/oauth/access_token": read tcp ... wsarecv: A connection attempt failed because the connected party did not properly respond...
```

Conclusion: GitHub's browser device page succeeded, but local `gh` could not exchange the device grant for a token.

## Proxy Difference Was the Breakpoint

Network checks timed out or were unreliable. Proxy inspection showed:

```powershell
netsh winhttp show proxy
```

Evidence:

```text
Direct access (no proxy server).
```

Environment proxy variables were empty:

```powershell
Get-ChildItem Env:HTTP_PROXY,Env:HTTPS_PROXY,Env:ALL_PROXY,Env:http_proxy,Env:https_proxy,Env:all_proxy -ErrorAction SilentlyContinue
```

But the Windows browser proxy was enabled:

```powershell
Get-ItemProperty -Path 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Internet Settings' |
  Select-Object ProxyEnable,ProxyServer,AutoConfigURL |
  Format-List
```

Evidence:

```text
ProxyEnable : 1
ProxyServer : 127.0.0.1:7890
```

Direct/proxy `curl` checks showed GitHub could be reached when the correct path was available:

```powershell
curl.exe -I --proxy http://127.0.0.1:7890 https://github.com --connect-timeout 20
curl.exe -I https://github.com --connect-timeout 20
```

## Auth Attempt 2: Force gh Through Browser Proxy

The next auth flow set terminal proxy variables before starting `gh auth login`:

```powershell
$env:HTTP_PROXY = 'http://127.0.0.1:7890'
$env:HTTPS_PROXY = 'http://127.0.0.1:7890'
gh auth login --hostname github.com --git-protocol https --web --clipboard
```

After completing the GitHub device page again, the log showed:

```text
Authentication complete.
Configured git protocol
Logged in as <username>
```

Final verification:

```powershell
gh auth status
```

Success evidence:

```text
Logged in to github.com account <username> (keyring)
Active account: true
Git operations protocol: https
Token: gho_************************************
Token scopes: 'gist', 'read:org', 'repo'
```

Git integration and API access were verified:

```powershell
gh auth setup-git
gh repo list <username> --limit 5
```

The repo list returned successfully.

## Lessons

1. `GitHub CLI 不可用` in Codex is usually a local `gh` availability/auth issue, not proof that the GitHub account is wrong.
2. `来源：暂无来源` means the local Git repo has no remote. It is separate from GitHub CLI installation.
3. Browser device activation success is not enough; always run `gh auth status`.
4. On Windows, browser proxy and terminal proxy can differ. If OAuth token exchange fails after browser success, inspect `HKCU:\Software\Microsoft\Windows\CurrentVersion\Internet Settings`.
5. When WinGet MSI install hangs, a user-scope portable release zip can be a clean fallback.
6. Sensitive fields must be scrubbed: passwords, tokens, one-time codes, and personal access tokens do not belong in reusable skill packages.
