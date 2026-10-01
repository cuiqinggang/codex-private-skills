# P2 GPT / Work + Codex Reality｜Benchmark Case 001

```ini
TASK_ID=ETAL-v2.0-GPT-CODEX-001
CASE_ID=ETAL-v2.0-CASE-001
ROLE=MEASURE_CODEX_PATH
CORE_BRAIN=GPT
EXECUTOR=Codex
OBJECTIVE=MEASURE_T_VALID_WORK_CODEX_CASE_001
```

## 目的

Codex 在本轮是**测评对象**。

不因为历史上经常使用 Codex 就假设它必须存在。

本测试回答：

> GPT 核心 + Codex 执行，在同一 Case 001 上能否比 P1 更快、更稳或更少人工，并最终降低完整 T_VALID？

## 统一起点

```text
P2_T0 =
GPT 已收到同一用户目标和同一冻结样本，
已经拥有足够信息、不再等待用户补充，
开始现实推进的时间。
```

## 统一终点

完全使用 Case 001 的机器 FINAL_VALID。

## 必须计入

- GPT 判断；
- 成熟方案检索；
- GPT→Codex 交接；
- Codex session / queue / execution；
- Browser / file / GitHub 等执行；
- Codex→GPT 结果回传；
- 普通失败恢复；
- 最终 verifier；
- 所有等待。

不得只报 Codex 内部 execution time。

## 输出

```ini
PATH=P2_GPT_WORK_CODEX
CASE_ID=ETAL-v2.0-CASE-001
FLOW_START=
FLOW_END=
T_VALID_WORK_CODEX_CASE_001=
RESULT=PASS|FAIL
USER_INTERVENTIONS=
RECOVERY_EVENTS=
FALSE_COMPLETION_EVENTS=
```

## 判断

如果 P2 比 P1 快：
- Codex 在此任务类保留为成熟执行组件。

如果 P2 比 P1 慢且没有补齐 VALID 缺口：
- 从该任务类主链删除 Codex。

这不影响 Codex 在其他 Benchmark Case 中重新竞争。
