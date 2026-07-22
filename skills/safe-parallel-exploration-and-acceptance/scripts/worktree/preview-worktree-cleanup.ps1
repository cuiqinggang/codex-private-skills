param([Parameter(Mandatory=$true)][string]$ProjectPath,[Parameter(Mandatory=$true)][string]$WorktreePath)
$ErrorActionPreference='Stop'; $p=[IO.Path]::GetFullPath($WorktreePath); $status=@(& git -C $p status --short 2>$null); $summary=(Test-Path -LiteralPath (Join-Path $p 'FAILURE_NOTES.md')) -or (Test-Path -LiteralPath (Join-Path $p 'INTEGRATION_ACCEPTANCE.md'))
[pscustomobject]@{status='PREVIEW_ONLY';worktree=$p;dirty=($status.Count-gt 0);status_lines=$status;summary_exists=$summary;safe_candidate=($status.Count-eq 0 -and $summary);command="git -C <project> worktree remove -- <worktree>"}|ConvertTo-Json -Depth 8










