# Polsia｜GPT CEO 独立复核与新自然节点派发（V003→CODEX-004）
TASK_ID=POLSIA_CAPABILITY_REPLICATION_20261011
CEO_DISPOSITION_ID=POLSIA-CEO-D003-20261011
METHOD=ENGINE.md@28
DECISION=ACCEPT_V003_FACT_FREEZE;STOP_REPEAT_EVIDENCE_AUDIT;PROCEED_NEW_MATURE_BUSINESS_NODE
PREVIOUS_VERSION=V003
PREVIOUS_FREEZE_ID=POLSIA-MOTHER-V003-F001
PREVIOUS_FREEZE_PATH=skills/artificial-single-page-extreme-time-engine/tasks/POLSIA_CAPABILITY_REPLICATION_20261011/Freeze_V003_CODEX003.md
PREVIOUS_FREEZE_BLOB_SHA=c8f2e1c974999e3d8128c64fed7cfbaa029a1fd3
NEXT_NODE=CODEX-004_MATURE_CONTENT_OPERATIONS
MOTHER_FINAL_VALID=NO
STATUS=CEO_REPLAN_APPROVED_NO_EXTERNAL_SIDE_EFFECTS

## GPT独立判定
- CODEX-003 官方 Codex CLI 已以退出码0结束；45项本地清单、GitHub事实冻结和VERSION_CURRENT/CURRENT的回读证据一致。其输出明确是“事实/缺口冻结”，不是引擎28的最终优化Freeze，也没有授权继续FINAL或新10轮。
- B/C FFmpeg候选缺同质量验证、同合同完整时序、争用、崩溃/UNKNOWN恢复证据。直接重做CODEX-003审计不能获得新证据，净收益≤0，停止该无新增输入的重复循环。保留CODEX-002现有视频素材GOOD和CODEX-003时间账本，不重复下载/重渲染/旧场景10轮。
- Polsia目标是公开成熟AI公司能力复用，不应困于单一媒体编码测速。下一节点选择另一个明确有业务输出、无外联副作用的实际可执行能力：成熟内容运营/交付包；使用现有已验收素材作为输入，展示“接单→资产整理→渠道素材与营销文案→独立质检→可交付包”的完整流程。不能拿营销草稿冒充真实广告投放、实际获客、收入或平台生产等效。

## CODEX-004执行合同（Executor）
输入固定：本机 nodes/CODEX-002/BASELINE/earthrise-landscape.mp4 与 earthrise-portrait.mp4、CODEX-002源头/署名及视觉验收回执；现有技能包和已安装成熟工具。仅在 C:\AI\Polsia-Codex-20261011\nodes\CODEX-004\ 写新增成果，原素材只读。
输出目标：基于已有可信媒体制成一份**实际可交付但不对外发布**的短视频内容运营包，至少提供中文/英文标题及简介、适配抖音/TikTok/YouTube Shorts 的三种渠道发布草案、源头与授权/署名检查单、资产manifest/UTF-8与媒体规格回执、交付清单。封面若有成熟FFmpeg单命令可按原素材导出，先按引擎28成熟基线→最多3现成候选→虚拟成熟→STOP_GATE→冻结→仅1次必要Reality，不逐项乱测。独立审核真实内容符合输入和授权；不能生成侵权/欺骗宣传，不自动投放或联系客户。
执行前：精确读取 GitHub CURRENT.md、VERSION_CURRENT.md、Freeze_V003_CODEX003.md、REUSE_ONLY_V4.md、ENGINE.md@28、本CEO决策文件，以及本地 MOTHER_CURRENT.md、CODEX-003/NEXT.md 和 CODEX-002已有验收。读取 v3.1.1 正式 ECC 索引仅用于成熟Checkpoint/接续思路，不热替换正在运行中的Codex、不创建新执行底座。
现场若已有合法已配置的一体化成熟公司/内容管理产品入口，优先直接使用其内建功能；没有则用现有Codex+FFmpeg+已有媒体技能最小合法组合，保留缺口。禁止从零开发新站、监控平台、调度器、数据库、业务框架。
此节点不得只返回新研究/兼容性报告而不产出实际可交付内容；不允许复跑CODEX-001/002/003既有验收，亦不得在缺少真实新证据时重复原先FFmpeg B/C审计或虚报 T*。
节点未达到目标时留下实际失败与下一可执行策略，不为了持续执行而造无价值轮次。成功完成自然节点时，先保存业务文件/回执→新的不可变V004事实Freeze及SHA→远端读取确认→更新 VERSION_CURRENT/CURRENT 和本地MOTHER_CURRENT→写NEXT；母任务仍FINAL_VALID=NO，不把一个渠道运营包等同完整Polsia。

## 本轮GPT故障根因及修复边界
Windows继续脚本错误地把GitHub的LATEST_FREEZE_PATH只取basename拼到本地工作区根目录；但 V003 真实本地冻结文件为 nodes/CODEX-003/FREEZE.md。正常NODE退出码0且V003成功，仍被误判为CODEX_EXIT_WITHOUT_NEW_VERIFIED_FREEZE。必须改为：比对当前GitHub/本机版本指针与MOTHER_CURRENT内的NODE_ID、VERSION、FREEZE_ID、对应在本机隔离工作区内真实存在的FREEZE_PATH、MANIFEST_PATH和MANIFEST_SHA256以及exit0；不强求远端不可变Freeze在根目录另存同名文件。成功才清除仅属于该已完成节点的INFLIGHT，不盲重发先前业务。真实不一致仍由GPT接管。
GPT每小时的独立监督不是即时后台模型；Windows原生计划任务应先基于确定性回执处理正常成功节点，不应该让所有正常结束都等待GPT人工唤醒。
