# 《新页面运行模板 第5版》

版本：第5版  
升级来源：《新页面运行模板 第4版》  
状态：CURRENT

## 1. 目的

新页面只做一件事：

**用最少上下文继续当前任务。**

禁止把完整历史、全部证据、长规则表、长 JSON、重复哈希重新塞进提示词。

## 2. 固定只读 4 个方法文件

```text
ENGINE_PATH=skills/artificial-single-page-extreme-time-engine/ENGINE.md
BRAIN_PATH=skills/artificial-single-page-extreme-time-engine/BRAIN.md
TASK_PATH=skills/artificial-single-page-extreme-time-engine/CURRENT_TASK_CONSTRAINTS.md
TEMPLATE_PATH=skills/artificial-single-page-extreme-time-engine/NEW_PAGE_TEMPLATE.md
```

权威仓库：

```text
REPO=cuiqinggang/codex-private-skills
REF=main 或明确冻结 commit
```

## 3. NEXT_PAGE_PROMPT 最小格式

默认只写：

```text
执行《人工单页面极限短时间引擎 第10版》和《极限短时间执行大脑 第5版》。

REPO=cuiqinggang/codex-private-skills
REF=<main或冻结commit>
读取：ENGINE.md / BRAIN.md / CURRENT_TASK_CONSTRAINTS.md / NEW_PAGE_TEMPLATE.md

任务：<一句话>
冻结事实：<最多3条>
下一步：<一句话>
禁止：<仅真正必要项>
```

正常目标：**10 行左右。**

## 4. 页面规则

- 一个页面只服务一个明确任务；
- 同页完成成熟方案搜索、简单融合、攻击迭代和一次性虚拟成熟；
- 不为微小优化机械换页；
- 复杂证据写文件，不复制进提示词；
- 页面开始卡顿时，立即最小冻结并换页。

## 5. 冻结

只冻结真正影响继续执行的事实：

```text
FINAL_VALID
当前 T*
当前成熟方案
真实 failure class（如有）
下一动作
```

机器标签如自动化确实需要，可以单独存冻结文件；**不再强制把巨大 JSON 放进 NEXT_PAGE_PROMPT 正文。**

## 6. 核心

```text
提示词是交接，不是数据库。
文件存证据，提示词只给下一步。
能短绝不长。
```
