# ECC v3.1.1 网络权威入口与长任务检查点复用规则

VERSION=ECC_V3_1_1_SOURCE_INDEX_V2
STATUS=SOURCE_VERIFIED;RUNTIME_NOT_INTEGRATED_WITH_POLSIA
SOURCE_REPOSITORY=cuiqinggang/ecc-v3.1.1
SOURCE_REF=v3.1.1
SOURCE_BRANCH=main
SOURCE_RELEASE=https://github.com/cuiqinggang/ecc-v3.1.1/releases/tag/v3.1.1
SOURCE_README=https://github.com/cuiqinggang/ecc-v3.1.1/blob/v3.1.1/README.md
SOURCE_README_BLOB=37b3e2ae9ca603ad059065b4d6c422cffab8463f
SOURCE_ATOMIC_STATE=https://github.com/cuiqinggang/ecc-v3.1.1/blob/v3.1.1/loopx/contract.py
SOURCE_ATOMIC_STATE_BLOB=849ab969b1a0f8b43535c6af07ca125091eb879a
CURRENT_FORMAL_ENGINE=skills/artificial-single-page-extreme-time-engine/ENGINE.md@28
SANRENXING_CANDIDATE=skills/artificial-single-page-extreme-time-engine/SANRENXING_V1_ENGINE30_DRAFT.md
PUBLIC_METHOD_PROMOTION=NO

## 核验事实
经已连接的GitHub官方连接器从已授权账户实际发现独立仓库 cuiqinggang/ecc-v3.1.1。Release v3.1.1 公开正式发布（2026-09-10），包含 ecc-v3.1-portable.zip（发布资产 SHA-256: f72c0a5318f04ed3d39478d10caced4c0ea9123c23fe5207a25f92f6d89c1537）及 ecc-v3.1-reasonix-integrated.zip（发布资产 SHA-256: ab32a1452a39fd04c62e11b79ee2fb6a2c091b08e597b9b67270c0422870a9af）。本次核验的是GitHub版本/发布元数据与源码内容；没有重新下载并校验zip原始字节，也没有在Polsia现场运行ECC，因此不可称该生产任务ECC已集成PASS。
该工程 README 内部标题仍写「ECC V3.1」，但发布标签、仓库名和Release明确为 v3.1.1；运行规则应读取v3.1.1固定tag，不能只以本地旧ecc-four-role-loop-orchestration V2.1.0 或旧 ecc-v3.1-production 的文字代替最新发布。

## 现成能力（直接来自仓库）
- loopx/contract.py：LOOP-CONTRACT.json / STATE.json / RUN-LOG.jsonl；STATE采用临时文件写入→fsync→读回→os.replace 原子更新；RUN-LOG只追加、每行fsync。证据为正式源码，指向程序级任务循环状态。
- loopx/engine.py、handoff.py：goal/scheduled/event/hybrid四种循环模式；CLOSED/WAITING/REPAIR/ECC_REQUIRED/HUMAN_REQUIRED/BLOCKED六态；GPT/ECC交接时返回四态，明确成功标准、游标、失败证据、下一动作。
- lease.py：租约所有权、跨进程锁、单调 fencing token、write_guard、失联接管；禁止双写。租约心跳示例默认30秒，但不得把心跳误当用户界面刷新或真实保存点。
- runners/codex_runner.py：原生Codex CLI调用、JSONL运行事件、退出码、限时/取消处理、日志脱敏。真实运行默认live=False，只有经过授权与配置确认才允许live=True；不得在未核实前接管现有Codex进程。
- scripts/fresh_resume.py：冷恢复测试，原文件三件套跨进程恢复。scripts/endurance60.py：60分钟耐力脚本示例，默认每10轮检查点、5分钟审计点、30秒租约心跳。检查点频率由工作量与写盘净成本决定，**不等于每10分钟/每10节点**。
- 版本发布随附便携版和可选Reasonix集成版；不能由存在发布包直接推断在某台Windows上已安装、验证通过或支持真实断电期间运算。

## 三人行/Polsia的正确复用边界
A. **节点Freeze**：一个自然工作节点完成，版本 V001→V002→V003... 不可变；提交GitHub后通过正式Contents API读取SHA，再更新动态CURRENT。不可删除旧节点Freeze审计。
B. **同节点Checkpoint**：任务仍在运行时保存最近可恢复的STATE/游标/实际完成清单/必要运行回执，不增加节点版本，不更换页面。优先用ECC内置原子状态写入；重写新检查点前保留上一个有效检查点到新数据验证成功；可仅保留最近1个有效状态与必要回退，**绝不删除RUN-LOG或未审计的原始外部操作回执**。
C. **触发时机**：重要里程碑、外部有副作用动作的回执、上下文压缩前、合适的周期；初始周期可以15分钟作为待验证默认值，按真实每次checkpoint耗时、丢失风险、日志事件量动态调整。不得按时间机械Freeze或全量复制大文件。
D. **断电/退出后恢复**：电脑关机时不执行，重启只依据最后落盘且校验通过的STATE/Freeze + 外部动作完成三态DONE/NOT_DONE/UNKNOWN作接续；UNKNOWN不可盲重发。原生Windows计划任务可触发但不替代ECC实际状态/租约验收。
E. **GPT重规划**：Codex同类错误重复、阻塞、未决执行结果或本机指针不一致时，先让GPT核实真正最后有效状态和工具回执，分辨正常退出与故障，修正授权范围内的NEXT；不得因为找不到CLI PID就断言业务失败。
F. **72小时**：这是连续运行能力的未来现实耐力验收目标而非自动停止时间；要求真实连续进度、Checkpoint、跨节点Freeze、恢复与资源耗时证据。72h到期不等于母任务DONE。

## 写入位置与版本
- GitHub共同工作区存方法索引、节点正式Freeze、CURRENT版本指针、不可变证据摘要及其SHA。
- Windows本机只承载大型MP4/实际工具日志、Codex真实执行状态与ECC运行态文件，必要时按GitHub的Freeze引用作校验；GitHub不是运行中的每秒日志数据库，也不是网站已上线的证明。
- 每次方法变更正常使用GitHub官方update_file（fetch当前SHA→update→fetch回读），历史版本由commit和不可变Freeze追溯。尚未验证的网站必须按成熟平台的部署流程验收，不能把GitHub上传当成公网功能就绪。


## ECC 默认版本锁定（2026-10-15）

- 用户指定当前默认正式版本：**ECC V3.1.1**；“ECC”“ECC最新版”“ECC 3.11”均指此版本。V2.1.0只作历史基线，禁止作为默认版本或读取失败时的替代品。
- 统一入口：`skills/artificial-single-page-extreme-time-engine/ECC_V3_1_1_NETWORK_AUTHORITY.md`。
- 正式源码：`cuiqinggang/ecc-v3.1.1`，tag `v3.1.1`，固定提交 `b9e651bc6c6751bff43db30b80d9cab983a7c412`。
- 发布：https://github.com/cuiqinggang/ecc-v3.1.1/releases/tag/v3.1.1
- 正文：https://github.com/cuiqinggang/ecc-v3.1.1/blob/b9e651bc6c6751bff43db30b80d9cab983a7c412/README.md
- README标题“V3.1”和发布包名“ecc-v3.1”属于该发布的原始命名，不能据此降级为V2.1.0。
- 已安装或云端目录若返回 `ecc-four-role-loop-orchestration V2.1.0`，必须标记历史副本并转读上述入口；不得把旧正文改个版本号冒充新版。新版不可读取时报告版本读取阻塞，不静默回退。
- 只在用户明确查询历史或旧任务锁定旧版本时读取V2.1.0；不删除旧冻结，不自动迁移正在运行的任务。后续升级须明确更新此默认指针。
- 本次核实发布、tag提交和README来源，不宣称本机部署、性能、长任务或恢复测试已通过。
