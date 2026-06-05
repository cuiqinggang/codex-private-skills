Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

Add-Type @'
using System;
using System.Runtime.InteropServices;
public class CodexWin32Input {
  [DllImport("user32.dll")] public static extern bool SetCursorPos(int X, int Y);
  [DllImport("user32.dll")] public static extern void mouse_event(uint dwFlags, uint dx, uint dy, uint dwData, UIntPtr dwExtraInfo);
}
'@

$ErrorActionPreference = "Stop"

$form = New-Object System.Windows.Forms.Form
$form.Text = "Codex Desktop Control Test"
$form.Width = 720
$form.Height = 360
$form.StartPosition = "Manual"
$form.Location = New-Object System.Drawing.Point(120, 120)
$form.TopMost = $true

$label = New-Object System.Windows.Forms.Label
$label.Text = "Temporary desktop-control test window"
$label.Dock = "Top"
$label.Height = 32
$label.TextAlign = "MiddleLeft"
$label.Padding = New-Object System.Windows.Forms.Padding(10, 0, 0, 0)

$textBox = New-Object System.Windows.Forms.TextBox
$textBox.Multiline = $true
$textBox.Dock = "Fill"
$textBox.Font = New-Object System.Drawing.Font("Consolas", 16)
$textBox.ScrollBars = "Vertical"

$form.Controls.Add($textBox)
$form.Controls.Add($label)

$timer = New-Object System.Windows.Forms.Timer
$timer.Interval = 600
$script:step = 0

$timer.Add_Tick({
    if ($script:step -eq 0) {
        $form.Activate()
        $textBox.Focus()
        $center = $textBox.PointToScreen(
            (New-Object System.Drawing.Point(
                ([int]($textBox.Width / 2)),
                ([int]($textBox.Height / 2))
            ))
        )
        [CodexWin32Input]::SetCursorPos($center.X, $center.Y) | Out-Null
        [CodexWin32Input]::mouse_event(0x0002, 0, 0, 0, [UIntPtr]::Zero)
        [CodexWin32Input]::mouse_event(0x0004, 0, 0, 0, [UIntPtr]::Zero)
        Set-Clipboard -Value "Codex desktop control test`r`nmouse click OK; keyboard paste OK"
        [System.Windows.Forms.SendKeys]::SendWait("^v")
        $script:step = 1
        $timer.Interval = 12000
        return
    }

    if ($script:step -eq 1) {
        $timer.Stop()
        $form.Close()
    }
})

$form.Add_Shown({
    $timer.Start()
})

[System.Windows.Forms.Application]::Run($form)
