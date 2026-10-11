# 执行补充V3：以我们自己的站点作为唯一真实验收载体
TASK_ID=POLSIA_CAPABILITY_REPLICATION_20261011
MODE=GPT_CEO_CODEX_EXECUTOR
SUPERSEDES_SCOPE=TEXT_ONLY_DEMOS_ARE_NOT_SUFFICIENT
PRESERVE=ACCEPTANCE_V2.md;EXECUTOR_TASK.md
USER_DECISION=BUILD_OWN_WEBSITE_AND_TEST_THERE
STATE=APPROVED_LOCAL_STAGING
TARGET=FUNCTIONAL_PARITY_OR_BETTER
FINAL_VALID=NO

## 用户最新决策
直接建立自主品牌的“AI一人公司”网站（如 AI Company Lab / AI公司实验站），网站名称、商标与页面视觉与 Polsia 独立，但对应 Polsia 的公开功能清单尽可能完整，达到同等功能及使用效果甚至超越；不限于前端静态演示。这个网站本身是后续虚拟成熟+真实故障注入+连续10轮无故障验收的平台。

## 成熟优先
1. 先查找用户机器已存在的一人公司 OS 网站、CASE-008 Polsia、CASE-015 Ploy/Webflow、n8n、Hermes、Codex、已有 UI/服务，不可无视成熟实现重新造壳。
2. 用成熟网站脚手架/现有 UI/现有任务队列或 n8n、既有日志/SQLite等持久层的最小组合。只允许为缺口做最小适配。不为好看构建第二套复杂框架。
3. 先实现能运行的真实端到端闭环：网站表单创建公司/目标→后端创建持久任务→指派至少两个已有真实适配器（如研究/代码或维护）→故障注入→分类和有限恢复→最终产物→页面可查看状态与原始证据/时间。高风险外联、支付、广告用模拟/审批门，不真实发送。
4. 逐项新增工程、研究、客服、营销、销售、运营预算、并发、审计、持久化、自愈能力，写功能等效性矩阵；不把空按钮、静态文案或冒充 AI 的模板回复标为能力通过。
5. 仅在本机 127.0.0.1/localhost 的隔离端口服务；不得占用已有端口、改变浏览器、代理、FlClash、凭据和生产系统；不可注册、部署公网或消耗真实财务账户。用户现有浏览器不新建第二浏览器实例；命令行 HTTP 也可完成测试。
6. 首先完成单次独立现实 POC，迭代修复后 Freeze，按 ACCEPTANCE_V2.md 严格连续10轮完整真实端到端测试。10/10 仅意味着测试的实际功能范围达标，不能等同第三方闭源后台全面复制成功。
7. 站点交付要求：本地可访问URL（确认真实启动和HTTP响应后再报告）、源码与启动入口、与公开 Polsia 功能逐项差分、完整证据、时长按X分Y秒Z毫秒、十轮原始结果。初步如需动态更新，将「网站可实际操作+可观察+可重放」作为第一节点。
8. Codex请使用可验证 Ultra 推理强度，实际日志展示 model/reasoning effort。GPT负责排障、深加工和最终验收，不将Codex未完成工作冒充已实现。

## 分期事实与停机标准
PHASE_1=合法独立站点+真实最小业务闭环
PHASE_2=核心业务能力矩阵实装+故障自愈
PHASE_3=虚拟成熟/Freeze→真实单次POC→冻结版本十次完整测试
PHASE_4=GPT审计+技能包成熟增强+可复用沉淀
停止条件不是“功能已描述”而是目标证据已达成；正常技术阻塞继续用GOOD/BAD/FIRST_DELTA和成熟解决方案，严守平台拒绝和用户权限边界。
