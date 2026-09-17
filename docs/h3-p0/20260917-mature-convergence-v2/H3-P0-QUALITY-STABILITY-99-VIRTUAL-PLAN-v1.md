# H3-P0 质量稳定性99：虚拟方案 v1

状态：`INDEPENDENT_99_PATH / VIRTUAL_ANALYSIS_COMPLETE / READY_FOR_BOUNDED_QUALITY_DIAGNOSTIC`

## 一、目标

新的独立99目标不是单纯追求最快，而是：

```text
质量稳定通过率 = 100%（硬约束）
在上述硬约束下：端到端时间最短
```

有限样本不能证明未来数学意义“永远100%”，因此工程认证定义为：固定认证集合 100% QC 通过、无人工挑 seed、无降低质量阈值、无无限重试。

当前不修改主 H3-P0 性能99历史事实；本路径单独解决 Star7 FP16 的质量稳定性。

## 二、已知真实事实

1. Star7 快速路径已真实把稳态 Total 压到约 5.5–8.7 s 区间；930100–930102 分别为 6.8896 / 8.6514 / 6.6044 s。
2. seed 930103：Star7 输出首帧近乎全白/平坦，QC FAIL；同 seed 原始 UNETLoader QC PASS。
3. 因此 930103 不是“seed 本身无效”；当前证据支持 `STAR7_QUALITY_FAIL=YES`。
4. Star7 v2.0.14 已对 condition_proj、50 个 DiT block FP32 residual、SwiGLU、attention out_proj、MLP fc2 等做 FP16 数值保护。
5. 原始 MiniMax H3 结构中仍有未被 Star7单独保护的数值边界，包括 AdaLN 投影/调制、QKV 投影、Q/K RMSNorm+RoPE、attention 主体、FinalLayer/最终输出边界等。
6. 失败产物是 finite、可解码但接近纯白，不是 NaN/Inf 崩溃；虚拟优先判断为“尺度/动态范围偏移或饱和”，而不是完全数值爆炸。

## 三、第一性原理质量链

固定任务的质量成立至少要求：

```text
输入 latent / conditioning 正常
→ timestep / AdaLN 调制尺度正常
→ 50层 DiT 中间状态动态范围正常
→ attention / MLP 分支不产生异常放大或塌缩
→ FinalLayer 输出 latent 保持有效动态范围
→ VAE decode 得到非黑、非白、非平坦视频
```

质量失败的物理/数值原因只能发生在这条链的某个边界；不存在“无原因白帧”。

## 四、当前候选原因排序（Virtual）

### Q1：AdaLN 调制边界（高优先）

原因：Star7 block wrapper 把 norm 输出转 FP16，但 `adaln_proj(t_emb)` 生成 shift/scale/gate 后，再通过 `_mod_scale_shift` / `_mod_gate` 参与所有 50 个 block。若某 seed 对应 latent 状态让调制值进入 FP16 敏感区，可能出现有限值但动态范围异常。

### Q2：Q/K RMSNorm + RoPE / attention 输入尺度（高优先）

原因：Star7 保护了 attention `out_proj`，但 qkv_proj、Q/K RMSNorm+RoPE 与 optimized attention 主体仍走 FP16/量化路径。异常可保持 finite，却把表示推到错误方向。

### Q3：FinalLayer / 最终输出边界（高优先）

原因：如果前 50 block 中间状态仍正常，而最终 latent 突然塌缩/偏置，FinalLayer 是最短解释；它直接决定送入 VAE 的输出动态范围。

### Q4：MLP/attention 已保护部分仍不足（中优先）

Star7 已对 SwiGLU、fc2、out_proj 做缩放保护，但固定缩放常数 `64 / 256` 可能在少数输入分布下仍不足。只有诊断证明异常从这些位置开始，才允许考虑调整。

### Q5：模型驻留/加载导致权重状态异常（低优先）

当前同 seed reference 能正常，且 Star7失败时模型可完整执行；无直接证据支持权重损坏。先不作为主候选。

## 五、最小质量诊断测试

目标：找到“Star7 与原始 Loader 第一次出现明显数值分叉”的边界。

不是性能测试；禁止 profiler、kernel trace、参数搜索、版本搜索。

固定两类 seed：

```text
FAIL_SEED = 930103
PASS_SEED = 930100
```

固定两条路径：

```text
FAST = Star7 Native FP16 Exact
REF  = 原始 UNETLoader
```

最多 4 条诊断运行：

```text
930103 FAST
930103 REF
930100 FAST
930100 REF
```

如果 930103 FAST 在诊断运行中不再复现白帧：记录 `FAILURE_NOT_REPRODUCED`，停止，不允许追加运行；返回 GPT 重新判断。

### 只记录以下边界的统计摘要

每个边界只记录：dtype、finite、min、max、mean、std、absmax；不保存完整 tensor。

```text
A. condition_proj 输出
B. t_emb / AdaLN shift-scale-gate
C. block 0 / 10 / 20 / 30 / 40 / 49：
   - norm+mod 后 h
   - attention 输出（out_proj 前/后）
   - MLP fc1 / activated / fc2 输出
   - block residual x
D. Q/K RMSNorm+RoPE 后 q/k 的 absmax/std（上述采样 block）
E. FinalLayer 输入、调制后、最终输出
F. VAE 前最终 video latent
```

诊断只判断数值分叉，不用这些运行做正式性能统计。

## 六、诊断裁决

### CASE A：首次分叉出现在 AdaLN

Virtual 修复优先级：仅把 AdaLN 投影/调制计算边界提升到 FP32，其他 FP16 保留。

### CASE B：首次分叉出现在 Q/K RMSNorm+RoPE / attention

Virtual 修复优先级：只扩大 Q/K norm/rope 或 attention 输入的 FP32 保护，不改全部 attention。

### CASE C：50个 block 大体正常，FinalLayer 才分叉

Virtual 修复优先级最高：只保护 FinalLayer。理论性能成本最小。

### CASE D：分叉从现有 out_proj/fc2/SwiGLU 保护点开始

检查现有固定缩放 64/256 是否覆盖失败样本动态范围；只允许设计一个基于观测上界的最小缩放修正，不做 sweep。

### CASE E：没有找到稳定可复现的内部数值分叉

当前最小修复路线不成熟；停止该路径。此时才把“Star7 + QC + 原始 Loader fallback”提升为保底质量稳定系统方案。

## 七、虚拟修复原则

任何候选修复必须同时满足：

```text
只改变一个明确数值边界
不改模型、seed、sampler、scheduler、VAE、任务合同
质量目标 = 失败 seed 930103 修复 + 已通过 seed 不退化
预计性能损失 <= 1.0 s 或 <= 15% Total（规划门槛）
可逆
一次 bounded A/B 可验证
```

如果需要大面积 FP32、版本迁移、参数 sweep、开放式 profiling 才能成立，则本修复路线判 `ROI_INSUFFICIENT`，转保底系统方案。

## 八、质量稳定性现实时间目标

基于当前 fast-path 实测：

```text
QUALITY_STABLE_FAST_TARGET = 6–9 s Total P50
QUALITY_STABLE_WIDE_TARGET = 5–11 s Total P50
QUALITY_PASS_CONSTRAINT = 100% on fixed certification set
```

这是质量稳定约束下的现实目标带，不修改原 `T_PHY_TOTAL_REFERENCE=0.23–0.57 s`。

## 九、Fallback 保底路线

只有最小数值修复路线无法成熟时，才启用：

```text
Star7 fast path
→ automatic QC
→ QC fail 时 same-seed 原始 UNETLoader
→ QC
→ 最终交付
```

它是第二优先级保障，不是当前第一选择。

## 十、当前状态

```text
QUALITY_STABILITY_99_PATH=OPEN
FIRST_PRINCIPLES_CAUSAL_MODEL=DEFINED
VIRTUAL_CAUSE_MATRIX=DEFINED
NEXT_ACTION=BOUNDED_NUMERICAL_BOUNDARY_DIAGNOSTIC
MAX_GPU_RUNS_NEXT=4
NO_FREE_EXPLORATION=YES
FALLBACK_PATH=RESERVED_SECOND_PRIORITY
```
