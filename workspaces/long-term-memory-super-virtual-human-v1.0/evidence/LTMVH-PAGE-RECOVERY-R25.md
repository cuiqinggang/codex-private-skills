# LTMVH Page Recovery Reality R25

- EVIDENCE_ID: LTMVH-RECOVERY-BROWSER-R25
- DATE: 2026-10-03
- MACHINE: DESKTOP-4A1EGTM
- TEST_BROWSER_PROFILE: C:\AI\Playwright-Native-AI-Browser\profile\tests
- CDP_ENDPOINT: http://127.0.0.1:9333
- SHARED_MCP_BROWSER_TOUCHED: NO
- BRANCH_USED: NO
- SECOND_BROWSER_FOR_SHARED_MCP: NO

## Reality result

A dedicated Playwright Chromium instance was started with the isolated `profile\tests` profile and CDP port 9333. CDP was independently verified through both `/json/version` and `/json/list`, with the controlled page at `https://chatgpt.com/`.

The R25 continuity task then executed the following real sequence:

```text
fault prompt submitted
→ active turn observed
→ progress intentionally suppressed
→ 8 s hard deadline exceeded
→ read-only page probe
→ stalled turn aborted
→ composer restored / stop button gone
→ current page navigated to true New chat
→ New chat probe: url=https://chatgpt.com/, userTurns=0, assistantTurns=0
→ minimal handoff sent
→ exactly-once marker check
→ expected ACK observed
```

Key timestamps (UTC):

```yaml
STALL_STARTED: 2026-10-03T12:44:45.363Z
HARD_DEADLINE: 2026-10-03T12:44:54.096Z
READ_ONLY_PROBE: 2026-10-03T12:44:54.097Z
ABORT_CONFIRMED: 2026-10-03T12:44:57.041Z
FINISHED: 2026-10-03T12:46:18.141Z
```

Final machine result:

```ini
FAULT_INJECTION=YES
TURN_ACTIVE_OBSERVED=YES
HARD_DEADLINE_EXCEEDED=YES
READ_ONLY_PROBE=PASS
ABORT_STALLED_TURN=PASS
CHECKPOINT=PASS
TRUE_NEW_CHAT=PASS
SUBMISSION_COUNT=1
MARKER_COUNT=1
EXACTLY_ONCE=PASS
ACK_CONFIRMED=YES
PAGE_LEASE_RETAINED=YES
BRANCH_USED=NO
NEW_BROWSER_LAUNCHED_BY_RUNTIME=NO
TRANSPORT=RAW_CDP_EXISTING_BROWSER

R25_PAGE_RECOVERY_REALITY=PASS
```

Recovered conversation URL:

`https://chatgpt.com/c/local-chatgpt%3A7cf086be-7e8b-4388-847b-09f3eb5e2b6c`

## Important interpretation

R25 closes the previously open page-level Reality gap for the isolated controllable test browser: a live generation was deliberately stalled, detected, probed, stopped, checkpointed, rotated to a genuine new conversation, handed off exactly once, and acknowledged.

This does **not** prove that the currently running `shared-mcp` production browser can be recovered in place when that browser was originally launched without CDP. R22 already recorded that production-browser control state as DEGRADED. Therefore:

```ini
DEDICATED_TEST_BROWSER_PAGE_RECOVERY=PASS
CURRENT_SHARED_MCP_IN_PLACE_RECOVERY=DEGRADED
FINAL_VALID=NO
```
