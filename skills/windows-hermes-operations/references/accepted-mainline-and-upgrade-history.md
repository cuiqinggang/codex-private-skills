## 2026-06-07 Accepted Mainline And Autostart

For the current accepted Windows native Hermes + Open WebUI + Docker autostart
state, read
`references/incident-2026-06-07-g39-g44-openwebui-autostart.md` before changing
Hermes, Docker, Open WebUI, Telegram, or login autostart. It records the
G39-G44 pass state, the mistakes made during repair, and the correct gated
flow. On 2026-06-07 evening, the accepted autostart path was extended to recover
Docker Desktop when it is stuck in `starting` with lingering
`com.docker.backend.exe` processes or Docker API HTTP 500. The fix belongs in
${REDACTED_SECRET}
try normal Docker startup, then clear Docker Desktop residue, terminate only the
`docker-desktop` WSL distro, start Docker Desktop again, start
`open-webui-clean`, and open `http://127.0.0.1:3000`.

Do not treat Docker account/login UI as the success criterion. The success
criterion is the background chain: `docker ps` stable, `open-webui-clean` up,
Open WebUI `3000` reachable, existing logged-in Google Chrome can use
`hermes-agent`, and Telegram remains connected to Hermes `8642`.

For browser verification, use the user's already logged-in Google Chrome window.
Do not open a separate temporary Chromium/Playwright browser to claim success,
because it will not share the user's Open WebUI login/session state. HTTP 200 is
not sufficient by itself; verify the logged-in web UI or an authenticated
Open WebUI chat call, and prefer the user's own visible test as final acceptance
when they have just confirmed it works.

## 2026-06-08 Autostart Conflict Hardening

If the user says reboot/login autostart did not connect Hermes to the browser,
or that startup scripts may conflict with other programs, read
`references/incident-2026-06-08-autostart-conflict-hardening.md`. The accepted
fix adds a single-instance mutex, unique log names with PID, explicit opening
of the user's existing Google Chrome profile to `http://127.0.0.1:3000`, and a
Startup-folder VBS fallback:

```text
${REDACTED_SECRET}
```

The Task Scheduler task `Hermes_OpenWebUI_AutoStart` can remain installed, but
it may have power settings that cannot be changed without higher privileges.
The script-level mutex prevents the scheduled task and Startup VBS from
conflicting when both launch.

## 2026-07-03 C Drive Startup Runtime

If the user says K drive is only backup/reference and startup must use the SSD
C drive, read `references/incident-2026-07-03-k-path-openwebui-autostart.md`.
The accepted current launch root is:

```text
${REDACTED_SECRET}
```

K drive may retain a backup copy, but active login startup wrappers should use
C drive. The current 8642 model id is `Hermes-GLM-5.2-OpenRouter`; older
`hermes-agent` checks should be treated as compatibility only.

## 2026-07-06 Open WebUI Triple Tab Autostart

If the user says Hermes/Open WebUI login opens three browser tabs, three login
pages, or multiple parallel Open WebUI pages, read
`references/incident-2026-07-06-openwebui-triple-tab-autostart.md`.
The accepted repair keeps the C-drive primary autostart entry as the only
browser opener, disables the old Stage 04b `HermesOpenWebUIAutoOpen.vbs`
Startup entry, and makes `Hermes_NewAPI_AutoRecover.ps1` start Hermes with
`-StartBackendOnly -NoOpen` instead of calling `START-HERMES-WEBUI.cmd`.
Do not remove the gateway or Telegram persistence entries just to fix duplicate
browser tabs.

## 2026-07-13 Hermes 0.18.2 Upgrade

For upgrading the C-drive Windows runtime from 0.17.0 to the latest 0.18.x
release while preserving Telegram, Open WebUI, login autostart, and the browser
light-chat route, read
`references/incident-2026-07-13-hermes-0182-upgrade.md`. The accepted target is
0.18.2. Back up the profile and local API-server patch, upgrade the existing
venv in place, run `hermes config migrate` when `config check` reports an old
schema, reapply only the minimal light-chat patch, and accept the 0.18 hidden
${REDACTED_SECRET}
in the C-drive launcher. Final acceptance requires a real streaming marker,
the strict Telegram diagnostic, the autostart `FINAL_PASS`, and a screenshot of
the already logged-in Chrome Open WebUI page.

## 2026-06-08 Hermes 0.16.0 Upgrade Repair

If upgrading Hermes to 0.16.0, or if 8642 `/health` and `/v1/models` pass but
chat returns `No models provided`, HTTP 502, or logs stop writing under
${REDACTED_SECRET}
`references/incident-2026-06-08-hermes-0160-upgrade.md`. The accepted fix is:
backup `.env`, `config.yaml`, `state.db`, launchers, and pip freeze; upgrade
the venv with `python -m pip install --upgrade hermes-agent==0.16.0`; move old
`site-packages\~...` invalid distribution leftovers to the backup directory;
${REDACTED_SECRET}
starting the gateway. Also check
${REDACTED_SECRET}
${REDACTED_SECRET}
and run `gateway run --replace --accept-hooks`. Otherwise Open WebUI can show
an empty response because the gateway reads the wrong default profile under
${REDACTED_SECRET}

Do not trust bare `hermes config show` or `hermes config set` unless
`HERMES_HOME` is set in that shell. Without it, Hermes 0.16 may read/write the
${REDACTED_SECRET}
wrong-profile gateway. Success requires direct chat through 8642, Open WebUI
3000 opened in the existing Google Chrome profile, and Telegram state
connected.

## 0.15.2 Upgrade Repair

If Hermes upgrade gets stuck, `hermes.exe` exists but fails with
`ModuleNotFoundError: No module named 'hermes_cli.main'`, 8642 is down after an
upgrade, or `/v1/models` returns 401 after setting up Hermes 0.15.x, read
`references/incident-2026-06-01-hermes-0152-upgrade-repair.md` before changing
the venv or launcher. Hermes 0.15.2 requires `API_SERVER_KEY`; local launchers
and health checks must send `Authorization: Bearer <API_SERVER_KEY>` for
`/v1/models` and chat checks.

## Open WebUI 3000 Shows No Model Selected

If Telegram/mobile Hermes can answer through DeepSeek, but the web page
`http://127.0.0.1:3000` or
`http://127.0.0.1:3000/admin/settings/connections` says no large model is
connected or selected, read
`references/openwebui-direct-deepseek-20260605.md` before changing Open WebUI.
This is the direct chain:

```text
Open WebUI 3000 -> Hermes 8642 -> DeepSeek deepseek-v4-pro
```

Do not route this repair through old New API `3001`. The likely fixes are:
sync Open WebUI's saved key to Hermes `API_SERVER_KEY`, set the connection
`model_ids` to `hermes-agent`, set Open WebUI default models to `hermes-agent`,
and verify Hermes still defaults to `deepseek-v4-pro`.
