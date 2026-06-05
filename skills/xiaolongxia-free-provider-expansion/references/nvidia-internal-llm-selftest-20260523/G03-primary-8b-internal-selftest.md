# PRIMARY Internal LLM Selftest

Generated: 2026-05-23T17:12:11.257Z

Status: `G03_PASS_PRIMARY_8B_INTERNAL_SELFTEST`

- Model mode: `primary`
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
| 1 | 200 | `meta/llama-3.1-8b-instruct` | false | true | 1595 | 家长可以帮助孩子建立写作思路，鼓励他们从生活中寻找写作素材。同时，陪伴孩子练习写作，提供反馈和指导。家长也可以帮助孩子改善写作技巧，例如组织结构、用词选择等。最重要的是，家长应该给... |
| 2 | 200 | `meta/llama-3.1-8b-instruct` | false | true | 2321 | 这个问题很常见，孩子们可能会感到困惑。首先，我们需要帮助孩子们理解题目背后的逻辑和思路。我们可以通过提供具体的例子和解释，帮助他们了解题目中涉及的数学概念和运算。另外，我们也可以鼓... |
| 3 | 200 | `meta/llama-3.1-8b-instruct` | false | true | 1113 | AI 辅导和普通补课的区别在于辅导的方式和方法。普通补课通常是老师直接传授知识，而 AI 辅导则是通过 AI 技术来辅助孩子学习和提高。AI 辅导可以通过提供个性化的学习建议、帮助... |
| 4 | 200 | `meta/llama-3.1-8b-instruct` | false | true | 850 | 家长可以先和孩子一起讨论，了解孩子的学习困难和担忧。然后，家长可以帮助孩子分解大任务，制定一个可行的学习计划。同时，家长可以陪伴孩子一起学习，提供指导和支持。还可以鼓励孩子自己思考... |
| 5 | 200 | `meta/llama-3.1-8b-instruct` | false | true | 1174 | 小龙虾就是个好帮手！它可以陪你一起学习，帮助你改进作文，讲解难懂的知识点。想写作文却不知道从哪里开始？小龙虾可以给你一些启发，帮助你想出主意。想提高成绩？小龙虾可以和你一起练习，帮... |

## Summary

- Success: 5/5
- Selected model OK: true
- Real sends: 0
- Model/API/provider leaks: 0
- False promises or unconfirmed claims: 0
