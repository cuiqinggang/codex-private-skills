# FAILURE INDEX — v1.0

正常任务只在触发条件命中时查。

- FI-N01：把 CURRENT 放回第一步。FAST_PATH：先算 T_PHY/T_MACHINE_STAR；V1 CURRENT 只是迭代输入。
- FI-N02：把成熟方案当目标。FAST_PATH：成熟方案只做 optional evidence。
- FI-N03：为了过 99 移动目标。FAST_PATH：target revision 必须有新证据与被推翻假设。
- FI-N04：强制单点精确预测。FAST_PATH：用区间、置信度、敏感度。
- FI-N05：无限制加智能体。FAST_PATH：通过 Agent Spawn Gate，只在净墙钟收益 > 0 时增加。
- FI-N06：多个 GPU-heavy worker 污染 benchmark。FAST_PATH：GPU benchmark 独占串行，辅助分析可并行。
- FI-N07：计时忽略 GPU 异步。FAST_PATH：CUDA Event / synchronize。
- FI-N08：去重甲改变任务。FAST_PATH：删除前后必须验证同一 TASK_CONTRACT 和结果身份。
- FI-N09：本机 PASS 但共同仓库未收口。FAST_PATH：formal report -> exact stage -> commit -> push -> remote verify。
- FI-N10：不可逆 instrumentation。FAST_PATH：hash before -> backup -> patch -> run -> restore -> hash proof。
- FI-N11：为了全面重新扫描。FAST_PATH：canonical skill/shared facts -> gap-only verification。
- FI-N12：预先设计大量阶段。FAST_PATH：结构从物理依赖和 Gap 自然产生。

旧技能环境级经验仍有效，不复制整份避免双源漂移。需要时读取 `skills/absolute-time-fireworks-optimization/references/FAILURE-INDEX.md`。旧 FI-14 Shared Fact Source Closure Omitted 已直接继承。
