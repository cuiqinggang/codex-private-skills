# RESULT — Bonsai 2 27B PQ2_0 256K baseline v3

- Status: `BLOCKED`
- Timestamp: `20260920-002126`
- Next action: `RETURN_TO_GPT`

## Outcome

The frozen v1/v2 results were inherited and the v3 minimal drift check passed. The required proxy discovery command was rejected before process creation by the managed safety policy because it included reading HKCU Internet Settings and persisting an actual selected endpoint.

The rejection explicitly prohibited an indirect workaround. No registry, Git proxy, WinHTTP proxy, FlClash port relationship, or proxy endpoint was read by that atomic command; no curl Range test was run. Runtime and model downloads did not start.

## Verified state

- v1 Phase A inherited: `PASS`
- v2 transport blocker inherited
- v3 drift check: `PASS`
- FlClash processes visible during drift check: `2`
- Existing explicit proxy endpoint: `UNKNOWN_POLICY_BLOCKED`
- Existing proxy transport: `NOT_TESTED`
- System proxy modified: `NO`
- Git proxy modified: `NO`
- FlClash modified: `NO`
- Network modified: `NO`
- Registry modified: `NO`
- Persistent proxy environment modified: `NO`
- Runtime download started: `NO`
- Model download started: `NO`
- 256K baseline: `NOT_RUN`

## Safety boundary

No `reg query`, UI automation, guessed port, port scan, proxy change, node switch, TUN/mode change, mirror, or alternate transport was attempted after the policy rejection.

## Evidence

- `evidence/drift-check.json` — SHA-256 `3c2e44458122c373654679f4a05fd29d56ca857f46201a7e0cd7db3e228b5bfc`, 1344 bytes
- `evidence/drift-check.txt` — SHA-256 `597cdd34d5fd57a8c608dcaab73adbfdc38ec0c633395500919cdaefae30dfa7`, 250 bytes
- `evidence/proxy-readonly-discovery.json` — SHA-256 `0fdb9ecc2fd84c1e6db32e3e86e84ae734d15c8db2399f202d0efd6584b8b3b6`, 1338 bytes
- `evidence/proxy-readonly-discovery.txt` — SHA-256 `d89c0d6ed32068e5b111c0bc974d799f1a4f3ceaa132bd119eb8053c965abd26`, 661 bytes
- `evidence/proxy-transport-summary.json` — SHA-256 `ec9247a21dbd4b8ed6c9121ecefba6965849ac009327f9b4cf289c972fa792a5`, 696 bytes
- `evidence/proxy-transport-tests.json` — SHA-256 `7eb70257593da06f682a3ddda54a9d260d4fc514f645237f5ca74b08f8da61a6`, 2 bytes

## Stop reason

`Managed safety policy blocked the required HKCU proxy read before proxy discovery could start.`
