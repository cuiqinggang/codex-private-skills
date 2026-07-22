# Governance Evolution Method

## Method

1. 发现问题。
2. 读取目标技能包。
3. 判断是规则缺口还是执行没按规则。
4. 如果规则缺口，补 source-of-truth。
5. 如果执行没按规则，补验证脚本 / gate。
6. 所有修改都要备份。
7. 所有硬规则都要二次验证。
8. 最终生成报告和状态码。

## Decision Guide

If the skill package has duplicated rules, create or repair `SOURCE-OF-TRUTH-MAP.md`.

If the package is too large, add context budget and progressive disclosure.

If PASS claims are untrusted, add script verification and stage gate verification.

If written requirements are skipped, add declared requirement coverage and Completion Ledger fields.

If generated files are left unclosed, add artifact checkpoint closure.

## Final Evidence

Every governance patch must produce:

- source readback
- backup report
- changed file list
- verification outputs
- final report
- final status codes
