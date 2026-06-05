# AUTO Internal LLM Selftest

Generated: 2026-05-23T17:12:54.655Z

Status: `G05_PASS_AUTO_FORCED_FALLBACK_INTERNAL_SELFTEST`

- Model mode: `auto`
- Simulate primary failure: true
- Route: `xiaolongxia-nvidia-nim-dryrun`
- Provider: `nvidia-nim-dryrun`
- Primary: `meta/llama-3.1-8b-instruct`
- Fallback: `meta/llama-3.1-70b-instruct`
- UI required: false
- Real send: false
- Key printed: false

| # | HTTP | Selected model | Fallback | Pass | Latency ms | Response |
|---:|---:|---|---|---|---:|---|
| 1 | 200 | `meta/llama-3.1-70b-instruct` | true | true | 6422 | 写作文需要先搭框架是因为这样可以帮助孩子理清思路，组织好自己的想法。就像盖房子一样，先搭好框架，才能填充内容。这样可以避免孩子写着写着不知道该写什么了，或者写完后发现自己写的东西杂... |

## Summary

- Success: 1/1
- Selected model OK: true
- Real sends: 0
- Model/API/provider leaks: 0
- False promises or unconfirmed claims: 0
