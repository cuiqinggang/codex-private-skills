# Read-only regression for GPT CEO + Codex Ultra continuous runtime v3.0.0
# Does not execute the runner, spawn Codex, modify flags, alter tasks or change network settings.
param([string]$Runner = $PSScriptRoot + '\CONTINUATION_RUNNER_V3.ps1')
$ErrorActionPreference = 'Stop'
$tokens = $null; $errors = $null
[System.Management.Automation.Language.Parser]::ParseFile($Runner,[ref]$tokens,[ref]$errors) | Out-Null
if ($errors.Count) { throw "PARSER_ERRORS=$($errors.Count)" }
$src = Get-Content -LiteralPath $Runner -Raw -Encoding UTF8
if ($src -notmatch 'RUNTIME_COMPONENT_VERSION=3\.0\.0') { throw 'VERSION_MISSING' }
if (-not $src.Contains('MANIFEST_SHA256=([A-Fa-f0-9]{64})\r?$')) { throw 'MANIFEST_CRLF_FIX_MISSING' }
if (-not $src.Contains('MOTHER_FINAL_VALID=YES\r?$')) { throw 'FINAL_CRLF_FIX_MISSING' }
$realHash='D378E405E49E83985ED000379630D183E942BFEF5A174CCF0357EDD0C34837BE'
$rx='(?m)^MANIFEST_SHA256=([A-Fa-f0-9]{64})\r?$'
$matchLF=([regex]::Match("MANIFEST_SHA256=$realHash`n",$rx)).Success
$matchCRLF=([regex]::Match("MANIFEST_SHA256=$realHash`r`n",$rx)).Success
$matchBad=([regex]::Match(('MANIFEST_SHA256='+('0'*64)+"`r`n"),$rx))
$rejectBad= $matchBad.Success -and $matchBad.Groups[1].Value -ne $realHash
$finalCRLF=("MOTHER_FINAL_VALID=YES`r`n" -match '(?m)^MOTHER_FINAL_VALID=YES\r?$')
$finalNo=("MOTHER_FINAL_VALID=NO`r`n" -match '(?m)^MOTHER_FINAL_VALID=YES\r?$')
if (-not ($matchLF -and $matchCRLF -and $rejectBad -and $finalCRLF -and -not $finalNo)) { throw 'FIXTURE_FAIL' }
# Optional current-real-state readback; scoped to user-provided workdir, no writes.
$root='C:\AI\Polsia-Codex-20261011'
$realtime='NOT_RUN'
$mother=Join-Path $root 'MOTHER_CURRENT.md'
if (Test-Path -LiteralPath $mother) {
  $data=Get-Content $mother -Raw -Encoding UTF8
  $match=[regex]::Match($data,$rx)
  if (-not $match.Success) {throw 'CURRENT_MANIFEST_FIELD_MISSING'}
  $pathMatch=[regex]::Match($data,'(?m)^MANIFEST_PATH=(.+)\r?$')
  if (-not $pathMatch.Success) {throw 'CURRENT_MANIFEST_PATH_MISSING'}
  $path=$pathMatch.Groups[1].Value.Trim()
  if (-not ([IO.Path]::GetFullPath($path).StartsWith(([IO.Path]::GetFullPath($root).TrimEnd('\')+'\'),[StringComparison]::OrdinalIgnoreCase))) {throw 'MANIFEST_OUT_OF_SCOPE'}
  if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {throw 'CURRENT_MANIFEST_FILE_MISSING'}
  if ((Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash -ne $match.Groups[1].Value) {throw 'CURRENT_MANIFEST_SHA_MISMATCH'}
  $realtime='PASS_READONLY_LOCAL_SHA'
}
[pscustomobject]@{Result='PASS_READONLY';Version='3.0.0';Parser='PASS';LF=$matchLF;CRLF=$matchCRLF;WrongHashRejected=$rejectBad;FinalYesCRLF=$finalCRLF;FinalNoRejected=(-not $finalNo);CurrentLocal=$realtime;CodexStarted=0;SchedulerMutated=$false} | ConvertTo-Json -Compress
