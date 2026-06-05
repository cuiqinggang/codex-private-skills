# Xiaolongxia NVIDIA Internal LLM Baseline Lock

Generated: 2026-05-24

Status: `BASELINE_LOCKED`

## Locked Conclusion

截至当前，小龙虾 NVIDIA 内部 LLM 主备切换能力已 100% 通过。

后续任何真实入口接入，都必须复用这个 selftest 脚本和技能包。

## Locked Evidence

- Final selftest status: `XIAOLONGXIA_NVIDIA_INTERNAL_LLM_SELFTEST_100_PASS`
- 8B primary model: `meta/llama-3.1-8b-instruct`
- 8B result: 5/5 passed
- 70B fallback model: `meta/llama-3.1-70b-instruct`
- 70B result: 3/3 passed
- Auto normal mode: passed, selected 8B
- Auto forced-primary-failure mode: passed, switched to 70B
- Real sends: 0
- Model/API/provider leaks: 0
- False promises or unconfirmed app/website/WeChat/price/renewal claims: 0
- 3011 OpenRouter production pool: unchanged
- OpenClaw production config: unchanged
- NVIDIA key: not printed, not written, not left in environment

## Mandatory Reuse Rule

Any later Xiaolongxia real-entry integration must start from this baseline and must reuse:

- Selftest script: `C:\Users\A\xiaolongxia-free-api-local\scripts\xiaolongxia-nvidia-llm-selftest.ps1`
- Provider/client script: `C:\Users\A\xiaolongxia-free-api-local\scripts\xiaolongxia-nvidia-llm-selftest.js`
- Local skill: `C:\Users\A\.codex\skills\xiaolongxia-free-provider-expansion`
- H mirror skill: `H:\CodexSkills\xiaolongxia-free-provider-expansion`
- Baseline evidence folder: `C:\Users\A\Desktop\1\output\XIAOLONGXIA-NVIDIA-INTERNAL-LLM-SELFTEST-20260523`

## Gate For Future Real Entry

Before connecting any real Xiaolongxia entry, the implementer must rerun the baseline selftest:

```powershell
Set-Location -LiteralPath 'C:\Users\A\xiaolongxia-free-api-local'
.\scripts\xiaolongxia-nvidia-llm-selftest.ps1 -ModelMode primary
.\scripts\xiaolongxia-nvidia-llm-selftest.ps1 -ModelMode fallback
.\scripts\xiaolongxia-nvidia-llm-selftest.ps1 -ModelMode auto
.\scripts\xiaolongxia-nvidia-llm-selftest.ps1 -ModelMode auto -SimulatePrimaryFailure
```

Proceed only if all remain true:

- 8B primary is 5/5.
- 70B fallback is 3/3.
- Auto normal selects 8B.
- Auto forced failure switches to 70B.
- Real sends remain 0 during test.
- No key, model/API/provider leak, false promise, or unconfirmed channel/price claim appears.
- 3011 OpenRouter production pool remains unchanged.
- OpenClaw production config remains unchanged unless a later task explicitly gates and approves a config change.

## Boundary

This baseline lock does not authorize:

- opening real group chats,
- sending messages,
- enabling automatic replies,
- changing 3011 production pool,
- changing OpenClaw production defaults,
- changing Hermes / AiMaShi,
- changing Open WebUI,
- changing old 3001 New API,
- writing or printing secrets.

## Baseline Lock Statement

This report is the current baseline lock for Xiaolongxia NVIDIA internal LLM primary/fallback switching. Future work must not bypass it or replace it with unverified assumptions.
