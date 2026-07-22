param(
    [string[]]$NamePattern = @('AI','Codex','Knowledge','CodeGraph','Hermes','sync','watchdog','LongText','Quota'),
    [switch]$IncludeProcesses
)

$pattern = ($NamePattern | ForEach-Object { [regex]::Escape($_) }) -join '|'
$rows = New-Object System.Collections.Generic.List[object]

Get-ScheduledTask |
    Where-Object {
        $_.TaskPath -eq '\' -and
        ($_.TaskName -match $pattern -or ($_.Actions | Where-Object { $_.Execute -match 'powershell|cmd|wscript|cscript' }))
    } |
    ForEach-Object {
        $task = $_
        foreach ($action in $task.Actions) {
            $args = [string]$action.Arguments
            $rows.Add([pscustomobject]@{
                Source = 'ScheduledTask'
                Name = $task.TaskName
                State = [string]$task.State
                Execute = [string]$action.Execute
                Arguments = $args
                SilentLikely = ($args -match '(?i)-WindowStyle\s+Hidden' -or [string]$action.Execute -match '(?i)wscript|cscript')
            })
        }
    }

$startupPaths = @(
    [Environment]::GetFolderPath('Startup'),
    "$env:ProgramData\Microsoft\Windows\Start Menu\Programs\Startup"
)
$shell = New-Object -ComObject WScript.Shell
foreach ($path in $startupPaths) {
    if (-not (Test-Path -LiteralPath $path)) { continue }
    Get-ChildItem -LiteralPath $path -Force | ForEach-Object {
        if ($_.Extension -eq '.lnk') {
            $shortcut = $shell.CreateShortcut($_.FullName)
            $target = [string]$shortcut.TargetPath
            $args = [string]$shortcut.Arguments
            $rows.Add([pscustomobject]@{
                Source = 'Startup'
                Name = $_.Name
                State = ''
                Execute = $target
                Arguments = $args
                SilentLikely = ($shortcut.WindowStyle -eq 7 -or $target -match '(?i)\.vbs$|wscript|cscript')
            })
        } else {
            $target = $_.FullName
            $rows.Add([pscustomobject]@{
                Source = 'Startup'
                Name = $_.Name
                State = ''
                Execute = $target
                Arguments = ''
                SilentLikely = ($target -match '(?i)\.vbs$')
            })
        }
    }
}

if ($IncludeProcesses) {
    Get-CimInstance Win32_Process |
        Where-Object { $_.Name -in @('powershell.exe','pwsh.exe','cmd.exe','conhost.exe','wscript.exe','cscript.exe') } |
        ForEach-Object {
            $rows.Add([pscustomobject]@{
                Source = 'Process'
                Name = "$($_.Name)#$($_.ProcessId)"
                State = "parent=$($_.ParentProcessId)"
                Execute = $_.Name
                Arguments = [string]$_.CommandLine
                SilentLikely = ($_.CommandLine -match '(?i)-WindowStyle\s+Hidden|wscript|cscript')
            })
        }
}

$rows | Sort-Object SilentLikely, Source, Name | Format-Table -AutoSize
