#requires -Version 5.1
# V6 pure advisory only. No networking, credential reads, process changes or dispatch.
[CmdletBinding()]
param(
  [ValidateSet('ready','down','unknown','quota_blocked')][string]$CState='unknown',
  [ValidateSet('ready','down','unknown')][string]$AState='unknown',
  [ValidateSet('ready','down','unknown')][string]$BState='unknown',
  [switch]$RequiresGitHubEvidence,
  [ValidateSet('new','completed','unknown')][string]$TaskExecutionState='new'
)
$ErrorActionPreference='Stop'
$route='BLOCKED';$reason='NO_VALID_ROUTE'
if($TaskExecutionState -eq 'unknown') { $reason='CHECK_EXISTING_TASK_BEFORE_RETRY' }
elseif($TaskExecutionState -eq 'completed') { $reason='ALREADY_COMPLETED_DO_NOT_REPLAY' }
elseif($RequiresGitHubEvidence) {
  if($BState -eq 'ready') { $route='B';$reason='EXPLICIT_GITHUB_EVIDENCE_REQUIRED' }
  else { $reason='GITHUB_EVIDENCE_ROUTE_UNAVAILABLE' }
}
elseif($CState -eq 'ready') { $route='C';$reason='C_DEFAULT_PRIORITY' }
elseif($CState -eq 'unknown') { $reason='CHECK_C_REAL_TOOL_AND_QUOTA_FIRST' }
elseif($AState -eq 'ready') { $route='A';$reason='C_UNAVAILABLE_A_READY' }
elseif($AState -eq 'unknown') { $reason='CHECK_A_REAL_TOOL_BEFORE_B' }
elseif($BState -eq 'ready') { $route='B';$reason='C_AND_A_UNAVAILABLE_B_READY' }
[ordered]@{
  version='6.0.0';policy='C_FIRST_A_SECOND_B_THIRD';selected_route=$route
  decision=$reason;requires_github_evidence=[bool]$RequiresGitHubEvidence
  advisory_only=$true;no_automatic_dispatch=$true
} | ConvertTo-Json -Compress
