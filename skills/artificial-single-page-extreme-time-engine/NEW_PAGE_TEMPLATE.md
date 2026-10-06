# 《新页面运行模板 第6版》

版本：第6版  
升级来源：《新页面运行模板 第5版》  
状态：CURRENT

## 1. 权威来源：必须标明网络共同工作区

每个新页面都必须明确：

```text
权威来源=网络共同工作区
REPO=cuiqinggang/codex-private-skills
REF=<main或冻结commit>
```

并读取固定 4 个文件：

```text
ENGINE_PATH=skills/artificial-single-page-extreme-time-engine/ENGINE.md
BRAIN_PATH=skills/artificial-single-page-extreme-time-engine/BRAIN.md
TASK_PATH=skills/artificial-single-page-extreme-time-engine/CURRENT_TASK_CONSTRAINTS.md
TEMPLATE_PATH=skills/artificial-single-page-extreme-time-engine/NEW_PAGE_TEMPLATE.md
```

**禁止先去 C 盘寻找方法文件。**

## 2. 三行信封：唯一强制标签

每次派发和回报只强制这三行：

```text
【页面名｜任务名｜序号｜虚/实】
状态机：<版本｜状态码｜阶段>
时间锚：TASK_ACCEPTED=<时间>｜CURRENT=<时间/节点>｜ELAPSED=<整体已用>｜T_VALID=<数值或null>｜T*=<数值或null>
```

### 四字段定位

固定只有 4 个字段：

```text
页面名｜任务名｜序号｜虚/实
```

- 页面名只用于机器定位，可自动生成；用户无需记忆。
- 任务名用于识别当前任务。
- 序号用于顺序。
- 虚/实用于区分虚拟成熟与 Reality。

### 状态机

仅保留：

```text
10 准备
20 虚拟成熟
30 虚实交接
40 Reality/验收
100 完成或冻结
```

### 时间锚

时间不能省，因为本方法的核心就是极限时间。

未产生的 T_VALID / T* 用 `null`，禁止写 N/A。

## 3. NEXT_PAGE_PROMPT 最小格式

正常只需要：

```text
【<页面>｜<任务>｜<序号>｜<虚/实>】
状态机：<版本｜状态码｜阶段>
时间锚：TASK_ACCEPTED=<...>｜CURRENT=<...>｜ELAPSED=<...>｜T_VALID=<...>｜T*=<...>

权威来源=网络共同工作区
REPO=cuiqinggang/codex-private-skills
REF=<main或冻结commit>
读取：ENGINE.md / BRAIN.md / CURRENT_TASK_CONSTRAINTS.md / NEW_PAGE_TEMPLATE.md

任务：<一句话>
冻结事实：<最多3条>
下一步：<一句话>
禁止：禁止自研、禁止从零重建；其他仅写真正必要项
```

目标：通常 12 行左右，不写长篇协议。

## 4. 明确删除

NEXT_PAGE_PROMPT 不再默认携带：

- 巨大 CEO_FREEZE_TAG_JSON；
- freeze_id / node_id / claim namespace；
- 大量 SHA256；
- 完整历史；
- 全量证据；
- HIPE/JEV 内部说明；
- DAG 说明；
- 长候选表；
- 重复的禁止清单；
- 为页面名称编写的人类说明。

这些需要时写入证据文件，不进入交接提示词。

## 5. 页面结束

只冻结继续执行真正需要的内容：

```text
FINAL_VALID
当前 T*
当前成熟方案
真实 failure class（如有）
下一动作
```

提示词是交接，不是数据库。

## 6. 核心

```text
网络共同工作区找方法
三行信封做定位
时间锚永远保留
正文只传下一步
证据放文件
禁止自研
```
