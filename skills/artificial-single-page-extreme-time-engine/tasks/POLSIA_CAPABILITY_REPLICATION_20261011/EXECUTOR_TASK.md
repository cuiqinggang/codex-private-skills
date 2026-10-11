# Polsia 全能力复用研究与极限短时间引擎反哺｜Codex 第一轮
TASK_ID=POLSIA_CAPABILITY_REPLICATION_20261011
NODE_ID=CODEX-001
MODE=READ_PUBLIC + CONTROLLED_LOCAL_POC
STATE=EXECUTOR_ASSIGNED
OWNER=GPT
AUTHORITATIVE_REPO=cuiqinggang/codex-private-skills
REF=main
START=2026-10-11
DONE_WHEN=已有成熟克隆技能核对完成、Polsia能力证据矩阵完成、至少一个无副作用故障自动恢复样例完成现实验收、交GPT审核
FINAL_VALID=NO

## 目标与核心问题
以 Polsia (https://polsia.com/) 的公开可核实功能作为成熟参照，建设可复用的“一人公司全能力复刻路线”，尤其复用其任务持续运行、异常分流、自动修复、跨角色协同的机制，反哺现有极限短时间引擎。此任务是现有技能包的成熟组合与最小补缺，不是复制私有程序、窃取数据或抄网页外观。完整公司能力是长期目标，本节点须报告覆盖度和缺口。

## 第一轮必须读的事实源
1. 网络 GitHub 仓库 main: AGENTS.md；00_START_HERE/COMMON-ENTRY.md；skills/artificial-single-page-extreme-time-engine/SKILL.md、START_HERE.md、ENGINE_V29_DRAFT.md，另外读取稳定 route 指针，尊重29版基本流程已冻结、公共总纲仍28版的差异。
2. 现有能力: skills/operation-demo-to-skill/SKILL.md（第3版）；skills/mature-outcome-automation/SKILL.md；本机 C:\AI\record-and-replay-evaluation\SKILL.md 和 C:\Users\A\.codex\skills\record-and-replay\SKILL.md；额外按需定位 n8n、Hermes、GitHub、browser-use、监测及其他已安装成熟能力。
3. Polsia 优先只读官方 https://polsia.com/ 和 https://polsia.com/deck 以及可信报道；营销自述与独立实测分列。报道融资约3000万美元，估值2.5亿美元，不是20亿美元。拒绝使用第三方域名当官方证据，特别不要将 polsiahq.com 默认当作该公司。
4. 按需查公开开源成熟组件（n8n、Temporal/Trigger.dev/Restate、LangGraph、OpenClaw、Claude Agent SDK等），选已成熟且环境匹配者。用户已有组件优先。

## 必须产出
A. CAPABILITY_MATRIX.md：研发/市场/客服/销售/财务接口/多任务/审计/异常恢复/长期自我改进，区分平台官网声称、独立验证、已落地能力和缺口。
B. REUSE_MAP.md：用户现有成熟工具的真实文件入口与证据，说明是否能完整替代，禁止虚构「全功能PASS」。
C. EXCEPTION_RECOVERY_POC：优先复用既有技能或小组合完成至少一条无副作用可重复的演示链：触发→执行→可控失败→错误分类→GOOD/BAD定位→有限安全恢复→有效结果→日志/耗时；若现成实现足够，直接配置使用，不另造底层。
D. RESULTS.md：现实工具回执、可重放命令/入口、时长按“X分Y秒Z毫秒”显示（计时有据才写）、失败原因及合法下一步；根据真实证据提出对引擎29版的最小兼容增强建议，不直接改动已冻结全局方法。

## 权限与纪律
- 不登录、不消费、不批量抓取、不破解/克隆商业私有代码/品牌。仅公开页面与授权环境，严格遵守网站访问条件。
- 禁止发送真人邮件、投广告、付款、部署生产、更改用户账户或修改代理。不得修改 FlClash、虚拟网卡、现有登录浏览器，不启动第二浏览器、不关闭任何已有浏览器。
- 只在独立隔离工作目录中做无副作用测试，不覆盖现有技能/生产文件。不生成未知来源的可执行程序。
- 用户无需反复批准合法无副作用分析；遇一般故障不得立刻停机：查GOOD基线、首差分，复用官方成熟修复；明确安全拒绝必须遵守。
- 先尽可能完成成熟方案虚拟筛选，Freeze之后才做一次必要 Reality；阶段未通过不能宣称FINAL_VALID。
- 这是 Codex 独立节点，结束后由 GPT 审核、深加工、决定是否升级统一技能，禁止抢占 GPT 最高主控权。
