# Version 3.1.0 read-only contract regression: never executes runner or launches Codex.
param([string]$Runner='C:\AI\Polsia-Codex-20261011\CONTINUATION_RUNNER_V3_1.ps1')
$ErrorActionPreference='Stop'
$tok=$null;$errs=$null
[System.Management.Automation.Language.Parser]::ParseFile($Runner,[ref]$tok,[ref]$errs) | Out-Null
if($errs.Count){throw 'PARSER_FAILED'}
$s=Get-Content -LiteralPath $Runner -Raw -Encoding UTF8
foreach($fragment in @('RUNTIME_COMPONENT_VERSION=3.1.0','REASON=CEO_NEXT_SCOPE_DECISION_REQUIRED','CODEX_LAUNCHED=NO','CODEX_EXIT_ZERO_WITHOUT_NEW_VERIFIED_FREEZE','MANIFEST_SHA256=([A-Fa-f0-9]{64})\r?$')) {if(-not $s.Contains($fragment)){throw ('REQUIRED_FRAGMENT_ABSENT:'+ $fragment)}}
$gate='(?m)^NEXT_DISPOSITION=CEO_APPROVED_[A-Z0-9_]+\r?$'
$tests=@(
 @{label='approved_crlf';value="NEXT_DISPOSITION=CEO_APPROVED_CODEX007_OFFLINE_ONLY`r`n";want=$true},
 @{label='approved_lf';value="NEXT_DISPOSITION=CEO_APPROVED_CODEX007_OFFLINE_ONLY`n";want=$true},
 @{label='proposed_crlf';value="NEXT_DISPOSITION=PROPOSED_ONLY;NOT_EXECUTED`r`n";want=$false},
 @{label='no_field';value="NEXT_NODE=CODEX-007`r`n";want=$false},
 @{label='unknown';value="NEXT_DISPOSITION=UNKNOWN`r`n";want=$false}
)
foreach($t in $tests){$real=($t.value -match $gate);if($real -ne $t.want){throw ('GATE_FAILURE:'+ $t.label)}}
$root='C:\AI\Polsia-Codex-20261011'
$state=Get-Content (Join-Path $root 'MOTHER_CURRENT.md') -Raw -Encoding UTF8
$manifest=([regex]::Match($state,'(?m)^MANIFEST_SHA256=([A-Fa-f0-9]{64})\r?$')).Groups[1].Value
$path=([regex]::Match($state,'(?m)^MANIFEST_PATH=(.+)\r?$')).Groups[1].Value.Trim()
if(-not $manifest -or -not (Test-Path -LiteralPath $path -PathType Leaf)){throw 'FREEZE_INPUT_MISSING'}
$actual=(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash
if($manifest -ne $actual){throw 'MANIFEST_SHA_MISMATCH'}
$bad=[regex]::Match("MANIFEST_SHA256=$('0'*64)`r`n",'(?m)^MANIFEST_SHA256=([A-Fa-f0-9]{64})\r?$')
if(-not $bad.Success -or $bad.Groups[1].Value -eq $actual){throw 'WRONG_HASH_CHECK_FAILED'}
[pscustomobject]@{Result='PASS_READONLY';Version='3.1.0';Parser=$true;GateFixtures=$tests.Count;CorrectManifest=$true;WrongHashRejected=$true;NoCodexStarted=$true;ScheduledTaskUnchanged=$true} | ConvertTo-Json -Compress
