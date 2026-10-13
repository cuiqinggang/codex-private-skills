#requires -Version 5.1
<#
.SYNOPSIS
  GPT-Windows dual bridge v0.3.4: pure, zero-network free-quota route advice.
.DESCRIPTION
  No Windows remote calls, changes, authentication, dispatch, or persisted state.
  Pass states proven for THIS task; do not equate ping or generic smoke with ability.
#>
[CmdletBinding()]
param(
  [ValidateSet('interactive','batch','long','recovery')][string]$TaskKind='interactive',
  [ValidateSet('ready','down','unknown')][string]$AState='unknown',
  [ValidateSet('ready','down','unknown')][string]$BState='unknown',
  [ValidateSet('ready','down','unknown','quota_blocked')][string]$RState='unknown',
  [ValidateRange(-1,10000)][int]$RemoteUsedCalls=-1,
  [ValidateRange(-1,100)][double]$RemoteRemainingPercent=-1,
  [ValidateRange(1,10000)][int]$EstimatedRemoteCalls=1,
  [ValidateSet('Auto','A','B','R')][string]$RequestedRoute='Auto',
  [switch]$Emergency,
  [switch]$ExplicitRemoteApproval
)
$ErrorActionPreference='Stop'
$warnings=New-Object 'System.Collections.Generic.List[string]'
$used=-1
$usageSource='UNKNOWN'
if($RemoteUsedCalls -ge 0){
  $used=$RemoteUsedCalls
  $usageSource='VERIFIED_REMOTE_USED'
} elseif($RemoteRemainingPercent -ge 0){
  # Rounded percent is only an approximation; conservatively round used upward.
  $used=[int][math]::Ceiling((100.0-$RemoteRemainingPercent)*100.0)
  $usageSource='APPROX_REMOTE_PERCENT'
}
$budget='UNKNOWN'
$rEligible=($RState -eq 'ready')
if($RState -eq 'quota_blocked'){
  $budget='EXHAUSTED'
  $rEligible=$false
  $warnings.Add('R_QUOTA_BLOCKED: never retry or re-pair to regain quota')
} elseif($used -lt 0){
  $rEligible=$false
  if($RequestedRoute -eq 'R'){
    $warnings.Add('R_USAGE_UNKNOWN: check official Remote quota dashboard before requesting Remote')
  }
} else {
  $predicted=$used+$EstimatedRemoteCalls
  if($used -ge 10000 -or $predicted -gt 10000){
    $budget='EXHAUSTED'
    $rEligible=$false
    $warnings.Add('R_NO_REMAINING_BUDGET: use A or B; do not retry')
  } elseif($used -ge 9500){
    $budget='MANUAL_ONLY_9500'
    $rEligible= $rEligible -and $Emergency.IsPresent -and $ExplicitRemoteApproval.IsPresent
    $warnings.Add('R_ABOVE_9500: explicit approval for EACH emergency request required')
  } elseif($used -ge 8000 -or $predicted -gt 9500){
    $budget='EMERGENCY_ONLY_8000'
    $rEligible= $rEligible -and $Emergency.IsPresent -and $ExplicitRemoteApproval.IsPresent -and ($predicted -le 9500)
    $warnings.Add('R_ABOVE_8000: stop normal Remote calls, preserve emergency reserve')
  } elseif($used -ge 7500){
    $budget='ORANGE_7500'
    $warnings.Add('R_ORANGE: use Remote only if A/B do not meet this task')
  } elseif($used -ge 6000){
    $budget='YELLOW_6000'
    $warnings.Add('R_YELLOW: stop nonessential Remote calls; prefer A/B')
  } else {
    $budget='NORMAL'
  }
}
if($TaskKind -eq 'long' -and $BState -eq 'ready'){
  $selected='B'
} elseif($AState -eq 'ready'){
  $selected='A'
} elseif($BState -eq 'ready'){
  $selected='B'
} elseif($rEligible){
  $selected='R'
} else {
  $selected='BLOCKED'
}
if($RequestedRoute -ne 'Auto' -and $RequestedRoute -ne $selected){
  $warnings.Add("ROUTE_MISMATCH: requested $RequestedRoute; selected $selected; change to the available lower-cost suitable route")
}
if($RequestedRoute -eq 'R' -and $selected -eq 'A'){
  $warnings.Add('R_WOULD_WASTE_QUOTA: prefer already-usable self-managed MCP')
}
if($RequestedRoute -eq 'B' -and $TaskKind -eq 'interactive' -and $AState -eq 'ready'){
  $warnings.Add('B_SLOW_FOR_INTERACTIVE: prefer A, avoid per-command GitHub job startup')
}
if($selected -eq 'BLOCKED'){
  $warnings.Add('NO_VALID_ROUTE: inspect per-task authorization/capability; do not retry a side-effecting UNKNOWN task')
}
$next= switch($selected){
  'A' { 'Use established OpenAI Tunnel + local open-source MCP; verify final output' }
  'B' { 'Dispatch existing suitable GitHub workflow once with task_id; verify run/job plus business result' }
  'R' { 'Use official Remote only for justified need; count actual calls and reserve quota' }
  default { 'Stop execution, report precise blocker and available repair path' }
}
[ordered]@{
  policy='REMOTE_DCR_QUOTA_OPERATIONS_V1'
  version='0.3.4'
  task_kind=$TaskKind
  selected_route=$selected
  status=$(if($selected -eq 'BLOCKED'){'BLOCKED'}else{'READY'})
  budget_status=$budget
  remote_usage_source=$usageSource
  remote_used_estimate=$(if($used -ge 0){$used}else{$null})
  estimated_remote_calls=$EstimatedRemoteCalls
  warnings=@($warnings.ToArray())
  suggested_action=$next
  note='Pre-call advisory only; not a remote-dispatch interceptor and not proof of live reachability'
} | ConvertTo-Json -Depth 5 -Compress
