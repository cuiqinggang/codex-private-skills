# 失败案例

## 记录格式

```
## Case ID: 日期
### 问题
### 预期
### 实际
### 根因分析
### 修复措施
```

（在正式使用后逐步积累）

## Case ID: 2026-06-23-ultrafusion-b-layer-speed-fable-mythos
### Problem
Future runs may treat B as review comments, cut ABCD for speed while still calling it full UltraFusion, or reuse stale Fable/Mythos availability claims.
### Expected
A/B/C/D are all V15 extreme layers. B is extreme model-level fusion over all valid A drafts. Reduced routes must be labeled honestly. Current model availability claims must be rechecked.
### Actual
The intake material documented the risk and clarified the correct route labels.
### Root Cause
Functional layer names can hide that every layer remains V15 extreme; speed pressure can cause label drift.
### Fix
Added rule patch `65-RULE-PATCHES/RULE-PATCH-20260623-ultrafusion-b-layer-speed-fable-mythos.md` and workflow `40-WORKFLOWS/A_ONLY_CORE2_FUSION_TEST_v1.0.md`.
