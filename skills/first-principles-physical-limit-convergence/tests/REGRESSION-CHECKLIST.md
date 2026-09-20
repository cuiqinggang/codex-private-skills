# Regression Checklist — v3.1.5

## 三核心方法

- [x] 当前方法只允许三个核心：极限短时间、成熟方案集群、高智能虚拟成熟。
- [x] 不存在第四核心。
- [x] 不存在“修复”这一独立方法路径。
- [x] 现实验证不是第四核心，只验证已冻结方案。
- [x] 任何失败如果需要改变冻结方案，必须返回 GPT 页面。

## 四字段任务定位

- [x] 正式标签格式固定为：`【页面名｜任务名｜序号｜核心归属】`。
- [x] 第四字段只允许三个中文核心名。
- [x] 第四字段禁止英文/数字别名。
- [x] 标签核心必须和任务正文真实工作一致。
- [x] 一条命令不得跨多个核心；必须先由 GPT 拆分。
- [x] 首行和末行定位标签必须完全一致。
- [x] 执行器最终回传最后一行必须原样 echo 四字段标签。

## 序号

- [x] 序号只表示 GPT 正式命令顺序。
- [x] 不存在 4..6 修复窗口。
- [x] 未闭环后是否存在新命令，只能由 GPT 页面决定。
- [x] 执行器不得把后续序号解释为修复权限。

## 执行器边界

- [x] GPT=方案判断、成熟方案组合、高智能虚拟成熟、重新冻结。
- [x] Codex/Reasonix/本地执行器=冻结命令执行器。
- [x] 执行器可以收集事实和 Reality Delta。
- [x] 执行器不得自行建立修复任务。
- [x] 执行器不得自行决定修复办法。
- [x] 执行器不得自行重新设计或增加路线。
- [x] 执行器不得自行修改模型、阈值、路由、fallback、验证合同。
- [x] 现实失败后必须 STOP 并返回 GPT 页面。

## 随机系统

- [x] ATTEMPT / DELIVERY 等历史能力只作为三个核心内部工具。
- [x] 任何自动 retry 必须来自 GPT 已冻结的合同，不构成 Codex 自由修复。
- [x] exact-seed 或其他任务合同继续受冻结合同约束。
- [x] 执行器不得因随机失败自行更换算法/路径。

## Automation

- [x] GitHub 可作为共享正式执行源。
- [x] checkpoint / 幂等 / ACTION_ID 等只作为执行工具。
- [x] 浏览器桥接只负责 transport。
- [x] 全局 Codex 接收门禁必须最终升级到四字段格式。
- [x] 即使 Skill 未加载，全局门禁仍必须阻止缺失/非法核心字段与执行器自行修复。

## Non-regression assertions

```text
THREE_CORE_ONLY=PASS
FOURTH_CORE_EXISTS=NO
FOUR_FIELD_LOCATOR=PASS
CHINESE_CORE_ONLY=PASS
REPAIR_WINDOW_EXISTS=NO
CODEX_EXECUTOR_ONLY=PASS
CODEX_SELF_REPAIR=FORBIDDEN
REAL_FAILURE_RETURNS_TO_GPT=PASS
NO_REAL_EXECUTION_REPLAN_LOOP=PASS
HISTORY_PRESERVED_AS_EVIDENCE_ONLY=YES
```
