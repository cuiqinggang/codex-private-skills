# G01 Internal LLM Entry Inventory

Status: `G01_PASS_INTERNAL_LLM_ENTRY_FOUND`

## Scope

This is a read-only inventory plus minimal wrapper decision for Xiaolongxia internal LLM/provider selftest.

## Findings

- Xiaolongxia UI or real group-chat app is not required for this task.
- The active local project directory is `C:\Users\A\xiaolongxia-free-api-local`.
- Existing model-call scripts were found under `C:\Users\A\xiaolongxia-free-api-local\scripts`.
- Existing `simulate-xiaolongxia-chat-call.ps1` calls the 3011 OpenRouter/New API pool and is simulation-only.
- Existing `test-nvidia-draft-wire-in.ps1` calls the NVIDIA candidate route but is draft/review-queue oriented.
- No enabled WeChat/Feishu/Telegram sender was found in `xiaolongxia-free-api-local`.
- The correct internal LLM selftest entry for this task is a minimal provider wrapper in `scripts\xiaolongxia-nvidia-llm-selftest.ps1` plus `scripts\xiaolongxia-nvidia-llm-selftest.js`.

## Excluded Functions

- No real message sender is called.
- No UI is opened.
- No group connector is used.
- No review_queue path is used by this selftest.

## Internal LLM Entry

`C:\Users\A\xiaolongxia-free-api-local\scripts\xiaolongxia-nvidia-llm-selftest.ps1`

This wrapper accepts a prompt set through `-ModelMode`, calls the NVIDIA candidate route, returns local JSON/Markdown results, and records selected model plus fallback behavior.
