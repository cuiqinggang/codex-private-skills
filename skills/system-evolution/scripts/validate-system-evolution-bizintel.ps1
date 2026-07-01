$ErrorActionPreference='Stop'
$Skill='C:\Users\A\.codex\skills\system-evolution'
$Task='TASK-SYS-EVO-BIZINTEL-PLAN-20260521-R2'
$Backup=Join-Path $Skill "backups\$Task"
Write-Host 'VALIDATE_BEGIN'

$RequiredFiles=@(
  'SKILL.md',
  'references\execution-policy.md',
  'references\video-source-intelligence.md',
  'references\long-coding-flow.md',
  'references\aggregation-distribution-biz-intel.md'
)

foreach($f in $RequiredFiles){
  $p=Join-Path $Skill $f
  if(!(Test-Path $p)){
    Write-Host "VALIDATE_FAIL_MISSING_FILE=$f"
    exit 1
  }
}

function Decode-Utf8Base64([string]$Value) {
  [System.Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($Value))
}

$RequiredKeywords=@(
  (Decode-Utf8Base64 '6IGa5ZCI5YiG5Y+R572R56uZ5ZWG5Lia5oOF5oql5aKe5by657O757uf'),
  (Decode-Utf8Base64 '5L2O5Lmw'),
  (Decode-Utf8Base64 '6auY5Y2W'),
  (Decode-Utf8Base64 '6aqM6K+B5Lu75Yqh'),
  (Decode-Utf8Base64 'c2tpbGwg5pu05paw6I2J5qGI'),
  'Business Intelligence Execution Boundary',
  (Decode-Utf8Base64 '6IGa5ZCI5YiG5Y+R572R56uZ55u45YWz6KeG6aKR5oOF5oql6KeE5YiZ'),
  'Business Intelligence Engineering Flow',
  'Level 3'
)

$All=''
foreach($f in $RequiredFiles){
  $All += "`n" + (Get-Content -LiteralPath (Join-Path $Skill $f) -Raw -Encoding UTF8)
}
foreach($k in $RequiredKeywords){
  if($All -notmatch [Regex]::Escape($k)){
    Write-Host "VALIDATE_FAIL_MISSING_KEYWORD=$k"
    exit 1
  }
}

$Before=Join-Path $Backup 'forbidden-path-hashes-before.txt'
$After=Join-Path $Backup 'forbidden-path-hashes-after.txt'
Remove-Item -LiteralPath $After -Force -ErrorAction SilentlyContinue
$Forbidden=@(
  'C:\Users\A\.codex\config.toml',
  'C:\Users\A\.codex\AGENTS.md',
  'C:\Users\A\.codex\auth.json',
  'C:\Users\A\.codex\tokens.json'
)

foreach($p in $Forbidden){
  if(Test-Path $p){
    $h=(Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash
    "$h  $p" | Add-Content -LiteralPath $After -Encoding UTF8
  } else {
    "MISSING  $p" | Add-Content -LiteralPath $After -Encoding UTF8
  }
}

if((Test-Path $Before) -and (Test-Path $After)){
  $b=Get-Content -LiteralPath $Before -Raw -Encoding UTF8
  $a=Get-Content -LiteralPath $After -Raw -Encoding UTF8
  if($b -ne $a){
    Write-Host 'VALIDATE_FAIL_FORBIDDEN_PATH_HASH_CHANGED'
    exit 1
  }
} else {
  Write-Host 'VALIDATE_FAIL_FORBIDDEN_HASH_BASELINE_MISSING'
  exit 1
}

Write-Host 'VALIDATE_PASS_BIZINTEL_SKILL_OK'
Write-Host 'VALIDATE_END'
