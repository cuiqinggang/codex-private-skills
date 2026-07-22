param(
    [int]$MinChars = 2000,
    [string]$OutputDirectory = "$env:USERPROFILE\.codex\manual-paste-attachments",
    [int]$PollMilliseconds = 200,
    [string]$TargetMode = "Codex"
)

$ErrorActionPreference = "Stop"

if ([Threading.Thread]::CurrentThread.GetApartmentState() -ne "STA") {
    Start-Process powershell.exe -WindowStyle Hidden -ArgumentList @(
        "-NoProfile",
        "-ExecutionPolicy", "Bypass",
        "-STA",
        "-File", "`"$PSCommandPath`"",
        "-MinChars", "$MinChars",
        "-OutputDirectory", "`"$OutputDirectory`"",
        "-PollMilliseconds", "$PollMilliseconds",
        "-TargetMode", "`"$TargetMode`""
    )
    exit
}

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Security
Add-Type @"
using System;
using System.Runtime.InteropServices;
public static class ForegroundWindow {
    [DllImport("user32.dll")]
    public static extern IntPtr GetForegroundWindow();
    [DllImport("user32.dll")]
    public static extern uint GetWindowThreadProcessId(IntPtr hWnd, out uint processId);
    [DllImport("user32.dll", CharSet=CharSet.Unicode)]
    public static extern int GetWindowText(IntPtr hWnd, System.Text.StringBuilder text, int count);
}
"@

New-Item -ItemType Directory -Force -Path $OutputDirectory | Out-Null
$logPath = Join-Path $OutputDirectory "auto-longtext-fileclip.log"
$pendingHash = $null
$pendingPath = $null
$pendingOriginalText = $null
$pendingCreatedAt = $null
$targetModes = @(
    $TargetMode -split "," |
        ForEach-Object { $_.Trim() } |
        Where-Object { $_ }
)
if ($targetModes.Count -eq 0) {
    $targetModes = @("Codex")
}

function Write-Log {
    param([string]$Message)
    $line = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') $Message"
    Add-Content -LiteralPath $logPath -Value $line -Encoding UTF8
}

function Get-TextHash {
    param([string]$Text)
    $sha = [System.Security.Cryptography.SHA256]::Create()
    try {
        $bytes = [System.Text.Encoding]::UTF8.GetBytes($Text)
        return ([BitConverter]::ToString($sha.ComputeHash($bytes))).Replace("-", "").ToLowerInvariant()
    } finally {
        $sha.Dispose()
    }
}

function Set-ClipboardFile {
    param([string]$Path)
    $files = New-Object System.Collections.Specialized.StringCollection
    [void]$files.Add($Path)
    [System.Windows.Forms.Clipboard]::SetFileDropList($files)
}

function Invoke-ClipboardOperation {
    param(
        [scriptblock]$Operation,
        [int]$Attempts = 10,
        [int]$DelayMilliseconds = 80
    )

    $lastError = $null
    for ($i = 0; $i -lt $Attempts; $i++) {
        try {
            return & $Operation
        } catch {
            $lastError = $_.Exception.Message
            Start-Sleep -Milliseconds $DelayMilliseconds
        }
    }
    throw $lastError
}

function Try-GetClipboardText {
    try {
        return Invoke-ClipboardOperation -Operation {
            if ([System.Windows.Forms.Clipboard]::ContainsText()) {
                return [System.Windows.Forms.Clipboard]::GetText()
            }
            return $null
        }
    } catch {
        Write-Log "CLIPBOARD_BUSY getText failed: $($_.Exception.Message)"
        return $null
    }
}

function Try-SetClipboardFile {
    param([string]$Path)
    try {
        Invoke-ClipboardOperation -Operation {
            Set-ClipboardFile $Path
            return $true
        } | Out-Null
        return $true
    } catch {
        Write-Log "CLIPBOARD_BUSY setFile failed: $($_.Exception.Message)"
        return $false
    }
}

function Test-ClipboardHasDifferentLongText {
    param([string]$ActivatedPath)

    try {
        $text = Try-GetClipboardText
        if ($text -eq $null) { return $false }
        if ($text.Length -lt $MinChars) { return $false }
        if ($pendingHash -eq $null) { return $true }
        return ((Get-TextHash $text) -ne $pendingHash)
    } catch {
        return $false
    }
}

function Get-TargetForeground {
    try {
        $hwnd = [ForegroundWindow]::GetForegroundWindow()
        if ($hwnd -eq [IntPtr]::Zero) { return $null }
        [uint32]$foregroundProcessId = 0
        [void][ForegroundWindow]::GetWindowThreadProcessId($hwnd, [ref]$foregroundProcessId)
        $titleBuilder = New-Object System.Text.StringBuilder 512
        [void][ForegroundWindow]::GetWindowText($hwnd, $titleBuilder, 512)
        $foregroundTitle = $titleBuilder.ToString()
        if ($foregroundProcessId -eq 0) { return $null }
        $p = Get-Process -Id $foregroundProcessId -ErrorAction SilentlyContinue
        if ($p -eq $null) { return $null }
        if ($targetModes -contains "CursorKilo") {
            if ($p.ProcessName -match "Cursor") {
                return "CursorKilo"
            }
        }
        if ($targetModes -contains "Codex") {
            if ($foregroundTitle -match "Codex") {
                return "Codex"
            }
            if ($p.ProcessName -match "Codex" -or $p.Path -match "Codex") {
                return "Codex"
            }
        }
        return $null
    } catch {
        return $null
    }
}

Write-Log "START MinChars=$MinChars TargetMode=$TargetMode OutputDirectory=$OutputDirectory"

while ($true) {
    try {
        $text = Try-GetClipboardText
        if ($text -ne $null) {
            if ($text -ne $null -and $text.Length -ge $MinChars) {
                $hash = Get-TextHash $text
                if ($hash -ne $pendingHash) {
                    $timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
                    $shortHash = $hash.Substring(0, 8)
                    $path = Join-Path $OutputDirectory "codex-pasted-text-$timestamp-$shortHash.txt"
                    [System.IO.File]::WriteAllText($path, $text, [System.Text.UTF8Encoding]::new($false))
                    $pendingHash = $hash
                    $pendingPath = $path
                    $pendingOriginalText = $text
                    $pendingCreatedAt = Get-Date
                    Write-Log "PENDING chars=$($text.Length) file=$path"
                }
            }
        }

        if ($pendingPath -ne $null -and $pendingCreatedAt -ne $null -and (Get-Date) -gt $pendingCreatedAt.AddMinutes(2)) {
            Write-Log "EXPIRED pending conversion after timeout file=$pendingPath"
            $pendingHash = $null
            $pendingPath = $null
            $pendingOriginalText = $null
            $pendingCreatedAt = $null
        }

        $foregroundTarget = Get-TargetForeground
        if ($pendingPath -ne $null -and (Test-Path -LiteralPath $pendingPath) -and $foregroundTarget -ne $null) {
            $activatedPath = $pendingPath
            $ok = Try-SetClipboardFile $activatedPath
            if ($ok) {
                Write-Log "ACTIVATED file clipboard for $foregroundTarget file=$activatedPath"
                $holdUntil = (Get-Date).AddSeconds(6)
                while ((Get-Date) -lt $holdUntil -and (Get-TargetForeground) -ne $null -and (Test-Path -LiteralPath $activatedPath)) {
                    Start-Sleep -Milliseconds 350
                    if (Test-ClipboardHasDifferentLongText -ActivatedPath $activatedPath) {
                        Write-Log "HOLD_ABORTED new long clipboard text detected while holding file=$activatedPath"
                        break
                    }
                    Try-SetClipboardFile $activatedPath | Out-Null
                }
                $pendingHash = $null
                $pendingPath = $null
                $pendingOriginalText = $null
                $pendingCreatedAt = $null
            }
        }
    } catch {
        Write-Log "ERROR $($_.Exception.Message)"
    }
    Start-Sleep -Milliseconds $PollMilliseconds
}
