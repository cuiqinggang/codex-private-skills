# FALLBACK Internal LLM Selftest

Generated: 2026-05-23T17:12:26.462Z

Status: `G04_PASS_FALLBACK_70B_INTERNAL_SELFTEST`

- Model mode: `fallback`
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
| 1 | 200 | `meta/llama-3.1-70b-instruct` | false | true | 7715 | 小明家里有 15 个苹果，他想分给 5 个朋友，每个朋友分得一样多。小明还想留下 2 个苹果自己吃。那么，小明应该给每个朋友多少个苹果呢？我们可以先把留下的 2 个苹果除外，剩下 ... |
| 2 | 200 | `meta/llama-3.1-70b-instruct` | false | true | 6420 | 家长们很忙，没时间辅导孩子学习怎么办？其实，AI 可以帮忙。它可以给孩子讲解思路，改正作文，陪伴孩子练习，启发孩子自己动脑想。孩子们可以通过和 AI 交互，提高自己的学习效率和兴趣... |
| 3 | 200 | `meta/llama-3.1-70b-instruct` | false | true | 8121 | 孩子使用 AI 辅助学习确实可能产生依赖性，但这取决于如何使用。我们的目标是让孩子学会使用 AI 作为工具，启发他们自己思考和解决问题，而不是简单地依赖 AI 的答案。通过与 AI... |

## Summary

- Success: 3/3
- Selected model OK: true
- Real sends: 0
- Model/API/provider leaks: 0
- False promises or unconfirmed claims: 0
