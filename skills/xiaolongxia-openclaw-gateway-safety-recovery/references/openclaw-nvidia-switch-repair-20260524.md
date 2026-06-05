# OpenClaw NVIDIA Switch Repair - 2026-05-24

## Status

`XIAOLONGXIA_OPENCLAW_NVIDIA_SWITCH_REPAIR_PASS`

## Incident

OpenClaw/Xiaolongxia visible web page showed `停止` and the session contained `assistant turn failed before producing content`.

Root cause:

- The visible session was still pinned to the old 3011/OpenRouter model-pool model alias `xiaolongxia-primary-temp`.
- 3011/OpenRouter fallback models were all failing with 403 pre-charge/balance errors.
- Fallback was not fully dead; it was falling back inside the exhausted 3011 pool. Cross-provider fallback to NVIDIA was missing from the active OpenClaw default route.

## Repair

Back up before editing:

- `C:\Users\A\.openclaw\openclaw.json`
- `C:\Users\A\.openclaw\agents\main\agent\models.json`

Set OpenClaw model route:

- Primary: `nvidia-nim/meta/llama-3.1-8b-instruct`
- Fallback: `nvidia-nim/meta/llama-3.1-70b-instruct`
- Secret source: local SecretRef/file only; do not write or print the NVIDIA key.

Restart gateway on loopback only:

```powershell
openclaw gateway run --force --allow-unconfigured --bind loopback --port 18789 --verbose
```

## Verification Evidence

Output root:

`C:\Users\A\Desktop\1\output\XIAOLONGXIA-OPENCLAW-INPROGRESS-STOP-REPAIR-20260524`

Key evidence:

- `G03-openclaw-config-validate.stdout.txt`
- `G04-openclaw-gateway-force-stdout.log`
- `G04-agent-nvidia8b-marker-rerun-summary.json`
- `G04-agent-nvidia70b-marker.stdout.json`
- `G04-auto-fallback-verified-summary.json`
- `G04-agent-default-after-restore-summary.json`
- `G04-openclaw-visible-window-after-refresh-crop.png`
- `final-report.md`

Verified markers:

- 8B marker: `XIAOLONGXIA_NVIDIA_SWITCH_REPAIR_8B_RERUN_OK`
- 70B marker: `XIAOLONGXIA_NVIDIA_SWITCH_REPAIR_70B_OK`
- Auto fallback marker: `XIAOLONGXIA_NVIDIA_AUTO_FALLBACK_70B_OK`
- Visible page marker: `XIAOLONGXIA_DEFAULT_AFTER_REPAIR_8B_OK`

## Lessons

- If the page shows `停止`, first inspect the selected model in the visible OpenClaw page.
- If the selector shows `xiaolongxia-primary-temp`, the page is using the old 3011/OpenRouter route.
- Do not treat repeated 3011 model fallback as a complete fallback solution when the whole pool is blocked by balance/pre-charge failures.
- Keep NVIDIA 8B/70B as a cross-provider route for Xiaolongxia when OpenRouter free/low-cost pool is exhausted.
- After route repair, take a full desktop screenshot, then a broad crop of the OpenClaw window. The accepted visible proof is the model selector showing `xiaolongxia-nvidia-8b...` plus an in-page marker reply.

## Safety

- Do not modify Hermes/AiMaShi.
- Do not modify Open WebUI.
- Do not modify old 3001.
- Do not modify 3011 model-pool config during this repair.
- Do not send real messages.
- Do not print API keys, tokens, passwords, or full secret values.
