# Script Verification Rules

## Purpose

Hard governance rules must be checked by scripts or deterministic checklist evidence.

## Rules

1. Hard rule must be verified（硬规则必须验证）.
2. Gate PASS requires verification（gate 通过需要验证）.
3. Forbidden action requires negative check（禁止项需要反向检查）.
4. Stage verification summary required（阶段验证汇总必需）.
5. Model self-claim is not verification（模型自称不算验证）.
6. Script preferred, deterministic checklist fallback（脚本优先，确定性清单兜底）.

## Verification Evidence

Acceptable evidence:

- script command log
- JSON result
- Markdown result
- deterministic checklist with concrete file paths, counts, hashes, logs, and status codes

Not acceptable:

- model says done
- final report says PASS without proof
- status code alone
- vague manual review
