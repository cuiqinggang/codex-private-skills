---
name: chatgpt-cdp-browser
description: Use when Codex needs to bridge to the logged-in ChatGPT website for planning, judgment, long-form reasoning, or strategy, then bring the result back for local execution. Covers Chrome CDP browser control, debug Chrome on 9333, optional Windows/WSL 9334 portproxy, agent-browser snapshot/click/fill/press/screenshot flow, UTF-8 Chinese input handling, and safe stop conditions for login, captcha, limits, or account prompts.
---

# ChatGPT CDP Browser

## Purpose

Use this skill to reuse the mature ChatGPT website bridge instead of re-inventing it. The intended division is:

1. ChatGPT website handles planning, judgment, long text, and strategy.
2. Codex handles local files, code changes, tests, screenshots, backups, and execution.

This skill automates the transport layer: attach to a user-logged-in ChatGPT browser, send one planning question, wait for the answer, capture/read evidence, and return the answer to Codex for implementation.

## Read First

For detailed commands and known-good history, read only the needed file:

- `ACTIVE_CHATGPT_CDP_STATUS.md`: current verified chain and dynamic values.
- `CHATGPT_CDP_KNOWN_GOOD_COMMANDS.md`: shortest command index.
- `CHATGPT_CDP_BROWSER_AUTOMATION_RUNBOOK.md`: full mature runbook and failure history.
- `SKILL.original-full.md`: original imported long-form skill from the H drive archive.

## Standard Flow

1. Start a dedicated debug Chrome with remote debugging on `127.0.0.1:9333` and a separate profile.
2. Have the user log in manually if ChatGPT is not already logged in.
3. If working from WSL or another agent side, expose Windows `9333` through `9334` and detect the WSL gateway dynamically.
4. Fetch the current `webSocketDebuggerUrl`; never reuse an old Browser WS after Chrome restarts.
5. Run `agent-browser --cdp "$WS" snapshot -i` and dynamically find the ChatGPT textbox ref.
6. Send exactly one message, wait for the answer, and capture screenshot or snapshot evidence.
7. Bring the ChatGPT answer back into Codex, turn it into an execution plan, and run local implementation/testing.

## Key Rules

- Do not automate password entry, captcha solving, account settings, payment, or bypassing limits.
- Stop and report if login, captcha, limit, policy, or security prompts appear.
- Do not use stale values for WSL gateway, Browser WS, or textbox ref.
- Re-run snapshot after page changes before clicking or filling.
- Send one message at a time; wait for completion and evidence before continuing.
- For Chinese text, prefer the UTF-8 file method from `CHATGPT_CDP_KNOWN_GOOD_COMMANDS.md`; direct PowerShell-to-WSL Chinese strings can become question marks.

## Known-Good Chain

The imported mature runbook verified this chain:

```text
Windows debug Chrome
-> 9333 original CDP port
-> 9334 Windows/WSL unified port
-> WSL/agent side
-> agent-browser
-> ChatGPT page
-> click textbox
-> fill English TEST_OK
-> fill UTF-8 Chinese prompt
-> press Enter
-> wait for reply
-> screenshot evidence
```

Verified statuses in the imported runbook:

```text
G01 debug Chrome login: PASS
G02 9333 -> 9334 -> WSL: PASS
G03 snapshot read: PASS
G04 English TEST_OK send: PASS
G05 direct Chinese: FAIL, encoding issue located
G05-FIX UTF-8 Chinese file send: PASS
```

## Minimum Command References

Use `references/g01-start-chrome.ps1` to start debug Chrome.
Use `references/g02-portproxy-9334.ps1` if WSL access through `9334` is needed.
Use `references/g03-snapshot.sh` to attach and read the page.
Use `references/g04-send-english.sh` for a simple send proof.
Use `references/g05-fix-send-chinese-utf8.sh` for Chinese prompt sending.

## Decision Boundary

Use this skill when the user explicitly wants the ChatGPT website involved as the planning/reasoning side of a Codex workflow. For ordinary web UI testing, prefer the `playwright` or `playwright-interactive` skill. For isolated browser demonstrations that do not need ChatGPT, prefer `virtual-mouse-keyboard-demo`.
