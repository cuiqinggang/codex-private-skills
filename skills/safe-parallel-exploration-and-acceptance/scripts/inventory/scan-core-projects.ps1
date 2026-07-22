param([Parameter(Mandatory=$true)][string[]]$ProjectPaths,[Parameter(Mandatory=$true)][string]$OutputDirectory)
$ErrorActionPreference='Stop'
Import-Module (Join-Path $PSScriptRoot '..\SafeExploration.Core.psm1') -Force
$out=Assert-ActivePath $OutputDirectory
New-Item -ItemType Directory -Force -Path $out|Out-Null
$rows=@()
foreach($raw in $ProjectPaths){
    $p=Resolve-SafeFullPath $raw
    if(-not (Test-Path -LiteralPath $p -PathType Container)){
        $rows+=[pscustomobject]@{name=(Split-Path -Leaf $p);path=$p;exists=$false;git_repository=$false;repository_root='';branch='';head='';dirty=$false;remote=$false;nested_repository='unknown';large_file_count=0;sensitive_name_count=0;environment='';worktree_suitable=$false;hooks_suitable=$false;recommended_mode='';status='NOT_FOUND'}
        continue
    }
    $git=Get-GitSnapshot $p
    $repoRoot=if($git.is_git_repository){(& git -C $p rev-parse --show-toplevel|Out-String).Trim()}else{''}
    $remote=if($git.is_git_repository){[bool]((& git -C $p remote|Out-String).Trim())}else{$false}
    $files=@(Get-ChildItem -LiteralPath $p -Recurse -File -Force -ErrorAction SilentlyContinue | Where-Object {$_.FullName -notmatch '\\(\.git|node_modules|\.venv|venv|__pycache__|dist|build|cache|outputs|backups)(\\|$)'} | Select-Object -First 5001)
    $large=@($files|Where-Object {$_.Length -ge 10MB -or $_.Extension -in @('.mp4','.mov','.mkv','.wav','.mp3','.onnx','.safetensors','.ckpt','.zip')})
    $sensitive=@($files|Where-Object {$_.Name -match '^(\.env($|\.)|.*(token|secret|credential|api[_-]?key|password).*)$|\.(pem|key|pfx|p12)$'})
    $env=@(Get-ProjectEnvironment $p)-join'+'
    $status=if($git.is_git_repository -and $git.status.Count -eq 0){'GIT_READY'}elseif($git.is_git_repository){'MANUAL_REVIEW_REQUIRED'}elseif($large.Count -gt 0 -or $files.Count -gt 5000){'MANUAL_REVIEW_REQUIRED'}else{'SAFE_BASELINE_CANDIDATE'}
    $mode=if($p -match 'ultrafusion|long-coding|knowledge-brain'){'MODE-C'}elseif($status -eq 'GIT_READY'){'MODE-B'}else{'MODE-A'}
    $rows+=[pscustomobject]@{name=(Split-Path -Leaf $p);path=$p;exists=$true;git_repository=$git.is_git_repository;repository_root=$repoRoot;branch=$git.branch;head=$git.head;dirty=($git.status.Count-gt0);remote=$remote;nested_repository='bounded_scan_not_asserted';large_file_count=$large.Count;sensitive_name_count=$sensitive.Count;environment=$env;worktree_suitable=($git.is_git_repository -and [bool]$git.head);hooks_suitable=$true;recommended_mode=$mode;status=$status}
}
$csv=Join-Path $out '20_核心项目Git与环境联合盘点.csv';$md=Join-Path $out '20_核心项目Git与环境联合盘点.md'
$rows|Export-Csv -LiteralPath $csv -NoTypeInformation -Encoding UTF8
$lines=@('# 20 核心项目 Git 与环境联合盘点','',"- 扫描时间：$(Get-Date -Format o)",'- 范围：用户指定和 Knowledge Brain 命中的 C 盘核心路径；未扫描 K 盘。','', '| 项目 | 路径 | Git | 状态 | 环境 | Worktree | 推荐模式 |','|---|---|---:|---|---|---:|---|')
$lines+=@($rows|ForEach-Object{"| $($_.name) | `$($_.path)` | $($_.git_repository) | $($_.status) | $($_.environment) | $($_.worktree_suitable) | $($_.recommended_mode) |"})
$lines|Set-Content -LiteralPath $md -Encoding UTF8
[pscustomobject]@{count=$rows.Count;git_ready=@($rows|Where-Object git_repository).Count;baseline_candidates=@($rows|Where-Object status -eq 'SAFE_BASELINE_CANDIDATE').Count;manual_review=@($rows|Where-Object status -eq 'MANUAL_REVIEW_REQUIRED').Count;csv=$csv;markdown=$md}|ConvertTo-Json -Depth 8




