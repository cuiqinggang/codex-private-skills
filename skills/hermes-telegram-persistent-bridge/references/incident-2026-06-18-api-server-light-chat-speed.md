# 2026-06-18 API Server Light Chat Speed Repair

## Trigger

Use this when Open WebUI / browser access to Hermes can answer but feels very
slow: first visible word takes many seconds, long answers appear to stall, while
Telegram remains fast.

## Boundaries

- Do not change Windows proxy, FlClash proxy/node/rules, Telegram proxy, or
  `TELEGRAM_PROXY=http://127.0.0.1:7890`.
- Do not print `.env`, bot tokens, `API_SERVER_KEY`, or provider keys.
- Preserve Telegram's normal Hermes Agent route unless the incident is
  explicitly Telegram-only.

## Root Cause Found

The browser path was not simply "network slow". `/v1/chat/completions` routed
ordinary Open WebUI chat through the full Hermes Agent. Each browser request
carried roughly 9k input tokens of agent/system/tool context before the user's
message. Streaming was enabled, but the first visible token still waited for the
model to process that heavy prompt.

`z-ai/glm-5.2` showed very slow first-token behavior only when OpenRouter was
allowed to use its default reasoning path. The model itself was not the final
root cause. Direct A/B testing showed that explicitly sending
`reasoning: {"enabled": false}` changes GLM-5.2 from a slow path to a normal
streaming path:

| GLM-5.2 OpenRouter request variant | First visible token |
| --- | ---: |
| default / no explicit reasoning control | 20s-49s observed |
| `reasoning: {"enabled": false}` | about 1.2s-5s observed |

## Repair Pattern

1. Run the normal diagnostic script and confirm Telegram/Gateway/8642 are alive.
2. Verify the real Gateway config with `HERMES_HOME=C:\Users\A\.hermes`; do not
   trust a plain shell if it resolves to AppData.
3. Keep `display.platforms.api_server.streaming: true`.
4. Add/keep a narrow `platform_toolsets.api_server` so browser does not inherit
   unnecessary tools.
5. Set main `agent.reasoning_effort: "none"` if the model supports reasoning
   controls. Confirm `GatewayRunner._load_reasoning_config()` returns
   `{'enabled': False}`.
6. Ensure `launcher/start-hermes-openwebui.ps1` passes `API_SERVER_KEY` from
   `.env` into the child Gateway process before `Start-Process`.
7. If browser still has slow first visible token, split ordinary browser chat
   from full Hermes Agent while keeping the same GLM-5.2 model:
   - keep Telegram on normal Hermes Agent;
   - make `/v1/chat/completions` stream ordinary OpenAI-compatible chat through a
     light direct model;
   - default the browser light model to `z-ai/glm-5.2`;
   - send OpenRouter `extra_body={"reasoning": {"enabled": False}}`;
   - leave session/automation endpoints on the full Agent route.

## Acceptance Evidence From Repair

After light browser chat was enabled, GLM-5.2 was kept as the browser model,
OpenRouter reasoning was explicitly disabled, and Gateway was restarted:

| Test | First visible | Total | Result |
| --- | ---: | ---: | --- |
| 6 short one-sentence prompts | 2.0s-4.2s | 2.1s-4.3s | completed |
| 2 long Chinese practical answers | 1.6s-4.4s | 10.5s-16.4s | completed |

Final stability run: 8/8 completed, 0 empty responses, `bad_json=0`,
`finish_done=true`. The largest first visible token delay was about 4.4s.

## Required Hardening

OpenRouter/GLM-5.2 may occasionally return an empty streaming completion with a
terminal finish reason. The browser route must not pass that blank result to the
user. Keep a one-time retry when the direct light stream finishes with no visible
content:

```text
if the first light-chat stream emits no content:
    retry once with the same model and reasoning disabled
```

## Notes

If future testing shows Open WebUI needs full Hermes tools, provide a separate
explicit Agent route instead of making every normal browser chat pay the full
agent prompt cost.
