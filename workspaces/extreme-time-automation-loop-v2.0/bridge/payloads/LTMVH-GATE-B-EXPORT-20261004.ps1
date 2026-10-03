param(
  [Parameter(Mandatory=$true)][string]$BridgeWorkDir,
  [Parameter(Mandatory=$true)][string]$TaskFile
)
$ErrorActionPreference='Stop'
$root='C:\AI\LTMVH-Gate-B-20261004'
$names=@(
  'BACKUP-BRAIN-BUSINESS-DONE-WHEN-20261004.md',
  'reasonix-attempt5-raw-write-event.jsonl',
  'reasonix-attempt5-metrics.json',
  'reasonix-attempt5-extraction.json'
)
$out=@()
foreach($name in $names){
  $p=Join-Path $root $name
  if(-not (Test-Path -LiteralPath $p)){ throw "MISSING_EVIDENCE: $p" }
  $bytes=[IO.File]::ReadAllBytes($p)
  $sha=(Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash
  $out += [ordered]@{
    name=$name
    path=$p
    size_bytes=$bytes.Length
    sha256=$sha
    base64=[Convert]::ToBase64String($bytes)
  }
}
[ordered]@{
  schema_version=1
  task='LTMVH-GATE-B-EXPORT-20261004'
  machine=$env:COMPUTERNAME
  runner=$env:RUNNER_NAME
  files=$out
} | ConvertTo-Json -Depth 6 -Compress | Write-Output
exit 0
