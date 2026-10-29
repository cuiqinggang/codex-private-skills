---
name: reuse-experience-brain
description: "读取和积累共同工作区的经验大脑。用户提到长期记忆、经验继承、越用越聪明、重复错误、旧解法，或AI化组织V4.2任务需要复用历史经验时加载。按触发词读取少量有来源的经验卡片，核对当前合同后采用或拒绝；收尾及21点复盘写回，保留反例并验证实际效果。"
---
# 经验大脑 V1
版本：V1，2026-10-27。它是V4.2的经验依赖，不替代执行大脑第25版、DSE或原专业技能，不增加调度层。

## 权威位置
共同工作区：`cuiqinggang/codex-private-skills` 的 `main`。
入口：`skills/reuse-experience-brain/SKILL.md`。
本技能随包经验是同版镜像；首次相关任务优先通过现有GitHub连接器读取线上 [经验索引](references/INDEX.md)，再取最相关1—3张卡。查询参数用 repository_full_name 与精确path。索引及卡片在同任务来源未变时复用，不每一步重新加载。Windows读取另加载当前Windows执行桥并先A。
没有线上访问时可读随包镜像，注明其版本/日期；不得把镜像当作最新项目状态。若正确行动依赖当前状态而无法核对，标记阻塞该动作，其他独立工作继续。

## 每次实际使用
1. 定义当前目标和合同；沿 [经验索引](references/INDEX.md) 按触发词读取相关卡片。只读导航与相关正文；不整库注入。
2. 核对环境、版本、正反约束、证据等级和不适用条件。项目状态以当前CURRENT/Freeze/最新原回执为准；卡片记录历史经验，不复活旧任务。
3. 把有效经验用于本次计划、检查或最小修复；过期/冲突/不适配就拒绝。没有命中正常继续成熟能力路由，不能凭空补经验。
4. 仅在经验影响行动时记一条最小回执：任务、经验ID/版本、采用或拒绝及原因、行动变化、真实结果、证据、时间。原任务回执已有这些字段时只留链接，不另写长报告。
5. 收尾把有新证据的增量留给原21点任务，按 [维护合同](references/MAINTENANCE.md) 去重、校验、保存与回读。无新事实不写；不自动晋升稳定规则。

## 旧记忆继承
读取 [继承映射](references/INHERITANCE.md) 和需要的 [来源清单](references/INHERITANCE.json)。
原方法/Freeze及原始日报保留原位；此包增加可跨页面读取的脱敏经验正文和原证据定位，不把所有旧资料复制入提示词，也不声称9份登记日报均已逐条蒸馏。

## 成熟与效果门
区分：保存、可找到、实际读取、改变行动、任务质量/时间净改善。文件存在或测试分数高不等于业务效率认证。
只读回忆/选路任务可用独立新上下文与隐藏期望答案验收；只证明这组回忆任务。全业务提速需同合同、同质量、同工具/成本边界的完整T_VALID对照，包含维护、检索、失败和返工。缺对照写NOT_MEASURED，不承诺模型权重变聪明或每轮必胜。
事实来源见 [成熟方案依据](references/SOURCES.md)；无需安装新的记忆框架。

## 经验卡片
- [Docker启动恢复边界](references/DOCKER-STARTUP.md)
- [H3历史精确复现](references/H3-REPLAY.md)
- [视频A/B编码契约](references/VIDEO-AB.md)
- [PayPal账户与收款资质](references/PAYPAL-ELIGIBILITY.md)
- [谷深强备V1.6宿主审计](references/GSB-V16.md)
- [租赁开源复用有效性门禁](references/RENTAL-REUSE.md)
- [Codex分层故障](references/CODEX.md)
- [Stripe来源叠色](references/STRIPE.md)
- [CalDAV取消缓存](references/CALDAV.md)
- [VEDA否决经验](references/VEDA.md)
- [Windows Harness兼容性](references/HARNESS.md)
- [HTTP重定向探针](references/HTTP-REDIRECT.md)
- [本机公网文件分享身份隔离与真实拖拽](references/FILE-SHARE.md)
- [交付制品与完整计时边界](references/DELIVERY-EFFICIENCY.md)
