# G05 Auto Switch Internal Selftest

Generated: 2026-05-23T17:13:18.745Z

Status: `G05_PASS_AUTO_SWITCH_INTERNAL_SELFTEST`

## Normal Auto

- Selected model: `meta/llama-3.1-8b-instruct`
- Used fallback: false
- Success: true
- HTTP: 200
- Real send: false

## Forced Primary Failure Auto

- Primary attempt is simulated as HTTP 503 inside the test process only.
- Selected model after switch: `meta/llama-3.1-70b-instruct`
- Used fallback: true
- Success: true
- HTTP: 200
- Real send: false

## Switch Order

`meta/llama-3.1-8b-instruct` -> `meta/llama-3.1-70b-instruct`
