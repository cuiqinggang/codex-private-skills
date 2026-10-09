# 《自动化B·单层页面极限短时间引擎》｜当前唯一方法指针

CURRENT_ENGINE=B33
CURRENT_BRAIN=B29
CURRENT_TEMPLATE=B23
ROUTE=B｜STATUS=METHOD_READY_FOR_VIRTUAL_MATURITY｜VIRTUAL_MATURE=NO｜FINAL_VALID=NO

## 版本继承（本技能包只有一份28版共同总纲）
- `ENGINE_B_V33.md` → B32 → B31 → B30 → B29 → `../../ENGINE.md` 第28版；
- `BRAIN_B_V29.md` → B28 → B27 → B26 → `../../BRAIN.md` 第25版；
- `NEW_PAGE_TEMPLATE_B_V23.md` → B22 → B21 → B20 → B19 → `../../NEW_PAGE_TEMPLATE.md` 第18版。

## 一条最短执行主线
GPT（当前用户ChatGPT普通浏览器页面）读取统一SKILL/START入口→本B指针与大脑→任务合同/Freeze→保守规划一个流畅自然节点→GPT连续实际执行并处理可修复卡点→节点完成或一轮合理修复仍无法推进则**先持久化冻结**→实际任务已FINAL_VALID则结束，否则现成 Windows 桥调用本路线薄GUI接力工具，在**同一浏览器窗口**点击“新聊天”并一次提交短状态码→新GPT页读取指针继续剩余任务。

**B默认不使用 n8n、专用浏览器或CDP 9223**；不用独立GPT Executor。无多路派发/回传/合并，无每节点临时计算留页收益。运行规则必须遵守总纲的成熟复用、权限、Exactly-once三态与真实有效时间指标。

## 接力成熟组件
- 既有 AutoHotkey v2 和成熟 UIA-v2（上游 Descolada/UIA-v2，锁定外部提交 `2846a9b10518a95cf26a6c43671a9512b231ccb7`）负责同一Chrome现有窗口内控件交互；最小适配 `adapter/B33_Handoff.ahk`。由GPT在当前有效Freeze的真实确认后通过既有Windows桥一次调用，不额外新建常驻调度状态机。
- 只读预检和失败安全可本地检测；自动点击/粘贴/提交及新页GPT完成状态接管**未经验收**。窗口或控件不匹配立刻退出，回退人工复制唯一状态码，不盲发、不重试。
- 用户可从入口直接选择B最新版；不需要逐次给出版本号。方法指针与任务状态指针必须分离，不得默默更新其它TASK历史。
- K盘本地ZIP每三天周期或用户要求时备份，**不与每次Freeze绑定**。本路线方法提交只更新GitHub，旧K盘快照允许滞后且须标注旧提交。

本文件本次发布仅是B33方法和薄接力工具**已定义/局部只读测试**，不是完整虚拟成熟通过或实际生产自动接力成功。

## B33短状态码接口（继承其余B32规则）
当合法Freeze已真实落盘、该TASK_ID CURRENT指针已核对后，仅发送 `续接B|cuiqinggang/codex-private-skills|<TASK_ID>|<FREEZE_ID>`。它是指向现有完整冻结文本的**索引**，不是把正文嵌在字符串里；新GPT以该码找到 `tasks/<TASK_ID>/CURRENT.md` 和冻结文件，自行读取最新任务内容。B33薄适配器已支持四字段短码并通过无发送正反例预检；未实际发送与接管，不能将规则发布视为现实验收。方法详见 `NEW_PAGE_TEMPLATE_B_V23.md`。

## B33发布时的认证边界
三节点真实持久化虚拟接续与21条故障分支已完成检查，详见 `../../scenarios/B33_FULL_STATE_VIRTUAL_REPLAY_V2.md`。它证明状态层虚拟流程，不含真实新聊天发送或同边界端到端T_VALID，因此 `VIRTUAL_MATURE=NO` 与 `FINAL_VALID=NO` 原样保留；这里只激活新方法与适配入口以便完成后续授权验收，不宣称已达物理最短时间。
