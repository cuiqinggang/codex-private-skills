# Stage 05: Google Gemini Vision Restore

Use this reference only for restoring Google Gemini image-reading support for
Windows native Hermes 0.14. Keep this stage narrow: do not reconnect New API,
Telegram, Docker, old watchdog flows, or unrelated startup layers.

## Stage 05 Gemini Vision Freeze

Final route decision on 2026-05-22:

- Gemini direct access succeeded with `gemini-2.5-flash`.
- The standalone Gemini vision bypass tool succeeded and returned a Chinese
  image description for a local test image.
- Hermes built-in `vision_analyze_tool` was not repaired further.
- The user decided to stop investing in Hermes/Gemini vision integration.
- Daily image understanding should default to GPT/ChatGPT because it is
  simpler, stronger, and more natural for this workflow.
- 日用图片理解默认使用 GPT/ChatGPT，Gemini 旁路冻结备用。

Do not build an image drop box, do not wire Telegram/Open WebUI image entry
points, and do not continue repairing Hermes built-in vision unless the user
explicitly unfreezes Stage 05 in a later task.

## Known Good Settings

- Provider: `google` in user-facing config; Hermes normalizes this to `gemini`.
- Model: `gemini-2.5-flash`.
- Base URL: `https://generativelanguage.googleapis.com/v1beta`.
- Proxy: `http://127.0.0.1:7890` for `HTTPS_PROXY`, `HTTP_PROXY`, and, when
  needed, `ALL_PROXY`.
- API key source: prefer `GEMINI_API_KEY` or `GOOGLE_API_KEY` from
  `C:\Users\A\.hermes\.env` or process environment. Never write keys to reports,
  synced H-drive files, or skill references.

## Failure Classification

- `429 RESOURCE_EXHAUSTED` usually means quota/model allocation. Do not treat it
  as a region failure until quota is checked.
- `gemini-2.0-flash` has previously had zero quota on this desktop. Prefer
  `gemini-2.5-flash`.
- `timeout`, `ConnectTimeout`, or `ReadTimeout` against
  `generativelanguage.googleapis.com` usually means the Gateway did not inherit
  proxy environment variables.
- `API_KEY_INVALID`, `401`, or `403` means key/auth; rotate or repair the local
  env key without printing it.
- `404` or model-not-found means the model name or account allocation changed.

## Minimal Restore Gates

1. Back up `C:\Users\A\.hermes\config.yaml`, `C:\Users\A\.hermes\.env`, and the
   active launcher under `H:\Hermes_Windows_Native_014\launcher\`.
2. Set `auxiliary.vision.provider` to `google` and
   `auxiliary.vision.model` to `gemini-2.5-flash`.
3. Keep the key in `.env`; do not paste it into shared docs. Be aware that on
   the 2026-05-22 Hermes build, a configured `auxiliary.vision.base_url` can be
   re-passed as an explicit base URL inside `async_call_llm`, which may route
   the async vision call through the OpenAI-compatible custom path instead of
   Gemini native. If built-in `vision_analyze` reports `API_KEY_INVALID` while a
   direct Gemini native call succeeds, stop and use the standalone fallback
   rather than patching Hermes package code during a light restore.
4. Set proxy variables in the launcher before `Start-Process` starts
   `hermes.exe gateway run --replace`:
   `HTTPS_PROXY=http://127.0.0.1:7890`,
   `HTTP_PROXY=http://127.0.0.1:7890`,
   `ALL_PROXY=http://127.0.0.1:7890`.
5. Restart only the Windows native Hermes Gateway processes under
   `H:\Hermes_Windows_Native_014`; do not stop unrelated PowerShell sessions by
   broad command-line text matching.
6. Verify direct Gemini with a proxied request to
   `/v1beta/models/gemini-2.5-flash`.
7. Verify image reading with Hermes `vision_analyze`. If direct Gemini passes
   but Hermes `vision_analyze` fails, create or use a local standalone fallback
   under the task output directory and report `HERMES_STAGE05_GEMINI_STANDALONE_VISION_PASS`
   only after it returns a Chinese description for a local image.

## Rollback

- Restore backed-up `config.yaml`, `.env`, and launcher scripts from the task
  output backup directory.
- Restart only Hermes Gateway and verify:
  `http://127.0.0.1:8642/health` is 200 and
  `http://127.0.0.1:8642/v1/models` includes `hermes-agent`.
- Remove any task-local standalone fallback only if the user explicitly asks.
