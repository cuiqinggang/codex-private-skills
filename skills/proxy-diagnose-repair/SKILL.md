---
name: proxy-diagnose-repair
description: Diagnose, preserve, compare, and cautiously repair Windows proxy/VPN/network states for flaky tools such as ChatGPT, OpenAI API clients, Electron apps, WeChat mini-programs, Clash/FlClash/Mihomo, V2Ray/Xray, and local proxy ports. Use when the user reports "network exception", "can use but unstable", ChatGPT/OpenAI 403/421/timeouts, DNS pollution, local proxy issues, or asks to save bad/good proxy states before changing links or nodes.
---

# Proxy Diagnose Repair

## Overview

Use this skill to freeze a partially working proxy/network state before changing it, collect read-only evidence, compare bad and good snapshots, then recommend or perform the smallest safe repair. Preserve the user's current working route unless they explicitly ask for a repair action.

## Safety Gate

Default to read-only diagnostics:

- Do not disable proxy, reset network, kill proxy processes, switch nodes, rewrite DNS, clear browser state, or restart apps during baseline capture.
- Stop before destructive or broad changes: deleting profiles, resetting network stack, changing account/payment/security state, exposing secrets, or batch-modifying proxy configs.
- Treat "still works but unstable" as a state to preserve first.

Repair actions are allowed only after a saved baseline and a clear comparison. Prefer reversible changes such as switching to a known-good node, changing app DNS mode inside the proxy client, or restoring a previously captured proxy setting.

## Workflow

1. Load the active AGENTS.md chain and `yesterday-replay-controlled-coding` first.
2. Classify the work:
   - Baseline capture: Level 1, read-only.
   - Comparing two saved states: Level 1.
   - Editing proxy/DNS/app settings: Level 2 if narrow and reversible; Level 3 if broad, destructive, or account/system-security impacting.
3. Create a timestamped folder under `output/network-diagnostics/`.
4. Run `scripts/capture-proxy-state.ps1` with the output folder and optional symptom note.
5. Read `summary.md` and the compact test files first. Load detailed logs only when needed.
6. If the user changes a link/node, capture a second snapshot and compare using `references/compare-and-repair.md`.
7. Recommend the smallest repair. If asked to perform it, preserve rollback data and verify again.

## Capture Command

Use PowerShell:

```powershell
$ts = Get-Date -Format 'yyyyMMdd-HHmmss'
${REDACTED_SECRET}
New-Item -ItemType Directory -Force -Path $out | Out-Null
${REDACTED_SECRET}
```

The script is read-only. It records system/user proxy settings, DNS, selected route/interface data, listening ports, key local proxy ports, related processes, DNS resolution for ChatGPT/OpenAI targets, direct-vs-proxy HTTP probes, client-like OpenAI checks, a health verdict, and a summary.

## Interpretation Priorities

- If local proxy port is down, inspect proxy client process first.
- If local proxy port is up but direct tests fail, that may be normal in restricted networks.
- If `health-verdict.md` says ChatGPT browser-like traffic returns `200 OK` and OpenAI API `/v1/models` returns expected unauthenticated `401`, treat the OpenAI-family network path as healthy even if bare `curl HEAD` shows `403` or `421`.
- If client-like ChatGPT/OpenAI checks return `403`, `421`, or time out, suspect node/export/DNS/rule mode rather than Windows proxy plumbing.
- If WinHTTP is direct but browser/Electron works through user proxy, do not change WinHTTP unless the failing app uses WinHTTP.
- If DNS returns unrelated, hijacked, or pollution-looking addresses for ChatGPT/OpenAI, compare proxy DNS mode and node behavior before touching Windows DNS.

## Resources

- `scripts/capture-proxy-state.ps1`: read-only Windows diagnostic capture.
- `scripts/repair-stale-app-proxy-sockets.ps1`: dry-run by default; detects stale app sockets to the local proxy and can restart only stale `WeChatAppEx.exe` runtimes when explicitly invoked.
- `references/compare-and-repair.md`: how to compare bad/good snapshots and choose minimal repairs.

When this skill is updated from a real incident, keep examples concise and add reusable checks to the script rather than long narrative notes.
