$ErrorActionPreference='Stop';$r='C:\AI\Polsia-V5-Parallel-20261012'
$a=Get-Content (Join-Path $r 'contracts\CEO_APPROVED_FIVE.json') -Raw -Encoding utf8|ConvertFrom-Json
if($a.gpt_ceo_approval -ne 'POLSIA-CEO-D008-POL5-20261012' -or @($a.branches).Count -ne 5){throw 'CEO授权不匹配'}
$exe='C:\Program Files\PowerShell\7\pwsh.exe';$receipts=@()
foreach($b in $a.branches){
 if($b.disposition -ne 'CEO_APPROVED_LOCAL_ISOLATED' -or $b.locator -ne ('【Polsia执行页｜'+$a.task_id+'｜'+$b.id+'｜实】')){throw '双门定位不通过'}
 $script=Join-Path $r ('branches\'+$b.id+'.ps1');if(-not(Test-Path $script)){throw ('工作单脚本未找到：'+$b.id)}
 $status=Join-Path $r ('branches\'+$b.id+'\status.json')
 if(Test-Path $status){$receipts+=@{branch=$b.id;state='ALREADY_EXISTS_NO_REPLAY'};continue}
 $proc=Start-Process -FilePath $exe -ArgumentList @('-NoLogo','-NoProfile','-NonInteractive','-File',('"' + $script + '"')) -WindowStyle Hidden -PassThru -WorkingDirectory $r -RedirectStandardOutput (Join-Path $r ('evidence\'+$b.id+'.out.log')) -RedirectStandardError (Join-Path $r ('evidence\'+$b.id+'.err.log'))
 $receipts+=@{branch=$b.id;pid=$proc.Id;state='START_REQUESTED'}
}
$receipts|ConvertTo-Json -Depth 6|Set-Content (Join-Path $r 'evidence\five-dispatch-receipt.json') -Encoding utf8
$receipts|ConvertTo-Json -Compress -Depth 6