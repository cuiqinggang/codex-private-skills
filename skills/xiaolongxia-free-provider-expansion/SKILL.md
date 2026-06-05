---
name: xiaolongxia-free-provider-expansion
description: Use when expanding Xiaolongxia's isolated local free/low-cost model provider pool beyond the current OpenRouter 3011 production pool, especially NVIDIA NIM candidate testing, marker evidence, A/B/C ranking, OpenClaw candidate provider configs, and safe non-production dry-runs.
metadata:
  short-description: Xiaolongxia provider expansion candidates
---

# Xiaolongxia Free Provider Expansion

Use this skill when testing new upstream providers as candidates for Xiaolongxia. This is not the production route.

## Boundaries

- Do not modify Hermes / AiMaShi.
- Do not modify Open WebUI.
- Do not modify old `3001` New API.
- Do not replace the current `3011` OpenRouter reduced production pool.
- Do not connect real group chats.
- Do not write global long-term environment variables.
- Do not print or save API keys.
- Do not add untested models to the formal backup list.

## Browser And Autostart Safety Cross-Reference

The 2026-05-24 Xiaolongxia autostart attempt produced a serious isolation failure: `http://localhost:3011` was mistaken for the Xiaolongxia UI and Hermes/AiMaShi appeared when the user expected Xiaolongxia. For browser-open, autostart, OpenClaw gateway recovery, or wrong-page recovery tasks, use `xiaolongxia-openclaw-gateway-safety-recovery`.

Never treat `3011` as Xiaolongxia product UI. `3011` is New API/model-pool management. OpenClaw manual gateway/browser recovery uses `http://127.0.0.1:18789/` only after current health and identity checks.

Before later Xiaolongxia/OpenClaw/browser recovery tasks, first run `G00-NewAPI-Start-And-Login`: independently confirm `http://127.0.0.1:3011` can open, log in, and show a New API backend page, then record `3011_CONFIRMED_AS_NEW_API_NOT_XIAOLONGXIA_UI`. If New API login is not confirmed, stop with `STOP_NEWAPI_LOGIN_NOT_CONFIRMED`.

Latest verified G00 savepoint:

- Status: `G00_NEWAPI_START_AND_LOGIN_PASS`
- Evidence root: `C:\Users\A\Desktop\1\output\XIAOLONGXIA-G00-NEWAPI-START-LOGIN-20260524`
- Admin username: `xya6338`
- Admin credential file: `C:\Users\A\xiaolongxia-free-api-local\secrets\newapi_admin_xya6338_login.txt`
- Confirmed channel page: `openrouter-free` in `xiaolongxia-free-pool`

Do not print the password from the credential file.

## Current Production Pool

Production stays on the OpenRouter reduced pool:

- Primary: `xiaolongxia-free/liquid/lfm-2.5-1.2b-instruct:free`
- Formal backups: `xiaolongxia-free/openai/gpt-oss-120b:free`, `xiaolongxia-free/openai/gpt-oss-20b:free`
- Final fallback: `xiaolongxia-free/openrouter/free`

## NVIDIA NIM Candidate Baseline

G07 result:

- Status: `NVIDIA_NIM_G07_CONNECT_PASS`
- Base URL: `https://integrate.api.nvidia.com/v1`
- Endpoint: `/chat/completions`
- Baseline model: `meta/llama-3.1-8b-instruct`
- HTTP status: `200`
- Note: PowerShell may display Chinese response text as mojibake; that is a terminal display issue, not necessarily an API failure.

The NVIDIA API key was exposed in chat during setup. For formal integration, prefer rotating it before production use. For the 2026-05-23 dry-run, the user explicitly allowed continuing with the current key, used only in the current PowerShell process and not written to reports, skills, or long-term environment variables.

## G08 Marker Test Method

Use one non-streaming request per model:

```powershell
POST https://integrate.api.nvidia.com/v1/chat/completions
Authorization: Bearer <NVIDIA_API_KEY>
Content-Type: application/json
```

Common body:

```json
{
  "model": "<model-id>",
  "messages": [
    { "role": "user", "content": "Return exactly this marker and nothing else: <MARKER>" }
  ],
  "temperature": 0,
  "max_tokens": 120,
  "stream": false
}
```

Do not print the key. Space requests by 2-3 seconds.

## G09 Ranking Rules

A class:

- HTTP 200.
- marker passed.
- latency acceptable.
- no 401 / 403 / 404.
- no serious 429.

B class:

- HTTP 200 but marker unstable.
- latency high.
- model available but Chinese/group-chat quality unknown.
- needs second test.

C class:

- 404 / 410 model not found or unavailable.
- 401 / 403 permission issue.
- serious 429.
- empty reply.
- not compatible with chat completions.

## Latest NVIDIA Candidate Evidence

Output root:

`C:\Users\A\Desktop\1\output\XIAOLONGXIA-NVIDIA-NIM-G08-G09-CANDIDATE-20260523`

Bundled evidence copy:

`references\nvidia-nim-g08-g13-20260523`

Status:

`XIAOLONGXIA_NVIDIA_NIM_CANDIDATE_CONFIG_PASS`

A class candidate models:

- `meta/llama-3.1-8b-instruct`
- `nvidia/nemotron-3-super-120b-a12b`
- `meta/llama-3.1-70b-instruct`

C class in this run:

- `moonshotai/kimi-k2.5`
- `minimaxai/minimax-m2.5`
- `z-ai/glm5`

## Candidate OpenClaw Config Rule

Generate only candidate files under an output directory. Do not overwrite `C:\Users\A\.openclaw\openclaw.json`.

Provider:

- id: `nvidia`
- base URL: `https://integrate.api.nvidia.com/v1`
- api: `openai-completions`
- key source: `${NVIDIA_API_KEY}` or SecretRef from local file/env
- models: A class only

Before promoting NVIDIA to formal backup:

1. Same model passes marker tests in 3 consecutive rounds.
2. Chinese Q&A test passes.
3. Xiaolongxia-style short reply test passes.
4. No 401 / 403 / 404.
5. 429 is not severe.
6. Average latency is acceptable.
7. No key leak.
8. Rollback path exists.

If NVIDIA fails or rate-limits, fall back to the current OpenRouter reduced pool.

## Bundled Runbook And Artifacts

This skill now carries the full G08-G13 savepoint for reuse:

- `references\nvidia-nim-g08-g13-20260523\G08-nvidia-marker-tests.md`
- `references\nvidia-nim-g08-g13-20260523\G08-nvidia-marker-tests.json`
- `references\nvidia-nim-g08-g13-20260523\G09-nvidia-candidate-ranking.md`
- `references\nvidia-nim-g08-g13-20260523\G10-candidate-config-summary.md`
- `references\nvidia-nim-g08-g13-20260523\G11-free-pool-two-layer-strategy.md`
- `references\nvidia-nim-g08-g13-20260523\final-report.md`
- `references\nvidia-nim-g08-g13-20260523\candidate-config\nvidia-provider-candidate.json`
- `references\nvidia-nim-g08-g13-20260523\candidate-config\nvidia-provider-candidate-notes.md`
- `references\nvidia-nim-g08-g13-20260523\candidate-config\nvidia-openclaw-rollback.md`

Reusable marker retest script:

`scripts\test-nvidia-nim-candidates.ps1`

Run it only after setting `NVIDIA_API_KEY` in the current PowerShell process or placing the key in the local secret file. Do not write a global long-term environment variable and do not print the key.

```powershell
$env:NVIDIA_API_KEY = "<key for this PowerShell process only>"
C:\Users\A\.codex\skills\xiaolongxia-free-provider-expansion\scripts\test-nvidia-nim-candidates.ps1
```

The script writes UTF-8 JSON and Markdown, redacts any accidental `nvapi-*` text from error summaries, and does not write global environment variables.

## Stability Dry-run Gate

The 2026-05-23 stability dry-run completed after the user explicitly allowed using the current key process-scoped for this one test.

Final status:

`XIAOLONGXIA_NVIDIA_NIM_STABILITY_DRYRUN_PASS`

Bundled evidence:

- `references\nvidia-nim-stability-dryrun-20260523\G14-precheck.md`
- `references\nvidia-nim-stability-dryrun-20260523\G15-stability-marker-tests.md`
- `references\nvidia-nim-stability-dryrun-20260523\G15-stability-marker-tests.json`
- `references\nvidia-nim-stability-dryrun-20260523\G16-chinese-qa-dryrun.md`
- `references\nvidia-nim-stability-dryrun-20260523\G16-chinese-qa-dryrun.json`
- `references\nvidia-nim-stability-dryrun-20260523\G17-xiaolongxia-style-dryrun.md`
- `references\nvidia-nim-stability-dryrun-20260523\G17-xiaolongxia-style-dryrun.json`
- `references\nvidia-nim-stability-dryrun-20260523\G18-nvidia-final-dryrun-ranking.md`
- `references\nvidia-nim-stability-dryrun-20260523\G18-nvidia-final-dryrun-ranking.json`
- `references\nvidia-nim-stability-dryrun-20260523\run-nvidia-stability-dryrun.js`

Result summary:

| Model | Marker | Chinese QA | Xiaolongxia style | Average latency | Tier |
| --- | --- | --- | --- | ---: | --- |
| `meta/llama-3.1-8b-instruct` | 3/3 | 3/3 A/B | 3/3 A/B | 738 ms | A+ |
| `meta/llama-3.1-70b-instruct` | 3/3 | 3/3 A/B | 2/3 A/B | 6631 ms | A+ |
| `nvidia/nemotron-3-super-120b-a12b` | 2/3 | 0/3 A/B | 0/3 A/B | 13263 ms | C |

Updated NVIDIA dry-run recommendation:

- Next OpenClaw dry-run primary candidate: `meta/llama-3.1-8b-instruct`.
- Next OpenClaw dry-run backup candidate: `meta/llama-3.1-70b-instruct`.
- Do not continue `nvidia/nemotron-3-super-120b-a12b` for Xiaolongxia group-chat replies in its current prompt form. It often emits English reasoning/instruction text and is too slow for this use case.

Important interpretation notes:

- `G15-stability-marker-tests.json`, `G16-chinese-qa-dryrun.json`, `G17-xiaolongxia-style-dryrun.json`, and `G18-nvidia-final-dryrun-ranking.json` are valid UTF-8 JSON and were verified with Node `JSON.parse`.
- Windows PowerShell may display UTF-8 Chinese as mojibake when reading these files. Treat that as a display-layer issue unless Node parsing or browser/file viewer verification fails.
- No production OpenClaw/OpenRouter configuration was changed.
- No real group chat was connected.
- No full API key was written to the evidence files or skill.

Promotion gate from candidate to formal backup:

1. Run one OpenClaw route dry-run using `meta/llama-3.1-8b-instruct` as NVIDIA primary and `meta/llama-3.1-70b-instruct` as NVIDIA backup.
2. Confirm fallback remains at the Xiaolongxia application or message-adapter layer unless OpenClaw fallback is proven.
3. Keep current OpenRouter 3011 production pool unchanged until NVIDIA route dry-run passes.
4. Keep real group chat disconnected until a separate low-risk message-entry test passes.

## OpenClaw NVIDIA Candidate Route Dry-run

The 2026-05-23 OpenClaw NVIDIA candidate route dry-run completed without changing production config.

Final status:

`XIAOLONGXIA_OPENCLAW_NVIDIA_ROUTE_DRYRUN_PASS`

Bundled evidence:

- `references\openclaw-nvidia-route-dryrun-20260523\G21-precheck.md`
- `references\openclaw-nvidia-route-dryrun-20260523\G21-precheck.json`
- `references\openclaw-nvidia-route-dryrun-20260523\G22-candidate-route-config.md`
- `references\openclaw-nvidia-route-dryrun-20260523\candidate-config\openclaw-nvidia-nim-dryrun.json`
- `references\openclaw-nvidia-route-dryrun-20260523\candidate-config\openclaw-nvidia-nim-dryrun-notes.md`
- `references\openclaw-nvidia-route-dryrun-20260523\candidate-config\openclaw-nvidia-nim-dryrun-rollback.md`
- `references\openclaw-nvidia-route-dryrun-20260523\G23-static-validation.md`
- `references\openclaw-nvidia-route-dryrun-20260523\G24-openclaw-route-dryrun.md`
- `references\openclaw-nvidia-route-dryrun-20260523\G24-openclaw-route-dryrun.json`
- `references\openclaw-nvidia-route-dryrun-20260523\G25-xiaolongxia-reply-template-dryrun.md`
- `references\openclaw-nvidia-route-dryrun-20260523\G25-xiaolongxia-reply-template-dryrun.json`
- `references\openclaw-nvidia-route-dryrun-20260523\G26-production-diff-check.md`
- `references\openclaw-nvidia-route-dryrun-20260523\G26-production-diff-check.json`
- `references\openclaw-nvidia-route-dryrun-20260523\run-openclaw-nvidia-route-dryrun.js`

Candidate route:

- Route name: `xiaolongxia-nvidia-nim-dryrun`
- Provider id: `nvidia-nim-dryrun`
- Base URL: `https://integrate.api.nvidia.com/v1`
- Key source: `NVIDIA_API_KEY`, injected only in the dry-run process from `C:\Users\A\xiaolongxia-free-api-local\secrets\nvidia_api_key.txt`
- Primary: `meta/llama-3.1-8b-instruct`
- Fallback: `meta/llama-3.1-70b-instruct`
- Excluded: `nvidia/nemotron-3-super-120b-a12b`

Route test result:

| Model | Marker | HTTP | Latency |
| --- | --- | ---: | ---: |
| `meta/llama-3.1-8b-instruct` | pass | 200 | 654 ms |
| `meta/llama-3.1-70b-instruct` | pass | 200 | 1245 ms |

Xiaolongxia style dry-run result:

- Status: `G25_PASS_XIAOLONGXIA_ROUTE_STYLE_DRYRUN`
- Usable replies: 5/5
- Primary `meta/llama-3.1-8b-instruct` handled all five style prompts.
- The dry-run script now explicitly tells the model that Xiaolongxia is an AI learning service name, not a seafood/animal topic.
- The evaluation rejects model/API leaks, false promises, product-name confusion, and unverified channel/pricing claims such as first-week free, renewal, app download, WeChat, website, or 24-hour claims.

Production unchanged evidence:

- `G26_PASS_PRODUCTION_UNCHANGED`
- OpenClaw config hash unchanged.
- 3011 compose and env hashes unchanged.
- 3011 production model list hash unchanged; model count remained 19.
- `openclaw config validate` passed after the dry-run.
- No real group chat was connected.
- No full key pattern was found in output, local skill, or H mirror.

Next stage condition:

Only after this savepoint, the next reasonable step is a "shadow test" using the candidate route behind a local adapter. It must still avoid real group posting, keep 3011 OpenRouter production unchanged, and log fallback behavior before any real message-entry test.

## NVIDIA Shadow Test Local Draft

The 2026-05-24 local shadow test completed without real group sending.

Final status:

`XIAOLONGXIA_NVIDIA_SHADOW_TEST_LOCAL_DRAFT_PASS`

Definition used:

`local simulated parent-group messages -> NVIDIA candidate route -> local draft reply JSON/Markdown -> human review`

Bundled evidence:

- `references\nvidia-shadow-test-local-draft-20260523\G29-precheck.md`
- `references\nvidia-shadow-test-local-draft-20260523\G29-precheck.json`
- `references\nvidia-shadow-test-local-draft-20260523\shadow-input\simulated-parent-group-messages.json`
- `references\nvidia-shadow-test-local-draft-20260523\G30-shadow-input-dataset.md`
- `references\nvidia-shadow-test-local-draft-20260523\G31-shadow-generated-drafts.md`
- `references\nvidia-shadow-test-local-draft-20260523\G31-shadow-generated-drafts.json`
- `references\nvidia-shadow-test-local-draft-20260523\G32-shadow-draft-quality-review.md`
- `references\nvidia-shadow-test-local-draft-20260523\G32-shadow-draft-quality-review.json`
- `references\nvidia-shadow-test-local-draft-20260523\G33-shadow-failure-fix-suggestions.md`
- `references\nvidia-shadow-test-local-draft-20260523\candidate-config\xiaolongxia-shadow-reply-rules.md`
- `references\nvidia-shadow-test-local-draft-20260523\candidate-config\xiaolongxia-shadow-reply-rules.json`
- `references\nvidia-shadow-test-local-draft-20260523\G35-production-diff-check.md`
- `references\nvidia-shadow-test-local-draft-20260523\G35-production-diff-check.json`
- `references\nvidia-shadow-test-local-draft-20260523\run-xiaolongxia-nvidia-shadow-test.js`

Shadow test result:

- Simulated messages: 12.
- Drafts generated: 12/12.
- Primary model used: `meta/llama-3.1-8b-instruct`.
- Fallback model available: `meta/llama-3.1-70b-instruct`.
- Fallback usage in this run: 0.
- Drafts scoring >= 4: 11/12.
- Model/API/provider leaks: 0.
- False promises: 0.
- English reasoning traces: 0.
- Garbled-text flag: 0.
- Real sends: 0.

One low-score sample:

- `SIM-007` phone-use question.
- Reason: it contained an unconfirmed channel/availability claim.
- Rule impact: future prompts must avoid saying APP, download, WeChat, website, phone version, 24-hour, first-week free, paid subscription, price, or renewal unless those facts are confirmed.

Current shadow reply rules:

- 60-120 Chinese characters.
- Human group-chat tone.
- Do not mention model/API/provider/NVIDIA/OpenAI/ChatGPT.
- Do not exaggerate or promise grade improvement.
- Do not auto-send.
- Human review is mandatory before any real group use.
- Low confidence output should become "suggest human reply".
- Sensitive topics should not be automatically answered.
- Learning replies should focus on explaining problems, improving writing, practice, and guided thinking.

Production unchanged evidence:

- `G35_PASS_PRODUCTION_UNCHANGED`.
- OpenClaw config hash unchanged.
- 3011 compose/env hashes unchanged.
- 3011 production model list hash unchanged.
- 3011 model count remained 19.
- No real send process risk after tightened check.
- `NVIDIA_API_KEY` was not left in the process environment.
- No full key pattern was found in output or skills.

Next stage condition:

The next stage is "human-review mode test": present drafts to the user for manual approval, still with no automatic sending and no real group connection. Do not proceed to real group entry until manual approval workflow and rollback logs are tested.

## NVIDIA Internal LLM Selftest

The 2026-05-24 internal LLM/provider selftest completed without opening Xiaolongxia UI and without sending messages.

Final status:

`XIAOLONGXIA_NVIDIA_INTERNAL_LLM_SELFTEST_100_PASS`

Definition used:

`Xiaolongxia internal LLM/provider wrapper -> NVIDIA candidate route -> 8B primary -> 70B fallback -> local JSON/Markdown evidence`

Selftest entry:

`C:\Users\A\xiaolongxia-free-api-local\scripts\xiaolongxia-nvidia-llm-selftest.ps1`

Supported modes:

- `-ModelMode primary`: calls `meta/llama-3.1-8b-instruct`.
- `-ModelMode fallback`: calls `meta/llama-3.1-70b-instruct`.
- `-ModelMode auto`: calls 8B first, then 70B if primary fails.
- `-ModelMode auto -SimulatePrimaryFailure`: simulates primary failure in the current test process and verifies fallback to 70B.

Bundled evidence:

- `references\nvidia-internal-llm-selftest-20260523\G01-internal-llm-entry-inventory.md`
- `references\nvidia-internal-llm-selftest-20260523\G02-internal-llm-selftest-script.md`
- `references\nvidia-internal-llm-selftest-20260523\G03-primary-8b-internal-selftest.md`
- `references\nvidia-internal-llm-selftest-20260523\G03-primary-8b-internal-selftest.json`
- `references\nvidia-internal-llm-selftest-20260523\G04-fallback-70b-internal-selftest.md`
- `references\nvidia-internal-llm-selftest-20260523\G04-fallback-70b-internal-selftest.json`
- `references\nvidia-internal-llm-selftest-20260523\G05-auto-switch-internal-selftest.md`
- `references\nvidia-internal-llm-selftest-20260523\G05-auto-switch-internal-selftest.json`
- `references\nvidia-internal-llm-selftest-20260523\G06-acceptance-check.md`
- `references\nvidia-internal-llm-selftest-20260523\G06-acceptance-check.json`
- `references\nvidia-internal-llm-selftest-20260523\baseline-lock-report.md`
- `references\nvidia-internal-llm-selftest-20260523\xiaolongxia-nvidia-llm-selftest.ps1`
- `references\nvidia-internal-llm-selftest-20260523\xiaolongxia-nvidia-llm-selftest.js`

Results:

- Xiaolongxia UI required: no.
- 8B primary internal selftest: 5/5 passed.
- 70B fallback internal selftest: 3/3 passed.
- Auto normal mode: passed, selected 8B.
- Auto forced-primary-failure mode: passed, switched to 70B.
- Real sends: 0.
- Model/API/provider leaks: 0.
- False promises or unconfirmed app/website/WeChat/price/renewal claims: 0.
- 3011 OpenRouter production pool unchanged; model count remained 19.
- OpenClaw production config unchanged and `openclaw config validate` passed.
- NVIDIA key was not printed, not written to reports/scripts/skill, and `NVIDIA_API_KEY` was not left in the environment.

Operational note:

This selftest is not UI testing, group-chat testing, message sending, human review, or review queue testing. It is the current mature local proof that Xiaolongxia's internal LLM/provider layer can call NVIDIA 8B/70B and can switch from 8B to 70B when the primary path fails.

Baseline lock:

- Baseline report: `references\nvidia-internal-llm-selftest-20260523\baseline-lock-report.md`
- Lock status: `BASELINE_LOCKED`
- Locked conclusion: Xiaolongxia NVIDIA internal LLM primary/fallback switching is 100% passed as of this savepoint.
- Mandatory reuse rule: any later real-entry integration must reuse `C:\Users\A\xiaolongxia-free-api-local\scripts\xiaolongxia-nvidia-llm-selftest.ps1` and this `xiaolongxia-free-provider-expansion` skill before proceeding.
- Future real-entry gate: rerun `-ModelMode primary`, `-ModelMode fallback`, `-ModelMode auto`, and `-ModelMode auto -SimulatePrimaryFailure`; proceed only if all remain passing and no real send, key leak, production config change, or unconfirmed claim appears.

## 2026-05-24 OpenClaw Route Repair Savepoint

Status:

`XIAOLONGXIA_OPENCLAW_NVIDIA_SWITCH_REPAIR_PASS`

The OpenClaw visible page failed after the 3011/OpenRouter pool returned repeated 403 pre-charge/balance errors. The old fallback chain rotated inside the exhausted 3011 pool and did not provide a useful cross-provider fallback.

The active OpenClaw route was repaired to:

- Primary: `nvidia-nim/meta/llama-3.1-8b-instruct`
- Fallback: `nvidia-nim/meta/llama-3.1-70b-instruct`

Required evidence files are under:

`C:\Users\A\Desktop\1\output\XIAOLONGXIA-OPENCLAW-INPROGRESS-STOP-REPAIR-20260524`

Key results:

- 8B OpenClaw marker passed: `XIAOLONGXIA_NVIDIA_SWITCH_REPAIR_8B_RERUN_OK`.
- 70B OpenClaw marker passed: `XIAOLONGXIA_NVIDIA_SWITCH_REPAIR_70B_OK`.
- Cross-provider fallback passed: `XIAOLONGXIA_NVIDIA_AUTO_FALLBACK_70B_OK`.
- Default restored to 8B and visible page marker passed: `XIAOLONGXIA_DEFAULT_AFTER_REPAIR_8B_OK`.

Operational rule:

If 3011/OpenRouter quota or balance fails, switch Xiaolongxia/OpenClaw to the NVIDIA 8B/70B route rather than retrying multiple exhausted 3011 free models.

## 2026-05-24 User Preference Update: Default To NVIDIA 70B

Status:

`XIAOLONGXIA_DEFAULT_MODEL_SWITCHED_TO_NVIDIA_70B_PASS`

The user rejected `meta/llama-3.1-8b-instruct` as too weak for Xiaolongxia's visible answers. The active OpenClaw default route was changed to:

- Primary: `nvidia-nim/meta/llama-3.1-70b-instruct`
- Fallbacks: none

Do not automatically fall back to 8B unless the user explicitly asks for a speed/cost-saving mode.

Evidence root:

`C:\Users\A\Desktop\1\output\XIAOLONGXIA-SWITCH-TO-70B-20260524`

Key evidence:

- `G01-current-model-summary.json`: before switch was 8B primary + 70B fallback.
- `G04-70b-primary-no-8b-fallback-summary.json`: after switch is 70B primary with empty fallback list.
- `G05-gateway-70b-only-restart-summary.json`: gateway log confirms `agent model: nvidia-nim/meta/llama-3.1-70b-instruct`.
- `G06-default-70b-quality-test-summary.json`: default model call returned from `meta/llama-3.1-70b-instruct`.
- `G07-visible-70b-session-crop.png`: visible Chrome/OpenClaw page shows `xiaolongxia-nvidia-70...`.

Future stronger free/low-cost models can be added only after the candidate test ladder: marker, Chinese QA, Xiaolongxia style, stability, and error-handling tests. Do not put untested models into the formal fallback list.

## 2026-05-24 Current Active Route: DeepSeek V4 Flash Direct

Status:

`XIAOLONGXIA_DEEPSEEK_DIRECT_WIRE_IN_PASS`

The user rejected continuing with NVIDIA 70B as the active route because it was too slow in visible use. The user then chose the paid official DeepSeek V4 Flash route because it is cheap enough and much faster in local testing.

Current active Xiaolongxia LLM route:

```text
Xiaolongxia internal LLM/provider wrapper
  -> DeepSeek official API
  -> deepseek-v4-flash
```

Active provider:

- Provider id: `deepseek-official-direct`
- Base URL: `https://api.deepseek.com`
- Chat endpoint: `https://api.deepseek.com/chat/completions`
- Model: `deepseek-v4-flash`
- Secret file: `C:\Users\A\xiaolongxia-free-api-local\secrets\deepseek_api_key.txt`
- Thinking mode: disabled with `thinking: { "type": "disabled" }`

Runtime fallback rule:

- No active fallback models.
- Do not keep NVIDIA 70B as runtime fallback unless the user explicitly re-enables it.
- Do not keep OpenRouter free models as runtime fallback.
- Old OpenRouter free-pool and NVIDIA tests are preserved as historical evidence only.

Important implementation note:

Direct DeepSeek API testing showed that DeepSeek V4 Flash can return HTTP 200 with empty `content` if thinking mode is left enabled and the token budget is consumed by hidden reasoning. For Xiaolongxia short replies, always send:

```json
{
  "thinking": {
    "type": "disabled"
  }
}
```

Direct selftest:

- Script: `C:\Users\A\xiaolongxia-free-api-local\scripts\xiaolongxia-deepseek-v4-flash-direct-selftest.ps1`
- Bundled script copy: `scripts\xiaolongxia-deepseek-v4-flash-direct-selftest.ps1`
- Evidence root: `C:\Users\A\Desktop\1\output\XIAOLONGXIA-DEEPSEEK-DIRECT-WIRE-IN-20260524`
- Bundled evidence: `references\deepseek-direct-wire-in-20260524`
- Final simple test accepted by user: 2/2 passed.
- Average latency in the final simple test: 2003 ms.
- Earlier full local style test also passed before the final simplified route was chosen, but the current operational check is the quick direct selftest.
- `3011` New API used: false.
- OpenRouter used: false.
- OpenClaw `18789` `/v1` proxy used: false.
- Real sends: 0.
- Key printed: false.

Config savepoints:

- Active provider JSON: `C:\Users\A\xiaolongxia-free-api-local\config\xiaolongxia-active-llm-provider.json`
- Policy doc: `C:\Users\A\xiaolongxia-free-api-local\config\xiaolongxia-deepseek-direct-policy.md`

Operational rule from this savepoint:

Use DeepSeek V4 Flash official direct as the only current active Xiaolongxia model. Treat all previous free-model/NVIDIA work as background history unless the user explicitly asks to re-enable a backup route.

Identity correction:

- If Xiaolongxia says it is GPT-4o, treat that as an identity prompt/hallucination issue, not proof of the actual model route.
- Verified after the incident: OpenClaw had `deepseek-official/deepseek-v4-flash` as primary and empty fallbacks; gateway logs showed `provider=deepseek-official model=deepseek-v4-flash thinking=off`.
- Recommended wording: `我是小龙虾，本地当前使用 DeepSeek 官方 deepseek-v4-flash。不是 GPT-4o。`

Reusable quick command:

```powershell
C:\Users\A\xiaolongxia-free-api-local\scripts\xiaolongxia-deepseek-v4-flash-direct-selftest.ps1 -Mode quick
```

## 2026-05-25 OpenClaw DeepSeek V4 Flash Active Config

Status:

`XIAOLONGXIA_DEEPSEEK_V4_FLASH_OPENCLAW_CONNECT_PASS`

The user asked to connect only the official DeepSeek V4 Flash model and remove runtime backups. The current OpenClaw route is:

```text
OpenClaw / Xiaolongxia gateway 18789
  -> provider deepseek-official
  -> model deepseek-v4-flash
```

Current config:

- OpenClaw config: `C:\Users\A\.openclaw\openclaw.json`
- Secret file: `C:\Users\A\xiaolongxia-free-api-local\secrets\deepseek_api_key.txt`
- Primary model: `deepseek-official/deepseek-v4-flash`
- Runtime fallback count: `0`
- Provider list: `deepseek-official` only
- Model list: `deepseek-v4-flash` only
- `models.mode`: `replace`
- Telegram/channel sending: disabled
- Plain API key in config: false

Evidence root:

`C:\Users\A\Desktop\1\output\XIAOLONGXIA-DEEPSEEK-V4-FLASH-OPENCLAW-CONNECT-20260525`

Detailed repair record:

`references\deepseek-v4-flash-openclaw-repair-20260525.md`

Verification evidence:

- `G01-config-state.json`: single DeepSeek provider, no fallbacks, no plaintext key.
- `G01-openclaw-config-validate.stdout.txt`: `Config valid: ~\.openclaw\openclaw.json`.
- `G02-gateway-start-summary.json`: gateway 18789 started and listened on loopback.
- `G03-gateway-health.json`: `ok: true`, root title `OpenClaw Control`.
- `G03-infer-local-summary.json`: `openclaw infer model run --local` returned marker.
- `G03-infer-gateway-summary.json`: `openclaw infer model run --gateway` returned marker.
- `G03-openclaw-agent-main-summary.json`: `openclaw agent --agent main` returned marker through the active DeepSeek model.
- `G03-final-config-summary.json`: primary `deepseek-official/deepseek-v4-flash`, fallback count `0`, provider ids only `deepseek-official`.

Known nuance:

- `/v1/chat/completions` with model `openclaw/main` can enter the embedded agent path but return `No response from OpenClaw` when the agent produces `NO_REPLY`; do not use that as the main acceptance path for Xiaolongxia browser/chat verification.
- The accepted verification paths are `openclaw infer model run --gateway` for provider transport and `openclaw agent --agent main --message ...` for OpenClaw/Xiaolongxia agent behavior.
- If the visible page says it is GPT-4o, treat it as a prompt identity issue. Verify actual routing from config, gateway logs, or the commands above.
- Actual-use retest showed an important distinction: DeepSeek official direct selftest was fast, but OpenClaw gateway/agent/browser path could take about `70-180 s`. Treat that as connected but not practical until a real Chinese prompt returns within an acceptable latency window.
- Do not claim browser/page readiness from marker success alone. Use direct provider test, OpenClaw transport test, and practical-use latency test as separate gates.

Actual-use retest evidence:

`C:\Users\A\Desktop\1\output\XIAOLONGXIA-DEEPSEEK-V4-FLASH-ACTUAL-USE-TEST-20260525`

Bundled actual-use evidence:

`references\deepseek-v4-flash-actual-use-20260525`

Saved repair reference:

`references\deepseek-v4-flash-openclaw-repair-20260525.md`

Fast replay commands:

```powershell
C:\Users\A\AppData\Roaming\npm\openclaw.cmd infer model run --gateway --model "deepseek-official/deepseek-v4-flash" --prompt "请只回复：XLX_DEEPSEEK_INFER_GATEWAY_OK" --json
C:\Users\A\AppData\Roaming\npm\openclaw.cmd agent --agent main --message "请只回复：XLX_DEEPSEEK_AGENT_MAIN_OK" --model "deepseek-official/deepseek-v4-flash" --thinking off --timeout 180 --json
C:\Users\A\xiaolongxia-free-api-local\scripts\xiaolongxia-deepseek-v4-flash-direct-selftest.ps1 -Mode quick
```
