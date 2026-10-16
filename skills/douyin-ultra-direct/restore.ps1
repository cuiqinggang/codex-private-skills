param(
    [string]$SourceDir = $PSScriptRoot
)

$ErrorActionPreference = 'Stop'

$Target = 'C:\AI\Douyin-Ultra-Direct'
$Desktop = [Environment]::GetFolderPath('Desktop')
$entryName = (@([char]0x6296,[char]0x97F3,[char]0x6781,[char]0x901F,[char]0x76F4,[char]0x4E0B,'.vbs') -join '')
$DesktopEntry = Join-Path $Desktop $entryName

$required = @('run.py','run-hidden.vbs','SKILL.md','RESTORE.md','legacy_direct_save.py')
foreach($name in $required){
    $p = Join-Path $SourceDir $name
    if(-not (Test-Path -LiteralPath $p)){
        throw "SOURCE_FILE_MISSING: $p"
    }
}

$python = 'C:\Users\A\AppData\Local\Programs\Python\Python313\python.exe'
if(-not (Test-Path -LiteralPath $python)){
    $cmd = Get-Command python.exe -ErrorAction SilentlyContinue
    if(-not $cmd){ throw 'PYTHON_NOT_FOUND' }
    $python = $cmd.Source
}

$curl = Get-Command curl.exe -ErrorAction Stop
$ffprobe = Get-Command ffprobe.exe -ErrorAction Stop

New-Item -ItemType Directory -Force -Path $Target | Out-Null

function Copy-IfDifferent {
    param([string]$Source,[string]$Destination)
    $src = [System.IO.Path]::GetFullPath($Source)
    $dst = [System.IO.Path]::GetFullPath($Destination)
    if($src -ieq $dst){ return }
    Copy-Item -LiteralPath $Source -Destination $Destination -Force
}

Copy-IfDifferent -Source (Join-Path $SourceDir 'run.py') -Destination (Join-Path $Target 'run.py')
$launcherText = [IO.File]::ReadAllText((Join-Path $SourceDir 'run-hidden.vbs'))
[IO.File]::WriteAllText((Join-Path $Target 'run-hidden.vbs'),$launcherText,[Text.Encoding]::Unicode)
Copy-IfDifferent -Source (Join-Path $SourceDir 'SKILL.md') -Destination (Join-Path $Target 'SKILL.md')
Copy-IfDifferent -Source (Join-Path $SourceDir 'RESTORE.md') -Destination (Join-Path $Target 'RESTORE.md')
[IO.File]::WriteAllText($DesktopEntry,$launcherText,[Text.Encoding]::Unicode)
$legacyTarget = 'C:\AI\Douyin-Direct-Save-Windows\src\direct_save.py'
if(Test-Path -LiteralPath $legacyTarget){
    Copy-Item -LiteralPath $legacyTarget -Destination ($legacyTarget + '.backup-' + (Get-Date -Format 'yyyyMMdd-HHmmss'))
    Copy-IfDifferent -Source (Join-Path $SourceDir 'legacy_direct_save.py') -Destination $legacyTarget
}

& $python -m py_compile (Join-Path $Target 'run.py')
if($LASTEXITCODE -ne 0){ throw 'PY_COMPILE_FAIL' }

$coreHash = (Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $Target 'run.py')).Hash.ToLowerInvariant()
$launcherHash = (Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $Target 'run-hidden.vbs')).Hash.ToLowerInvariant()
$desktopHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $DesktopEntry).Hash.ToLowerInvariant()

if($launcherHash -ne $desktopHash){ throw 'DESKTOP_ENTRY_MISMATCH' }

Write-Output 'RESTORE=PASS'
Write-Output ('CORE=' + (Join-Path $Target 'run.py'))
Write-Output ('CORE_SHA256=' + $coreHash)
Write-Output ('DESKTOP_ENTRY=' + $DesktopEntry)
Write-Output ('ENTRY_SHA256=' + $desktopHash)
Write-Output ('CURL=' + $curl.Source)
Write-Output ('FFPROBE=' + $ffprobe.Source)
Write-Output ('FALLBACK_PRESENT=' + (Test-Path -LiteralPath 'C:\AI\Douyin-Direct-Save-Windows\Douyin-Direct-Save.cmd'))
Write-Output 'REALITY_EXECUTED=NO'
