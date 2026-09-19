# RESULT — Qwen3.8 / Bonsai 2 27B PQ2_0 256K baseline

- Status: `BLOCKED`
- Timestamp: `20260919-224518`
- Next action: `RETURN_TO_GPT`

## Outcome

Phase A passed and its evidence was saved. Phase B stopped before `setup.ps1` because the pinned upstream script does not implement `BONSAI_SKIP_GGUF` and unconditionally calls `Download-GgufModel`. Executing it would have violated the command pack and the explicit instruction not to download a model during runtime preparation.

No model download, server start, 256K request, fallback, proxy change, network-setting change, or system-setting change occurred.

## Phase A

- PowerShell: `7.6.6` (`C:\Program Files\PowerShell\7\pwsh.exe`)
- GPU: `NVIDIA GeForce RTX 2080 Ti`
- GPU memory: `22528` MiB total; `1501` MiB used at capture
- CUDA driver-reported version: `13.1`
- System RAM: `31.947` GiB total; `16.39` GiB available
- C: free: `352.893` GiB
- Hard gates: `PASS`
- Staging files after stop: `0`

## Phase B blocker

- Bonsai-demo HEAD: `17b143e889a45c090816b520e79a50c996164e1f`
- `BONSAI_SKIP_GGUF` references in pinned `setup.ps1`: `0`
- Unconditional call: `setup.ps1:373` → `Download-GgufModel $fam $sz`
- `setup.ps1` executed: `NO`
- GGUF files present: `0`
- Runtime binary files present: `0`

## Required baseline fields

The model, CUDA runtime path, KV4 state, effective 262144 context, 240K–245K prompt, markers, timings, and resource peaks are unmeasured because execution stopped at the required safety boundary. Their numeric fields remain `0` and boolean runtime assertions remain `false` in `RESULT.json`; they are not claimed as failures of the model itself.

## Evidence

- `evidence/Invoke-PhaseA.ps1` — SHA-256 `54a857f345966f9cfaca42e6f81ed6576aa9db2939b1b45f5bd18ece079870cb`, 8703 bytes
- `evidence/phase-b-blocker.json` — SHA-256 `71086279c9c0ca4fd542b9f8007e7e17c768819866b29c4b0dbfdf247b8c3698`, 1058 bytes
- `evidence/powershell-guard-incidents.jsonl` — SHA-256 `6ef0a6754d44d7a3056f77b050a39349e606134e4fcedb90d1e85fc6f41b1091`, 2023 bytes
- `evidence/preflight.json` — SHA-256 `d614bb717c029c90d60e2482c4f229155e73817ef3eb6ad4df8f6c3a14df4f12`, 8396 bytes
- `evidence/preflight.txt` — SHA-256 `5e48da523fbe7ef303b88cfee13ae2f512ccbeed08aef8ce07814a6654a4ef54`, 873 bytes
- `evidence/setup-skip-audit.txt` — SHA-256 `96972d496f51d5e97dc8d2ad6a68a4f43fc894ece910c5b5cf09e596302a5a82`, 2028 bytes

## Stop reason

`Pinned setup.ps1 lacks BONSAI_SKIP_GGUF; continuing would start a model download and violate the task contract.`
