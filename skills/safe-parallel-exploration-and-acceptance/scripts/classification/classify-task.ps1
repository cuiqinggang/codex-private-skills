param(
  [Parameter(Mandatory=$true)][string]$ProjectPath,
  [Parameter(Mandatory=$true)][string]$TaskDescription,
  [ValidateSet('low','medium','high','critical')][string]$Risk='medium',
  [int]$FileCount=1,
  [switch]$StableVersion,
  [switch]$MultipleSolutions,
  [switch]$Parallel,
  [switch]$RollbackRequired,
  [switch]$FormalDelivery,
  [ValidateSet('L0','L1','L2','L3','UNKNOWN')][string]$DefaultLevel='UNKNOWN'
)
$ErrorActionPreference='Stop'
$score=0
switch($Risk){'medium'{$score+=2};'high'{$score+=4};'critical'{$score+=6}}
if($StableVersion){$score+=2}; if($MultipleSolutions){$score+=3}; if($Parallel){$score+=3}; if($RollbackRequired){$score+=2}; if($FormalDelivery){$score+=2}
if($FileCount -gt 5){$score+=1}; if($FileCount -gt 20){$score+=1}
switch($DefaultLevel){'L2'{$score=[Math]::Max($score,4)};'L3'{$score=[Math]::Max($score,7)}}
if($Risk -eq 'low' -and -not $MultipleSolutions -and -not $Parallel -and $FileCount -le 2){$mode='MODE-A'} elseif($score -ge 7){$mode='MODE-C'} else {$mode='MODE-B'}
$statusCode=if($mode -eq 'MODE-C'){30}elseif($mode -eq 'MODE-B'){20}else{10}
$result=[ordered]@{schema_version='1.0';status_code=$statusCode;project_path=[IO.Path]::GetFullPath($ProjectPath);task_description=$TaskDescription;score=$score;mode=$mode;git_required=($mode-ne'MODE-A');worktree_required=($mode-ne'MODE-A');three_round_tests=($mode-eq'MODE-C' -or $FormalDelivery);screenshots_required=[bool]$FormalDelivery;zip_required=[bool]$FormalDelivery;manual_review_required=($Risk-in @('high','critical') -or $StableVersion);integration_candidate_required=($mode-eq'MODE-C');reason="risk=$Risk; stable=$([bool]$StableVersion); multiple=$([bool]$MultipleSolutions); parallel=$([bool]$Parallel); default_level=$DefaultLevel"}
$result | ConvertTo-Json -Depth 8
exit 0










