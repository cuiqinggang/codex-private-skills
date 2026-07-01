# Bridge Policy

Use `chatgpt-screenshot-bridge` only when GPT web planning/review is explicitly needed and the user has enabled it for the current conversation.

## Allowed

- send text prompts,
- copy latest text response,
- verify visible status,
- use screenshots to locate explicit ChatGPT controls.

## Stop Immediately

- login or captcha,
- account/security prompt,
- payment or billing screen,
- privacy-sensitive form,
- production admin panel,
- missing send/copy controls,
- unsafe or ambiguous voice/microphone/stop controls.

## Completion Signal

When ChatGPT shows the mid-page down arrow, generation is likely complete and Codex can scroll to the bottom or use the response card copy button.

## Copy Rule

Prefer the response card copy button. If clipboard proof fails, re-check the screenshot state before repeating. Do not switch to DOM/CDP routes unless the user explicitly approves a route change.
