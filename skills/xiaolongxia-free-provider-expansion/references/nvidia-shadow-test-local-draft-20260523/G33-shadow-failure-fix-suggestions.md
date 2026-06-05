# G33 Failure Fix Suggestions

Status: `G33_FIX_SUGGESTIONS_READY`

| Message | Category | Reason |
| --- | --- | --- |
| SIM-007 | 手机能不能用 | 包含未确认渠道/价格声明 |

Suggested system prompt additions:

- If unsure about price, channel, app, website, or availability, say "可以先人工确认后再回复".
- Keep replies closer to 60-100 Chinese characters.
- If the question asks for medical, legal, financial, account, payment, or privacy advice, generate "建议人工回复" instead of an answer.

Model routing suggestion:

- Keep 8B as primary.
- Use 70B fallback only when 8B fails or gets score below 4 in local review.
- Do not auto-send low-score replies.
