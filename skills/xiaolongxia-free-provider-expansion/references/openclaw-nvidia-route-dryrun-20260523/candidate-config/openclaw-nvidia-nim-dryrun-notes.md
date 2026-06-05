# OpenClaw NVIDIA NIM Dry-run Notes

This is a candidate route only. It does not overwrite production OpenClaw config and does not connect real group chat.

- Route name: `xiaolongxia-nvidia-nim-dryrun`
- Provider id: `nvidia-nim-dryrun`
- Base URL: `https://integrate.api.nvidia.com/v1`
- Key source: `NVIDIA_API_KEY`, injected from the local secret file into the current dry-run process only.
- Primary: `meta/llama-3.1-8b-instruct`
- Fallback: `meta/llama-3.1-70b-instruct`
- Current 3011 OpenRouter production pool remains unchanged.
- A previously tested C-class high-latency model is intentionally excluded from this candidate route.
