# Jev Decision Accelerator v0.1 — v3.1.2 Experimental Overlay

状态：`EXPERIMENTAL_SHADOW_ONLY`

本文件不是第四核心，也不改变 v3.1.2 三核心。它只属于：

```text
CORE_3_HIGH_INTELLIGENCE_VIRTUAL_MATURITY
  -> JEV_DECISION_ACCELERATOR
```

## 1. 目标

把高智能已经定义好的、答案空间有限的语义判断，从“LLM 生成文字 -> 解析文字 -> 再分支”压缩为：

```text
MACHINE_STATE
-> TYPED QUESTIONS
-> Jev calibrated probabilities
-> deterministic code branch
```

唯一目标仍是 `T_VALID -> min`。Jev 只可减少决策/路由/判别时间，不得把 GPU compute、I/O、decode、hash、QC 等物理工作虚构为已消失。

## 2. 四类职责

```text
DETERMINISTIC_FACT / ARITHMETIC / VERIFICATION -> CODE
FINITE_SEMANTIC_DECISION                         -> JEV
SYNTHESIS / NEW PLAN / CODE CREATION            -> GPT/DeepSeek
FINAL HARD ACCEPTANCE                            -> CODE VERIFIER
```

目标不是全部改成 Jev，而是把 Jev 放到它物理上最有优势的位置。

## 3. Jev 适配条件

只有同时满足以下条件才进入 Jev：state 已由程序或冻结证据构造；answer space 预先闭合；任务属于 classification/routing/gating/ranking；不要求生成新文字/代码/算法；动作仍由代码执行；高影响动作有 confidence gate；最终正确性仍由 deterministic verifier 保证。

## 4. OpenRouter 传输

```text
POST https://openrouter.ai/api/alpha/decisions
MODEL_PINNED=typesafe/jev-1.13
MODEL_FLOATING=~typesafe/jev-latest
AUTH=OPENROUTER_API_KEY environment variable only
```

禁止把 API key 写入 GitHub、command pack、JSON evidence、prompt/state、shell history 或日志。

私有项目默认强制 provider.zdr=true 且 provider.data_collection=deny；若不存在满足策略的 endpoint，则 FAIL CLOSED，不自动放宽隐私条件。

## 5. 首轮 primitives

首轮 H3-P0 shadow 只使用 `noul` 和 `choice`。暂不把 `score` 放进第一轮 release gate。

## 6. 正确率策略

不得直接用固定 0.5 阈值上线。必须使用历史已知答案回放并扫描 confidence threshold。

Release gate：

```text
CRITICAL_AUTO_ACCEPTED_ERRORS = 0
ILLEGAL_OUTPUTS               = 0
PRIVACY_DOWNGRADE             = 0
H3_GPU_RERUNS                 = 0
```

若无法达到零关键自动误判，Jev 只能是 ADVISORY，不得持有自动执行权。

## 7. 批处理也是优化变量

必须比较 MEGA_BATCH（全部一次）、FAMILY_BATCH（同类一次）、CASE_BATCH（逐 case）。最终选择 `min(P95_END_TO_END_DECISION_TIME)` subject to correctness gates。

## 8. H3-P0 首个验证

```text
H3-P0-JEV-SHADOW-01
GPU_RUNS=0
SOURCE=already-frozen H3-P0 evidence
PURPOSE=reverse replay known decisions
```

冻结事实源：

```text
docs/h3-p0/20260917-mature-convergence-v2/H3-P0-FINAL-99-FREEZE-v1.md
docs/h3-p0/20260917-mature-convergence-v2/H3-P0-FINAL-99-FREEZE-v1.json
docs/h3-p0/20260917-mature-convergence-v2/H3-P0-END-TO-END-METHOD-RETROSPECTIVE-v1.md
```

不得重新跑 H3 GPU，不得修改原 H3-P0 FINAL_99。

## 9. 晋级

SHADOW PASS 后才允许设计一个低风险 real gated control-plane task；真实 gated 通过后，才有资格切 first-principles v3.1.3。v3.1.2 本身保持冻结。
