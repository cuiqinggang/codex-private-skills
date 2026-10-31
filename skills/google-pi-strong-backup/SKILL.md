---
name: google-pi-strong-backup
description: "谷深双擎强备系统V2：Pi主执行、Google按需协作、DSH仅显式回退。用于Pi替换DSH强备、主系统不可用时独立接单、原生会话接续、Google规划复核、旧订单核账和同合同性能对照。"
---
# 谷深双擎强备系统 V2：Pi＋Google

时间锚：2026-10-31，Asia/Shanghai。组织方法沿《AI 自动化组织》V5；本包独立于旧DSH V1.6技能。本轮已完成限定范围默认切换。先读[当前验收与入口](references/acceptance.md)，以设备CURRENT、真实回执和哈希为准；不扩大为任意业务或多日无人值守认证。

## 唯一主执行者

默认使用本机已验收的Official Oh My Pi运行时及既有DeepSeek模型。Google Gemini只在规划或独立复核有需要时参与；不强制双模型。不得调用GPT、ChatGPT、Codex或Claude完成强备业务。不得隐瞒实际后台。

DSH不参加正常强备执行；保留旧`google-deepseek-strong-backup`原生技能、入口和证据供明确回退。不要把旧同名技能原位改成Pi说明，否则DSH原生加载会冲突。DSH目录内的确定性配方、独立校验器、权限组件可继续复用；它们不是DSH智能体运行。

## 本机入口

当前版本化宿主根：`C:\Users\A\Documents\DSH-Workspace\gsb-pi-google-v2-20261031`。
先执行该目录`run_backup.py --check`，仅证明依赖存在；DSH回退文件缺失不得阻断Pi。普通任务用`--task-file <文件> --cwd <原授权目录> --json --print`；恢复加`--session-id <原OMP会话>`；入口核对原目录内的OMP会话头，拒绝DSH会话、未知UUID和错cwd。本包`scripts/run_backup.py`是同一入口的转接，不能在非Windows环境假称已调用。

进入Windows用当前执行桥V13，D→A→B→C；Pi自己的本机工具不是这些远程通道。不要套旧技能的A优先说明。

只读业务使用官方OMP `--cwd`和原ACL运行器：仅独立运行元数据目录获得写能力，业务cwd不获得写能力；已实测写业务目录被拒绝。只读与写入会话各自在原元数据目录恢复，不复制私有会话或凭据。启动元数据不等于业务写入。`--mode`仅提供任务类别提示，Pi统一原生选路。

订单正式服务位于原订单workspace下`service-pi-v2`，原`deliver.cmd`已切换；版本根`order-service`仅为隔离测试副本，不用于旧订单。

## 执行合同

1. 先核对TASK_ID、输入/产物哈希、已确认步骤、提交状态和CURRENT；继承原共同经验索引及命中1—3张卡，不全库注入。
2. 按需加载AI自动化组织V5、成熟能力路由、时间方法、相关专业配方与经验。复用原配方、原生Skills/MCP、原continuity及独立校验器；不另建调度器、状态机、浏览器或记忆系统。
3. 冻结输入→工具→产物→独立验收→故障→恢复合同，完成虚拟成熟与STOP_GATE，再做相关整体Reality。普通故障最小修复并继续。
4. 本地文件用原工具与workspace-write/read-only边界；不放宽ACL，不读凭据，不改系统/网络/代理或他人会话。外部账号操作仍依本次明确授权。
5. 恢复保持原TASK_ID、cwd与OMP原生session；DSH session不能冒充OMP session。旧执行树未确认结束不得交接；UNKNOWN先只读核账，不盲重发。已确认成品不重新生成。
6. 订单跨版本必须沿用原workspace/jobs与continuity；隔离测试的新jobs目录不能直接替代生产任务账本。已提交请求先读原delivery.json并核验输入/成品哈希，再决定是否执行剩余步骤。
7. Google使用原正式shared_browser MCP与原登录身份。只操作自己的任务页；发送前核对唯一标记，未知提交先核账。核对真实助手回答、实际发送次数和页面所有权；输入回显、模型自报、合并文本命中不能证明协作成功。遇登录墙如实阻塞，不读取或迁移身份数据。
8. 优先独立确定性校验；退出码0、文件存在、模型DONE均不够。交付RESULT与最小恢复回执，记录TASK_ID、实际执行器、session/cwd、QA、产物哈希、已完成/剩余与唯一NEXT_ACTION。

## 验收与时间

固定质量、安全、正确性、成本、成功率与资源，优化完整T_VALID_E2E；包含失败、审核误判、修复、等待、恢复和读回。修正验收器时保留原回执，另记更正时间，不能把更正后的通过套回原耗时。SDK估算不是实际账单。

仅按[当前回执](references/acceptance.md)声明已验范围。本地原生进程恢复、确定性订单交接、浏览器现场恢复、整机重启、多日无人值守是不同范围。旧本地文件重启证据不能认证新浏览器或任意业务的自动续交付。订单服务模型自身中断若无原会话自动续接证据，保持有界停止与核账，不冒充全自动恢复。
