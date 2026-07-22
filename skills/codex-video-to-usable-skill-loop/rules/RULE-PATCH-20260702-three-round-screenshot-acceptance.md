# Rule Patch: Three-Round Screenshot Acceptance Gate

Date: 2026-07-02
Status: ACTIVE

## Value Judgment

HIGH_VALUE. This rule changes the default definition of "done" for durable Codex outputs. It reduces false completion claims by requiring actual use, repeated verification, repair evidence, and screenshot proof before final acceptance.

## Trigger Keywords

- 三轮实际测试
- 截图验证
- FINAL_PASS
- 默认验收规则
- 最终写入技能包
- 资料库
- 知识库
- 命令包
- 项目交付包
- 部署包
- 恢复包
- 测试包
- 自动化脚本

## Applies To

Use this gate before claiming completion for final outputs written into:

- skill packages
- knowledge bases
- material libraries
- command packages
- Codex, Hermes, or Kilo execution packages
- default rules
- project summaries
- delivery ZIPs
- recovery packages
- deployment packages
- test packages
- automation scripts

## Required Acceptance Gate

No final durable output is complete until all three rounds pass:

1. Round 1: basic open or basic run test.
2. Round 2: real use or real invocation test.
3. Round 3: recovery, retest, or boundary verification.

Each round must produce screenshot evidence. Text-only verification is not enough.

## Screenshot Evidence Rule

Treat missing screenshots as unverified work. Acceptable evidence includes:

- successful run screenshot
- actual file existence screenshot
- directory structure screenshot
- opened web panel screenshot
- test output screenshot
- PASS log screenshot
- recovered or retested run screenshot

## Required Acceptance Record Fields

Every final durable output must record:

- artifact name
- artifact path
- write location
- three-round test results
- screenshot evidence paths
- failures
- repair process
- retest result
- final conclusion: PASS, FAIL, or PARTIAL

## Completion Labels

- FINAL_PASS: allowed only when all three rounds passed and screenshot evidence exists.
- PARTIAL: some outputs exist, but one or more required rounds or screenshots are missing.
- FAIL: required output cannot be opened, invoked, recovered, or verified after repair attempts.

## Preflight Instruction

Before starting a complex durable-output task, check whether this acceptance gate applies. If it applies, plan screenshot capture and three verification rounds before writing the final answer.

## Failure Review Entry Point

If a task is claimed complete without three rounds or screenshot evidence, add a failure review using the local failure-review template and rerun acceptance before claiming PASS.

