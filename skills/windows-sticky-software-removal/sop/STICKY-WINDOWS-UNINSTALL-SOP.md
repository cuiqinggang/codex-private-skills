# Sticky Windows Software Removal SOP

## Purpose

Remove Windows software that resists normal uninstall without breaking unrelated system components or network access.

This SOP is based on the Xunfei IME removal case. It is especially useful for IMEs, 360-like tools, security suites, shell extensions, updaters, and software that keeps restarting after uninstall.

## Phase 0: Safety

1. Confirm the user explicitly wants removal.
2. Identify software name, publisher, install path, process names, package ID.
3. Do not close proxy/network clients unless the user explicitly approves. If the app pulling the target alive is a proxy such as FlClash, choose boot-time deletion instead.
4. Do not delete broad folders such as `C:\Program Files (x86)\Vendor` unless verified empty or single-product.
5. For security suites, assume self-protection and drivers may exist. Prefer official uninstaller first; do not rip out drivers blindly in a live system.

## Phase 1: Normal Uninstall

Check:

```powershell
winget list --id <Package.Id>
Get-ItemProperty 'HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*','HKLM:\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*' |
  Where-Object { $_.DisplayName -like '*PRODUCT*' }
```

Try:

```powershell
winget uninstall --id <Package.Id> --silent --accept-source-agreements
```

Then verify:

```powershell
winget list --id <Package.Id>
Get-Process | Where-Object { $_.ProcessName -match '<process-pattern>' }
Test-Path '<install-path>'
```

If uninstall reports success but artifacts remain, continue.

## Phase 2: Remove Active User Integration

For IMEs/input methods:

```powershell
Get-WinUserLanguageList | ForEach-Object {
  [PSCustomObject]@{
    LanguageTag=$_.LanguageTag
    InputMethodTips=($_.InputMethodTips -join ', ')
  }
} | Format-List
```

Remove target IME TIP from the language list:

```powershell
$list=Get-WinUserLanguageList
foreach($lang in $list){
  $tips=@($lang.InputMethodTips | Where-Object { $_ -notmatch '<target-tip-guid-or-clsid>' })
  $lang.InputMethodTips.Clear()
  foreach($tip in $tips){ [void]$lang.InputMethodTips.Add($tip) }
}
Set-WinUserLanguageList $list -Force
```

Also clean current-user CTF remnants:

```powershell
Remove-Item -LiteralPath 'HKCU:\Software\Microsoft\CTF\DirectSwitchHotkeys\<key>' -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -LiteralPath 'HKCU:\Software\Microsoft\CTF\TIP\<target-clsid>' -Recurse -Force -ErrorAction SilentlyContinue
```

## Phase 3: Find What Revives It

Kill once, wait, then inspect parent process:

```powershell
taskkill /F /IM <target.exe> /T
Start-Sleep -Seconds 5
Get-CimInstance Win32_Process -Filter "Name='<target.exe>'" |
  Select-Object ProcessId,ParentProcessId,Name,CommandLine
```

If parent is Explorer, Codex, FlClash, browser, or another ordinary app, it may be restoring an old input context or loading a shell/IME component. Do not kill critical/proxy apps casually. Prefer removing registrations or boot-time deletion.

## Phase 4: Remove Persistence

Check:

```powershell
Get-CimInstance Win32_Service | Where-Object { $_.Name -match '<pattern>' -or $_.DisplayName -match '<pattern>' }
Get-ScheduledTask | Where-Object { $_.TaskName -match '<pattern>' -or $_.TaskPath -match '<pattern>' }
Get-ItemProperty 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Run','HKLM:\Software\Microsoft\Windows\CurrentVersion\Run','HKLM:\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Run' -ErrorAction SilentlyContinue
```

Remove exact entries only.

For 360-like security suites also check drivers:

```powershell
Get-CimInstance Win32_SystemDriver |
  Where-Object { $_.Name -match '<pattern>' -or $_.DisplayName -match '<pattern>' -or $_.PathName -match '<install-path-pattern>' } |
  Select-Object Name,DisplayName,State,StartMode,PathName
```

For IME/COM/TSF registrations, identify exact GUIDs from registry values pointing to install path:

```powershell
Get-ChildItem 'HKLM:\Software\Microsoft\CTF','HKLM:\Software\WOW6432Node\Classes','HKLM:\Software\Classes' -Recurse -ErrorAction SilentlyContinue |
  ForEach-Object {
    $p=$_.PSPath
    $props=Get-ItemProperty -LiteralPath $p -ErrorAction SilentlyContinue
    foreach($prop in $props.PSObject.Properties){
      if(($prop.Value -is [string]) -and ($prop.Value -like '*Vendor*Product*')){
        [PSCustomObject]@{Key=$p;Name=$prop.Name;Value=$prop.Value}
      }
    }
  }
```

## Phase 5: Take Ownership And Try Hot Delete

Only after integrations are removed:

```powershell
takeown /F "<install-path>" /R /D Y
icacls "<install-path>" /grant SYSTEM:F Administrators:F /T /C
taskkill /F /IM <target.exe> /T
Remove-Item -LiteralPath "<install-path>" -Recurse -Force
```

If access denied persists for a DLL or EXE, it is likely loaded by a system/user session. Continue to Phase 6.

## Phase 6: First Reboot Strategy - SYSTEM Startup Task

Use this when current desktop apps keep reviving the target but the target is not a driver.

Create a SYSTEM startup task that:

1. Removes system registrations.
2. Takes ownership.
3. Kills target processes.
4. Retries deletion multiple times.
5. Deletes itself only if the target directory is gone.
6. Keeps itself for the next startup if deletion failed.

This was necessary in the Xunfei case, but it failed on `iFlyIMEQuickLaunch.dll`, proving a stronger method was needed.

## Phase 7: Second Reboot Strategy - PendingFileRenameOperations

Use this when a startup task runs but deletion fails with access denied on a DLL. This queues deletion for the Windows Session Manager, earlier than normal user apps and scheduled tasks.

Queue every file/directory under the target path:

```powershell
$target = '<install-path>'
$sessionManager = 'HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager'
$existing = @((Get-ItemProperty -LiteralPath $sessionManager -Name PendingFileRenameOperations -ErrorAction SilentlyContinue).PendingFileRenameOperations)
$entries = New-Object System.Collections.Generic.List[string]
foreach ($item in $existing) { if ($item) { [void]$entries.Add($item) } }

$children = Get-ChildItem -LiteralPath $target -Recurse -Force -ErrorAction SilentlyContinue |
  Sort-Object { $_.FullName.Length } -Descending

foreach ($child in $children) {
  [void]$entries.Add('\??\' + $child.FullName)
  [void]$entries.Add('')
}
[void]$entries.Add('\??\' + $target)
[void]$entries.Add('')

New-ItemProperty -LiteralPath $sessionManager `
  -Name PendingFileRenameOperations `
  -Value ([string[]]$entries.ToArray()) `
  -PropertyType MultiString `
  -Force | Out-Null
```

Then reboot again.

## Phase 8: Final Verification

After reboot:

```powershell
winget list --id <Package.Id>
Get-WinUserLanguageList
Get-Process | Where-Object { $_.ProcessName -match '<pattern>' }
Test-Path '<install-path>'
Get-ItemProperty 'HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager' -Name PendingFileRenameOperations -ErrorAction SilentlyContinue
```

If the directory still exists after Phase 7, escalate to Safe Mode or Windows Recovery Environment deletion.

## Backward Proof: Start From Complete Removal

Do not judge success by whether a command ran. Judge success from the final state and work backward.

Final state A: the app is not installable/managed anymore.

- Proof: package manager/control panel no longer lists it.
- Required upstream actions: official uninstaller or uninstall registry cleanup.
- If false: rerun official uninstall, inspect uninstall registry, and do not claim success.

Final state B: Windows no longer offers or loads the integration.

- Proof for IMEs: `Get-WinUserLanguageList` has no target TIP GUID.
- Proof for shell/security tools: no shell extension, browser/homepage hook, service, driver, scheduled task, or startup entry points to the product path.
- Required upstream actions: remove user language entries, HKCU CTF keys, HKLM TSF/COM keys, Run entries, tasks, services, and drivers as applicable.
- If false: file deletion may appear to work but the software can revive or leave broken integration.

Final state C: no related process can revive after a wait.

- Proof: kill target processes, wait 5-15 seconds, inspect parent process if it returns.
- Required upstream actions: remove integration and persistence before deleting files.
- If false: identify parent process. If parent is a proxy/network tool, do not kill it without explicit approval; prefer boot-time deletion.

Final state D: install directory is gone.

- Proof: `Test-Path <install-path>` returns `False`.
- Required upstream actions: remove integration, kill process, take ownership/ACL, delete files.
- If false due to access denied: check if files are loaded; escalate from hot delete to SYSTEM startup task, then to `PendingFileRenameOperations`.

Final state E: no early-boot cleanup debt remains.

- Proof: startup cleanup task deleted itself only after directory removal, and `PendingFileRenameOperations` no longer contains target paths after reboot.
- Required upstream actions: cleanup scripts must log success/failure and must not self-delete unless the target is absent.
- If false: keep retry mechanism or escalate to Safe Mode/Recovery Environment.

Use this backward proof after every sticky removal. Missing any final state means the removal is not complete.

## Security Suite / 360 Escalation

360-like tools can be harder than IMEs because they may include self-protection, services, drivers, browser/homepage protection, file protection, and multiple related products. Use the same model, but be more conservative:

1. Use the vendor uninstaller first and choose the real uninstall path. Some 360 uninstall flows use retention-oriented wording such as continuing protection, leaving reluctantly, or abandoning protection. Read each prompt carefully.
2. Reboot after official uninstall. Public vendor guidance says residual files/folders may be deleted after reboot.
3. If residue remains, do not assume the whole vendor folder is safe to delete. Inventory all 360-related products first.
4. Check services, drivers, scheduled tasks, startup, browser hooks, homepage protection, shell extensions, and install directories.
5. If normal mode cannot delete, use Safe Mode or `PendingFileRenameOperations`.
6. If drivers or kernel protection remain, prefer vendor cleanup tool, Safe Mode, or recovery environment over live force deletion.

## Why Two Reboots May Be Needed

First reboot with a SYSTEM scheduled task is useful when ordinary desktop processes keep the target alive. However, scheduled tasks still run after some Windows components and can lose races with DLL loading.

Second reboot using `PendingFileRenameOperations` is earlier. The Session Manager processes this queue before normal login apps and before most user-mode locks. It is the right escalation when a DLL remains locked after startup-task cleanup.
