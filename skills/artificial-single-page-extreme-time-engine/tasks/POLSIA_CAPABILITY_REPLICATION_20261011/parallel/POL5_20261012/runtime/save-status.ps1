param([Parameter(Mandatory=$true)][string]$Id,[Parameter(Mandatory=$true)][string]$Status,[Parameter(Mandatory=$true)][string]$Step,[int]$Verified=0,[string]$Evidence='',[string]$Issue='')
$ErrorActionPreference='Stop'
$root='C:\AI\Polsia-V5-Parallel-20261012'
$ap=Get-Content -LiteralPath (Join-Path $root 'contracts\CEO_APPROVED_FIVE.json') -Encoding utf8 -Raw|ConvertFrom-Json
$b=@($ap.branches|Where-Object {$_.id -eq $Id})|Select-Object -First 1
if(-not $b -or $b.disposition -ne 'CEO_APPROVED_LOCAL_ISOLATED' -or $b.locator -ne "【Polsia执行页｜$($ap.task_id)｜$Id｜实】"){throw '授权与页面定位核验失败'}
$folder=Join-Path $root ('branches\'+$Id)
New-Item -Path $folder -ItemType Directory -Force|Out-Null
$file=Join-Path $folder 'status.json'
$started=([DateTime]::UtcNow).ToString('o')
if(Test-Path $file){try{$old=Get-Content $file -Encoding utf8 -Raw|ConvertFrom-Json;if($old.started_utc){$started=$old.started_utc}}catch{}}
$out=[ordered]@{id=$Id;name=$b.name;status=$Status;step=$Step;verified_steps=$Verified;planned_steps=4;checkpoint='母冻结V008；本分支未冻结';evidence=$Evidence;issue=$Issue;contract_blob=$b.contract_blob;locator=$b.locator;started_utc=$started;updated_utc=([DateTime]::UtcNow).ToString('o')}
$temp=$file+'.'+$PID+'.tmp'
[IO.File]::WriteAllText($temp,($out|ConvertTo-Json -Depth 8),[Text.UTF8Encoding]::new($false))
Move-Item -LiteralPath $temp -Destination $file -Force
try{& (Join-Path $root 'monitor\publish-status.ps1') -Once|Out-Null}catch{}
Write-Output "$Id $Status $Verified/4"