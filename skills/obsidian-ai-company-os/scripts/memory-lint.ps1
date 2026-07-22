param(
  [Parameter(Mandatory=$true)][string]$CandidatePath,
  [string]$OutputPath = ""
)

$ErrorActionPreference = 'Stop'
$allowedStatus = @('candidate','confirmed','deprecated','archived')
$required = @('stable_id','source','created_at','updated_at','status','scope')
$files = if (Test-Path -LiteralPath $CandidatePath -PathType Container) {
  @(Get-ChildItem -LiteralPath $CandidatePath -File -Recurse -Filter '*.md')
} elseif (Test-Path -LiteralPath $CandidatePath -PathType Leaf) {
  @(Get-Item -LiteralPath $CandidatePath)
} else { throw "CandidatePath not found: $CandidatePath" }

$rows = @()
$seen = @{}
foreach ($file in $files) {
  $text = Get-Content -LiteralPath $file.FullName -Raw
  $front = if ($text -match '(?s)^---\s*(.*?)\s*---') { $Matches[1] } else { '' }
  $meta = @{}
  foreach ($line in ($front -split "`r?`n")) {
    if ($line -match '^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$') { $meta[$Matches[1].ToLowerInvariant()] = $Matches[2].Trim().Trim('"') }
  }
  $errors = @()
  foreach ($name in $required) { if (-not $meta.ContainsKey($name) -or [string]::IsNullOrWhiteSpace($meta[$name])) { $errors += "MISSING_$($name.ToUpperInvariant())" } }
  if ($meta.stable_id -and $meta.stable_id -notmatch '^mem-[a-z0-9][a-z0-9._-]{2,127}$') { $errors += 'INVALID_STABLE_ID' }
  if ($meta.status -and $meta.status -notin $allowedStatus) { $errors += 'INVALID_STATUS' }
  if ($meta.scope -and $meta.scope -notmatch '^(global|project:[^\s]+|workflow:[^\s]+)$') { $errors += 'INVALID_SCOPE' }
  foreach ($field in @('created_at','updated_at')) { if ($meta[$field]) { try { [void][DateTimeOffset]::Parse($meta[$field]) } catch { $errors += "INVALID_$($field.ToUpperInvariant())" } } }
  if ($meta.stable_id) { if ($seen.ContainsKey($meta.stable_id)) { $errors += 'DUPLICATE_STABLE_ID'; $seen[$meta.stable_id] += @($file.FullName) } else { $seen[$meta.stable_id] = @($file.FullName) } }
  $rows += [pscustomobject]@{path=$file.FullName;stable_id=$meta.stable_id;status=$meta.status;scope=$meta.scope;result=$(if($errors.Count){'FAIL'}else{'PASS'});errors=$errors}
}
$failed = @($rows | Where-Object result -eq 'FAIL').Count
$result = [pscustomobject]@{generated_at=(Get-Date).ToString('o');candidate_path=(Resolve-Path -LiteralPath $CandidatePath).Path;files=$files.Count;passed=$files.Count-$failed;failed=$failed;result=$(if($failed){'FAIL'}else{'PASS'});rows=$rows}
if ($OutputPath) { $result | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $OutputPath -Encoding UTF8 }
$result | ConvertTo-Json -Depth 8
if ($failed) { exit 1 }
