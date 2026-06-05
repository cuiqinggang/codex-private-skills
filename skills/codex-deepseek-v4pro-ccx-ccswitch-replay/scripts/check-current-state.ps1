param()

$ErrorActionPreference = "Continue"

function Test-PortOccupied {
    param([int]$Port)
    foreach ($hostName in @("127.0.0.1", "localhost")) {
        $client = [System.Net.Sockets.TcpClient]::new()
        try {
            $async = $client.BeginConnect($hostName, $Port, $null, $null)
            if ($async.AsyncWaitHandle.WaitOne(500)) {
                $client.EndConnect($async)
                return $true
            }
        } catch {
            # Connection refused or unavailable means no listener on this host form.
        } finally {
            $client.Close()
        }
    }
    return $false
}

$configPath = "C:\Users\A\.codex\config.toml"
$configExists = Test-Path -LiteralPath $configPath
$configText = if ($configExists) { Get-Content -LiteralPath $configPath -Raw } else { "" }
$model = ""
if ($configText -match '(?m)^\s*model\s*=\s*"([^"]+)"') { $model = $Matches[1] }
$forbiddenFlashPattern = '(?i)deepseek-v4-flash'

$ccxProc = Get-Process -Name "ccx-windows-amd64" -ErrorAction SilentlyContinue
$ccSwitchDb = "C:\Users\A\.cc-switch\cc-switch.db"
$providerExists = $false
if (Test-Path -LiteralPath $ccSwitchDb) {
    try {
        $py = @"
import sqlite3, pathlib
p = pathlib.Path(r'$ccSwitchDb')
con = sqlite3.connect(str(p))
row = con.execute("select count(*) from providers where app_type='codex' and name='DeepSeek-V4Pro-Backup-via-CCX'").fetchone()
print(row[0])
con.close()
"@
        $count = $py | python -
        $providerExists = ([int]$count -gt 0)
    } catch {
        $providerExists = $false
    }
}

$warn = $false
$rows = [ordered]@{
    ConfigExists = $configExists
    DefaultModel = $model
    SuperpowersEnabled = ($configText -match '(?i)superpowers')
    HasDeepSeekFlash = ($configText -match $forbiddenFlashPattern)
    Port3000Occupied = (Test-PortOccupied -Port 3000)
    Port13000Occupied = (Test-PortOccupied -Port 13000)
    CcxRunning = [bool]$ccxProc
    CcSwitchDbExists = (Test-Path -LiteralPath $ccSwitchDb)
    CcSwitchBackupProviderExists = $providerExists
}

foreach ($entry in $rows.GetEnumerator()) {
    Write-Output ("{0}: {1}" -f $entry.Key, $entry.Value)
}

if (-not $configExists) { $warn = $true }
if ($model -ne "gpt-5.5") { $warn = $true }
if (-not ($configText -match '(?i)superpowers')) { $warn = $true }
if ($configText -match $forbiddenFlashPattern) { $warn = $true }
if (-not $providerExists) { $warn = $true }

if ($warn) {
    Write-Output "SKILL_CHECK_WARN"
    exit 1
}

Write-Output "SKILL_CHECK_PASS"
exit 0
