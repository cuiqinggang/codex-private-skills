# Recent Use Log

## 2026-06-30

- Trigger: user clarified that short paste works, but long messages in Kilo/Cursor need to appear as file-style pasted text and were failing.
- Diagnosis: the existing long-text converter and watchdog were running, and Codex Desktop activation logs were fresh. The script only recognized Codex foreground windows, so Cursor/Kilo was outside the activation scope.
- Fix: added `TargetMode`, kept default `Codex`, and started current runtime with `Codex,CursorKilo`. Startup and watchdog launchers now preserve `-TargetMode "Codex,CursorKilo"`.
- Test round 1: long text became a file-drop clipboard in Cursor foreground, but the log target was ambiguous because the Cursor title contained `Codex`.
- Test round 2: after a stricter log-target change, the test failed because title matching was too narrow. This caught a real regression before handoff.
- Test round 3: `CURSOR_KILO_LONGTEXT_FILECLIP_PASS`; short text stayed text, long text became a file-drop clipboard, generated `.txt` existed under `.codex\manual-paste-attachments`, content marker matched, clipboard restored, and log showed `ACTIVATED file clipboard for CursorKilo`.
- Result: `CURSOR_KILO_LONGTEXT_FILECLIP_PASS`.

## 2026-07-04

- Trigger: user reported that copying long text from the left panel and pasting into Kilo/Cursor produced a different-looking `@...txt` value instead of the copied content.
- Diagnosis: the original mature skill was found and reused. The proven 2026-06-30 route was `CURSOR_KILO_LONGTEXT_FILECLIP_PASS`, not the later experimental `@kilo-longtext/...` mention route.
- Mistake corrected: an attempted `@file` mention route caused confusing UI behavior such as `No files or folders found`; this was not accepted as the canonical route.
- Repair: restored `auto-longtext-fileclip.ps1` and `install-auto-longtext-fileclip.ps1` from the mature `bak-kilo-mention-20260630-174250` version, then kept `TargetMode "Codex,CursorKilo"`.
- Hardening: added a small hold-abort guard so a newly copied long text can interrupt an old held file clipboard during rapid repeated tests.
- Verification: three accepted file-clip passes. Round 1 and round 2 from `three-round-original-skill-fileclip-results-v2.json` passed with `ContainsFileDropList=True`, file exists, and unique marker matched. Extra round 3 from `third-pass-extra-fileclip-result.json` also passed.
- Result: `CURSOR_KILO_LONGTEXT_FILECLIP_PASS_RESTORED`.

## 2026-07-04 Kilo UI Correction

- Trigger: user required real Kilo input-box proof, not backend clipboard proof. User copied long text from PPT and Kilo did not paste it correctly.
- Actual UI finding: `FileDropList` generation was correct in the backend, but the real Kilo chat input did not accept the `.txt` file-drop clipboard. Screenshots `10-after-long-filedrop-ui-paste.png` and `11-kilo-state-after-long-filedrop-bring-front.png` showed the input stayed empty.
- Root cause: the converter was allowed to target `CursorKilo`; this changed long text into a `.txt` file-drop clipboard, which is useful for Codex Desktop but wrong for Kilo chat.
- Repair: restarted the converter with `-TargetMode Codex` only. Kilo/Cursor is no longer intercepted, so copied PPT/browser text remains normal text for raw `Ctrl+V`.
- Accepted Kilo evidence:
  - Short paste focus proof: `09-after-short-actual-kilo-input-paste.png`.
  - Raw long paste proof: `12-after-raw-longtext-ui-paste.png`, 26,567 chars visible in Kilo input.
  - Send/readback proof: `15-response-after-25s.png`, Kilo replied with marker `KILO_E2E_RAW_LONGTEXT_UI_20260704_ac0710a383954bc1b38af53fe12c1328`.
  - Final fixed-runtime proof: `17-kilo-foreground-text-paste.png`, converter running `TargetMode Codex`, clipboard type stayed `Text`, 14,258 chars pasted into Kilo.
${REDACTED_SECRET}
- Result: `KILO_CHAT_LONGTEXT_RAW_CTRLV_PASS_WITH_CODEX_FILECLIP_ONLY`.
