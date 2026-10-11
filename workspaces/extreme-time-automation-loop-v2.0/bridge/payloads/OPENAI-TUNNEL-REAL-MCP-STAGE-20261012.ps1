param(
    [string]$BridgeWorkDir,
    [string]$TaskFile,
    [switch]$Launch
)
$ErrorActionPreference = 'Stop'
$root = 'C:\AI\GPT-Windows-Bridge-B'
$installed = Join-Path $root 'Launch-OpenAI-Real-MCP.ps1'
$exe = Join-Path $root 'tunnel\v0.0.16\tunnel-client.exe'
$entry = Join-Path $root 'mcp\node_modules\@wonderwhy-er\desktop-commander\dist\index.js'
$tunnelId = 'tunnel_6acbeee2ce888191b775cd53429c7597'

if (-not $Launch) {
    if (-not $TaskFile -or -not $BridgeWorkDir) { throw 'Staging requires the authorized bridge task inputs.' }
    if (-not (Test-Path -LiteralPath $exe)) { throw 'FULL_TUNNEL_CLIENT_MISSING' }
    if (-not (Test-Path -LiteralPath $entry)) { throw 'REAL_DESKTOP_COMMANDER_MCP_MISSING' }
    $code = [IO.File]::ReadAllText($PSCommandPath)
    $tokens=$null;$errors=$null
    [void][System.Management.Automation.Language.Parser]::ParseInput($code,[ref]$tokens,[ref]$errors)
    if ($errors.Count) { throw ('STAGE_PARSE_FAIL: ' + ($errors | Out-String)) }
    [IO.File]::WriteAllText($installed,$code,[Text.UTF8Encoding]::new($false))
    $check=(Get-FileHash -LiteralPath $installed -Algorithm SHA256).Hash
    Write-Output "REAL_TUNNEL_LAUNCHER_STAGED=$installed"
    Write-Output "REAL_TUNNEL_LAUNCHER_SHA256=$check"
    Write-Output 'REAL_TUNNEL_STAGE_PASS'
    Write-Output 'DEMO_TUNNEL_LEFT_UNCHANGED=YES'
    Write-Output 'NO_RUNTIME_KEY_USED=YES'
    exit 0
}
if (-not [Environment]::UserInteractive) { throw 'Requires an interactive Windows user session, not Windows Runner NETWORK SERVICE.' }
$identity = [Security.Principal.WindowsIdentity]::GetCurrent().Name
if ($identity -match 'NETWORK SERVICE|SYSTEM|LOCAL SERVICE') { throw "Invalid account for desktop tunnel: $identity" }
$node = (Get-Command node.exe -ErrorAction Stop).Source
foreach ($item in @($exe,$entry)) { if (-not (Test-Path -LiteralPath $item)) { throw "Missing: $item" } }
Write-Host "Windows user: $identity"
Write-Host "Official tunnel: $exe"
Write-Host "Real MCP entrypoint: $entry"
Write-Host "Tunnel ID: $tunnelId"
Write-Warning 'This will replace the demo mcp-stub with REAL Desktop Commander MCP, including file writes and command execution.'
Write-Warning 'User approved retaining the ChatGPT plugin settings: No authentication + Allow all actions. Neither setting is modified by this script.'
Write-Warning 'These settings allow highly privileged tool calls without per-action confirmations. The OpenAI tunnel/workspace access must remain controlled, and the key must stay local.'
Write-Host 'User consent for these plugin settings is recorded in the 2026-10-12 skill update. Only the runtime key must be entered interactively.'
$key = Read-Host 'Paste the OpenAI runtime API key (hidden)' -AsSecureString
if ($key.Length -lt 16) { throw 'RUNTIME_KEY_MISSING_OR_TOO_SHORT' }
$ptr=[Runtime.InteropServices.Marshal]::SecureStringToBSTR($key)
try { $env:CONTROL_PLANE_API_KEY = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($ptr) }
finally { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($ptr) }
try {
    $all=@(Get-CimInstance Win32_Process | Where-Object {$_.Name -eq 'tunnel-client.exe'})
    if ($all.Count -gt 1) { throw "MULTIPLE_ACTIVE_TUNNEL_CLIENTS: $($all.Count); refuse unsafe switch" }
    if ($all.Count -eq 1) {
        $p=$all[0]
        if ([string]::IsNullOrWhiteSpace($p.CommandLine)) { throw "CANNOT_VERIFY_EXISTING_TUNNEL_PROCESS_$($p.ProcessId)" }
        if ($p.CommandLine -notmatch [regex]::Escape($tunnelId)) { throw "EXISTING_TUNNEL_DIFFERENT_ID_$($p.ProcessId)" }
        if ($p.CommandLine -notmatch 'embedded-mcp-stub') { throw "EXISTING_PROCESS_NOT_DEMO_$($p.ProcessId)" }
        Write-Host "Stopping only confirmed demo tunnel process PID $($p.ProcessId)"
        Stop-Process -Id $p.ProcessId -ErrorAction Stop
        for($i=0;$i -lt 20;$i++){if(-not (Get-Process -Id $p.ProcessId -ErrorAction SilentlyContinue)){break};Start-Sleep -Milliseconds 250}
        if(Get-Process -Id $p.ProcessId -ErrorAction SilentlyContinue){throw 'DEMO_TUNNEL_NOT_STOPPED'}
    }
    $mcpCmd = '"' + $node + '" "' + $entry + '" --no-onboarding'
    Write-Host 'Starting real Desktop Commander MCP over the existing official tunnel.'
    Write-Host 'Keep this console open; the health URL is dynamic. No credentials are written to disk.'
    & $exe run --control-plane.tunnel-id $tunnelId --mcp.command $mcpCmd --health.listen-addr 127.0.0.1:0
    $code=$LASTEXITCODE
    if($code -ne 0){throw "TUNNEL_REAL_MCP_EXIT_$code"}
} finally {
    Remove-Item Env:\CONTROL_PLANE_API_KEY -ErrorAction SilentlyContinue
}
