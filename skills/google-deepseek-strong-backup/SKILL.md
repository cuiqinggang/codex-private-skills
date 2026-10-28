---
name: google-deepseek-strong-backup
description: "谷深双擎强备系统V1.6兼容接入层。在GPT、ChatGPT、Codex不可用时，用Windows现有DSH与按需Gemini承接AI化组织V4.2方法、DSH成熟能力包1.1.4及任务恢复；也用于核查旧V1.5.1验收与版本差异。"
---
# 谷深双擎强备系统 V1.6
版本：V1.6；2026-10-28。本版升级宿主接入，不修改冻结V4.2，也不把V1.5.1恢复候选晋升正式版。
当前发布范围与实测结果见[验收回执](references/ACCEPTANCE.json)；未生成或未通过时保持候选。

## 独立承接
在OpenAI/GPT/ChatGPT/Codex不可用时，用本机已安装DSH作为单一主执行者；Gemini网页按真实净收益提供规划或复核，不强制每题双模型。禁止把GPT工具、ChatGPT插件、账号授权或imagegen等能力当作DSH自动拥有。
首次先读[宿主绑定与能力边界](references/HOST-BINDING.md)，再用原生skill依次加载ai-organization-v4-2、dsh-extreme-effective-time、dsh-mature-capabilities和reuse-experience-brain。它们是完整原包，不是改名版本；已有宿主绑定冲突按本文件说明显式处理。

## 最短执行合同
1. 读任务N000/最新节点与已提交产物。新任务另建TASK_ID；恢复保持原TASK_ID、session-id和cwd，先核账再续未完成部分。
2. 根据真实输入定义交付物、质量、权限、成本和验收；固定T*=min(T_VALID)，所有检索、失败、复验、保存时间计入。未完整计时写NOT_MEASURED。
3. 从当前共同经验索引找相关1—3张卡；联网共同仓可读就读最新，无法访问时使用随包镜像并注明日期。无命中直接继续。历史经验不得覆盖当前状态。
4. 复用DSH成熟能力1.1.4和本地索引，只读当前目标的原技能/配方。保留成熟基线，至多三条可行路径；对输入→工具→成品→审核→异常→恢复做虚拟成熟，满足STOP_GATE后Freeze。
5. 用本机DSH原生工具完成一次整体Reality。普通故障在原合同内最小修复并继续；实质换路线重新冻结受影响部分。不要要求用户回到GPT，禁止依赖codex-cli-bridge执行。
6. 优先已有独立确定性校验；复杂内容才按净收益请Gemini审核。检查真实产物后交付。退出码0、模型DONE、文件存在均不足以认证业务通过。
7. 留最小回执：TASK_ID/NODE_ID、版本、来源与经验采用、技能/工具真实证据、产物路径、QA、时间、session-id/cwd、未完成项及唯一NEXT_ACTION。有新经验交原21点任务，不新建记忆系统。

## 直接使用
DSH已有安装时，使用原生 `/google-deepseek-strong-backup <实际任务>`，或调用本包scripts/run_backup.py。
完整安装、双击入口、恢复和Gemini手工交接见[使用指南](references/START-HERE.md)。
scripts/install_backup.py默认只检查，带--apply才把本包及两项完整原依赖安装到既有DSH Home；不安装运行时、不覆盖其他版本、不复制凭据。
本机安装已有DSH成熟能力必须为1.1.4、时间方法为1.0.1；不把两个版本混称。完整来源与文件哈希见references/SOURCE-MANIFEST.json。

## 恢复边界
复用reasonix-continuity、官方--session-id及原run_resumable.py。自动重试只适用该原工具允许的本地文件任务；外部写入UNKNOWN先只读对账，不盲重发、不换新ID。
原V1.5.1崩溃、计划任务、睡眠唤醒是限定恢复证据；本次读回真实重启回执仍缺失。断电、登录前恢复、多日无人值守及外部exactly-once仍未认证。
没有真实持久执行器接单，关闭窗口后不承诺继续运行。专业能力只按本次实际证据标PRESENT/LOADED/EXECUTED/ACCEPTED，不宣称完整复制GPT平台。
