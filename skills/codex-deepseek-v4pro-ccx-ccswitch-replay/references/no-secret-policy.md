# No Secret Policy

- Do not save the DeepSeek official API key in this skill.
- Do not echo the DeepSeek key in reports.
- Do not write the DeepSeek key into Git, H drive documentation, screenshots, summaries, or logs.
- Do not include copied `.env` files in skill packages.
- Do not print CCX proxy access keys unless the user explicitly asks in a private local troubleshooting context.
- If a DeepSeek key is required and unavailable, output:

```text
NEED_DEEPSEEK_API_KEY
```

Then stop.

Final reports may say only whether a key was present, never its value.
