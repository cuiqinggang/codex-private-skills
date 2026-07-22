param([Parameter(Mandatory=$true)][string]$ProjectPath,[switch]$ConfirmDisable)
$p=[IO.Path]::GetFullPath($ProjectPath);$policy=Join-Path $p '.codex\exploration-policy.json'
if(-not $ConfirmDisable){[pscustomobject]@{status='PREVIEW_ONLY';project=$p;preserve=@('evidence','Git history','worktrees','rollback records')}|ConvertTo-Json;exit 0}
if(Test-Path -LiteralPath $policy){$s=Get-Content -LiteralPath $policy -Encoding UTF8 -Raw|ConvertFrom-Json;$s.enabled=$false;$s|Add-Member -NotePropertyName disabled_at -NotePropertyValue (Get-Date -Format o) -Force;$s|ConvertTo-Json|Set-Content -LiteralPath $policy -Encoding UTF8}
[pscustomobject]@{status='SAFE_EXPLORATION_DISABLED';project=$p;evidence_preserved=$true;worktrees_preserved=$true}|ConvertTo-Json





