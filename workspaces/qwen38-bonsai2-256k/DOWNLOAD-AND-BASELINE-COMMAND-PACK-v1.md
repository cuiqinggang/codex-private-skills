# Bonsai 2 27B PQ2_0 — 256K 下载与现实基线命令包 v1

状态：COMMAND_PACK_REVIEWED / READY_FOR_CODEX / NOT_EXECUTED

## 0. 任务合同

~~~text
SKILL_ID=first-principles-physical-limit-convergence
SKILL_VERSION=3.1.2
CANONICAL_BRANCH=codex/first-principles-physical-limit-convergence-v3.1.2

TASK=Qwen3.8/Bonsai2-27B-PQ2_0-256K-baseline
TARGET_CONTEXT=262144
ONLY_REAL_MODEL_VARIANT=PQ2_0
SECOND_MODEL_DOWNLOAD=FORBIDDEN
PTQ1_0_DOWNLOAD=FORBIDDEN
MMProj_DOWNLOAD=FORBIDDEN
DRAFT_MODEL_DOWNLOAD=FORBIDDEN
SPECULATIVE_DECODING=OFF
THINKING=OFF
KV_CACHE=Q4_0
CONCURRENCY=1
TEXT_ONLY=YES
T_PHY=OFF

DO_NOT_CHANGE_PROXY=YES
DO_NOT_CHANGE_SYSTEM_NETWORK=YES
DO_NOT_CHANGE_UNRELATED_SYSTEM_SETTINGS=YES
NO_PARAMETER_SWEEP=YES
NO_CONTEXT_SWEEP=YES
NO_AUTOMATIC_128K_FALLBACK=YES
NO_64K_FINAL_PATH=YES
~~~

当前唯一目标：

~~~text
在 262144 上下文稳定可生产运行的前提下，
建立第一份真实 T_END_TO_END 基线。
~~~

如果 256K 失败：保存证据、停止、返回 GPT。不得自行改为 128K。

---

# 1. 固定上游与模型身份

~~~text
BONSAI_DEMO_REPO=https://github.com/PrismML-Eng/Bonsai-demo.git
BONSAI_DEMO_COMMIT=17b143e889a45c090816b520e79a50c996164e1f
LLAMA_CPP_RELEASE_TAG=prism-b10709-9a9394a

HF_REPO=prism-ml/Ternary-Bonsai-2-27B-gguf
HF_FILE=Ternary-Bonsai-2-27B-PQ2_0.gguf
DISPLAY_SIZE≈7.21GB
~~~

注意：DISPLAY_SIZE 只用于人工识别。最终完整性必须以 Hugging Face 文件元数据返回的“精确字节数 + LFS/SHA256”与本地实测 SHA256 为准。

Bonsai 2 必须使用 PrismML 对应的 llama.cpp 运行时；禁止用 stock llama.cpp 代替。

---

# 2. 本机工作区

固定新工作区：

~~~text
C:\AI\Bonsai2-27B-256K
~~~

目录：

~~~text
C:\AI\Bonsai2-27B-256K\Bonsai-demo
C:\AI\Bonsai2-27B-256K\downloads\staging
C:\AI\Bonsai2-27B-256K\evidence
~~~

规则：

- 目录不存在才创建。
- 已存在时先只读检查，不删除、不清空、不覆盖未知文件。
- 所有临时下载保留在 staging；失败后保留可续传数据。
- 完整性验证通过后才原子移动到 Bonsai-demo\models\bonsai2-gguf\27B。
- 不改变代理。
- 不从 System32 等系统目录执行。

---

# 3. Phase A — 只读预检

先记录：

~~~text
PowerShell 实际版本
git --version
curl.exe --version
aria2c 是否存在及版本
nvidia-smi
GPU 名称
GPU 总显存 / 当前占用
CUDA driver reported version
系统 RAM 总量 / 可用量
C: 剩余空间
当前代理相关环境变量（只读，绝不修改）
~~~

硬门禁：

1. 必须看到 NVIDIA GPU 和目标 2080 Ti 级设备；
2. 后续 Bonsai runtime 必须落到 CUDA binary，不允许静默 CPU fallback；
3. C: 建议至少保留 20 GiB 可用空间；不足则停止并回报；
4. PowerShell 目标优先 pwsh 7；不得通过修改系统 ExecutionPolicy 来绕过；
5. 任何未知阻断都先保存证据并停止，禁止修改代理或系统网络。

证据保存为：

~~~text
evidence\<timestamp>\preflight.json
evidence\<timestamp>\preflight.txt
~~~

---

# 4. Phase B — 固定上游运行时，只安装运行所需内容

如果 Bonsai-demo 不存在：

~~~text
git clone https://github.com/PrismML-Eng/Bonsai-demo.git C:\AI\Bonsai2-27B-256K\Bonsai-demo
~~~

随后必须：

~~~text
git fetch --all --tags
git checkout --detach 17b143e889a45c090816b520e79a50c996164e1f
git rev-parse HEAD
~~~

HEAD 必须精确等于固定提交。

运行 setup.ps1 时只准备运行时，禁止由 setup.ps1 下载模型：

~~~text
BONSAI_FAMILY=bonsai2
BONSAI_MODEL=27B
BONSAI_SKIP_GGUF=1
~~~

本步骤的目的只是得到 PrismML 固定版本的 Windows CUDA llama.cpp binary 与必要 Python/Hugging Face 依赖。

完成后必须证明：

~~~text
RUNTIME_COMMIT_MATCH=YES
CUDA_BINARY_EXISTS=YES
CPU_FALLBACK_USED=NO
MODEL_FILES_DOWNLOADED_BY_SETUP=0
~~~

若 setup 意外下载了任何 GGUF 大模型：停止，不继续基线；保留日志并返回 GPT。

---

# 5. Phase C — 固定下载方法：测速 → 并行 → 续传 → 监控 → 校验

## C1. 只下载一个文件

本轮唯一允许的大模型文件：

~~~text
Ternary-Bonsai-2-27B-PQ2_0.gguf
~~~

禁止下载：

~~~text
PTQ1_0
F16
mmproj
dspark
其他量化
~~~

## C2. 先读取官方元数据

使用固定 commit 下 setup 创建的 Python / huggingface_hub，读取 HF_REPO 中 HF_FILE 的：

~~~text
repo revision / commit
exact size bytes
LFS OID / SHA256（若 API 暴露）
~~~

保存到：

~~~text
evidence\<timestamp>\hf-metadata.json
~~~

若无法得到可信 SHA256，至少保存官方 exact size 和 repo commit；下载后仍必须计算本地 SHA256，标记 HASH_SOURCE=LOCAL_ONLY，不得虚构远端 hash。

## C3. 下载测速与并行策略

这是既定下载方法，不允许直接盲目全速下载。

原则：

~~~text
PROBE -> SELECT -> CONTINUE -> MONITOR -> VERIFY
~~~

优先复用 aria2c；如果本机已有 aria2c，则使用“同一 partial 文件、不同并行度、连续续传”的方法，不浪费已下载数据：

1. x1 / s1：30 秒；
2. x4 / s4：在同一 partial 上继续 30 秒；
3. 只有 x4 稳定且仍有明显带宽余量时，才测试 x8 / s8 30 秒；
4. 每阶段记录：
   - elapsed_s
   - bytes_before
   - bytes_after
   - delta_bytes
   - MiB_per_s
   - retry_count
   - error_count
5. 选择“实际平均速度最快且稳定”的并行度继续下载；
6. 不因单次峰值盲目选择更高并发。

aria2 必须开启：

~~~text
continue/resume
fixed output name
no auto rename
retry
retry wait
timeout
file-allocation=none
~~~

测速阶段产生的 partial 数据必须继续使用，禁止为了正式下载重新从 0 开始。

如果 aria2c 不存在：

- 不修改代理；
- 不为了本任务擅自改系统级下载配置；
- 使用固定 Python venv 内 Hugging Face 官方 hf/Xet 下载作为并行/断点续传 fallback；
- 同样记录实际下载速度、重试、总时间和断点状态；
- 不得删除已进入 HF cache 的有效块再重下。

## C4. 运行中监控

每 30 秒记录：

~~~text
timestamp
downloaded_bytes
delta_bytes
interval_MiB_s
process_alive
~~~

触发重新测速/恢复而不是重下：

~~~text
连续 60 秒无有效字节增长
OR
连续约 120 秒实际速度低于本轮最佳稳定测速的 50%
~~~

动作：

~~~text
停止当前下载进程（保留 partial/cache）
-> 记录原因
-> 重新测速
-> 从已有数据续传
~~~

不得删除已下载数据。

## C5. 完整性验证

下载完成后：

1. 精确文件字节数必须等于官方 metadata；
2. 计算本地 SHA256；
3. 若远端 LFS SHA256 可得，必须精确一致；
4. 运行 GGUF 基础可读性检查；
5. 验证通过才从 staging 原子移动到：

~~~text
C:\AI\Bonsai2-27B-256K\Bonsai-demo\models\bonsai2-gguf\27B\Ternary-Bonsai-2-27B-PQ2_0.gguf
~~~

保存：

~~~text
download-probes.json
download-monitor.csv
download-final.json
sha256.txt
~~~

---

# 6. Phase D — 256K 服务器启动

环境必须显式设置，不允许使用 RAM-tiered auto context：

~~~text
BONSAI_FAMILY=bonsai2
BONSAI_MODEL=27B
BONSAI_CTX=262144
BONSAI_KV4=1
BONSAI_SPECULATIVE=0
BONSAI_NGL=99
~~~

视觉文件未下载，因此保持纯文本。

启动 standalone llama server 时，必须显式关闭思考：

~~~text
--reasoning-budget 0
--reasoning-format none
~~~

如当前 PrismML 启动脚本还支持 chat-template thinking 参数，同时传入 enable_thinking=false；若该参数与当前 binary 不兼容，不得自行猜参数，保留 reasoning-budget=0 作为主门禁并记录实际 /props 与响应行为。

启动后必须回读：

~~~text
/health
/props
~~~

并证明：

~~~text
SERVER_HEALTH=PASS
EFFECTIVE_CONTEXT=262144
CUDA_PATH_ACTIVE=YES
GPU_OFFLOAD_FULL_OR_EXPECTED=YES
KV4_ACTIVE=YES
THINKING_OFF=YES
SPECULATIVE_OFF=YES
~~~

任一关键项不成立：停止，不做长上下文测试。

---

# 7. Phase E — 第一份真实 256K 基线

## E1. 输入规模

模型窗口仍是 262144，不把窗口塞到最后一个 token。

构造确定性长文本并通过 server 的 tokenizer 实际计数，使完整 prompt 落在：

~~~text
TARGET_PROMPT_TOKENS=240000..245000
~~~

至少保留约 17K 以上的输出/工具余量。

长文本中放置三个随机生成但在本轮冻结的标记：

~~~text
BEGIN_MARKER
MIDDLE_MARKER
END_MARKER
~~~

位置分别在前部、中部和接近尾部。

末尾任务只要求确定性执行：

~~~text
读取三个标记；
只返回 JSON；
字段 begin / middle / end 必须分别与三个标记完全一致；
另返回 sum=42；
不解释；
不思考展开。
~~~

输出上限：

~~~text
max_tokens <= 128
temperature = 0
~~~

## E2. 计时

权威总时间：

~~~text
T_END_TO_END =
从发出真实 240K~245K token 请求
到收到完整有效 JSON 响应
~~~

同时保存运行时 timings：

~~~text
prompt_tokens
prompt_ms
prompt_tokens_per_second
generated_tokens
generation_ms
generation_tokens_per_second
T_END_TO_END
~~~

## E3. 资源监控

长请求期间每 1 秒记录：

~~~text
GPU memory used/total
GPU utilization
GPU temperature
GPU power
system RAM used/available
server process alive
~~~

输出：

~~~text
resource-monitor.csv
resource-summary.json
~~~

必须记录：

~~~text
PEAK_VRAM
VRAM_HEADROOM_AT_PEAK
PEAK_SYSTEM_RAM
SYSTEM_RAM_HEADROOM_AT_PEAK
~~~

本轮先采集真实余量，不人为设一个未经实测证明的“最佳显存占满比例”。

## E4. 正确性与稳定性

PASS 至少要求：

~~~text
server did not crash
no OOM
no context truncation below requested target
response JSON parseable
three markers exact match
sum == 42
server health remains PASS after request
~~~

如果出现：

~~~text
OOM
server crash
CUDA allocation failure
effective context < 262144
prompt cannot complete
明显输出损坏
~~~

则：

~~~text
256K_BASELINE=FAIL
AUTO_FALLBACK_128K=NO
SAVE_EVIDENCE=YES
RETURN_TO_GPT=YES
~~~

---

# 8. 本轮禁止项

~~~text
不下载 PTQ1_0
不下载第二个量化版本
不下载视觉塔
不下载 drafter
不开 speculative
不做 128K / 64K 横向测试
不做 batch sweep
不做 KV 格式 sweep
不做 CUDA 参数 sweep
不做其他 runtime 对比
不改变代理
不改变系统网络
不自行启动“广域成熟方案池”的下一候选
~~~

现实数据回来后由 GPT 决定下一刀。

---

# 9. 结果写回共同工作区

执行结束，无论 PASS / FAIL / BLOCKED，必须在本分支创建：

~~~text
workspaces/qwen38-bonsai2-256k/results/<timestamp>/RESULT.md
workspaces/qwen38-bonsai2-256k/results/<timestamp>/RESULT.json
~~~

RESULT.json 至少包含：

~~~json
{
  "task": "qwen38-bonsai2-pq2-256k-baseline-v1",
  "status": "PASS|FAIL|BLOCKED",
  "model_file": "Ternary-Bonsai-2-27B-PQ2_0.gguf",
  "model_size_bytes": 0,
  "model_sha256": "",
  "upstream_demo_commit": "17b143e889a45c090816b520e79a50c996164e1f",
  "effective_context": 0,
  "target_prompt_tokens": 0,
  "actual_prompt_tokens": 0,
  "thinking_off": true,
  "kv4_active": true,
  "cuda_active": true,
  "download_probe_best_mib_s": 0,
  "download_total_seconds": 0,
  "t_end_to_end_seconds": 0,
  "prompt_tokens_per_second": 0,
  "generation_tokens_per_second": 0,
  "peak_vram_mib": 0,
  "vram_headroom_mib": 0,
  "peak_system_ram_mib": 0,
  "system_ram_headroom_mib": 0,
  "marker_check": "PASS|FAIL",
  "post_health": "PASS|FAIL",
  "failure_reason": "",
  "next_action": "RETURN_TO_GPT"
}
~~~

同时保存本轮主要日志/CSV/JSON 证据或其精确路径与哈希。

最后：

~~~text
git status
精确 stage 本轮新增文件
git commit
git push 到 codex/qwen38-bonsai2-pq2-256k-baseline-v1
远端回读 RESULT.md / RESULT.json
REMOTE_VERIFY=PASS
STOP
~~~

禁止 git add .、force push、reset --hard。

---

# 10. PowerShell 可靠性要求

执行前必须读取本仓库：

~~~text
skills/powershell-reliability-guard/SKILL.md
~~~

任何本轮新生成的 .ps1 包装脚本必须：

- 使用 pwsh 7 目标；
- 先静态/解析检查；
- 通过该技能的统一 guard 入口后再实际执行；
- 参数用数组/具名参数，不拼接脆弱长字符串；
- 原生命令以 LASTEXITCODE 判断成功；
- 中文/UTF-8 文件显式处理编码；
- 不使用 ExecutionPolicy Bypass 绕过门禁。

---

# 11. 当前停止点

本命令包只授权：

~~~text
下载 PQ2_0
-> 完整校验
-> 建立 262144 context server
-> 关闭思考 + KV4
-> 完成一份 240K~245K token 真实长上下文基线
-> 写回远端
-> STOP
~~~

即使 PASS，也不得自动下载 PTQ1_0 或进入下一优化路线。
