# CASE-009 Case Study — Webflow → Ploy

## 已验证现实样板
Webflow 已经把视觉开发、CMS、Analytics、优化、SEO、Localization、AI/AEO 等能力做成成熟网站平台；因此成熟网站基础设施的大量问题不应从零研发。

Ploy 官方资料显示其产品包含 Agent、网站生成/编辑、living design system、Astro/React/TypeScript/Tailwind 技术栈、Analytics/visitor insights、GA4/GSC、CMS/DB、发布版本、域名、工作流、Audience，以及 40+ integrations。发布采用 immutable snapshot 并支持 rollback；安全层包含 scoped OAuth、TLS/AES 和 isolated builds。

YC 页面截至 2026-09 显示 Ploy Team Size=14，Bryant Chou 为 Webflow 2013–2025 cofounder/CTO。

## $750k Slurper 的意义
Bryant Chou 在 2026-06-19 YC Podcast 公开访谈中称，为 Ploy Slurper 花费约 **$750,000 worth of tokens**。他把 Slurper 描述为确定性方法：读取现有网站并重建 design system 与组件；演示称约 75 秒。

这不是 Ploy 整体总开发成本，而是首次探索一个关键能力的高投入。后来者的价值在于产品形态、约束和成熟路径已经公开，第二次实现不应重复同等探索成本。

## 最值得吸收的创新
- 网站从静态资产变成主动增长执行面。
- Agent 持有公司、站点、部署、品牌与外部业务系统上下文。
- 页面生成只是入口，后续继续分析、SEO/AEO、访客识别、CRM/工作流和增长动作。
- design system + deterministic constraints 抑制生成式 UI 不一致。
- Preview / Deploy / Rollback 把 AI 行动纳入生产控制。

## 对一人公司的组织压缩
`目标拥有者 + 核心推理大脑 + 自动化 AI 工厂 + 确定性验证工具`

不会写代码的创始人不需要成为代码审查者；系统必须把代码质量转成可读的功能、性能、安全、回滚和稳定性证据。

## 禁止误读
- 不把 14 人 Ploy 描述成当前严格一人公司。
- 不把 $750k 描述成 Ploy 全公司总成本。
- 不把本技能的 36–72h / $8k–12k 推导写成 Ploy 官方数字。
- 不因为已有成熟样板就跳过真实生产验证。
