param(
  [Parameter(Mandatory = $false)]
  [string]$Number,

  [Parameter(Mandatory = $true)]
  [string]$Title,

  [Parameter(Mandatory = $true)]
  [string]$ReportPath,

  [Parameter(Mandatory = $false)]
  [string]$EvidenceZipPath,

  [Parameter(Mandatory = $false)]
  [string[]]$KeyFiles = @(),

  [Parameter(Mandatory = $false)]
  [string]$KeyFilesList
)

$ErrorActionPreference = 'Stop'
$desktop = 'C:\Users\A\Desktop'

function Get-NextNumber {
  for ($i = 100; $i -le 999; $i++) {
    $n = [string]$i
    if (-not (Test-Path -LiteralPath (Join-Path $desktop $n)) -and
        -not (Test-Path -LiteralPath (Join-Path $desktop "$n.zip"))) {
      return $n
    }
  }
  throw 'No available three-digit desktop number.'
}

if ([string]::IsNullOrWhiteSpace($Number)) {
  $Number = Get-NextNumber
}

if ($Number -notmatch '^\d{3}$') {
  throw 'Number must be exactly three digits.'
}

$folder = Join-Path $desktop $Number
$zip = Join-Path $desktop "$Number.zip"
$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'

if (Test-Path -LiteralPath $folder) {
  Move-Item -LiteralPath $folder -Destination (Join-Path $desktop "$Number.backup-$stamp") -Force
}

if (Test-Path -LiteralPath $zip) {
  Move-Item -LiteralPath $zip -Destination (Join-Path $desktop "$Number.zip.backup-$stamp") -Force
}

New-Item -ItemType Directory -Force -Path $folder | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $folder 'key_files') | Out-Null

if (-not (Test-Path -LiteralPath $ReportPath)) {
  throw "ReportPath not found: $ReportPath"
}

Copy-Item -LiteralPath $ReportPath -Destination $folder -Force

if ($EvidenceZipPath -and (Test-Path -LiteralPath $EvidenceZipPath)) {
  Copy-Item -LiteralPath $EvidenceZipPath -Destination $folder -Force
}

$allKeyFiles = @()
if ($KeyFiles) {
  $allKeyFiles += $KeyFiles
}

if (-not [string]::IsNullOrWhiteSpace($KeyFilesList)) {
  $allKeyFiles += ($KeyFilesList -split ';' | Where-Object { -not [string]::IsNullOrWhiteSpace($_) })
}

foreach ($file in $allKeyFiles) {
  if ($file -and (Test-Path -LiteralPath $file)) {
    Copy-Item -LiteralPath $file -Destination (Join-Path $folder 'key_files') -Force
  }
}

@"
# $Number Package

Title:
$Title

Report:
$ReportPath

Evidence ZIP:
$EvidenceZipPath

Rule:
This is a compact desktop numeric handoff package for tools that cannot read the chat transcript.
"@ | Set-Content -LiteralPath (Join-Path $folder "README_$Number.md") -Encoding UTF8

Add-Type -AssemblyName System.IO.Compression.FileSystem
[System.IO.Compression.ZipFile]::CreateFromDirectory($folder, $zip, [System.IO.Compression.CompressionLevel]::Optimal, $false, [System.Text.Encoding]::UTF8)

$zipObj = [System.IO.Compression.ZipFile]::OpenRead($zip)
try {
  $entries = $zipObj.Entries.Count
} finally {
  $zipObj.Dispose()
}

[PSCustomObject]@{
  Number = $Number
  Folder = $folder
  Zip = $zip
  ZipBytes = (Get-Item -LiteralPath $zip).Length
  ZipEntries = $entries
}
