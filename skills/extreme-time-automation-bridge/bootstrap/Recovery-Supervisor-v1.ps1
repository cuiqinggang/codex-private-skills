param([switch]$ProbeOnly)
$ErrorActionPreference='Stop'
$root='C:\AI\GPT-Windows-Bridge-B'
$persist=Join-Path $root 'persistence'
$exe=Join-Path $root 'tunnel\v0.0.16\tunnel-client.exe'
$entry=Join-Path $root 'mcp\node_modules\@wonderwhy-er\desktop-commander\dist\index.js'
$tunnelId='tunnel_6acbeee2ce888191b775cd53429c7597'
$keyFile=Join-Path (Join-Path $env:LOCALAPPDATA 'GPT-Windows-Tunnel') 'runtime-key.dpapi'
$log=Join-Path $persist 'Recovery-Supervisor-v1.jsonl'
function Note([string]$event,[object]$value) {
  $obj=@{utc=[DateTime]::UtcNow.ToString('o');event=$event;detail=$value;supervisor_pid=$PID}
  $line=$obj|ConvertTo-Json -Compress -Depth 3
  Add-Content -LiteralPath $log -Value $line -Encoding UTF8
  if($ProbeOnly){Write-Output $line}
}
$mutex=[Threading.Mutex]::new($false,'Local\GPT-Windows-Tunnel-Recovery-v1')
$owns=$false
try {
  $owns=$mutex.WaitOne(0)
  if(!$owns){Note 'ALREADY_RUNNING' $null;return}
  $user=[Security.Principal.WindowsIdentity]::GetCurrent().Name
  $expected=$env:USERDOMAIN+'\'+$env:USERNAME
  if($user -ne $expected){throw 'USER_IDENTITY_MISMATCH'}
  if($ProbeOnly) {
    $p=@(Get-CimInstance Win32_Process -Filter "Name='tunnel-client.exe'")
    Note 'PROBE' @{tunnel_count=$p.Count;key_enrolled=(Test-Path $keyFile);exe_present=(Test-Path $exe);mcp_present=(Test-Path $entry);user=$user}
    return
  }
  Note 'SUPERVISOR_STARTED' $user
  $last=''
  $quickFailures=0
  while($true) {
    $all=@(Get-CimInstance Win32_Process -Filter "Name='tunnel-client.exe'")
    if($all.Count -gt 0) {
      $status=if($all.Count -eq 1){'EXISTING_TUNNEL'}else{'MULTIPLE_TUNNELS'}
      if($status -ne $last){Note $status @($all|ForEach-Object{$_.ProcessId});$last=$status}
      Start-Sleep -Seconds 10
      continue
    }
    if(!(Test-Path $keyFile)){if($last-ne 'WAITING_FOR_LOCAL_ENROLLMENT'){Note 'WAITING_FOR_LOCAL_ENROLLMENT' $null;$last='WAITING_FOR_LOCAL_ENROLLMENT'};Start-Sleep -Seconds 15;continue}
    if(!(Test-Path $exe) -or !(Test-Path $entry)){if($last-ne 'BINARIES_MISSING'){Note 'BINARIES_MISSING' $null;$last='BINARIES_MISSING'};Start-Sleep -Seconds 30;continue}
    $last='START_ATTEMPT'
    $secure=$null;$bstr=[IntPtr]::Zero
    try {
      $encrypted=Get-Content -LiteralPath $keyFile -Raw -ErrorAction Stop
      $secure=ConvertTo-SecureString -String $encrypted -ErrorAction Stop
      if($secure.Length -lt 16){throw 'ENROLLED_KEY_TOO_SHORT'}
      $bstr=[Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
      $env:CONTROL_PLANE_API_KEY=[Runtime.InteropServices.Marshal]::PtrToStringBSTR($bstr)
    } catch {
      Note 'CREDENTIAL_UNAVAILABLE' $_.Exception.GetType().Name
      Start-Sleep -Seconds 60
      continue
    } finally {
      if($bstr -ne [IntPtr]::Zero){[Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr)}
      $bstr=[IntPtr]::Zero;$secure=$null
    }
    $started=[DateTime]::UtcNow;$exitCode=-999
    try {
      if(@(Get-CimInstance Win32_Process -Filter "Name='tunnel-client.exe'").Count -ne 0) {
        Note 'START_ABORT_EXISTING_PROCESS' $null
        continue
      }
      $mcpCommand='node.exe '+($entry.Replace('\','/'))+' --no-onboarding'
      Note 'TUNNEL_START' @{mcp='official_stdio';pid=$PID}
      $savedErrorActionPreference=$ErrorActionPreference
      try {
        $ErrorActionPreference='Continue'
        & $exe run --control-plane.tunnel-id $tunnelId --mcp.command $mcpCommand --mcp.stdio-send-initialized-notification --health.listen-addr 127.0.0.1:0 2>&1 | Out-Null
        $exitCode=$LASTEXITCODE
      } finally {
        $ErrorActionPreference=$savedErrorActionPreference
      }
    } catch {
      Note 'TUNNEL_EXCEPTION' $_.Exception.GetType().Name
    } finally {
      Remove-Item Env:\CONTROL_PLANE_API_KEY -ErrorAction SilentlyContinue
    }
    $elapsed=([DateTime]::UtcNow-$started).TotalSeconds
    Note 'TUNNEL_EXIT' @{code=$exitCode;elapsed_seconds=[math]::Round($elapsed,1)}
    if($elapsed -ge 180){$quickFailures=0}else{$quickFailures++}
    $delay=if($quickFailures -ge 5){180}else{[math]::Min(60,5*[math]::Pow(2,$quickFailures))}
    Start-Sleep -Seconds $delay
  }
} finally {
  if($owns){$mutex.ReleaseMutex()}
  $mutex.Dispose()
}
