# GPT / ChatGPT Work Reality｜Benchmark Case 001

```ini
TASK_ID=ETAL-v2.0-GPT-WORK-001
CASE_ID=ETAL-v2.0-CASE-001
PAGE_NAME=极限短时间自动化闭环 v2.0
ROLE=MEASURE_PRIMARY_INTELLIGENT_PATH
CORE_BRAIN=GPT
CODEX=NOT_ASSUMED
OBJECTIVE=MEASURE_T_VALID_WORK_CASE_001
```

## 测试题

固定读取：

- `BENCHMARK_SUITE_R1.md`
- `BENCHMARK_CASE_001_DOUYIN.md`
- `REALITY_CONTRACT.md`
- `MATURE_SOLUTION_COMPETITION_R3_GPT_CORE.md`

然后执行 Case 001。

用户只给一次目标和冻结样本：

> 把这条抖音分享链接以完整、有声、可正常播放的视频下载到 Windows 桌面；普通路径选择、成熟方案检索、执行、失败恢复和机器验收自动完成。

## 规则

1. GPT 是核心大脑。
2. 不预设 Codex 必须参与。
3. 优先检索 / 复用已有成熟完成方案。
4. 不重新开发下载器。
5. 不修改 FlClash / Windows 网络代理。
6. 不允许用户做人肉 GPT↔执行器消息总线。
7. 机器可验事实必须自动验收。
8. 全部等待 / 失败 / 恢复计入同一 T_VALID。

## 输出

```ini
PATH=P1_GPT_WORK
CASE_ID=ETAL-v2.0-CASE-001
FLOW_START=
FLOW_END=
T_VALID_WORK_CASE_001=
RESULT=PASS|FAIL
USER_INTERVENTIONS=
RECOVERY_EVENTS=
FALSE_COMPLETION_EVENTS=
CODEX_USED=YES|NO
```

若 P1 需要 Codex 才能完成，不在这一结果里伪装成 Work-only PASS；转入 P2 单独计时。

## FINAL_VALID

完全服从 `BENCHMARK_CASE_001_DOUYIN.md` 的 FINAL_VALID。
