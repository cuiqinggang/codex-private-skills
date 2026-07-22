param([Parameter(Mandatory=$true)][string]$IntegrationWorktree,[Parameter(Mandatory=$true)][string]$OutputPath)
$p=[IO.Path]::GetFullPath($IntegrationWorktree)
$lines=@('# 主线准入建议','','- 自动合并：否','- 自动 push：否',"- 当前分支：$(& git -C $p branch --show-current)","- HEAD：$(& git -C $p rev-parse HEAD)",'','## Git status','```text')+@(& git -C $p status --short)+@('```','','## Diff stat','```text')+@(& git -C $p diff --stat)+@('```','','## 人工确认','- 展示测试、限制和回滚后，由用户决定是否合并 main。')
$out=[IO.Path]::GetFullPath($OutputPath)
$parent=Split-Path -Parent $out
if($parent){New-Item -ItemType Directory -Force -Path $parent|Out-Null}
$lines|Set-Content -LiteralPath $out -Encoding UTF8







