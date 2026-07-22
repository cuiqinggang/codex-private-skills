# Failure Review Entry

## 2026-07-10 - Mature Desktop cleanup route was hard to discover

- Symptom: `preflight_reuse_check.py` returned no strong match even though a prior Desktop cleanup report and cleanup-governance skill existed.
- Cause: the skill description and triggers emphasized Knowledge Brain and large-directory cleanup, not Desktop screenshots, step/check numbers, or one-off scripts.
- Repair: added explicit Desktop trigger phrases, a dedicated SOP, and a conservative plan-first script.
- Prevention: future Desktop cleanup tasks must search both historical reports and skills using `桌面整理/桌面清理/截图/step/check/中间文件` terms.
- Acceptance: a future preflight or direct skill match must route Desktop clutter cleanup to this package.
