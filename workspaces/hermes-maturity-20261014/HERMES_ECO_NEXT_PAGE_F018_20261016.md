# Hermes 生态站｜下一页面接续 F018｜2026-10-16

**权威 CURRENT：** `workspaces/hermes-maturity-20261014/HERMES_ECO_CURRENT_20261015.json`（虽然文件名带20261015，正文已更新到 `HERMES-ECO-F018-20261016`，以动态 Freeze 为准）。
**总任务：** `HERMES-ECO-20261014`。项目范围按《三人行》V2的成熟复用/Exactly-once/冻结→Reality方法执行，但该V2仍 `REVIEW_PENDING_NOT_ACTIVE`，不能改全局默认；Hermes上位母技能为v2.0。
**Windows执行桥：** GitHub正式 `skills/extreme-time-automation-bridge/SKILL.md` v7.0.0，Freeze `FREEZE-GPT-WINDOWS-BRIDGE-V7-A-PAUSED-20261016`。C=Remote_Desktop_Commander第一入口，B=GitHub Runner备用或原生证据，A=GPT_Windows_MCP_Bridge已PAUSED_BY_USER，任何情形不得因C失效回退A。C调用前按list_devices挑在线设备，running的call_id必须用get_tool_result回收。用户禁止改变FlClash/Windows系统代理、凭据和正在用的浏览器；不要重装Hermes、启动第二隧道或第二浏览器。

## 本轮真实已完成，禁止重复做
- F013官方外部目录修复，现有 `C:/Users/A/AppData/Local/hermes/config.yaml`中 `skills.external_dirs=[C:/Users/A/.hermes/skills]`；新Hermes原生skills_list从72恢复171，2个命名技能均实际skill_view成功。
- F014跨Codex/Knowledge Brain仅按需只读：已证明可读取 `C:/Users/A/.codex/skills` 的单份SKILL.md与 `C:/Users/A/.codex/knowledge-brain/ROUTING_MAP.md`，不自动开放218份Codex技能到可写external_dirs。
- F017知识技能快速路单样本CLI耗时91.82s，旧深度样本202.49s；仅REALITY_OBSERVED_CANDIDATE，不能宣称普适2倍或物理T*。见母技能references/CODEX-KB-ON-DEMAND-20261015.md。
- F018 2026-10-16 经C实际复验：Hermes原生skills_list=171、母技能及Repair两个skill_view成功、知识库原生read_file成功；CLI exit0，墙钟26939ms，只有一次只读样本。
- F018在不查看或上传凭据正文的前提下将一份历史旧YAML配置备份SHA一致隔离到既有本机备份区，保留移位manifest与旧历史JSON；原全量技能包静态检查恢复18/18 PASS，高置信敏感信息模式0次命中。详情：`F018_SKILL_BACKUP_SECRET_SCAN_REMEDIATION_20261016.md`。
- 本地V7判路器PS Parser=0，SHA和云端Freeze一致；实时C通道ping成功、C选C/C不可用选B/A不许派单实际检查通过；并且从未调用A。

## 保持UNKNOWN或PENDING，不得冒充已成熟
- 整站 `FINAL_VALID=NO`，连续完整验收仍0/5。F002原自写Runs API HTTP400，无成功ack，原任务UNKNOWN，严禁盲目重放；Runs API不是日常CLI或WebUI业务前置门。
- 旧OpenWebUI服务健康≠已有浏览器实际GUI会话成功；不能新开受保护浏览器，不对未授权UI做实验。
- 原生音频/视频和视觉tool事件、模型路由全场景独立质量、Hermes跨重启会话恢复、Windows冷启动、7-14天观察和五轮整站综合Reality未通过。
- 项目当前配置SHA历史值和F018实测值不同，CURRENT已保留两份哈希供差分，不要据此猜测配置出错；F013功能已实测通过。不可读取/打印配置敏感字段。

## 下节点选择
优先使用已有正式 `C:/Users/A/AppData/Local/hermes/bin/ltmvh-hermes-formal.ps1`（OpenRouter deepseek/deepseek-v4.1-flash），按任务合同选择一个尚未通过且有获准现实路径的自然能力Gate；先GOOD/BAD/FIRST_DELTA与成熟候选→Freeze→一次Reality→独立测试与完整T_VALID；失败回虚，KEEP/ABANDONED/NOT_APPLICABLE。若是GUI/凭据/网络受保护门无法合法操作，标记PENDING并优先可独立完成的其余Gate。不要重复已经PASS的F013/F014/F018简单任务。只对具有完全相同输入/质量/模型/条件的任务做真实时间对比，不为1秒改变架构。完成后持久化GitHub CURRENT并回读，任务状态必须可由下一页无缝接续。
