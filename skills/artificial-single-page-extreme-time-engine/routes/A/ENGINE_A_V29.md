# 《自动化A·单专用浏览器多页面协作方案 第29版》
ROUTE=A
A_ENGINE_VERSION=29
INHERITS=ENGINE.md@28; BRAIN.md@25; NEW_PAGE_TEMPLATE.md@18; routes/A/ROUTE.md@A28（升级前历史）
METHOD_KIND=A29_DELTA_ONLY
STATUS=METHOD_PUBLISHED_PENDING_DIFFERENTIAL_REALITY
REUSE_GATE=MATURE_BASELINE_ACCEPTED
FINAL_REALITY_VALID=NOT_TESTED
T_VALID=UNKNOWN

## 唯一改动：主控CEO的浏览器位置
原A28角色职责、任务隔离和冻结恢复合同不变。将**唯一活跃CEO的ChatGPT标签页**放入用户已经登录且正在运行的专用AI浏览器（Windows原项目 `C:\AI\Playwright-Native-AI-Browser`，现有CDP `127.0.0.1:9223`）。Executor仍以独立ChatGPT标签页承载独立自然节点，默认共享同一个专用浏览器实例和现有登录Profile，不新开其他Chrome浏览器/身份/Profile。不假设当前运行中的旧CEO已经自动迁移；迁移只可在真实Freeze后且新CEO已合法接管确认时进行。

### 简单任务：CEO-only
一个已登录专用浏览器 + 一个有效CEO标签页；无需Executor，无需额外n8n层，无强制新聊天，无意义重规划时禁止强制换页。GPT在原会话直接完成任务，原任务VALID优先。

### 复杂任务：CEO + 按需Executor标签
仍在**同一浏览器实例**按真实需要新增0..N个Executor标签页，不要求开多个浏览器进程。每个Executor有唯一TASK_ID/NODE_ID/OWNER_TAB_ID或URL/合同/父Freeze/Done_When，只负责自己的自然节点，完成后持久化不可变节点证据→CEO验证并Merge→仅关闭该任务拥有且已确认可清理的Executor标签。不能通过共享Profile判定标签内容天然隔离。并行只对真正独立的任务；同标签、同聊天、窗口焦点、导航和Profile级副作用按实际冲突范围协调。不能以同浏览器标签并行推断模型工作可并发或无相互干扰。

### CEO安全所有权
- 任一任务逻辑上唯一ACTIVE_CEO（同任务只有一个全局写者）；CEO标签为受保护的控制页，不得由Executor退出、清理、迁移、浏览器重连或失败恢复代码关闭、导航或覆盖。
- 浏览器/标签操作必须核验所属TASK_ID、角色、真实ChatGPT URL、唯一目标标签及前后状态；未确认归属不得点击/发送/关闭。关闭仅允许当前任务创建且已完成的Executor标签，不得清理任何其他用户或其他任务标签。
- CEO换页严格执行先Freeze持久化→新CEO接管确认→旧CEO退役；新会话接管若没有可验证的受许可执行入口，则保留旧CEO、停止自动换页并输出最短中文人工恢复提示词。不默认自动发送，UNKNOWN不重发。
- 用户、n8n、Codex及其他合法客户端仍可共享浏览器，不独占进程或封禁其它用户工具；共享Profile、Cookie、扩展、窗口激活、同一资源点击仍是潜在冲突作用域。优先复用既有原生协作协议/队列/浏览器技能，禁止新造锁、调度器、浏览器控制服务。

## 成熟能力复用及证据
1. 原ENGINE28/BRAIN25/模板18的角色、Freeze、≤3 CEO Freeze轮换门、自然节点、Exactly-once、先成熟基线后整套虚拟再一次最终Reality、T*=min(T_VALID)全部继承。
2. 旧 A/n8n F002 实测PASS：n8n原生MCP标签读取与可逆DOM写、跨工作流串行、Remove Duplicates跨重启、Wait恢复、写后故障同键不重复提交、多客户端只读共存。不得重跑这些已验收组件。
3. 专用浏览器先前 CDP9223 + Microsoft Playwright MCP 只读已PASS，现有ChatGPT标签真实可读；B33 F023还在原已登录专用Chrome内新建测试标签、真实点击“新聊天”、确认编辑器、关闭自有临时标签且保留原两个标签（16.887秒、无消息发送）。属于可复用的**浏览器控制证据**，不是A29 CEO完整迁移或多标签并行PASS。
4. 原A第28版自身记录明确尚未验收：跨客户端同目标资源仲裁、不同目标真实写并发、异常局部释放、UNKNOWN端到端对账、正式业务集成、同合同全程计时。A29不自动补齐这些缺口。
5. B33受保护自动发送路线已由用户在独立TASK中STOP；本A29不调用B33受锁的--commit，不修改其保护，不借单浏览器/GUI/CDP绕过既有平台工具安全拒绝。

## A29微型差分验收（安排次日，今天只升级方法）
A. 静态指针：ROUTE声明A29→本文件→共同ENGINE28/BRAIN25/模板18真实存在，其他路由和n8n F002未被覆盖。
B. 在用户原有专用Chrome中只读确认CEO标签的唯一归属、Executor临时标签的TASK/NODE标记与浏览器实例不变。不能凭两个ChatGPT页面自动断定哪一个是CEO。
C. 对本任务**新建且确认归属**的临时Executor标签执行无发送导航/只读检查及受控关闭，证明CEO及原用户标签保持不变、独立节点Freeze可读；不得写入未归属会话。
D. 只做一次最小交叉干扰差分：同一浏览器中CEO保持可读，临时Executor进行只读操作，核验它们的页面URL、选中状态和任务/节点归属不混淆；若浏览器焦点变化会影响UIA动作则标记局部串行而非谎称完全并行。
E. 只在明确获准的实际入口能安全且唯一归属时，另行安排官网真实自动发送/新模型接管；没有获准就保持NOT_TESTED，绝不换工具规避以前拒绝。
F. 如果B→A或两个浏览器→一个浏览器的全链时长没有同合同实测，保持T_VALID=UNKNOWN。不得将减少浏览器数量推算成X倍提速。

## 版本及独立任务状态
A29是A路线的最薄定位覆盖层，不重写公共ENGINE28；执行大脑仍25，模板仍18，原其他TASK_ID的任务合同和Freeze不可回写。
本方案变更的是**浏览器布局和目标归属**，不是取消隔离、不允许关闭CEO、不承诺不可能发生共享Profile冲突。A29方法可在指针核验后发布；次日微型差分Reality是**独立验收**，在完成前状态：METHOD_READY / DIFFERENTIAL_REALITY_PENDING / FINAL_VALID=NO。
