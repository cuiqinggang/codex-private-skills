# 路径A｜GPT原生全自动 Reality｜标准题001

```ini
TASK_ID=ETAL-v2.0-GPT-A-001
CASE_ID=ETAL-v2.0-CASE-001
PATH=A
CORE_BRAIN=GPT
CODEX=NO
MANUS=NO
EXECUTION_BRIDGE=extreme-time-automation-bridge
USER_INTERVENTION_DURING_TASK=0
OBJECTIVE=MEASURE_FULL_T_VALID
```

## 唯一可见输入

正式起表时只读取：
- BENCHMARK_SUITE_R2.md
- BENCHMARK_CASE_001_FULL_LIFECYCLE_R2.md
- 冻结后的标准题001原始需求
- 必要现实环境与权限边界

不得读取历史最终实现、历史修复答案、最终冻结代码。

## 路径定义

GPT负责需求理解、成熟方案检索、比较、组合、根因判断、修正/换路与最终判断。
Windows现实操作通过“极限短时间自动化执行桥”完成。执行桥没有决策权。

正式任务运行期间，用户不得作为 GPT↔Windows 消息总线；任何一次人工复制命令、转述结果、选择下一步或人工补验收都使本轮 PATH_VALID=NO。

## 起表前门禁

先完成 ETAL-BRIDGE-SMOKE-001。
桥未 Reality PASS 时，Case 001 不起表。

## 输出

```ini
PATH=A_GPT_AUTONOMOUS
FLOW_START=
FLOW_END=
T_VALID=
FINAL_VALID=YES|NO
PATH_VALID=YES|NO
USER_INTERVENTIONS=0
RECOVERY_EVENTS=
FALSE_COMPLETION_EVENTS=
```
