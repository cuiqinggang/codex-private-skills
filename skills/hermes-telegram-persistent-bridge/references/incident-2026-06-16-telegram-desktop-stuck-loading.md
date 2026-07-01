# 2026-06-16 Telegram Desktop Stuck Loading Repair

## Value Judgment

HIGH_VALUE.

This incident should be reused because it prevents repeated long debugging when
the Hermes Telegram bridge is healthy but Telegram Desktop itself is stuck on
the loading or connecting screen. It also records a user rule: do not alter the
Windows or FlClash proxy configuration while repairing this class of problem.

## Trigger Phrases

Use this note when the user says:

- Telegram Desktop is stuck on "loading", "connecting", or a green welcome/chat
  background.
- Telegram was closed fully and then reopened, but it will not load chats.
- Hermes Telegram bot still works or diagnostics pass, but the desktop client
  UI is stuck.
- The user asks to reinstall Telegram Desktop while preserving useful state.

## Critical Boundary

Do not change Windows proxy, FlClash proxy settings, FlClash node selection,
FlClash rules, or the Telegram Desktop proxy setting unless the user explicitly
asks for that exact action.

On this machine, the known good proxy is:

```text
127.0.0.1:7890
```

Changing proxy state can break Hermes, Telegram Bot API checks, browser access,
and other user workflows. Prefer read-only proxy checks:

```powershell
Get-ItemProperty 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Internet Settings' |
  Select-Object ProxyEnable,ProxyServer,AutoConfigURL
Invoke-WebRequest -Uri 'https://api.telegram.org' -Proxy 'http://127.0.0.1:7890' -UseBasicParsing -TimeoutSec 15
```

## Diagnosis Pattern

First separate two different systems:

1. Hermes Telegram bridge:
   `C:\Users\A\.codex\skills\hermes-telegram-persistent-bridge\scripts\check-hermes-telegram.ps1`
2. Telegram Desktop client:
   `%APPDATA%\Telegram Desktop\Telegram.exe` and `%APPDATA%\Telegram Desktop\tdata`

If the Hermes diagnostic passes, do not keep restarting Hermes to fix a stuck
Telegram Desktop UI. In this incident Hermes stayed PASS while Telegram Desktop
was stuck.

Evidence that points to Telegram Desktop local client state:

- Telegram process exists and responds, but only connects to `127.0.0.1:7890`.
- Telegram log stops after reading MTP data/config and never reaches normal sync.
- Fresh or old local state shows `Update Info: MTP is unavailable`.
- Telegram Web and Bot API work through the same proxy.
- Hermes receives inbound messages and logs `response ready`.

Useful read-only commands:

```powershell
Get-CimInstance Win32_Process -Filter "Name='Telegram.exe'" |
  Select-Object ProcessId,ExecutablePath,CommandLine

$p = Get-Process Telegram -ErrorAction SilentlyContinue | Select-Object -First 1
if ($p) {
  Get-NetTCPConnection -OwningProcess $p.Id -ErrorAction SilentlyContinue |
    Select-Object LocalAddress,LocalPort,RemoteAddress,RemotePort,State
}

Get-Content -LiteralPath "$env:APPDATA\Telegram Desktop\log.txt" -Tail 120 |
  Select-String -Pattern 'MTP|mtp|Update Info|connection|Connection|proxy|Proxy|network|Network|error|Error|DC'
```

## Failed or Low-Value Paths From This Incident

These consumed time and should not be the default next time:

- Repeated Hermes restarts after the Hermes diagnostic already passes.
- Treating Open WebUI 3000 as required for Telegram Desktop loading.
- Removing or changing Telegram Desktop `settingss` without a very specific
  reason; it may contain client settings such as proxy state.
- Broad FlClash restarts or proxy configuration experiments.
- Assuming a process path is correct without checking `ExecutablePath`.

## Recommended Repair Ladder

### G01 - Prove Hermes Bridge Health

Run:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\A\.codex\skills\hermes-telegram-persistent-bridge\scripts\check-hermes-telegram.ps1"
```

Continue only if Hermes passes. If Hermes fails, use
`windows-native-014-telegram-runbook.md` first.

### G02 - Prove Telegram Network Through Existing Proxy

Do not modify proxy settings. Only verify:

```powershell
Invoke-WebRequest -Uri 'https://api.telegram.org' -Proxy 'http://127.0.0.1:7890' -UseBasicParsing -TimeoutSec 15
Invoke-WebRequest -Uri 'https://web.telegram.org/k/' -Proxy 'http://127.0.0.1:7890' -UseBasicParsing -TimeoutSec 20
```

If these pass, the proxy path is good enough for Telegram services.

### G03 - Confirm the Running Telegram Executable

This was the key trap in the 2026-06-16 repair. A backup copy of
`Telegram.exe` was accidentally launched, making the operator think the new
installation was still broken.

Run:

```powershell
Get-CimInstance Win32_Process -Filter "Name='Telegram.exe'" |
  Select-Object ProcessId,ExecutablePath,CommandLine
```

The normal new installation path should be:

```text
C:\Users\A\AppData\Roaming\Telegram Desktop\Telegram.exe
```

If a process is running from a backup directory such as
`work\telegram-desktop-full-old-state-*`, close that old process and launch the
new path explicitly.

### G04 - Conservative Local Client Cleanup

Only after G01-G03. Back up before moving anything.

Safe to move out temporarily:

- `tdata\working`
- `tdata\temp`
- `tdata\dumps`
- old `log.txt` / `log_start*.txt`

Do not move `settingss` by default. Do not move `key_datas` unless intentionally
forcing a re-login.

### G05 - Official Reinstall With Rollback

If the client still sticks, use a clean reinstall while preserving rollback:

1. Download the official installer from `https://telegram.org/dl/desktop/win64`.
2. Validate:
   - file starts with `MZ`
   - size is reasonable
   - Authenticode signature is valid
   - signer is `Telegram FZ-LLC`
3. Stop Telegram.
4. Move the old full directory, do not delete it:

```text
%APPDATA%\Telegram Desktop
```

to a timestamped backup under the active workspace, for example:

```text
work\telegram-desktop-full-old-state-YYYYMMDD-HHMMSS
```

5. Run the official installer.
6. Start the new path:

```text
C:\Users\A\AppData\Roaming\Telegram Desktop\Telegram.exe
```

7. Ask the user to log in from the phone.

Phone QR path:

```text
Telegram mobile -> Settings -> Devices -> Link Desktop Device
```

### G06 - Shortcut and Acceptance Checks

After login, verify shortcuts point to the new installation path:

```powershell
$paths=@(
  "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Telegram Desktop\Telegram.lnk",
  "$env:USERPROFILE\Desktop\Telegram.lnk"
)
$shell=New-Object -ComObject WScript.Shell
foreach($p in $paths){
  if(Test-Path -LiteralPath $p){
    $s=$shell.CreateShortcut($p)
    [pscustomobject]@{shortcut=$p; target=$s.TargetPath; working_dir=$s.WorkingDirectory}
  }
}
```

Acceptance criteria:

- Only the new path is running.
- Desktop and Start Menu shortcuts target the new path.
- User can see chats in Telegram Desktop.
- Hermes diagnostic returns PASS.
- Sending "hello" or "你好" to the Hermes bot produces `inbound message` and
  `response ready` in `C:\Users\A\.hermes\logs\gateway.log`.

## 2026-06-16 Acceptance Evidence

Final confirmed state:

- Running process:
  `C:\Users\A\AppData\Roaming\Telegram Desktop\Telegram.exe`
- Desktop and Start Menu shortcuts:
  `C:\Users\A\AppData\Roaming\Telegram Desktop\Telegram.exe`
- Hermes diagnostic:
  PASS
- Hermes log:
  inbound Telegram message and `response ready` were observed.
- Old state backup:
  `C:\Users\A\Documents\Codex\2026-06-16\telegram-telegram-telegram-telegram\work\telegram-desktop-full-old-state-20260616-182644`

## Next-Run Reuse Instruction

When this symptom appears again, do not start with proxy changes. Start by
running the Hermes diagnostic, then check the Telegram process path. If Hermes
passes and Telegram Desktop is stuck, go directly to this client-state ladder.
