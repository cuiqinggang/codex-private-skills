#Requires AutoHotkey v2.0
#SingleInstance Force
#Include %A_ScriptDir%\Lib\UIA.ahk
; B32 tiny UI adapter. Uses upstream AutoHotkey v2 + Descolada/UIA-v2,
; not a scheduler, general lock service, or independent task state machine.
; Default is read-only verification; --commit performs ONE ChatGPT handoff.
if (A_Args.Length < 1) {
    FileAppend "FAIL:NO_PROMPT_FILE`n", "*"
    ExitApp 11
}
promptFile := A_Args[1]
commit := (A_Args.Length >= 2 && A_Args[2] = "--commit")
if !FileExist(promptFile) {
    FileAppend "FAIL:PROMPT_NOT_FOUND`n", "*"
    ExitApp 12
}
prompt := FileRead(promptFile, "UTF-8")
if (StrLen(prompt) < 40 || !InStr(prompt, "TASK_ID=") || !InStr(prompt, "FREEZE_ID=") || !InStr(prompt, "START_HERE.md")) {
    FileAppend "FAIL:UNVERIFIED_ENVELOPE`n", "*"
    ExitApp 13
}
; Never activate arbitrary windows or browsers.
if (WinGetProcessName("A") != "chrome.exe") {
    FileAppend "BLOCKED:ACTIVE_WINDOW_NOT_CHATGPT`n", "*"
    ExitApp 14
}
try {
    root := UIA.ElementFromHandle("A")
    ; The Chrome tab title may omit "ChatGPT"; verify the real origin using
    ; the mature UIA address-bar element instead of comparing window titles.
    trustedAddress := 0
    for addressName in ["地址和搜索栏", "Address and search bar"] {
        try {
            addresses := root.FindElements({Type:"Edit", Name:addressName})
            for addressEl in addresses {
                try {
                    if RegExMatch(addressEl.Value, "i)^(https?://)?chatgpt\.com(/|$)")
                        trustedAddress += 1
                }
            }
        }
    }
    if (trustedAddress != 1) {
        FileAppend "BLOCKED:CHATGPT_ADDRESS_NOT_VERIFIED`n", "*"
        ExitApp 20
    }
    ; Locate by semantic UIA button identity, independent of sidebar width.
    newChat := 0
    for label in ["新聊天", "New chat"] {
        try {
            found := root.FindElements({Type:"Button", Name:label})
            for button in found {
                if (!button.IsOffscreen && button.IsEnabled) {
                    if newChat {
                        FileAppend "BLOCKED:AMBIGUOUS_NEW_CHAT`n", "*"
                        ExitApp 15
                    }
                    newChat := button
                }
            }
        }
    }
    if !newChat {
        FileAppend "BLOCKED:NEW_CHAT_CONTROL_UNVERIFIED`n", "*"
        ExitApp 16
    }
    if !commit {
        FileAppend "DRY_RUN:NEW_CHAT_CONTROL_FOUND_NO_SEND`n", "*"
        ExitApp 0
    }
    if InStr(prompt, "VIRTUAL_TEST_ONLY=YES") {
        FileAppend "BLOCKED:TEST_ENVELOPE_COMMIT_FORBIDDEN`n", "*"
        ExitApp 21
    }
    ; Action 1: frozen, unique NEXT_PAGE_PROMPT already read and validated.
    ; Action 2: click New chat *inside the existing current ChatGPT window*.
    newChat.Click()
    ; No fixed delay: look up a ready composer using mature UIA properties.
    composerEl := 0
    editorLabels := ["向 ChatGPT 提问", "询问 ChatGPT", "询问任何问题", "Message ChatGPT", "Ask anything", "发送消息给 ChatGPT"]
    editorDeadline := A_TickCount + 2000
    while A_TickCount < editorDeadline {
        root := UIA.ElementFromHandle("A")
        editMatches := 0
        for candidate in root.FindElements({Type:"Edit"}) {
            try {
                for label in editorLabels {
                    if (candidate.Name = label && candidate.IsEnabled && !candidate.IsOffscreen) {
                        composerEl := candidate
                        editMatches += 1
                        break
                    }
                }
            }
        }
        if editMatches = 1
            break
        if editMatches > 1 {
            FileAppend "BLOCKED:AMBIGUOUS_NEW_CHAT_COMPOSER_NO_SUBMIT`n", "*"
            ExitApp 27
        }
        Sleep 20
    }
    if !composerEl {
        FileAppend "BLOCKED:NEW_CHAT_COMPOSER_NOT_READY_NO_SUBMIT`n", "*"
        ExitApp 17
    }
    ; Action 3: paste once and submit once. No retry on ambiguous result.
    composerEl.Click()
    savedClipboard := ClipboardAll()
    A_Clipboard := prompt
    if !ClipWait(2) {
        A_Clipboard := savedClipboard
        FileAppend "BLOCKED:CLIPBOARD_ERROR_NO_SUBMIT`n", "*"
        ExitApp 18
    }
    Send "^v"
    ; No fixed delay: send only if the complete prompt is readable in editor.
    pasteReady := false
    pasteDeadline := A_TickCount + 2000
    expectedText := StrReplace(prompt, "`r`n", "`n")
    while A_TickCount < pasteDeadline {
        observedText := ""
        try observedText := composerEl.Value
        if observedText = "" {
            try observedText := composerEl.TextPattern.DocumentRange.GetText(-1)
        }
        if StrReplace(observedText, "`r`n", "`n") = expectedText {
            pasteReady := true
            break
        }
        Sleep 20
    }
    A_Clipboard := savedClipboard
    if !pasteReady {
        FileAppend "BLOCKED:PASTE_NOT_VERIFIED_NO_SUBMIT`n", "*"
        ExitApp 28
    }
    Send "{Enter}"
    FileAppend "SUBMIT_ATTEMPTED_ONCE:VERIFY_CHAT_RECEIPT_EXTERNALLY`n", "*"
    ExitApp 0
} catch as ex {
    FileAppend "UNKNOWN:" ex.Message "`n", "*"
    ExitApp 19
}
