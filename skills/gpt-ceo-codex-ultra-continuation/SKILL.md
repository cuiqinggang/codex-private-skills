---
name: gpt-ceo-codex-ultra-continuation
description: GPT CEO＋Codex Ultra持续执行。成熟并行动态调整、轻量中文故障监控、Grafana完整版保留、声音报警、保存点与事故诊断。以真实回执和完整有效总时间为准。
---

# GPT CEO＋Codex Ultra 连续运行技能｜V5

SKILL_VERSION=V5
METHOD_VERSION=V5
VERSION_POLICY=INTEGER_ONLY
ENGINE=28_FOR_CURRENT_POLSIA_UNCHANGED
LIVE_WINDOWS_RUNTIME=3.1.0_UNCHANGED
BUSINESS_FREEZE=V008_UNCHANGED
BUSINESS_FINAL_VALID=NO
PREVIOUS_SKILL_VERSION=V4_PRESERVED

**唯一权威索引**：`cuiqinggang/codex-private-skills/main` 的 `skills/artificial-single-page-extreme-time-engine/GPT_CODEX_ULTRA_CONTINUATION_INDEX.md`。正式方法是同目录 `GPT_CODEX_ULTRA_CONTINUATION_V5.md`。本技能 `v5/README.md` 是最短运行手册，`v5/KNOWN_ISSUES_AND_ACCEPTANCE.md` 为事故及修复复用规范，`v5/EVIDENCE_MANIFEST.json` 为证据边界和 Git Blob 列表，`v5/CHANGELOG.md` 为整数升级记录；`v5/dashboard-lite.ps1` 是轻量中文界面源码快照（本次发布不能替代Windows现场字节比对）。

## 首先做什么（按顺序）

1. **查权威**：从 GitHub 精确读取索引／本文件／V5方法／母任务 CURRENT、VERSION_CURRENT、最后 Freeze 和 CEO 合同，核对 TASK_ID、FREEZE_ID、版本、SHA、最新NEXT状态。再读 Windows 的真正状态文件、报警事件、计划任务及运行进程。若Windows工具不可用，说明只持历史快照，不得直接声称当前在线或故障已修复。
2. **判断权限和 Exactly-once**：CEO 是唯一批准／合并入口。任何新 Codex 执行必须通过“CEO正式批准到达Windows真实NEXT合同＋精确页面定位标签”双门。DONE绝不重播、UNKNOWN先查回执和外部副作用；正常 `WAITING_CEO` 不允许被监控当作死机重启；多个执行器不得并发写母 CURRENT/VERSION 指针。
3. **动态并发**：九类公司能力加跨系统集成，共十个逻辑方向；独立任务可并行，局部 BLOCKED 不阻断无关任务。PS7原生运行空间的阶段实测基线：本地计算与短任务默认并行2，净收益确认后到4；等待型默认4，净收益确认后到8。十方向≠十个重型Codex进程；Codex 1/2/3 Agent真实模型测试尚未完成。以同合同、同质量、含审核恢复和集成的完整有效时间选择并发数。
4. **日常监控仅用精简中文窗口**：Windows目录 `C:\AI\Polsia-Unified-V4\`，计划任务 `Polsia-Unified-Monitor-V4` 每分钟采样，`dashboard-lite.ps1` 每60秒显示故障摘要；桌面入口 `Polsia Codex - Live Status`。监控只读、不派工；采样 `snapshot.json`、十方向 `config.json`、事件 `incidents.jsonl`、分支状态文件不可停止。中文界面显示运行／待派发／阻塞／异常，不向用户显示英文内部代码。
5. **报警与分级**：只有新的实际故障、故障集合变化或采样长期失联发出特殊双音＋Windows内建中文语音；同一故障不每分钟重复播报。存储故障 `DETECTED` 与解除 `CLEARED`；窗口关闭不得导致后台采集中断。已知权限阻塞须显示、合法修复，不得使用生产未知结果盲重试。语音引擎退出成功与用户听到声音是两项不同验收。
6. **重型完整监控离线保存**：Grafana OSS 13.2.3＋Infinity 4.1.1；软件 `C:\AI\Polsia-Observability-Grafana\grafana-13.2.3\`，22项历史配置工具及诊断归档 `C:\AI\Polsia-Observability-Grafana\历史方案-完整监控-20261012\`。已取消默认运行及登录启动；只有未来全流程多节点收益明确且经授权才恢复。轻量模式已移除Grafana JSON数据发布步骤，重新启动前需恢复数据连接和完整验收，不重新造可视化系统。
7. **出故障先查技能包故障库**：GOOD成熟基线→BAD复现→首个差异→优先复用已成熟方案→最小修复→验证→记录新证据→冻结；逐项记录具体症结、权限、恢复回执。业务结果 UNKNOWN 必须先对账。不要遇到常见错误就停，也不要未经授权改系统权限、代理、浏览器、支付或生产环境。
8. **新版本与测试边界**：任何界面、流程或方法改变，要做新版本对应的现实验收，不能复用旧成功声明替代实际效果。采集器含 V008 特定SHA校验，V009后必须单独适配并验证；模型级并行、GPT主动接管、断电/72小时、九类业务最终能力仍未认证。

## 已核验的历史成果与数据入口

- Windows原生并发：36轮、432任务回执、134144次SHA256，PASS（只限原生计算／模拟等待）。原报告 `tasks/POLSIA_CAPABILITY_REPLICATION_20261011/benchmarks/POLSIA_PARALLEL_CAPACITY_20261012.md`。
- 十个逻辑方向、两项隔离试点（V008清单128项、Git损坏原生恢复SHA一致），每60秒采集、故障测试发现与解除及历史保留。
- 原完整 Grafana 9面板／10方向、原生Infinity查询 PASS；已停用常驻，未删除产品、数据与归档。
- 日常纯中文窗口、一次隔离模拟故障与中文语音引擎执行、修复后最终单窗口存活 PASS；完整版停前工作集351.5MB，其他时点501.5MB；轻量约100MB。**无法推断必能多开一个Agent**。中文窗口首次启动参数出错的历史失败亦留档。
- 本次 V5 只发布方法／技能包；Windows远程连接器额度耗尽，**未重新运行或字节核验现役Windows脚本**。证据文件与未完成项目详见 `v5/EVIDENCE_MANIFEST.json` 和事故诊断文档。

## 禁止变更的旧资产

历史 V4 入口原样归档为 `v4/SKILL_V4_ARCHIVE.md`，V4方法正文及 `v4/{config.json,collect.ps1,dashboard.ps1,pilot.ps1,install.ps1}` 不改。Windows 旧项目的 `CONTINUE_EXISTING_CODEX.ps1`、`Polsia-Codex-Mother-Continue`、引擎28、业务冻结V008、FlClash／代理、原浏览器全部保持。n8n `skills/n8n-multi-agent-operations-control-plane/SKILL.md` 的1.0.2仍是独立技能，管理权限401不得绕过。

真实付款、退款、发消息、投放、公网发布、生产改动和凭据读取必须额外授权。Polsia 母任务仍 `MOTHER_FINAL_VALID=NO`，V5 不自动批准 CODEX-009。