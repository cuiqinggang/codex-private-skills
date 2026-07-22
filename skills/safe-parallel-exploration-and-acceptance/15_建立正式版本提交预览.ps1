param([Parameter(Mandatory=$true)][string]$ProjectPath,[string]$Version='v1.0.0')
$p=[IO.Path]::GetFullPath($ProjectPath);[pscustomobject]@{status='PREVIEW_ONLY';project=$p;version=$Version;branch=(& git -C $p branch --show-current);head=(& git -C $p rev-parse HEAD);git_status=@(& git -C $p status --short);actions=@('update CHANGELOG','update version','commit after user confirmation','tag after acceptance');auto_commit=$false;auto_merge=$false;auto_push=$false}|ConvertTo-Json -Depth 8







