param(
  [Parameter(Mandatory=$true)]
  [string]$TargetPath,

  [string]$RunOnceCleanupCommand
)

$ErrorActionPreference = 'Stop'

if (-not (Test-Path -LiteralPath $TargetPath)) {
  Write-Output "Target missing already: $TargetPath"
  exit 0
}

$sessionManager = 'HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager'
$existing = @()
try {
  $value = (Get-ItemProperty -LiteralPath $sessionManager -Name PendingFileRenameOperations -ErrorAction SilentlyContinue).PendingFileRenameOperations
  if ($value) { $existing = @($value) }
} catch {
  $existing = @()
}

$entries = New-Object System.Collections.Generic.List[string]
foreach ($item in $existing) {
  if ($null -ne $item) { [void]$entries.Add($item) }
}

$children = Get-ChildItem -LiteralPath $TargetPath -Recurse -Force -ErrorAction SilentlyContinue |
  Sort-Object { $_.FullName.Length } -Descending

foreach ($child in $children) {
  [void]$entries.Add('\??\' + $child.FullName)
  [void]$entries.Add('')
}

[void]$entries.Add('\??\' + $TargetPath)
[void]$entries.Add('')

New-ItemProperty -LiteralPath $sessionManager `
  -Name PendingFileRenameOperations `
  -Value ([string[]]$entries.ToArray()) `
  -PropertyType MultiString `
  -Force | Out-Null

if ($RunOnceCleanupCommand) {
  New-ItemProperty -Path 'HKLM:\Software\Microsoft\Windows\CurrentVersion\RunOnce' `
    -Name ('Cleanup_' + [IO.Path]::GetFileName($TargetPath)) `
    -Value $RunOnceCleanupCommand `
    -PropertyType String `
    -Force | Out-Null
}

Write-Output "Scheduled $($children.Count) children plus target for deletion on next boot."
