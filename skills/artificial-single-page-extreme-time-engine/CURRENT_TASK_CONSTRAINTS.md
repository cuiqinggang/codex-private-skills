# 《当前任务目标与正反约束｜任务合同规范 第2版》

规范版本：第2版
升级来源：第1版
状态：CURRENT
当前活动任务：NONE

## 1. 任务合同只回答“要什么”

任务合同是任务级 Source of Truth。

它锁定：
- 用户最终现实目标；
- 正向必须项；
- 反向禁止项；
- 完成标准；
- 证据标准；
- 用户现实操作路径；
- 范围和硬边界。

它不记录“现在做到哪里”；执行进度由 CURRENT_TASK_FREEZE 管理。

## 2. 初次接到现实任务的固定生成流程

### Step 1：保留用户原始意图
记录 USER_REQUEST_RAW 的最小忠实摘要。
不得先把用户任务改写成某个实现方案。

### Step 2：提炼 FINAL_REALITY_GOAL
只写最终现实结果：
“用户最后真正要得到什么”。

禁止把工具、模型、代码结构、网页步骤等实现偏好误当目标，除非用户明确要求它本身就是结果。

### Step 3：生成 POSITIVE_PROMPT
只列：
- 必须具备；
- 必须保留；
- 不能为了更快而牺牲；
- 用户真正关心的质量/功能/体验。

### Step 4：生成 NEGATIVE_PROMPT
只列：
- 绝不能发生；
- 表面完成但现实不接受；
- 属于目标漂移；
- 降质、绕路、假完成、错误替代；
- 用户已明确禁止的操作。

### Step 5：冻结范围与边界
IN_SCOPE
OUT_OF_SCOPE
HARD_BOUNDARIES

### Step 6：冻结 USER_PATH
写出用户最终最简现实操作路径。
USER_PATH_GATE=FAIL 的方案不得成为正式冠军。

### Step 7：把目标改写为验收标准
FINAL_VALID_STANDARD
DONE_WHEN

要求尽量可观察、可测、可判定。
禁止用“看起来差不多”“应该可以”作为 FINAL_VALID。

### Step 8：定义证据
EVIDENCE_REQUIRED

证据只为证明 DONE_WHEN，不为堆日志。

### Step 9：反向漏洞检查
逐项问：
- 有没有满足文字但没有满足用户真实目标的情况？
- 有没有更快但质量/功能变差的情况？
- 有没有测试器通过、真实任务失败的情况？
- 有没有依靠用户额外人工才能成立的情况？
- 有没有违反 HARD_BOUNDARIES 的情况？

发现漏洞先修合同，不进入执行。

### Step 10：Freeze
第一次冻结：

CONTRACT_VERSION=1
CONTRACT_STATUS=FROZEN
FREEZE_VERSION=0

然后才进入执行。

## 3. 标准任务合同

```yaml
TASK_ID: <唯一任务ID>
CONTRACT_VERSION: 1
CONTRACT_STATUS: FROZEN

USER_REQUEST_RAW: >
  <用户原始意图的最小忠实摘要>

FINAL_REALITY_GOAL: >
  <最终现实结果，不先写实现>

POSITIVE_PROMPT:
  - <必须实现/保留>

NEGATIVE_PROMPT:
  - <禁止/失败/漂移项>

IN_SCOPE:
  - <必须完成>

OUT_OF_SCOPE:
  - <明确不做>

HARD_BOUNDARIES:
  - <不可突破>

USER_PATH:
  - <用户最简操作>

FINAL_VALID_STANDARD:
  - <最终有效标准>

DONE_WHEN:
  - <可验收条件>

EVIDENCE_REQUIRED:
  - <必要证据>

CURRENT_FREEZE_VERSION: 0
```

## 4. 后续执行不得重写合同

后续 CEO：
读当前 CONTRACT_VERSION
→ 读最新 FREEZE_VERSION
→ 继续执行。

以下不改变 CONTRACT_VERSION：
- 换 CEO 页面；
- 换 Executor；
- 节点 PASS/FAIL；
- Reality Delta；
- 修 bug；
- 更换更快成熟路线；
- T* 更新；
- 新增证据。

## 5. CONTRACT_VERSION 升级

只有以下实质变化才：

1 → 2 → 3 → ...

- 用户最终目标改变；
- FINAL_VALID/DONE_WHEN 被 Reality 证明定义错误或不足；
- POSITIVE_PROMPT 改变；
- NEGATIVE_PROMPT 改变；
- 范围或硬边界改变；
- USER_PATH 本身被用户改成新的硬要求。

升级必须记录：
OLD_CONTRACT_VERSION
CHANGE_REASON
DELTA
NEW_CONTRACT_VERSION

旧版本保留，不静默覆盖。

## 6. FINAL_VALID 门

FINAL_VALID=YES 只允许同时满足：

DONE_WHEN 全部满足
+
EVIDENCE_REQUIRED 足够
+
NEGATIVE_PROMPT 未触发
+
HARD_BOUNDARIES 未违反
+
USER_PATH_GATE=PASS（用户型任务）

否则只能 NO 或 UNKNOWN。

## 7. 与冻结状态的分工

TASK_CONTRACT：
应该做什么，什么叫完成。

CURRENT_TASK_FREEZE：
现在做到哪里，哪些事实已经不可重复，下一步从哪里恢复。

两者必须同时存在，不能互相替代。

一句话：

**初次接任务先把用户真实目标变成可验收、可防漂移的合同；后续所有页面只推进状态，不偷偷改题。**
