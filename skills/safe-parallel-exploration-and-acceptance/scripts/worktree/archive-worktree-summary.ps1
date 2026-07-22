param([Parameter(Mandatory=$true)][string]$WorktreePath,[Parameter(Mandatory=$true)][string]$ArchivePath)
$ErrorActionPreference='Stop'
$w=[IO.Path]::GetFullPath($WorktreePath);$a=[IO.Path]::GetFullPath($ArchivePath)
if($a -match '^[Kk]:\\'){throw '禁止写入 K 盘'}
New-Item -ItemType Directory -Force -Path $a|Out-Null
$lines=@('# Worktree Archive Summary','',"- Worktree: $w","- Time: $(Get-Date -Format o)",'','## Git status','```text')+@(& git -C $w status --short)+@('```','','## Commits','```text')+@(& git -C $w log --oneline -10)+@('```')
$slug=(Split-Path -Leaf $w) -replace '[^A-Za-z0-9._-]','-'
$out=Join-Path $a ("worktree-summary-$slug-"+(Get-Date -Format yyyyMMdd-HHmmss-fff)+'.md')
$lines|Set-Content -LiteralPath $out -Encoding UTF8
$out



