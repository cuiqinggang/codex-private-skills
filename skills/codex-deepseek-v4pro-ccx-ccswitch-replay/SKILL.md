---
name: codex-deepseek-v4pro-ccx-ccswitch-replay
description: "Restore, repair, migrate, or verify the 2026-05-14 Windows Codex DeepSeek V4 Pro backup route via CCX/API Proxy and CC Switch."
---

# Codex DeepSeek V4 Pro Backup via CCX and CC Switch

Use this skill only to replay the proven 2026-05-14 Windows path:

DeepSeek official API -> CCX/API Proxy -> `http://localhost:13000/v1` -> CC Switch Codex provider -> Codex API-key provider -> `deepseek-v4-pro` -> `DEEPSEEK_V4PRO_CODEX_BACKUP_OK`.

## Trigger Phrases

Load this skill when the user asks:

- "閹垹顦?Codex DeepSeek V4 Pro 婢跺洨鏁ょ捄顖滃殠"
- "闁插秵鏌婇柊宥囩枂 Codex DeepSeek"
- "Codex 妫版繂瀹虫稉宥咁檮閿涘苯鍨?DeepSeek V4 Pro"
- "婢跺秶骞?CCX + CC Switch 閹?DeepSeek"
- "Codex DeepSeek V4 Pro 婢跺洨鏁ゅΟ鈥崇€锋穱顔碱槻"
- "閹?2026-05-14 閹存劕濮涘鍫滅伐閹垹顦?

## When To Use

- GPT/Codex quota is insufficient and the user wants a manual backup route.
- CCX needs to be reinstalled, restarted, or repaired.
- CC Switch provider needs to be recreated or verified.
- A new Windows machine needs the same backup route.
- The old backup route stopped working and needs layered diagnosis.

## When Not To Use

- Do not use this as the default daily GPT route.
- Do not replace default `model = "gpt-5.5"`.
- Do not configure or select DeepSeek Flash.
- Do not change or stop Open WebUI on port `3000`.
- Do not save, print, or report DeepSeek API keys.
- Do not point Codex directly at `https://api.deepseek.com` as the final route.

## Fixed Rules

- Default GPT-5.5 stays unchanged.
- DeepSeek V4 Pro is manual backup only.
- Only use `deepseek-v4-pro`.
- CCX uses `13000`; Open WebUI keeps `3000`.
- Backup before any config write.
- Verify before reporting success.
- If a required key, component, or compatibility layer is missing, stop with `SAFE_STOP_PASS`.
- If DeepSeek API key is needed and unavailable, output `NEED_DEEPSEEK_API_KEY` and stop.

## One-Line Recovery Strategy

First confirm the GPT default path is untouched, then start or repair CCX on `13000`, confirm the CC Switch backup provider, and test Codex with a temporary provider override; do not directly modify the default `gpt-5.5` config.

## Required References

- Read `references/success-case-20260514.md` for the known-good case.
- Read `references/replay-checklist.md` before reinstalling or repairing.
- Read `references/verification.md` before claiming success.
- Read `references/rollback.md` before changing existing config.
- Read `references/no-secret-policy.md` before handling any key.
- Read `references/troubleshooting.md` when a layer fails.

## Scripts

- `scripts/check-current-state.ps1`: read-only status check.
- `scripts/verify-deepseek-v4pro-backup.ps1`: CCX and optional Codex backup route verification.

## 2026-05-18 鏈€绲傛垚鍔熻矾绶氳鍏?

### 1. Codex 妗岄潰鍦栧舰鐗堜笉鍙敤

- Codex 妗岄潰鍦栧舰鐗堜粛鍙楀畼鏂归搴﹂檺鍒讹紝涓嶈兘浣滅偤 DeepSeek V4 Pro 鐨勫彲闈犲叆鍙ｃ€?
- 涓嶈鍐嶄娇鐢ㄦ闈㈢増鑸婃渻瑭遍€茶椹楄瓑銆?

### 2. 鏈€绲傝窇閫氱殑鎴愮啛璺窔

- 璺窔锛?*Codex CLI + 鐛ㄧ珛 CODEX_HOME + CCX localhost:13000/v1 + DeepSeek V4 Pro**銆?
- 涓嶈淇敼 Hermes/鎰涢Μ浠曘€?
- 涓嶈淇敼 Open WebUI銆?
- 涓嶈娣峰叆 DeepSeek Flash銆?
- 涓嶈鍦?C:\Windows\system32 鍋氶爡鐩€?
- 鐪熷浠诲嫏鍓嶅厛 cd 鍒伴爡鐩洰閷勩€?

### 3. 鎴愬姛璀夋摎

- `npx -y @openai/codex@latest --version` 杩斿洖 `codex-cli 0.130.0`
- model: `deepseek-v4-pro`
- provider: `ccx-deepseek-v4pro-backup`
- 鍥炶 `CODEX_DEEPSEEK_CLI_OK`
- Sandbox ready
- 鍥炶 `DEEPSEEK_SANDBOX_OK`
${REDACTED_SECRET}

### 4. 闂滈嵉姝ラ

1. 寰炶垔鎴愬姛妗堜緥 `.env` 灏庡叆 `CCX_PROXY_ACCESS_KEY`銆?
${REDACTED_SECRET}
3. 閰嶇疆 `wire_api = "responses"`銆?
4. 鐢?`CODEX_HOME` 鎸囧悜鐛ㄧ珛閰嶇疆鍟熷嫊 Codex CLI锛?

```powershell
${REDACTED_SECRET}
npx -y @openai/codex@latest
```

### 5. 娉ㄦ剰浜嬮爡

- 涓嶈鍐嶄娇鐢ㄦ闈㈢増鑸婃渻瑭遍璀夈€?
- 涓嶈淇敼 Hermes/鎰涢Μ浠曘€?
- 涓嶈淇敼 Open WebUI銆?
- 涓嶈娣峰叆 DeepSeek Flash銆?
- 涓嶈鍦?C:\Windows\system32 鍋氶爡鐩€?
- 鐪熷浠诲嫏鍓嶅厛 cd 鍒伴爡鐩洰閷勩€?

