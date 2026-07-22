param([Parameter(Mandatory=$true)][string[]]$RouteStatePaths,[Parameter(Mandatory=$true)][string]$OutputDirectory)
$ErrorActionPreference='Stop'; $out=[IO.Path]::GetFullPath($OutputDirectory); if($out-match'^[Kk]:\\'){throw'禁止写入 K 盘'};New-Item -ItemType Directory -Force -Path $out|Out-Null;$rows=@()
foreach($sp in $RouteStatePaths){$s=Get-Content -LiteralPath $sp -Encoding UTF8 -Raw|ConvertFrom-Json;$rows+=[pscustomobject]@{route=$s.task_name;status=$s.route_status;tests=@($s.tests).Count;passed=@($s.tests|Where-Object status -eq 'passed').Count;decision=if($s.route_status-eq'ROUTE_PASS'){'ADOPT_ALL'}elseif($s.route_status-eq'ROUTE_PARTIAL_PASS'){'ADOPT_PARTIAL'}else{'ARCHIVE'};evidence=$sp}}
$rows|Export-Csv -LiteralPath (Join-Path $out 'route-comparison.csv') -NoTypeInformation -Encoding UTF8; @('# Route Comparison','', '| Route | Status | Tests | Passed | Decision | Evidence |','|---|---|---:|---:|---|---|')+@($rows|ForEach-Object{"| $($_.route) | $($_.status) | $($_.tests) | $($_.passed) | $($_.decision) | `$($_.evidence)` |"})|Set-Content -LiteralPath (Join-Path $out 'route-comparison.md') -Encoding UTF8; $rows|ConvertTo-Json -Depth 8










