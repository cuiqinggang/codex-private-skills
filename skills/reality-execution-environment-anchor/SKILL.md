---
name: reality-execution-environment-anchor
description: 现实执行环境精确锚定与数字孪生基线。只读采集 TARGET 运行时与 COLLECTOR 宿主事实，生成安全指纹、漂移证据和 Exact Twin 输入；部分或失败基线也追加归档，但不得冒充 Environment-99。
metadata:
  version: "1.1.0"
  status: REALITY_ANCHOR_COMPLETE
---
# 现实执行环境精确锚定与数字孪生基线
本技能服务于“成熟方案集群 + 高智能虚拟成熟”，不是第四核心。
用途：采集现实 Codex 执行环境、建立现实指纹、保存 Exact Twin 输入、比较漂移、追加历史版本，为 Virtual-99 / Environment-99 提供真实地基。
固定原则：REALITY_FIRST（现实事实优先）、NO_GUESSING（禁止猜测）、READ_ONLY_CAPTURE_FIRST（先只读采集）、NO_ENVIRONMENT_HARDENING_DURING_CAPTURE（采集期间禁止硬化）、GPT_DESIGNS_HARDENING（由 GPT 设计硬化）、CODEX_DETERMINISTIC_EXECUTOR_ONLY（Codex 只确定性执行）、HISTORY_APPEND_ONLY（历史只追加）。
当前为 REALITY_ANCHOR_COMPLETE，TWIN_INPUT_READY=YES；当前权威状态见 snapshots/2026-09-21-r2/45-REALITY-ENVIRONMENT-ANCHOR-R2-FINAL.json，权威指纹见同目录 46-REALITY-FINGERPRINT-V3.json。辅助可观测状态未全部 PASS，不影响已冻结的当前 TARGET 失败语义；ENVIRONMENT_99=NOT_YET。


## v1.1.0 完整归档升级

v1.0.0 的 R1/R2 数据与最终 Reality Fingerprint V3 全部保留。
v1.1.0 新增 COLLECTION-PROCESS-R1-R2.md，固化完整采集、双上下文、失败、恢复、远端安全镜像和最终收口过程。
唯一正式 Twin 消费者：first-principles-physical-limit-convergence@3.1.6/components/exact-reality-digital-twin@1.0.0。
历史只追加，不覆盖。
