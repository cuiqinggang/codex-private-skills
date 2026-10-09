# 《自动化A·单专用浏览器双层页面极限短时间引擎 第29版》｜稳定路线入口
ROUTE=A
A_ENGINE_VERSION=29
A_ENGINE_FILE=routes/A/ENGINE_A_V29.md
ROOT_ENGINE_FILE=ENGINE.md
ROOT_ENGINE_VERSION=28
BRAIN_FILE=BRAIN.md
BRAIN_VERSION=25
TEMPLATE_FILE=NEW_PAGE_TEMPLATE.md
TEMPLATE_VERSION=18
METHOD_STATUS=A29_PUBLISHED_DIFFERENTIAL_REALITY_PENDING
TASK_STATE_SCOPE=PER_TASK_ID
ACTIVE_TASK_EXAMPLE=A29_CEO_DEDICATED_BROWSER_20261010

## 版本继承（不可混写）
A29仅为A路线中“CEO与Executor共用已经登录的专用浏览器、按需新增Executor标签”的**最薄位置变更**。共同引擎ENGINE.md=28、执行大脑BRAIN.md=25、页面模板NEW_PAGE_TEMPLATE.md=18完全不变；A28的历史行为保留，B路线不升级。详细新增语义只读 `routes/A/ENGINE_A_V29.md`，不把公共A28整套文档复制一份。
A路由整数版本从A28→A29连续升级；本次既没有升级公共总纲，也没有推出A26大脑或A19模板。

## 运行
- **简单任务**：用户原有专用AI浏览器（现有CDP9223）中仅CEO标签完成，不要求新Executor、不强制n8n、不强制新页。
- **复杂任务**：同一专用浏览器保留唯一ACTIVE_CEO标签，按任务拆分临时创建0..N个独立Executor标签（不是多个浏览器实例/Profile）。每个Executor一节点一Freeze，CEO在核验后Merge；仅关闭自有已完成Executor标签，不可关闭或覆盖CEO或任何其他用户标签。
- 共享浏览器和多客户端遵守第28版的最小真实冲突域协调；同标签、共享焦点、Profile级变化不能假定完全隔离。冻结与角色归属保持唯一；UNKNOWN禁止盲重试。
- 完整时间准则 `T*=min(T_VALID)`；无需n8n时不启用，有真实外部等待或编排需要时可调用已验证的成熟组件。Windows双路执行桥v0.3.1及原Playwright MCP按需复用，不得新开发控制器、调度器或状态机。
- 已有A/n8n F002测试保持历史有效；其仍未验收的跨客户端实际冲突协调与统一业务提交不可误记为PASS。
- 不调整用户FlClash/已有Chrome Profile。此前 B33 的保护锁和平台安全拒绝没有因A29启用而解除；未经许可不得自动发送。

## 发布与验收分离
本A29版本在GitHub稳定入口发布表示**方法布局决策正式生效**，不代表CEO已在用户电脑真实迁移、所有隔离重新通过或完整自动接管完成。A29任务合同及冻结按独立 `tasks/A29_CEO_DEDICATED_BROWSER_20261010/CURRENT.md` 读取，后续2026-10-11只进行必要且合法的差分测试和微小完善。已PASS的旧组件无需重测；对共享Profile/窗口焦点/标签归属等新差异不得宣称风险为零。
A29发布前的A28版本文件仍可从GitHub提交历史读取；有必要回退时恢复以前的ROUTE，而不是改写其他任务Freeze。

## 启动读取
固定入口 `SKILL.md → START_HERE.md → routes/A/ROUTE.md` 确定A29；再按 `BRAIN.md → 当前TASK合同和Freeze → NEW_PAGE_TEMPLATE.md` 读取实际任务状态；`ENGINE.md` 由Brain按需调用，同时继承本 `ENGINE_A_V29.md` 差分覆盖。方法提交与动态状态提交不得混用。
