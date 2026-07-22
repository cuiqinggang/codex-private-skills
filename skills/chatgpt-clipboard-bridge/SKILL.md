---
name: chatgpt-clipboard-bridge
description: "Use when Codex should execute GPT-provided planning through the user's already logged-in ChatGPT website in Windows Chrome via a minimal clipboard bridge: send a planning prompt, wait only for a newly added assistant answer copy button, copy the answer through that official button, save answer_raw.md, structurally extract codex_plan.md without rewriting GPT, then execute automatically unless a Level 3 high-risk action appears. Do not use for API calls, browser-debugging integrations, login handling, OCR/page-body reading, account/payment/security prompts, or bypassing limits."
---

# ChatGPT Clipboard Bridge

## Stage

This is a stage-complete skill package. Use it now, keep testing it, and update it as the workflow matures.

Route note: for ChatGPT web send/copy work, prefer
`chatgpt-screenshot-bridge` first when the current task explicitly allows real
desktop mouse/keyboard input. Use this clipboard bridge as the no-real-pointer
fallback when real input is not allowed, the screenshot bridge is unavailable,
or the screenshot bridge fails preflight.

Included resources:

- `scripts/chatgpt-clipboard-bridge.ps1`: run the Windows ChatGPT website clipboard bridge.
- `scripts/chatgpt-clipboard-bridge-unit-test.ps1`: validate bridge encoding, Copy-response matching, TASK_ID, and prompt reading rules.
- `scripts/chatgpt-clipboard-bridge-discipline-test.ps1`: validate execution-discipline rules are present in the workspace.
- `scripts/validate_plan_format.py`: validate ChatGPT planning answers contain required round fields.
- `references/execution-discipline.md`: durable rules for GPT planning -> Codex execution.
- `references/multi-round-closure.md`: lessons and rules for multi-round closed-loop tests.

## Role

The bridge only carries text:

```text
prompt -> ChatGPT website -> assistant answer copy button -> answer_raw.md
```

ChatGPT plans. Codex executes. The bridge does not judge, rewrite, scrape page text, OCR, handle login, handle payment, or bypass limits.

Default desktop-safety rule for this machine: use the already opened fresh GPT
page when the user provides one; do not open another GPT page unless asked. Use
the original simple Windows bridge flow: copy prompt to clipboard, UI Automation
focus the GPT input, paste/send with virtual keystrokes, wait for a newly added
assistant answer copy button, and invoke that button with UI Automation. Do not
move the real mouse pointer. Coordinate mouse clicks or real pointer movement
require explicit `-AllowRealInput` for that run. Save a concise `-TracePath`
operation log when testing or changing the bridge.

Known 2026-05-09 desktop findings: UI Automation `ValuePattern.SetValue` may
not trigger ChatGPT's web input event. The working no-real-pointer path is to
focus the existing GPT input with UI Automation, then use virtual keystrokes
(`Ctrl+V`, `Enter`) against that focused input. If the semantic GPT input cannot
be found or focused, stop instead of falling back to coordinates.

${REDACTED_SECRET}
`docs/chatgpt-clipboard-bridge-current-flow.md` before re-testing. The
2026-05-09 working window pattern was `任务回显确认|ChatGPT`; the successful
echo evidence is under
${REDACTED_SECRET}
Do not switch to Playwright, a virtual browser, or a fresh GPT page unless the
user asks.

## Execution Discipline

Treat GPT output as execution instructions, not reference text.

- 默认自动执行，只有高风险才停。
- Codex 不改写 GPT: do not rewrite, translate, summarize, optimize, add steps, or delete steps.
- Convert `answer_raw.md` to `codex_plan.md` only by 结构提取.
- `codex_plan.md` must preserve GPT steps 一一对应. Formatting and numbering may change; meaning may not.
- If extracted steps add, remove, or change GPT actions, STOP.
- Enforce 执行范围锁: execute only inside `output/chatgpt-clipboard-bridge/` or an explicitly specified target directory. Otherwise STOP.

Risk levels:

- Level 0: only writes under `output/`, no deletes, no existing-code changes, no unknown commands. Execute automatically.
- Level 1: creates new files, writes logs, modifies temp/test output. Execute automatically and log.
- Level 2: modifies existing code, runs build/test, overwrites files. Execute automatically after backup, diff, and execution log.
- Level 3: deletes files, batch-modifies the project, runs unknown commands such as `curl | bash`, changes system config, operates accounts/secrets/payment/network permissions. STOP and ask the user.

Read `references/execution-discipline.md` when converting GPT output into an executable plan or when a risk decision is unclear.
Read `references/multi-round-closure.md` before running multi-round closed-loop tests.

## Standard Flow

1. Generate or accept a `TASK_ID`.
2. Include `TASK_ID` in the prompt and require ChatGPT to include it in the answer.
3. Read prompt files with explicit UTF-8.
4. Put the prompt into the Windows clipboard.
5. Use the already opened fresh GPT page unless the user asks to open another.
6. Verify the existing page by running `-NoSend` and finding/focusing the ChatGPT input.
7. Use UI Automation focus plus virtual keystrokes to operate controls without moving the real pointer.
8. Paste/set the prompt and send.
9. Wait for a newly added assistant answer copy button.
10. If the button is delayed, use the grace wait to press virtual End in no-real-input mode. Do not read page text.
11. Click/invoke the last assistant answer copy button, preferring UI Automation `InvokePattern`.
12. Read the clipboard.
13. Stop if the answer does not contain `TASK_ID`.
14. Save `answer_raw.md`.
15. Convert `answer_raw.md` into `codex_plan.md` by structure extraction only.
16. Execute the plan according to the risk levels.
17. Save `execution_log.md` and `result.md`.
18. For multi-round loops, save `result_report_to_gpt.md`, send it back through the bridge, and repeat only with a valid next-round plan.

## Required Planning Format

Before executing a ChatGPT planning answer, validate that it contains:

- `TASK_ID`
- `ROUND`
- `## 本轮目标`
- `## Codex 执行步骤`
- `## 测试要求`
- `## 成功判定`
- `## 失败停止条件`
- `END_TASK_ID`

If any field is missing, do not execute. Save the failure, report it to ChatGPT, and request corrected next-round planning.

## Completion Signal

The only ChatGPT answer completion signal is a newly added, clickable assistant answer button named:

- `复制`
- `复制回复`
- `Copy`
- `Copy response`

Do not treat these as completion:

- `复制消息`
- `复制表格`
- `Copy message`
- `Copy table`
- code-block copy buttons
- fixed wait time
- screenshot/OCR/text appearance

Allowed reveal behavior:

- Wait a short grace period after normal timeout.
- Press virtual End to reveal delayed controls in no-real-input mode.
- Continue to require a newly added assistant answer copy button.
- Never fall back to CDP, page-body text, assistant-message text extraction, or OCR.

## Stop Conditions

Stop and report clearly when:

- No ChatGPT Chrome/Edge window is found.
- The active window is not ChatGPT.
- The input box is not found.
- No new assistant answer copy button appears before timeout.
- Clipboard is empty or too short after clicking copy.
- The answer is missing `TASK_ID`.
- Prompt or answer has encoding corruption.
- `-NoRealInput` is enabled and UI Automation cannot update the actual ChatGPT input value or invoke an enabled send/copy button.
- `codex_plan.md` changes GPT meaning instead of preserving steps 一一对应.
- The requested action is Level 3 high risk.
- The page asks for login, captcha, usage limit, risk control, account security, payment, or other human/account action.

## Commands

Run a bridge request from a prompt file:

```powershell
${REDACTED_SECRET}
```

### Windows Chrome title preflight

Do not assume the logged-in ChatGPT Chrome window title contains `ChatGPT`.
On this desktop the verified logged-in GPT window may be titled by the current
conversation, for example:

```text
任务回显确认 - Google Chrome
```

Before declaring that no GPT window exists, enumerate visible Chrome/Edge
top-level titles and use the current conversation title in `WindowTitlePattern`.

```powershell
Add-Type @'
using System;
using System.Text;
using System.Runtime.InteropServices;
public class CodexWinTitleProbe {
  public delegate bool EnumWindowsProc(IntPtr hWnd, IntPtr lParam);
  [DllImport("user32.dll")] public static extern bool EnumWindows(EnumWindowsProc lpEnumFunc, IntPtr lParam);
  [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr hWnd);
  [DllImport("user32.dll", CharSet=CharSet.Unicode)] public static extern int GetWindowText(IntPtr hWnd, StringBuilder text, int count);
  [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr hWnd, out uint processId);
}
'@
$items = New-Object System.Collections.Generic.List[object]
[CodexWinTitleProbe]::EnumWindows({ param($h,$l)
  if ([CodexWinTitleProbe]::IsWindowVisible($h)) {
    $titleBuilder = New-Object System.Text.StringBuilder 512
    [void][CodexWinTitleProbe]::GetWindowText($h, $titleBuilder, $titleBuilder.Capacity)
    [uint32]$processId = 0
    [void][CodexWinTitleProbe]::GetWindowThreadProcessId($h, [ref]$processId)
    $proc = Get-Process -Id $processId -ErrorAction SilentlyContinue
    $title = $titleBuilder.ToString()
    if ($title.Length -gt 0 -and $proc -and $proc.ProcessName -match '^(chrome|msedge)$') {
      $items.Add([pscustomobject]@{ProcessName=$proc.ProcessName; Id=$processId; Title=$title})
    }
  }
  $true
}, [IntPtr]::Zero) | Out-Null
$items | Sort-Object Title | Format-Table -AutoSize -Wrap
```

Verified command shape for this desktop state:

Legacy Windows bridge preflight, no real input:

```powershell
${REDACTED_SECRET}
  -PromptPath .\prompt.md `
  -TaskId '<unique-task-id>' `
  -WindowTitlePattern '任务回显确认|ChatGPT' `
  -OutputPath .\output\chatgpt-clipboard-bridge\answer_raw.md `
  -TimeoutSec 420 `
  -CompletionGraceSec 120
```

Before a real task, `-NoSend` is the low-risk preflight. It must prove the
existing fresh GPT page reaches a ChatGPT input and stop before sending.

Existing-page virtual-input preflight:

```powershell
${REDACTED_SECRET}
  -PromptPath .\prompt.md `
  -TaskId '<unique-task-id>' `
  -WindowTitlePattern '任务回显确认|ChatGPT' `
  -OutputPath .\output\chatgpt-clipboard-bridge\nosend-answer.md `
  -NoRealInput `
  -NoSend
```

If the bridge fails at window discovery, first update `WindowTitlePattern`
from the enumerated Chrome title. Do not stop at the default
`-WindowTitlePattern 'ChatGPT'` failure.

For readiness, run a short echo prompt requiring a unique `TASK_ID`, then
confirm `answer_raw.md` contains that same `TASK_ID`. The successful 2026-05-09
old-flow smoke test saved evidence under
${REDACTED_SECRET}

Run static bridge checks from a workspace that has the bridge script copied locally:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\chatgpt-clipboard-bridge-unit-test.ps1
```

Run execution-discipline checks:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\chatgpt-clipboard-bridge-discipline-test.ps1
```

## Encoding

- Read prompt files with `[System.IO.File]::ReadAllText($path, [System.Text.Encoding]::UTF8)`.
- Save PowerShell scripts containing Chinese UI strings as UTF-8 with BOM for Windows PowerShell 5.
- Save outputs as UTF-8.
- Never rely on `Get-Content -Raw` for Chinese prompt files in Windows PowerShell 5.

## Outputs

For each task, prefer a task folder containing:

- `prompt.md`
- `answer_raw.md`
- `codex_plan.md`
- `execution_log.md`
- `result.md`

Keep the package small. Future updates should strengthen tests and execution discipline before adding capabilities.
