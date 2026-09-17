# H3-P0 最终认证重试命令 v1

状态：`READY_FOR_ONE_BOUNDED_CERTIFICATION_RETRY`

方法：`first-principles-physical-limit-convergence v1.9.0`

依据：

- `H3-P0-FINAL-99-REPORT.md`
- `H3-P0-FINAL-CERTIFICATION-REPAIR-v1.md`

## 1. 目标

不再优化，只重新做一次合理化的最终认证。

固定赢家仍为：`Star7 Native FP16 Exact`。

禁止：新候选、新模型、新参数、W4A8、INT8 VAE、条件缓存、host-sync、profiler、kernel trace、版本搜索、参数搜索。

Codex 只允许处理执行层问题，不允许改变方案。

---

## 2. 固定配置

```text
Loader = MiniMaxH3FP16LoaderStar7
Diffusion = minimax_h3_fl2va_pruned_int8_convrot.safetensors
Text Encoder = qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors
Video VAE = minimax_h3_video_vae_fp16.safetensors
Flags = --fast-disk --reserve-vram 1.0 --disable-pinned-memory
```

固定任务：T2VA / 32×32 / 5帧 / 1步 / static frame / res_multistep / beta / 无输入音频 / 真实 MP4。

---

## 3. 两次预热

固定做 2 次预热，不计正式统计：

```text
930098
930099
```

只要求任务完成和技术输出链正常；记录时间但不进入 P50/P95。

---

## 4. 正式 seed 池

按顺序使用：

```text
930100
930101
930102
930103
930104
930105
930106
930107
930108
930109
```

备用：

```text
930110
930111
```

目标：得到 10 条 Star7 正式有效样本。

---

## 5. QC 与 seed 归因

普通 PASS 必须满足：MP4存在、32×32×5、可解码、finite、非黑非平坦、每帧 range>=8、std>=1.5、保存 SHA256。

若某个 Star7 seed 发生：

```text
history完成
MP4可解码
像素finite
但画面近乎全白/平坦
```

则不立即把 Star7 判失败。

只允许做 1 次同 seed reference 对照：

```text
Loader = 原始标准 UNETLoader
其余 diffusion/text encoder/VAE/flags/task/seed 完全相同
```

reference 对照只做 QC 归因，不用于性能统计。

### reference 也平坦/全白

```text
SEED_INVALID=YES
```

该 seed 不计入 Star7 正式认证；使用下一个备用 seed。

### reference QC PASS

```text
STAR7_QUALITY_FAIL=YES
FINAL_CERTIFICATION=FAIL
STOP
RETURN_TO_GPT
```

最多允许 2 个 `SEED_INVALID` 替换；若两个备用 seed 都用完仍不足10条有效正式样本：停止返回 GPT。

任何其他技术 QC 失败、崩溃、NaN/Inf、无法解码等直接 FAIL，不做 seed 归因。

---

## 6. 计时

```text
Generation = sampler_function 前后 CUDA Event + synchronize
Total = POST /prompt 前 → history complete 且真实 MP4 已存在
Path = Total - Generation
QC 在 RESULT_READY 后，不计入 Total
```

---

## 7. 最终通过条件

必须得到 10 条有效 Star7 正式运行，并同时满足：

```text
VALID_FORMAL_RUNS=10/10
QC_PASS=10/10
NO_CRASH=YES
NO_AUTO_RETRY=YES
TOTAL_P50 <= 14.0s
GENERATION_P50 <= 5.0s
PATH_P50 <= 9.0s
TOTAL_P95 <= 2.0 * TOTAL_P50
TOTAL_MAX <= 2.5 * TOTAL_P50
LAST3_MEDIAN <= FIRST3_MEDIAN * 1.5
```

通过后生成新的：

- `H3-P0-FINAL-99-REPORT-v2.md`
- `H3-P0-FINAL-99-STATE-v2.json`

并推送、远端回读核验。

只有认证 PASS + remote verify PASS 才写：

```text
H3_P0_GENERATION_99=YES
H3_P0_PATH_99=YES
FINAL_99=YES
FREEZE=YES
```

否则：

```text
FINAL_99=NO
FREEZE=NO
STOP
RETURN_TO_GPT
```

---

## 8. 运行上限

```text
2次预热
+ 10条目标正式 Star7
+ 最多2条 Star7 备用 seed
+ 最多2条同 seed reference QC 归因
```

最大 GPU 运行数：16。

不得自动增加。
