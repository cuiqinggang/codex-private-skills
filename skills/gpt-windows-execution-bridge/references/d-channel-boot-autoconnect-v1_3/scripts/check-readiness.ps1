param(
  [string]$ProjectRoot = 'C:/AI/DevSpace-Benchmark-20261031',
  [string]$ExpectedOrigin = '',
  [switch]$Fixed
)
$ErrorActionPreference = 'Stop'
$useFixed = $Fixed -or (Test-Path (Join-Path $ProjectRoot 'connector-fixed/active.json'))
$runtimeDirectory = if ($useFixed) { 'connector-fixed' } else { 'connector' }
$localPort = if ($useFixed) { 17677 } else { 17676 }
$r = [ordered]@{
  schema_version = 1
  checked_at = (Get-Date).ToUniversalTime().ToString('o')
  task_name = 'GPT-DevSpace-D-AutoConnect-V13'
  task_state = 'UNKNOWN'
  service_metadata = 'NOT_CHECKED'
  fixed_origin = 'NOT_VERIFIED'
  native_connection = 'NOT_MEASURED'
  reboot_acceptance = 'NOT_MEASURED'
  next_action = 'CHECK_EXISTING_SERVICE'
}
try { $r.task_state = [string](Get-ScheduledTask -TaskName $r.task_name).State }
catch { $r.task_state = 'UNAVAILABLE' }
try {
  $s = Get-Content (Join-Path $ProjectRoot ($runtimeDirectory + '/status.json')) -Raw -Encoding utf8 | ConvertFrom-Json
  $u = [uri]$s.origin
  if ($u.Scheme -ne 'https' -or $u.UserInfo -or $u.Query -or $u.Fragment -or $u.AbsolutePath -ne '/') { throw 'INVALID_ORIGIN' }
  $origin = $u.GetLeftPart([System.UriPartial]::Authority)
  if ($s.mcp_url -cne ($origin + '/mcp')) { throw 'MCP_URL_MISMATCH' }
  $r.mcp_url = $s.mcp_url
  $local = Invoke-RestMethod ('http://127.0.0.1:' + $localPort + '/.well-known/oauth-authorization-server') -TimeoutSec 8
  $headers = @{ 'User-Agent' = 'DChannelReadiness/1.2' }
  $public = Invoke-RestMethod ($origin + '/.well-known/oauth-authorization-server') -Headers $headers -TimeoutSec 8
  $resource = Invoke-RestMethod ($origin + '/.well-known/oauth-protected-resource/mcp') -Headers $headers -TimeoutSec 8
  if ($local.issuer -cne ($origin + '/') -or $public.issuer -cne $local.issuer -or $resource.resource -cne $s.mcp_url) { throw 'OAUTH_METADATA_MISMATCH' }
  $r.service_metadata = 'PASS'
  $r.refresh_grant_advertised = (@($public.grant_types_supported) -contains 'refresh_token')
  if ($u.Host -like '*.trycloudflare.com') {
    $r.fixed_origin = 'NO_QUICK_TUNNEL'
    $r.next_action = 'COMPLETE_NGROK_LOGIN_AND_FIXED_ENDPOINT'
  } elseif (-not $ExpectedOrigin) {
    $r.next_action = 'VERIFY_ACCOUNT_ASSIGNED_FIXED_ORIGIN'
  } elseif ($ExpectedOrigin.TrimEnd('/') -ceq $origin) {
    $r.fixed_origin = 'MATCHES_EXPECTED_ORIGIN'
    $r.next_action = 'VERIFY_NATIVE_CONNECTION_AND_REBOOT'
  } else {
    $r.fixed_origin = 'EXPECTED_ORIGIN_MISMATCH'
    $r.next_action = 'RECONCILE_CONFIGURATION'
  }
} catch {
  $r.service_metadata = 'FAIL_OR_UNAVAILABLE'
  $r.next_action = 'READ_EXISTING_HEALTH_RECEIPT_AND_RECONCILE'
}
$r | ConvertTo-Json -Depth 4
if ($r.service_metadata -ne 'PASS') { exit 2 }
# Exit 0 only describes this read-only check, never native or unattended acceptance.
