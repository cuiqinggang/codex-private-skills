param([Parameter(Mandatory=$true)][string]$IntegrationWorktree)
$p=[IO.Path]::GetFullPath($IntegrationWorktree);$unmerged=@(& git -C $p diff --name-only --diff-filter=U);$status=@(& git -C $p status --short);$sensitive=@($status|Where-Object{$_-match'\.env|\.pem|\.key|\.pfx|\.p12'});[pscustomobject]@{status=if($unmerged.Count-or$sensitive.Count){'CONFLICTS_FOUND'}else{'NO_BLOCKING_CONFLICTS'};unmerged=$unmerged;sensitive_status=$sensitive;git_status=$status}|ConvertTo-Json -Depth 8










