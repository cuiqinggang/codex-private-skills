# Multi-Round Closure Experience

Use this reference when testing or running a closed loop:

```text
ChatGPT planning -> Codex execution -> Codex result report -> ChatGPT next planning -> Codex next execution
```

## Lessons From TASK-20260505-MULTIROUND-MDREPORT

1. Start with yesterday replay:
   - Search prior bridge outputs.
   - Search existing skills.
   - Reuse frozen successful commands and scripts.

2. Require fixed ChatGPT planning format:
   - `TASK_ID`
   - `ROUND`
   - `## 本轮目标`
   - `## Codex 执行步骤`
   - `## 测试要求`
   - `## 成功判定`
   - `## 失败停止条件`
   - `END_TASK_ID`

3. Treat invalid GPT planning as a loop event:
   - Do not execute invalid or out-of-bound advice.
   - Save `answer_raw.md`.
   - Structurally extract why it is invalid.
   - Send `result_report_to_gpt.md` asking for corrected next-round planning.

4. Keep each round separate:
   - `prompt_to_gpt.md`
   - `answer_raw.md`
   - `codex_plan.md`
   - `execution_log.md`
   - `result_report_to_gpt.md`

5. Prove the validator works both ways:
   - Valid round passes.
   - Invalid round fails for the expected missing fields.

6. Handle delayed Copy response controls conservatively:
   - If the page still shows a stop-generating state, continue condition-based waiting.
   - If normal timeout expires, use a short grace wait and reveal controls by pressing End or moving near the message bottom.
   - Still require `复制回复 / Copy response`.
   - Do not use CDP, OCR, page-body text, or assistant-message text extraction as fallback.

## Do Not Expand

- Do not add browser capabilities.
- Do not use CDP.
- Do not OCR.
- Do not read page body text.
- Do not extract assistant message text directly when Copy response is missing.
- Do not rewrite GPT into a different plan.
