# G02 Internal LLM Selftest Script

Status: `G02_PASS_SELFTEST_SCRIPT_READY`

Created:

- `C:\Users\A\xiaolongxia-free-api-local\scripts\xiaolongxia-nvidia-llm-selftest.ps1`
- `C:\Users\A\xiaolongxia-free-api-local\scripts\xiaolongxia-nvidia-llm-selftest.js`

Supported modes:

- `-ModelMode primary`: calls `meta/llama-3.1-8b-instruct`.
- `-ModelMode fallback`: calls `meta/llama-3.1-70b-instruct`.
- `-ModelMode auto`: calls 8B first, then 70B if primary fails.
- `-ModelMode auto -SimulatePrimaryFailure`: simulates primary failure in-process and verifies fallback to 70B.

Safety:

- Does not require Xiaolongxia UI.
- Does not connect group chat.
- Does not send messages.
- Reads NVIDIA key from local secret file only.
- Clears process `NVIDIA_API_KEY` after run.
- Writes JSON/Markdown evidence only under the task output directory.
