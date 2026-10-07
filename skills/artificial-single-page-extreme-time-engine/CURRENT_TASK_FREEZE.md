# 《当前任务冻结状态规范 第1版》

规范版本：第1版
状态：CURRENT
当前活动任务：NONE

## 1. 作用

本文件/同类任务文件只回答：

> 现在做到哪里？哪些事实已经冻结？下一步从哪里继续？

它不得改写任务目标、正向约束、反向约束或 FINAL_VALID 标准。
这些只由 TASK_CONTRACT / CURRENT_TASK_CONSTRAINTS 管理。

## 2. 全局冻结版本

每个现实任务建立时：

FREEZE_VERSION=0

只要 CEO 正式接受一个新的状态事实，不论结果为 PASS / FAIL / UNKNOWN / BLOCKED，都表示项目状态已经改变：

FREEZE_VERSION=N -> N+1

必须使用自然整数，禁止小数。

并行 Executor 不直接竞争写全局 FREEZE_VERSION：
- 每个 Executor 只产出自己的不可变 NODE_FREEZE_ID；
- CEO 是唯一全局状态写者；
- CEO 按实际接受顺序 Merge；
- 每接受一个导致项目状态变化的结果，FREEZE_VERSION +1。

因此并行不会制造两个相同“下一版本”。

## 3. 每个冻结必须保存

- TASK_ID
- CONTRACT_VERSION
- FREEZE_VERSION
- NODE_FREEZE_ID / CEO_FREEZE_ID
- RESULT_STATUS=PASS|FAIL|UNKNOWN|BLOCKED
- STATE_CODE
- 已冻结事实
- EVIDENCE_LOCATION
- REALITY_DELTA（如有）
- CURRENT_T_STAR
- OPEN_ITEMS
- NEXT_CONTROL_DECISION
- NEXT_NODE
- SOURCE_REPO
- SOURCE_REF
- TIMESTAMP

失败也是有效的新状态；不得因为 FAIL 就丢弃页面成果。

## 4. Executor 冻结

一个 Executor 页面只负责一个完整自然执行节点。

节点结束：
NODE_FREEZE
→ 证据持久化
→ 回报 CEO
→ CEO 接受/登记
→ 页面立即关闭

成功、失败、UNKNOWN 都执行同一生命周期。

Executor 页面禁止被重新分配为第二个自然执行节点。

## 5. CEO 冻结

CEO 到达稳定控制边界时：
CEO_FREEZE
→ 更新 FREEZE_VERSION
→ 生成 CEO_FREEZE_TAG_JSON
→ 刷新 CURRENT_TASK_FREEZE
→ 生成唯一 NEXT_PAGE_PROMPT（如需换页/任务结束）
→ Persist First
→ Close Second

## 6. NEXT_PAGE_PROMPT 命名

下一页提示词必须绑定最新状态版本：

NEXT_PAGE_PROMPT_V<FREEZE_VERSION>

正文必须明确：
CONTRACT_VERSION=<n>
FREEZE_VERSION=<n>

新 CEO 只从最新 FREEZE_VERSION 接管，不重放旧聊天。

## 7. 当前空闲状态

ACTIVE_TASK=NONE
CONTRACT_VERSION=null
FREEZE_VERSION=null
NEXT_NODE=WAIT_FOR_TASK
