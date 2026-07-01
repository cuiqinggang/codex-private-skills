# Troubleshooting

## 3000 Is Occupied

Cause: Docker Open WebUI uses `localhost:3000`.

Fix: do not stop Open WebUI and do not take port `3000`. Configure CCX to use `13000`; if unavailable use `13001` or `13002`.

## CC Switch Portable Zip Cannot Run

Cause: the portable zip may be valid but rejected by Windows with "This app cannot run on your PC".

Fix: download the official v3.14.1 MSI and extract without installing:

```powershell
msiexec.exe /a "CC-Switch-v3.14.1-Windows.msi" /qn TARGETDIR="<extract-dir>"
```

Run the extracted executable under `Programs\CC Switch\cc-switch.exe`.

## DeepSeek Models List Shows Flash And Pro

Cause: DeepSeek `/v1/models` may list multiple models.

Fix: configure only `deepseek-v4-pro` in the CCX channel and CC Switch provider. Do not add or select DeepSeek Flash.

## Codex Enter API Key Is Confusing

Do not enter the DeepSeek official API key in Codex.

Codex `Enter API key` uses the CCX proxy access key. CCX stores the DeepSeek official key locally and translates the request.

## Direct DeepSeek URL Fails

Directly pointing Codex at `https://api.deepseek.com` can fail because Codex expects Responses-compatible behavior.

Use CCX `/v1/responses` through `http://localhost:13000/v1`.

## DeepSeek Key Missing

If the DeepSeek official key is not already available:

```text
NEED_DEEPSEEK_API_KEY
```

Stop. Do not create partial config that pretends to work.

## Verification Fails

Diagnose by layer:

1. DeepSeek upstream: key, quota, base URL, upstream model.
2. CCX: process, port, `.env`, Responses channel, proxy access key.
3. CC Switch: provider exists, backup-only, API URL, model, auth.
4. Codex temporary provider: `base_url`, `wire_api`, `env_key`, model.
5. Network: DNS, proxy, firewall, GitHub or DeepSeek reachability.

Fix only the failing layer and rerun verification.
