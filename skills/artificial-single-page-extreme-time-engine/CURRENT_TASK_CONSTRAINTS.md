# 《当前任务目标与正反约束｜任务合同规范 第1版》

规范版本：第1版  
状态：CURRENT  
用途：定义每个现实任务“不漂移”的任务合同  
当前活动任务：NONE

## 1. 核心原则

任务合同负责回答：

> 最终要得到什么？什么必须有？什么绝不能有？怎样才算真正完成？

它不负责回答“具体怎么做”。

任何新现实任务都必须先生成并冻结 TASK_CONTRACT，再进入实现或 Reality。

聊天、CEO、Executor、临时计划、Reality 页面都不得静默改写任务合同。

## 2. 每个任务的合同字段

```yaml
TASK_ID: <唯一任务ID>
CONTRACT_VERSION: 1
CONTRACT_STATUS: DRAFT|FROZEN|SUPERSEDED

FINAL_REALITY_GOAL: >
  <最终现实目标；只写结果，不写实现偏好>

POSITIVE_PROMPT:
  - <必须实现/必须保留的正向要求>

NEGATIVE_PROMPT:
  - <禁止出现；出现即漂移、失败或降级的反向要求>

IN_SCOPE:
  - <必须完成>

OUT_OF_SCOPE:
  - <明确不做>

HARD_BOUNDARIES:
  - <不可突破的现实/安全/环境边界>

FINAL_VALID_STANDARD:
  - <最终有效标准>

DONE_WHEN:
  - <机器或人工可验证完成条件1>
  - <完成条件2>

EVIDENCE_REQUIRED:
  - <文件/日志/截图/Run ID/Hash/实测结果等>

USER_PATH:
  - <用户最简现实操作路径>

CURRENT_FREEZE_VERSION: 0
CURRENT_STATE_CODE: 10
CURRENT_T_STAR_MS: null
```

## 3. 合同如何生成

新任务进入 CEO 后按固定顺序：

1. 读取用户原始任务；
2. 抽取最终现实结果，不把当前实现偏好误写成目标；
3. 写 POSITIVE_PROMPT：必须实现的结果特征；
4. 写 NEGATIVE_PROMPT：禁止项、漂移项、失败项；
5. 明确 IN_SCOPE / OUT_OF_SCOPE / HARD_BOUNDARIES；
6. 把“看起来完成”改写成 FINAL_VALID_STANDARD / DONE_WHEN；
7. 定义 EVIDENCE_REQUIRED；
8. 定义 USER_PATH；
9. 从反面检查：是否存在“形式完成但实际失败”的漏洞；
10. Freeze 为 CONTRACT_VERSION=1。

若任务需要外部成熟标准、真实产品标准或物理边界才能定义 VALID，可以在冻结前做最小必要检索/分析；但检索服务于“把完成标准定义正确”，不能先实现再倒推标准。

## 4. 正提示词 / 反提示词的含义

这里的 POSITIVE_PROMPT / NEGATIVE_PROMPT 是任务级约束，不局限于图像生成。

POSITIVE_PROMPT：
- 最终结果必须具备什么；
- 用户真正要保留什么；
- 哪些质量/功能/体验不能丢。

NEGATIVE_PROMPT：
- 哪些结果即使表面完成也不接受；
- 哪些行为属于目标漂移；
- 哪些降质、绕路、假完成、错误替代必须禁止。

它们与 FINAL_REALITY_GOAL 一起构成“不漂移层”。

## 5. CONTRACT_VERSION 升级规则

每个任务从 1 开始，只允许自然整数：

1 → 2 → 3 → 4 …

只有以下情况允许升级：
- 用户明确改变最终目标；
- Reality/证据证明原 FINAL_VALID 定义错误或不足；
- 正向要求确实新增/删除/改变；
- 反向禁止项确实新增/删除/改变；
- 任务范围或硬边界发生真实变化。

以下情况不得升级 CONTRACT_VERSION：
- 换 Executor；
- 换实现路线；
- 页面换页；
- 节点完成；
- Reality FAIL；
- 修 bug；
- 仅更新 T*；
- 仅新增证据；
- 仅推进状态。

合同升级必须显式写：
OLD_CONTRACT_VERSION
→ CHANGE_REASON
→ DELTA
→ NEW_CONTRACT_VERSION

禁止静默覆盖旧合同。

## 6. FREEZE_VERSION 与合同版本分离

FREEZE_VERSION 表示“做到哪里”。

每个 CEO 自然控制节点完成后：

FREEZE_VERSION=N → N+1

即使 CONTRACT_VERSION 不变，FREEZE_VERSION 也继续上升。

例：

CONTRACT_VERSION=1  
FREEZE_VERSION=1  
FREEZE_VERSION=2  
FREEZE_VERSION=3

如果中途用户改变最终验收标准：

CONTRACT_VERSION=2  
FREEZE_VERSION=4

因此：
- CONTRACT_VERSION = 目标/验收定义版本；
- FREEZE_VERSION = 项目状态版本。

不得混用。

## 7. FINAL_VALID 门

FINAL_VALID=YES 只允许在：

DONE_WHEN 全部满足
+
EVIDENCE_REQUIRED 全部具备
+
NEGATIVE_PROMPT 无触发
+
HARD_BOUNDARIES 无违反

否则：
FINAL_VALID=NO 或 UNKNOWN。

## 8. 新 CEO 的合同读取规则

新 CEO 不重新发明任务目标。

固定：
读取当前 FROZEN TASK_CONTRACT
→ 读取最新 CEO_FREEZE
→ 校验 CONTRACT_VERSION / FREEZE_VERSION
→ 基于新状态刷新执行计划

只有发现合同本身需要修订，才进入 CONTRACT_REVISION 并自然数 +1。

## 9. 当前空闲状态

当前没有绑定具体现实任务：

ACTIVE_TASK=NONE  
ACTIVE_CONTRACT_VERSION=null  
ACTIVE_FREEZE_VERSION=null

收到下一现实任务时：
先生成 TASK_CONTRACT_VERSION=1；
再进入 PAGE_TOPOLOGY_GATE。

一句话：

**目标、FINAL_VALID、正向要求、反向禁止项用 CONTRACT_VERSION 锁死；执行过程只推动 FREEZE_VERSION，不允许借“执行中调整”偷偷漂移任务。**
