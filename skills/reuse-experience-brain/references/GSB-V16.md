# EXP-GSB-001｜DSH强备V1.6原生技能审计与限定交付
版本V1；核查日期2026-10-28；类型CASE/ERROR/CANDIDATE_RULE；证据等级=真实DSH宿主调用日志、48行独立订单业务和20/20独立内容QA；不是全部V4.2能力等价认证。
触发：需要以不依赖GPT/Codex的DSH宿主承接已具备工具的业务；原模型METHOD-RECEIPT/RESULT自报六项原生技能，且N001称session-id未暴露。
环境：Windows现有DSH官方0.2.1-rc.2，谷深双擎可选V1.6入口；旧V1.5.1恢复版本仍保留。现有技能ai-organization-v4-2、reuse-experience-brain、dsh-extreme-effective-time、dsh-mature-capabilities及google-deepseek-strong-backup。
LAST_GOOD：宿主原生工具调用日志和CLI记录。FIRST_DELTA：模型文字回执多报一项没有skill工具调用的dsh-shared-browser-and-aiorg-v3，并漏写真实session-id。
最小修正：保留不可变原回执；新增N002-HOST-AUDIT.json，以宿主工具事件确认实际5/5原生加载及CLI会话身份；同一会话只读接续、不再重跑业务。
真实回归：48行含前导零、退款、重复客户的订单，产出CSV、JSON、DOCX、XLSX四份；20/20独立内容/公式和缓存检查PASS、合计178418分；同session只读续接21.596秒且工作区哈希未变。DSH启动至退出176.606秒、至独立QA177.452秒仅是局部范围；完整T_VALID=NOT_MEASURED。
适用：检查智能体模型自报与宿主原生调用是否一致；在授权环境内选择独立DSH可选入口，用真实日志和独立QA判断已经完成的限定业务。
不适用：声称Gemini自动网页派发/审核、ChatGPT专用插件等价、真实重启或断电无人值守恢复、外部交易恰好一次、Word/Excel视觉渲染或完整T_VALID提速；5项“加载”不等于全部复杂能力已实际验收。
原始证据：C:\AI\DeepSeek-Gemini-Failsafe\V1.6-AIORG-20261028\UPGRADE-ACCEPTANCE.md、evidence\NATIVE-LOAD-AUDIT.json、evidence\INDEPENDENT-ORDER-QA.json、evidence\RESUME-QA.json；C:\Users\A\Documents\DSH-Workspace\gsb-v16-20261028-001\CURRENT.json、N002-HOST-AUDIT.json；2026-10-28-DSE-INCREMENTAL.md。原始工作区不搬迁。

## 2026-11-01路由更新：旧V1.6是显式回退，不再是强备默认
原V1.6的五技能宿主审核及48行订单20/20仍属于有效历史限定证据；但10月31日22:31后的现行强备默认已由原项目及GitHub main的google-pi-strong-backup/SKILL.md明确切为Pi主执行、Google按需协作，DSH仅显式回退。读取本卡时不得把历史V1.6当当前默认，也不能将Pi V2限定发布门外推到跨整机重启、多日SLA。详见新卡EXP-GSB-PI-V2-001与C:\Users\A\Documents\DSH-Workspace\gsb-pi-google-v2-20261031\DEPLOYMENT.json。
