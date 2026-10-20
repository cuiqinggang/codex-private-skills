# Lovable 全能力本地复刻｜正式母任务合同 V001
TASK_ID=LOVABLE_FULL_CAPABILITY_REPLICA_20261021
CONTRACT_VERSION=V001
DATE=2026-10-21
OWNER=GPT_CEO
EXECUTOR=CODEX_CLI_SCOPED_PARALLEL
METHOD_REF=skills/artificial-single-page-extreme-time-engine/SANRENXING_V5.md@SRX-V5-F001-20261020
STATE_METHOD=REQUESTED_LIGHT_STATE_V3_UNVERIFIED;FALLBACK_READABLE_LIGHT_STATE_V1
BRIDGE=V11_C_FIRST
LOCAL_ROOT=C:\AI\Lovable-Full-Replica-V1-20261021
POLSIA_REFERENCE=C:\Users\A\.codex\skills\polsia-clone-local-foundation-v3\SKILL.md
POLSIA_REFERENCE_SHA_PRECHECK=2026-10-21_655_FILES_PASS_163_SOURCE_FILES_PASS
MOTHER_FINAL_VALID=NO
REAL_BUSINESS=FORBIDDEN
PUBLIC_DEPLOYMENT=FORBIDDEN
REAL_PAYMENTS=FORBIDDEN
REAL_CUSTOMER_OUTREACH=FORBIDDEN

## 原始用户目标
以已冻结《Polsia 本地核心能力复刻技能包》第3版作为成熟样板，对Lovable（lovable.dev）的公开主打能力、产品定位、用户界面交互范式与“想法→商业机会→可售产品→营销获客→销售→支付→交付→分析利润→持续优化”的**全部公开可验证业务闭环**做最大范围本地功能复用。不是单纯生成网站；也不接入真实商业客户/生产支付/外发广告。目标是可真实操作、可持久化、可自动测试的本地仿真平台和技能包，不能把空壳UI或静态文案冒充功能。

## 来源与版权边界
使用Lovable官网公开可合法访问的页面、文档、公开演示与用户提供研究资料。不得取得或假定有原站私有源代码/模型提示/用户数据；不得复制受保护品牌资产、logo、商标或造成官方身份混淆。允许参考公开界面信息架构、交互层次、布局、色彩节奏和工作台使用体验，制作原创实现并显著标注“非官方本地研究复刻”。“网站样式一样”按高相似度用户体验和视觉布局验证，不直接盗用受保护素材。

## 核心验收功能（真实本地执行而非口头）
1. Lovable式首页与输入框、项目列表、自然语言需求到可运行页面/应用、预览/编辑/历史版本/导出（可用成熟模板/离线规则引擎；模型能力不可用标NOT_TESTED）。
2. 从idea到商业计划：客户痛点、市场假设、竞品、价值主张、定价与风险；本地可运行，不把模型猜测当真实调查。
3. 运营与GTM：产品定位、SEO内容、推广方案、营销素材、渠道任务、CRM潜客/线索/商机漏斗；全部测试数据明确SANDBOX。
4. 销售与收款模拟：报价、订单、Stripe式TEST_MODE支付模拟、退款/订阅/履约；幂等键与真实/测试分离；禁止生产扣款。
5. 财务与经营：收入、成本、毛利、CAC/LTV假设、留存/复购、净利润看板；模拟数据显著标记，不得宣称实际盈利。
6. AI一人公司：CEO/工程/研究/营销/客服/财务逻辑角色、任务依赖、持久状态、错误检测/恢复、证据/回执/审批、模拟自主迭代。优先复用Polsia V3已验收隔离功能，绝不修改其冻结包。
7. 视觉：响应式首页、产品工作台、商业运营面板、设计系统、空态/加载/错误/导航，公开Lovable UX范式高保真但独立品牌。
8. 真实测试：至少1条从“输入创意→创建并预览可运行产品→编辑版本→营销方案→沙盒线索→测试订单→交付→净利润看板→故障恢复”的完整自动化E2E；对照源站仅声明已核实公开部分。端点、前后端、持久化、权限、质量、视觉截图、恢复与回滚均有原始证据。

## 6个并行工作项（允许根据资源动态调至3–8，按净有效时间选）
W01=PUBLIC_SITE_UX: Lovable式公开站点和应用生成入口；原创设计与响应式布局；独立模块文件。
W02=APP_BUILDER: 自然语言→模板/组件生成、代码预览、项目编辑、版本快照与本地预览；优先成熟工具。
W03=IDEA_MARKET_RESEARCH: 商机研究、persona、市场与竞争、价值定位、定价假设、证据标记。
W04=GTM_CRM: SEO/推广内容、营销计划、线索/商机/客户流程、转化漏斗，测试数据。
W05=SALES_FINANCE: 沙盒报价/订单/支付/退款/订阅、利润/CAC/LTV经营分析、真实测试隔离。
W06=OPERATIONS_RECOVERY_QA: Polsia V3成熟逻辑角色/持久任务/故障恢复的最小授权复用；自动化测试与独立审计。
CEO_INTEGRATOR=唯一主分支/全局状态写者，合并W01-W06，修复接口差异，执行端到端测试。各Worker仅写各自隔离目录，不写母任务CURRENT，不操作原Polsia V3。
统一输出协议：各Worker需 README、模块源码、接口契约、单元/集成测试、RESULTS.md、EVIDENCE.json、SHA256/实际耗时；STATUS只允许PASS_REAL/PARTIAL/FAIL_REAL/NOT_TESTED/UNKNOWN。

## 运行约束
优先现有Polsia V3的read-only preflight、已安装Codex、现有Windows桥、Node/Python/FFmpeg、现成开源组件；禁止为此另造调度器、消息总线、浏览器桥。Windows当前约32GB RAM，2026-10-21检查有多个既存Codex进程和约12GB空闲，不能机械启动8个高负载进程；先并行少量且测实际资源与争用，只有净有效时间获益才扩至5–8。跨进程持久化只使用已存在的合规调度/Loop/n8n（如果确实已配置且授权），不自行注册新的后台服务。
当前GitHub只找到LIGHT_STATE_V1.md，用户指定LIGHT_STATE_V3未在该权威路径确认；先搜索已安装成熟V3，找不到就标METHOD_VERSION_UNVERIFIED并按V5中已有安全checkpoint规则与可回读V1执行，不能伪称V3已生效。
V11 C通道已list_devices找到在线Windows，C无副作用PowerShell探针回执V11_C_DIRECT_PONG；未切换A/B。
安全与Exactly-once：外部副作用未知先查回执，不盲重放；无授权不花钱/发邮件/投广告/接真实支付/部署公网/改用户现有浏览器代理与项目。所有业务数据为明确虚构沙盒数据。原Polsia和Lovable旧任务的METHOD_REF/CURRENT不可覆盖。

## 交付物
本地完整可运行项目与一键本地启动（仅localhost）、全功能菜单/业务流程、原生测试与浏览器截图、能力覆盖矩阵（源站公开证据/实现/未实现/模拟）、故障注入回执、集成报告、成本与时间账本、README、SKILL.md第1版及不可变Freeze，必要时独立GitHub保存。
DONE_WHEN=本地应用启动、关键UI可见、业务主闭环真实可操作且持久化、六个模块独立测试+整体验收PASS、无未经授权外部动作、状态/源码/回执可回读。若某项功能依赖不可得私有API，明确NOT_IMPLEMENTABLE_AS_PRIVATE_EQUIVALENCE，不虚报100%复制。
T_VALID_REAL=UNKNOWN_UNTIL_COMPLETE
FINAL_VALID=NO
