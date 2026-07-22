# Compare And Repair

Use this reference after at least one bad snapshot exists. Prefer collecting a good snapshot after the user switches link/node, then compare before changing Windows or app settings.

## Compare Order

1. `05-user-internet-proxy.txt`
   - Confirm proxy enable state and port did not unintentionally change.
   - If the good state uses a different local port, identify which app changed it before editing anything.
2. `local-proxy-port-tests.txt`
   - Confirm the configured proxy port accepts TCP.
   - If false, inspect the proxy client process, not browser settings first.
3. `dns-*.txt`
   - Look for ChatGPT/OpenAI domains resolving to unrelated, hijacked, local, or suspicious IPs.
   - Treat repeated strange DNS across default DNS and public DNS as a node/route/DNS-mode clue, not proof that Windows DNS must be changed.
4. `curl-direct-vs-proxy.txt`
   - Direct failure can be expected on restricted networks.
   - Proxy success for Google/Cloudflare plus failure for ChatGPT/OpenAI usually points to node, rules, SNI, DNS mode, or endpoint reputation.
   - Bare `curl -I https://chatgpt.com/` can return `403` even when browser-like traffic works. Do not use it alone as the recovery verdict.
5. `client-like-openai-checks.txt`
   - Treat browser-like ChatGPT `200 OK` as a strong ChatGPT reachability signal.
   - Treat OpenAI API `/v1/models` returning `401 Unauthorized` with a missing bearer message as a healthy API reachability signal.
   - Treat timeout, repeated `403`, or repeated `421` here as a stronger failure signal than the bare curl file.
6. `health-verdict.md`
   - Read this before making a repair decision.
   - `HEALTHY for ChatGPT/OpenAI-style client traffic` means no proxy repair is needed just because bare curl shows `403/421`.
   - If this verdict is healthy while the app still fails, suspect app-specific cache/session/runtime state.
7. `04-winhttp-proxy.txt`
   - Only change WinHTTP when the failing program is WinHTTP-based.

## Minimal Repair Ladder

Use the lowest step that fits the evidence:

1. Switch to a known-good link/node inside the existing proxy client and recapture.
2. Refresh only the proxy client subscription/profile if the user requested it and current profile is backed up/exported.
3. Adjust proxy client DNS mode/rule behavior only when bad DNS leakage is proven and the app exposes a reversible setting.
4. Restore Windows user proxy only if it no longer matches the working proxy client port.
5. Set WinHTTP proxy only for a known WinHTTP client, and save the previous WinHTTP state first.
6. Restart the affected app only after preserving the current state.

## Intermittent Paoluz / FlClash Pattern

When the same node or link works again after re-pasting and saving, treat the literal node content as less suspicious than runtime state:

- profile/rule reload
- DNS/fake-ip mapping cache
- rule provider refresh state
- old connection pool state
- app-specific Chromium/Electron cache, Secure DNS, or QUIC/HTTP3 behavior
- stale local app sockets, especially `WeChatAppEx.exe` `CLOSE_WAIT` connections to old `FlClashCore.exe` PIDs after the proxy core reloads

Do not classify bare `curl HEAD` `403/421` as failure if `health-verdict.md` is healthy. In this pattern, the mature path is:

1. Capture the failing state immediately.
2. Save FlClash logs/Connections/Requests around the failure timestamp when available.
3. Re-save/reload the same profile without changing the node.
4. Capture the recovered state.
5. Compare app-specific domains, rule hits, DNS answers, and client-like checks.
6. Only then consider a single reversible change: refresh rule providers, adjust DNS/fake-ip mode, or clear app cache.

If Paoluz is a WeChat mini-program and the proxy remains healthy, run `scripts/repair-stale-app-proxy-sockets.ps1` in dry-run mode. If it reports stale `WeChatAppEx.exe` sockets to old proxy-core PIDs, restart only those stale `WeChatAppEx.exe` processes before touching FlClash or Windows proxy settings.

Treat installing third-party "clash doctor" skills as low priority unless the package has high trust. A search on 2026-06-10 found low-install candidates only, so prefer this local skill plus official Clash/Mihomo/FlClash docs.

## Stop Conditions

Stop before:

- deleting proxy profiles or subscriptions
- resetting Windows network stack
- changing router DNS globally
- editing hosts file
- exposing tokens, URLs, passwords, or subscription secrets in reports
- changing account, payment, or security settings

## Report Shape

For the user, include:

- where snapshots are saved
- what still works
- what fails
- strongest evidence for the fault layer
- what was not changed
- recommended next comparison or repair step
