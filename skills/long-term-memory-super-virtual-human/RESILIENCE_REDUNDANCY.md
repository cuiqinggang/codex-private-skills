# 长期记忆超级虚拟人｜低相关冗余与韧性合同 v0.1

## 核心原则

关键能力不能只有单点。

```ini
CRITICAL_CAPABILITY_REDUNDANCY_REQUIRED=YES
MIN_MATURE_PATHS=2
LOW_CORRELATION_REQUIRED=YES
PRIMARY_OPTIMIZES=T_VALID
BACKUP_FIRST_GOAL=VALID_AND_RECOVERABLE
FAILOVER_BEFORE_REPAIR=YES
RESTORE_REDUNDANCY_AFTER_FAILOVER=YES
```

“低相关”不是简单复制同一个工具两份，而是尽量分离：
- 控制面；
- 认证方式；
- 传输链路；
- 运行身份/会话；
- 执行引擎；
- 供应商；
- 存储位置。

## 运行规则

```text
主路健康 → 走完整 T_VALID 最短路径
主路异常 → 不先长时间抢修
          → 立即切已验证备路完成任务
          → 业务恢复后再修主路
          → 同步补回第二条低相关冗余
```

备路允许更慢，但必须能完成同一个 FINAL_VALID。

## 当前关键能力冗余矩阵

| 关键能力 | 主路 | 低相关备路 | 当前状态 |
|---|---|---|---|
| GPT→Windows 文件/命令 | Desktop Commander Remote（A 用户会话） | GitHub Actions self-hosted runner（Windows 服务身份） | 双路 Reality 已有 |
| Windows GUI / 浏览器操作 | 原生 Connector/DOM/Playwright/Computer-use 类执行面 | virtual-mouse-keyboard / screenshot route / pywinauto 类成熟路径 | 按需 Reality |
| 代码工程 | GPT 直接工具/本地工具（适合时） | Codex / Reasonix 工程执行器 | 按任务竞争 |
| 长流程 | GPT + TASK_CONTRACT + Checkpoint | ECC v3.1.1 / Reasonix 集成路线 | ECC 成熟资产已验证 |
| 项目状态存储 | GitHub 共同私库 | K 盘本地 mirror + bundle + 快速 Skill 副本 | 本地 Reality 进行中 |
| GPT 服务故障 | GPT 主脑 | 独立 Reasonix/DeepSeek 等备脑 | 尚未完整认证 |

## Failover Gate

只有满足以下条件的备路才能计入“冗余”：
1. 不依赖主路同一个关键故障点；
2. 能真实完成最小代表任务；
3. 有明确启动入口；
4. 有机器可验证结果；
5. 定期做健康检查；
6. 故障切换不要求临时从零安装整套系统。

“配置文件存在”“曾经安装过”“理论可用”不能算成熟冗余。

## 人工边界

人工不是默认最后一步。

只有以下情况才请求用户：
- 目标/价值判断；
- 用户本人 MFA / 验证码 / 身份确认；
- 支付/新增费用；
- 账号安全设置；
- 不可逆高风险动作；
- 平台明确要求真人。

其他故障优先自动切成熟备路。

## 与极限短时间的关系

冗余不是第二优化目标。

```text
没有备路时：主路故障 → 无 VALID
有备路时：主路故障 → 较慢但仍产生 VALID
```

因此冗余属于 VALID 集合的韧性保障；在所有能达到 VALID 的候选内，仍只比较完整 T_VALID。
