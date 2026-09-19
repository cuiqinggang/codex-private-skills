# Bonsai 2 27B PQ2_0 — 256K 下载与现实基线命令包 v2

状态：READY_FOR_CODEX / SUPERSEDES_v1_PHASE_B / NOT_EXECUTED

## 0. 本轮只修复一个阻断

v1 已完成 Phase A，远端结果：
- RESULT commit: 664a2289ede02d295611384e41fd6777331b369d
- Phase A: PASS
- 阻断：固定上游 setup.ps1 不支持 BONSAI_SKIP_GGUF，并在第 373 行无条件调用 Download-GgufModel。

本 v2 不重做完整 Phase A，不修改模型目标，不增加候选。
唯一修复：

~~~text
不再执行 setup.ps1
-> 按同一固定上游 release 直接安装 Windows CUDA runtime
-> 再只下载 PQ2_0
-> 继续 256K 基线
~~~

如果任何未定义阻断出现：保存证据、RETURN_TO_GPT、STOP。

---

# 1. 冻结合同

~~~text
SKILL_ID=first-principles-physical-limit-convergence
SKILL_VERSION=3.1.2
TARGET_CONTEXT=262144
ONLY_MODEL=Ternary-Bonsai-2-27B-PQ2_0.gguf
PTQ1_0=FORBIDDEN
MMProj=FORBIDDEN
DRAFT_MODEL=FORBIDDEN
THINKING=OFF
SPECULATIVE=OFF
KV4=ON
CONCURRENCY=1
TEXT_ONLY=YES
T_PHY=OFF

DO_NOT_CHANGE_PROXY=YES
DO_NOT_CHANGE_SYSTEM_NETWORK=YES
DO_NOT_CHANGE_UNRELATED_SYSTEM_SETTINGS=YES
NO_CONTEXT_SWEEP=YES
NO_PARAMETER_SWEEP=YES
NO_AUTO_128K_FALLBACK=YES
~~~

唯一目标：

~~~text
262144 上下文稳定可运行
+
得到真实 T_END_TO_END
~~~

---

# 2. 复用已验证 Phase A

必须先远端回读：
- workspaces/qwen38-bonsai2-256k/results/20260919-224518/RESULT.md
- workspaces/qwen38-bonsai2-256k/results/20260919-224518/RESULT.json

确认：
~~~text
phase_a=PASS
setup_executed=false
model_download_started=false
~~~

只做最小漂移检查，不重跑完整 Phase A：
- pwsh 仍可用；
- aria2c 仍可用；
- RTX 2080 Ti 仍可见；
- C: 可用空间仍 > 20 GiB；
- 不存在已启动的本项目 llama-server。

若漂移检查失败，停止。

---

# 3. Phase B v2 — 不执行 setup.ps1，直接安装固定 CUDA runtime

固定上游：

~~~text
BONSAI_DEMO_COMMIT=17b143e889a45c090816b520e79a50c996164e1f
LLAMA_RELEASE=prism-b10709-9a9394a
~~~

本机 driver 报告 CUDA 13.1。按该固定 setup.ps1 的原始选择逻辑：
- >= 13.3 才选 cuda-13.3
- >= 12.4 且 < 13.3 选 cuda-12.4

因此本轮唯一 runtime：

~~~text
CUDA_VARIANT=12.4
~~~

必须使用以下两个官方 release asset：

1) llama-prism-b10709-9a9394a-bin-win-cuda-12.4-x64.zip
- bytes=253442371
- sha256=f565c8428c1f108311f65ed97f02425188b3aa3c745c2bc597521bbd24bcbbc9

2) cudart-llama-bin-win-cuda-12.4-x64.zip
- bytes=391443627
- sha256=8c79a9b226de4b3cacfd1f83d24f962d0773be79f1e7b75c6af4ded7e32ae1d6

来源：
~~~text
https://github.com/PrismML-Eng/llama.cpp/releases/tag/prism-b10709-9a9394a
~~~

下载 URL 使用对应 release/download 地址。

## 3.1 runtime 下载也使用固定下载法

不能用 Invoke-WebRequest 直接盲下。

每个 asset 都：

~~~text
测速 -> 选择并行度 -> 续传 -> 监控 -> SHA256 -> 解压
~~~

优先 aria2c，同一 partial 文件：
- x1/s1 最多 30 秒；
- 未完成时 x4/s4 继续最多 30 秒；
- 只有 x4 稳定且仍有明显余量时再 x8/s8；
- 如果测速阶段已经下载完成，立即校验，不再额外测速。

必须保留：
- runtime-download-probes.json
- runtime-download-monitor.csv
- runtime-download-final.json

aria2 必须：
~~~text
continue=true
auto-file-renaming=false
allow-overwrite=false
file-allocation=none
max-tries>=5
retry-wait>=2
timeout>=30
~~~

不得删除 partial 后重下。

## 3.2 runtime 校验与安装

两个 ZIP：
- 精确字节数匹配；
- SHA256 精确匹配；
- 才允许 Expand-Archive。

目标目录：

~~~text
C:\AI\Bonsai2-27B-256K\Bonsai-demo\bin\cuda
~~~

不得删除未知既有目录。若目标已有内容：
- 先记录文件列表与 hash；
- 只有确认是本项目旧 runtime 且与固定 release 不一致时才备份到本项目 backup 子目录；
- 不做系统级修改。

解压完成必须存在：
~~~text
bin\cuda\llama-server.exe
bin\cuda\llama-cli.exe
~~~

写入与上游一致的：
~~~text
bin\cuda\.llama_release
prism-b10709-9a9394a cuda-12.4
~~~

运行：
~~~text
llama-server.exe --version
~~~

并保存 stdout/stderr/exit code。

必须证明：
~~~text
RUNTIME_SOURCE=PINNED_RELEASE
CUDA_VARIANT=12.4
RUNTIME_HASH_VERIFIED=YES
CUDA_BINARY_EXISTS=YES
SETUP_PS1_EXECUTED=NO
MODEL_FILES_DOWNLOADED_DURING_RUNTIME_PHASE=0
~~~

---

# 4. Phase C — 只下载 PQ2_0

唯一文件：

~~~text
HF_REPO=prism-ml/Ternary-Bonsai-2-27B-gguf
HF_FILE=Ternary-Bonsai-2-27B-PQ2_0.gguf
HF_RESOLVE=https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf/resolve/main/Ternary-Bonsai-2-27B-PQ2_0.gguf?download=true
~~~

禁止：
~~~text
PTQ1_0
F16
mmproj
dspark
其他模型
~~~

## 4.1 元数据

下载前保存：
- resolve HEAD/redirect headers；
- 可获得的 exact size；
- ETag / X-Linked-Size / LFS/Xet 元数据；
- 若可获得远端 SHA256/LFS OID则保存。

若远端 SHA256 不可直接获得：
~~~text
HASH_SOURCE=LOCAL_ONLY
~~~
但最终本地 SHA256仍必须计算。

## 4.2 模型固定下载法

仍用：
~~~text
PROBE -> SELECT -> CONTINUE -> MONITOR -> VERIFY
~~~

aria2 同一 partial：
1. x1/s1 30 秒；
2. x4/s4 续传 30 秒；
3. x4稳定且仍可能收益时才 x8/s8；
4. 选择“真实平均速度最快且稳定”的配置继续；
5. 30 秒记录一次 bytes / delta / MiB/s / process_alive；
6. 连续 60 秒无增长，或连续约120秒低于最佳稳定测速50%，保留 partial，停止当前进程，重新测速后续传。

如 Hugging Face/Xet 对 aria2 分段不兼容：
- 不修改代理；
- 不删除已下载有效数据；
- 可使用本机已有 hf/huggingface-cli；
- 若本机没有 hf，但已有兼容 Python，则只允许在本项目目录创建隔离 venv 并安装 huggingface_hub；
- 禁止系统级 Python/winget 安装；
- fallback 也必须支持续传/缓存，并记录原因。

完成：
- 精确字节数校验；
- 本地 SHA256；
- 若有远端 SHA256则精确比对；
- 基础 GGUF 可读性检查；
- 验证通过后原子放置到：

~~~text
C:\AI\Bonsai2-27B-256K\Bonsai-demo\models\bonsai2-gguf\27B\Ternary-Bonsai-2-27B-PQ2_0.gguf
~~~

---

# 5. Phase D — 256K 服务

显式环境：

~~~text
BONSAI_FAMILY=bonsai2
BONSAI_MODEL=27B
BONSAI_CTX=262144
BONSAI_KV4=1
BONSAI_SPECULATIVE=0
BONSAI_NGL=99
~~~

禁止 auto context。

使用固定上游：
~~~text
scripts\start_llama_server.ps1
~~~

注意：固定版本的 27B launcher 会重建 ServerArgs，默认保持 thinking；因此本轮必须在脚本尾部参数中显式覆盖：

~~~text
--reasoning-budget 0
--reasoning-format none
--chat-template-kwargs {"enable_thinking":false}
~~~

若最后一个 chat-template 参数在实际 binary 不兼容：
- 不猜测新参数；
- reasoning-budget=0 和 reasoning-format=none 仍是硬门禁；
- 保存错误与 /props/响应证据后返回 GPT。

启动后验证：
~~~text
/health=PASS
/props effective context=262144
CUDA binary active
KV4 active
thinking off
speculative off
~~~

任一关键项失败：停止，不做长 prompt。

---

# 6. Phase E — 唯一 256K 现实基线

模型窗口：
~~~text
262144
~~~

实际 prompt：
~~~text
240000..245000 tokens
~~~

使用 server tokenizer 实际计数，不按字符数猜。

保留三个固定随机标记：
- BEGIN_MARKER
- MIDDLE_MARKER
- END_MARKER

末尾任务：
~~~text
只返回 JSON：
begin=<BEGIN_MARKER>
middle=<MIDDLE_MARKER>
end=<END_MARKER>
sum=42
不解释。
~~~

生成：
~~~text
max_tokens<=128
temperature=0
~~~

权威：
~~~text
T_END_TO_END = 发出真实长请求 -> 收到完整有效 JSON
~~~

同时保存：
- actual_prompt_tokens
- prompt_ms
- prompt_tokens_per_second
- generated_tokens
- generation_ms
- generation_tokens_per_second
- T_END_TO_END
- 1秒粒度 GPU VRAM/util/temp/power
- system RAM used/available
- peak VRAM/headroom
- peak RAM/headroom

PASS：
~~~text
no OOM
no crash
no context truncation
JSON parseable
3 markers exact
sum=42
post-health PASS
~~~

失败后：
~~~text
NO_AUTO_128K
SAVE_EVIDENCE
RETURN_TO_GPT
STOP
~~~

---

# 7. 结果与停止点

创建新的结果目录，不覆盖第一次 BLOCKED 结果：

~~~text
workspaces/qwen38-bonsai2-256k/results/<new_timestamp>/RESULT.md
workspaces/qwen38-bonsai2-256k/results/<new_timestamp>/RESULT.json
~~~

必须特别记录：
~~~text
prior_blocker_commit=664a2289ede02d295611384e41fd6777331b369d
runtime_bootstrap_method=PINNED_RELEASE_DIRECT
setup_ps1_executed=false
runtime_asset_hashes
model_sha256
effective_context
actual_prompt_tokens
download_probe_best_mib_s
download_total_seconds
T_END_TO_END
prompt_tokens_per_second
generation_tokens_per_second
peak_vram_mib
vram_headroom_mib
peak_system_ram_mib
system_ram_headroom_mib
marker_check
post_health
next_action=RETURN_TO_GPT
~~~

然后：
- 精确 stage 本轮新增结果/证据；
- 禁止 git add .；
- commit；
- push 同一分支；
- 远端回读 RESULT.md / RESULT.json；
- remote verify；
- STOP。

即使 PASS，也不自动下载 PTQ1_0，不进入下一优化。
