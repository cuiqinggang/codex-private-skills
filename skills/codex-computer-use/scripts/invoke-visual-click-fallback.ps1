[CmdletBinding()]
param(
  [string]$ProcessName,
  [string]$TitleContains,
  [double]$XRatio = 0.5,
  [double]$YRatio = 0.5,
  [int]$XOffset = 0,
  [int]$YOffset = 0,
  [switch]$Maximize,
  [string]$BeforeScreenshot,
  [string]$AfterScreenshot,
  [string]$WaitForFile,
  [int]$WaitForFileTimeoutMs = 3000
)

$ErrorActionPreference = 'Stop'

Add-Type -AssemblyName System.Drawing
Add-Type @"
using System;
using System.Text;
using System.Runtime.InteropServices;

public class CodexVisualClickWin32 {
  public delegate bool EnumWindowsProc(IntPtr hWnd, IntPtr lParam);

  [DllImport("user32.dll")]
  public static extern bool EnumWindows(EnumWindowsProc lpEnumFunc, IntPtr lParam);

  [DllImport("user32.dll")]
  public static extern bool IsWindowVisible(IntPtr hWnd);

  [DllImport("user32.dll")]
  public static extern int GetWindowText(IntPtr hWnd, StringBuilder lpString, int nMaxCount);

  [DllImport("user32.dll")]
  public static extern uint GetWindowThreadProcessId(IntPtr hWnd, out uint processId);

  [DllImport("user32.dll")]
  public static extern bool GetWindowRect(IntPtr hWnd, out RECT lpRect);

  [DllImport("user32.dll")]
  public static extern bool SetForegroundWindow(IntPtr hWnd);

  [DllImport("user32.dll")]
  public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);

  [DllImport("user32.dll")]
  public static extern bool SetCursorPos(int X, int Y);

  [DllImport("user32.dll")]
  public static extern void mouse_event(uint dwFlags, uint dx, uint dy, uint dwData, UIntPtr dwExtraInfo);

  [DllImport("user32.dll", SetLastError=true)]
  public static extern uint SendInput(uint nInputs, INPUT[] pInputs, int cbSize);

  [StructLayout(LayoutKind.Sequential)]
  public struct INPUT {
    public uint type;
    public MOUSEINPUT mi;
  }

  [StructLayout(LayoutKind.Sequential)]
  public struct MOUSEINPUT {
    public int dx;
    public int dy;
    public uint mouseData;
    public uint dwFlags;
    public uint time;
    public UIntPtr dwExtraInfo;
  }

  public struct RECT {
    public int Left;
    public int Top;
    public int Right;
    public int Bottom;
  }
}
"@

function Get-TargetWindow {
  $matches = New-Object System.Collections.Generic.List[object]
  [CodexVisualClickWin32]::EnumWindows({
    param($hWnd, $lParam)

    if (-not [CodexVisualClickWin32]::IsWindowVisible($hWnd)) {
      return $true
    }

    $pidValue = 0
    [void][CodexVisualClickWin32]::GetWindowThreadProcessId($hWnd, [ref]$pidValue)
    $process = Get-Process -Id $pidValue -ErrorAction SilentlyContinue
    if (-not $process) {
      return $true
    }

    if ($ProcessName -and $process.ProcessName -ne $ProcessName) {
      return $true
    }

    $titleBuilder = New-Object System.Text.StringBuilder 1024
    [void][CodexVisualClickWin32]::GetWindowText($hWnd, $titleBuilder, $titleBuilder.Capacity)
    $title = $titleBuilder.ToString()
    if ($TitleContains -and $title -notlike "*$TitleContains*") {
      return $true
    }

    $rect = New-Object CodexVisualClickWin32+RECT
    [void][CodexVisualClickWin32]::GetWindowRect($hWnd, [ref]$rect)
    $width = $rect.Right - $rect.Left
    $height = $rect.Bottom - $rect.Top
    if ($width -le 0 -or $height -le 0) {
      return $true
    }

    $matches.Add([pscustomobject]@{
      Handle = $hWnd
      ProcessId = $process.Id
      ProcessName = $process.ProcessName
      Title = $title
      Left = $rect.Left
      Top = $rect.Top
      Right = $rect.Right
      Bottom = $rect.Bottom
      Width = $width
      Height = $height
    }) | Out-Null
    return $true
  }, [IntPtr]::Zero) | Out-Null

  $matches | Sort-Object Width, Height -Descending | Select-Object -First 1
}

function Save-WindowScreenshot {
  param(
    [Parameter(Mandatory = $true)]$Window,
    [Parameter(Mandatory = $true)][string]$Path
  )

  New-Item -ItemType Directory -Force -Path (Split-Path -Parent $Path) | Out-Null
  $bitmap = New-Object System.Drawing.Bitmap $Window.Width, $Window.Height
  $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
  try {
    $graphics.CopyFromScreen($Window.Left, $Window.Top, 0, 0, $bitmap.Size)
    $bitmap.Save($Path, [System.Drawing.Imaging.ImageFormat]::Png)
  } finally {
    $graphics.Dispose()
    $bitmap.Dispose()
  }
}

if ($XRatio -lt 0 -or $XRatio -gt 1 -or $YRatio -lt 0 -or $YRatio -gt 1) {
  throw 'XRatio and YRatio must be between 0 and 1'
}

$window = Get-TargetWindow
if (-not $window) {
  throw "No visible target window matched ProcessName='$ProcessName' TitleContains='$TitleContains'"
}

if ($Maximize) {
  [void][CodexVisualClickWin32]::ShowWindow($window.Handle, 3)
  Start-Sleep -Milliseconds 500
  $window = Get-TargetWindow
}

[void][CodexVisualClickWin32]::SetForegroundWindow($window.Handle)
Start-Sleep -Milliseconds 250

if ($BeforeScreenshot) {
  Save-WindowScreenshot -Window $window -Path $BeforeScreenshot
}

$x = [int][Math]::Round($window.Left + ($window.Width * $XRatio) + $XOffset)
$y = [int][Math]::Round($window.Top + ($window.Height * $YRatio) + $YOffset)

[void][CodexVisualClickWin32]::SetCursorPos($x, $y)
Start-Sleep -Milliseconds 100
$inputs = New-Object 'CodexVisualClickWin32+INPUT[]' 2
$inputs[0].type = 0
$inputs[0].mi.dwFlags = 0x0002
$inputs[1].type = 0
$inputs[1].mi.dwFlags = 0x0004
$sent = [CodexVisualClickWin32]::SendInput(2, $inputs, [Runtime.InteropServices.Marshal]::SizeOf([type]'CodexVisualClickWin32+INPUT'))
if ($sent -ne 2) {
  [CodexVisualClickWin32]::mouse_event(0x0002, 0, 0, 0, [UIntPtr]::Zero)
  Start-Sleep -Milliseconds 80
  [CodexVisualClickWin32]::mouse_event(0x0004, 0, 0, 0, [UIntPtr]::Zero)
}
Start-Sleep -Milliseconds 300

if ($AfterScreenshot) {
  $afterWindow = Get-TargetWindow
  if ($afterWindow) {
    Save-WindowScreenshot -Window $afterWindow -Path $AfterScreenshot
  }
}

$fileResult = $null
if ($WaitForFile) {
  $deadline = [DateTime]::UtcNow.AddMilliseconds($WaitForFileTimeoutMs)
  while ([DateTime]::UtcNow -lt $deadline -and -not (Test-Path -LiteralPath $WaitForFile -PathType Leaf)) {
    Start-Sleep -Milliseconds 100
  }
  if (Test-Path -LiteralPath $WaitForFile -PathType Leaf) {
    $fileResult = Get-Content -LiteralPath $WaitForFile -Raw
  }
}

[pscustomobject]@{
  ok = if ($WaitForFile) { [bool]$fileResult } else { $true }
  processName = $window.ProcessName
  processId = $window.ProcessId
  title = $window.Title
  rect = [pscustomobject]@{
    left = $window.Left
    top = $window.Top
    right = $window.Right
    bottom = $window.Bottom
    width = $window.Width
    height = $window.Height
  }
  click = [pscustomobject]@{
    x = $x
    y = $y
    xRatio = $XRatio
    yRatio = $YRatio
    xOffset = $XOffset
    yOffset = $YOffset
  }
  beforeScreenshot = $BeforeScreenshot
  afterScreenshot = $AfterScreenshot
  waitForFile = $WaitForFile
  fileResult = if ($fileResult) { $fileResult.Trim() } else { $null }
} | ConvertTo-Json -Depth 5
