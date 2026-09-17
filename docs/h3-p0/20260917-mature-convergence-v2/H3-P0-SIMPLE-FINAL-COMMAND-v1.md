# H3-P0 简洁最终执行命令 v1

状态：`READY_TO_EXECUTE / MAIN_PATH_ONLY`

方法：`first-principles-physical-limit-convergence v1.9.0（第一性原理物理极限收敛引擎 v1.9.0）`

## 1. 当前结论

```text
当前主路径赢家 = Star7 Native FP16 Exact
E1裁决 = KEEP（保留）
Total P50 = 10.562 s
Total P95 = 14.510 s
最快有效样本 = 6.484 s
T_PHY_TOTAL_REFERENCE（物理极限参照） = 0.23–0.57 s
REAL_STATE_OPTIMUM_RANGE（本机现实最优区间） = 4–14 s
```

Star7 已经真实进入本机现实目标区间。

当前主流程不再增加任何新候选。

W4A8、INT8 VAE、conditioning cache（条件缓存）、host-sync（主机同步）等全部不插回当前主流程。

## 2. 第一步：安装/核验母技能 v1.9.0

从正式分支：

```text
codex/first-principles-physical-limit-convergence-v1.9.0
```

读取：

```text
skills/first-principles-physical-limit-convergence/VERSION
skills/first-principles-physical-limit-convergence/SKILL.md
```

要求：

```text
VERSION=1.9.0
```

本机旧技能先备份，再同步 v1.9.0，回读确认。

不得修改代理、网络、ComfyUI、Python、Torch、CUDA 或模型。

## 3. 第二步：使用当前 Star7 KEEP 配置

固定配置：

```text
Loader（加载器） = MiniMaxH3FP16LoaderStar7
Diffusion（扩散模型） = minimax_h3_fl2va_pruned_int8_convrot.safetensors
Text Encoder（文本编码器） = qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors
Video VAE（视频VAE） = minimax_h3_video_vae_fp16.safetensors
Flags（启动参数） = --fast-disk --reserve-vram 1.0 --disable-pinned-memory
```

任务固定：

```text
T2VA
32×32
5 frames（5帧）
1 step（1步）
prompt = static frame
sampler = res_multistep
scheduler = beta
no input audio（无输入音频）
real MP4（真实MP4）
```

不得改变任何性能变量。

## 4. 第三步：最终10次认证

先做 1 次预热，不计统计：

```text
920099
```

然后连续做 10 次正式运行：

```text
920100
920101
920102
920103
920104
920105
920106
920107
920108
920109
```

总 GPU 运行数：11。

禁止自动追加第 12、第 13 次。

## 5. 计时

```text
Generation（核心生成）
= sampler_function 前后 CUDA Event + synchronize

Total（总时间）
= POST /prompt 前 → history 完成且真实 MP4 已存在

Path（路径时间）
= Total - Generation

QC（质量检查）
= RESULT_READY 后执行，不计入 Total
```

## 6. 每条质量检查

必须全部通过：

```text
history complete（历史完成）
MP4 exists（MP4存在）
ffprobe = 32×32×5
ffmpeg decode succeeds（可解码）
finite pixels（有限像素）
non-black / non-flat（非黑、非平坦）
every frame range >= 8
每帧标准差 std >= 1.5
保存产物 SHA256
```

## 7. 最终认证通过条件

```text
正式有效运行 = 10/10
QC通过 = 10/10
无崩溃 = YES
无自动重试 = YES
P95 Total <= 2.0 × P50 Total
最大 Total <= 2.5 × P50 Total
```

并检查是否存在明显持续变慢：

```text
最后3条 Total 中位数
<= 前3条 Total 中位数 × 1.5
```

### 通过

进入最终冻结。

### 不通过

```text
FINAL_CERTIFICATION（最终认证）= FAIL
停止
保存证据
返回 GPT
```

不得在同一任务里继续发明新优化路线。

## 8. 最终冻结

生成：

```text
H3-P0-FINAL-99-REPORT.md
H3-P0-FINAL-99-STATE.json
```

包含：

- 当前母技能 v1.9.0；
- 固定任务合同；
- Star7 最终配置；
- E1 KEEP 证据；
- 10 次正式 P50/P95 Generation/Path/Total；
- QC 10/10；
- 物理极限 0.23–0.57 s；
- 本机现实最优区间 4–14 s；
- E2R/E2P 作为历史证据；
- 其他候选已转为独立99路径或暂缓；
- 模型/源码/工作流哈希；
- Git 提交与远端核验回执。

如果最终认证和远端核验均通过：

```text
H3_P0_GENERATION_99=YES
H3_P0_PATH_99=YES
FINAL_99=YES
FREEZE=YES
```

然后停止并返回 GPT。

## 9. 禁止事项

本次最终执行中禁止：

- W4A8 测试；
- 新模型下载；
- INT8 VAE 测试；
- conditioning cache 测试；
- host-sync patch；
- profiler（性能剖析）；
- kernel trace（内核追踪）；
- 参数搜索；
- 版本搜索；
- 新候选；
- 中间结果正常时返回 GPT 重新设计。

当前任务只做：

```text
Star7 KEEP
→ 10次最终认证
→ 远端冻结
→ 完成
```
