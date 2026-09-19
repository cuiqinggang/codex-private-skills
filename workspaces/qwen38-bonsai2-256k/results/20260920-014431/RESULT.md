# Qwen3.8 / Ternary Bonsai 2 27B 256K - v4 result

STATUS=BLOCKED_RUNTIME_COMPATIBILITY
NEXT_ACTION=RETURN_TO_GPT
STOP=true
RESULT_TIMESTAMP=20260920-014431
V3_COMMIT=8a293bb4a459436893b9d8e6ce1187e0497ca529

## Proxy discovery

- WINDOWS_HKCU_PROXY_SOURCE=POLICY_BLOCKED_EXCLUDED
- GIT_PROXY_SOURCE_STATUS=POLICY_BLOCKED_SENSITIVE_VALUE
- WINHTTP_SOURCE_STATUS=NONE
- FLCLASH_LISTENER_SOURCE_STATUS=FOUND
- ATOMIC_COMMANDS_USED=true
- POLICY_BYPASS_ATTEMPTED=false
- source=FlClashCore_process_listener
- candidate_count=2
- loopback=true
- endpoint_fingerprint=f1410cd719dcee161d171a3729c50bffabb9325546e31867d85db2b0773db22e
- raw_endpoint_persisted=false

Git proxy value discovery was frozen after managed safety review rejected sensitive-value disclosure. It was not interpreted as NONE and was not retried. WinHTTP independently returned Direct access. The exact FlClashCore PID had two loopback LISTEN sockets; no port scan or port guess was used.

## Range probe

- asset=llama-prism-b10709-9a9394a-bin-win-cuda-12.4-x64.zip
- requested_range=0-1048575
- proxy_protocol=http
- http_status=206
- bytes_received=1048576
- elapsed_ms=3637.314
- exit_code=0
- range_probe_status=PASS
- existing_proxy_transport=PASS

No raw host or port is persisted.

## Runtime acquisition and verification

- Asset 1: x1/s1 completed; bytes=253442371; SHA256=f565c8428c1f108311f65ed97f02425188b3aa3c745c2bc597521bbd24bcbbc9; PASS.
- Asset 2: x1/s1 produced a 249820203-byte reusable partial; x4/s4 continued it to bytes=391443627; SHA256=8c79a9b226de4b3cacfd1f83d24f962d0773be79f1e7b75c6af4ded7e32ae1d6; PASS.
- x8 was unnecessary and not run.
- Both verified archives were extracted to the frozen runtime target.
- Required llama and CUDA runtime files were present after extraction.

## Runtime compatibility gate

The first version query produced no output. The single diagnostic follow-up returned exit_code=-1073741795 (0xC000001D, illegal instruction) with no version output.

RUNTIME_VERSION_GATE=FAIL
RUNTIME_COMPATIBILITY=FAIL_ILLEGAL_INSTRUCTION
MODEL_DOWNLOAD=NOT_STARTED
SERVER_262144=NOT_STARTED
BASELINE_240K_245K=NOT_RUN

The run stopped at the required runtime gate. No model or baseline request was made; unavailable metrics are null in RESULT.json.

## Frozen contract and mutations

TARGET_CONTEXT=262144
ONLY_MODEL=Ternary-Bonsai-2-27B-PQ2_0.gguf
KV4=ON
THINKING=OFF
SPECULATIVE=OFF
TEXT_ONLY=YES
CONCURRENCY=1
T_PHY=OFF
NO_AUTO_128K_FALLBACK=YES
PTQ1_0=FORBIDDEN
F16=FORBIDDEN
MMPROJ=FORBIDDEN
DRAFTER=FORBIDDEN

system_proxy_modified=false
git_proxy_modified=false
flclash_modified=false
network_modified=false
registry_modified=false
persistent_proxy_env_modified=false
