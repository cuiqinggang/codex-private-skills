# UltraFusion 6.1B Official Site URLs and Test Command

Date: 2026-07-02

## Official site URLs

Use only these test entrances:

- GPT / ChatGPT: https://chatgpt.com/
- DeepSeek Chat: https://chat.deepseek.com/
- Qianwen Chinese site: https://www.qianwen.com/
- Qwen Chat international backup: https://chat.qwen.ai/

Priority:

1. GPT uses chatgpt.com.
2. DeepSeek uses chat.deepseek.com.
3. Qwen uses qianwen.com first.
4. Use chat.qwen.ai only if qianwen.com is unavailable or blocked.

## Test readiness

Ready for one full connectivity and route test.

Prepared:

1. Two-level routing rule is defined.
2. Official site URLs are defined.
3. GitHub repo and file paths are defined.
4. GPT direct route can be tested now.
5. High-value three-site route can be tested now.
6. Coordinate plus step-by-step screenshot method can record the evidence.

Caution:

1. If local V15_FULL is not found, do not mark V15 full-chain test as passed.
2. This run should test site connection, two-level route, three-model A-layer samples, and GPT final fusion.
3. If login, captcha, or risk control appears, capture screenshots and stop for user confirmation.
4. Use Qwen international backup only if the Qianwen Chinese site is unavailable.

## Codex test command

Run one UltraFusion 6.1B site-connectivity and route test with coordinate plus step-by-step screenshot evidence.

Open and verify these sites:

1. https://chatgpt.com/
2. https://chat.deepseek.com/
3. https://www.qianwen.com/
4. https://chat.qwen.ai/ only as backup if qianwen.com is unavailable.

Test A: ordinary question route.

Question:

What is the capital of France? Answer briefly.

Expected route:

GPT direct answer only. Do not use DeepSeek, Qwen, V15, A/B/C/D, or multi-model fusion.

Test B: high-value route skeleton.

Question:

Design a low-cost multi-model answer workflow for deciding whether a normal question should use GPT only or escalate to multi-model review. Give route rules, failure handling, and acceptance criteria.

Expected route:

1. GPT initial framing.
2. DeepSeek official site answer as depth and adversarial review.
3. Qianwen or Qwen official site answer as third perspective.
4. GPT final fusion.

If V15_FULL is not found locally, label this test as non-V15 skeleton test. Do not claim V15 full chain passed.

Evidence requirements:

1. Screenshot before each site interaction.
2. Screenshot after each answer appears.
3. Save clipboard or copied answer text.
4. Save a final markdown report with PASS/PARTIAL/FAIL.
5. Include every screenshot path in the report.
6. Final status may be PASS only if all screenshots exist and every route decision matches UltraFusion 6.1B.
