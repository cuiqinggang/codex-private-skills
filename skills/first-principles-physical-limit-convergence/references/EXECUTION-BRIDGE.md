# EXECUTION BRIDGE

这是基础设施，不是新的方法阶段。

```text
METHOD = first-principles-physical-limit-convergence
REASONING_BRAIN = ChatGPT_Web
EXECUTOR = Codex
SHARED_FACT_SOURCE = cuiqinggang/codex-private-skills
BRIDGE = playwright-native-ai-browser
```

新版闭环：

```text
STEP-1 PHYSICAL MODEL / DECISION
-> Codex local implementation
-> V1/Vn real run
-> authoritative evidence
-> formal result package
-> GitHub shared fact source
-> remote verify
-> reasoning brain re-reads facts
-> GAP / KEEP / ROLLBACK / NEXT / 99
```

高价值决策点必须返回推理大脑；禁止一次生成长期盲跑的几十步优化任务。

ChatGPT 负责：任务合同、Physical DAG、T_PHY/T_MACHINE_STAR、多智能体策略、Gap 排序、KEEP/ROLLBACK/NEXT/99。
Codex 负责：本机事实核验、受控修改、权威计时、最小真实测试、原始证据、正式报告、Git publication。
GitHub 是持久 shared fact source。浏览器只负责通信，不复制第二套方法 Skill。

多个支持智能体可以并行做只读分析，但单 GPU 正式 benchmark 独占资源，避免并发写同一 repo/worktree，最终由一个 integrator 统一合同、单位与计时边界。
