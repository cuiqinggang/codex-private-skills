param(
    [string]$PromptPath = "docs/chatgpt-clipboard-bridge-plan-prompt.md",
    [string]$Prompt,
    [string]$TaskId,
    [string]$OutputPath = "output/chatgpt-clipboard-bridge/answer_raw.md",
    [int]$TimeoutSec = 180,
    [int]$CompletionGraceSec = 120,
    [string]$WindowTitlePattern = "ChatGPT",
    [switch]$NoSend,
    [switch]$OpenFreshWindow,
    [string]$FreshWindowUrl = "https://chatgpt.com/",
    [ValidateSet("App", "Window")]
    [string]$FreshWindowMode = "App",
    [int]$FreshWindowWaitSec = 30,
    [switch]$NoRealInput,
    [switch]$AllowRealInput,
    [string]$TracePath
)

$ErrorActionPreference = "Stop"

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes

$script:NoRealInput = ([bool]$NoRealInput -or -not [bool]$AllowRealInput)
$script:TracePath = $TracePath
$script:PreferredWindowHandles = @()

Add-Type @"
using System;
using System.Text;
using System.Runtime.InteropServices;

public static class CodexBridgeWin32 {
  public delegate bool EnumWindowsProc(IntPtr hWnd, IntPtr lParam);
  [DllImport("user32.dll")] public static extern bool EnumWindows(EnumWindowsProc lpEnumFunc, IntPtr lParam);
  [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr hWnd);
  [DllImport("user32.dll", CharSet=CharSet.Unicode)] public static extern int GetWindowText(IntPtr hWnd, StringBuilder text, int count);
  [DllImport("user32.dll", CharSet=CharSet.Unicode)] public static extern int GetClassName(IntPtr hWnd, StringBuilder text, int count);
  [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr hWnd, out uint processId);
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd);
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
  [DllImport("user32.dll")] public static extern bool SetCursorPos(int X, int Y);
  [DllImport("user32.dll")] public static extern void mouse_event(uint dwFlags, uint dx, uint dy, uint dwData, UIntPtr dwExtraInfo);
}
"@

function Write-Step {
    param([string]$Message)
    $line = "[chatgpt-bridge] $Message"
    Write-Host $line
    if ($script:TracePath) {
        $traceDir = Split-Path -Parent $script:TracePath
        if ($traceDir) {
            New-Item -ItemType Directory -Force -Path $traceDir | Out-Null
        }
        Add-Content -LiteralPath $script:TracePath -Value ("{0} {1}" -f (Get-Date -Format "s"), $line) -Encoding UTF8
    }
}

trap {
    Write-Step ("ERROR: {0}" -f $_.Exception.Message)
    exit 1
}

function Assert-RealInputAllowed {
    param([string]$Action)
    if ($script:NoRealInput) {
        throw "Real Windows mouse/keyboard input is disabled; refused action: $Action"
    }
}

function Click-Point {
    param([double]$X, [double]$Y)
    Assert-RealInputAllowed "coordinate mouse click"
    [CodexBridgeWin32]::SetCursorPos([int]$X, [int]$Y) | Out-Null
    Start-Sleep -Milliseconds 120
    [CodexBridgeWin32]::mouse_event(0x0002, 0, 0, 0, [UIntPtr]::Zero)
    [CodexBridgeWin32]::mouse_event(0x0004, 0, 0, 0, [UIntPtr]::Zero)
}

function Send-KeysSafe {
    param([string]$Keys)
    Write-Step "Sending virtual keystrokes: $Keys"
    [System.Windows.Forms.SendKeys]::SendWait($Keys)
}

function Invoke-OrClick {
    param($Button, $Center)

    try {
        $pattern = $Button.GetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern)
        $pattern.Invoke()
        return
    } catch {
        if ($script:NoRealInput) {
            throw "UI Automation InvokePattern failed and coordinate click fallback is disabled: $($_.Exception.Message)"
        }
        Click-Point -X $Center.X -Y $Center.Y
    }
}

function Get-RectCenter {
    param($Element)
    $rect = $Element.Current.BoundingRectangle
    if ($rect.IsEmpty -or $rect.Width -le 0 -or $rect.Height -le 0) {
        return $null
    }
    [pscustomobject]@{
        X = $rect.Left + ($rect.Width / 2)
        Y = $rect.Top + ($rect.Height / 2)
        Bottom = $rect.Bottom
    }
}

function Get-BrowserWindows {
    param([string]$TitlePattern)

    $windows = New-Object System.Collections.Generic.List[object]
    [CodexBridgeWin32]::EnumWindows({
        param($hWnd, $lParam)
        if ([CodexBridgeWin32]::IsWindowVisible($hWnd)) {
            $titleBuilder = New-Object System.Text.StringBuilder 512
            $classBuilder = New-Object System.Text.StringBuilder 256
            [void][CodexBridgeWin32]::GetWindowText($hWnd, $titleBuilder, $titleBuilder.Capacity)
            [void][CodexBridgeWin32]::GetClassName($hWnd, $classBuilder, $classBuilder.Capacity)
            [uint32]$processId = 0
            [void][CodexBridgeWin32]::GetWindowThreadProcessId($hWnd, [ref]$processId)
            $proc = Get-Process -Id $processId -ErrorAction SilentlyContinue
            $title = $titleBuilder.ToString()
            if ($title.Length -gt 0 -and $proc -and $proc.ProcessName -match "^(chrome|msedge)$") {
                if ($TitlePattern -and $title -notmatch $TitlePattern) {
                    return $true
                }
                $windows.Add([pscustomobject]@{
                    Handle = $hWnd
                    HandleId = $hWnd.ToInt64()
                    ProcessName = $proc.ProcessName
                    Title = $title
                    ClassName = $classBuilder.ToString()
                })
            }
        }
        return $true
    }, [IntPtr]::Zero) | Out-Null

    return $windows.ToArray()
}

function Get-BrowserExecutable {
    $paths = @(
        "C:\Program Files\Google\Chrome\Application\chrome.exe",
        "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        "C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    )

    foreach ($path in $paths) {
        if (Test-Path -LiteralPath $path) {
            return $path
        }
    }

    $cmd = Get-Command -Name @("chrome.exe", "msedge.exe") -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($cmd) {
        return $cmd.Source
    }

    throw "Could not find Chrome or Edge executable."
}

function Open-FreshChatGptWindow {
    $before = @(Get-BrowserWindows | ForEach-Object { $_.HandleId })
    $browser = Get-BrowserExecutable

    Write-Step "Opening fresh ChatGPT $FreshWindowMode window: $FreshWindowUrl"
    if ($FreshWindowMode -eq "App") {
        Start-Process -FilePath $browser -ArgumentList @("--app=$FreshWindowUrl") | Out-Null
    } else {
        Start-Process -FilePath $browser -ArgumentList @("--new-window", $FreshWindowUrl) | Out-Null
    }

    $deadline = (Get-Date).AddSeconds($FreshWindowWaitSec)
    do {
        Start-Sleep -Seconds 1
        $fresh = @(Get-BrowserWindows -TitlePattern $WindowTitlePattern |
            Where-Object { $before -notcontains $_.HandleId } |
            Sort-Object ProcessName, Title)

        if ($fresh.Count -gt 0) {
            $script:PreferredWindowHandles = @($fresh | ForEach-Object { $_.HandleId })
            Write-Step "Fresh browser window candidate: $($fresh[0].Title)"
            return
        }
    } while ((Get-Date) -lt $deadline)

    Write-Step "Fresh window was not uniquely identified; falling back to title matching"
}

function Find-ChatGptWindow {
    $windows = @(Get-BrowserWindows -TitlePattern $WindowTitlePattern)
    if ($script:PreferredWindowHandles.Count -gt 0) {
        $preferred = @($windows | Where-Object { $script:PreferredWindowHandles -contains $_.HandleId })
        if ($preferred.Count -gt 0) {
            $windows = $preferred
        }
    }

    $window = $windows |
        Sort-Object { if ($_.Title -match "ChatGPT|Codex") { 0 } else { 1 } }, ProcessName, Title |
        Select-Object -First 1

    if (-not $window) {
        throw "Could not find a Chrome/Edge window matching: $WindowTitlePattern"
    }

    Write-Step "Matched browser window: $($window.Title)"
    [CodexBridgeWin32]::ShowWindow($window.Handle, 9) | Out-Null
    [CodexBridgeWin32]::SetForegroundWindow($window.Handle) | Out-Null
    Start-Sleep -Milliseconds 800

    return [System.Windows.Automation.AutomationElement]::FromHandle($window.Handle)
}

function Find-Textbox {
    param($Root)

    $editCondition = New-Object System.Windows.Automation.PropertyCondition(
        [System.Windows.Automation.AutomationElement]::ControlTypeProperty,
        [System.Windows.Automation.ControlType]::Edit
    )
    $edits = $Root.FindAll([System.Windows.Automation.TreeScope]::Descendants, $editCondition)

    $textboxCandidates = @()
    foreach ($edit in $edits) {
        $name = $edit.Current.Name
        if ($name -match "地址|搜索栏|Address|Search") {
            continue
        }
        if ($name -match "ChatGPT|Message|Ask|发送|聊天|消息|输入") {
            $center = Get-RectCenter $edit
            if ($center) {
                $textboxCandidates += [pscustomobject]@{ Element = $edit; Center = $center; Name = $name }
            }
        }
    }

    return $textboxCandidates | Sort-Object { $_.Center.Bottom } -Descending | Select-Object -First 1
}

function Get-BottomInputFallback {
    param($Root)

    $rect = $Root.Current.BoundingRectangle
    if ($rect.IsEmpty -or $rect.Width -le 0 -or $rect.Height -le 0) {
        return $null
    }

    [pscustomobject]@{
        Name = "bottom-center fallback"
        Center = [pscustomobject]@{
            X = $rect.Left + ($rect.Width / 2)
            Y = $rect.Bottom - 95
            Bottom = $rect.Bottom
        }
    }
}

function Get-CopyButtons {
    param($Root)

    $buttonCondition = New-Object System.Windows.Automation.PropertyCondition(
        [System.Windows.Automation.AutomationElement]::ControlTypeProperty,
        [System.Windows.Automation.ControlType]::Button
    )
    $buttons = $Root.FindAll([System.Windows.Automation.TreeScope]::Descendants, $buttonCondition)

    $copyButtons = @()
    foreach ($button in $buttons) {
        $name = $button.Current.Name
        if ($name -match "复制消息|复制表格") {
            continue
        }
        if ($name -match "^(复制|复制回复|Copy|Copy response)$") {
            $center = Get-RectCenter $button
            if ($center) {
                $copyButtons += [pscustomobject]@{ Element = $button; Center = $center; Name = $name }
            }
        }
    }

    return @($copyButtons | Sort-Object { $_.Center.Bottom })
}

function Reveal-CopyResponseControls {
    param($Root)

    if ($script:NoRealInput) {
        Write-Step "NoRealInput enabled; using virtual End key only"
        Send-KeysSafe "{END}"
        return
    }

    $rect = $Root.Current.BoundingRectangle
    if (-not $rect.IsEmpty -and $rect.Width -gt 0 -and $rect.Height -gt 0) {
        [CodexBridgeWin32]::SetCursorPos(
            [int]($rect.Left + ($rect.Width / 2)),
            [int]($rect.Bottom - 220)
        ) | Out-Null
    }
    Send-KeysSafe "{END}"
}

function Set-TextboxValue {
    param($Element, [string]$Text, [string]$ExpectedMarker)

    function Test-TextboxValueCommitted {
        param($TargetElement, [string]$Marker)
        if (-not $Marker) {
            return $true
        }

        try {
            $currentValuePattern = $TargetElement.GetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern)
            $currentValue = $currentValuePattern.Current.Value
            return ($currentValue -and $currentValue.Contains($Marker))
        } catch {
            Write-Step "Could not verify UI Automation input value: $($_.Exception.Message)"
            return $false
        }
    }

    try {
        $valuePattern = $Element.GetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern)
        if (-not $valuePattern.Current.IsReadOnly) {
            $valuePattern.SetValue($Text)
            Start-Sleep -Milliseconds 200
            if (Test-TextboxValueCommitted -TargetElement $Element -Marker $ExpectedMarker) {
                Write-Step "Prompt inserted with UI Automation ValuePattern"
                return $true
            }
            Write-Step "ValuePattern did not update the actual ChatGPT input value"
        }
    } catch {
        Write-Step "ValuePattern input unavailable: $($_.Exception.Message)"
    }

    try {
        $legacyPattern = $Element.GetCurrentPattern([System.Windows.Automation.LegacyIAccessiblePattern]::Pattern)
        $legacyPattern.SetValue($Text)
        Start-Sleep -Milliseconds 200
        if (Test-TextboxValueCommitted -TargetElement $Element -Marker $ExpectedMarker) {
            Write-Step "Prompt inserted with UI Automation LegacyIAccessiblePattern"
            return $true
        }
        Write-Step "LegacyIAccessiblePattern did not update the actual ChatGPT input value"
    } catch {
        Write-Step "LegacyIAccessible input unavailable: $($_.Exception.Message)"
    }

    return $false
}

function Find-SendButton {
    param($Root)

    $buttonCondition = New-Object System.Windows.Automation.PropertyCondition(
        [System.Windows.Automation.AutomationElement]::ControlTypeProperty,
        [System.Windows.Automation.ControlType]::Button
    )
    $buttons = $Root.FindAll([System.Windows.Automation.TreeScope]::Descendants, $buttonCondition)

    $sendButtons = @()
    foreach ($button in $buttons) {
        if (-not $button.Current.IsEnabled) {
            continue
        }
        $name = $button.Current.Name
        if ($name -match "^(Send|Send message|Send prompt|发送|发送消息|发送提示)$") {
            $center = Get-RectCenter $button
            if ($center) {
                $sendButtons += [pscustomobject]@{ Element = $button; Center = $center; Name = $name }
            }
        }
    }

    return $sendButtons | Sort-Object { $_.Center.Bottom } -Descending | Select-Object -First 1
}

function Wait-For-NewCopyButton {
    param(
        $Root,
        [int]$InitialCount,
        [int]$TimeoutSec,
        [int]$CompletionGraceSec
    )

    $deadline = (Get-Date).AddSeconds($TimeoutSec)
    do {
        Start-Sleep -Seconds 2
        $buttons = @(Get-CopyButtons $Root)
        if ($buttons.Count -gt $InitialCount) {
            return $buttons[-1]
        }
    } while ((Get-Date) -lt $deadline)

    $graceDeadline = (Get-Date).AddSeconds($CompletionGraceSec)
    do {
        Reveal-CopyResponseControls -Root $Root
        Start-Sleep -Seconds 2
        $buttons = @(Get-CopyButtons $Root)
        if ($buttons.Count -gt $InitialCount) {
            return $buttons[-1]
        }
    } while ((Get-Date) -lt $graceDeadline)

    return $null
}

if (-not $Prompt) {
    if (-not (Test-Path -LiteralPath $PromptPath)) {
        throw "Prompt file not found: $PromptPath"
    }
    $resolvedPromptPath = (Resolve-Path -LiteralPath $PromptPath)
    $Prompt = [System.IO.File]::ReadAllText($resolvedPromptPath, [System.Text.Encoding]::UTF8)
}

if (-not $TaskId) {
    $TaskId = "TASK-" + (Get-Date -Format "yyyyMMdd-HHmmss") + "-" + ([guid]::NewGuid().ToString("N").Substring(0, 8))
}

$Prompt = @"
TASK_ID: $TaskId

请在回答中原样包含这一行：TASK_ID: $TaskId

$Prompt
"@

New-Item -ItemType Directory -Force -Path (Split-Path -Parent $OutputPath) | Out-Null

if ($OpenFreshWindow) {
    Open-FreshChatGptWindow
}

Write-Step "Activating ChatGPT browser window"
$root = Find-ChatGptWindow

$initialCopyButtons = @(Get-CopyButtons $root)
Write-Step "Initial copy button count: $($initialCopyButtons.Count)"

$textbox = Find-Textbox $root
if (-not $textbox) {
    if ($script:NoRealInput) {
        throw "NoRealInput enabled and no semantic ChatGPT textbox was found; refusing coordinate fallback."
    }
    Write-Step "Could not find semantic ChatGPT textbox; using bottom-center input fallback"
    $textbox = Get-BottomInputFallback $root
}
if (-not $textbox) {
    throw "Could not find a likely ChatGPT input location."
}

if ($script:NoRealInput) {
    Write-Step "Focusing input textbox with UI Automation only: $($textbox.Name)"
    try {
        $textbox.Element.SetFocus()
    } catch {
        throw "UI Automation focus failed and coordinate click fallback is disabled: $($_.Exception.Message)"
    }
} else {
    Write-Step "Clicking input textbox: $($textbox.Name)"
    Click-Point -X $textbox.Center.X -Y $textbox.Center.Y
    Start-Sleep -Milliseconds 300
}

Set-Clipboard -Value $Prompt
Write-Step "Prompt copied to clipboard"

if ($NoSend) {
    Write-Step "NoSend enabled; stopping before paste/send"
    exit 0
}

if ($script:NoRealInput) {
    Send-KeysSafe "^v"
    Start-Sleep -Milliseconds 300
    Send-KeysSafe "{ENTER}"
} else {
    Send-KeysSafe "^v"
    Start-Sleep -Milliseconds 300
    Send-KeysSafe "{ENTER}"
}
Write-Step "Prompt sent"

Write-Step "Waiting for a new Copy button; this is the completion signal"
$copyButton = Wait-For-NewCopyButton -Root $root -InitialCount $initialCopyButtons.Count -TimeoutSec $TimeoutSec -CompletionGraceSec $CompletionGraceSec
if (-not $copyButton) {
    throw "Timed out waiting for a new Copy/复制 button. The answer is not confirmed complete."
}

Write-Step "Clicking final Copy button: $($copyButton.Name)"
[System.Windows.Forms.Clipboard]::Clear()
Invoke-OrClick -Button $copyButton.Element -Center $copyButton.Center
Start-Sleep -Seconds 1

$answer = Get-Clipboard -Raw
if (-not $answer -or $answer.Trim().Length -lt 20) {
    throw "Clipboard did not contain a valid copied answer after clicking Copy."
}
if (-not $answer.Contains($TaskId)) {
    throw "Copied answer does not contain TASK_ID: $TaskId"
}

Set-Content -Path $OutputPath -Value $answer -Encoding UTF8
Write-Step "Answer saved: $OutputPath"
