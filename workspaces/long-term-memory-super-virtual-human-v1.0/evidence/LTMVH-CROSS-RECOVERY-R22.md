# LTMVH Cross-Recovery Reality R22

- EVIDENCE_ID: LTMVH-CROSS-RECOVERY-R22
- DATE: 2026-10-03
- MACHINE: DESKTOP-4A1EGTM
- RUNNER: DESKTOP-4A1EGTM-etal
- CHECKOUT_USED: NO
- DCR_FAILURE_INJECTED: YES
- DCR_INITIAL_PING_AFTER_INJECTION: TIMEOUT
- RECOVERY_CONTROL_PLANE: GitHub Actions -> self-hosted runner -> C:\AI\LTMVH-Recovery\requests\revive-dcr.flag -> Recovery-Request-Watchdog.ps1
- RECOVERY_ACK_AT: 2026-10-03T19:59:06.2812225+08:00
- DCR_POST_RECOVERY_PING: PASS
- PATH_B_OUT_OF_BAND_RECOVERY: PASS

## Fault injection evidence

At 2026-10-03T19:58:27+08:00, the DCR watchdog / command shell / node remote process set was force-terminated. The next DCR ping timed out, proving loss of the primary Windows control path.

A GitHub push then triggered `.github/workflows/ltmvh-dcr-cross-recovery-reality.yml`. The workflow contains no checkout step. The self-hosted Windows runner wrote a local recovery request flag. The already-installed user-session Recovery Request Watchdog acknowledged the request and relaunched DCR. A subsequent independent DCR ping returned pong.

## Acceptance correction

Previous `Recover-LTMVH.ps1 -Mode Full` could return PASS when DCR and the browser watchdog were alive even though CDP and the continuity runtime were unavailable.

That local acceptance rule was corrected on 2026-10-03 so Full PASS now requires:
- DCR alive
- browser watchdog alive
- CDP 9223 available
- continuity runtime alive
- controlState = CDP_AVAILABLE

After the correction, the current browser state correctly evaluates to DEGRADED because the existing shared browser is running without remote debugging / CDP control.

## Current boundary

R22 proves only the out-of-band Windows control recovery path. It does NOT prove end-to-end ChatGPT page recovery.

Overall recovery remains NOT FINAL PASS until a separate Reality demonstrates:
1. active page/turn failure,
2. checkpoint retained,
3. true New chat, not Branch,
4. exactly-once handoff,
5. expected ACK / continuation,
6. no manual user forwarding.

Current blocker: the existing shared-mcp browser is alive but was started without CDP, and the safety contract forbids closing that existing browser merely to make a test pass.
