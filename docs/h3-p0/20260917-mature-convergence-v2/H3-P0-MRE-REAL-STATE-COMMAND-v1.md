# H3-P0 MRE 真实态校准命令包 v1

状态：RELEASED（已发布）

本命令包只完成一件事：在旧 H3-P0 已冻结、已验证的 V3 基础上，用成熟的一次性 runner（运行器）做一次 MRE（极简真实运行），取得新的真实运行态数据；完成后立即停止，不进入任何优化候选，不产生 V1→Vn 探索链。

## 0. 方法和事实源

新方法：`first-principles-physical-limit-convergence v1.5.0（第一性原理物理极限收敛引擎1.5版）`。

只读方法来源：

`origin/codex/first-principles-physical-limit-convergence-v1.5.0`

执行分支：

`codex/h3-p0-mature-convergence-v2`

旧冻结事实根：

`654a47489cb68a958f689484a07bcaa5c659f8e2`

必须先读取：

- `docs/h3-p0/20260916-first-principles-v1/H3-P0-LEGACY-EXPLORATION-RETROSPECTIVE.md`
- `docs/h3-p0/20260916-first-principles-v1/H3-P0-LEGACY-EVIDENCE-INDEX.md`
- `docs/h3-p0/20260916-first-principles-v1/H3-P0-FAILURE-INDEX.md`
- `docs/h3-p0/20260916-first-principles-v1/H3-P0-EMPIRICAL-PRIORS.md`
- `docs/h3-p0/20260916-first-principles-v1/H3-P0-runner.py`

不要全盘扫描 `C:\AI`，不要重新研究已知问题。

## 1. 本轮固定物理参照

```text
T_PHY_GENERATION（核心生成物理极限）= 0.05~0.12 s
T_PHY_PATH（系统路径物理极限）= 0.18~0.45 s
T_PHY_TOTAL（总物理参照）= 0.23~0.57 s
```

这些只是物理极限参照，不是现实99门槛。

本轮禁止直接沿用旧 `T_MACHINE_STAR_V1=1.15~3.40 s` 作为最终现实目标；必须等 MRE 数据完成后，由 GPT 结合真实运行态重新计算：

`T_MACHINE_STAR_REAL（真实态本机稳定理论极限）`。

Codex 本轮不负责自行修订现实极限，只负责提供完整、可信的真实数据。

## 2. 固定任务合同

```text
MODE=T2VA（纯文本生成）
WIDTH=32
HEIGHT=32
FRAMES=5
STEPS=1
PROMPT=static frame
SAMPLER=res_multistep
SCHEDULER=beta
INPUT_AUDIO=NO（无外部音频）
FINAL_OUTPUT=REAL_MP4（真实MP4）
```

正式 seed（随机种子）：

```text
COLD=910001（冷态观察，不进统计）
WARMUP=910002（预热，不进统计）
FORMAL=910100,910102,910103（3条正式样本）
```

禁止改变任务合同来换取速度。

## 3. 本轮唯一运行配置

直接复用旧 `LAST_GOOD（最近保留版）=V3_RESERVE1`：

```text
--fast-disk
--reserve-vram 1.0
--disable-pinned-memory
PORT=8194
```

禁止测试：

- Star7；
- ComfyUI 新版本；
- pinned-memory；
- reserve-vram 新值；
- VAE full-load；
- profiler（性能剖析器）；
- 新 kernel（内核）；
- 新量化；
- 新缓存；
- 新预取；
- 任何其他优化候选。

本轮只是“测真实状态”，不是“优化”。

## 4. 直接复用成熟 runner，不重新造测试框架

权威 runner：

`C:\Users\A\Documents\Codex\codex-private-skills\docs\h3-p0\20260916-first-principles-v1\H3-P0-runner.py`

先核对它与仓库冻结版本一致；如本地文件存在未知修改，不覆盖，先报告并从冻结提交提取只读副本到本轮临时目录。

该 runner 已具备：

- canonical workflow（权威母版）SHA 检查；
- 32×32 / 5帧 / 1步受控去重甲；
- CUDA Event（CUDA事件）核心生成计时；
- 端到端 T_TOTAL（总时间）计时；
- T_PATH = T_TOTAL - T_GENERATION；
- 1次冷态 + 1次预热 + 固定正式 seed；
- ffprobe / ffmpeg QC（质量检查）；
- 非黑/非平坦帧检查；
- MP4 SHA256；
- samplers.py 自动备份和 finally 自动恢复；
- 启动前 8194/8195 监听门禁；
- 服务启动超时；
- 单 prompt 超时；
- summary 和逐 run JSON 落盘。

不要重写上述能力。

## 5. 新证据根

创建独立证据目录：

`C:\AI\H3-P0-Acceptance\mature-convergence-v2\20260917-mre-01`

不得写入旧冻结证据根：

`C:\AI\H3-P0-Acceptance\fp-convergence\20260916-run-01`

旧目录只读。

## 6. 运行前成熟门禁

先做只读检查并保存 `preflight.json`：

```text
8194_LISTENER=NO
8195_LISTENER=NO
NO_OTHER_H3_COMFYUI=YES
NO_OTHER_CUDA_COMPUTE_WORKLOAD=YES
```

记录但不修改：

- GPU 名称；
- VRAM 总量/当前空闲；
- NVIDIA driver（显卡驱动）；
- Python；
- Torch；
- CUDA；
- ComfyUI commit（提交版本）；
- comfy-kitchen；
- comfy-aimdo；
- 当前 runner SHA256；
- canonical workflow SHA256；
- samplers.py SHA256；
- 三个模型的路径与文件大小（不要为了本轮重新哈希几十GB模型）。

禁止修改：

- 网络代理；
- 系统代理；
- FlClash；
- 系统安全设置；
- GPU power limit（功耗限制）；
- GPU overclock（超频）；
- 全局 Python / Torch / CUDA 环境。

如果发现其他 CUDA compute（CUDA计算）工作负载，先停止本轮 MRE，不要终止未知进程。

## 7. 启动方式：独立一次性任务，避免会话断开造成重复运行

不要使用复杂嵌套 PowerShell `-Command "..."`。

如果需要启动脚本，写一个明确 UTF-8 的临时 `.ps1`，先做语法检查，再执行。

用独立进程启动旧 runner，使 Codex/AI 会话短暂断开时本地任务仍可自然完成；保存：

- runner PID；
- 进程创建时间；
- 完整命令；
- stdout 路径；
- stderr 路径；
- launch time（启动时间）。

正式 runner 参数固定为：

```text
--evidence C:\AI\H3-P0-Acceptance\mature-convergence-v2\20260917-mre-01
--phase MRE_REAL_STATE_01
--reserve 1.0
--pinned disabled
--runs 3
--cold
```

不允许自动进入下一 phase（阶段）。

## 8. 断线/恢复规则

如果 Codex、浏览器或模型会话中断：

`AI_SESSION_FAILURE != LOCAL_EXPERIMENT_FAILURE（AI会话失败不等于本地实验失败）`。

恢复后必须先检查：

- 保存的 runner PID + 创建时间；
- 8194 listener（监听）；
- server-MRE_REAL_STATE_01.log；
- runs/ 目录；
- summary-MRE_REAL_STATE_01.json；
- instrumentation-restore-proof.json；
- 文件最近更新时间。

只要进程仍在、8194 属于该实例、日志/结果仍在前进，禁止重启。

如果 runner 已退出但：

- 冷态结果存在；
- warmup 存在；
- 3条正式 run 完整；
- 3/3 QC PASS；
- summary 完整；
- samplers.py 已恢复且 SHA before == SHA after；

则直接判定 `MRE_COMPLETED=YES（极简真实运行已完成）`，禁止重跑。

`psutil.NoSuchProcess（进程已消失异常）` 只表示进程可能已经自然退出；先检查结果，不得因此重跑 GPU。

如果证据不完整且 PID/8194 均消失、文件也不再增长，才允许从同一 MRE 阶段恢复；不得启动第二个并发实例。

## 9. 正式测量

runner 应顺序完成：

```text
1. COLD 910001（冷态观察）
2. WARMUP 910002（预热）
3. FORMAL 910100
4. FORMAL 910102
5. FORMAL 910103
6. QC
7. summary
8. terminate 8194
9. restore samplers.py
10. verify SHA restore
```

GPU 正式运行期间禁止启动 profiler、连续 nvidia-smi 高频采样或其他 CUDA 重任务。

可在 timed window（计时窗口）之外保存：

- 启动前 GPU idle（空闲）快照；
- 服务 ready（就绪）后快照；
- 全部完成后的 GPU 快照。

## 10. 必须输出的数据

对冷态、预热、3条正式样本逐条保存：

```text
seed（随机种子）
total_s（总时间）
generation_cuda_s（核心生成CUDA时间）
generation_wall_s（核心生成墙钟时间）
path_s（系统路径时间）
result_ready（结果完成边界）
MP4 path（视频路径）
MP4 SHA256
frame means/ranges/stds（帧均值/范围/标准差）
task_completed（任务是否真实完成）
```

正式 summary 必须有：

```text
GENERATION_P50/P95（核心生成P50/P95）
PATH_P50/P95（系统路径P50/P95）
TOTAL_P50/P95（总时间P50/P95）
```

再与旧 V3 同 seed 数据做只读配对比较：

```text
OLD_V3_GENERATION_P50=20.226025 s
OLD_V3_PATH_P50=17.970201 s
OLD_V3_TOTAL_P50=38.042308 s
```

输出：

- 每个相同 seed 的 Generation/Path/Total 差值；
- P50/P95 漂移；
- 是否出现软件/运行路径变化；
- 不得因为漂移自动调参数或重跑。

## 11. 真实态校准报告

生成：

`docs/h3-p0/20260917-mature-convergence-v2/H3-P0-MRE-REAL-STATE-01.md`

以及：

`docs/h3-p0/20260917-mature-convergence-v2/H3-P0-MRE-REAL-STATE-01.json`

报告必须区分：

```text
STATIC_FACTS（静态事实）
LEGACY_PRIORS（旧任务经验先验）
NEW_MRE_OBSERVATIONS（新极简真实运行观测）
CONFLICTS（新旧冲突）
REAL_STATE_FACTS（当前可确认真实态事实）
UNKNOWN_REMAINDER（仍未知部分）
```

只写事实，不在本轮自动推导 Star7 或下一优化候选。

## 12. 本轮停止条件

满足以下条件立即停止：

```text
MRE_COMPLETE=YES
FORMAL_VALID_RUNS=3
FORMAL_QC_PASS=3/3
SUMMARY_COMPLETE=YES
SAMPLERS_RESTORED=YES
NO_SECOND_H3_INSTANCE=YES
REAL_STATE_REPORT_WRITTEN=YES
```

然后：

```text
NO_NEW_OPTIMIZATION=YES
NO_STAR7_TEST=YES
NO_VIRTUAL_99_EXECUTION=YES
RETURN_TO_GPT=YES
```

把结果交回 GPT，由 GPT 使用：

`T_PHY（物理极限） + 新MRE真实数据 + V1~V11经验先验 + 成熟方案资料`

计算：

`T_MACHINE_STAR_REAL（真实态本机稳定理论极限）`

并构建后续完整 `VIRTUAL_MATURE_PATH（虚拟成熟路径）`。

## 13. Git 收口

本轮新增的正式报告、JSON、必要的小型控制/启动脚本和运行命令说明保存到共同工作区：

`cuiqinggang/codex-private-skills`

分支：

`codex/h3-p0-mature-convergence-v2`

禁止：

```text
git add .
git reset --hard
force push
```

只精确 stage（暂存）本轮新文件。

提交建议：

`test(h3-p0): capture mature-convergence MRE real state`

完成：

```text
COMMIT
→ PUSH
→ REMOTE VERIFY（远端核验）
```

最终只回报：

- MRE 是否完成；
- 冷态/预热/3条正式样本是否齐全；
- Generation / Path / Total P50/P95；
- 与旧 V3 的配对漂移；
- QC；
- samplers.py 是否恢复；
- 是否发生环境漂移/故障；
- 证据目录；
- 报告路径；
- commit SHA；
- remote HEAD；
- 是否已严格停止、未进入下一优化。
