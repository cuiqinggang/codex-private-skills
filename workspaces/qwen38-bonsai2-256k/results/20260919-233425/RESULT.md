# RESULT — Bonsai 2 27B PQ2_0 256K baseline v2

- Status: `BLOCKED`
- Timestamp: `20260919-233425`
- Next action: `RETURN_TO_GPT`

## Outcome

The verified Phase A result from commit `664a2289ede02d295611384e41fd6777331b369d` was inherited. The v2 minimal drift check passed. Phase B v2 stopped during the pinned CUDA runtime download before extraction.

The x1 aria2 probe received a GitHub release-assets redirect but no bytes within 30 seconds. The x4 probe failed with TLS handshake error 2746 (remote forced close). A curl HEAD check to the same fixed GitHub URL failed to connect to `github.com:443` with exit code 28. The contract forbids proxy or system-network changes, so execution stopped.

## Verified state

- `phase_a=PASS` (inherited)
- `drift_check=PASS`
- `runtime_bootstrap_method=PINNED_RELEASE_DIRECT`
- `setup_ps1_executed=false`
- Runtime ZIP bytes received: `0`
- Runtime hashes verified: `NO`
- Runtime extracted: `NO`
- CUDA binary installed: `NO`
- Model download started: `NO`
- GGUF files downloaded: `0`
- 256K server/baseline: `NOT_RUN`
- Proxy/network/system settings changed: `NO`
- Empty partial and aria2 continuation control file preserved: `YES`

## Runtime assets

- `llama-prism-b10709-9a9394a-bin-win-cuda-12.4-x64.zip` — expected 253442371 bytes, SHA-256 `f565c8428c1f108311f65ed97f02425188b3aa3c745c2bc597521bbd24bcbbc9`; actual 0 bytes, unverified.
- `cudart-llama-bin-win-cuda-12.4-x64.zip` — expected 391443627 bytes, SHA-256 `8c79a9b226de4b3cacfd1f83d24f962d0773be79f1e7b75c6af4ded7e32ae1d6`; not started.

## Baseline fields

All model, server, context, prompt, timing, marker, and resource fields remain zero or `NOT_RUN`; none are claimed as model failures.

## Evidence

- `evidence/drift-check.json` — SHA-256 `056cc845b291bd1265eae6b2ccd087b219d95271c8490b2143bae4468ac0b386`, 901 bytes
- `evidence/drift-check.txt` — SHA-256 `fc21aa57b9359295ec0e9057573ff2e07b56a2dd4a7100ca1c7563b2e5194ff4`, 299 bytes
- `evidence/Invoke-PhaseBv2.ps1` — SHA-256 `35d0ec4c66f94746bfaef701aa2edd232b9f655a00c235a3b1eb2ad50d25aafe`, 17838 bytes
- `evidence/llama-probe-x1.aria2.txt` — SHA-256 `088c0329cb104342e022c16a1f8960ef682a50ec0b174b9c630d0a063d210270`, 226 bytes
- `evidence/llama-probe-x1.stderr.txt` — SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`, 0 bytes
- `evidence/llama-probe-x1.stderr.txt.failed-invocation1` — SHA-256 `225ba2ab840dcc98cedbca8d93b602685b63f8f5616b74c95788de3912200183`, 487 bytes
- `evidence/llama-probe-x1.stdout.txt` — SHA-256 `2345f56415153d7fbf6ef81e870deb23652dae99075dedda5d5b92dc0ad706e4`, 2357 bytes
- `evidence/llama-probe-x4.aria2.txt` — SHA-256 `1ea7a07b4f1fb6e9f3831ffbc0f9c18fc11b9e96ffc28370bd42a13e8c0bc03c`, 823 bytes
- `evidence/llama-probe-x4.stderr.txt` — SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`, 0 bytes
- `evidence/llama-probe-x4.stderr.txt.failed-invocation1` — SHA-256 `0059295b451b2f0a5118d6ae14a0d96cc54d787ae57a76321638b3372b480bd8`, 487 bytes
- `evidence/llama-probe-x4.stdout.txt` — SHA-256 `a2884bbdbbe00ee4d48cf68313a9593396af10d702ff1cb566dd9a577f0846a8`, 3295 bytes
- `evidence/network-diagnostic.txt` — SHA-256 `b66df143f7471e52822f1fe76df4e99c7eaf80c5ec01f6449757ddaefec1676d`, 392 bytes
- `evidence/powershell-guard-incidents.jsonl` — SHA-256 `27ad1aea42c20a6817c8c9bc1261829595fadc4a24b95ded76f14a623d8dc636`, 1698 bytes
- `evidence/runtime-download-final.json` — SHA-256 `0bfcfb28a4117eec1d1a2a660df768f4af4c781d935fac6dcb5e9279b3929b6c`, 1514 bytes
- `evidence/runtime-download-monitor.csv` — SHA-256 `6b19f5c73da11e588725b9de18ceae4174388e93567c05343560cf1aa198d4b1`, 325 bytes
- `evidence/runtime-download-probes.json` — SHA-256 `4cb9ac0ac70778e1a730f854f70f06817b515063d28f89ac5c29751a928bcba9`, 1478 bytes
- `evidence/runtime-existing-before.json` — SHA-256 `7eb70257593da06f682a3ddda54a9d260d4fc514f645237f5ca74b08f8da61a6`, 2 bytes

## Stop reason

`Pinned GitHub runtime download was unreachable without prohibited network/proxy changes.`
