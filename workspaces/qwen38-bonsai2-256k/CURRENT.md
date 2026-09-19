# Qwen3.8 / Bonsai 2 27B 256K — 当前执行入口

当前正式命令包：

`DOWNLOAD-AND-BASELINE-COMMAND-PACK-v2.md`

原因：v1 的 Phase B 假定固定上游 setup.ps1 支持 BONSAI_SKIP_GGUF；第一次现实执行证明该变量不存在，且 setup.ps1 会无条件进入模型下载。v1 因此正确 BLOCKED 并保留为历史证据。

v2 只修复这一点：绕过 setup.ps1，直接从同一固定 PrismML llama.cpp release 下载并校验 CUDA runtime，然后继续唯一 PQ2_0 + 262144 上下文基线。

第一次 BLOCKED 结果：
`results/20260919-224518/`

当前仍不授权 PTQ1_0、128K fallback、视觉塔、drafter、推测解码或其他候选。
