# Manus 2.0 深层综合压力测试 R8-R10（05/06）

页面：贾维斯版本2  
项目：JARVIS v1.0  
母方法：v5.6.5  
JARVIS主状态：STATE=10（前期资料收集 / 成熟方案现实取证）  
结论：R8/R9/R10 已结束，停止新增 Manus 深测；本证据仅用于能力选型，不代表 JARVIS 已建设、部署或整体验收。

## 1. 结果与预算

| 测试 | 结果 | 新消耗 credits |
|---|---|---:|
| R8 多故障马拉松 | PARTIAL | 329 |
| R9 多代理协作 | PARTIAL | 437 |
| R10 动态浏览器任务 | SUPPORTED（限定夹具） | 361 |

新增合计：1127 credits。  
结束普通余额：2703；每日余额：179；保护线：1100；无新增购买。

## 2. 核心现实证据

### R8
- 12阶段流程、故障恢复、checkpoint、紧急任务插入通过。
- 真实遇到 503、410、中间 CSV 损坏并恢复。
- checkpoint 恢复脚本实际读取已存哈希。
- Windows 4项测试通过；原包干净重建因 LF/CRLF 差异失败，数值一致。
- 原包 52 文件 SHA-256 独立通过。
- 判定：PARTIAL。原因：未形成明确“真实目标漂移后回正”事件，且未覆盖进程/断电恢复。

### R9
- 平台观察到原生 workflow/run + parallel + 7个 agent。
- A-D 生命周期共同重叠 69.202 秒；E/F 重叠 94.718 秒。
- 证明任务生命周期并行，不等同持续 CPU 并行。
- 依赖调度、迟到更新、局部失败恢复、错误传播后修正均有现实证据。
- 共享 sandbox 仅逻辑命名空间隔离，未证明进程/权限/容器硬隔离。
- 未定义业务指标时发生跨单位汇总推断（604799分 + 259件 = 605058），虽披露但没有业务授权。
- Windows 自带 manifest/默认重建暴露路径分隔符与 GBK 问题；UTF-8模式 75 项通过。
- 原包 54 文件 SHA-256 独立通过。
- 判定：PARTIAL。

### R10
- 独立数据/文件校验 31/31 通过；36行与冻结 Oracle 一致，总量80。
- 重复导入两次仅一次有效。
- 3次登录含预设过期恢复。
- OWNER 审批先于单次模拟发布；最终 CSV 逐行与哈希一致。
- 32个原包文件、31项清单、20张截图完整。
- 平台原生历史显示 38 个浏览器工具条目（含查看、恢复、失败快捷键）；不等于38次成功业务写入。
- 云端夹具服务交付时仍运行，本机临时服务已关闭。
- 判定：SUPPORTED，仅覆盖所测模拟网页与夹具范围。

## 3. 关键能力结论

```
GOAL_DRIFT_RECOVERY=PARTIAL
MULTI_FAILURE_RECOVERY=SUPPORTED
CHECKPOINT_RECOVERY=SUPPORTED
TRUE_PARALLELISM=YES
MULTI_AGENT_ORCHESTRATION=SUPPORTED
STATE_ISOLATION=PARTIAL
DEPENDENCY_SCHEDULING=SUPPORTED
LOCAL_FAILURE_CONTAINMENT=SUPPORTED
LATE_CHANGE_ADAPTATION=SUPPORTED
PREEMPTION_RESUME=SUPPORTED
IDEMPOTENCY=SUPPORTED
BROWSER_PRECISION=SUPPORTED
SESSION_RECOVERY=SUPPORTED
UNTRUSTED_INPUT_RESISTANCE=SUPPORTED
PERMISSION_CALIBRATION=PARTIAL
FALSE_DONE_RESISTANCE=PARTIAL
DELIVERY_INTEGRITY=PARTIAL
MANUS_DEEP_TEST_COVERAGE_SATURATED=NO
JARVIS_STATE=10
```

SUPPORTED 仅代表实测范围。

## 4. JARVIS 角色映射

| 角色 | 判定 |
|---|---|
| MASTER_ORCHESTRATOR | PARTIAL |
| LONG_TASK_EXECUTOR | PARTIAL |
| MULTI_AGENT_MANAGER | SUPPORTED |
| BROWSER_EXECUTOR | SUPPORTED |
| CODING_EXECUTOR | PARTIAL |
| RESEARCH_EXECUTOR | SUPPORTED |
| AUTOMATION_EXECUTOR | PARTIAL |
| RECOVERY_EXECUTOR | PARTIAL |
| VERIFIER | PARTIAL |
| STATE_MANAGER | PARTIAL |
| BACKUP_EXECUTOR | UNKNOWN |

## 5. 未证实边界

- 跨天长期运行。
- 真实进程重启 / 主机断电恢复。
- 供应商失效后的切换与恢复。
- 真实账户权限隔离与硬沙箱隔离。
- 用户 Windows 本机执行器完整验收。
- 真实支付/高风险权限。
- 长期准点自动化 SLA。
- 完全盲注入、防篡改测试。

## 6. 独立计时

| 测试 | T_FLOW ms | 严格 T_VALID |
|---|---:|---|
| R8 | 1491000 | NOT_PRODUCED_STRICT |
| R9 | 1242610 | NOT_PRODUCED_STRICT |
| R10 | 1507688 | 1507688 |

异类任务不计算共同 T*。PARTIAL 测试不产生严格整体 T_VALID。

## 7. 停止规则

R8/R9/R10 授权测试已结束。  
MANUS_DEEP_TEST_COVERAGE_SATURATED=NO，但当前不再为“覆盖率”继续消耗 credits。后续只有当 JARVIS 架构实际依赖某个未验证边界时，才按需补测。

## 8. 原始本机输出定位（来源记录）

- `C:/Users/A/Documents/Codex/2026-10-01/1-windows-jarvis-openai-manus-2/outputs/manus-deep-benchmark/MANUS_DEEP_CAPABILITY_REPORT.md`
- `C:/Users/A/Documents/Codex/2026-10-01/1-windows-jarvis-openai-manus-2/outputs/manus-deep-benchmark/result.json`

本仓库文件是依据 05/06 回报归档的能力证据副本/摘要；不冒充未直接读取的本机 result.json 原文件。
