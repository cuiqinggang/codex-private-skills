# Qwen3.8 / Bonsai 2 27B — 256K 极限短时间现实基线

状态：V1_BLOCKED_SAFELY / V2_READY_TO_RESUME

## 唯一目标

在 262144 上下文窗口、稳定可生产运行的硬条件下，得到当前机器的第一份真实端到端时间基线，并为后续“极限短时间”收敛提供现实锚点。

当前不研究 64K / 128K，不下载第二个模型版本，不做参数扫面，不做推测解码，不做多模态。

只有现实证据证明 256K 在当前硬件与成熟方案下不可成立时，才返回 GPT 决定是否降为 128K。本命令包自身禁止自动降级。

## 当前唯一现实候选

- 模型：Ternary Bonsai 2 27B
- 权重：PQ2_0
- Hugging Face 仓库：prism-ml/Ternary-Bonsai-2-27B-gguf
- 文件：Ternary-Bonsai-2-27B-PQ2_0.gguf
- 官方演示仓库：PrismML-Eng/Bonsai-demo
- 固定上游提交：17b143e889a45c090816b520e79a50c996164e1f
- 该提交 setup.ps1 固定的 llama.cpp 预编译版本：prism-b10709-9a9394a
- 上下文：262144
- KV 缓存：4 位
- 思考模式：关闭
- 并发：单任务
- 视觉模块：不下载、不加载
- 推测解码：关闭
- T_PHY 理论物理极限：关闭

## 文件

- DOWNLOAD-AND-BASELINE-COMMAND-PACK-v1.md：唯一执行来源
- COMMAND-PACK-AUDIT-v1.md：静态审核结果

执行完成后，Codex 必须把真实结果、日志摘要、下载验证、模型哈希、运行配置、256K 请求计时与资源峰值推回本分支，再停止并返回 GPT。

## 方法位置

本任务严格映射到 first-principles-physical-limit-convergence v3.1.2 的三核心：

1. 极限短时间：唯一优化指标仍为真实任务端到端时间。
2. 广域成熟方案池：本轮只把已经收敛出的 PQ2_0 官方成熟路径拿到现实中建立锚点；其余候选仍保留在广域池中，不下载。
3. 高智能虚拟成熟：现实基线返回后再决定下一刀，执行器不得现场扩展新路线。


## 2026-09-19 现实回传与 v2

第一次执行在 Phase B 正确停止：固定上游 `setup.ps1` 不支持 `BONSAI_SKIP_GGUF`，会无条件进入模型下载。结果已冻结在 commit `664a2289ede02d295611384e41fd6777331b369d`。

当前唯一执行入口改为：
- `CURRENT.md`
- `DOWNLOAD-AND-BASELINE-COMMAND-PACK-v2.md`
- `COMMAND-PACK-AUDIT-v2.md`

v2 不再执行 `setup.ps1`，而是直接从同一固定 PrismML llama.cpp release 下载并 SHA256 校验 Windows CUDA 12.4 runtime，再继续唯一 PQ2_0 / 262144 上下文基线。其他目标与禁项不变。
