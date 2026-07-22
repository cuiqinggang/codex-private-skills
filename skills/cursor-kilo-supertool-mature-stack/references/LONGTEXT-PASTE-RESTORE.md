# Cursor/Kilo Long Text Paste Restore

## Canonical Rule

Use the existing mature skill first:

```text
${REDACTED_SECRET}
```

For Codex Desktop long text, the proven mature route is **file clipboard** mode.

For the Kilo chat input inside Cursor, 2026-07-04 end-to-end UI testing showed
that `.txt` file-drop clipboard content is not accepted as a usable chat paste.
Kilo must keep the original text clipboard and use normal `Ctrl+V`.

## Correct Runtime

Start the original mature converter for Codex only:

```powershell
${REDACTED_SECRET}
```

Expected process:

```text
auto-longtext-fileclip.ps1 -MinChars 2000 -TargetMode Codex
```

Expected behavior:

- Short text remains normal text.
- Long text over 2000 chars is written to:

```text
${REDACTED_SECRET}
```

- When Codex Desktop is foreground, the clipboard becomes a file-drop clipboard
  pointing at that `.txt` file.
- When Kilo/Cursor is foreground, the clipboard remains normal text so the Kilo
  chat input can receive the long content directly.

## 2026-07-04 Correction

A mistaken experimental route converted long text into:

```text
@.kilo-longtext/...
@kilo-longtext/...
```

That was not the original proven skill route and produced confusing UI behavior
such as `No files or folders found`. Do not use that route as the acceptance
standard.

The corrected route restores Codex Desktop file-clip behavior but excludes Kilo
chat input from file-drop conversion:

```text
CODEX_LONGTEXT_FILECLIP_PASS
KILO_CHAT_LONGTEXT_RAW_CTRLV_PASS
```

## Verification Standard

Do not claim PASS from configuration alone. Run at least three paste tests.

For Codex Desktop file-clip tests:

1. Generate a unique long text with a unique marker.
2. Put it on the clipboard.
3. Put Cursor/Kilo in the foreground.
4. Wait for the converter.
5. Confirm:

```text
Clipboard.ContainsFileDropList() = True
file exists
file content contains the unique marker for this round
```

If a round fails, check foreground focus and the log:

```text
${REDACTED_SECRET}
```

For Kilo chat input tests:

1. Put Kilo/Cursor in the foreground.
2. Copy or set a unique long text while Kilo is foreground or before switching
   to Kilo from a non-Codex source app such as PowerPoint.
3. Confirm the clipboard type remains `Text`, not `FileDropList`.
4. Press `Ctrl+V` in the Kilo chat input.
5. Confirm with a screenshot that the long text appears in the input.
6. Send one controlled marker test and confirm Kilo replies with the marker.

## 2026-07-04 Evidence

Backend file-clip passes from the earlier attempted route:

- Round 1: `codex-pasted-text-20260704-194932-05f0026c.txt`, marker matched.
- Round 2: `codex-pasted-text-20260704-194953-538db995.txt`, marker matched.
- Extra Round 3: `codex-pasted-text-20260704-195254-13db64f6.txt`, marker matched.

Evidence files:

```text
${REDACTED_SECRET}
${REDACTED_SECRET}
```

These are now classified as **Codex/file-clip backend evidence only**, not Kilo
chat input acceptance.

Actual Kilo UI end-to-end evidence:

- FileDropList route failed in the real Kilo input: `10-after-long-filedrop-ui-paste.png`
  and `11-kilo-state-after-long-filedrop-bring-front.png` show the Kilo input
  stayed empty even though the generated file contained the marker.
- Raw text route passed: `12-after-raw-longtext-ui-paste.png` shows 26,567
  characters pasted into Kilo.
- Send/readback passed: `15-response-after-25s.png` shows Kilo replied with
  `KILO_E2E_RAW_LONGTEXT_UI_20260704_ac0710a383954bc1b38af53fe12c1328`.
- Fixed runtime passed with converter running Codex-only: `17-kilo-foreground-text-paste.png`
  shows Kilo accepted 14,258 characters while clipboard type stayed `Text`.

Evidence directory:

```text
${REDACTED_SECRET}
```

## Terminal Ctrl+V

For the bottom Cursor integrated terminal, use the separate mature skill:

```text
${REDACTED_SECRET}
```

It ensures `Cursor\User\keybindings.json` contains terminal-scoped paste
bindings for `ctrl+v` and `shift+insert`.
