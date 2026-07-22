# 2026-06-08 Hermes 0.16.0 Upgrade And HERMES_HOME Repair

## Scope

This note records the accepted repair path for upgrading the Windows native
Hermes stack from `hermes-agent` 0.15.2 to 0.16.0 while preserving:

- Hermes gateway: `http://127.0.0.1:8642`
- Open WebUI: `http://127.0.0.1:3000`
- Direct chain: Open WebUI 3000 -> Hermes 8642 -> DeepSeek `deepseek-v4-pro`
- Telegram polling bridge through the Windows native Hermes gateway
- User's existing logged-in Google Chrome profile

Do not route this flow through old New API `3001`.

## Backups Used

Before upgrading or editing launchers, create a backup directory like:

```text
${REDACTED_SECRET}
```

Back up at least:

```text
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
H:\Hermes_Windows_Native_014\launcher\auto-start-hermes-openwebui.ps1
H:\Hermes_Windows_Native_014\launcher\start-hermes-openwebui.ps1
H:\Hermes_Windows_Native_014\launcher\hermes-014-runtime.ps1
H:\Hermes_Windows_Native_014\AUTO-START-HERMES-OPENWEBUI.cmd
${REDACTED_SECRET}
pip freeze output
pip show hermes-agent output
```

## Upgrade Command

Use the Hermes venv Python:

```powershell
H:\Hermes_Windows_Native_014\venv\Scripts\python.exe -m pip install --upgrade hermes-agent==0.16.0
H:\Hermes_Windows_Native_014\venv\Scripts\python.exe -m pip show hermes-agent
H:\Hermes_Windows_Native_014\venv\Scripts\hermes.exe --version
```

Accepted version evidence:

```text
hermes-agent 0.16.0
Hermes Agent v0.16.0 (2026.6.5)
```

## Invalid Distribution Cleanup

If pip prints warnings like:

```text
WARNING: Ignoring invalid distribution ~ermes-agent
```

list only the venv `site-packages` entries starting with `~` and move them to
the upgrade backup directory. Do not delete them directly.

```powershell
$sp = Resolve-Path -LiteralPath 'H:\Hermes_Windows_Native_014\venv\Lib\site-packages'
${REDACTED_SECRET}
New-Item -ItemType Directory -Force -Path $backup | Out-Null
$items = Get-ChildItem -LiteralPath $sp -Force | Where-Object { $_.Name -like '~*' }
foreach ($item in $items) {
  $resolved = Resolve-Path -LiteralPath $item.FullName
  if (-not ($resolved.Path.StartsWith($sp.Path, [System.StringComparison]::OrdinalIgnoreCase))) {
    throw "Refusing path outside site-packages: $($resolved.Path)"
  }
  Move-Item -LiteralPath $item.FullName -Destination (Join-Path $backup $item.Name)
}
H:\Hermes_Windows_Native_014\venv\Scripts\python.exe -m pip show hermes-agent
```

Success criterion: `pip show hermes-agent` returns 0.16.0 without invalid
distribution warnings.

## Critical 0.16.0 HERMES_HOME Issue

After the 0.16.0 upgrade, the gateway can appear healthy but use the wrong
profile if launchers do not force `HERMES_HOME`. Symptoms:

- 8642 `/health` returns 200.
- 8642 `/v1/models` returns `hermes-agent`.
- Chat returns `No models provided` or HTTP 502.
${REDACTED_SECRET}
${REDACTED_SECRET}
- `hermes config show` without `$env:HERMES_HOME` shows an empty or incomplete
  model config.
- Direct chat returns a DeepSeek 400 indicating the model name is empty even
  though `/v1/models` lists `hermes-agent`.
- Open WebUI displays the user's message and creates an assistant bubble, but
  the answer text is blank.

Fix the launchers so every path uses the real profile:

```powershell
# H:\Hermes_Windows_Native_014\launcher\start-hermes-openwebui.ps1
${REDACTED_SECRET}
$env:HERMES_HOME = $DataPath

# H:\Hermes_Windows_Native_014\launcher\auto-start-hermes-openwebui.ps1
${REDACTED_SECRET}
$env:HERMES_HOME = $HermesHome

# H:\Hermes_Windows_Native_014\launcher\hermes-014-runtime.ps1
${REDACTED_SECRET}
$LOG_DIR = Join-Path $HERMES_HOME 'logs'
$ENV_FILE = Join-Path $HERMES_HOME '.env'
$env:HERMES_HOME = $HERMES_HOME
$env:HOME = 'C:\Users\A'
& $HERMES_EXE gateway run --replace --accept-hooks @args
```

The old `hermes-014-runtime.ps1` entry is especially important because it can
still become the process that owns port 8642 after reboot or manual recovery.
Before the fix it used `H:\Hermes_Windows_Native_014\runtime` and could cause
${REDACTED_SECRET}
minimal config may contain only `model.provider: deepseek` and no model name.

When manually running config commands, set the profile first:

```powershell
${REDACTED_SECRET}
H:\Hermes_Windows_Native_014\venv\Scripts\hermes.exe config show
```

Avoid using bare `hermes config set` without `HERMES_HOME`; it can write to
${REDACTED_SECRET}

## Restart And Verification

Restart through the accepted autostart chain:

```powershell
cmd.exe /c "H:\Hermes_Windows_Native_014\AUTO-START-HERMES-OPENWEBUI.cmd"
```

Expected autostart log evidence:

```text
PASS Windows Hermes owns 8642 and health is OK
PASS /v1/models has hermes-agent
PASS Docker API already ready
PASS Open WebUI already healthy
PASS Open WebUI 3000 HTTP 200
OPEN existing Google Chrome profile to http://127.0.0.1:3000
FINAL_PASS Windows native Hermes Open WebUI autostart ready
```

Run direct Hermes chat:

```powershell
${REDACTED_SECRET}
  Where-Object { $_ -match "^API_SERVER_KEY=" } |
  Select-Object -First 1) -replace "^API_SERVER_KEY=", ""
$body = @{
  model = "hermes-agent"
  messages = @(@{ role = "user"; content = "Reply exactly HERMES_0160_DIRECT_OK" })
  stream = $false
} | ConvertTo-Json -Depth 8
Invoke-WebRequest -Uri "http://127.0.0.1:8642/v1/chat/completions" `
  -Method Post -UseBasicParsing -TimeoutSec 180 `
  -Headers @{ Authorization = "Bearer $key"; "Content-Type" = "application/json" } `
  -Body $body
```

Success criterion: HTTP 200 and response contains `HERMES_0160_DIRECT_OK`.

Run health and Telegram checks:

```powershell
${REDACTED_SECRET}
${REDACTED_SECRET}
```

Expected evidence:

```text
WINDOWS_HERMES_8642_MAINLINE_PASS
WINDOWS_HERMES_HEALTHCHECK_PASS
state api_server connected PASS
state telegram connected PASS
Hermes health endpoint PASS
Hermes models endpoint PASS
Open WebUI PASS
Result: PASS
```

Final acceptance can include the user's visible browser test in the already
logged-in Google Chrome profile, because that is the only proof that the
browser session and account state are actually usable.

