# Future Codex Lite Power Upgrade Template

Use this as the starting point for a future task-specific output folder:

```powershell
$TaskId = "CODEX-DESKTOP-LITE-POWER-UPGRADE-YYYYMMDD"
${REDACTED_SECRET}
$Logs = Join-Path $Root "logs"
New-Item -ItemType Directory -Force -Path $Logs | Out-Null
```

## G01 Read-Only Diagnosis

Purpose: collect versions, config signals, skills/plugins, and core tools without printing secrets.

```powershell
codex --version
npm view @openai/codex version
npm view @openai/codex dist-tags --json
npm list -g @openai/codex --depth=0
node --version
npm --version
git --version
python --version
gh --version
winget --version
Get-AppxPackage -Name OpenAI.Codex | Select-Object Name,PackageFullName,Version
Select-String -LiteralPath "$env:USERPROFILE\.codex\config.toml" -Pattern '^model\s*=|^\[plugins\.".*"\]|enabled\s*='
Get-ChildItem -LiteralPath "$env:USERPROFILE\.codex\skills" -Directory | Select-Object Name
Get-ChildItem -LiteralPath "$env:USERPROFILE\.codex\plugins\cache" -Directory | Select-Object Name
```

Success: default model is still `gpt-5.5`; stable latest is identified; no secrets printed.

## G02 Backup

${REDACTED_SECRET}

```powershell
$Stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$Source = "$env:USERPROFILE\.codex"
$Dest = Join-Path $Root "backup.codex-$Stamp"
$Log = Join-Path $Logs "G02-robocopy-backup-$Stamp.log"
robocopy $Source $Dest /E /COPY:DAT /DCOPY:DAT /R:2 /W:2 /XJ /NFL /NDL /NP /TEE /LOG:$Log
if ($LASTEXITCODE -gt 7) { throw "Backup failed with robocopy exit code $LASTEXITCODE" }
```

Success: robocopy exit code is `0..7`; no old backup overwritten.

## G03 Stable Upgrade

Purpose: upgrade only from official stable sources.

```powershell
npm view @openai/codex dist-tags --json
npm install -g @openai/codex@latest --loglevel=warn
codex --version
npm list -g @openai/codex --depth=0
winget upgrade --name Codex --source msstore --disable-interactivity --accept-source-agreements
Get-AppxPackage -Name OpenAI.Codex | Select-Object Name,PackageFullName,Version
```

Success: npm `latest` is installed; alpha/beta/pre-release tags are not installed; Store source has no newer stable package or upgrades cleanly.

## G04-G06 Lite Policy And Curation

Purpose: keep the system useful without bulk installs.

Keep:

- GPT-5.5 default model
- Superpowers
- `yesterday-replay-controlled-coding`
- PowerShell, Git, Node/npm, Python
- browser/browser-use/Chrome, Playwright/screenshot
- GitHub CLI and GitHub skills
- DeepSeek fallback routes, not default

Do not install by default:

- alpha/beta/pre-release Codex
- unknown-source plugins
- bulk MCP/toolbox collections
- duplicate AI CLIs
- Figma/database/cloud MCPs unless the current project requires them

Success: curation report lists keep/optional/review-later and deletes nothing.

## G07 Real Smoke Test

Purpose: prove Codex can write files, run commands, and verify visible output.

Minimum marker:

```text
CODEX_LITE_POWER_UPGRADE_SMOKE_OK
```

If checking HTML, serve it by HTTP instead of `file:`:

```powershell
python -m http.server 0 --bind 127.0.0.1
```

Use Playwright CLI with `--filename` for screenshots.

Success:

- script exit code `0`
- marker appears in command output
- browser snapshot includes marker when browser capability is available

## G08 Final Report

Final report must include:

- old/new CLI and Desktop versions
- whether stable latest was installed or already current
- official source evidence
- enabled enhancements
- not-installed items and reasons
- keep/optional/review-later plugin/skill lists
- GPT-5.5, Superpowers, and DeepSeek fallback preservation
- AGENTS.md validation
- smoke output
- rollback paths
- skipped checks and residual risks
- one of the allowed final status codes
