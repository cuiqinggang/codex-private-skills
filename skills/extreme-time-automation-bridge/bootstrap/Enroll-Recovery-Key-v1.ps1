$ErrorActionPreference='Stop'
if(-not [Environment]::UserInteractive){throw 'ENROLL_ONLY_IN_INTERACTIVE_WINDOWS_SESSION'}
$vault=Join-Path $env:LOCALAPPDATA 'GPT-Windows-Tunnel'
$file=Join-Path $vault 'runtime-key.dpapi'
$task='GPT-Windows-Tunnel-Recovery-v1'
New-Item -Path $vault -ItemType Directory -Force | Out-Null
$user=[Security.Principal.WindowsIdentity]::GetCurrent().Name
& icacls.exe $vault '/inheritance:r' '/grant:r' ($user+':(OI)(CI)F') 'SYSTEM:(OI)(CI)F' '/Q' | Out-Null
if($LASTEXITCODE -ne 0){throw 'VAULT_ACL_FAILED'}
$secret=Read-Host 'Enter the Runtime Key on this PC (hidden, never sent to ChatGPT)' -AsSecureString
if($null -eq $secret -or $secret.Length -lt 16){throw 'RUNTIME_KEY_MISSING_OR_TOO_SHORT'}
$enc=ConvertFrom-SecureString -SecureString $secret
$tmp=$file+'.tmp'
[IO.File]::WriteAllText($tmp,$enc,[Text.UTF8Encoding]::new($false))
Move-Item -LiteralPath $tmp -Destination $file -Force
$test=ConvertTo-SecureString -String ([IO.File]::ReadAllText($file)) -ErrorAction Stop
if($test.Length -ne $secret.Length){throw 'DPAPI_SELF_TEST_FAILED'}
'DPAPI_ENROLLMENT=PASS'
'SECRET_STORED_ONLY_ENCRYPTED=TRUE'
$t=Get-ScheduledTask -TaskName $task -ErrorAction SilentlyContinue
if($t){Start-ScheduledTask -TaskName $task; 'RECOVERY_TASK_START_REQUESTED=TRUE'}
else {'RECOVERY_TASK_NOT_INSTALLED=TRUE'}
'CURRENT_TUNNEL_LEFT_UNCHANGED=TRUE'
Read-Host 'Press Enter to close' | Out-Null
