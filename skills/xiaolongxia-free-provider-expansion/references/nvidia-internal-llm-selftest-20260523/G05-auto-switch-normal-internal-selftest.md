# AUTO Internal LLM Selftest

Generated: 2026-05-23T17:12:50.184Z

Status: `G05_PASS_AUTO_NORMAL_INTERNAL_SELFTEST`

- Model mode: `auto`
- Simulate primary failure: false
- Route: `xiaolongxia-nvidia-nim-dryrun`
- Provider: `nvidia-nim-dryrun`
- Primary: `meta/llama-3.1-8b-instruct`
- Fallback: `meta/llama-3.1-70b-instruct`
- UI required: false
- Real send: false
- Key printed: false

| # | HTTP | Selected model | Fallback | Pass | Latency ms | Response |
|---:|---:|---|---|---|---:|---|
| 1 | 200 | `meta/llama-3.1-8b-instruct` | false | true | 1945 | 孩子写作文需要先搭框架是因为这样可以帮助他们组织思路，明确文章的结构和内容。搭框架可以让孩子清楚地知道要写什么，如何写什么，最后呈现出一个整体的文章。这样可以减少写作的混乱和杂乱，... |

## Summary

- Success: 1/1
- Selected model OK: true
- Real sends: 0
- Model/API/provider leaks: 0
- False promises or unconfirmed claims: 0
