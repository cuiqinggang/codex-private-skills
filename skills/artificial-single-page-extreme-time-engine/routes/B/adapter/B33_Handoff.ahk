#Requires AutoHotkey v2.0
#SingleInstance Force
#Include %A_ScriptDir%\Lib\UIA.ahk

; Limit UIA search to the document belonging to the selected Chrome tab.
; Background tabs can expose enabled controls: IsOffscreen alone is insufficient.
SelectedChatDocument(root) {
    selectedName := ""
    selectedCount := 0
    for tab in root.FindElements({Type:"TabItem"}) {
        try {
            if tab.SelectionItemPattern.IsSelected {
                selectedName := tab.Name
                selectedCount += 1
            }
        }
    }
    if selectedCount != 1
        return 0
    candidateDoc := 0
    docCount := 0
    for doc in root.FindElements({Type:"Document"}) {
        try {
            title := doc.Name
            if title != "" && InStr(selectedName, title) = 1 {
                candidateDoc := doc
                docCount += 1
            }
        }
    }
    return docCount = 1 ? candidateDoc : 0
}
; B32 tiny UI adapter. Uses upstream AutoHotkey v2 + Descolada/UIA-v2,
; not a scheduler, general lock service, or independent task state machine.
; Default is read-only verification; --commit performs ONE ChatGPT handoff.
if (A_Args.Length < 1) {
    FileAppend "FAIL:NO_PROMPT_FILE`n", "*"
    ExitApp 11
}
promptFile := A_Args[1]
commit := (A_Args.Length >= 2 && A_Args[2] = "--commit")
stage := "INPUT_VALIDATION"
if !FileExist(promptFile) {
    FileAppend "FAIL:PROMPT_NOT_FOUND`n", "*"
    ExitApp 12
}
prompt := Trim(FileRead(promptFile, "UTF-8"), "`r`n")
; B33: send only a short code. Full task text stays in the existing GitHub Freeze.
parts := StrSplit(prompt, "|")
if (parts.Length != 4 || parts[1] != Chr(0x7EED) Chr(0x63A5) "B"
    || parts[2] != "cuiqinggang/codex-private-skills"
    || !RegExMatch(parts[3], "^[A-Za-z0-9_-]+$")
    || !RegExMatch(parts[4], "^[A-Za-z0-9_-]+$")) {
    FileAppend "FAIL:INVALID_STATE_CODE`n", "*"
    ExitApp 13
}
; Never activate arbitrary windows or browsers.
targetHwnd := WinExist("A")
if (!targetHwnd || WinGetProcessName("ahk_id " targetHwnd) != "chrome.exe") {
    FileAppend "BLOCKED:ACTIVE_WINDOW_NOT_CHATGPT`n", "*"
    ExitApp 14
}
try {
    stage := "CHATGPT_IDENTITY"
    root := UIA.ElementFromHandle(targetHwnd)
    ; The Chrome tab title may omit "ChatGPT"; verify the real origin using
    ; the mature UIA address-bar element instead of comparing window titles.
    trustedAddress := 0
    oldChatUrl := ""
    for addressName in ["地址和搜索栏", "Address and search bar"] {
        try {
            addresses := root.FindElements({Type:"Edit", Name:addressName})
            for addressEl in addresses {
                try {
                    if RegExMatch(addressEl.Value, "i)^(https?://)?chatgpt\.com(/|$)") {
                        trustedAddress += 1
                        oldChatUrl := addressEl.Value
                    }
                }
            }
        }
    }
    if (trustedAddress != 1) {
        FileAppend "BLOCKED:CHATGPT_ADDRESS_NOT_VERIFIED`n", "*"
        ExitApp 20
    }
    ; Resolve only the currently selected ChatGPT document, not background tabs.
    activeDoc := SelectedChatDocument(root)
    if !activeDoc {
        FileAppend "BLOCKED:ACTIVE_CHAT_DOCUMENT_UNVERIFIED`n", "*"
        ExitApp 29
    }
    ; Locate by semantic UIA button identity, independent of sidebar width.
    newChat := 0
    for label in ["新聊天", "New chat"] {
        try {
            found := activeDoc.FindElements({Type:"Button", Name:label})
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
    if !WinActive("ahk_id " targetHwnd) {
        FileAppend "BLOCKED:FOCUS_CHANGED_BEFORE_CLICK`n", "*"
        ExitApp 30
    }
    stage := "NEW_CHAT_CLICK"
    newChat.Click()
    stage := "WAIT_NEW_CHAT_COMPOSER"
    ; No fixed delay: look up a ready composer using mature UIA properties.
    composerEl := 0
    editorLabels := ["向 ChatGPT 提问", "询问 ChatGPT", "询问任何问题", "Message ChatGPT", "Ask anything", "发送消息给 ChatGPT"]
    editorDeadline := A_TickCount + 2000
    editorReady := false
    while A_TickCount < editorDeadline {
        root := UIA.ElementFromHandle(targetHwnd)
        activeDoc := SelectedChatDocument(root)
        if !activeDoc {
            Sleep 20
            continue
        }
        ; Verify the old conversation is no longer the destination.
        onNewChat := false
        for addressName in ["地址和搜索栏", "Address and search bar"] {
            try {
                bar := root.FindElement({Type:"Edit", Name:addressName})
                if RegExMatch(bar.Value, "i)^(https?://)?chatgpt\.com/?(\?.*)?$")
                    onNewChat := true
            }
        }
        editMatches := 0
        for candidate in activeDoc.FindElements({Type:"Edit"}) {
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
        if editMatches = 1 && onNewChat {
            editorReady := true
            break
        }
        if editMatches > 1 {
            FileAppend "BLOCKED:AMBIGUOUS_NEW_CHAT_COMPOSER_NO_SUBMIT`n", "*"
            ExitApp 27
        }
        Sleep 20
    }
    if !editorReady {
        FileAppend "BLOCKED:NEW_CHAT_COMPOSER_NOT_READY_NO_SUBMIT`n", "*"
        ExitApp 17
    }
    ; Action 3: paste once and submit once. No retry on ambiguous result.
    if !WinActive("ahk_id " targetHwnd) {
        FileAppend "BLOCKED:FOCUS_CHANGED_BEFORE_PASTE`n", "*"
        ExitApp 31
    }
    stage := "FOCUS_NEW_CHAT_COMPOSER"
    composerEl.Click()
    savedClipboard := ClipboardAll()
    A_Clipboard := prompt
    if !ClipWait(2) {
        A_Clipboard := savedClipboard
        FileAppend "BLOCKED:CLIPBOARD_ERROR_NO_SUBMIT`n", "*"
        ExitApp 18
    }
    stage := "PASTE_SHORT_CODE"
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
    if !WinActive("ahk_id " targetHwnd) {
        FileAppend "BLOCKED:FOCUS_CHANGED_BEFORE_SEND`n", "*"
        ExitApp 32
    }
    stage := "SUBMIT_ONCE"
    Send "{Enter}"
    stage := "SUBMIT_ATTEMPT_RECORDED"
    FileAppend "SUBMIT_ATTEMPTED_ONCE:VERIFY_CHAT_RECEIPT_EXTERNALLY`n", "*"
    ExitApp 0
} catch as ex {
    FileAppend "UNKNOWN_STAGE=" stage ";ERROR=" ex.Message "`n", "*"
    ExitApp 19
}
