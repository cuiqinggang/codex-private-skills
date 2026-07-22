param([Parameter(Mandatory=$true)][string]$ProjectPath)
$ErrorActionPreference='Stop'; & git -c core.quotepath=false -C ([IO.Path]::GetFullPath($ProjectPath)) worktree list --porcelain










